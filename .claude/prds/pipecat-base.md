---
name: pipecat-base
description: Foundational Pipecat implementation for real-time voice-based daily life assistant
status: backlog
created: 2025-10-29T00:07:25Z
---

# PRD: Pipecat-Base

## Executive Summary

Pipecat-base establishes the foundational infrastructure for a voice-first daily life assistant using the Pipecat framework. This implementation provides real-time, conversational voice interaction with ultra-low latency (500-800ms), enabling natural communication with an AI assistant that can help manage daily tasks, calendars, information retrieval, and smart home control.

**Value Proposition:** Transform daily task management from manual, multi-app interactions into a natural, voice-driven experience that feels like talking to a personal assistant.

## Problem Statement

### Current State
Users currently manage their daily lives through fragmented, manual interactions:
- Switching between multiple apps for calendar, tasks, reminders
- Typing queries and commands on keyboards/touchscreens
- Navigating complex UIs for simple actions
- Losing context when jumping between different tools
- Difficulty multitasking while managing digital tasks

### The Pain
- **Time-consuming:** Every task requires device unlock, app navigation, typing
- **Cognitively taxing:** Mental overhead of remembering which app to use for what
- **Context switching:** Constant interruptions to workflow
- **Accessibility barriers:** Not hands-free friendly, difficult while driving/cooking/exercising

### Why Now?
- Real-time voice AI technology has reached production-ready maturity (500-800ms latency)
- LLMs can understand complex, contextual requests
- Speech recognition accuracy is highly reliable
- TTS voices sound natural and engaging
- User expectations for voice interaction have been set by consumer assistants

## User Stories

### Primary Persona: The Busy Professional
**Profile:** 30-45 years old, tech-savvy, juggles work and personal life, values efficiency

#### User Journey: Morning Routine
1. **Wake up** → "Good morning, Alex"
2. **Daily briefing** → Assistant provides weather, calendar, priorities
3. **Task planning** → "Add a reminder to review the Johnson proposal at 2 PM"
4. **Information** → "What's on my calendar today?"
5. **Adjustment** → "Move my 3 PM meeting to 4 PM"

**Pain Points Addressed:**
- No need to check multiple apps
- Hands-free while getting ready
- Natural language, no UI navigation
- Context maintained throughout conversation

#### User Journey: Work Day
1. **Quick captures** → "Remind me to email Sarah about the meeting notes"
2. **Information lookup** → "What's the latest on the project deadline?"
3. **Task management** → "Mark the design review as complete"
4. **Smart home** → "Set the office to focus mode"

#### User Journey: Evening Wind-down
1. **Review day** → "What did I accomplish today?"
2. **Plan tomorrow** → "What's on my schedule for tomorrow?"
3. **Personal time** → "Set a timer for 30 minutes for meditation"
4. **Home control** → "Turn off all the lights except bedroom"

### Secondary Persona: The Digital Nomad
**Profile:** 25-40 years old, remote worker, values flexibility and mobility

**Key Needs:**
- Hands-free task management while traveling
- Quick information access without pulling out devices
- Time zone-aware scheduling
- Location-based reminders

### Tertiary Persona: The Smart Home Enthusiast
**Profile:** 28-50 years old, invested in home automation, values convenience

**Key Needs:**
- Voice control for all smart home devices
- Scene and automation management
- Status monitoring without checking apps
- Integration with existing smart home ecosystem

## Requirements

### Functional Requirements

#### FR1: Real-Time Voice Interaction
- **FR1.1:** Accept continuous voice input via microphone
- **FR1.2:** Detect speech boundaries with <300ms latency (VAD)
- **FR1.3:** Transcribe speech to text in real-time
- **FR1.4:** Maintain conversational context across multiple turns
- **FR1.5:** Generate natural language responses
- **FR1.6:** Synthesize speech output with natural-sounding voice
- **FR1.7:** Stream audio output with <500ms total latency

#### FR2: Pipeline Architecture
- **FR2.1:** Implement modular processor pipeline (Input → VAD → STT → LLM → TTS → Output)
- **FR2.2:** Support parallel processing where possible
- **FR2.3:** Enable service swapping without code rewrites
- **FR2.4:** Implement graceful error handling and recovery
- **FR2.5:** Log all pipeline events for debugging

