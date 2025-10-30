---
name: better-search
status: in_progress
created: 2025-10-30T20:26:36Z
updated: 2025-10-30T20:50:40Z
progress: 33%
prd: .claude/prds/better-search.md
github: null
---

# Epic: better-search

## Overview

Add immediate, hardcoded voice acknowledgments to mask search API latency and create a more responsive, natural conversation experience. This is a **minimal, surgical change** to the existing event handler system - no new architecture, no new dependencies, just ~20 lines of code to dramatically improve perceived responsiveness.

**Core Problem**: 4-7 seconds of silence when user asks search questions makes the system feel broken.

**Solution**: Speak within 500ms using hardcoded phrases while search executes in background.

## Architecture Decisions

### AD1: Use Existing Event Handler Infrastructure
**Decision**: Modify `on_function_calls_started` event handler in `functions/__init__.py`

**Rationale**:
- ✅ Event already exists and fires at the right time
- ✅ Has access to TTS service and function metadata
- ✅ Zero new infrastructure needed
- ✅ Leverages Pipecat's async execution model (acknowledgment + search run in parallel)

**Alternative Rejected**: Create new middleware layer → Too complex for simple feature

### AD2: Hardcoded Phrase Pool with Random Selection
**Decision**: Define 6 phrase strings, use `random.choice()` for variety

**Rationale**:
- ✅ Instant execution (<1ms phrase selection vs 1-2s LLM generation)
- ✅ Simple to implement and maintain
- ✅ Sufficient variety to avoid robotic repetition
- ✅ Easy to customize/extend later

**Alternative Rejected**: LLM-generated acknowledgments → Too slow (defeats the purpose)

### AD3: Function-Name-Based Triggering
**Decision**: Check `fc.function_name == "web_search"` to trigger acknowledgment

**Rationale**:
- ✅ Only applies to slow functions (search), not fast ones (lights)
- ✅ Easy to extend to other functions later (Google Tasks, etc.)
- ✅ No configuration needed - uses existing function metadata

**Alternative Rejected**: Always acknowledge all functions → Unnecessary for fast HA calls

### AD4: Direct TTS Queue, No LLM Bypass
**Decision**: Call `tts.queue_frame(TTSSpeakFrame(phrase))` directly in event handler

**Rationale**:
- ✅ Bypasses LLM generation delay entirely
- ✅ Pipecat handles queueing and ordering automatically
- ✅ Non-blocking - doesn't delay function execution
- ✅ Already proven pattern in error handler

**Alternative Rejected**: Try to make LLM faster → Can't reliably get <500ms

## Technical Approach

### No Frontend/UI Changes
This is entirely backend/voice pipeline work. Zero UI changes needed.

### Backend: Single File Modification

**File**: `pipecat-quickstart/functions/__init__.py`
**Function**: `setup_event_handlers()`
**Lines Changed**: ~20 lines (add phrase pool + selection logic)

**Current Code** (lines 41-53):
```python
@llm.event_handler("on_function_calls_started")
async def on_function_start(service, function_calls):
    logger.info(f"Function calls started: {[fc.function_name for fc in function_calls]}")
    # LLM naturally generates acknowledgments - no manual intervention needed
```

**Modified Code**:
```python
@llm.event_handler("on_function_calls_started")
async def on_function_start(service, function_calls):
    logger.info(f"Function calls started: {[fc.function_name for fc in function_calls]}")

    # Immediate acknowledgments for search (masks API latency)
    import random

    # Phrase pool for variety
    SEARCH_ACKNOWLEDGMENTS = [
        "Hold on",
        "Give me a sec",
        "Let me check",
        "One moment",
        "Looking that up",
        "Searching"
    ]

    for fc in function_calls:
        if fc.function_name == "web_search":
            phrase = random.choice(SEARCH_ACKNOWLEDGMENTS)
            await tts.queue_frame(TTSSpeakFrame(phrase))
            logger.info(f"Immediate acknowledgment: '{phrase}' for {fc.function_name}")
```

**That's it.** No other files need to change.

### Infrastructure: Zero Changes

- ✅ No new dependencies
- ✅ No new API keys
- ✅ No database changes
- ✅ No deployment changes
- ✅ No configuration files

## Implementation Strategy

### Phase 1: Core Implementation (30 min)
**Simplest path to working feature:**

1. Add phrase pool constant to `functions/__init__.py`
2. Add random selection logic in event handler
3. Add TTS queue call for web_search functions
4. Add logging for verification

**Deliverable**: Working acknowledgments for search

### Phase 2: Testing & Validation (30 min)
**Verify it works and meets requirements:**

1. **Latency test**: Log timestamps, verify <500ms
2. **Variety test**: Trigger 10 searches, verify different phrases
3. **Parallel test**: Verify search still completes while speaking
4. **Error test**: Verify graceful handling if TTS fails

**Deliverable**: Validated implementation meeting success criteria

### Phase 3: Documentation (15 min)
**Minimal docs update:**

1. Add code comments explaining the pattern
2. Update `system-patterns.md` with "Immediate Acknowledgment Pattern"
3. Optional: Add to progress.md

**Deliverable**: Documented feature

**Total Time**: ~1.5 hours (not 3-4 as PRD estimated - simpler than initially planned)

## Task Breakdown Preview

Breaking this down into **minimal, sequential tasks**:

- [ ] **Task 1**: Add immediate voice acknowledgments for web search (30 min)
  - Modify event handler
  - Add phrase pool
  - Implement random selection
  - Add logging

