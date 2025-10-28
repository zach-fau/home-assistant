"""Structured logging configuration for Home Voice Assistant.

This module sets up logging with configurable levels, formatters, and handlers.
It supports both standard text format and JSON format for structured logging.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from src.config import LoggingConfig


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: The log record to format

        Returns:
            JSON-formatted log message
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        return json.dumps(log_data)


class StructuredLogger:
    """Wrapper around Python's logging that supports structured logging."""

    def __init__(self, name: str, config: Optional[LoggingConfig] = None):
        """Initialize structured logger.

        Args:
            name: Logger name (typically __name__)
            config: Logging configuration (uses defaults if None)
        """
        self.logger = logging.getLogger(name)
        self.config = config or LoggingConfig()

        # Only configure if not already configured
        if not self.logger.handlers:
            self._configure()

    def _configure(self) -> None:
        """Configure the logger with handlers and formatters."""
        # Set logging level
        level = getattr(logging, self.config.level)
        self.logger.setLevel(level)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Set formatter based on configuration
        if self.config.json_format:
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(self.config.format)

        console_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(console_handler)

        # Prevent propagation to root logger
        self.logger.propagate = False

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with optional extra fields.

        Args:
            message: Log message
            **kwargs: Additional fields to include in structured logs
        """
        self._log(logging.DEBUG, message, kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message with optional extra fields.

        Args:
            message: Log message
            **kwargs: Additional fields to include in structured logs
        """
        self._log(logging.INFO, message, kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with optional extra fields.

        Args:
            message: Log message
            **kwargs: Additional fields to include in structured logs
        """
        self._log(logging.WARNING, message, kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message with optional extra fields.

        Args:
            message: Log message
            **kwargs: Additional fields to include in structured logs
        """
        self._log(logging.ERROR, message, kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message with optional extra fields.

        Args:
            message: Log message
            **kwargs: Additional fields to include in structured logs
        """
        self._log(logging.CRITICAL, message, kwargs)

    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback.

        Args:
            message: Log message
            **kwargs: Additional fields to include in structured logs
        """
        kwargs["exc_info"] = True
        self._log(logging.ERROR, message, kwargs)

    def _log(self, level: int, message: str, extra_fields: Dict[str, Any]) -> None:
        """Internal logging method that handles extra fields.

        Args:
            level: Logging level
            message: Log message
            extra_fields: Additional fields for structured logging
        """
        if extra_fields:
            # Create a custom LogRecord with extra fields
            extra = {"extra_fields": extra_fields}
            self.logger.log(level, message, extra=extra)
        else:
            self.logger.log(level, message)


def setup_logging(config: Optional[LoggingConfig] = None) -> None:
    """Setup root logger configuration.

    Args:
        config: Logging configuration (uses defaults if None)
    """
    config = config or LoggingConfig()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.level))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, config.level))

    # Set formatter
    if config.json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(config.format)

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def get_logger(name: str, config: Optional[LoggingConfig] = None) -> StructuredLogger:
    """Get a structured logger instance.

    Args:
        name: Logger name (typically __name__)
        config: Logging configuration (uses defaults if None)

    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(name, config)
