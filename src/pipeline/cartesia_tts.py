"""Cartesia Text-to-Speech integration for Pipecat pipeline.

This module provides configured Cartesia TTS service using Sonic model
for natural-sounding, low-latency speech synthesis with streaming support.
"""

import sys
from typing import Optional

try:
    from pipecat.services.cartesia import CartesiaTTSService
except ImportError:
    print("Error: pipecat-ai[cartesia] is not installed.", file=sys.stderr)
    print("Please install with: pip install 'pipecat-ai[cartesia]'", file=sys.stderr)
    sys.exit(1)

from src.config import PipelineConfig, APIKeys
from src.logger import get_logger

logger = get_logger(__name__)


def create_cartesia_tts_service(
    api_keys: APIKeys,
    pipeline_config: PipelineConfig,
) -> CartesiaTTSService:
    """Create and configure Cartesia TTS service.

    This uses Cartesia's Sonic model which provides:
    - Natural-sounding voice synthesis
    - Low latency streaming output
    - Multiple voice options
    - Emotion and tone control

    Args:
        api_keys: API keys configuration containing Cartesia key
        pipeline_config: Pipeline configuration with TTS settings

    Returns:
        Configured CartesiaTTSService instance

    Raises:
        RuntimeError: If TTS service initialization fails
    """
    logger.info(
        "Creating Cartesia TTS service",
        model=pipeline_config.tts_model,
        voice=pipeline_config.tts_voice,
    )

    try:
        # Create Cartesia TTS service with configuration
        tts_service = CartesiaTTSService(
            api_key=api_keys.cartesia_api_key,
            voice_id=pipeline_config.tts_voice,
            model_id=pipeline_config.tts_model,
        )

        logger.info("Cartesia TTS service created successfully")
        return tts_service

    except Exception as e:
        logger.exception(f"Failed to create Cartesia TTS service: {e}")
        raise RuntimeError(f"Cartesia TTS initialization failed: {e}") from e


def get_supported_models() -> list[str]:
    """Get list of supported Cartesia models.

    Returns:
        List of model names supported by Cartesia
    """
    return [
        "sonic-english",  # English optimized model
        "sonic-multilingual",  # Multilingual support
    ]


def get_popular_voices() -> dict[str, str]:
    """Get popular Cartesia voice IDs with descriptions.

    Returns:
        Dictionary mapping voice names to their IDs
    """
    return {
        "Barbershop Man": "79a125e8-cd45-4c13-8a67-188112f4dd22",
        "British Lady": "79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e",
        "Midwestern Woman": "71a7ad14-091c-4e8e-a314-022ece01c121",
        "Reading Lady": "e13cae5c-ec59-4f71-b0a6-266df3c9e41a",
        "Friendly Sidekick": "95856005-0332-41b0-935f-352e296aa0df",
        "Calm Woman": "a0e99841-438c-4a64-b679-ae501e7d6091",
        "Professional Man": "fb26447f-308b-471e-8b00-8e9f04284eb5",
        "Conversational Lady": "156fb8d2-335b-4950-9cb3-a2d33befec77",
        "Helpful Woman": "820a3788-2b37-4d21-847a-b65d8a68c99a",
        "Child": "9eabb40b-1bc9-4d99-8310-8f3c5c336252",
    }


def list_voice_options():
    """Print available voice options for user selection."""
    voices = get_popular_voices()
    models = get_supported_models()

    print("\n=== Cartesia TTS Configuration ===")
    print("\nSupported Models:")
    for model in models:
        print(f"  - {model}")

    print("\nPopular Voices:")
    for name, voice_id in voices.items():
        print(f"  - {name}: {voice_id}")

    print("\nTo use a different voice, set TTS_VOICE in your .env file")
    print("Visit https://docs.cartesia.ai for more voice options")
