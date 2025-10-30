# GitHub Issue Mapping: extensive-tools Epic

**Epic Issue**: [#21](https://github.com/zach-fau/home-assistant/issues/21) - Epic: Extensive Tools Integration

**Created**: 2025-10-30
**Status**: backlog
**Progress**: 0/10 tasks completed (0%)

---

## Task Issues

| Local File | GitHub Issue | Title | Status | Dependencies |
|------------|--------------|-------|--------|--------------|
| 22.md | [#22](https://github.com/zach-fau/home-assistant/issues/22) | Configuration System + Weather Integration | open | None |
| 23.md | [#23](https://github.com/zach-fau/home-assistant/issues/23) | Google Services Bundle (Calendar, Gmail, Keep, Fit) | open | #22 |
| 24.md | [#24](https://github.com/zach-fau/home-assistant/issues/24) | Timer/Alarm System (APScheduler) | open | #22 |
| 25.md | [#25](https://github.com/zach-fau/home-assistant/issues/25) | Unified News Integration (AP + NYT) | open | #22 |
| 26.md | [#26](https://github.com/zach-fau/home-assistant/issues/26) | Morning Briefing Core (Manager + Scheduler) | open | #22, #23, #25 |
| 27.md | [#27](https://github.com/zach-fau/home-assistant/issues/27) | Briefing Polish (Skip, Templates, Context-Aware) | open | #26 |
| 28.md | [#28](https://github.com/zach-fau/home-assistant/issues/28) | Spotify Music Control | open | #22 |
| 29.md | [#29](https://github.com/zach-fau/home-assistant/issues/29) | Package Tracking (AfterShip) | open | #22, #26 |
| 30.md | [#30](https://github.com/zach-fau/home-assistant/issues/30) | Plaid Finance Integration | open | #22 |
| 31.md | [#31](https://github.com/zach-fau/home-assistant/issues/31) | Integration Testing + Documentation | open | #22-#30 |

---

## Original Task Numbers → GitHub Issues

| Original | GitHub Issue |
|----------|--------------|
| 001.md   | #22          |
| 002.md   | #23          |
| 003.md   | #24          |
| 004.md   | #25          |
| 005.md   | #26          |
| 006.md   | #27          |
| 007.md   | #28          |
| 008.md   | #29          |
| 009.md   | #30          |
| 010.md   | #31          |

---

## Parallelization Opportunities

### Phase 1: Foundation (Sequential)
- #22 → #23 → (parallel opportunities open up)

### Phase 2: Parallel Execution (After #22)
Can be worked on simultaneously:
- #24 (Timer/Alarm System)
- #25 (Unified News Integration)

### Phase 3: Briefing MVP (After #22, #23, #25)
- #26 (Morning Briefing Core) - Sequential, blocks Phase 4

### Phase 4: Parallel Features (After #26)
Can be worked on simultaneously:
- #27 (Briefing Polish) - Note: conflicts with #26, wait for it to complete
- #28 (Spotify Music Control)
- #29 (Package Tracking)
- #30 (Plaid Finance)

### Phase 5: Final Validation (After all above)
- #31 (Integration Testing + Documentation) - Sequential, final task

---

## Epic Timeline

**Estimated Total Effort**: 58 hours

### Critical Path (Sequential Tasks)
1. #22 (6h) → Foundation
2. #23 (8h) → Google Services
3. #26 (8h) → Briefing Core
4. #31 (4h) → Final Testing

**Critical Path Total**: 26 hours

### Parallel Tasks (Can Execute Concurrently)
- #24 (4h) - Timer/Alarm
- #25 (6h) - News
- #27 (2h) - Briefing Polish
- #28 (6h) - Spotify
- #29 (6h) - Package Tracking
- #30 (8h) - Plaid Finance

**Parallel Tasks Total**: 32 hours

---

## Repository Information

- **GitHub Repository**: zach-fau/home-assistant
- **Epic Branch**: epic/extensive-tools (to be created as worktree)
- **Base Directory**: `.claude/epics/extensive-tools/`
- **PRD**: `.claude/prds/extensive-tools.md`

---

## Notes

- All task files renamed from sequential numbering (001-010) to GitHub issue numbers (22-31)
- All `depends_on` and `conflicts_with` fields updated to reference GitHub issue numbers
- Epic issue (#21) created on GitHub with full context
- Ready for `/pm:epic-start extensive-tools` to begin implementation
