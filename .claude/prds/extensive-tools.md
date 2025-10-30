---
name: extensive-tools
description: Comprehensive personal life management integrations including calendar, email, news, finance, music, fitness, timers, weather, and intelligent morning briefings
status: backlog
created: 2025-10-30T22:05:07Z
---

# PRD: Extensive Tools Integration

## Executive Summary

Expand the Alex voice assistant from basic home control and task management to a comprehensive personal life assistant by integrating 10+ essential services. This PRD covers calendar management (Google Calendar), communication (Gmail), news (AP News, New York Times), financial monitoring (Plaid), music control (Spotify), fitness tracking (Google Fit), weather forecasting, package tracking, note-taking (Google Keep), and timer/alarm systems.

The centerpiece feature is an intelligent **Morning Briefing** that synthesizes information from all integrated services into a personalized daily summary, delivered either on-demand via voice command or automatically at a scheduled time. Future enhancements include a gentle wake-up experience with soothing sounds that fade into the briefing.

**Value Proposition**: Transform Alex from a task-focused assistant into a holistic life management platform that proactively surfaces relevant information, reduces cognitive load, and streamlines daily routines through natural voice interactions.

## Problem Statement

### Current State
Alex currently supports:
- Home automation (Home Assistant)
- Task management (Google Tasks)
- Web search (Tavily)

While useful, this leaves significant gaps in daily life management:

**Information Fragmentation**
- Users must check multiple apps/services separately (email, calendar, news, weather)
- No unified morning routine to plan the day
- Context switching between devices disrupts focus

**Reactive vs Proactive**
- Assistant only responds when asked, doesn't proactively surface important information
- No synthesis of cross-service insights (e.g., "traffic is bad, leave 15 min early for your 9am meeting")

**Limited Scope**
- Can't manage calendar, read/send emails, or control music playback
- No financial visibility or package tracking
- Missing essential daily-use integrations

### Why Now?
1. **Google OAuth Infrastructure**: Already implemented for Google Tasks, easy to extend to Calendar, Gmail, Keep, Fit
2. **Proven Pattern**: Successful integration pattern established (home_assistant.py, web_search.py, google_tasks.py)
3. **User Subscriptions**: User already pays for AP News and NYT, should leverage premium access
4. **Morning Routine Gap**: No automated way to start the day with comprehensive briefing

### User Impact
Without these integrations:
- 10-15 minutes each morning manually checking services
- Missed appointments due to calendar not being voice-accessible
- Information overload from checking too many apps
- Reduced assistant utility (limited to home control + tasks)

## User Stories

### Primary Persona: Busy Professional (Gyatso)

**Background**:
- Works from home with flexible schedule
- Manages personal tasks, calendar, and home automation
- Subscribes to premium news services (AP, NYT)
- Wants hands-free access to information while multitasking

**Daily Routine**:
- Morning: Wake up, get briefing on day ahead
- Throughout day: Quick checks of email, calendar, weather
- Evening: Set timers for cooking, play music, check tasks

---

### User Story 1: Morning Briefing (Core Feature)

**As a** busy professional
**I want** an automated morning briefing that synthesizes information from all my services
**So that** I can start my day informed without manually checking multiple apps

**Acceptance Criteria**:
- [ ] Briefing can be triggered by voice command ("Good morning" or "Give me my briefing")
- [ ] Briefing can be scheduled to play automatically at user-configured time (e.g., 7:00 AM)
- [ ] Briefing includes (all configurable):
  - Today's weather forecast
  - Calendar events for the day
  - Unread email count + important emails
  - Today's tasks from Google Tasks
  - Top news headlines from AP News and NYT (with brief summaries)
  - Package delivery updates (if any expected today)
  - Optional: Account balances from configured banks
- [ ] Each component can be enabled/disabled via configuration
- [ ] User can skip sections by voice ("Skip news", "Next section")
- [ ] Briefing adapts based on calendar (e.g., mentions "gym at 6pm" if workout scheduled)
- [ ] Different briefing templates for weekday vs weekend

**Future Enhancement**:
- Soothing sound (nature sounds, gentle music) starts playing
- Sound gradually decreases in volume
- Assistant begins speaking briefing as sound fades
- Creates gentle, pleasant wake-up experience

---

### User Story 2: Google Calendar Integration

**As a** user with a busy schedule
**I want** voice-controlled access to my Google Calendar
**So that** I can check, create, and modify appointments hands-free

**Voice Interactions**:
- "What's on my calendar today?"
- "Do I have anything scheduled for tomorrow afternoon?"
- "Schedule dentist appointment for next Tuesday at 2pm"
- "Move my 3pm meeting to 4pm"
- "Cancel my meeting with John"
- "What time is my next meeting?"

**Acceptance Criteria**:
- [ ] List calendar events (today, tomorrow, specific date, date range)
- [ ] Create new calendar events with title, date, time, duration
- [ ] Update existing events (time, title, location)
- [ ] Delete calendar events
- [ ] Query next upcoming event
- [ ] Support multiple calendars (personal, work)
- [ ] Handle recurring events appropriately
- [ ] Voice confirmation before creating/deleting events

---

### User Story 3: Gmail Integration

**As a** user who receives important emails
**I want** voice access to my Gmail inbox
**So that** I can stay informed without opening my laptop

**Voice Interactions**:
- "Do I have any unread emails?"
- "Read my latest emails"
- "Read emails from [sender name]"
- "Send an email to [contact]" (voice-compose body)
- "What emails did I get today about [topic]?"
- "Mark all as read"