#### FR3: Service Integrations
- **FR3.1:** Integrate Deepgram for speech-to-text
- **FR3.2:** Integrate OpenAI GPT-4 for language understanding
- **FR3.3:** Integrate Cartesia for text-to-speech
- **FR3.4:** Support WebRTC transport for audio streaming
- **FR3.5:** Enable service configuration via environment variables

#### FR4: Context Management
- **FR4.1:** Maintain conversation history (minimum 10 turns)
- **FR4.2:** Implement context aggregation for user and assistant
- **FR4.3:** Define system prompt for assistant personality
- **FR4.4:** Support context pruning for long conversations
- **FR4.5:** Preserve critical context across sessions

#### FR5: Session Management
- **FR5.1:** Initialize session on client connection
- **FR5.2:** Clean up resources on disconnection
- **FR5.3:** Handle multiple concurrent sessions
- **FR5.4:** Provide session status monitoring

#### FR6: Development & Testing
- **FR6.1:** Local development server at http://localhost:7860
- **FR6.2:** Web-based client for testing voice interaction
- **FR6.3:** Debug logging for all pipeline stages
- **FR6.4:** Metrics collection for latency monitoring

### Non-Functional Requirements

#### NFR1: Performance
- **Target Latency:** 500-800ms end-to-end response time
  - VAD detection: <300ms
  - STT transcription: streaming, <200ms first word
  - LLM response: streaming, <500ms first token
  - TTS synthesis: streaming, <200ms first audio
- **Throughput:** Support at least 10 concurrent voice sessions
- **Reliability:** 99% uptime during development phase

#### NFR2: Scalability
- **Horizontal scaling:** Support multiple bot instances
- **Resource efficiency:** <2GB RAM per session
- **Connection handling:** Graceful degradation under load

#### NFR3: Security
- **API keys:** Stored in environment variables, never committed
- **Data privacy:** No conversation logging in production
- **Transport security:** Encrypted WebRTC connections
- **Authentication:** (Future: user authentication required)

#### NFR4: Maintainability
- **Code quality:** Type hints, docstrings, PEP 8 compliance
- **Documentation:** Inline comments, architecture diagrams
- **Configuration:** Environment-based service configuration
- **Testing:** Unit tests for processors, integration tests for pipeline

#### NFR5: Usability
- **Voice quality:** Natural, clear speech synthesis
- **Response accuracy:** High intent recognition rate
- **Error messages:** Clear, actionable error communication
- **Latency perception:** Responses feel immediate (<1 second)

## Success Criteria

### Quantitative Metrics

1. **Latency Targets**
   - ✅ 95th percentile end-to-end latency <800ms
   - ✅ Average latency <600ms
   - ✅ VAD detection <300ms

2. **Accuracy Metrics**
   - ✅ STT word error rate <5%
   - ✅ Intent recognition accuracy >90%
   - ✅ Successful completion rate >85%

3. **Reliability Metrics**
   - ✅ System uptime >99%
   - ✅ Error recovery success rate >95%
   - ✅ Session stability (no crashes) >99%

4. **User Experience**
   - ✅ Conversation feels natural (subjective evaluation)
   - ✅ Voice quality rated >4/5
   - ✅ Response relevance >90%

### Qualitative Success Indicators

1. **Developer Experience**
   - ✅ New developers can run locally in <15 minutes
   - ✅ Service swapping takes <5 minutes
   - ✅ Debugging pipeline issues is straightforward

2. **User Experience**
   - ✅ Users prefer voice over typing for quick tasks
   - ✅ Natural conversation flow (minimal repeats/clarifications)
   - ✅ Assistant feels responsive and attentive

3. **Technical Foundation**
   - ✅ Pipeline architecture supports easy feature additions
   - ✅ Modular design enables service experimentation
   - ✅ Codebase is maintainable and well-documented

## Technical Architecture

### High-Level Architecture

