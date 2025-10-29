---
name: tool-use
description: Enable Alex voice assistant to interact with external tools and services via OpenAI function calling
status: backlog
created: 2025-10-29T01:04:47Z
---

# PRD: Tool Use for Alex Voice Assistant

## Executive Summary

Enable Alex to control the real world through voice commands by implementing tool/function calling capabilities. This transforms Alex from a conversational assistant into an actionable agent that can control smart home devices, manage tasks, search the web, and automate workflows - all through natural voice interaction.

**Value Proposition:** "Alex, turn off the living room lights" → Lights turn off. "Alex, add buy groceries to my tasks" → Task added to Google Tasks. Voice becomes the universal interface to your digital and physical world.

**Approach:** Leverage Pipecat's native OpenAI function calling support to incrementally add tool integrations, starting with highest-impact use cases (Home Assistant, Google Tasks) and expanding to web automation.

---

## Problem Statement

### What problem are we solving?

**Current State:** Alex can have conversations but cannot take actions in the real world. Users must manually switch between voice interaction and traditional interfaces (apps, switches, browsers) to accomplish tasks.

**Pain Points:**
1. **Context Switching:** "Alex, what's the weather?" → Alex responds → User must manually adjust thermostat
2. **Limited Utility:** Alex knows what to do but can't do it ("I can help with planning" vs actually creating calendar events)
3. **Friction:** Voice is fast for input but requires manual follow-through, negating speed benefits
4. **Fragmented Control:** Home automation, task management, web search all require separate interfaces

### Why is this important now?

1. **Foundation Complete:** Alex has stable voice pipeline (Tasks 001-004 complete)
2. **Technology Availability:** Pipecat supports function calling, APIs are accessible
3. **User Need:** You want faster, easier access to automation and information
4. **Incremental Approach:** Can build features one at a time without big-bang release

**Mission:** Make voice the fastest, easiest way to control your digital and physical environment.

---

## User Stories

### Primary Persona: You (Power User)

**Background:**
- Technical user comfortable with automation
- Uses Home Assistant for smart home control
- Manages tasks/calendar via Google services
- Values speed and efficiency
- Willing to iterate on rough features

### User Journeys

#### Journey 1: Smart Home Control via Voice

**Current Experience:**
1. Think "lights are too bright"
2. Pull out phone
3. Open Home Assistant app
4. Find light entity
5. Adjust brightness
6. Put phone away

**With Tool Use:**
1. Say "Alex, dim the living room lights to 30%"
2. Lights adjust immediately
3. Alex confirms: "Done, living room lights set to 30%"

**Pain Points Addressed:**
- Eliminates app switching
- Faster than manual control
- Works hands-free

#### Journey 2: Task Management

**Current Experience:**
1. Think of task while cooking
2. Forget task
3. OR: Wash hands, open Google Tasks app, type task, return to cooking

**With Tool Use:**
1. Say "Alex, add order chicken stock to my grocery list"
2. Alex: "Added to your tasks"
3. Continue cooking uninterrupted

#### Journey 3: Information Retrieval with Action

**Current Experience:**
1. Ask Alex "What's the weather?"
2. Alex: "75 degrees and sunny"
3. Manually think "should open windows"
4. Walk around opening windows

**With Tool Use:**
1. Ask Alex "What's the weather?"
2. Alex: "75 and sunny. Want me to open the smart blinds?"
3. You: "Yes"
4. Blinds open automatically

#### Journey 4: Natural Latency Masking

**Without Dynamic Feedback:**
1. "Alex, search for best coffee shops"
2. [Awkward 2-3 second silence]
3. Alex: "I found three options..." (feels slow)

**With Dynamic Feedback:**
1. "Alex, search for best coffee shops"
2. Alex: "Sure, let me look that up..." (immediate, <1 sec)
3. [Alex is talking, search happens in background]
4. Alex: "I found three highly rated options..." (feels instant)

**Pain Points Addressed:**
- Eliminates perceived latency
- More conversational and natural
- Varied responses prevent robotic feel

---

## Requirements

### Functional Requirements

#### FR1: Function Calling Framework

**Must Have:**
- Register functions with OpenAI LLM using Pipecat's `FunctionSchema`
- Execute functions asynchronously during conversation
- Return results to LLM for natural language response
- Handle function call lifecycle events (`on_function_calls_started`, etc.)
- Provide voice feedback during function execution ("Let me check...")

**Function Registration Example:**
```python
llm.register_function("control_light", control_light_handler)
```

#### FR2: Home Assistant Integration

**Must Have:**
- Control lights (on/off, brightness, color)
- Control switches (on/off)
- Query device states
- Use HA REST API with authentication

**Tool Definition:**
```
Function: control_device
Parameters:
  - entity_id: string (e.g., "light.living_room")
  - action: enum ["turn_on", "turn_off", "toggle"]
  - brightness: optional integer (0-255)
  - color: optional string (hex color)
```

