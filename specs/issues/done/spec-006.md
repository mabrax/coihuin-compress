---
id: spec-006
title: Delta-as-Operation Model
issue: ISSUE-006
version: 1.0.0
created: 2025-12-17
---

# Delta-as-Operation Model

## Overview

This specification simplifies coihuin-compress from a three-concept model (checkpoint, delta artifact, merge) to a two-operation model (checkpoint, delta). Based on real-world usage, users never create separate delta files—they simply want to update existing checkpoints with what changed.

The word "delta" carries inherent semantic meaning (change/difference). Using "delta" as a verb—"delta the checkpoint"—is intuitive and eliminates unnecessary conceptual overhead.

## Design Principles

1. **Two operations only**: checkpoint (create) and delta (update)
2. **No intermediate artifacts**: Delta is an operation, not a file
3. **Git for history**: Version tracking delegated to Git, not duplicate artifacts
4. **Inline over separate**: Changes recorded inline in checkpoint, not in separate files

## Design Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| Keep delta artifact files? | No | Users always skip them; Git provides history |
| Keep "merge" command? | No | Confusing; "delta" already implies the update |
| Keep inline delta sections? | Yes | Useful for seeing recent changes in checkpoint |
| What about delta-format.md? | Archive/remove | Spec for an artifact we're eliminating |
| How to track progression? | Git | `git log`, `git diff` provide full history |

## Structure

### The Two Operations

| Operation | Trigger | Action |
|-----------|---------|--------|
| **checkpoint** | "checkpoint", "create checkpoint", "save state" | Create fresh snapshot from scratch |
| **delta** | "delta", "update checkpoint", "add delta" | Update existing checkpoint with what changed |

### Workflow

```
Session 1 (new work):
  → "checkpoint" → creates new checkpoint

Session 2+ (continuing):
  → User loads checkpoint manually
  → work...
  → "delta" → identifies changes, updates checkpoint inline

Done:
  → move checkpoint to archive/
```

### What "Delta" Does

When user says "delta":

1. Identify what changed since checkpoint was loaded
2. Update checkpoint sections:
   - **Decisions**: Append new decisions
   - **Play-By-Play**: Append new entries, summarize old
   - **Artifact Trail**: Update file statuses, add new files
   - **Current State**: Replace entirely
   - **Next Actions**: Replace entirely
   - **Breadcrumbs**: Add new, prune stale
3. Add inline delta section with timestamp (optional, for visibility)
4. Update `last_delta` timestamp in frontmatter
5. Output updated checkpoint

### Inline Delta Section Format

When changes are significant, append an inline delta section to the checkpoint:

```markdown
---

## Delta: <ISO-8601 timestamp>

### What Changed
[Brief summary of changes]

### Artifacts
| File | Action | Description |
|------|--------|-------------|
| ... | created/modified/deleted | ... |

### Status Transitions
| Item | Before | After |
|------|--------|-------|
| ... | ... | ... |

### Breadcrumbs
| Type | Reference | Hint |
|------|-----------|------|
| ... | ... | ... |
```

This section is **part of the checkpoint file**, not a separate artifact. It provides immediate visibility into recent changes without needing Git.

## Removals

### Files to Archive/Delete

| File | Action | Reason |
|------|--------|--------|
| `.claude/skills/coihuin-compress/delta-format.md` | Delete | Spec for eliminated artifact |
| `specs/delta-format.md` | Delete | Duplicate spec |
| `examples/delta.md` | Delete | Example of eliminated artifact |

### Concepts to Remove from SKILL.md

1. **Delta operation** (current): "Show incremental changes since loaded checkpoint (without merging)" → DELETE
2. **Merge operation**: Entire section → DELETE
3. **Reference to delta-format.md**: Remove from table
4. **Reference to examples/delta.md**: Remove from table

### Concepts to Add to SKILL.md

1. **Delta operation** (new): "Update existing checkpoint with what changed"

## SKILL.md Changes

### Before (Operations section)

```markdown
### Delta
Show incremental changes since loaded checkpoint (without merging).
...

### Merge
Generate delta and apply to loaded checkpoint.
...
```

### After (Operations section)

```markdown
### Delta
Update existing checkpoint with what changed.

**Trigger**: "delta", "update checkpoint", "add delta"

**Prerequisite**: User has loaded existing checkpoint into context.

**How**:
1. Identify changes since checkpoint was loaded:
   - New decisions made
   - Work completed (play-by-play)
   - Files created/modified/deleted
   - State transitions
2. Update checkpoint sections:
   - **Decisions**: Append new
   - **Play-By-Play**: Append new, summarize old
   - **Artifact Trail**: Update statuses, add new files
   - **Current State**: Replace entirely
   - **Next Actions**: Replace entirely
   - **Breadcrumbs**: Add new, prune stale
3. Optionally add inline delta section for visibility
4. Update `last_delta` timestamp in frontmatter
5. Output updated checkpoint (user saves to file)

**Git for history**: Use `git log checkpoints/active/<file>.md` to see checkpoint progression over time.
```

### Reference Files Table (update)

| File | Purpose |
|------|---------|
| `checkpoint-format.md` | Checkpoint structure specification |
| `examples/checkpoint.md` | Reference checkpoint example |
| `validate.py` | Format validation script |

(Remove delta-format.md and examples/delta.md rows)

## Implementation

Execute changes in this order:

### Step 1: Delete delta artifact files

```bash
rm .claude/skills/coihuin-compress/delta-format.md
rm specs/delta-format.md
rm -f examples/delta.md  # if exists
```

### Step 2: Update SKILL.md

1. Replace Workflow diagram (remove "merge" reference)
2. Replace Delta operation section (new definition)
3. Delete Merge operation section entirely
4. Update Reference Files table (remove delta entries)

### Step 3: Update checkpoint-format.md (optional)

Add to frontmatter fields table:
- `last_delta` (optional): ISO-8601 timestamp of last delta operation

### Step 4: Validate

1. Verify skill loads: trigger skill and confirm no errors
2. Test checkpoint operation: create a test checkpoint
3. Test delta operation: load checkpoint, make changes, run delta
4. Verify Git history works: `git log checkpoints/active/<test>.md`

### Step 5: Clean up

1. Update ISSUE-006.md: mark scope items complete
2. Move ISSUE-006.md to `specs/issues/done/`

## Integration

### With Git

Git replaces delta artifact files for version history:

| Need | Git Command |
|------|-------------|
| See checkpoint history | `git log checkpoints/active/chk-feature.md` |
| See what changed | `git diff HEAD~1 checkpoints/active/chk-feature.md` |
| Restore previous version | `git show <commit>:checkpoints/active/chk-feature.md` |

### With Checkpoint Format

The checkpoint format gains:
- Optional `last_delta` frontmatter field
- Optional inline `## Delta: <timestamp>` sections

No changes to required structure.

## Example

User workflow:

```
User: [loads checkpoint] Here's my checkpoint for the auth feature.

[... works on auth feature ...]

User: delta

Claude: I'll update the checkpoint with what changed.

**Changes identified:**
- Decision: Use JWT over sessions
- Play-by-play: Implemented login endpoint
- Artifacts: Created auth.ts, modified routes.ts
- Current state: Login working, logout pending
- Next actions: Implement logout, add refresh tokens

[Outputs updated checkpoint with inline delta section]
```

## References

- [ISSUE-006](ISSUE-006.md): Issue driving this change
- [checkpoint-format.md](../../.claude/skills/coihuin-compress/checkpoint-format.md): Checkpoint structure
- [history/2025-12-16-dialectic-audit.md]: Original dialectic discussion