```
┌─────────────┐
│   Browser   │
│   Client    │
└──────┬──────┘
       │ WebRTC
       ↓
┌─────────────────────────────────────────────┐
│           Pipecat Pipeline                  │
│                                             │
│  Input → VAD → STT → Context → LLM →       │
│          TTS → Output                       │
└─────────────────────────────────────────────┘
       ↓         ↓        ↓
┌──────────┐ ┌─────────┐ ┌──────────┐
│ Deepgram │ │ OpenAI  │ │ Cartesia │
│   STT    │ │   LLM   │ │   TTS    │
└──────────┘ └─────────┘ └──────────┘
```

### Component Breakdown

#### 1. Transport Layer (WebRTC)
- **Purpose:** Audio streaming between client and server
- **Technology:** Daily.co or native WebRTC
- **Responsibilities:**
  - Receive audio input stream
  - Send audio output stream
  - Manage connection lifecycle

#### 2. Voice Activity Detection (VAD)
- **Technology:** Silero VAD
- **Configuration:** 0.2s stop threshold
- **Responsibilities:**
  - Detect speech start/end
  - Filter out silence and background noise
  - Trigger STT processing

#### 3. Speech-to-Text (STT)
- **Primary:** Deepgram Nova-2
- **Fallback:** AssemblyAI
- **Responsibilities:**
  - Real-time speech transcription
  - Streaming word delivery
  - Handle multiple languages (future)

#### 4. Context Aggregation
- **Technology:** LLMContextAggregatorPair
- **Responsibilities:**
  - Maintain conversation history
  - Format messages for LLM
  - Prune old context when needed

#### 5. Language Model (LLM)
- **Primary:** OpenAI GPT-4 Turbo
- **Fallback:** Anthropic Claude
- **System Prompt:**
  ```
  You are Alex, a helpful daily life assistant.

  Personality:
  - Concise and efficient (aim for 1-2 sentence responses)
  - Friendly and warm
  - Proactive in offering help
  - Patient with clarifications

  Capabilities (current):
  - General conversation
  - Information and explanations
  - Planning and scheduling discussions

  Response Guidelines:
  - Keep responses brief for voice interaction
  - Ask clarifying questions when uncertain
  - Acknowledge actions clearly
  - Use natural, conversational language
  ```

#### 6. Text-to-Speech (TTS)
- **Primary:** Cartesia (low latency)
- **Fallback:** ElevenLabs (high quality)
- **Voice Configuration:**
  - Professional, warm tone
  - Medium pacing
  - Clear enunciation

#### 7. Pipeline Runner
- **Responsibilities:**
  - Orchestrate all processors
  - Handle errors and retries
  - Emit metrics and logs
  - Manage task lifecycle

### Data Flow

```
User speaks → Microphone → WebRTC → VAD
    ↓
Speech detected → Audio frames → STT
    ↓
Transcribed text → User context aggregator
    ↓
Messages with history → LLM
    ↓
Streaming response tokens → Assistant context aggregator
    ↓
Response text → TTS
    ↓
Audio frames → WebRTC → Speaker → User hears
```

### Configuration Management

**Environment Variables (.env):**
```bash
# Required Services
DEEPGRAM_API_KEY=your_key
OPENAI_API_KEY=your_key
CARTESIA_API_KEY=your_key

# Optional
DAILY_API_KEY=your_key  # If using Daily transport
LOG_LEVEL=INFO
ENABLE_METRICS=true
```

## Constraints & Assumptions

### Technical Constraints

1. **Python Version:** Requires Python 3.10+ (3.12 recommended)
2. **Network Requirements:** Stable internet for API calls, WebRTC streaming
3. **API Costs:** Usage-based pricing for STT, LLM, TTS services
4. **Latency Dependencies:** Constrained by external API response times
5. **Browser Compatibility:** WebRTC support required (modern browsers only)

### Business Constraints

1. **Budget:** API costs for development phase (~$50-100/month estimated)
2. **Timeline:** Foundation must be complete for follow-on features
3. **Resources:** Single developer for initial implementation
4. **Expertise:** Requires familiarity with Python async/await patterns

### Assumptions

1. **API Availability:** External services (Deepgram, OpenAI, Cartesia) maintain >99% uptime
2. **Service Quality:** STT/TTS quality meets user expectations without extensive tuning
3. **User Environment:** Users have quality microphone and speakers
4. **Network Quality:** Users have stable broadband internet (>1Mbps)
5. **Development Setup:** Developer has access to create accounts and obtain API keys