**Acceptance Criteria**:
- [ ] Check unread email count
- [ ] List recent emails (sender, subject, snippet)
- [ ] Read full email body (optimized for voice)
- [ ] Send new emails (to, subject, body)
- [ ] Search emails by sender, subject, or keyword
- [ ] Mark emails as read/unread
- [ ] Archive emails
- [ ] Filter important/starred emails
- [ ] Respect privacy: ask for confirmation before reading emails aloud in shared spaces

---

### User Story 4: News Integration (AP News & New York Times)

**As a** subscriber to premium news services
**I want** curated headlines and summaries from AP and NYT
**So that** I stay informed with quality journalism

**Voice Interactions**:
- "What's the latest news?"
- "Give me today's top stories"
- "What's happening in politics?"
- "Any tech news today?"
- "Read me that article about [topic]"

**Acceptance Criteria**:
- [ ] Integrate with AP News API using user's subscription
- [ ] Integrate with New York Times API using user's subscription
- [ ] Fetch top headlines (configurable: 3-10 articles)
- [ ] Provide headline + brief summary (1-2 sentences)
- [ ] Filter by section (politics, tech, world, business, science)
- [ ] User can configure which sections to include in morning briefing
- [ ] Voice-optimized summaries (concise, clear)
- [ ] Option to hear full article (text-to-speech of article body)
- [ ] Respect user's subscription/paywall access

---

### User Story 5: Weather Forecasting

**As a** user planning daily activities
**I want** accurate weather forecasts
**So that** I can dress appropriately and plan outdoor activities

**Voice Interactions**:
- "What's the weather like?"
- "Do I need an umbrella today?"
- "What's the forecast for this weekend?"
- "Is it going to rain tomorrow?"
- "What's the temperature right now?"

**Acceptance Criteria**:
- [ ] Current weather conditions (temp, conditions, humidity, wind)
- [ ] Hourly forecast (next 12-24 hours)
- [ ] Daily forecast (next 7 days)
- [ ] Severe weather alerts
- [ ] Smart recommendations ("Bring an umbrella", "Good day for outdoor run")
- [ ] Location-based (use configured home location or ask for location)
- [ ] Integrate with OpenWeatherMap or WeatherAPI (best free/affordable option)
- [ ] Include in morning briefing

---

### User Story 6: Timer & Alarm System

**As a** user cooking, working, or managing time
**I want** voice-controlled timers and alarms
**So that** I can track time without using my hands

**Voice Interactions**:
- "Set a timer for 10 minutes"
- "Set a timer for the chicken" (named timer)
- "How much time is left on my timer?"
- "Cancel the timer"
- "Set an alarm for 7am tomorrow"
- "Wake me up at 6:30"
- "Snooze"

**Acceptance Criteria**:
- [ ] Create multiple concurrent timers
- [ ] Name timers for easy reference
- [ ] Check remaining time on timers
- [ ] Cancel/pause/resume timers
- [ ] Set alarms with specific time and date
- [ ] Recurring alarms (weekdays, weekends, custom)
- [ ] Snooze functionality (configurable duration)
- [ ] Integration with Home Assistant (trigger lights/scenes when alarm goes off)
- [ ] Distinct sounds for timers vs alarms
- [ ] Voice notification when timer ends

---

### User Story 7: Music Control (Spotify)

**As a** music listener
**I want** voice control of Spotify playback
**So that** I can enjoy music hands-free

**Voice Interactions**:
- "Play some focus music"
- "Play my workout playlist"
- "Play jazz"
- "Skip this song"
- "Pause music"
- "What's playing?"
- "Turn up the volume"
- "Add this to my liked songs"

**Acceptance Criteria**:
- [ ] Play music (song, artist, album, playlist, genre)
- [ ] Playback controls (play, pause, skip, previous)
- [ ] Volume control
- [ ] Query current track info
- [ ] Add songs to playlists or liked songs
- [ ] Create new playlists
- [ ] Search Spotify library
- [ ] Control playback device (speaker, computer, phone)
- [ ] Integrate with Spotify Web API

---

### User Story 8: Package Tracking

**As a** frequent online shopper
**I want** automatic package tracking
**So that** I know when deliveries are arriving

**Voice Interactions**:
- "Where's my Amazon package?"
- "When is my package arriving?"
- "Do I have any deliveries today?"
- "Track package [tracking number]"

**Acceptance Criteria**:
- [ ] Add packages by tracking number
- [ ] Auto-detect carrier (USPS, UPS, FedEx, Amazon, etc.)
- [ ] Show delivery status and estimated arrival
- [ ] Proactive notifications when package is out for delivery
- [ ] Include in morning briefing if delivery expected today
- [ ] Integrate with AfterShip or 17track API
- [ ] Support multiple active packages
- [ ] Mark packages as received

---

### User Story 9: Finance Monitoring (Plaid)

**As a** financially conscious user
**I want** quick access to my account balances
**So that** I can stay aware of my financial status

**Voice Interactions**:
- "What's my checking account balance?"
- "Show me recent transactions"
- "How much did I spend this week?"
- "What's my savings account balance?"

**Acceptance Criteria**:
- [ ] Connect bank accounts via Plaid (secure, read-only access)
- [ ] Query account balances (checking, savings, credit cards)
- [ ] List recent transactions (last N transactions or past X days)
- [ ] Transaction summaries (spending by category, weekly totals)
- [ ] Privacy-aware: require voice confirmation before reading balances aloud
- [ ] Support multiple banks/accounts
- [ ] Optional: Include checking balance in morning briefing
- [ ] Handle Plaid link expiration gracefully

**Privacy Considerations**:
- Read-only access (no transfers or payments)
- Encrypted credential storage
- Optional in morning briefing (user can disable)
- Confirmation required before speaking financial info in shared spaces

---

### User Story 10: Note-Taking (Google Keep)

