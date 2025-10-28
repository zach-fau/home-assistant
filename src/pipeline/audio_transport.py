"""Audio I/O transport configuration for Pipecat pipeline.

This module provides configured audio transport using Pipecat's LocalAudioTransport
for handling microphone input and speaker output.
"""

import sys
from typing import Optional

try:
    from pipecat.transports.local.audio import (
        LocalAudioTransport,
        LocalAudioTransportParams,
    )
except ImportError:
    print("Error: pipecat-ai[local] is not installed.", file=sys.stderr)
    print("Please install with: pip install 'pipecat-ai[local]'", file=sys.stderr)
    sys.exit(1)

from src.config import AudioConfig
from src.logger import get_logger

logger = get_logger(__name__)


def create_local_audio_transport(
    audio_config: AudioConfig,
) -> LocalAudioTransport:
    """Create and configure a local audio transport for microphone/speaker I/O.

    Args:
        audio_config: Audio configuration from application config

    Returns:
        Configured LocalAudioTransport instance

    Raises:
        RuntimeError: If audio transport initialization fails
    """
    logger.info(
        "Creating local audio transport",
        sample_rate=audio_config.sample_rate,
        channels=audio_config.channels,
        input_device=audio_config.input_device,
        output_device=audio_config.output_device,
    )

    try:
        # Create transport parameters
        params = LocalAudioTransportParams(
            audio_in_sample_rate=audio_config.sample_rate,
            audio_out_sample_rate=audio_config.sample_rate,
            audio_in_channels=audio_config.channels,
            audio_out_channels=audio_config.channels,
            input_device_index=audio_config.input_device,
            output_device_index=audio_config.output_device,
        )

        # Create transport
        transport = LocalAudioTransport(params=params)

        logger.info("Local audio transport created successfully")
        return transport

    except Exception as e:
        logger.exception(f"Failed to create audio transport: {e}")
        raise RuntimeError(f"Audio transport initialization failed: {e}") from e


def list_audio_devices():
    """List available audio input and output devices.

    This is useful for debugging and device selection.
    """
    try:
        import pyaudio

        logger.info("Listing available audio devices")
        p = pyaudio.PyAudio()

        print("\n=== Available Audio Devices ===")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(f"\nDevice {i}: {info['name']}")
            print(f"  Max Input Channels: {info['maxInputChannels']}")
            print(f"  Max Output Channels: {info['maxOutputChannels']}")
            print(f"  Default Sample Rate: {info['defaultSampleRate']}")

        p.terminate()

    except ImportError:
        logger.error("PyAudio is not installed. Cannot list audio devices.")
        print("Error: PyAudio is not installed.", file=sys.stderr)
    except Exception as e:
        logger.exception(f"Failed to list audio devices: {e}")
        print(f"Error listing audio devices: {e}", file=sys.stderr)
