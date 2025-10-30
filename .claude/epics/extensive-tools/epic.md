---
name: extensive-tools
status: backlog
created: 2025-10-30T22:15:02Z
progress: 0%
prd: .claude/prds/extensive-tools.md
github: null
---

# Epic: Extensive Tools Integration

## Overview

Transform Alex from a task-focused assistant into a comprehensive personal life management platform by adding 10 new service integrations plus an intelligent morning briefing system. This epic delivers voice and programmatic access to calendar, email, news, weather, timers, music, packages, finance, notes, and fitness tracking.

**Core Strategy**: Leverage existing Google OAuth infrastructure and established integration patterns to minimize development time while maximizing user value through the morning briefing orchestration layer.

## Architecture Decisions

### AD1: Batch Google Services Integration
**Decision**: Implement all 4 Google services (Calendar, Gmail, Keep, Fit) in a single task using shared OAuth

**Rationale**:
- All use same authentication mechanism (already working for Google Tasks)
- Similar API patterns and error handling
- Efficient to implement together (~12 hours vs 16 hours separately)
- ✅ Reduces integration count from 4 to 1

**Alternative Rejected**: Separate integration per service → Unnecessary duplication

### AD2: Unified News Module
**Decision**: Single `news.py` module supporting both AP and NYT APIs

**Rationale**:
- Both APIs have similar structure (headlines, summaries, sections)
- Shared caching and rate limiting logic
- Configurable source selection in single config
- ✅ Reduces integration count from 2 to 1

**Alternative Rejected**: Separate modules → Code duplication, harder to maintain

### AD3: Morning Briefing as Orchestration Layer
**Decision**: Briefing system calls existing integration functions (not separate data fetchers)

**Rationale**:
- Reuses all integration functions (no duplicate API calls)
- Briefing just orchestrates parallel calls and formats output
- Scheduler trigger is thin wrapper around function calls
- ✅ Minimal new code (~200 lines vs 400+ for separate system)

**Alternative Rejected**: Separate briefing data layer → Duplicates all API logic

### AD4: Timer/Alarm via APScheduler
**Decision**: Python APScheduler library with in-memory state (no database initially)

**Rationale**:
- Robust, battle-tested library
- Handles concurrent timers, scheduling, persistence
- Can add database persistence later if needed
- ✅ Fast implementation (4 hours)

**Alternative Rejected**: Home Assistant integration → Too complex, external dependency

### AD5: Configuration in YAML
**Decision**: Single `config.yaml` for all integrations and briefing settings

**Rationale**:
- Human-readable and editable
- PyYAML already in ecosystem
- Easy to version control (with secrets in .env)
- Supports nested structures for briefing components

**Alternative Rejected**: Multiple config files → Harder to manage, fragmenting

### AD6: Defer Optional Database
**Decision**: No database in v1; use filesystem (JSON) for package tracking only

**Rationale**:
- Database is overkill for single-user assistant
- Package tracking state fits in single JSON file
- Can add SQLite later if analytics needed
- ✅ Saves 2-3 hours setup time

**Alternative Rejected**: SQLite from start → Premature optimization

### AD7: Parallel API Calls in Briefing
**Decision**: Use `asyncio.gather()` to fetch all briefing data concurrently

**Rationale**:
- Briefing must complete in <30 seconds (NFR1.1)
- Sequential API calls would take 15-20 seconds minimum
- Python asyncio handles parallelization elegantly
- Graceful degradation (if one service fails, others continue)

**Alternative Rejected**: Sequential calls → Too slow, violates performance requirement

## Technical Approach

### Integration Layer

Following the established pattern from `google_tasks.py`, `home_assistant.py`, and `web_search.py`:

**New Integration Modules** (10 total, grouped for efficiency):

1. **`google_services.py`** (batched)
   - Calendar: list, create, update, delete events
   - Gmail: read, send, search, mark read/unread
   - Keep: create notes, manage lists, query
   - Fit: query steps, activity, log workouts
   - **Leverage**: Single OAuth, shared error handling

