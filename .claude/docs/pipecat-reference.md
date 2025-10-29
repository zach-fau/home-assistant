# Pipecat Framework - Developer Reference

**Last Updated:** 2025-10-29
**Purpose:** Complete reference for building a daily life assistant with Pipecat

---

## Table of Contents

1. [What is Pipecat?](#what-is-pipecat)
2. [Core Architecture](#core-architecture)
3. [Key Concepts](#key-concepts)
4. [Installation & Setup](#installation--setup)
5. [Building Your First Bot](#building-your-first-bot)
6. [Pipeline Patterns](#pipeline-patterns)
7. [Services & Integrations](#services--integrations)
8. [Production Deployment](#production-deployment)
9. [Daily Life Assistant Use Cases](#daily-life-assistant-use-cases)
10. [Best Practices](#best-practices)

---

## What is Pipecat?

Pipecat is an **open-source Python framework** for building **real-time voice and multimodal conversational AI agents**. It orchestrates multiple AI services simultaneously, managing the complex timing and coordination between speech recognition, language models, and speech synthesis.

### Key Advantages

- **Ultra-Low Latency:** 500-800ms response times for natural conversations
- **Modular Design:** Swap AI providers without extensive code rewrites
- **Real-time Processing:** Stream processing eliminates waiting at each step
- **Production Ready:** Built-in error handling, logging, and scaling
- **Everything in Parallel:** While the LLM generates later parts of a response, earlier sections are already being converted to speech and played back

### What You Can Build

- Voice assistants with natural speech interaction
- Phone-based customer service agents
- Multimodal applications (audio + video + text)
- Interactive storytelling and companions
- Voice-controlled games and experiences
- Task automation with structured conversations

---

## Core Architecture

### The Pipeline Model

Pipecat uses a **sequential pipeline architecture** where data flows through a series of processors:

```python
pipeline = Pipeline([
    transport.input(),              # Audio/data input
    rtvi,                           # Real-time voice interaction
    stt,                            # Speech-to-text
    context_aggregator.user(),      # User context management
    llm,                            # Language model processing
    tts,                            # Text-to-speech synthesis
    transport.output(),             # Audio/data output
    context_aggregator.assistant(), # Assistant context management
])
```

### Data Flow

```
User Speech → Audio Capture → VAD → STT → Context → LLM → TTS → Audio Output
```

1. **Audio Capture** - Browser microphone input via WebRTC
2. **Voice Activity Detection (VAD)** - Silero VAD identifies speech boundaries
3. **Speech-to-Text (STT)** - Real-time transcription (e.g., Deepgram)
4. **Context Aggregation** - Conversation history management
5. **Language Model (LLM)** - Generate intelligent responses (e.g., OpenAI)
6. **Text-to-Speech (TTS)** - Voice synthesis (e.g., Cartesia, ElevenLabs)
7. **Audio Playback** - Stream to user's device

**Critical Insight:** Each processor receives specific frame types, performs its specialized task, outputs new frames, and passes through unhandled frames. Most data flows downstream, but frames can move upstream when needed.

---

## Key Concepts

### 1. Frames

**Frames** are data packages flowing through the application. They contain specific information types:

- Audio frames from microphones
- Transcribed text from STT
- LLM responses
- Synthesized speech from TTS
- Control frames for system events

Think of frames as messages passed between processors in the pipeline.

### 2. Frame Processors

**Frame Processors** are specialized workers handling distinct tasks:

- **STT Processor:** Converts audio frames to text frames
- **LLM Processor:** Converts text frames to response text frames
- **TTS Processor:** Converts text frames to audio frames
- **Context Processor:** Maintains conversation history
- **VAD Processor:** Detects speech boundaries

Each processor:
- Receives specific frame types
- Performs specialized processing
- Outputs new frames
- Passes through unhandled frames

### 3. Pipelines

**Pipelines** are connected processor chains that orchestrate frame flow automatically. They handle:

- Sequential data processing
- Parallel execution where possible
- Error propagation
- Event management

### 4. Services

**Services** are external AI integrations that power processors:

- Speech recognition (Deepgram, AssemblyAI, Whisper)
- Language models (OpenAI, Anthropic, Gemini)
- Speech synthesis (Cartesia, ElevenLabs, Google)
- Video generation (HeyGen, Tavus)
- Memory systems (mem0)

### 5. Transports

**Transports** handle network communication:

- **WebRTC:** Real-time audio/video streaming
- **WebSocket:** Data streaming
- **Daily:** Video conferencing platform integration
- **Twilio:** Phone system integration

### 6. Context Management

**Context** maintains conversation state:

- Conversation history
- System prompts (bot personality)
- User preferences
- Session data

Uses OpenAI message format:
```python
[
    {"role": "system", "content": "You are a helpful assistant..."},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
]
```

---

## Installation & Setup

### Prerequisites

- **Python:** 3.10+ (3.12 recommended)
- **Package Manager:** `uv` (modern Python package manager)
- **API Keys:** Deepgram, OpenAI, Cartesia (for basic voice bot)

### Install uv Package Manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Method 1: Quickstart Template (Recommended)

```bash
# Clone quickstart repository
git clone https://github.com/pipecat-ai/pipecat-quickstart.git
cd pipecat-quickstart

# Setup environment
cp env.example .env

# Edit .env with your API keys
# DEEPGRAM_API_KEY=your_key
# OPENAI_API_KEY=your_key
# CARTESIA_API_KEY=your_key

# Install dependencies
uv sync

# Run locally
uv run bot.py
```

**Access:** `http://localhost:7860/client`

**Note:** Initial startup takes ~20 seconds as Pipecat downloads models.

### Method 2: From Scratch

```bash
# Create new project
uv init my-assistant && cd my-assistant

# Install Pipecat with services
uv add "pipecat-ai[daily,openai,deepgram,cartesia]"

# Create your bot.py
# (see code examples below)
```

### Available Service Extras

```bash
# STT providers
uv add "pipecat-ai[deepgram,assemblyai,whisper]"

# TTS providers
uv add "pipecat-ai[cartesia,elevenlabs,azure]"

# LLM providers
uv add "pipecat-ai[openai,anthropic,gemini]"

# Transports
uv add "pipecat-ai[daily,twilio]"

# All services
uv add "pipecat-ai[all]"
```

---

## Building Your First Bot

### Minimal Voice Bot Structure

```python
import asyncio
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.transports.services.daily import DailyTransport
from pipecat.vad.silero import SileroVADAnalyzer

async def main():
    # Configure services
    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))

    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4"
    )

    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id="default"
    )

    # Setup transport
    transport = DailyTransport(
        room_url="your_daily_room_url",
        token="your_daily_token",
        bot_name="Assistant",
    )

    # Voice activity detection
    vad = SileroVADAnalyzer(stop_secs=0.2)

    # Build pipeline
    pipeline = Pipeline([
        transport.input(),
        vad,
        stt,
        llm,
        tts,
        transport.output(),
    ])

    # Create task and run
    task = PipelineTask(pipeline)
    runner = PipelineRunner()
    await runner.run(task)

if __name__ == "__main__":
    asyncio.run(main())
```

### Complete Bot with Context Management

```python
from pipecat.processors.aggregators.llm_context import (
    LLMContextAggregatorPair,
    LLMContext
)

# Initialize context
messages = [
    {
        "role": "system",
        "content": "You are a helpful daily assistant. Be concise and friendly."
    }
]

context = LLMContext(messages=messages)
context_aggregator = LLMContextAggregatorPair(
    user=context,
    assistant=context
)

# Build pipeline with context
pipeline = Pipeline([
    transport.input(),
    vad,
    stt,
    context_aggregator.user(),     # Add user messages to context
    llm,
    tts,
    transport.output(),
    context_aggregator.assistant(), # Add assistant responses to context
])
```

### Event Handling

```python
@transport.event_handler("on_client_connected")
async def on_client_connected(transport, client):
    print(f"Client connected: {client}")
    # Queue initial greeting
    await task.queue_frame(LLMRunFrame())

@transport.event_handler("on_client_disconnected")
async def on_client_disconnected(transport, client):
    print(f"Client disconnected: {client}")
```

---

## Pipeline Patterns

### Basic Voice Assistant

```python
Pipeline([
    transport.input(),
    vad,
    stt,
    llm,
    tts,
    transport.output(),
])
```

### Context-Aware Assistant

```python
Pipeline([
    transport.input(),
    vad,
    stt,
    context_aggregator.user(),
    llm,
    tts,
    transport.output(),
    context_aggregator.assistant(),
])
```

### Multimodal (Voice + Vision)

```python
Pipeline([
    transport.input(),
    vad,
    stt,
    vision_processor,
    context_aggregator.user(),
    llm,
    tts,
    video_processor,
    transport.output(),
    context_aggregator.assistant(),
])
```

### Turn Management

```python
from pipecat.processors.turn_analyzer import LocalSmartTurnAnalyzerV3

turn_analyzer = LocalSmartTurnAnalyzerV3()

Pipeline([
    transport.input(),
    vad,
    turn_analyzer,
    stt,
    llm,
    tts,
    transport.output(),
])
```

---

## Services & Integrations

### Speech-to-Text (STT) - 16+ Providers

**Recommended for Daily Assistant:**
- **Deepgram:** Best latency and accuracy balance
- **AssemblyAI:** Excellent accuracy, good features
- **OpenAI Whisper:** Local processing option

```python
# Deepgram
from pipecat.services.deepgram import DeepgramSTTService
stt = DeepgramSTTService(
    api_key=os.getenv("DEEPGRAM_API_KEY"),
    model="nova-2"
)

# AssemblyAI
from pipecat.services.assemblyai import AssemblyAISTTService
stt = AssemblyAISTTService(
    api_key=os.getenv("ASSEMBLYAI_API_KEY")
)
```

### Text-to-Speech (TTS) - 20+ Providers

**Recommended for Daily Assistant:**
- **Cartesia:** Ultra-low latency, natural voices
- **ElevenLabs:** Best voice quality
- **OpenAI TTS:** Good balance of quality and speed

```python
# Cartesia
from pipecat.services.cartesia import CartesiaTTSService
tts = CartesiaTTSService(
    api_key=os.getenv("CARTESIA_API_KEY"),
    voice_id="a0e99841-438c-4a64-b679-ae501e7d6091"  # Example voice
)

# ElevenLabs
from pipecat.services.elevenlabs import ElevenLabsTTSService
tts = ElevenLabsTTSService(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
    voice_id="21m00Tcm4TlvDq8ikWAM"  # Example voice
)
```

### Language Models (LLM) - 17+ Providers

**Recommended for Daily Assistant:**
- **OpenAI GPT-4:** Best general performance
- **Anthropic Claude:** Excellent for complex reasoning
- **Google Gemini:** Good multimodal capabilities

```python
# OpenAI
from pipecat.services.openai import OpenAILLMService
llm = OpenAILLMService(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4-turbo-preview"
)

# Anthropic
from pipecat.services.anthropic import AnthropicLLMService
llm = AnthropicLLMService(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-opus-20240229"
)
```

### Voice Activity Detection (VAD)

```python
from pipecat.vad.silero import SileroVADAnalyzer

# Standard configuration
vad = SileroVADAnalyzer(
    stop_secs=0.2  # How long to wait after speech stops
)

# More responsive (faster interruptions)
vad = SileroVADAnalyzer(stop_secs=0.1)

# More patient (fewer false interruptions)
vad = SileroVADAnalyzer(stop_secs=0.5)
```

---

## Production Deployment

### Pipecat Cloud

**Prerequisites:**
- Pipecat Cloud account
- Docker and Docker Hub account
- Pipecat CLI: `uv tool install pipecat-ai-cli`

### Deployment Configuration

Create `pcc-deploy.toml`:

```toml
agent_name = "daily-assistant"
image = "YOUR_DOCKERHUB_USERNAME/daily-assistant:0.1"
secret_set = "daily-assistant-secrets"

[scaling]
    min_agents = 1
    max_agents = 5
```

### Deployment Steps

```bash
# 1. Authenticate
pipecat cloud auth login

# 2. Upload secrets
pipecat cloud secrets set daily-assistant-secrets --file .env

# 3. Build and push Docker image
pipecat cloud docker build-push

# 4. Deploy
pipecat cloud deploy

# 5. Monitor
pipecat cloud logs daily-assistant
```

### Dockerfile Example

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY bot.py .

# Install dependencies
RUN uv sync

# Run bot
CMD ["uv", "run", "bot.py"]
```

---

## Daily Life Assistant Use Cases

### 1. Calendar Management

```python
# System prompt
"""
You are a calendar assistant. You can:
- Schedule events
- Check availability
- Set reminders
- Update meetings

Access the user's calendar via the calendar_tool function.
"""

# Integration with calendar API
async def calendar_tool(action, **kwargs):
    if action == "schedule":
        # Create event
        pass
    elif action == "check":
        # Check availability
        pass
```

### 2. Task Management

```python
# System prompt
"""
You are a task management assistant. You can:
- Create tasks
- Update task status
- Set priorities
- Check deadlines

Use the task_tool function to manage tasks.
"""
```

### 3. Information Retrieval

```python
# System prompt
"""
You are an information assistant with web search capabilities.
You can:
- Search the web
- Summarize articles
- Answer questions with sources
- Provide real-time information

Use the search_tool function when needed.
"""
```

### 4. Smart Home Control

```python
# System prompt
"""
You are a smart home assistant. You can:
- Control lights
- Adjust temperature
- Manage scenes
- Check device status

Use the smart_home_tool function to control devices.
"""
```

### 5. Communication

```python
# System prompt
"""
You are a communication assistant. You can:
- Read emails
- Send messages
- Make calls
- Schedule communications

Use the communication_tool function as needed.
"""
```

---

## Best Practices

### Performance Optimization

1. **Choose Low-Latency Services**
   - STT: Deepgram Nova-2
   - TTS: Cartesia
   - LLM: GPT-4 Turbo or Claude 3

2. **Configure VAD Appropriately**
   ```python
   # Balance between responsiveness and false interruptions
   vad = SileroVADAnalyzer(stop_secs=0.2)
   ```

3. **Enable Streaming**
   - All services should stream responses
   - Don't wait for complete responses

4. **Monitor Latency**
   ```python
   params = PipelineParams(
       enable_metrics=True,
       enable_usage_metrics=True
   )
   ```

### Context Management

1. **System Prompts**
   ```python
   messages = [
       {
           "role": "system",
           "content": """
           You are a helpful daily assistant named Alex.

           Personality:
           - Concise and efficient
           - Friendly but professional
           - Proactive in helping

           Capabilities:
           - Calendar management
           - Task tracking
           - Information lookup
           - Smart home control
           """
       }
   ]
   ```

2. **Context Pruning**
   - Limit conversation history to recent messages
   - Summarize older context
   - Keep critical information in system prompt

3. **User Preferences**
   - Store user preferences
   - Adapt to user's communication style
   - Learn from interactions

### Error Handling

```python
try:
    await runner.run(task)
except Exception as e:
    logger.error(f"Pipeline error: {e}")
    # Graceful degradation
    # Notify user
    # Restart pipeline if needed
```

### Monitoring & Analytics

```python
# Enable built-in monitoring
params = PipelineParams(
    enable_metrics=True,
    enable_usage_metrics=True,
    sentry_dsn=os.getenv("SENTRY_DSN")  # Optional
)

# OpenTelemetry integration
from pipecat.observability import configure_opentelemetry
configure_opentelemetry()
```

### Security

1. **API Key Management**
   - Use environment variables
   - Never commit keys to git
   - Rotate keys regularly

2. **User Authentication**
   - Implement user authentication
   - Session management
   - Access control

3. **Data Privacy**
   - Encrypt sensitive data
   - Clear conversation history
   - Comply with privacy regulations

---

## Quick Reference

### Essential Imports

```python
# Core
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask

# Services
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.cartesia import CartesiaTTSService

# Transports
from pipecat.transports.services.daily import DailyTransport

# Processors
from pipecat.vad.silero import SileroVADAnalyzer
from pipecat.processors.aggregators.llm_context import (
    LLMContextAggregatorPair,
    LLMContext
)
from pipecat.processors.turn_analyzer import LocalSmartTurnAnalyzerV3
```

### Common Configurations

**Development:**
- Local testing with `http://localhost:7860`
- Debug logging enabled
- Fast iteration

**Production:**
- Cloud deployment
- Monitoring enabled
- Error tracking (Sentry)
- Auto-scaling configured

---

## Resources

- **Documentation:** https://docs.pipecat.ai
- **GitHub:** https://github.com/pipecat-ai/pipecat
- **Quickstart:** https://github.com/pipecat-ai/pipecat-quickstart
- **Discord:** Active community support
- **Examples:** Check GitHub for use case examples

---

## Next Steps for Building Daily Assistant

1. ✅ **Foundation:** Set up Pipecat with basic voice interaction
2. 📅 **Calendar Integration:** Connect to calendar API
3. ✅ **Task Management:** Implement task tracking
4. 🔍 **Information Retrieval:** Add web search capabilities
5. 🏠 **Smart Home:** Integrate with Home Assistant
6. 💬 **Communication:** Email and messaging integration
7. 🎯 **Personalization:** Learn user preferences
8. 🚀 **Deploy:** Production deployment to cloud

---

*This document will evolve as we build out the daily life assistant. Keep it updated with new patterns, learnings, and best practices.*