## Dependencies

### External Dependencies

#### Required Services (API Keys Needed)
1. **Deepgram**
   - Account creation: https://deepgram.com
   - Pricing: Pay-as-you-go
   - Criticality: High (primary STT)

2. **OpenAI**
   - Account creation: https://platform.openai.com
   - Pricing: Per-token
   - Criticality: High (primary LLM)

3. **Cartesia**
   - Account creation: https://cartesia.ai
   - Pricing: Pay-as-you-go
   - Criticality: High (primary TTS)

4. **Daily.co** (Optional)
   - Account creation: https://daily.co
   - Pricing: Free tier available
   - Criticality: Medium (can use alternative transport)

#### Python Dependencies
```toml
[dependencies]
pipecat-ai = "^0.1.0"
python-dotenv = "^1.0.0"
```

### Internal Dependencies

1. **Development Environment**
   - `uv` package manager installed
   - Python 3.10+ installed
   - Git for version control

2. **Knowledge Dependencies**
   - Understanding of async Python
   - Familiarity with WebRTC concepts
   - Basic pipeline architecture knowledge

3. **Infrastructure**
   - Local development machine (8GB+ RAM recommended)
   - Internet connectivity
   - Audio I/O devices

## Out of Scope

The following are explicitly **NOT** part of pipecat-base and will be addressed in future PRDs:

### Future Features (Separate PRDs)
1. **Calendar Integration** - Actual calendar API connections
2. **Task Management** - Todo list database and CRUD operations
3. **Smart Home Control** - Home Assistant integration
4. **Email/Messaging** - Communication service integrations
5. **Web Search** - Real-time information retrieval
6. **Multi-User Support** - User authentication and profiles
7. **Mobile Apps** - Native iOS/Android applications
8. **Persistent Storage** - Database for conversation history
9. **Advanced AI Features** - RAG, function calling, tools
10. **Production Deployment** - Cloud hosting, auto-scaling

### Explicitly Excluded
1. **GUI/Dashboard** - No administrative interface (CLI only)
2. **Payment Processing** - No billing or subscription management
3. **Analytics Dashboard** - No usage analytics UI
4. **Custom Voice Training** - Using pre-built TTS voices only
5. **Offline Mode** - Requires internet connectivity
6. **Video Processing** - Audio-only for now
7. **Multi-Language** - English only for initial version
8. **Custom Wake Word** - No "Hey Alex" activation (manual start)

## Implementation Phases

### Phase 1: Foundation Setup (Week 1)
**Goal:** Get basic Pipecat pipeline running locally

**Tasks:**
1. Set up development environment
2. Clone pipecat-quickstart repository
3. Configure API keys for Deepgram, OpenAI, Cartesia
4. Run basic example and verify all services work
5. Test voice interaction end-to-end

**Success Criteria:**
- ✅ Can run `uv run bot.py` successfully
- ✅ Can speak to assistant and receive voice responses
- ✅ Latency feels acceptable (<1 second)

### Phase 2: Custom Configuration (Week 1-2)
**Goal:** Customize pipeline for daily assistant use case

**Tasks:**
1. Define custom system prompt for assistant personality
2. Configure VAD for optimal responsiveness
3. Tune STT/TTS settings for clarity and speed
4. Implement robust error handling
5. Add comprehensive logging

**Success Criteria:**
- ✅ Assistant responds with appropriate personality
- ✅ VAD correctly detects speech boundaries
- ✅ Errors are logged and handled gracefully

### Phase 3: Context Enhancement (Week 2)
**Goal:** Improve conversation quality with better context management

**Tasks:**
1. Implement conversation history management
2. Add context pruning for long conversations
3. Test multi-turn conversations
4. Optimize token usage for LLM calls

**Success Criteria:**
- ✅ Assistant remembers conversation context
- ✅ Multi-turn conversations flow naturally
- ✅ No context overflow errors

### Phase 4: Monitoring & Metrics (Week 2-3)
**Goal:** Add observability for performance tracking

**Tasks:**
1. Enable built-in metrics collection
2. Implement latency tracking
3. Add usage cost monitoring
4. Create simple dashboard for metrics review

