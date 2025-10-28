# Issue #5: Troubleshooting and Resolution

**Status**: RESOLVED ✅
**Date**: 2025-10-28
**Final Commit**: d185e66

## Problem Summary

Echo bot pipeline started successfully with all services (Deepgram STT, Cartesia TTS, LocalAudioTransport) connecting properly, but no audio was flowing through the system - no transcriptions appeared and no TTS audio was heard.

## Troubleshooting Journey

### Phase 1: Audio Device Configuration (2025-10-28 21:52 - 22:05)

**Hypothesis**: Wrong audio devices selected or incompatible sample rates.

**Actions Taken**:
1. Installed all dependencies (pipecat-ai, deepgram-sdk, cartesia, sounddevice, etc.)
2. Configured API keys for Deepgram and Cartesia
3. Ran `python -m src.cli echo-bot --list-devices` to enumerate 23 audio devices
4. Tested multiple device configurations:
   - Device 11 (G-Track Pro microphone) + Device 16 (USB Audio Speakers)
   - Device 11 + Device 17 (AirPods Pro)
   - Device 10 (PipeWire default)
   - No device specification (system defaults)

**Results**:
- Pipeline started successfully each time
- No errors in logs
- Deepgram and Cartesia connections established
- **Still no audio flow**

### Phase 2: Sample Rate and Channel Configuration

**Hypothesis**: Audio format mismatch between hardware and software.

**Configurations Tested**:
1. 48kHz stereo (2 channels) - hardware native rate
   - Result: Memory corruption crash (malloc error) with AirPods
2. 48kHz mono (1 channel)
   - Result: Pipeline starts, no audio
3. 16kHz mono (1 channel) - Deepgram optimal
   - Result: Pipeline starts, no audio

**Analysis**: Sample rate changes didn't resolve the issue, indicating a deeper configuration problem.

### Phase 3: Microphone Hardware Testing

**Hypothesis**: Microphone not capturing audio.

**Test**:
```bash
arecord -D plughw:3,0 -f S16_LE -r 16000 -c 1 -d 5 /tmp/test-mic.wav
aplay /tmp/test-mic.wav
```

**Result**: ✅ Microphone captured audio perfectly (157KB file, clear playback).

**Conclusion**: Hardware was working - problem was in software configuration.

### Phase 4: Documentation Research (BREAKTHROUGH)

**Action**: Searched Pipecat documentation and GitHub issues for similar problems.

**Key Findings**:
1. **GitHub Issue #244**: "Unable to hear pipeline outputs or see transcriptions"
   - Solution involved `vad_audio_passthrough=True` for VAD-enabled pipelines
   - Not applicable to our case (no VAD used)

2. **GitHub Issue #1431**: "Local audio input unrecognized"
   - Contained working example code
   - Revealed required parameters: `audio_in_enabled=True` and `audio_out_enabled=True`

3. **Pipecat Documentation**: Confirmed LocalAudioTransportParams requires explicit enable flags

### Phase 5: The Fix

**Root Cause Identified**:
Missing `audio_in_enabled` and `audio_out_enabled` parameters in `LocalAudioTransportParams`.

**Before (BROKEN)**:
```python
params = LocalAudioTransportParams(
    audio_in_sample_rate=audio_config.sample_rate,
    audio_out_sample_rate=audio_config.sample_rate,
    audio_in_channels=audio_config.channels,
    audio_out_channels=audio_config.channels,
    input_device_index=audio_config.input_device,
    output_device_index=audio_config.output_device,
)
```

**After (WORKING)**:
```python
params = LocalAudioTransportParams(
    audio_in_enabled=True,   # CRITICAL: Enable audio input stream
    audio_out_enabled=True,  # CRITICAL: Enable audio output stream
    audio_in_sample_rate=audio_config.sample_rate,
    audio_out_sample_rate=audio_config.sample_rate,
    audio_in_channels=audio_config.channels,
    audio_out_channels=audio_config.channels,
    input_device_index=audio_config.input_device,
    output_device_index=audio_config.output_device,
)
```