2. **`news.py`** (unified)
   - AP News API integration (user subscription)
   - NYT API integration (user subscription)
   - Configurable sources, sections, article limits
   - Voice-optimized summaries

3. **`weather.py`**
   - OpenWeatherMap API
   - Current conditions, hourly, daily forecasts
   - Severe weather alerts
   - Smart recommendations

4. **`timer_alarm.py`**
   - APScheduler for timers and alarms
   - Multiple concurrent timers with names
   - Recurring alarms
   - Home Assistant integration for alarm triggers (optional)

5. **`spotify.py`**
   - Spotify Web API (OAuth)
   - Playback control, search, playlists
   - Volume control, device management

6. **`package_tracking.py`**
   - AfterShip API
   - Add/remove packages
   - Query delivery status
   - JSON file persistence for active packages

7. **`plaid_finance.py`**
   - Plaid Link for bank authentication
   - Read-only account balances
   - Recent transactions
   - Privacy controls (confirmation before speaking)

Each module exports:
```python
def register_[service]_functions(llm, tts) -> list[FunctionSchema]
```

### Morning Briefing System

**New Modules** (briefing orchestration):

**`briefing/manager.py`**:
```python
class BriefingManager:
    def __init__(self, config, llm, tts):
        self.config = config
        self.llm = llm
        self.tts = tts

    async def generate_briefing(self) -> dict:
        """Fetch data from all enabled services in parallel."""
        tasks = []
        if self.config.weather_enabled:
            tasks.append(self._fetch_weather())
        if self.config.calendar_enabled:
            tasks.append(self._fetch_calendar())
        # ... other services

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return self._format_briefing(results)

    async def deliver_briefing(self, briefing_text: str):
        """Speak briefing via TTS."""
        await self.tts.queue_frame(TTSSpeakFrame(briefing_text))
```

**`briefing/scheduler.py`**:
```python
class BriefingScheduler:
    def __init__(self, briefing_manager, config):
        self.scheduler = AsyncIOScheduler()
        self.briefing_manager = briefing_manager

    def start(self):
        """Schedule daily briefing at configured time."""
        self.scheduler.add_job(
            self.briefing_manager.deliver_briefing,
            CronTrigger(hour=7, minute=0),  # From config
            id='morning_briefing'
        )
        self.scheduler.start()
```

**`briefing/config.py`**:
```python
@dataclass
class BriefingConfig:
    enabled: bool
    scheduled_time: str
    weather_enabled: bool
    calendar_enabled: bool
    # ... other component flags

    @classmethod
    def load(cls, yaml_path: str) -> 'BriefingConfig':
        """Load from config.yaml."""
        ...
```

### Configuration System

**`config/briefing_config.yaml`**:
```yaml
morning_briefing:
  enabled: true
  scheduled_time: "07:00"
  timezone: "America/Los_Angeles"

  components:
    weather: { enabled: true, location: "Seattle, WA" }
    calendar: { enabled: true, max_events: 5 }
    email: { enabled: true, max_emails: 3 }
    tasks: { enabled: true, max_tasks: 5 }
    news:
      enabled: true
      sources:
        - { name: "ap", sections: ["politics", "tech"], max_articles: 2 }
        - { name: "nyt", sections: ["business"], max_articles: 1 }
    packages: { enabled: true }
    finance: { enabled: false }  # Opt-in only
    fitness: { enabled: false }
```

### Authentication

**Leverage Existing**:
- `google_auth.py` → Extend for Calendar, Gmail, Keep, Fit APIs

**New Auth Modules**:
- `spotify_auth.py` → OAuth 2.0 for Spotify
- `plaid_auth.py` → Plaid Link for bank connections

### Data Flow

**Voice Command Flow**:
```
User: "What's on my calendar?"
  → STT (Deepgram)
  → LLM (GPT-4) → Function call: list_calendar_events
  → google_services.py → Google Calendar API
  → Format voice response
  → LLM synthesis
  → TTS (Cartesia)
  → User
```

