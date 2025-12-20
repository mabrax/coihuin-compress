---
checkpoint: chk-unified-command
created: 2025-12-20T19:40:43Z
anchor: Phase 2 complete
last_delta: 2025-12-20T20:02:56Z
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
- **Unified command triggers**: "use compress skill", "compress", "compress skill" all invoke unified command
- **Context detection**: Checkpoint loaded = frontmatter visible in context; Significant work = 2+ files or decision made

### Technical Context

- **Project type**: Claude Code skill (markdown-based, no build step)
- **Skill location**: `.claude/skills/coihuin-compress/` (local) and `~/.claude/skills/coihuin-compress/` (global)
- **Validation**: `uv run format-check.py <file>` for checkpoint format validation
- **Sync check**: `./scripts/sync-check.sh` to compare local/global

### Breadcrumbs

| Type | Reference | Hint |
|------|-----------|------|
| file | `plan/unified-command-implementation.md` | Full 5-phase implementation plan with success criteria |
| file | `.claude/skills/coihuin-compress/SKILL.md` | Main skill definition (Phase 1 + Phase 2 changes) |
| file | `.claude/skills/coihuin-compress/index-format.md` | INDEX.md format specification (created in Phase 1) |
| file | `scripts/sync-check.sh` | Local/global sync utility (enhanced with --sync flag) |
| file | `CHANGELOG.md` | Documents planned features in [Unreleased] section |

### Play-By-Play

- Phase 1.1-1.5 → INDEX.md foundation → Spec, SKILL.md updates, directory structure
- Post-Phase 1 → Enhanced sync-check.sh → --sync flag, --help, handles missing global
- Phase 2.1-2.5 → Unified Command section → Trigger phrases, decision tree, context detection, backward compatibility

### Artifact Trail

| File | Status | Key Change |
|------|--------|------------|
| `.claude/skills/coihuin-compress/index-format.md` | created | INDEX.md format specification |
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Phase 1: INDEX steps; Phase 2: Unified Command section |
| `scripts/sync-check.sh` | modified | Added --sync flag, --help, initial sync for missing global dir |
| `CHANGELOG.md` | created | Documents planned features |
| `plan/unified-command-implementation.md` | created | Full implementation plan |

### Current State

**Phase 1: INDEX.md Foundation** - COMPLETE
**Phase 2: Unified Command Workflow** - COMPLETE
- Added Unified Command section to SKILL.md after Workflow
- Trigger phrases defined: "use compress skill", "compress", "compress skill"
- Decision tree covers: no checkpoint, checkpoint loaded + work, work complete, work diverging
- Context detection rules defined for all states
- Backward compatibility documented
- Local and global skill directories in sync

**Remaining phases**:
- Phase 3: Fork Detection (6 tasks)
- Phase 4: Proactive Archive Suggestion (5 tasks)
- Phase 5: format-check.py INDEX Validation (6 tasks)

### Next Actions

1. **Phase 3.1**: Add "Fork Detection" section to SKILL.md after Unified Command
2. **Phase 3.2**: Define strong fork signals (user says unrelated, needs impl plan, multi-issue)
3. **Phase 3.3**: Define weak fork signals (different files, scope creep)
4. **Phase 3.4**: Define what is NOT a fork (trivial fixes, config changes)
5. **Phase 3.5**: Write fork decision flow with user prompt options (A/B/C)
6. **Phase 3.6**: Add advisory principles (always ask, never auto-fork)

## User Rules

- Never commit without user approval
- Never include time estimates in plans
- Use `date` command for date-related tasks

---

## Delta: 2025-12-20T20:02:56Z

### What Changed

Completed Phase 2: Added Unified Command section to SKILL.md with trigger phrases, decision tree, context detection rules, and backward compatibility documentation.

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Added Unified Command section (70 lines) after Workflow |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| Phase 2: Unified Command Workflow | pending | complete |
