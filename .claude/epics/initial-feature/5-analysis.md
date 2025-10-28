---
issue: 5
title: Core Pipecat Pipeline with STT and TTS
analyzed: 2025-10-28T21:35:00Z
complexity: medium
estimated_hours: 8-12
---

# Work Stream Analysis: Issue #5

## Overview
Implement the core conversation pipeline using Pipecat framework, integrating Deepgram for speech-to-text and Cartesia Sonic for text-to-speech. Build an "echo bot" to validate the complete audio processing pipeline.

## Work Stream: Pipecat Pipeline Implementation

**Type**: Sequential (single agent)
**Estimated Time**: 8-12 hours
**Agent Type**: general-purpose

### Scope
Build the complete conversation pipeline with:
1. Pipecat framework setup and configuration
2. Audio I/O transport (microphone and speakers)
3. Deepgram WebSocket integration for streaming STT
4. Cartesia Sonic TTS integration
5. Echo bot logic (listen → transcribe → speak back)
6. Latency measurement and logging
7. Graceful interruption handling

### Files to Create/Modify
```
src/
├── pipeline/
│   ├── __init__.py
│   ├── audio_transport.py    # Audio I/O handling
│   ├── deepgram_stt.py       # Deepgram integration
│   ├── cartesia_tts.py       # Cartesia TTS integration
│   └── echo_bot.py           # Main pipeline orchestration
├── cli.py                     # Update to add echo-bot command
└── config.py                  # Update with audio/pipeline config

requirements.txt               # Add audio dependencies
```

### Implementation Steps

1. **Pipecat Setup** (2 hours)
   - Install Pipecat and audio dependencies
   - Configure audio transport for microphone/speaker I/O
   - Set up basic pipeline structure
   - Test audio input/output

2. **Deepgram STT Integration** (3 hours)
   - Create Deepgram client with WebSocket
   - Configure Nova-2 model for best accuracy
   - Enable interim results for low latency
   - Implement streaming transcription processor
   - Test STT with sample audio

3. **Cartesia TTS Integration** (3 hours)
   - Create Cartesia Sonic client
   - Select natural-sounding voice
   - Implement TTS processor in pipeline
   - Handle audio format conversions
   - Test TTS output quality

4. **Echo Bot Pipeline** (2 hours)
   - Wire up complete pipeline flow
   - Implement echo logic (transcription → TTS)
   - Add conversation state management
   - Handle interruptions and barge-in
   - Implement graceful shutdown

5. **Latency & Testing** (2 hours)
   - Add latency measurements
   - Log STT and TTS timings
   - Test end-to-end (target < 2 seconds)
   - Test interruption handling
   - Verify restart reliability

### Dependencies
Additional packages needed:
- pipecat-ai (already in requirements)
- deepgram-sdk (for Deepgram API)
- cartesia-python (for Cartesia API)
- pyaudio or sounddevice (for audio I/O)
- numpy (for audio processing)

### Acceptance Criteria
- Pipecat pipeline runs and processes audio
- Deepgram accurately transcribes speech (>95%)
- Cartesia produces natural-sounding speech
- Audio I/O works with microphone/speakers
- Echo bot successfully repeats what user says
- Interruptions handled gracefully
- Latency measured and logged
- Pipeline restarts reliably

### Testing Strategy
- Manual testing with microphone input
- Test various phrases and accents
- Measure end-to-end latency
- Test interruption scenarios
- Verify WebSocket cleanup on shutdown

### Success Metrics
- STT latency < 500ms
- TTS latency < 300ms to first audio
- End-to-end < 2 seconds
- Clean startup and shutdown
- No memory leaks during continuous operation

## Coordination Notes
- **Depends on**: Issue #4 (Project Foundation) - COMPLETED ✓
- **Blocks**: Issue #6 (LLM Integration)
- **No Conflicts**: Sequential implementation, single stream
- **Critical**: This establishes the audio pipeline for all future work