- [ ] **Task 2**: Test and validate latency improvements (30 min)
  - Measure TTFS (time to first sound)
  - Test phrase variety
  - Verify no blocking/race conditions
  - Validate against success criteria

- [ ] **Task 3**: Document immediate acknowledgment pattern (15 min)
  - Add code comments
  - Update system-patterns.md
  - Update progress tracking

**Total: 3 tasks, ~1.5 hours**

## Dependencies

### Internal Dependencies
**All already satisfied:**
- ✅ Pipecat event system (`on_function_calls_started`)
- ✅ TTS service (Cartesia with `queue_frame()` support)
- ✅ Function metadata (function name available in event)

### External Dependencies
**None - everything needed already exists**

### No Blockers
This feature can be implemented immediately with zero waiting.

## Success Criteria (Technical)

### Performance Benchmarks
| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Time to first sound (TTFS) | 4-7s | <500ms | Log timestamps |
| Acknowledgment duration | N/A | 0.5-1.5s | TTS synthesis time |
| Search completion time | 3-5s | 3-5s (unchanged) | Tavily API latency |
| Total perceived latency | 4-7s | <1s (ack) + 3-5s (search) | User experience |

### Quality Gates
**Before marking as complete:**
- [ ] TTFS measured at <500ms (10 test runs)
- [ ] All 6 phrases used at least once in 20 trials
- [ ] No errors in logs during concurrent searches
- [ ] Search results still arrive correctly (no blocking)
- [ ] User (Gyatso) confirms improved responsiveness

### Acceptance Criteria
From PRD user stories - must satisfy:
1. ✅ Voice acknowledgment plays within 500ms of search trigger
2. ✅ Acknowledgment is brief (1-3 words)
3. ✅ Search continues in background while speaking
4. ✅ Multiple varied acknowledgments (not always same phrase)
5. ✅ Phrases sound natural ("Hold on" vs "Initiating search protocol")

## Estimated Effort

**Revised estimate: 1.5-2 hours** (down from PRD's 3-4 hours)

**Why shorter?**
- Extremely focused scope (1 file, 1 function)
- Leverages 100% existing infrastructure
- No new dependencies or configuration
- Testing is straightforward (log analysis)

**Breakdown**:
- Implementation: 30 min
- Testing: 30 min
- Documentation: 15 min
- Buffer: 15 min

**Critical Path**: None - can be done in single session

**Resource Requirements**: 1 developer (Gyatso + Claude Code)

## Risks & Mitigation

### Low-Risk Implementation

**Risk 1: TTS latency >500ms**
- **Likelihood**: Very Low (Cartesia typically <300ms for short phrases)
- **Impact**: Medium (defeats purpose)
- **Mitigation**: Test with real API first; if needed, use 1-word phrases ("Searching")

**Risk 2: Acknowledgment overlaps with results**
- **Likelihood**: Very Low (0.5-1.5s acknowledgment + 3-5s search = no overlap)
- **Impact**: Low (sounds weird but doesn't break)
- **Mitigation**: Keep phrases very brief; Pipecat handles queuing

**Risk 3: Users find it annoying**
- **Likelihood**: Very Low (universally accepted UX pattern)
- **Impact**: Low (easy to disable)
- **Mitigation**: Natural variety prevents roboticness; easy to turn off if needed

## Future Enhancements

**Not in scope, but easy to add later:**

1. **Per-function phrase pools** (5 min)
   - Google Tasks: "Let me check your tasks..."
   - Home Assistant: (none - fast enough without)

2. **User configuration** (30 min)
   - Add config file for custom phrases
   - Toggle acknowledgments on/off per function

3. **Progress updates** (1 hour)
   - "Still looking..." if search takes >5s
   - Requires timer + second TTS call

4. **Analytics** (1 hour)
   - Track phrase usage distribution
   - Measure completion rates before/after
   - A/B test different phrase sets

**None of these are needed for v1** - the basic implementation solves the problem.

## Simplifications from PRD

The PRD was comprehensive but we can simplify:

1. **Dropped**: Phase 3 (function-specific customization)
   - **Why**: Only web_search is slow enough to need this
   - **Savings**: 30 minutes

2. **Dropped**: Automated testing setup
   - **Why**: Manual testing with logs is sufficient for 1.5 hour feature
   - **When**: Add tests later if we expand the feature

3. **Dropped**: Configuration system
   - **Why**: Hardcoded phrases work fine, easy to change later
   - **Savings**: No config file, no loading logic

4. **Kept**: Everything that actually solves the problem
   - Immediate acknowledgments ✅
   - Phrase variety ✅
   - Performance targets ✅

**Result**: Same user value, half the implementation time.

---

**Implementation Priority**: High (major UX improvement, minimal effort)
**Technical Risk**: Low (simple, well-understood change)
**User Impact**: High (4-7s → <1s perceived latency)
**Maintenance Burden**: Negligible (20 lines of code, no new dependencies)

**Ready to implement!** This is a textbook "quick win" - high impact, low effort, low risk.

## Tasks Created
- [x] 001.md - Add immediate voice acknowledgments for web search (parallel: false) ✅ Completed 2025-10-30
- [ ] 002.md - Test and validate latency improvements (parallel: false, depends on: 001)
- [ ] 003.md - Document immediate acknowledgment pattern (parallel: false, depends on: 001, 002)

Total tasks: 3
Completed: 1
In Progress: 0
Remaining: 2
Parallel tasks: 0
Sequential tasks: 3
Estimated total effort: 1.25 hours (0.5 + 0.5 + 0.25)
Actual effort (001): ~0.3 hours (faster than estimated)
