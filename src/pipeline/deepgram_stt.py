"""Deepgram Speech-to-Text integration for Pipecat pipeline.

This module provides configured Deepgram STT service using Nova-2 model
for accurate, low-latency speech recognition with streaming support.
"""

import sys
from typing import Optional

try:
    from pipecat.services.deepgram import DeepgramSTTService
except ImportError:
    print("Error: pipecat-ai[deepgram] is not installed.", file=sys.stderr)
    print("Please install with: pip install 'pipecat-ai[deepgram]'", file=sys.stderr)
    sys.exit(1)

from src.config import PipelineConfig, APIKeys
from src.logger import get_logger

logger = get_logger(__name__)


def create_deepgram_stt_service(
    api_keys: APIKeys,
    pipeline_config: PipelineConfig,
) -> DeepgramSTTService:
    """Create and configure Deepgram STT service.

    This uses Deepgram's Nova-2 model which provides:
    - Best accuracy for general transcription
    - Low latency streaming
    - Support for interim results
    - Automatic punctuation and formatting

    Args:
        api_keys: API keys configuration containing Deepgram key
        pipeline_config: Pipeline configuration with STT settings

    Returns:
        Configured DeepgramSTTService instance

    Raises:
        RuntimeError: If STT service initialization fails
    """
    logger.info(
        "Creating Deepgram STT service",
        model=pipeline_config.stt_model,
        language=pipeline_config.stt_language,
        interim_results=pipeline_config.stt_interim_results,
    )

    try:
        # Create Deepgram STT service with configuration
        stt_service = DeepgramSTTService(
            api_key=api_keys.deepgram_api_key,
            model=pipeline_config.stt_model,
            language=pipeline_config.stt_language,
            interim_results=pipeline_config.stt_interim_results,
        )

        logger.info("Deepgram STT service created successfully")
        return stt_service

    except Exception as e:
        logger.exception(f"Failed to create Deepgram STT service: {e}")
        raise RuntimeError(f"Deepgram STT initialization failed: {e}") from e


def get_supported_models() -> list[str]:
    """Get list of supported Deepgram models.

    Returns:
        List of model names supported by Deepgram
    """
    return [
        "nova-2",  # Best overall accuracy and performance
        "nova",    # Previous generation, still good
        "enhanced",  # Enhanced model for specific use cases
        "base",    # Base model for basic transcription
    ]


def get_supported_languages() -> list[str]:
    """Get list of commonly supported languages.

    Returns:
        List of language codes supported by Deepgram
    """
    return [
        "en-US",  # English (US)
        "en-GB",  # English (UK)
        "en-AU",  # English (Australia)
        "en-NZ",  # English (New Zealand)
        "en-IN",  # English (India)
        "es",     # Spanish
        "fr",     # French
        "de",     # German
        "it",     # Italian
        "pt",     # Portuguese
        "nl",     # Dutch
        "ja",     # Japanese
        "ko",     # Korean
        "zh",     # Chinese
    ]
