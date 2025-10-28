"""Command-line interface for Home Voice Assistant.

This module provides a CLI for testing and running the voice assistant.
It uses argparse for command-line argument parsing.
"""

import argparse
import sys
from typing import List, Optional

from src.config import get_config
from src.logger import get_logger, setup_logging


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="home-voice-assistant",
        description="Home Voice Assistant - Control your smart home with voice commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --check-config          Check configuration validity
  %(prog)s --debug                 Run in debug mode
  %(prog)s --log-level DEBUG       Set log level to DEBUG
  %(prog)s --json-logs             Output logs in JSON format

For more information, visit: https://github.com/yourusername/home-voice-assistant
        """
    )

    # Configuration options
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="Check configuration validity and exit"
    )

    parser.add_argument(
        "--config-file",
        type=str,
        default=".env",
        help="Path to configuration file (default: .env)"
    )

    # Logging options
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level (overrides config file)"
    )

    parser.add_argument(
        "--json-logs",
        action="store_true",
        help="Output logs in JSON format"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (equivalent to --log-level DEBUG)"
    )

    # Version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    return parser


def check_configuration() -> bool:
    """Check if configuration is valid.

    Returns:
        True if configuration is valid, False otherwise
    """
    logger = get_logger(__name__)

    try:
        logger.info("Checking configuration...")
        config = get_config()

        # Validate API keys
        logger.info("Validating API keys...")
        if not config.api_keys.deepgram_api_key:
            logger.error("Deepgram API key is missing")
            return False
        if not config.api_keys.openai_api_key:
            logger.error("OpenAI API key is missing")
            return False
        if not config.api_keys.cartesia_api_key:
            logger.error("Cartesia API key is missing")
            return False
        logger.info("API keys validated successfully")

        # Validate Home Assistant config
        logger.info("Validating Home Assistant configuration...")
        if not config.home_assistant.url:
            logger.error("Home Assistant URL is missing")
            return False
        if not config.home_assistant.token:
            logger.error("Home Assistant token is missing")
            return False
        logger.info(
            "Home Assistant configuration validated",
            url=config.home_assistant.url
        )

        # Log configuration summary
        logger.info(
            "Configuration validated successfully",
            debug_mode=config.debug,
            log_level=config.logging.level,
            json_format=config.logging.json_format
        )

        return True

    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return False
    except Exception as e:
        logger.exception(f"Configuration validation failed: {e}")
        return False


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command-line arguments (uses sys.argv if None)

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Setup logging based on arguments
    try:
        from src.config import LoggingConfig

        # Determine log level
        log_level = "DEBUG" if args.debug else (args.log_level or "INFO")

        # Create logging config
        logging_config = LoggingConfig(
            level=log_level,
            json_format=args.json_logs
        )

        # Setup logging
        setup_logging(logging_config)
        logger = get_logger(__name__, logging_config)

        logger.info("Starting Home Voice Assistant CLI")

        # Handle check-config command
        if args.check_config:
            logger.info("Running configuration check...")
            if check_configuration():
                logger.info("Configuration check passed")
                print("\nConfiguration is valid!")
                return 0
            else:
                logger.error("Configuration check failed")
                print("\nConfiguration check failed. Please check the logs above.")
                return 1

        # Default: show help and configuration status
        logger.info("No command specified, showing help")
        parser.print_help()
        print("\n" + "=" * 70)
        print("Configuration Status:")
        print("=" * 70)

        if check_configuration():
            print("Configuration is valid and ready to use.")
            print("\nNext steps:")
            print("  1. Run with --check-config to verify your setup")
            print("  2. Start the voice assistant (coming soon)")
        else:
            print("Configuration is invalid. Please fix the errors above.")
            return 1

        return 0

    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 130
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
