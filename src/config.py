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


class AppConfig(BaseSettings):
    """Main application configuration."""

    # API Keys
    api_keys: Optional[APIKeys] = None

    # Home Assistant
    home_assistant: Optional[HomeAssistantConfig] = None

    # Logging
    logging: Optional[LoggingConfig] = None

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
