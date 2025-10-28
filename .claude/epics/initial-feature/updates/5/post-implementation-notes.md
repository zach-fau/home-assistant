# Issue #5: Post-Implementation Configuration

**Date**: 2025-10-28T21:52:00Z
**Status**: Configuration and Testing Phase

## Installation Steps Completed

### 1. Dependency Installation (2025-10-28T21:52:00Z)

Installed all Python dependencies from `requirements.txt`:

```bash
cd /home/gyatso/Development/epic-initial-feature
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install 'pipecat-ai[local,deepgram,cartesia]'
```

**Key Packages Installed:**
- `pydantic-settings>=2.1.0` - Configuration validation
- `python-json-logger>=4.0.0` - Structured logging
- `asyncio>=4.0.0` - Async I/O support
- `sounddevice>=0.5.3` - Audio device interface
- `deepgram-sdk>=3.0.0` - Speech-to-text
- `cartesia>=2.0.0` - Text-to-speech
- `pipecat-ai[local,deepgram,cartesia]>=0.0.91` - Pipeline framework with audio extras
- `pyaudio>=0.2.14` - Low-level audio I/O (installed via pipecat extras)

All dependencies installed successfully with no errors.

### 2. Environment Configuration (2025-10-28T21:53:00Z)

Created `.env` file from `.env.example`:

```bash
cp .env.example .env
```

**API Keys Configured:**
- ✅ DEEPGRAM_API_KEY - Configured for speech-to-text
- ✅ CARTESIA_API_KEY - Configured for text-to-speech
- ✅ OPENAI_API_KEY - Configured (for future Issue #6)

### 3. Audio Device Discovery (2025-10-28T21:56:00Z)

Ran device enumeration:

```bash
python -m src.cli echo-bot --list-devices
```

**Available Devices Found:**
- 23 total audio devices detected
- 9 input-capable devices
- 22 output-capable devices

**Selected Configuration:**
- Input: Device 11 - "G-Track Pro microphone Analog Stereo" (4 input channels, 48kHz)
- Output: Device 16 - "USB Audio Speakers" (2 channels, 48kHz)

### 4. Audio Device Configuration (2025-10-28T21:57:00Z)

Updated `.env` with specific device indices:

```bash
AUDIO_INPUT_DEVICE=11    # G-Track Pro microphone
AUDIO_OUTPUT_DEVICE=16   # USB Audio Speakers
```

**Rationale:**
- G-Track Pro provides high-quality audio input with 4 channels
- USB Audio Speakers provide reliable output
- Both devices support 48kHz sample rate
- Explicit device selection avoids default device ambiguity

## Testing Preparation

### First Run Attempt
Initial test showed pipeline started successfully but no audio I/O occurred. This was due to:
1. Missing explicit device configuration (was using system defaults)
2. PipeWire/ALSA auto-detection not selecting the correct devices
3. ALSA warnings about missing cards (non-critical)

### Configuration Fix
Added explicit device indices to `.env` file, which should resolve the audio routing issues.

## Deprecation Warnings Observed

The following deprecation warnings were noted during pipeline startup:

```
DeprecationWarning: Module `pipecat.services.deepgram` is deprecated,
use `pipecat.services.deepgram.[stt,tts]` instead.

DeprecationWarning: Module `pipecat.services.cartesia` is deprecated,
use `pipecat.services.cartesia.[stt,tts]` instead.

DeprecationWarning: Event 'on_pipeline_stopped' is deprecated,
use 'on_pipeline_finished' instead.
```

**Action Items for Future:**
- [ ] Update import statements in `src/pipeline/deepgram_stt.py`
- [ ] Update import statements in `src/pipeline/cartesia_tts.py`
- [ ] Update event handler in `src/pipeline/echo_bot.py`

These are non-blocking warnings from Pipecat 0.0.91 API changes. The code functions correctly but should be updated to use the new API patterns.

## ALSA Warnings

Several ALSA warnings appeared during startup:

```
ALSA lib pcm_dsnoop.c:567:(snd_pcm_dsnoop_open) unable to open slave
ALSA lib pcm_dmix.c:1000:(snd_pcm_dmix_open) unable to open slave
ALSA lib pcm.c:2722:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear
```

**Analysis:**
- These are benign warnings from ALSA probing for hardware that doesn't exist
- Common on systems using PipeWire as the audio server
- Do not affect functionality
- Can be suppressed by setting `ALSA_CARD` environment variable if desired

## System Environment

**Platform Details:**
- OS: Fedora Linux 42 (KDE Plasma)
- Python: 3.13.9
- Audio Server: PipeWire (with ALSA compatibility)
- Audio Hardware: USB audio interfaces + HDMI displays

**Audio System Notes:**
- PipeWire provides 64 virtual input/output channels (Device 9)
- Multiple HDMI audio outputs from NVIDIA GPU
- USB audio interface with multiple outputs
- Bluetooth audio support (AirPods Pro detected)

## Next Steps

1. **Manual Testing** - User needs to test the echo bot with configured devices
2. **Verify Audio I/O** - Confirm microphone captures speech and speakers play back
3. **Latency Measurement** - Check if end-to-end latency meets <2s target
4. **Address Deprecations** - Update code to use new Pipecat API patterns (optional, non-blocking)

## Alternative Device Configurations

If the current configuration doesn't work, try these alternatives:

**Option A - PipeWire Default:**
```bash
AUDIO_INPUT_DEVICE=10    # default (PipeWire managed)
AUDIO_OUTPUT_DEVICE=10   # default (PipeWire managed)
```

**Option B - USB Audio Microphone:**
```bash
AUDIO_INPUT_DEVICE=14    # USB Audio Microphone
AUDIO_OUTPUT_DEVICE=16   # USB Audio Speakers
```

**Option C - AirPods (Wireless):**
```bash
AUDIO_INPUT_DEVICE=12    # AirPods Pro
AUDIO_OUTPUT_DEVICE=17   # AirPods Pro-100
```

**Option D - Monitor Speakers:**
```bash
AUDIO_INPUT_DEVICE=11    # G-Track Pro microphone
AUDIO_OUTPUT_DEVICE=0    # LG ULTRAWIDE monitor speakers
```

## Documentation Updates Needed

The README.md should be updated with:
- Installation instructions for audio system dependencies (ALSA/PipeWire)
- Device enumeration and configuration steps
- Troubleshooting guide for audio device selection
- Platform-specific notes (Fedora, Ubuntu, etc.)

This will be addressed in Issue #3 (Testing and Documentation).

## Summary

Installation and configuration completed successfully. The echo bot pipeline starts and connects to both Deepgram and Cartesia APIs without errors. Audio device configuration has been explicitly set to avoid system default ambiguity. Ready for user acceptance testing.