**Morning Briefing Flow**:
```
Scheduled Trigger (7:00 AM) OR Voice Command ("Good morning")
  → BriefingScheduler → BriefingManager.generate_briefing()
  → Parallel API calls (asyncio.gather):
      - fetch_weather()
      - fetch_calendar()
      - fetch_email()
      - fetch_tasks()
      - fetch_news()
      - fetch_packages()
  → Format cohesive narrative (2-3 minutes of speech)
  → TTS queue
  → User hears complete briefing
```

## Implementation Strategy

### Simplified 4-Phase Approach (≤10 Tasks Total)

**Key Optimization**: Batch related integrations, leverage shared infrastructure

---

### Phase 1: Foundation + High-Impact Tools (3 tasks, ~18 hours)

**Goal**: Establish configuration system and implement most-requested integrations

1. **Configuration System + Weather** (6 hours)
   - Create `config.yaml` structure
   - Add PyYAML loading
   - Implement weather integration (OpenWeatherMap)
   - **Deliverable**: Config-driven weather queries working

2. **Google Services Bundle** (8 hours)
   - Extend `google_auth.py` for 4 APIs (Calendar, Gmail, Keep, Fit)
   - Implement `google_services.py` with all handlers
   - Function schemas for ~15 new functions
   - **Deliverable**: Voice access to calendar, email, notes, fitness

3. **Timer/Alarm System** (4 hours)
   - APScheduler setup
   - `timer_alarm.py` with handlers for timers and alarms
   - Integration with Home Assistant for alarm triggers (optional)
   - **Deliverable**: Voice-controlled timers and alarms

**Phase 1 Total**: 18 hours

---

### Phase 2: News + Briefing MVP (3 tasks, ~16 hours)

**Goal**: Add news sources and build morning briefing orchestration

4. **Unified News Integration** (6 hours)
   - `news.py` supporting AP News and NYT APIs
   - Configurable sources and sections
   - Voice-optimized summaries
   - **Deliverable**: News queries and headlines working

5. **Morning Briefing Core** (8 hours)
   - `briefing/manager.py` - Parallel data fetching
   - `briefing/config.py` - Load YAML settings
   - `briefing/scheduler.py` - Scheduled delivery
   - Voice command trigger ("Good morning")
   - **Deliverable**: Briefing combines weather + calendar + tasks + news

6. **Briefing Polish** (2 hours)
   - Skip functionality ("Skip news", "Next section")
   - Weekday vs weekend templates
   - Context-aware adaptations
   - **Deliverable**: Production-ready briefing UX

**Phase 2 Total**: 16 hours

---

### Phase 3: Lifestyle Integrations (2 tasks, ~12 hours)

**Goal**: Add entertainment and convenience features

7. **Spotify Music Control** (6 hours)
   - `spotify_auth.py` OAuth setup
   - `spotify.py` with playback control handlers
   - Playlist management, search, volume control
   - **Deliverable**: Voice-controlled music playback

8. **Package Tracking** (6 hours)
   - `package_tracking.py` with AfterShip API
   - JSON file persistence for active packages
   - Add to morning briefing
   - **Deliverable**: Voice package queries and briefing inclusion

**Phase 3 Total**: 12 hours

---

### Phase 4: Finance + Final Polish (2 tasks, ~12 hours)

**Goal**: Complete remaining integrations and polish

9. **Plaid Finance Integration** (8 hours)
   - `plaid_auth.py` Plaid Link setup
   - `plaid_finance.py` with account balance handlers
   - Privacy controls (confirmation before speaking)
   - **Deliverable**: Voice account balance queries

10. **Integration Testing + Documentation** (4 hours)
    - End-to-end briefing testing
    - Performance benchmarks (briefing <30s)
    - Update all function registration in `__init__.py`
    - Setup guides for each API
    - **Deliverable**: Production-ready, documented system

**Phase 4 Total**: 12 hours

---

### **Total Implementation**: 10 tasks, ~58 hours (vs PRD's 80-100)

**Efficiency Gains**:
- Batching Google services: Saved 4 hours
- Unified news module: Saved 2 hours
- No database: Saved 3 hours
- Briefing as orchestrator: Saved 4 hours
- Defer fitness to Phase 1 bundle: Saved 1 hour
- **Total Saved**: ~14 hours (18% reduction)

