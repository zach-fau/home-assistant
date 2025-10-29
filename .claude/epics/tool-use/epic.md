---
name: tool-use
status: backlog
created: 2025-10-29T21:20:46Z
updated: 2025-10-29T21:54:09Z
progress: 0%
prd: .claude/prds/tool-use.md
github: https://github.com/zach-fau/home-assistant/issues/11
---

# Epic: Tool Use for Alex Voice Assistant

## Overview

Add function calling capabilities to Alex, enabling voice-controlled interactions with external tools and services. Transform Alex from conversational to actionable - controlling smart home devices, managing tasks, and searching the web entirely through voice commands.

**Core Value:** Voice becomes the fastest interface to your digital and physical world.

**Approach:** Leverage Pipecat's existing OpenAI function calling support. Build incrementally in 3 phases: (1) Core framework + Home Assistant, (2) Google Tasks, (3) Web search APIs.

---

## Architecture Decisions

### 1. Leverage Pipecat's Native Function Calling

**Decision:** Use Pipecat's built-in `FunctionSchema` and `register_function()` APIs

**Rationale:**
- Already integrated with OpenAI's function calling
- Handles async execution automatically
- Event handlers for lifecycle management
- No need to build custom framework

**Alternative Rejected:** Custom function orchestration layer (unnecessary complexity)

### 2. Modular Function Organization

**Decision:** Create `functions/` directory with separate modules per integration

**Structure:**
```
functions/
├── __init__.py          # Registration coordinator
├── home_assistant.py    # HA REST API calls
├── google_tasks.py      # Google Tasks OAuth
├── web_search.py        # Tavily Search API
└── schemas.py           # Shared FunctionSchema definitions
```

**Rationale:**
- Easy to add new integrations
- Clear separation of concerns
- Each module can be developed/tested independently
- Matches Pipecat examples pattern

### 3. Configuration-Driven Entity Mapping

**Decision:** Store entity ID mappings in JSON config file, not hardcoded

**Example:** `config/ha_entities.json`
```json
{
  "living_room_lights": "light.living_room_main",
  "bedroom_lights": "light.bedroom_ceiling"
}
```

**Rationale:**
- User can add devices without code changes
- Supports friendly names in voice commands
- Easy to maintain and update
- Separates data from code

### 4. Dynamic Voice Feedback via LLM

