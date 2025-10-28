---
name: initial-feature
status: backlog
created: 2025-10-28T20:47:03Z
progress: 0%
prd: .claude/prds/initial-feature.md
github: https://github.com/zach-fau/home-assistant/issues/1
---

# Epic: Home Voice Assistant with Pipecat

## Overview
Build a production-ready, real-time voice assistant using the Pipecat framework that orchestrates Deepgram (STT), GPT-4o-mini (LLM), and Cartesia Sonic (TTS) into a seamless conversational pipeline. The system will leverage GPT-4o-mini's function calling capabilities to execute tools for Home Assistant control, web search, and productivity tasks, enabling genuinely useful hands-free assistance.

## Architecture Decisions

### Core Framework Choice: Pipecat
**Decision**: Use Pipecat as the conversation orchestration framework
**Rationale**:
- Purpose-built for real-time conversational AI pipelines
- Native support for streaming STT, LLM, and TTS
- Built-in handling of conversation state and interruptions
- Reduces complexity of managing async audio streams and API coordination

### Async Python Architecture
**Decision**: Python 3.11+ with asyncio for all I/O operations
**Rationale**:
- Pipecat is Python-native with async design
- Multiple concurrent API calls (STT, LLM, TTS, tools) require non-blocking I/O
- Natural fit for streaming audio and WebSocket connections
- Rich ecosystem of async HTTP clients (aiohttp)

### Function Calling for Tool Integration
**Decision**: Use GPT-4o-mini's native function calling for tool execution
**Rationale**:
- LLM determines appropriate tool and parameters from natural language
- Type-safe tool definitions with JSON schema
- Reduces prompt engineering complexity
- Built-in parameter validation

### Modular Tool System
**Decision**: Plugin-based tool architecture with unified interface
**Rationale**:
- Easy to add new capabilities without modifying core pipeline
- Each tool is self-contained with clear dependencies
- Enables parallel tool development
- Simplifies testing of individual tools

### API Service Selection
**Decision**: Cloud-based APIs for all AI services initially
**Rationale**:
- Lowest latency with Deepgram Nova-2, Cartesia Sonic streaming
- GPT-4o-mini provides best cost/performance for function calling
- Reduces infrastructure complexity for MVP
- Local options can be added later as plugins

## Technical Approach

### Core Conversational Pipeline
The heart of the system is a Pipecat pipeline that orchestrates the conversation flow:

```
Audio Input → Deepgram STT → Pipecat State Manager → GPT-4o-mini → Tool Executor → Response Generator → Cartesia TTS → Audio Output
```

**Implementation details:**
- Use Pipecat's built-in transport for audio I/O (microphone/speaker)
- Configure Deepgram WebSocket for streaming STT with low latency
- Implement Pipecat pipeline stages for each component
- Use Pipecat's context management for conversation state
- Handle barge-in and interruptions via Pipecat's interruption system

### Tool Execution Layer
Function calling enables the LLM to invoke tools dynamically. Tools are registered with JSON schema definitions:

**Tool Interface:**
```python
class Tool:
    name: str
    description: str
    parameters: JSONSchema
    async def execute(self, **kwargs) -> ToolResult
```

**Priority Tools:**
1. **Home Assistant Controller**: REST API + WebSocket for device control and state queries
2. **Web Search Engine**: Brave Search or SerpAPI for information retrieval
3. **Calendar/Reminder Manager**: Local or cloud-based task management
4. **Timer/Alarm System**: Simple time-based reminders

### Configuration Management
**Approach**: Environment-based configuration with validation
- API keys stored in `.env` file (not committed)
- User preferences in `config.yaml` (voice settings, wake word, etc.)
- Tool-specific configuration (Home Assistant URL, search API choice)
- Runtime validation with clear error messages

### Error Handling Strategy
**Graceful degradation with user feedback:**
- API failures → retry with exponential backoff → inform user if persistent
- Network issues → queue requests, notify user of connectivity problems
- Tool execution errors → report to user, continue conversation
- Audio I/O errors → restart pipeline, log for debugging

## Implementation Strategy

### Development Approach
**Incremental integration with continuous testing:**
1. Start with minimal Pipecat pipeline (STT → TTS passthrough)
2. Add LLM layer without function calling (basic conversation)
3. Integrate function calling framework with one simple tool (timer)
4. Add Home Assistant integration (highest value tool)
5. Expand with additional tools incrementally
6. Optimize latency and polish UX

### Risk Mitigation
**Latency management:**
- Use streaming responses from all services
- Parallel tool execution where possible
- Cache frequently accessed data (Home Assistant states)
- Profile and optimize hot paths

**API cost control:**
- Implement rate limiting
- Monitor usage with logging
- Use cheaper models where possible (GPT-4o-mini is already cost-effective)
- Add configurable usage caps

**Testing strategy:**
- Unit tests for each tool independently
- Integration tests for pipeline components
- End-to-end tests with recorded audio samples
- Load testing for latency profiling

## Task Breakdown Preview

### 1. Project Foundation
Set up project structure, dependency management, and configuration system
- Python project with Poetry/pip for dependencies
- Environment configuration with validation
- Logging and debugging infrastructure
- Basic CLI for testing components

### 2. Core Pipecat Pipeline
Implement the basic conversation loop with audio I/O
- Pipecat pipeline setup with audio transport
- Deepgram STT integration with streaming
- Cartesia Sonic TTS integration
- Basic "echo bot" functionality for pipeline validation

