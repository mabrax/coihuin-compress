---
name: coihuin-compress
description: Proactive context compression for long coding sessions. Creates checkpoints (state snapshots) and deltas (incremental changes). Use when the user asks to "create checkpoint", "checkpoint", "save state", "compress context", "create delta", "delta", "what changed", or "merge checkpoint".
---

# Coihuin Compress

Proactive context compression at natural breakpoints, not reactive to token limits.

## Workflow

```
Session 1 (new work):
  → "checkpoint" → creates new checkpoint

Session 2+ (continuing):
  → User loads checkpoint manually
  → work...
  → "merge" → generates delta + merges into checkpoint

Done:
  → move checkpoint to archive/
```

**Key principle**: User controls the flow. Load checkpoint manually, then tell the skill what to do.

## Operations

### Checkpoint

Create new state snapshot from scratch.

**Trigger**: "checkpoint", "create checkpoint", "save state"

**When**: New work, fresh start, or no existing checkpoint to merge into.

**How**:
1. Read `checkpoint-format.md` for structure
2. Extract "What Must Survive" from conversation
3. Generate checkpoint following the format
4. Save to `checkpoints/active/<name>.md`
5. Validate: `uv run validate.py checkpoint <file>`

### Delta

Show incremental changes since loaded checkpoint (without merging).

**Trigger**: "delta", "create delta", "what changed"

**Prerequisite**: User has loaded existing checkpoint into context.

**When**: Want to see changes without merging, or need standalone delta for audit.

**How**:
1. Read `delta-format.md` for structure
2. Load the source checkpoint
3. Categorize changes: Added / Modified / Removed / Status Transitions
4. Generate delta following the format
5. Validate: `uv run validate.py delta <file>`

### Merge

Generate delta and apply to loaded checkpoint.

**Trigger**: "merge", "merge checkpoint", "update checkpoint"

**Prerequisite**: User has loaded existing checkpoint into context.

**How**:
1. Generate delta (comparing loaded checkpoint vs current session)
2. Show delta to user for review
3. Apply changes to checkpoint:
   - **Decisions**: Append new decisions
   - **Play-By-Play**: Append new entries, summarize old
   - **Artifact Trail**: Update file statuses, add new files
   - **Current State**: Replace entirely
   - **Next Actions**: Replace entirely
4. Update `created` timestamp in frontmatter
5. Output merged checkpoint (user saves to file)
6. Optionally output delta for audit

### Archive

Move completed checkpoint to historical storage.

**When**: Feature/epic complete, work finished.

**How**:
1. Move from `checkpoints/active/` to `checkpoints/archive/`
2. Optionally keep associated deltas for audit trail

## Directory Structure

```
checkpoints/
├── active/                    # Currently loaded into context
│   └── chk-feature-name.md    # One per active feature/epic
└── archive/                   # Historical, not loaded
    ├── chk-auth-system.md
    └── chk-payment-flow.md
```

## Reference Files

| File | Purpose |
|------|---------|
| `checkpoint-format.md` | Checkpoint structure specification |
| `delta-format.md` | Delta structure specification |
| `examples/checkpoint.md` | Reference checkpoint example |
| `examples/delta.md` | Reference delta example |
| `validate.py` | Format validation script |

## Priority Hierarchy (token pressure)

1. **Must Keep**: Problem, session intent, decisions, current state, next actions
2. **Should Keep**: Recent artifact trail, recent play-by-play, technical context
3. **Can Summarize**: Older play-by-play, completed artifacts, historical decisions