**Example Commands:**
- "Turn off the bedroom lights"
- "Set living room lights to 50% brightness"
- "Turn on the kitchen switch"

#### FR3: Google Tasks Integration

**Must Have:**
- Create new tasks
- List tasks
- Mark tasks complete
- Use Google Tasks API with OAuth

**Tool Definition:**
```
Function: manage_task
Parameters:
  - action: enum ["create", "list", "complete"]
  - title: string (for create)
  - task_id: string (for complete)
  - notes: optional string
```

**Example Commands:**
- "Add buy milk to my tasks"
- "What's on my task list?"
- "Mark task XYZ as complete"

#### FR4: Web Search (Tavily/Brave API)

**Should Have:**
- Perform web searches via API (NOT browser automation)
- Extract top 3 results
- Summarize findings via voice
- Use Tavily (LLM-optimized) or Brave Search API

**Tool Definition:**
```
Function: web_search
Parameters:
  - query: string
  - num_results: integer (default 3)
  - search_api: enum ["tavily", "brave"] (default "tavily")
```

**Example Commands:**
- "Search for best Italian restaurants nearby"
- "Look up the capital of Mongolia"
- "Find the latest news on AI"

#### FR5: Browser Automation (Playwright - Optional)

**Nice to Have:**
- Navigate websites for complex interactions
- Fill forms
- Take screenshots
- Extract data from sites without APIs
- Use ONLY when API not available (slower than API calls)

**Tool Definition:**
```
Function: navigate_website
Parameters:
  - url: string
  - action: enum ["navigate", "click", "fill", "screenshot"]
  - selector: optional string (for click/fill)
  - text: optional string (for fill)
```

**Example Commands:**
- "Take a screenshot of example.com"
- "Navigate to my bank website" (followed by manual interaction)

#### FR6: Dynamic Voice Feedback

**Must Have:**
- Varied, natural responses during function execution (not static phrases)
- LLM generates contextual acknowledgments while function runs
- Examples:
  - "Sure, let me check on that..."
  - "Give me just a second..."
  - "Looking that up now..."
  - "On it!"
  - "Let me see..."
- Masks perceived latency (talking while searching)
- Different phrase each time for natural feel

**Implementation:**
```python
@llm.event_handler("on_function_calls_started")
async def on_function_start(service, function_calls):
    # Let LLM generate natural acknowledgment
    # This happens while function executes async in background
    # User hears response immediately, then result 2-3s later
    pass  # LLM automatically generates natural transition
```

#### FR7: Error Handling

**Must Have:**
- Graceful failures ("Sorry, I couldn't reach Home Assistant")
- Voice feedback during slow operations
- Retry logic for transient failures
- Clear error messages

#### FR8: Configuration Management

**Must Have:**
- Store API keys securely in `.env`
- Map friendly names to entity IDs (config file)
- Separate credentials from code

**Example Config:**
```json
{
  "home_assistant": {
    "url": "http://homeassistant.local:8123",
    "entities": {
      "living_room_lights": "light.living_room_main",
      "bedroom_lights": "light.bedroom_ceiling"
    }
  }
}
```

### Non-Functional Requirements

#### NFR1: Performance

- **Function Call Latency:**
  - Home Assistant: <3 seconds
  - Web Search (API): <2 seconds
  - Google Tasks: <3 seconds
  - Browser Automation: <15 seconds (when necessary)
- **Voice Feedback:** Immediate acknowledgment (<1 second)
- **Concurrent Operations:** Support multiple tools without blocking

#### NFR2: Reliability

- **Success Rate:** >95% for Home Assistant calls (when HA is available)
- **Availability:** Graceful degradation when services unavailable
- **Recovery:** Auto-retry on transient failures (network blips)

#### NFR3: Security

- **Credentials:** Store API keys in `.env` (gitignored)
- **OAuth:** Secure token refresh for Google APIs
- **Network:** Support VPN/local network for Home Assistant

#### NFR4: Maintainability

- **Modular Design:** Each integration in separate file
- **Schema-Driven:** Function schemas define contracts
- **Logging:** Comprehensive logs for debugging
- **Testing:** Manual testing checklist (no automated tests required yet)

#### NFR5: Scalability

- **Incremental:** Add tools one at a time
- **Extensible:** Easy to add new functions
- **No Limit:** Support 10+ tools without degradation

---

## Success Criteria

### Measurable Outcomes

1. **Tool Adoption:**
   - Use voice commands for 80% of Home Assistant interactions within 1 week
   - Create 50% of tasks via voice within 2 weeks

2. **User Satisfaction:**
   - Commands work reliably (subjective: "doesn't frustrate me")
   - Response time feels acceptable
   - Prefer voice over manual interface