**Success Criteria:**
- ✅ Can measure end-to-end latency
- ✅ Can track API usage and costs
- ✅ Can identify performance bottlenecks

### Phase 5: Documentation & Handoff (Week 3)
**Goal:** Document implementation for future development

**Tasks:**
1. Update pipecat-reference.md with learnings
2. Create architecture diagrams
3. Write setup instructions
4. Document configuration options
5. Create troubleshooting guide

**Success Criteria:**
- ✅ New developer can set up in <15 minutes
- ✅ Common issues have documented solutions
- ✅ Architecture is clearly explained

## Risks & Mitigations

### Risk 1: API Cost Overruns
**Probability:** Medium | **Impact:** Medium

**Mitigation:**
- Set up API usage alerts
- Monitor costs daily during development
- Implement rate limiting if needed
- Use cheaper models for testing (GPT-3.5)

### Risk 2: Latency Exceeds Targets
**Probability:** Low | **Impact:** High

**Mitigation:**
- Test latency early and often
- Have backup service providers identified
- Optimize pipeline configuration
- Consider geographic API endpoint selection

### Risk 3: Poor Voice Quality
**Probability:** Low | **Impact:** Medium

**Mitigation:**
- Test multiple TTS voices before committing
- Gather user feedback early
- Have ElevenLabs as fallback for quality
- Optimize audio settings (sample rate, bitrate)

### Risk 4: Service Outages
**Probability:** Low | **Impact:** High

**Mitigation:**
- Implement health checks for all services
- Have fallback providers configured
- Graceful degradation strategy
- User-friendly error messages

### Risk 5: Development Complexity
**Probability:** Medium | **Impact:** Medium

**Mitigation:**
- Start with quickstart template (proven foundation)
- Follow Pipecat documentation closely
- Join Discord community for support
- Iterate in small, testable increments

## Testing Strategy

### Unit Testing
- VAD configuration validation
- Context aggregation logic
- Error handling paths
- Configuration parsing

### Integration Testing
- Full pipeline execution
- Service connectivity
- Session lifecycle
- Multi-turn conversations

### Performance Testing
- Latency measurement (p50, p95, p99)
- Concurrent session handling
- Memory usage profiling
- API rate limiting behavior

### User Acceptance Testing
- Natural conversation flow
- Response accuracy
- Voice quality assessment
- Error recovery experience

## Future Considerations

### Extensibility Points

1. **Plugin Architecture**
   - Custom processors for future features
   - Service adapters for new AI providers
   - Transport options for different platforms

2. **Tool Integration**
   - Function calling framework for LLM
   - API integration layer
   - Database connectors

3. **Multi-Modal Expansion**
   - Video processing capability
   - Screen sharing integration
   - Image understanding

### Scaling Path

1. **Horizontal Scaling**
   - Container-based deployment
   - Load balancer for multiple instances
   - Session affinity management

2. **Optimization Opportunities**
   - Model caching
   - Response caching for common queries
   - Streaming optimizations

## Glossary

- **Frames:** Data packages flowing through the Pipecat pipeline
- **Processor:** Specialized component that handles specific frame types
- **Pipeline:** Chain of processors orchestrating data flow
- **VAD:** Voice Activity Detection - identifies speech boundaries
- **STT:** Speech-to-Text - transcription service
- **TTS:** Text-to-Speech - voice synthesis service
- **LLM:** Large Language Model - AI for understanding and generation
- **WebRTC:** Web Real-Time Communication - protocol for streaming
- **Transport:** Component managing network communication

## References

- **Pipecat Documentation:** https://docs.pipecat.ai
- **Pipecat Quickstart:** https://github.com/pipecat-ai/pipecat-quickstart
- **Pipecat Reference:** `.claude/docs/pipecat-reference.md`
- **Deepgram Docs:** https://developers.deepgram.com
- **OpenAI Docs:** https://platform.openai.com/docs
- **Cartesia Docs:** https://docs.cartesia.ai

---

## Next Steps

After PRD approval, run:
```
/pm:prd-parse pipecat-base
```

This will create an implementation epic with detailed tasks and sub-issues for building out the pipecat-base foundation.
