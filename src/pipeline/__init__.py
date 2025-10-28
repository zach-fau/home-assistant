"""Voice processing pipeline using Pipecat framework.

This package contains the core voice processing pipeline components:
- audio_transport: Audio I/O handling for microphone and speaker
- deepgram_stt: Speech-to-text using Deepgram Nova-2
- cartesia_tts: Text-to-speech using Cartesia Sonic
- echo_bot: Echo bot pipeline orchestration
"""

__all__ = [
    "audio_transport",
    "deepgram_stt",
    "cartesia_tts",
    "echo_bot",
]