## Tasks Created

- [ ] 001.md - Configuration System + Weather Integration (parallel: false)
- [ ] 002.md - Google Services Bundle (Calendar, Gmail, Keep, Fit) (parallel: false, depends on: 001)
- [ ] 003.md - Timer/Alarm System (APScheduler) (parallel: true, depends on: 001)
- [ ] 004.md - Unified News Integration (AP + NYT) (parallel: true, depends on: 001)
- [ ] 005.md - Morning Briefing Core (Manager + Scheduler) (parallel: false, depends on: 001, 002, 004)
- [ ] 006.md - Briefing Polish (Skip, Templates, Context-Aware) (parallel: true, depends on: 005, conflicts with: 005)
- [ ] 007.md - Spotify Music Control (parallel: true, depends on: 001)
- [ ] 008.md - Package Tracking (AfterShip) (parallel: true, depends on: 001, 005)
- [ ] 009.md - Plaid Finance Integration (parallel: true, depends on: 001)
- [ ] 010.md - Integration Testing + Documentation (parallel: false, depends on: 001-009)

**Total tasks**: 10
**Completed**: 0
**In Progress**: 0
**Remaining**: 10
**Parallel tasks**: 6 (Tasks 003, 004, 006, 007, 008, 009)
**Sequential tasks**: 4 (Tasks 001, 002, 005, 010)
**Estimated total effort**: 58 hours (6h + 8h + 4h + 6h + 8h + 2h + 6h + 6h + 8h + 4h)

## Dependencies

### External Dependencies

**APIs & Services** (all identified in PRD):
- Google Calendar, Gmail, Keep, Fit APIs (OAuth via existing setup)
- AP News API (user subscription)
- New York Times API (user subscription)
- OpenWeatherMap API (free tier)
- Spotify Web API (OAuth)
- AfterShip API (free tier: 100 shipments/mo)
- Plaid API (paid: ~$0.50-2/mo per user)

**Python Libraries** (add to `requirements.txt`):
```
google-auth-oauthlib
google-api-python-client
spotipy
plaid-python
apscheduler
pyyaml
```

### Internal Dependencies

**Existing Infrastructure** (already working):
- Pipecat pipeline (STT, LLM, TTS) ✅
- OpenAI function calling framework ✅
- `google_auth.py` (Google OAuth for Tasks) ✅
- Integration pattern established ✅

**New Infrastructure** (to be built):
- Configuration management (`config.yaml` loading)
- Briefing orchestration layer
- Scheduler system (APScheduler)

**No Blockers**: All dependencies are available, no external blockers

## Success Criteria (Technical)

### Performance Benchmarks

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Morning briefing latency | < 30 seconds | Timer logs (trigger → completion) |
| Individual query response | < 3 seconds (95th percentile) | Function execution time |
| Parallel API call efficiency | 70%+ time saved vs sequential | Compare parallel vs sequential timings |
| System uptime | 99%+ | Error logs + health checks |

### Quality Gates

**Before marking epic complete**:
- [ ] All 10 integrations working and registered
- [ ] Morning briefing delivers <30 seconds
- [ ] Configuration system loads from YAML
- [ ] Google OAuth working for 4 services
- [ ] Spotify, Plaid auth flows complete
- [ ] Voice commands documented (example list)
- [ ] Setup guides for each API
- [ ] No Python syntax errors or import failures
- [ ] User (Gyatso) completes acceptance testing

### Acceptance Criteria

From PRD user stories:
- [ ] Morning briefing triggered by voice ("Good morning") or scheduled (7 AM)
- [ ] Briefing includes 5+ configurable components
- [ ] Voice access to calendar (create, list, update, delete events)
- [ ] Voice access to email (read, send, search)
- [ ] News from AP and NYT with summaries
- [ ] Weather forecasts with smart recommendations
- [ ] Timers and alarms with Home Assistant integration
- [ ] Spotify playback control
- [ ] Package tracking with briefing inclusion
- [ ] Plaid account balances with privacy controls

## Estimated Effort

**Total**: 58 hours (~7 weeks at 8 hours/week, or 2 weeks full-time)