**As a** user with ideas and reminders
**I want** voice-dictated notes
**So that** I can capture thoughts without breaking focus

**Voice Interactions**:
- "Add a note: buy milk"
- "Create a shopping list"
- "Add bananas to my shopping list"
- "What's on my shopping list?"
- "Remind me that [note content]"

**Acceptance Criteria**:
- [ ] Create new notes via voice dictation
- [ ] Create and manage lists (shopping, to-do, etc.)
- [ ] Add items to existing lists
- [ ] Query notes by keyword
- [ ] Mark list items as complete
- [ ] Set location-based reminders (if Google Keep supports)
- [ ] Integration with Google Keep API
- [ ] Separate from Google Tasks (Keep for quick notes, Tasks for structured to-dos)

---

### User Story 11: Fitness Tracking (Google Fit)

**As a** health-conscious user
**I want** access to my fitness data
**So that** I can track progress and stay motivated

**Voice Interactions**:
- "How many steps have I taken today?"
- "Did I hit my step goal?"
- "Log a 30-minute run"
- "What's my weekly activity summary?"

**Acceptance Criteria**:
- [ ] Query daily steps
- [ ] Query weekly activity summary
- [ ] Log workouts (type, duration, calories)
- [ ] Check progress toward daily goals
- [ ] Integration with Google Fit API
- [ ] Optional: Include step count in morning briefing

---

## Requirements

### Functional Requirements

#### FR1: Integration Framework
- **FR1.1**: All integrations follow the established pattern (see `home_assistant.py`, `web_search.py`, `google_tasks.py`)
- **FR1.2**: Each integration is a separate module in `functions/` directory
- **FR1.3**: Function schemas defined with proper OpenAI function calling format
- **FR1.4**: Async handlers for all API calls
- **FR1.5**: Proper error handling with user-friendly voice responses
- **FR1.6**: Logging for debugging and monitoring

#### FR2: Morning Briefing System
- **FR2.1**: Configurable briefing components (user can enable/disable each section)
- **FR2.2**: Scheduled automatic delivery at user-configured time
- **FR2.3**: On-demand delivery via voice command ("Good morning", "Give me my briefing")
- **FR2.4**: Voice-optimized content (concise, natural phrasing)
- **FR2.5**: Skip functionality (user can skip sections during playback)
- **FR2.6**: Template system for weekday vs weekend briefings
- **FR2.7**: Context-aware (adapts based on calendar, weather, etc.)

**Future Enhancement (FR2.8)**: Gentle wake-up mode
- Soothing sound starts playing (nature sounds, ambient music)
- Sound gradually fades in volume
- Assistant begins briefing as sound fades
- Snooze functionality

