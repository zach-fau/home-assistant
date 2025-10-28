"""Configuration management for Home Voice Assistant.

This module handles loading and validating configuration from environment variables
using Pydantic models. It ensures all required API keys and settings are present
before the application starts.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIKeys(BaseSettings):
    """API keys for external services."""

    deepgram_api_key: str = Field(
        ...,
        description="Deepgram API key for speech-to-text",
        alias="DEEPGRAM_API_KEY"
    )
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key for language model",
        alias="OPENAI_API_KEY"
    )
    cartesia_api_key: str = Field(
        ...,
        description="Cartesia API key for text-to-speech",
        alias="CARTESIA_API_KEY"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class HomeAssistantConfig(BaseSettings):
    """Home Assistant connection settings."""

    url: str = Field(
        default="http://localhost:8123",
        description="Home Assistant instance URL",
        alias="HOME_ASSISTANT_URL"
    )
    token: str = Field(
        ...,
        description="Home Assistant long-lived access token",
        alias="HOME_ASSISTANT_TOKEN"
    )
    verify_ssl: bool = Field(
        default=True,
        description="Whether to verify SSL certificates",
        alias="HOME_ASSISTANT_VERIFY_SSL"
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Ensure URL doesn't end with a trailing slash."""
        return v.rstrip("/")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class LoggingConfig(BaseSettings):
    """Logging configuration settings."""

    level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        alias="LOG_LEVEL"
    )
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format",
        alias="LOG_FORMAT"
    )
    json_format: bool = Field(
        default=False,
        description="Whether to output logs in JSON format",
        alias="LOG_JSON_FORMAT"
    )

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        """Ensure log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v_upper

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class AudioConfig(BaseSettings):
    """Audio configuration for voice pipeline."""

    sample_rate: int = Field(
        default=16000,
        description="Audio sample rate in Hz",
        alias="AUDIO_SAMPLE_RATE"
    )
    channels: int = Field(
        default=1,
        description="Number of audio channels (1=mono, 2=stereo)",
        alias="AUDIO_CHANNELS"
    )
    chunk_size: int = Field(
        default=1024,
        description="Audio chunk size for processing",
        alias="AUDIO_CHUNK_SIZE"
    )
    input_device: Optional[int] = Field(
        default=None,
        description="Input device index (None=default)",
        alias="AUDIO_INPUT_DEVICE"
    )
    output_device: Optional[int] = Field(
        default=None,
        description="Output device index (None=default)",
        alias="AUDIO_OUTPUT_DEVICE"
    )

    @field_validator("sample_rate")
    @classmethod
    def validate_sample_rate(cls, v: int) -> int:
        """Ensure sample rate is valid."""
        valid_rates = [8000, 16000, 24000, 48000]
        if v not in valid_rates:
            raise ValueError(f"Sample rate must be one of: {', '.join(map(str, valid_rates))}")
        return v

    @field_validator("channels")
    @classmethod
    def validate_channels(cls, v: int) -> int:
        """Ensure channels is valid."""
        if v not in [1, 2]:
            raise ValueError("Channels must be 1 (mono) or 2 (stereo)")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class PipelineConfig(BaseSettings):
    """Pipeline configuration for voice processing."""

    # Speech-to-Text
    stt_model: str = Field(
        default="nova-2",
        description="Deepgram STT model to use",
        alias="STT_MODEL"
    )
    stt_language: str = Field(
        default="en-US",
        description="Speech recognition language",
        alias="STT_LANGUAGE"
    )
    stt_interim_results: bool = Field(
        default=True,
        description="Enable interim STT results for lower latency",
        alias="STT_INTERIM_RESULTS"
    )

    # Text-to-Speech
    tts_voice: str = Field(
        default="79a125e8-cd45-4c13-8a67-188112f4dd22",
        description="Cartesia voice ID",
        alias="TTS_VOICE"
    )
    tts_model: str = Field(
        default="sonic-english",
        description="Cartesia TTS model",
        alias="TTS_MODEL"
    )

    # Pipeline settings
    max_silence_duration: float = Field(
        default=1.5,
        description="Maximum silence duration before ending utterance (seconds)",
        alias="PIPELINE_MAX_SILENCE"
    )
    enable_interruptions: bool = Field(
        default=True,
        description="Allow user to interrupt bot speech",
        alias="PIPELINE_ENABLE_INTERRUPTIONS"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


class AppConfig(BaseSettings):
    """Main application configuration."""

    # API Keys
    api_keys: Optional[APIKeys] = None

    # Home Assistant
    home_assistant: Optional[HomeAssistantConfig] = None

    # Logging
    logging: Optional[LoggingConfig] = None

    # Audio
    audio: Optional[AudioConfig] = None

    # Pipeline
    pipeline: Optional[PipelineConfig] = None

    # Application settings
    debug: bool = Field(
        default=False,
        description="Enable debug mode",
        alias="DEBUG"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __init__(self, **kwargs):
        """Initialize configuration and load nested configs."""
        super().__init__(**kwargs)

        # Load nested configurations
        self.api_keys = APIKeys()
        self.home_assistant = HomeAssistantConfig()
        self.logging = LoggingConfig()
        self.audio = AudioConfig()
        self.pipeline = PipelineConfig()


def load_config() -> AppConfig:
    """Load and validate application configuration.

    Returns:
        AppConfig: Validated configuration object

    Raises:
        ValidationError: If required configuration is missing or invalid
    """
    # Check if .env file exists
    env_path = Path(".env")
    if not env_path.exists():
        raise FileNotFoundError(
            "Configuration file .env not found. "
            "Please copy .env.example to .env and fill in your API keys."
        )

    try:
        config = AppConfig()
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration: {e}") from e


# Global config instance (lazy loaded)
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get the global configuration instance.

    Returns:
        AppConfig: The global configuration object
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config
