---
id: ISSUE-006
title: "Simplify to delta-as-operation model"
nature: enhancement
impact: visible
version: minor
status: done
created: 2025-12-16
updated: 2025-12-17

context:
  required: []
  recommended: []

depends_on: []
blocks: []
---

## Problem

The current model has three concepts that confuse users:
1. **checkpoint** → create a snapshot
2. **delta** → create a delta *artifact file*
3. **merge** → combine delta into checkpoint

In practice, users always skip delta file creation and just want to update the checkpoint. The mental overhead of "delta files" and "merge" is unnecessary.

## Real-World Usage Feedback

After a half-week of using the skill, the actual pattern is:
- Create checkpoint at session start
- Work on tasks
- Say "add the delta to the checkpoint" (meaning: update it with what changed)
- Never create separate delta files

The word "delta" already carries semantic meaning (change/difference). Using it as a verb—"delta the checkpoint"—is intuitive.

## Proposed Model

**Simplified to two operations:**

| Command | Action |
|---------|--------|
| `checkpoint` | Create a fresh snapshot |
| `delta` | Update existing checkpoint with what changed |

No intermediate artifacts. No merge step. Git provides version history.

## Scope

### In Scope

- [x] Reframe issue to reflect delta-as-operation model
- [x] Update SKILL.md to reflect delta-as-operation model
- [x] Archive or remove delta-format.md and related specs
- [x] Update checkpoint format if needed (added last_delta field)
- [x] Update any references to "merge" command (removed)

### Out of Scope

- Changing checkpoint format structure
- Removing inline delta sections from checkpoints (those are useful)
- Git integration features

## Acceptance Criteria

- [x] SKILL.md describes only two operations (checkpoint, delta)
- [x] No references to delta artifact files remain
- [x] No references to "merge" as separate command
- [x] delta-format.md archived or removed
- [x] User can say "delta" and checkpoint gets updated

## Notes

### What Stays

- **Inline delta sections** in checkpoints (the `## Delta: <timestamp>` sections)
- **Intelligent update logic** (identify changes, avoid redundancy)
- **Git for history** (`git log`, `git diff` for progression)

### What Goes

- Delta as a separate artifact file
- The "merge" command/concept
- `delta-format.md` as an active spec

### Historical Context

Originally from dialectic audit tension #3. Initial reframing (2025-12-16) identified that delta = intelligent merging and Git provides history. This update (2025-12-17) goes further based on real usage: eliminate the delta artifact entirely, make "delta" the verb for updating checkpoints.

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 3
