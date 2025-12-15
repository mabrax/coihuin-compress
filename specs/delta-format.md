# Delta Format Specification

Version: 1.0.0

## Overview

A **delta** captures incremental changes between two checkpoints. Instead of regenerating a full summary each time, deltas record only what changed, enabling efficient state reconstruction and audit trails.

## Design Principles

1. **Incremental**: Only capture what changed, not the full state
2. **Anchored**: Always reference the checkpoints it bridges
3. **Mergeable**: Can be merged into the target checkpoint to produce a new full state
4. **Auditable**: Provides history of how work evolved

## Relationship to Checkpoints

```
[chk-001] ---(delta-001-002)---> [chk-002] ---(delta-002-003)---> [chk-003]
    ^                                ^                                ^
    |                                |                                |
 Full State                     Full State                       Full State
                    ^                                ^
                    |                                |
              Changes Only                    Changes Only
```

**Key insight from Factory.ai**: Rather than regenerating the entire summary per request, maintain a persistent summary and update it incrementally when truncating old messages.

## Structure

```markdown
---
delta: <from-checkpoint>-to-<to-checkpoint>
created: <ISO-8601 timestamp>
from: <source checkpoint id>
to: <target checkpoint id>
---

## Summary
[One-sentence description of what this delta represents]

## Changes

### Added
[New information that didn't exist in the source checkpoint]

### Modified
[Information that changed between checkpoints]

| Section/Field | Before | After |
|---------------|--------|-------|
| ... | ... | ... |

### Removed
[Information dropped from the checkpoint - no longer relevant]

### Status Transitions
[State changes for tracked items]

| Item | Before | After |
|------|--------|-------|
| ... | ... | ... |

## Merge Instructions
[How to apply this delta to produce the target checkpoint]
```

## Field Definitions

### Header Fields

| Field | Required | Description |
|-------|----------|-------------|
| `delta` | Yes | Identifier in format `<from>-to-<to>` |
| `created` | Yes | ISO-8601 timestamp |
| `from` | Yes | Source checkpoint ID |
| `to` | Yes | Target checkpoint ID |

### Body Sections

| Section | Required | Purpose |
|---------|----------|---------|
| Summary | Yes | Quick description of what changed |
| Added | Yes* | New information introduced |
| Modified | Yes* | Changed information with before/after |
| Removed | Yes* | Information no longer relevant |
| Status Transitions | No | State changes for tracked items |
| Merge Instructions | No | How to mechanically apply the delta |

*At least one of Added/Modified/Removed must be present.

## Delta Categories

### 1. Structural Deltas
Changes to the shape of information:
- New sections added
- Sections removed
- Section reorganization

### 2. Value Deltas
Changes to specific values:
- Version updates
- Status changes
- Configuration modifications

### 3. Artifact Deltas
Changes to tracked files/outputs:
- New files created
- Files modified
- Files deleted

### 4. Progress Deltas
Changes to work state:
- Phases completed
- Tasks done
- Blockers resolved/introduced

## Delta Triggers

Generate a delta when:

1. **Checkpoint created**: Always generate delta from previous checkpoint
2. **Significant change**: Major decision or direction shift
3. **Audit required**: Need to track what happened between states

## Compression Strategy

Deltas enable efficient compression because:

1. **Avoid re-summarization**: Only summarize the new span
2. **Merge incrementally**: Update existing summary rather than regenerate
3. **Prune history**: Old deltas can be dropped once merged into checkpoint

```
Naive approach (Factory's "Naive"):
[Full conversation] → Summarize all → Summary

Incremental approach (This spec):
[New span only] → Delta → Merge into existing checkpoint → Updated checkpoint
```

## Example

```markdown
---
delta: chk-002-to-chk-003
created: 2025-12-14T16:00:00Z
from: chk-002
to: chk-003
---

## Summary
Phase 3 (Game Mechanics) completed: timer, scoring, and combo system implemented.

## Changes

### Added

**New Files Created:**
| File | Purpose |
|------|---------|
| `src/services/scoring.ts` | Score calculation, combos, stars |
| `src/hooks/useTimer.ts` | Timer with pause/resume, penalty |
| `src/hooks/useGameState.ts` | Game state with useReducer |
| `src/components/Timer/Timer.tsx` | MM:SS display with critical colors |
| `src/components/ScoreBoard/ScoreBoard.tsx` | Live score, combo, accuracy |
| `src/components/GameOverModal/GameOverModal.tsx` | Stars and score breakdown |

**New Functionality:**
- 3 game modes: Combined, Timed, Precision
- Combo system: x1 (1-2), x1.5 (3-5), x2 (6-9), x3 (10+)
- Star rating: 3 (>95%), 2 (>75%), 1 (>50%)
- Timer penalty: -5 seconds per error

### Modified

| Section | Before | After |
|---------|--------|-------|
| Play-By-Play | Phases 1-2 complete | Phases 1-3 complete |
| Current State | Phase 2 done, Phase 3 next | Phase 3 done, Phase 4 next |
| Next Actions | Implement game mechanics | Implement levels and progression |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| Phase 3: Sistema de Juego | Ready | Closed |
| Phase 4: Niveles y Progresión | Blocked | Ready |

## Merge Instructions
1. Append new files to Artifact Trail
2. Add Phase 3 to Play-By-Play as completed
3. Replace Current State with Phase 3 complete
4. Replace Next Actions with Phase 4 tasks
5. Update phase status table
```

## Delta Lifecycle

```
1. Create checkpoint N
2. Work continues...
3. Create checkpoint N+1
4. Generate delta N-to-N+1
5. (Optional) Validate: apply delta to N, compare with N+1
6. Archive or discard delta once no longer needed for audit
```

## References

- Factory.ai: "Compressing Context" - Incremental update strategy
- Git: Commit (snapshot) + diff (delta) model
- Example deltas: `docs/examples/delta-*.md`