#### FR3: Configuration System
- **FR3.1**: User configuration file (YAML or JSON) for all integrations
- **FR3.2**: Enable/disable individual integrations
- **FR3.3**: Configure briefing components and schedule
- **FR3.4**: API keys and credentials management
- **FR3.5**: Privacy settings (e.g., don't read finance info in shared spaces)
- **FR3.6**: Default settings for new users

#### FR4: Authentication & Security
- **FR4.1**: Reuse existing Google OAuth for Calendar, Gmail, Keep, Fit
- **FR4.2**: Secure credential storage (encrypted, not in git)
- **FR4.3**: API key management for third-party services
- **FR4.4**: Plaid Link integration for bank authentication
- **FR4.5**: Token refresh handling for all OAuth services
- **FR4.6**: Read-only access where possible (Plaid, Gmail reading)
- **FR4.7**: Read-write access where needed (Calendar, Gmail sending, Tasks)

#### FR5: Voice Interaction Design
- **FR5.1**: Natural language understanding (leverage OpenAI LLM)
- **FR5.2**: Confirmation prompts for destructive actions (delete event, send email)
- **FR5.3**: Clarification questions when intent is ambiguous
- **FR5.4**: Context retention across conversation turns
- **FR5.5**: Concise voice responses (optimize for speech, not text)
- **FR5.6**: Error messages that guide users to fix issues

#### FR6: Programmatic Access
- **FR6.1**: All functions accessible via Python API (not just voice)
- **FR6.2**: Documented function interfaces for programmatic use
- **FR6.3**: Ability to chain functions (e.g., create event + add task + send email)
- **FR6.4**: Support for automation workflows

### Non-Functional Requirements

#### NFR1: Performance
- **NFR1.1**: Morning briefing completes in < 30 seconds (for typical configuration)
- **NFR1.2**: Individual queries respond in < 3 seconds
- **NFR1.3**: API timeouts set appropriately (5-10 seconds)
- **NFR1.4**: Parallel API calls where possible (briefing fetches concurrently)
- **NFR1.5**: Caching for frequently accessed data (weather, news)

#### NFR2: Reliability
- **NFR2.1**: Graceful degradation (if one service fails, others continue)
- **NFR2.2**: Retry logic for transient API failures
- **NFR2.3**: Fallback mechanisms (e.g., if AP News fails, try NYT)
- **NFR2.4**: Comprehensive error logging
- **NFR2.5**: Health checks for critical services

#### NFR3: Privacy & Security
- **NFR3.1**: All credentials stored encrypted
- **NFR3.2**: No logging of sensitive data (passwords, financial info)
- **NFR3.3**: User consent required for reading sensitive info aloud
- **NFR3.4**: Clear documentation of data access and usage
- **NFR3.5**: Compliance with API terms of service (Gmail, Plaid, etc.)

#### NFR4: Usability
- **NFR4.1**: Setup process documented with step-by-step guides
- **NFR4.2**: Clear error messages when API keys missing
- **NFR4.3**: Example voice commands documented
- **NFR4.4**: Configuration via simple config file (not code)
- **NFR4.5**: Sensible defaults (works out of box for common use cases)

#### NFR5: Maintainability
- **NFR5.1**: Consistent code patterns across all integrations
- **NFR5.2**: Comprehensive docstrings and comments
- **NFR5.3**: Unit tests for each integration
- **NFR5.4**: Integration tests for morning briefing
- **NFR5.5**: Modular design (easy to add/remove integrations)

#### NFR6: Cost Efficiency
- **NFR6.1**: Use free/affordable APIs where possible
- **NFR6.2**: Minimize API calls (caching, batching)
- **NFR6.3**: Document costs for paid services (Plaid, news APIs)
- **NFR6.4**: Configuration to disable expensive features

## Success Criteria

### Quantitative Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Services integrated | 3 (HA, Tasks, Search) | 13+ | Count of working integrations |
| Morning routine time | 10-15 min (manual) | < 2 min (briefing) | User timing |
| Voice commands supported | ~20 | 100+ | Function count |
| Daily voice interactions | 5-10 | 30+ | Usage logs |
| User-reported value | N/A | 8+/10 | User survey |
| Integration uptime | N/A | 99%+ | Error logs |
| Average query latency | ~2s | < 3s | Performance monitoring |

### Qualitative Goals

**User Experience**:
- [ ] User can go through entire morning routine without touching phone/computer
- [ ] Assistant feels proactive, not just reactive
- [ ] Voice interactions feel natural and conversational
- [ ] User trusts assistant with sensitive information (finance, email)

**Technical Excellence**:
- [ ] Code follows established patterns consistently
- [ ] Documentation is comprehensive and up-to-date
- [ ] New integrations can be added in < 4 hours
- [ ] System is stable and reliable

**Business Value**:
- [ ] Assistant becomes essential part of daily routine
- [ ] User recommends system to others
- [ ] Foundation for future commercial product

## Architecture Overview

### System Components

```
Alex Voice Assistant
├── Core Pipeline (Pipecat)
│   ├── Speech-to-Text (Deepgram)
│   ├── LLM (OpenAI GPT-4)
│   └── Text-to-Speech (Cartesia)
│
├── Integration Layer (functions/)
│   ├── google_calendar.py       (NEW)
│   ├── gmail.py                 (NEW)
│   ├── news.py                  (NEW - AP, NYT)
│   ├── weather.py               (NEW)
│   ├── timer_alarm.py           (NEW)
│   ├── spotify.py               (NEW)
│   ├── package_tracking.py      (NEW)
│   ├── plaid_finance.py         (NEW)
│   ├── google_keep.py           (NEW)
│   ├── google_fit.py            (NEW)
│   ├── google_tasks.py          (Existing)
│   ├── home_assistant.py        (Existing)
│   └── web_search.py            (Existing)
│
├── Morning Briefing System (NEW)
│   ├── briefing_manager.py      (Orchestrates briefing)
│   ├── briefing_config.py       (User configuration)
│   ├── briefing_scheduler.py    (Scheduled delivery)
│   └── briefing_templates.py    (Weekday/weekend templates)
│
├── Configuration
│   ├── config.yaml              (User settings)
│   ├── .env                     (API keys)
│   └── credentials/             (OAuth tokens)
│
└── Authentication (google_auth.py, spotify_auth.py, plaid_auth.py)
```

### Integration Pattern

Each integration follows this structure:

```python
# functions/[service_name].py

# 1. API Client Setup
API_KEY = os.getenv("SERVICE_API_KEY")

# 2. Handler Functions
async def operation_handler(function_name, tool_call_id, arguments, llm, context_aggregator, result_callback):
    """Perform operation and return results via callback."""
    # Extract arguments
    # Call external API
    # Format response for voice
    # Send via result_callback

# 3. Schema Definitions
def create_operation_schema():
    """Define OpenAI function schema."""
    return FunctionSchema(...)

# 4. Registration Function
def register_service_functions(llm, tts):
    """Register all functions with LLM."""
    llm.register_function("operation_name", operation_handler)
    return [create_operation_schema(), ...]
```

### Morning Briefing Architecture

**briefing_manager.py**:
```python
class BriefingManager:
    async def generate_briefing(self, config: BriefingConfig) -> str:
        """Generate morning briefing text."""
        # Fetch data from all enabled services (parallel)
        weather = await fetch_weather() if config.include_weather else None
        calendar = await fetch_calendar() if config.include_calendar else None
        news = await fetch_news() if config.include_news else None
        # ... other services

        # Format into cohesive briefing
        briefing_text = self.format_briefing(weather, calendar, news, ...)
        return briefing_text

    async def deliver_briefing(self, briefing_text: str):
        """Deliver briefing via TTS."""
        await tts.queue_frame(TTSSpeakFrame(briefing_text))
```

**briefing_scheduler.py**:
```python
class BriefingScheduler:
    def schedule_daily_briefing(self, time: str, config: BriefingConfig):
        """Schedule recurring briefing at specified time."""
        # Use APScheduler or similar
        # Trigger briefing_manager.generate_briefing() at scheduled time
```

### Data Flow

1. **Voice Command** → STT → LLM → Function Call
2. **Function Handler** → External API → Format Response → Callback
3. **LLM** → Synthesize Response → TTS → User

**Morning Briefing Flow**:
1. **Trigger** (scheduled time or voice command)
2. **Fetch Data** (parallel API calls to all enabled services)
3. **Format** (create cohesive narrative)
4. **Deliver** (TTS, handling interruptions/skips)

## Implementation Strategy

### Phase 1: High-Priority Tools (Est. 2-3 weeks)

**Goal**: Implement most impactful integrations first

**Integrations**:
1. Google Calendar (4-6 hours)
2. Weather API (2-3 hours)
3. Timer/Alarm System (4-6 hours)

**Morning Briefing MVP** (6-8 hours):
- Basic briefing with weather + calendar + tasks
- Voice command trigger only
- No scheduling yet

**Total Effort**: ~20-25 hours

### Phase 2: Communication & News (Est. 2-3 weeks)

**Integrations**:
1. Gmail (6-8 hours)
2. AP News API (4-6 hours)
3. New York Times API (4-6 hours)
4. Google Keep (4-6 hours)

**Morning Briefing Enhancements**:
- Add email, news, and notes to briefing
- Implement scheduled delivery
- Add configuration system

**Total Effort**: ~25-30 hours

### Phase 3: Lifestyle & Entertainment (Est. 2-3 weeks)

**Integrations**:
1. Spotify (6-8 hours)
2. Package Tracking (4-6 hours)
3. Google Fit (3-4 hours)

**Morning Briefing Polish**:
- Weekday vs weekend templates
- Skip functionality
- Context-aware adaptations

**Total Effort**: ~20-25 hours

### Phase 4: Finance & Advanced Features (Est. 1-2 weeks)

**Integrations**:
1. Plaid Finance (8-10 hours - complex auth)

**Morning Briefing Advanced**:
- Gentle wake-up mode (soothing sound fade-in)
- Voice customization
- Advanced privacy controls

**Total Effort**: ~15-20 hours

### Total Implementation: 6-10 weeks (80-100 hours)

**Phases can be parallelized or reordered based on priority.**

## Technical Specifications

### API Selection & Rationale

| Service | API Provider | Reasoning | Cost |
|---------|--------------|-----------|------|
| Calendar | Google Calendar API | Existing OAuth, comprehensive | Free (quota) |
| Email | Gmail API | Existing OAuth, full-featured | Free (quota) |
| News (AP) | AP News API | User subscription, quality journalism | Subscription |
| News (NYT) | NYT API | User subscription, quality journalism | Subscription |
| Weather | OpenWeatherMap | Free tier sufficient, reliable | Free (< 1M calls/mo) |
| Music | Spotify Web API | Industry standard, well-documented | Free |
| Timers/Alarms | Local (Python) | No external API needed | Free |
| Package Tracking | AfterShip | Supports 1000+ carriers | Free tier (100 shipments/mo) |
| Finance | Plaid | Industry leader, secure, supports most banks | Pay-per-user (~$0.50-2/mo) |
| Notes | Google Keep API | Existing OAuth | Free |
| Fitness | Google Fit API | Existing OAuth | Free |

### Configuration File Structure

**config/briefing_config.yaml**:
```yaml
morning_briefing:
  enabled: true
  scheduled_time: "07:00"  # 24-hour format
  timezone: "America/Los_Angeles"

  components:
    weather:
      enabled: true
      location: "Seattle, WA"

    calendar:
      enabled: true
      max_events: 5
      calendars: ["primary", "work"]

    email:
      enabled: true
      unread_only: true
      max_emails: 3
      important_only: false

    tasks:
      enabled: true
      list: "@default"
      max_tasks: 5

    news:
      enabled: true
      sources:
        - name: "ap"
          sections: ["politics", "technology", "world"]
          max_articles: 3
        - name: "nyt"
          sections: ["business", "science"]
          max_articles: 2

    packages:
      enabled: true
      only_if_delivery_today: true

    finance:
      enabled: false  # Privacy: opt-in only
      accounts: ["checking"]  # Don't read full balances by default

    fitness:
      enabled: false
      metrics: ["steps", "active_minutes"]

  templates:
    weekday: "formal"  # More structured
    weekend: "casual"  # More relaxed

  gentle_wakeup:
    enabled: false  # Future feature
    sound: "nature"
    fade_duration_seconds: 60
```

### Environment Variables (.env)

```bash
# Google Services (OAuth)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# News APIs
AP_NEWS_API_KEY=...
NYT_API_KEY=...

# Weather
OPENWEATHER_API_KEY=...

# Music
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...

# Finance
PLAID_CLIENT_ID=...
PLAID_SECRET=...
PLAID_ENV=sandbox  # or development, production

# Package Tracking
AFTERSHIP_API_KEY=...
```

### Database Schema (Optional)

For persistent data (package tracking, user preferences):

```sql
-- Package Tracking
CREATE TABLE packages (
    id INTEGER PRIMARY KEY,
    tracking_number TEXT UNIQUE,
    carrier TEXT,
    status TEXT,
    estimated_delivery DATE,
    last_updated TIMESTAMP,
    marked_received BOOLEAN DEFAULT FALSE
);

-- User Preferences (alternative to config file)
CREATE TABLE user_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP
);

-- Briefing History (for analytics)
CREATE TABLE briefing_logs (
    id INTEGER PRIMARY KEY,
    delivered_at TIMESTAMP,
    components TEXT,  -- JSON array of included components
    duration_seconds FLOAT,
    skipped BOOLEAN
);
```

**Note**: Start with config file, add database only if needed for scale/features.

## Dependencies

### External Dependencies

**APIs & Services**:
- Google Calendar API (OAuth)
- Gmail API (OAuth)
- Google Keep API (OAuth)
- Google Fit API (OAuth)
- AP News API (subscription required)
- New York Times API (subscription required)
- OpenWeatherMap API
- Spotify Web API (OAuth)
- Plaid API (finance)
- AfterShip API (package tracking)

**Python Libraries** (add to requirements.txt):
```
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
spotipy  # Spotify client
plaid-python
apscheduler  # For briefing scheduling
pyyaml  # For config parsing
```

### Internal Dependencies

**Existing Infrastructure**:
- Pipecat pipeline (STT, LLM, TTS)
- OpenAI function calling framework
- Google OAuth setup (from google_tasks integration)
- Home Assistant for timer/alarm triggers (optional)

**New Infrastructure**:
- Configuration management system
- Morning briefing orchestration
- Scheduled task system (APScheduler)
- Optional: Database for persistent data

### Account Requirements

**User Must Have**:
- Google account (for Calendar, Gmail, Keep, Fit)
- Spotify account (for music control)
- AP News subscription (for premium news access)
- New York Times subscription (for premium news access)
- Bank accounts compatible with Plaid (for finance)

**Developer Must Configure**:
- Google Cloud Console project (enable APIs)
- Spotify Developer account (get API credentials)
- Plaid Developer account
- API keys for weather, news, package tracking

## Constraints & Assumptions

### Technical Constraints

**TC1: API Rate Limits**
- Google APIs: 10,000 requests/day (Calendar), 1 billion/day (Gmail)
- Spotify: 180 requests per 30 seconds per user
- Plaid: Limited by plan (Development: 100 Items)
- OpenWeatherMap: 1,000 calls/day (free tier)

**Mitigation**: Implement caching, respect rate limits, upgrade plans if needed

**TC2: Voice Interaction Limitations**
- STT accuracy varies by accent, background noise
- LLM may misinterpret ambiguous commands
- TTS can't convey email formatting, links, etc.

**Mitigation**: Confirmation prompts, clarification questions, fallback to programmatic access

**TC3: Authentication Complexity**
- Multiple OAuth flows (Google, Spotify, Plaid)
- Token expiration and refresh handling
- User must authorize each service separately

**Mitigation**: Clear setup documentation, automated token refresh, graceful error messages

**TC4: Morning Briefing Latency**
- Fetching data from 10+ services takes time
- Sequential API calls would be too slow

**Mitigation**: Parallel API calls, caching, timeout handling, graceful degradation

### Timeline Constraints

**Timeline**: 6-10 weeks for full implementation

**Risks**:
- API changes or deprecations
- Unexpected authentication issues (especially Plaid)
- Scope creep (too many features)

**Mitigation**:
- Phased implementation (MVP first, then iterate)
- Focus on high-priority integrations in Phase 1
- User testing after each phase

### Resource Constraints

**Development Resources**:
- Primary: User (Gyatso) + Claude Code assistant
- No dedicated QA, design, or backend team

**Infrastructure Costs**:
- Hosting: Existing (running locally or on home server)
- API costs: ~$5-10/month (Plaid, AfterShip if over free tier)
- News APIs: Covered by existing subscriptions

### Assumptions

**A1**: User has technical expertise to set up API credentials and OAuth flows

**A2**: User's Google account, Spotify account, and bank accounts are compatible with chosen APIs

**A3**: User primarily uses the assistant in private settings (home) where reading sensitive info aloud is acceptable

**A4**: User is comfortable with voice-first interaction (primary use case)

**A5**: Existing Pipecat infrastructure is stable and performant enough to handle additional integrations

**A6**: OpenAI LLM can reliably interpret user intent for all new commands (based on success with existing integrations)

**A7**: User will configure credentials and settings manually (no automated setup wizard in v1)

## Out of Scope

Explicitly **not** included in this PRD:

### OS1: Multi-User Support
- No user authentication or per-user profiles
- Single-user assistant (no family/roommate separation)
- **Rationale**: Adds complexity, not needed for personal assistant

### OS2: Mobile App
- No dedicated iOS/Android app
- Voice interaction only (no GUI for configuration)
- **Rationale**: Focus on voice-first experience, web UI later if needed

### OS3: Advanced Email Features
- No email filtering, labeling, or organization
- No calendar invite acceptance/decline
- No email search by attachment type
- **Rationale**: Core read/send functionality sufficient for v1

### OS4: Financial Transactions
- No bill pay, transfers, or payments via voice
- Read-only finance access
- **Rationale**: Security risk, regulatory complexity

### OS5: Music Library Management
- No playlist creation/editing (beyond adding songs)
- No lyrics display or music discovery
- **Rationale**: Focus on playback control, not curation

### OS6: Complex Timer Features
- No recurring timers
- No timer linked to specific actions (e.g., "remind me every hour")
- **Rationale**: Basic timer/alarm sufficient for v1

### OS7: Location-Based Features
- No geofencing or location-aware reminders
- No "Where am I?" or navigation queries
- **Rationale**: Home-based assistant, location not critical

### OS8: Third-Party Integrations Beyond Listed
- No Slack, Discord, Twitter, etc.
- No smart home devices beyond Home Assistant
- **Rationale**: Scope management, focus on core life tools

### OS9: Advanced News Features
- No article bookmarking or reading history
- No custom news sources beyond AP/NYT
- No topic-specific deep dives
- **Rationale**: Briefing-focused, not news reader replacement

### OS10: Fitness Coaching
- No workout suggestions or coaching
- Read-only fitness data
- **Rationale**: Google Fit already provides coaching

**Future Consideration**: These features may be added in future iterations based on user feedback and demand.

## Success Metrics & KPIs

### Usage Metrics

**UM1: Morning Briefing Adoption**
- **Metric**: % of days user triggers or receives morning briefing
- **Target**: 80%+ (5-7 days per week)
- **Measurement**: Briefing logs

**UM2: Integration Usage**
- **Metric**: Number of integrations actively used per week
- **Target**: 8+ of 13 integrations
- **Measurement**: Function call logs

**UM3: Daily Voice Interactions**
- **Metric**: Average voice commands per day
- **Current**: 5-10 (Tasks, HA, Search)
- **Target**: 30+ (with new integrations)
- **Measurement**: LLM function call logs

### Performance Metrics

**PM1: Briefing Latency**
- **Metric**: Time from trigger to completion
- **Target**: < 30 seconds (for typical configuration)
- **Measurement**: Briefing timer logs

**PM2: Query Response Time**
- **Metric**: Average time from voice command to response
- **Target**: < 3 seconds (95th percentile)
- **Measurement**: Function execution time logs

**PM3: System Uptime**
- **Metric**: % of time assistant is available
- **Target**: 99%+
- **Measurement**: Health check logs

### Quality Metrics

**QM1: User Satisfaction**
- **Metric**: Self-reported satisfaction score
- **Target**: 8+/10
- **Measurement**: Weekly user survey

**QM2: Error Rate**
- **Metric**: % of commands that fail or require retry
- **Target**: < 5%
- **Measurement**: Error logs

**QM3: Voice Recognition Accuracy**
- **Metric**: % of commands correctly interpreted by LLM
- **Target**: 90%+
- **Measurement**: LLM intent classification logs (manual review)

### Business Metrics

**BM1: Time Savings**
- **Metric**: Minutes saved per day (vs manual app checking)
- **Current**: 0 (manual: 10-15 min/day)
- **Target**: 10-15 min/day (briefing: 2 min)
- **Measurement**: User self-report

**BM2: Assistant Utility**
- **Metric**: User-reported "essential" rating
- **Target**: "Can't live without it" (subjective)
- **Measurement**: User interview

**BM3: Feature Completeness**
- **Metric**: % of daily life tasks covered by assistant
- **Target**: 80%+ (vs 30% currently)
- **Measurement**: User task audit

## Risks & Mitigation

### High Risk

**R1: Plaid Authentication Complexity**
- **Risk**: Bank authentication fails, users unable to link accounts
- **Impact**: High (critical feature)
- **Likelihood**: Medium (Plaid is complex)
- **Mitigation**:
  - Thorough testing with multiple banks
  - Clear error messages and troubleshooting guide
  - Make finance integration optional (not required)
  - Fall back to manual balance entry if needed

**R2: API Rate Limit Exceeded**
- **Risk**: Heavy usage exceeds free tier limits (OpenWeatherMap, Google)
- **Impact**: Medium (service disruption)
- **Likelihood**: Low (single user, reasonable limits)
- **Mitigation**:
  - Implement caching (weather: 30 min, news: 1 hour)
  - Monitor usage via logs
  - Upgrade to paid plans if needed (~$10-20/month)

**R3: Privacy Concerns**
- **Risk**: User uncomfortable with voice assistant reading financial/email data aloud
- **Impact**: High (user trust)
- **Likelihood**: Medium
- **Mitigation**:
  - Privacy controls (confirmation before reading sensitive data)
  - Finance integration disabled by default
  - Clear documentation of data access
  - No cloud storage of sensitive data

### Medium Risk

**R4: OAuth Token Expiration**
- **Risk**: Google/Spotify tokens expire, assistant can't access services
- **Impact**: Medium (service disruption until re-auth)
- **Likelihood**: High (tokens expire after 1-7 days)
- **Mitigation**:
  - Implement robust token refresh logic
  - Graceful error handling (prompt user to re-authenticate)
  - Monitor token expiration in logs

**R5: News API Changes**
- **Risk**: AP or NYT changes API, integration breaks
- **Impact**: Medium (loss of news feature)
- **Likelihood**: Low (stable APIs)
- **Mitigation**:
  - Follow API changelog
  - Implement version checks
  - Fallback to web search if needed

**R6: Scope Creep**
- **Risk**: Too many features requested, timeline extends indefinitely
- **Impact**: Medium (delayed launch)
- **Likelihood**: High (common issue)
- **Mitigation**:
  - Strict adherence to phased implementation
  - "Out of Scope" section clearly defined
  - Regular check-ins to assess progress vs scope

### Low Risk

**R7: Timer System Reliability**
- **Risk**: Python-based timers miss triggers or lose state
- **Impact**: Low (annoying but not critical)
- **Likelihood**: Low (Python timers reliable)
- **Mitigation**:
  - Use robust library (APScheduler)
  - Persist timer state to disk
  - Integration with Home Assistant as backup

**R8: Voice Recognition Failure**
- **Risk**: STT misunderstands commands in noisy environment
- **Impact**: Low (user retries command)
- **Likelihood**: Medium (depends on environment)
- **Mitigation**:
  - Use high-quality STT (Deepgram)
  - Confirmation prompts for critical actions
  - Programmatic access as fallback

## Future Enhancements

Beyond the scope of this PRD, potential future features:

### FE1: Multi-User Support
- User profiles and authentication
- Per-user briefings and preferences
- Family calendar and shared tasks

### FE2: Gentle Wake-Up Mode
- Soothing sound playback (nature, music)
- Gradual fade-in and volume decrease
- Briefing starts as sound fades
- Smart alarm (wake during light sleep phase with fitness tracker)

### FE3: Context-Aware Suggestions
- "Traffic is bad, leave 15 min early for your meeting"
- "You have a gym appointment but it's raining, suggest indoor workout?"
- "Low bank balance, skip expensive dinner suggestion"

### FE4: Advanced Email Automation
- Auto-respond to simple emails
- Email summarization (daily digest)
- Priority inbox management
- Calendar invite auto-accept/decline

### FE5: Smart Home Integration
- Trigger home automation based on briefing (lights on during briefing)
- Weather-based home adjustments (close blinds if sunny)
- Package arrival notifications via doorbell camera

### FE6: Mobile Companion App
- Visual dashboard for briefing
- Quick toggles for integrations
- Fallback when voice isn't available

### FE7: Advanced Finance Features
- Spending analytics and budgeting
- Bill reminders
- Investment portfolio tracking
- Cryptocurrency prices

### FE8: Health & Wellness
- Medication reminders
- Water intake tracking
- Sleep quality monitoring (via Google Fit or sleep tracker)

### FE9: Learning & Personalization
- Learn user preferences over time
- Adaptive briefing (show what user actually cares about)
- Predictive suggestions

### FE10: Multi-Device Support
- Sync across multiple assistants (bedroom, office, kitchen)
- Seamless handoff between devices
- Distributed briefing (start in bedroom, continue in kitchen)

## Appendix

### A1: API Documentation Links

- [Google Calendar API](https://developers.google.com/calendar)
- [Gmail API](https://developers.google.com/gmail/api)
- [Google Keep API](https://developers.google.com/keep)
- [Google Fit API](https://developers.google.com/fit)
- [AP News API](https://developer.ap.org/)
- [New York Times API](https://developer.nytimes.com/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [Plaid API](https://plaid.com/docs/)
- [AfterShip API](https://developers.aftership.com/)

### A2: Example Voice Interactions

**Morning Briefing**:
```
User: "Good morning"
Alex: "Good morning! It's Wednesday, October 30th. The weather today is partly cloudy
       with a high of 62 degrees. You have three events on your calendar: team standup
       at 9am, lunch with Sarah at noon, and dentist appointment at 3pm. You have 5
       unread emails, including one from your manager marked important. Your top task
       for today is to finish the quarterly report. In the news, AP reports that...
       [continues with news headlines]. You have one package arriving today from Amazon.
       That's your briefing. Have a great day!"
```

**Calendar**:
```
User: "What's on my calendar today?"
Alex: "You have three events today: team standup at 9am, lunch with Sarah at noon,
       and dentist appointment at 3pm."

User: "Schedule a meeting with John tomorrow at 2pm"
Alex: "Creating a meeting with John for tomorrow, October 31st at 2pm. What should
       I title it?"
User: "Project sync"
Alex: "Done! I've created 'Project sync with John' for tomorrow at 2pm."
```

**Email**:
```
User: "Do I have any unread emails?"
Alex: "You have 5 unread emails. The most recent are from your manager about the
       quarterly review, from Amazon about your order shipment, and from LinkedIn
       about job recommendations."

User: "Read the one from my manager"
Alex: "Email from Sarah Johnson, subject 'Quarterly Review Meeting', received 2 hours
       ago: 'Hi, I'd like to schedule our quarterly review for next week. Are you
       available Tuesday or Wednesday afternoon? Let me know. Thanks, Sarah.'"
```

**News**:
```
User: "What's the latest news?"
Alex: "Here are today's top stories: From AP News, 'Congress passes infrastructure
       bill after months of debate' - The bill includes 550 billion in new spending...
       From the New York Times, 'Tech companies face new AI regulations' - European
       Union proposes strict rules..."
```

**Timer**:
```
User: "Set a timer for 20 minutes"
Alex: "Timer set for 20 minutes. I'll let you know when it's done."

[20 minutes later]
Alex: "Your 20-minute timer is done."
```

### A3: Configuration Examples

**Minimal Configuration** (just briefing enabled):
```yaml
morning_briefing:
  enabled: true
  scheduled_time: "07:00"
  components:
    weather: { enabled: true }
    calendar: { enabled: true }
    tasks: { enabled: true }
```

**Power User Configuration** (all features):
```yaml
morning_briefing:
  enabled: true
  scheduled_time: "06:30"
  timezone: "America/Los_Angeles"

  components:
    weather: { enabled: true, location: "Seattle, WA" }
    calendar: { enabled: true, max_events: 10, calendars: ["primary", "work", "personal"] }
    email: { enabled: true, max_emails: 5, important_only: true }
    tasks: { enabled: true, max_tasks: 8 }
    news:
      enabled: true
      sources:
        - { name: "ap", sections: ["politics", "tech", "business"], max_articles: 3 }
        - { name: "nyt", sections: ["science", "health"], max_articles: 2 }
    packages: { enabled: true }
    finance: { enabled: true, accounts: ["checking", "savings"] }
    fitness: { enabled: true, metrics: ["steps", "calories"] }

  templates:
    weekday: "formal"
    weekend: "casual"
```

### A4: Testing Plan

**Unit Tests**:
- Each integration module has test coverage
- Mock external APIs
- Test error handling paths

**Integration Tests**:
- Test morning briefing with all components
- Test OAuth flows
- Test configuration loading

**Manual Testing**:
- Voice command testing in real environment
- User acceptance testing after each phase
- Privacy/security review

**Performance Testing**:
- Load test API calls (simulate heavy usage)
- Measure briefing latency
- Test parallel API calls

### A5: Rollout Plan

**Week 1-2**: Phase 1 (Calendar, Weather, Timer)
- Implement integrations
- Basic morning briefing MVP
- User testing

**Week 3-4**: Phase 2 (Gmail, News, Keep)
- Add communication tools
- Enhanced morning briefing
- Configuration system

**Week 5-6**: Phase 3 (Spotify, Packages, Fit)
- Lifestyle integrations
- Briefing polish
- Skip functionality

**Week 7-8**: Phase 4 (Finance)
- Plaid integration
- Privacy controls
- Final testing

**Week 9-10**: Polish & Documentation
- Bug fixes
- Comprehensive documentation
- User training

---

**End of PRD**

**Next Steps**:
1. Review and approval
2. Run `/pm:prd-parse extensive-tools` to create implementation epic
3. Begin Phase 1 development
