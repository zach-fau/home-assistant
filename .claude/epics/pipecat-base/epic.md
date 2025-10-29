---
name: pipecat-base
status: backlog
created: 2025-10-29T00:15:21Z
progress: 0%
prd: .claude/prds/pipecat-base.md
github: null
---

# Epic: Pipecat-Base Foundation

## Overview

Implement a production-ready voice AI assistant foundation using Pipecat framework. This epic establishes real-time voice interaction (500-800ms latency) with modular pipeline architecture, enabling natural conversation for daily life management. The implementation leverages the existing pipecat-quickstart template to minimize custom code and accelerate delivery.

**Approach:** Use pipecat-quickstart as the foundation, customize for daily assistant use case, add monitoring and documentation. Focus on configuration over implementation.

## Architecture Decisions

### 1. Use Pipecat Quickstart Template
**Decision:** Fork/clone pipecat-quickstart instead of building from scratch
**Rationale:**
- Proven, production-ready architecture
- Reduces implementation time from weeks to days
- Includes best practices and optimizations
- Active maintenance and community support

### 2. Service Selection
**Decision:** Deepgram (STT) + OpenAI GPT-4 (LLM) + Cartesia (TTS)
**Rationale:**
- Deepgram: Best latency/accuracy balance for real-time
- OpenAI: Superior context understanding, function calling ready for future
- Cartesia: Ultra-low latency TTS, natural voice quality
- All have proven Pipecat integrations

### 3. Transport Layer
**Decision:** Use Daily.co WebRTC transport (from quickstart)
**Rationale:**
- Included in quickstart template
- Handles WebRTC complexity
- Free tier sufficient for development
- Easy to swap later if needed

### 4. Context Management
**Decision:** LLMContextAggregatorPair with 10-turn history
**Rationale:**
- Built into Pipecat
- Sufficient for conversational flow
- Prevents token bloat
- Easy to extend later

### 5. Development Environment
**Decision:** Local-first with uv package manager
**Rationale:**
- Fast iteration cycles
- No cloud costs during development
- Easy debugging
- Quickstart template is optimized for local dev

## Technical Approach

### Minimal Custom Code Strategy

**Leverage Existing:**
- ✅ Pipeline architecture (from quickstart)
- ✅ Service integrations (from quickstart)
- ✅ WebRTC transport (from quickstart)
- ✅ VAD configuration (from quickstart)
- ✅ Web client UI (from quickstart)

**Customize Only:**
- System prompt for daily assistant personality
- Voice selection for TTS
- Logging configuration
- Metrics collection
- Documentation

### File Structure
```
pipecat-base/
├── bot.py                    # Main pipeline (minimal changes from quickstart)
├── .env                      # API keys and configuration
├── pyproject.toml            # Dependencies (from quickstart)
├── README.md                 # Setup and usage documentation
├── docs/
│   └── architecture.md       # Architecture documentation
└── tests/                    # Basic integration tests
    └── test_pipeline.py
```

### Configuration Over Code

**System Prompt** (bot.py):
```python
system_prompt = """
You are Alex, a helpful daily life assistant.

Personality:
- Concise and efficient (1-2 sentence responses)
- Friendly and warm
- Proactive in offering help
- Patient with clarifications

Capabilities (current):
- General conversation and information
- Planning and scheduling discussions
- Helpful explanations and advice

Response Guidelines:
- Keep responses brief for voice interaction
- Ask clarifying questions when uncertain
- Acknowledge actions clearly
- Use natural, conversational language
"""
```

**Voice Configuration** (bot.py):
```python
tts = CartesiaTTSService(
    api_key=os.getenv("CARTESIA_API_KEY"),
    voice_id="a0e99841-438c-4a64-b679-ae501e7d6091",  # Professional, warm tone
)
```

**VAD Configuration** (bot.py):
```python
vad = SileroVADAnalyzer(
    stop_secs=0.2  # Balance between responsiveness and false interruptions
)
```

### Infrastructure

**Local Development:**
- Run via `uv run bot.py`
- Access at `http://localhost:7860/client`
- Hot reload for quick iteration