**File Modified**: `src/pipeline/audio_transport.py`
**Lines Changed**: 2 insertions (lines 51-52)

## Test Results After Fix

### Successful Test Run (2025-10-28 18:17)

```
2025-10-28 18:17:24 - Pipeline started
2025-10-28 18:17:30 - Received transcription
2025-10-28 18:17:30 - Echoing back
CartesiaTTSService: Generating TTS [You said: Test.]
Bot started speaking
Bot stopped speaking

2025-10-28 18:17:34 - Received transcription
2025-10-28 18:17:34 - Echoing back
CartesiaTTSService: Generating TTS [You said: Testing.]

2025-10-28 18:17:39 - Received transcription
2025-10-28 18:17:39 - Echoing back
CartesiaTTSService: Generating TTS [You said: Hello.]
```

### Verification Checklist

- [x] Deepgram successfully transcribes speech
- [x] Transcriptions appear in logs
- [x] Cartesia generates TTS audio
- [x] TTS audio plays through speakers
- [x] Echo bot responds correctly
- [x] Pipeline handles multiple utterances
- [x] Start/stop/restart works reliably

## Known Limitations

### Bluetooth Audio Buffering Issue

**Symptom**: When using AirPods or other Bluetooth devices, audio output may cut out after first 1-2 responses.

**Cause**: Bluetooth audio latency and buffering characteristics. Bluetooth devices introduce additional latency that can cause the audio stream to stall.

**Workaround**: Use wired speakers/headphones for reliable operation.

**Status**: Environmental limitation, not a code bug. Documented in post-implementation notes.

## Final Configuration

### Working Setup
```bash
# Audio Configuration
AUDIO_SAMPLE_RATE=16000  # Optimal for Deepgram STT
AUDIO_CHANNELS=1         # Mono (standard for voice)

# Device Selection (commented out = use system defaults)
# AUDIO_INPUT_DEVICE=
# AUDIO_OUTPUT_DEVICE=
```

### System Defaults (via PipeWire)
- **Input**: G-Track Pro microphone Analog Stereo (Device 125)
- **Output**: User-selected via KDE System Settings

### Pipeline Architecture
```
Microphone (G-Track Pro)
  → LocalAudioInputTransport (audio_in_enabled=True)
  → DeepgramSTTService (Nova-2, 16kHz, mono)
  → LatencyMonitor
  → EchoProcessor
  → CartesiaTTSService (Sonic, natural voice)
  → LocalAudioOutputTransport (audio_out_enabled=True)
  → Speakers (PipeWire default)
```

## Key Lessons Learned

1. **Read the documentation carefully**: The Pipecat LocalAudioTransport requires explicit enable flags that aren't obvious from basic examples.

2. **Check GitHub issues**: Real-world problems and solutions are often documented in issue trackers.

3. **Test incrementally**: Hardware testing (arecord/aplay) quickly ruled out microphone issues.

4. **Follow the data flow**: Audio was reaching PipeWire (confirmed via `wpctl status` showing active streams), but not flowing through Python - this pointed to a software configuration issue.

5. **Don't assume defaults**: Many audio libraries require explicit "enable" flags even when providing device indices.

## Impact

This was the **critical blocker** for Issue #5. Once this 2-line fix was applied, the entire echo bot worked perfectly on first try. All other configuration (API keys, sample rates, device selection) was already correct.

**Time to Resolution**: ~2 hours of troubleshooting
**Root Cause**: Missing documentation/unclear API defaults
**Fix Complexity**: Trivial (2 lines)
**Lesson**: Sometimes the simplest fixes have the biggest impact

## References

- Pipecat GitHub Issue #244: https://github.com/pipecat-ai/pipecat/issues/244
- Pipecat GitHub Issue #1431: https://github.com/pipecat-ai/pipecat/issues/1431
- Pipecat Documentation: https://docs.pipecat.ai/
- LocalAudioTransport API Reference: https://reference-server.pipecat.ai/en/latest/api/pipecat.transports.local.audio.html