**Breakdown by Phase**:
- Phase 1 (Foundation): 18 hours (31%)
- Phase 2 (News + Briefing): 16 hours (28%)
- Phase 3 (Lifestyle): 12 hours (21%)
- Phase 4 (Finance + Polish): 12 hours (20%)

**Critical Path**: Tasks 1-5 are sequential (must complete in order), Tasks 6-9 can be parallelized

**Resource Requirements**: 1 developer (Gyatso + Claude Code assistant)

**Risk Buffer**: Built-in 15% buffer per task estimate

## Risks & Mitigation

### High Priority Risks

**R1: Plaid Authentication Complexity**
- **Impact**: Finance integration delayed or fails
- **Likelihood**: Medium (Plaid is complex)
- **Mitigation**:
  - Schedule as last integration (Phase 4)
  - Clear documentation for Plaid Link setup
  - Make finance optional (can skip if needed)
  - Test with multiple banks during Task 9

**R2: Morning Briefing Latency**
- **Impact**: Briefing takes >30s, poor UX
- **Likelihood**: Low (parallel calls should work)
- **Mitigation**:
  - Implement Task 5 with parallelization from start
  - Add timeouts per API call (5s max)
  - Graceful degradation (skip slow services)
  - Performance benchmarking in Task 10

**R3: OAuth Token Expiration**
- **Impact**: Services stop working until re-auth
- **Likelihood**: High (Google tokens expire 1-7 days)
- **Mitigation**:
  - Implement robust token refresh in Task 2
  - Clear error messages prompting re-auth
  - Monitor token expiration in logs

### Medium Priority Risks

**R4: API Rate Limits**
- **Impact**: Service disruption during heavy use
- **Likelihood**: Low (single user, generous limits)
- **Mitigation**:
  - Implement caching (weather: 30min, news: 1hr)
  - Monitor API usage in logs
  - Document rate limits in setup guides

**R5: Scope Creep**
- **Impact**: Timeline extends indefinitely
- **Likelihood**: Medium (common issue)
- **Mitigation**:
  - Strict adherence to 10-task plan
  - Defer all "Future Enhancements" from PRD
  - Regular check-ins to assess scope vs progress

### Low Priority Risks

**R6: Configuration Complexity**
- **Impact**: User struggles with YAML config
- **Likelihood**: Low (user is technical)
- **Mitigation**:
  - Provide example configs in Task 1
  - Clear comments in default `config.yaml`
  - Sensible defaults (most components enabled)

## Simplifications & Improvements

**Key Optimizations from PRD**:

1. **Batched Google Services** → Reduced 4 integrations to 1 task
2. **Unified News Module** → Single codebase for AP + NYT
3. **Briefing as Orchestrator** → No duplicate data fetching logic
4. **Defer Database** → Filesystem only, add DB later if needed
5. **Combined Testing** → Single task for all integration testing

**Leverage Existing Functionality**:
- Google OAuth: Already working for Tasks, extend for 4+ APIs
- Function Calling Pattern: Replicate from `google_tasks.py`, `home_assistant.py`
- TTS Queue: Use existing `tts.queue_frame()` for briefing
- Error Handling: Reuse patterns from `web_search.py`

**Result**: Same user value (all PRD features), 42 hours saved (vs 100-hour estimate)

## Future Enhancements (Deferred)

**Not in this epic, but noted for future**:
- Gentle wake-up mode (sound fade-in before briefing)
- Multi-user support (per-user profiles)
- Advanced email automation (auto-respond, filtering)
- Smart home integration (trigger lights during briefing)
- Mobile companion app
- Context-aware suggestions (traffic alerts, etc.)

These can be added in future epics once core functionality is validated.

---

**Implementation Priority**: High (major UX upgrade, reasonable effort)
**Technical Risk**: Low-Medium (proven patterns, minor auth complexity)
**User Impact**: Very High (10-15 min/day saved, 80%+ life task coverage)
**Maintenance Burden**: Low (modular design, well-documented)

**Ready for task decomposition!** Run `/pm:epic-decompose extensive-tools` to create detailed task files.