**Monitoring:**
```python
params = PipelineParams(
    enable_metrics=True,
    enable_usage_metrics=True,
    log_level="INFO"
)
```

**No Production Deployment Yet:**
- Out of scope for this epic
- Focus on local development perfection
- Production deployment in future epic

## Implementation Strategy

### Phase 1: Foundation (Priority: High)
**Goal:** Get quickstart running with our API keys

**Tasks:**
1. Clone pipecat-quickstart
2. Configure API keys (Deepgram, OpenAI, Cartesia)
3. Verify basic voice interaction works
4. Document setup process

**Success:** Can speak to assistant and get responses

### Phase 2: Customization (Priority: High)
**Goal:** Customize for daily assistant use case

**Tasks:**
1. Update system prompt for "Alex" personality
2. Select and configure optimal TTS voice
3. Tune VAD responsiveness
4. Add structured logging
5. Configure metrics collection

**Success:** Assistant has appropriate personality and behavior

### Phase 3: Testing & Validation (Priority: Medium)
**Goal:** Ensure quality and reliability

**Tasks:**
1. Measure end-to-end latency (target <800ms p95)
2. Test multi-turn conversation flow
3. Verify error handling and recovery
4. Create basic integration tests
5. Document known issues and workarounds

**Success:** Meets all NFRs and quality gates

### Phase 4: Documentation (Priority: Medium)
**Goal:** Enable future development

**Tasks:**
1. Write comprehensive README
2. Document architecture decisions
3. Create troubleshooting guide
4. Update pipecat-reference.md with learnings
5. Record performance benchmarks

**Success:** New developer can set up in <15 minutes

## Task Breakdown Preview

Simplified to 8 high-level tasks (aim for <10 total):

- [ ] **T1: Environment Setup** - Install dependencies, clone quickstart, verify prerequisites
- [ ] **T2: Service Configuration** - Obtain API keys, configure .env, verify service connectivity
- [ ] **T3: Basic Pipeline Validation** - Run quickstart bot, test voice interaction end-to-end
- [ ] **T4: Assistant Customization** - Update system prompt, select TTS voice, configure personality
- [ ] **T5: Performance Tuning** - Optimize VAD, measure latency, tune for <800ms target
- [ ] **T6: Monitoring & Logging** - Enable metrics, add structured logging, create cost tracking
- [ ] **T7: Quality Assurance** - Integration tests, multi-turn conversation validation, error scenarios
- [ ] **T8: Documentation** - README, architecture docs, troubleshooting guide, setup video

## Dependencies

### External Services (Critical Path)
1. **Deepgram Account** - Create account, obtain API key, verify quota
2. **OpenAI Account** - Create account, obtain API key, verify quota
3. **Cartesia Account** - Create account, obtain API key, verify quota
4. **Daily.co Account** (Optional) - Free tier sufficient for development

### Development Environment
- Python 3.10+ (3.12 recommended)
- `uv` package manager installed
- Git for version control
- Microphone and speakers for testing

### Knowledge Prerequisites
- Basic Python familiarity
- Understanding of async/await patterns (can be learned during implementation)
- Comfort with command-line tools

## Success Criteria (Technical)

### Performance Benchmarks
- ✅ **Latency:** p95 end-to-end <800ms, average <600ms
- ✅ **VAD Response:** Speech detection <300ms
- ✅ **Memory:** <2GB RAM per session
- ✅ **Stability:** No crashes during 30-minute conversation

### Quality Gates
- ✅ **STT Accuracy:** <5% word error rate in testing
- ✅ **Voice Quality:** Natural-sounding, clear enunciation
- ✅ **Context Memory:** Maintains context across 10+ turn conversation
- ✅ **Error Recovery:** Graceful handling of service failures

### Developer Experience
- ✅ **Setup Time:** New developer productive in <15 minutes
- ✅ **Documentation:** Complete README with troubleshooting
- ✅ **Code Quality:** Type hints, docstrings, PEP 8 compliance
- ✅ **Testing:** Basic integration test suite

### User Experience (Subjective)
- ✅ **Natural Flow:** Conversations feel smooth and responsive
- ✅ **Personality:** Assistant feels helpful and friendly
- ✅ **Clarity:** Voice output is easy to understand
- ✅ **Reliability:** Consistent behavior across sessions