### 3. LLM Integration with Function Calling
Add GPT-4o-mini with tool execution framework
- OpenAI API integration with streaming
- Function calling schema definitions
- Tool registration and execution system
- Conversation context management

### 4. Home Assistant Integration
Implement comprehensive smart home control
- Home Assistant REST API client
- WebSocket connection for real-time events
- Device discovery and state queries
- Scene and automation triggers
- Function definitions for common operations

### 5. Web Search Tool
Add information retrieval capability
- Brave Search or SerpAPI integration
- Result summarization logic
- Caching for repeated queries
- Function definition for search operations

### 6. Productivity Toolkit
Implement calendar, reminders, and timer functionality
- Timer and alarm system
- Reminder creation and management
- Calendar integration (local or CalDAV)
- Note-taking capability

### 7. Error Handling and Polish
Robust error recovery and user experience refinements
- Comprehensive error handling with user feedback
- Retry logic and graceful degradation
- Audio feedback improvements
- Latency optimization

### 8. Testing and Documentation
Ensure reliability and maintainability
- Unit and integration test suite
- End-to-end testing with sample conversations
- User documentation and setup guide
- Developer documentation for adding tools

## Dependencies

### External Service Dependencies
- **Deepgram API** (STT): Required for speech recognition
- **OpenAI API** (GPT-4o-mini): Required for LLM and function calling
- **Cartesia Sonic API** (TTS): Required for voice synthesis
- **Home Assistant**: Pre-existing installation required
- **Web Search API**: Brave Search or SerpAPI for information retrieval

### Infrastructure Dependencies
- **Python 3.11+**: Required for latest async features
- **Audio hardware**: Microphone and speakers with adequate quality
- **Network connectivity**: Reliable internet for cloud APIs (< 100ms latency ideal)
- **Compute resources**: Minimum 2GB RAM, 2 CPU cores (Raspberry Pi 4+ compatible)

### Third-Party Libraries
- **Pipecat**: Core framework for conversation orchestration
- **aiohttp**: Async HTTP client for API requests
- **python-dotenv**: Environment configuration
- **Home Assistant Python client**: Simplified API access
- **Audio libraries**: PyAudio or similar for audio I/O

## Success Criteria (Technical)

### Performance Benchmarks
- **End-to-end latency**: P95 < 2.5 seconds (speech input → audio response)
- **STT latency**: < 500ms from speech end to transcription
- **LLM response time**: < 1.5 seconds for function calls, < 3 seconds for reasoning
- **TTS latency**: < 300ms to first audio chunk
- **System stability**: 24+ hours continuous operation without restart

### Quality Gates
- **Speech recognition accuracy**: > 95% on clear speech (verified with test samples)
- **Command success rate**: > 95% for supported operations
- **Tool execution reliability**: > 98% success rate for Home Assistant commands
- **Code coverage**: > 80% for core pipeline and tool execution
- **Integration tests**: 100% passing for critical user journeys

### Acceptance Criteria
- User can complete all core user journeys from PRD hands-free
- System handles at least 10 distinct task types successfully
- Graceful error handling with clear user feedback
- Configuration is straightforward with sensible defaults
- Documentation enables new users to set up system in < 30 minutes

## Estimated Effort

### Overall Timeline
**MVP (Phases 1-2): 4-6 weeks**
- Week 1-2: Core pipeline and basic conversation
- Week 3-4: Home Assistant integration and tool framework
- Week 5-6: Additional tools and polish

**Full Feature Set: 8-10 weeks**
- Week 7-8: Productivity tools comprehensive implementation
- Week 9-10: Optimization, testing, and documentation

### Resource Requirements
- **Primary developer**: Full-time equivalent for duration
- **Testing support**: Part-time for integration testing
- **API costs**: $20-50/month for development and testing

### Critical Path Items
1. Pipecat pipeline stability (blocks all other work)
2. Function calling framework (required for all tools)
3. Home Assistant integration (highest value feature)
4. Latency optimization (affects user experience significantly)

### Risk Buffer
- 20% time buffer for unexpected integration challenges
- Additional time for API latency optimization if needed
- Potential for extended testing phase based on stability

## Tasks Created
- [ ] [001.md](.claude/epics/initial-feature/001.md) - Project Foundation and Configuration Setup (parallel: false)
- [ ] [002.md](.claude/epics/initial-feature/002.md) - Core Pipecat Pipeline with STT and TTS (parallel: false)
- [ ] [003.md](.claude/epics/initial-feature/003.md) - LLM Integration with Function Calling Framework (parallel: false)
- [ ] [004.md](.claude/epics/initial-feature/004.md) - Home Assistant Integration (parallel: true)
- [ ] [005.md](.claude/epics/initial-feature/005.md) - Web Search Tool Integration (parallel: true)
- [ ] [006.md](.claude/epics/initial-feature/006.md) - Productivity Toolkit Implementation (parallel: true)
- [ ] [007.md](.claude/epics/initial-feature/007.md) - Error Handling and Polish (parallel: false)
- [ ] [008.md](.claude/epics/initial-feature/008.md) - Testing and Documentation (parallel: false)

**Total tasks:** 8
**Parallel tasks:** 3 (tasks 004, 005, 006 can run concurrently after task 003)
**Sequential tasks:** 5
**Estimated total effort:** 72-92 hours (4-6 weeks for one developer)