3. **Capability:**
   - 5+ working tools by end of Phase 1
   - 10+ working tools by end of Phase 2
   - Complex multi-step workflows possible (Phase 3)

### Key Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Function call success rate | >95% | Manual tracking |
| Average response time (HA) | <3 sec | Subjective |
| Average response time (Web) | <10 sec | Subjective |
| Tools implemented | 5 (Phase 1) | Count |
| Daily voice commands | >10 | Self-reported |

### Definition of Success

"I can control my most common smart home devices and manage my tasks entirely through voice, and it's faster than using traditional interfaces."

---

## Constraints & Assumptions

### Technical Constraints

1. **Pipecat Limitations:**
   - Known issue: OpenAI Realtime may stop responding during function calls
   - Mitigation: Use async patterns, provide immediate feedback

2. **Network Dependencies:**
   - Home Assistant must be reachable
   - Google APIs require internet
   - Playwright requires stable connection

3. **Authentication:**
   - OAuth flows require manual setup
   - Tokens may expire and need refresh

### Resource Constraints

1. **Time:** Building incrementally, no hard deadlines
2. **Solo Developer:** Single user (you) building and testing
3. **Environment:** Linux (Fedora), Python 3.13, existing pipecat-quickstart

### Assumptions

1. **Home Assistant Available:** You have HA instance running locally
2. **Entity IDs Known:** You can provide entity IDs for devices
3. **Google Account:** You have access to Google Tasks/Calendar APIs
4. **Iteration:** Willing to test and provide feedback
5. **MVP Acceptable:** Rough features are okay, polish later

---

## Out of Scope

### Explicitly NOT Building (For Now)

1. **Production Deployment:** No cloud hosting, multi-user support, or public access
2. **Advanced NLP:** No custom entity recognition beyond OpenAI's capabilities
3. **Visual Interface:** No GUI for configuration or control
4. **Mobile App:** Voice only, no companion app
5. **Multi-Room Audio:** Single Alex instance, not distributed
6. **Claude Computer Use:** Too complex, defer to future (use Playwright instead)
7. **Automated Testing:** Manual testing acceptable for MVP
8. **Rate Limiting/Quotas:** Assume reasonable personal use
9. **Offline Mode:** Requires internet and external services
10. **Access Control:** Single user, no permissions/roles

### Future Considerations

- Multi-user support
- Advanced automation (routines, triggers)
- Learning/personalization
- Voice-only configuration
- Mobile companion app

---

## Dependencies

### External Dependencies

1. **Home Assistant:**
   - Running HA instance (local or VPN-accessible)
   - Long-lived access token
   - Known entity IDs

2. **Google APIs:**
   - GCP project with Tasks API enabled
   - OAuth 2.0 credentials
   - Token refresh mechanism

3. **OpenAI:**
   - Existing API key (already configured)
   - Function calling support (GPT-4)

4. **Python Packages:**
   - `httpx` (HTTP requests)
   - `google-api-python-client` (Google APIs)
   - `google-auth-httplib2` (Google auth)
   - `playwright` (browser automation)

### Internal Dependencies

1. **Pipecat-Base Foundation:**
   - Tasks 001-004 must be complete
   - Stable voice pipeline
   - Alex personality configured

2. **Configuration:**
   - `.env` file with API keys
   - Entity mapping config file
   - OAuth credentials (Google)

3. **Network:**
   - Home network access
   - Stable internet connection

### Knowledge Dependencies

1. **Home Assistant API:** REST API documentation
2. **Google Tasks API:** Python client examples
3. **Pipecat Function Calling:** Example code, schemas
4. **Playwright:** Browser automation basics

---

## Implementation Phases

### Phase 1: Foundation (Est. 2 weeks)

**Goal:** Basic function calling working with Home Assistant

**Deliverables:**
1. Function calling framework set up
2. 3-5 Home Assistant tools working:
   - Light control (on/off/brightness)
   - Switch control
   - Device state queries
3. Event handlers for feedback
4. Error handling basics
5. Configuration file for entity mapping

**Success Criteria:**
- Can control lights via voice reliably
- Immediate voice feedback works
- Errors handled gracefully

### Phase 2: Productivity Tools (Est. 2 weeks)

**Goal:** Google Tasks integration

**Deliverables:**
1. Google Tasks OAuth setup
2. Task creation via voice
3. Task listing
4. Task completion
5. Optional: Google Calendar integration

**Success Criteria:**
- Can create tasks hands-free
- Managing tasks is faster than app

### Phase 3: Web Search & Advanced (Est. 3 weeks)

**Goal:** Web search via API and optional browser automation

**Deliverables:**
1. Tavily or Brave Search API integration
2. Result summarization via voice
3. Optional: Playwright for complex website interactions
4. Additional integrations (weather, news, etc.)
5. Multi-step workflows