## Estimated Effort

### Timeline: 5-7 Days (Single Developer)

**Day 1-2: Setup & Validation**
- Environment setup
- Service configuration
- Basic validation

**Day 3-4: Customization & Tuning**
- System prompt refinement
- Voice selection
- Performance optimization

**Day 5: Testing**
- Latency measurements
- Multi-turn conversations
- Error scenarios

**Day 6-7: Documentation**
- Architecture documentation
- Setup instructions
- Troubleshooting guide

### Resource Requirements
- **Developer Time:** 5-7 full days
- **API Costs:** ~$10-20 for development/testing
- **Infrastructure:** Local machine only (8GB+ RAM recommended)

### Critical Path Items
1. **Day 1 AM:** API keys obtained (cannot proceed without)
2. **Day 1 PM:** Basic pipeline running (validates entire approach)
3. **Day 3:** Latency validation (may require service adjustments)

## Risks & Mitigations

### Risk 1: API Key Delays
**Impact:** Blocks all work
**Mitigation:** Start API account creation immediately, have credit card ready for verification

### Risk 2: Latency Exceeds Target
**Impact:** Poor user experience
**Mitigation:** Test early (Day 1), have backup service providers ready (AssemblyAI, ElevenLabs)

### Risk 3: Voice Quality Issues
**Impact:** Medium - can iterate on voice selection
**Mitigation:** Test multiple Cartesia voices, have ElevenLabs as fallback

### Risk 4: Quickstart Template Issues
**Impact:** Low - template is well-maintained
**Mitigation:** Check GitHub issues first, join Pipecat Discord for support

## Out of Scope (Future Epics)

Explicitly excluded from this epic:

- ❌ Calendar API integration
- ❌ Task management database
- ❌ Smart home control (Home Assistant)
- ❌ Web search capabilities
- ❌ Function calling / tool use
- ❌ Persistent conversation storage
- ❌ User authentication
- ❌ Production cloud deployment
- ❌ Mobile applications
- ❌ Multi-language support

These will be separate epics building on this foundation.

## Validation & Acceptance

### Must Have (Blocking)
1. Can run `uv run bot.py` successfully
2. Voice interaction works end-to-end
3. Latency <800ms (p95)
4. Multi-turn context maintained
5. Errors handled gracefully
6. Documentation complete

### Should Have (Important)
1. Metrics collection enabled
2. Integration tests passing
3. Architecture documented
4. Troubleshooting guide created

### Nice to Have (Optional)
1. Video demo of setup process
2. Cost tracking dashboard
3. Multiple voice options tested
4. Performance optimization notes

## Next Steps

After epic creation:
```bash
/pm:epic-decompose pipecat-base
```

This will create 8 detailed task files with:
- Specific implementation steps
- Acceptance criteria
- Code examples
- Testing procedures

## Tasks Created

- [ ] 001.md - Environment Setup (parallel: false)
- [ ] 002.md - Service Configuration (parallel: false, depends on: 001)
- [ ] 003.md - Basic Pipeline Validation (parallel: false, depends on: 001, 002)
- [ ] 004.md - Assistant Customization (parallel: true, depends on: 003)
- [ ] 005.md - Performance Tuning (parallel: true, depends on: 003)
- [ ] 006.md - Monitoring & Logging (parallel: true, depends on: 003)
- [ ] 007.md - Quality Assurance (parallel: false, depends on: 004, 005, 006)
- [ ] 008.md - Documentation (parallel: false, depends on: 007)

**Total tasks:** 8
**Parallel tasks:** 3 (tasks 004, 005, 006 can run simultaneously)
**Sequential tasks:** 5 (tasks 001, 002, 003, 007, 008 must run in order)
**Estimated total effort:** 16-23 hours (~3-5 working days)

**Critical Path:** 001 → 002 → 003 → (004 || 005 || 006) → 007 → 008

---

**Key Success Factor:** Leverage existing quickstart template to minimize custom code. Focus on configuration, documentation, and validation rather than building from scratch.
