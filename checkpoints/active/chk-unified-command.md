---
checkpoint: chk-unified-command
created: 2025-12-20T19:40:43Z
anchor: Phase 1 complete
---

## Problem

Enhance the coihuin-compress skill with four capabilities that reduce user cognitive overhead:

1. **INDEX.md integration** - Quick inventory of active checkpoints (lost during global/local sync)
2. **Unified command** - Single "use compress skill" entry point that intelligently chooses operation
3. **Fork detection** - Identify when work diverges into parallel streams requiring separate checkpoints
4. **Proactive archive** - Suggest archiving when work appears complete

## Session Intent

Implement the 5-phase enhancement plan documented in `plan/unified-command-implementation.md`. Each phase builds on the previous. Complete all tasks and verify success criteria before moving to the next phase.

## Essential Information

### Decisions

- **INDEX location**: `checkpoints/active/INDEX.md` - colocated with active checkpoints
- **INDEX structure**: Quick reference table (Checkpoint, Description, Last Updated) + summary sections per checkpoint (Problem, Scope, Status)
- **Sync script enhancement**: Added `--sync` flag to actually perform sync, not just check

### Technical Context

- **Project type**: Claude Code skill (markdown-based, no build step)
- **Skill location**: `.claude/skills/coihuin-compress/` (local) and `~/.claude/skills/coihuin-compress/` (global)
- **Validation**: `uv run format-check.py <file>` for checkpoint format validation
- **Sync check**: `./scripts/sync-check.sh` to compare local/global

### Breadcrumbs

| Type | Reference | Hint |
|------|-----------|------|
| file | `plan/unified-command-implementation.md` | Full 5-phase implementation plan with success criteria |
| file | `.claude/skills/coihuin-compress/SKILL.md` | Main skill definition (modified in Phase 1) |
| file | `.claude/skills/coihuin-compress/index-format.md` | INDEX.md format specification (created in Phase 1) |
| file | `scripts/sync-check.sh` | Local/global sync utility (enhanced with --sync flag) |
| file | `CHANGELOG.md` | Documents planned features in [Unreleased] section |

### Play-By-Play

- Phase 1.1 → Created `index-format.md` specification → Defines table + summary section format
- Phase 1.2 → Added INDEX step to Checkpoint operation → Step 6 in SKILL.md
- Phase 1.3 → Added INDEX step to Delta operation → Step 5 in SKILL.md
- Phase 1.4 → Added INDEX step to Archive operation → Step 3 in SKILL.md
- Phase 1.5 → Updated Directory Structure → Added INDEX.md to tree + Reference Files table
- Post-Phase 1 → Enhanced sync-check.sh → Added --sync flag, --help, handles missing global dir
- Post-Phase 1 → Synced local to global → All 6 files now in sync

### Artifact Trail

| File | Status | Key Change |
|------|--------|------------|
| `.claude/skills/coihuin-compress/index-format.md` | created | INDEX.md format specification |
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Added INDEX steps to all 3 operations, updated Directory Structure and Reference Files |
| `scripts/sync-check.sh` | modified | Added --sync flag, --help, initial sync for missing global dir |
| `CHANGELOG.md` | created | Documents planned features |
| `plan/unified-command-implementation.md` | created | Full implementation plan |

### Current State

**Phase 1: INDEX.md Foundation** - COMPLETE
- All 5 tasks done (1.1-1.5)
- All success criteria met
- Local and global skill directories in sync

**Remaining phases**:
- Phase 2: Unified Command Workflow (5 tasks)
- Phase 3: Fork Detection (6 tasks)
- Phase 4: Proactive Archive Suggestion (5 tasks)
- Phase 5: format-check.py INDEX Validation (6 tasks)

### Next Actions

1. **Phase 2.1**: Add "Unified Command" section to SKILL.md after Workflow section
2. **Phase 2.2**: Define trigger phrases ("use compress skill", "compress", etc.)
3. **Phase 2.3**: Write decision tree logic (no checkpoint → create, checkpoint loaded → delta, etc.)
4. **Phase 2.4**: Define context detection rules (what "checkpoint loaded" means, what "significant work" means)
5. **Phase 2.5**: Add backward compatibility note (explicit commands still work)

## User Rules

- Never commit without user approval
- Never include time estimates in plans
- Use `date` command for date-related tasks