**Success Criteria:**
- Can search and get voice summaries (<2 sec response)
- Playwright available for complex tasks (when needed)
- 10+ total tools working
- Complex commands possible ("Turn off lights and add reminder")

---

## Technical Architecture

### File Structure

```
pipecat-quickstart/
├── bot.py                      # Main entry point (modified)
├── functions/                  # NEW: Tool implementations
│   ├── __init__.py
│   ├── home_assistant.py       # HA integration
│   ├── google_tasks.py         # Google Tasks
│   ├── web_search.py           # Playwright search
│   ├── schemas.py              # Function schemas
│   └── utils.py                # Shared utilities
├── config/                     # NEW: Configuration
│   ├── ha_entities.json        # Entity ID mapping
│   └── function_config.json    # Tool settings
├── .env                        # API keys (existing)
├── TOOL_USE_RESEARCH.md        # Research findings (created)
└── README.md                   # Updated docs
```

### Function Calling Flow

```
1. User: "Turn off the living room lights"
   ↓
2. STT (Deepgram): Transcribe to text
   ↓
3. LLM (OpenAI): Recognize intent → call function "control_light"
   ↓
4. Pipecat: Trigger event handler
   ↓
5. Alex (TTS): "Let me do that for you..."
   ↓
6. Function Handler: Execute control_light()
   ↓
7. Home Assistant API: POST /api/services/light/turn_off
   ↓
8. Result: {"success": true, "entity": "light.living_room"}
   ↓
9. LLM: Process result → generate response
   ↓
10. Alex (TTS): "Living room lights are off"
```

### Sample Code Structure

```python
# bot.py modifications
from functions import register_all_functions

llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"))
register_all_functions(llm, tts)

# functions/__init__.py
def register_all_functions(llm, tts):
    from .home_assistant import register_ha_functions
    from .google_tasks import register_task_functions

    register_ha_functions(llm, tts)
    register_task_functions(llm, tts)

# functions/home_assistant.py
def register_ha_functions(llm, tts):
    llm.register_function("control_light", control_light_handler)

    @llm.event_handler("on_function_calls_started")
    async def on_function_start(service, calls):
        await tts.queue_frame(TTSSpeakFrame("Let me do that..."))
```

---

## Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Function call breaks voice flow | Medium | High | Immediate feedback, async operations |
| Home Assistant down | Low | Medium | Graceful errors, retry logic |
| OAuth tokens expire | Medium | Low | Auto-refresh, clear instructions |
| LLM calls wrong function | Medium | Medium | Clear schemas, testing |
| Web search too slow | High | Medium | Limit to essential use, cache results |
| Too many tools overwhelm LLM | Medium | High | Add incrementally, clear descriptions |
| API rate limits | Low | Low | Reasonable use, backoff |

---

## Open Questions

1. **Entity Naming:** Should friendly names be configurable or hardcoded?
   - **Leaning:** Config file for flexibility

2. **Multi-Step Workflows:** Should Alex automatically chain actions?
   - **Leaning:** Start simple, single action per command

3. **Confirmation:** Should destructive actions require confirmation?
   - **Leaning:** No for lights/switches, yes for delete operations

4. **Fallback:** What happens when function fails?
   - **Leaning:** Voice error message, don't break conversation

5. **Logging:** How detailed should function logs be?
   - **Leaning:** Comprehensive for debugging, configurable level

---

## References

### Research
- `TOOL_USE_RESEARCH.md` - Comprehensive research findings
- Pipecat Function Calling: https://github.com/pipecat-ai/pipecat/blob/main/examples/foundational/14-function-calling.py
- Home Assistant REST API: https://developers.home-assistant.io/docs/api/rest/
- Google Tasks API: https://developers.google.com/tasks
- Playwright Docs: https://playwright.dev/python/

### Related PRDs
- `pipecat-base.md` - Foundation PRD (Tasks 001-008)

### Dependencies
- Task 004 (Assistant Customization) - Complete
- Pipecat 0.0.91 - Installed
- OpenAI API - Configured

---

## Appendix: Example Commands

### Home Assistant
- "Turn on the living room lights"
- "Dim the bedroom lights to 20%"
- "Set kitchen lights to blue"
- "Turn off all lights"
- "Is the front door locked?"

### Google Tasks
- "Add buy milk to my grocery list"
- "Create a task to call mom tomorrow"
- "What's on my task list?"
- "Mark the first task as complete"

### Web Search (API)
- "Search for best pizza near me"
- "Look up the weather forecast"
- "Find the latest news on AI"

### Browser Automation (Optional - when no API available)
- "Take a screenshot of example.com"
- "Navigate to my banking website" (for manual interaction)

### Multi-Step (Future)
- "Good night" → Turn off lights, lock doors, set alarm
- "I'm leaving" → Lights off, thermostat down, lock doors
- "Movie time" → Dim lights, close blinds, pause music
