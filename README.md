# Home Voice Assistant

A Python-based voice assistant for controlling Home Assistant using natural language. Built with Pipecat AI for real-time voice conversations.

## Features

- Real-time voice conversations using Pipecat AI
- Speech-to-text with Deepgram
- Natural language processing with OpenAI
- Text-to-speech with Cartesia
- Integration with Home Assistant for smart home control
- Structured logging with JSON support
- Configuration validation and management

## Prerequisites

- Python 3.11 or higher
- Home Assistant instance (local or remote)
- API keys for:
  - Deepgram (speech-to-text)
  - OpenAI (language model)
  - Cartesia (text-to-speech)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/home-voice-assistant.git
cd home-voice-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment:
```bash
cp .env.example .env
```

5. Edit `.env` and fill in your API keys and Home Assistant details:
```bash
# Edit with your favorite editor
nano .env
# or
vim .env
```

## Configuration

The application uses a `.env` file for configuration. All settings are validated on startup.

### Required Configuration

#### API Keys

- **DEEPGRAM_API_KEY**: Get from [Deepgram Console](https://console.deepgram.com/)
- **OPENAI_API_KEY**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **CARTESIA_API_KEY**: Get from [Cartesia](https://cartesia.ai/)

#### Home Assistant

- **HOME_ASSISTANT_URL**: Your Home Assistant instance URL (e.g., `http://localhost:8123`)
- **HOME_ASSISTANT_TOKEN**: Long-lived access token from Home Assistant
  - Create at: `http://your-ha-url:8123/profile/security`

### Optional Configuration

- **LOG_LEVEL**: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) - default: INFO
- **LOG_JSON_FORMAT**: Output logs in JSON format - default: false
- **HOME_ASSISTANT_VERIFY_SSL**: Verify SSL certificates - default: true
- **DEBUG**: Enable debug mode - default: false

## Usage

### Check Configuration

Verify your configuration is valid:
```bash
python -m src.cli --check-config
```

### Run with Debug Logging

```bash
python -m src.cli --debug
```

### Run with JSON Logs

Useful for log aggregation and monitoring:
```bash
python -m src.cli --json-logs
```

### Command-Line Options

```bash
python -m src.cli --help
```

Available options:
- `--check-config`: Check configuration validity and exit
- `--config-file PATH`: Path to configuration file (default: .env)
- `--log-level LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--json-logs`: Output logs in JSON format
- `--debug`: Enable debug mode (equivalent to --log-level DEBUG)
- `--version`: Show version information

## Project Structure

```
home-voice-assistant/
├── src/
│   ├── __init__.py
│   ├── config.py      # Configuration management with Pydantic
│   ├── logger.py      # Structured logging setup
│   └── cli.py         # Command-line interface
├── tests/
│   └── __init__.py
├── .env.example       # Configuration template
├── .gitignore
├── requirements.txt   # Python dependencies
└── README.md
```

## Development

### Configuration Module (`src/config.py`)

Handles loading and validating configuration using Pydantic models. Provides:
- Type-safe configuration
- Environment variable loading
- Validation with clear error messages
- Nested configuration structures

Example usage:
```python
from src.config import get_config

config = get_config()
print(config.api_keys.deepgram_api_key)
print(config.home_assistant.url)
```

### Logging Module (`src/logger.py`)

Provides structured logging with support for both text and JSON formats:

```python
from src.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing request", user_id=123, action="light_on")
logger.error("Failed to connect", endpoint="/api/lights")
```

### CLI Module (`src/cli.py`)

Command-line interface using argparse. Provides:
- Configuration validation
- Help text and examples
- Logging control
- Future command extensions

## Troubleshooting

### Configuration Errors

If you see configuration validation errors:
1. Ensure `.env` file exists (copy from `.env.example`)
2. Check all required API keys are filled in
3. Verify Home Assistant URL is correct (no trailing slash)
4. Confirm Home Assistant token is valid

### Home Assistant Connection

To test Home Assistant connection:
```bash
curl -X GET \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  http://your-ha-url:8123/api/
```

Should return: `{"message":"API running."}`

### API Key Issues

- **Deepgram**: Ensure you have credits in your account
- **OpenAI**: Check API key has proper permissions and billing is set up
- **Cartesia**: Verify API key is active

## Next Steps

After setting up the foundation, the following features will be added:
- Voice pipeline implementation
- Home Assistant API client
- Natural language command processing
- Voice conversation handling
- Device control capabilities

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Ensure tests pass
4. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions:
- GitHub Issues: [Project Issues](https://github.com/yourusername/home-voice-assistant/issues)
- Documentation: [Project Wiki](https://github.com/yourusername/home-voice-assistant/wiki)

## Acknowledgments

- [Pipecat AI](https://github.com/pipecat-ai/pipecat) - Real-time voice conversation framework
- [Home Assistant](https://www.home-assistant.io/) - Open source home automation
- [Deepgram](https://deepgram.com/) - Speech-to-text API
- [OpenAI](https://openai.com/) - Language models
- [Cartesia](https://cartesia.ai/) - Text-to-speech API