**Decision:** Let OpenAI generate varied acknowledgment phrases (don't hardcode)

**Implementation:** Use `on_function_calls_started` event, let LLM naturally transition
- "Sure, let me check..."
- "Give me a second..."
- "On it!"

**Rationale:**
- More natural conversation flow
- Masks latency perception
- Prevents robotic repetition
- Leverages existing LLM capabilities

### 5. Web Search via Tavily API

**Decision:** Use Tavily Search API for web search, reserve Playwright for complex automation only

**Rationale:**
- Tavily is LLM-optimized (returns structured, ready-to-summarize results)
- API calls are 5-10x faster than browser automation (<2 sec vs 10-15 sec)
- Simpler implementation than browser-based search
- Lower resource usage
- Free tier: 1,000 searches/month (sufficient for personal use)

**When to Use Playwright:** Form filling, multi-page navigation, screenshot capture (only when API unavailable)

### 6. Async-First Design

**Decision:** All function calls must be async, return results via callback

**Pattern:**
```python
async def control_light(params: FunctionCallParams):
    # Do work
    await params.result_callback(result)
```

**Rationale:**
- Prevents blocking voice pipeline
- Supports concurrent operations
- Matches Pipecat's execution model

---

## Technical Approach

### Core Components

#### 1. Function Calling Framework (Already Exists in Pipecat)
- **What:** OpenAI function calling integration
- **What We Build:** Registration logic, event handlers
- **Complexity:** Low (leverage existing)

#### 2. Home Assistant Integration
- **Protocol:** REST API over HTTP
- **Auth:** Long-lived access token (Bearer token)
- **Operations:** Light control, switch control, device queries
- **Key Challenge:** Entity ID discovery and mapping

#### 3. Google Tasks Integration
- **Protocol:** Google Tasks API (REST)
- **Auth:** OAuth 2.0 with token refresh
- **Operations:** Create, list, complete tasks
- **Key Challenge:** OAuth flow setup

#### 4. Web Search Integration
- **API:** Tavily Search
- **Protocol:** REST API with API key
- **Operations:** Search, extract top 3-5 results
- **Key Challenge:** Result summarization for voice

### Modified Files

**Existing Files to Modify:**
1. `bot.py` - Add function registration call
2. `.env` - Add API keys/tokens
3. `pyproject.toml` - Add dependencies (httpx, google-api-python-client)

**New Files to Create:**
4. `functions/__init__.py` - Registration coordinator
5. `functions/home_assistant.py` - HA integration
6. `functions/google_tasks.py` - Tasks integration
7. `functions/web_search.py` - Tavily Search integration
8. `functions/schemas.py` - Function schemas
9. `config/ha_entities.json` - Entity mapping
10. `config/.gitignore` - Ensure config files tracked

**Total New Code:** ~500-800 lines across 8 files

---

## Implementation Strategy

### Phase 1: Core + Home Assistant (Week 1-2)

**Goal:** Voice-controlled lights and switches

**Key Deliverable:** "Alex, turn off the living room lights" works end-to-end

**Critical Path:**
1. Set up `functions/` module structure
2. Implement Home Assistant REST API client
3. Register light control function
4. Test with 3-5 devices
5. Add error handling

**Risk Mitigation:**
- Start with single function (lights on/off)
- Add complexity incrementally
- Test frequently

### Phase 2: Google Tasks (Week 3-4)

**Goal:** Voice task management

**Key Deliverable:** "Alex, add buy milk to my tasks" works

**Critical Path:**
1. Set up Google OAuth (one-time)
2. Implement task creation
3. Implement task listing
4. Add task completion

**Risk Mitigation:**
- OAuth setup is one-time pain, document thoroughly
- Test token refresh logic
- Handle auth failures gracefully

### Phase 3: Web Search (Week 5-7)

**Goal:** Voice-activated web search with results

**Key Deliverable:** "Alex, search for best coffee shops" returns summarized results

**Critical Path:**
1. Integrate Tavily Search API
2. Implement result extraction
3. Test voice summarization
4. Optimize response formatting

**Risk Mitigation:**
- Monitor API usage (1,000 searches/month free tier)
- Cache frequent searches if needed
- Handle rate limits gracefully

### Testing Approach

**Manual Testing Checklist per Phase:**
1. Happy path works (command → action → confirmation)
2. Error cases handled (service down, auth fail, network issues)
3. Latency acceptable (<3 sec for HA, <2 sec for search)
4. Multiple commands in sequence work
5. Voice feedback feels natural

**No Automated Tests:** MVP acceptable, add later if needed

---

## Task Breakdown Preview

High-level task categories (will be decomposed into detailed tasks):

### Phase 1: Foundation (3 tasks)
- [ ] **Task 1:** Function calling framework setup
  - Create `functions/` module structure
  - Implement registration system
  - Add event handlers for feedback
  - Update `bot.py` with function registration

- [ ] **Task 2:** Home Assistant integration
  - Implement REST API client
  - Create light control function
  - Add entity mapping config
  - Test with 3-5 devices

- [ ] **Task 3:** Error handling & configuration
  - Add graceful error handling
  - Implement retry logic
  - Create configuration management
  - Document setup process

### Phase 2: Productivity (2 tasks)
- [ ] **Task 4:** Google Tasks OAuth setup
  - Set up Google Cloud project
  - Implement OAuth flow
  - Add token refresh logic
  - Test authentication

- [ ] **Task 5:** Google Tasks operations
  - Implement task creation
  - Add task listing
  - Add task completion
  - Test multi-turn task management

### Phase 3: Web & Advanced (2-3 tasks)
- [ ] **Task 6:** Web search API integration
  - Integrate Tavily Search API
  - Implement result extraction
  - Add voice summarization
  - Test with various queries

- [ ] **Task 7:** Additional integrations (optional)
  - Add weather API
  - Add news API
  - Expand web search capabilities
  - Test multi-step workflows

- [ ] **Task 8:** Polish & optimization (optional)
  - Performance tuning
  - Enhanced error messages
  - Usage analytics
  - Documentation updates

**Total: 7-8 tasks** (meets <10 requirement)

---

## Dependencies

### External Dependencies

**Required Services:**
1. Home Assistant instance (local/VPN-accessible)
   - Long-lived access token
   - Entity IDs for devices
2. Google Cloud Platform account
   - Tasks API enabled
   - OAuth 2.0 credentials
3. Tavily Search API account
   - Free tier: 1,000 searches/month
   - API key

### Internal Dependencies

**Prerequisites:**
1. Pipecat-Base Tasks 001-004 complete ✅
2. Alex personality configured ✅
3. Stable voice pipeline ✅

**Configuration:**
1. `.env` file with API keys
2. Network access to Home Assistant
3. Internet connection for Google/search APIs

### Python Packages

**New Dependencies:**
```toml
httpx = "^0.24.0"                  # HTTP client
google-api-python-client = "^2.0"  # Google APIs
google-auth-httplib2 = "^0.2.0"    # Google auth
google-auth-oauthlib = "^1.0.0"    # OAuth flow
```

**Optional:**
```toml
playwright = "^1.40.0"  # Browser automation (Phase 3 optional)
```

---

## Success Criteria (Technical)

### Performance Benchmarks

| Metric | Target | Measurement |
|--------|--------|-------------|
| Function call latency (HA) | <3 seconds | Subjective timing |
| Function call latency (Search) | <2 seconds | Subjective timing |
| Function call latency (Tasks) | <3 seconds | Subjective timing |
| Voice feedback delay | <1 second | Immediate perception |
| Success rate | >95% | Manual tracking |

### Quality Gates

**Phase 1 Complete When:**
- Can control 5+ Home Assistant devices reliably
- Errors handled gracefully (service down, wrong entity, etc.)
- Voice feedback feels natural (varied responses)
- User prefers voice over HA app for common tasks

**Phase 2 Complete When:**
- Can create/list/complete tasks via voice
- OAuth works and refreshes automatically
- Faster than opening Google Tasks app
- Multi-turn task management works

**Phase 3 Complete When:**
- Can search and get voice-summarized results
- Response time <2 seconds
- Results are relevant and useful
- 10+ total functions working

### Acceptance Criteria

From PRD:
1. 80% of HA interactions via voice within 1 week
2. 50% of tasks created via voice within 2 weeks
3. Commands work reliably (subjective: doesn't frustrate)
4. Response time feels acceptable
5. Prefer voice over traditional interfaces

---

## Estimated Effort

### Timeline

| Phase | Duration | Parallel | Total Elapsed |
|-------|----------|----------|---------------|
| Phase 1: Foundation | 2 weeks | No | 2 weeks |
| Phase 2: Tasks | 2 weeks | No | 4 weeks |
| Phase 3: Search | 2-3 weeks | Partially | 6-7 weeks |

**Total: 6-7 weeks** (building incrementally, testing frequently)

### Resource Requirements

**Developer:** 1 (you)
**Hours per Week:** Flexible (no hard deadlines)
**Environment:** Existing pipecat-quickstart setup

### Critical Path Items

1. **Week 1:** Function framework + basic HA integration
2. **Week 2:** Multiple HA devices + error handling
3. **Week 3:** Google OAuth setup (one-time pain)
4. **Week 4:** Task operations complete
5. **Week 5-6:** Web search API integration
6. **Week 7:** Polish & additional tools (optional)

### Complexity Assessment

| Task | Complexity | Risk |
|------|------------|------|
| Function framework | Low | Low (leverage Pipecat) |
| Home Assistant | Low | Low (simple REST API) |
| Google Tasks | Medium | Medium (OAuth setup) |
| Web Search | Low | Low (simple API calls) |
| Error Handling | Medium | Medium (many edge cases) |
| Browser Automation | High | High (defer to Phase 3) |

**Overall: Medium complexity** due to OAuth and integration testing

---

## Simplifications & Optimizations

**Leveraging Existing Functionality:**

1. **Pipecat's Function Calling** - Don't build custom framework
2. **OpenAI's LLM** - Generates dynamic feedback automatically
3. **Existing Voice Pipeline** - No changes to STT/TTS/VAD
4. **REST APIs** - Simple HTTP calls, no complex protocols
5. **JSON Config** - No custom DSL or complex configuration

**Scope Reductions:**

1. **No Automated Tests** - Manual testing sufficient for MVP
2. **No GUI** - Voice-only configuration
3. **Single User** - No access control or multi-user support
4. **No Production Deployment** - Local use only
5. **Basic Error Handling** - Graceful failures, no sophisticated retry logic initially
6. **Limited Playwright** - Only if absolutely needed, not for basic search

**Result: Achievable in 6-7 weeks with <800 lines of new code**

---

## Risk Mitigation

### Key Risks

1. **OAuth Setup Complexity**
   - **Mitigation:** Follow Google's quick start guide, document thoroughly
   - **Fallback:** Start with API key-based services first

2. **Function Call Latency Breaks Flow**
   - **Mitigation:** Dynamic voice feedback masks latency
   - **Fallback:** Add "working on it" acknowledgments

3. **Too Many Tools Overwhelm LLM**
   - **Mitigation:** Add tools incrementally, test after each
   - **Fallback:** Limit to 10-12 most useful tools

4. **Home Assistant Unavailable**
   - **Mitigation:** Graceful errors, retry logic
   - **Fallback:** Clear voice message, don't break conversation

5. **API Rate Limits**
   - **Mitigation:** Monitor usage, stay under free tiers
   - **Fallback:** Implement basic caching

---

## Next Steps

**After Epic Approval:**

1. Run `/pm:epic-decompose tool-use` to create detailed task files
2. Each task will include:
   - Specific implementation steps
   - Code examples
   - Testing checklist
   - Acceptance criteria
   - Dependencies and blockers

**Start Point:** Task 1 (Function Calling Framework Setup)

---

## Tasks Created

- [ ] #12 (12.md) - Function Calling Framework Setup (parallel: false, dependencies: none)
- [ ] #13 (13.md) - Home Assistant Integration (parallel: false, dependencies: #12)
- [ ] #14 (14.md) - Error Handling & Configuration (parallel: false, dependencies: #12, #13)
- [ ] #15 (15.md) - Google Tasks OAuth Setup (parallel: true, dependencies: #12)
- [ ] #16 (16.md) - Google Tasks Operations (parallel: false, dependencies: #12, #15)
- [ ] #17 (17.md) - Tavily Web Search Integration (parallel: true, dependencies: #12)
- [ ] #18 (18.md) - Additional Integrations (Optional) (parallel: false, dependencies: #12-#17)
- [ ] #19 (19.md) - Polish & Optimization (Optional) (parallel: false, dependencies: #12-#17)

**Total tasks:** 8
**Parallel tasks:** 2 (Tasks #15, #17 can run alongside Task #13)
**Sequential tasks:** 6
**Estimated total effort:** 48-73 hours across 6-7 weeks

**Critical Path:**
1. Task #12 (4-6 hours) → Foundational
2. Task #13 (8-12 hours) → Home Assistant integration
3. Task #14 (6-10 hours) → Error handling
4. Tasks #15-#17 can proceed in parallel after Task #12
5. Tasks #18-#19 are optional polish

---

## References

- **Research:** `/pipecat-quickstart/TOOL_USE_RESEARCH.md`
- **PRD:** `.claude/prds/tool-use.md`
- **Pipecat Examples:** https://github.com/pipecat-ai/pipecat/tree/main/examples
- **Home Assistant API:** https://developers.home-assistant.io/docs/api/rest/
- **Google Tasks API:** https://developers.google.com/tasks
- **Tavily API:** https://www.tavily.com/
