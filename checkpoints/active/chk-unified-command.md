---
checkpoint: chk-unified-command
created: 2025-12-20T19:40:43Z
anchor: Phase 4 complete
last_delta: 2025-12-20T20:30:16Z
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
- **Phase 4 revision**: Dialectic review revealed redundancy; revised to integrate with existing sections instead of creating new "Proactive Archive" section

### Technical Context

- **Project type**: Claude Code skill (markdown-based, no build step)
- **Skill location**: `.claude/skills/coihuin-compress/` (local) and `~/.claude/skills/coihuin-compress/` (global)
- **Validation**: `uv run format-check.py <file>` for checkpoint format validation
- **Sync check**: `./scripts/sync-check.sh` to compare local/global

### Breadcrumbs

| Type | Reference | Hint |
|------|-----------|------|
| file | `plan/unified-command-implementation.md` | Full 5-phase implementation plan with success criteria |
| file | `.claude/skills/coihuin-compress/SKILL.md` | Main skill definition (Phases 1-4 changes) |
| file | `.claude/skills/coihuin-compress/index-format.md` | INDEX.md format specification (created in Phase 1) |
| file | `scripts/sync-check.sh` | Local/global sync utility (enhanced with --sync flag) |
| file | `CHANGELOG.md` | Documents planned features in [Unreleased] section |

### Play-By-Play

- Phase 1.1-1.5 → INDEX.md foundation → Spec, SKILL.md updates, directory structure
- Post-Phase 1 → Enhanced sync-check.sh → --sync flag, --help, handles missing global
- Phase 2.1-2.5 → Unified Command section → Trigger phrases, decision tree, context detection, backward compatibility
- Phase 3.1-3.6 → Fork Detection section → Strong/weak signals, not-a-fork cases, decision flow, advisory principles
- Phase 4 (revised) → Proactive Archive → Dialectic review, integrated into existing sections (no new section)

### Artifact Trail

| File | Status | Key Change |
|------|--------|------------|
| `.claude/skills/coihuin-compress/index-format.md` | created | INDEX.md format specification |
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Phases 1-4: INDEX, Unified Command, Fork Detection, Proactive Archive |
| `scripts/sync-check.sh` | modified | Added --sync flag, --help, initial sync for missing global dir |
| `CHANGELOG.md` | created | Documents planned features |
| `plan/unified-command-implementation.md` | created | Full implementation plan |

### Current State

**Phase 1: INDEX.md Foundation** - COMPLETE
**Phase 2: Unified Command Workflow** - COMPLETE
**Phase 3: Fork Detection** - COMPLETE
**Phase 4: Proactive Archive Suggestion** - COMPLETE (revised approach)
- Dialectic review identified redundancy with existing "Proactive Advisory Triggers" section
- Revised: integrated into existing sections instead of creating new section
- Added "Work complete" trigger to When to Suggest table
- Added archive suggestion template to What to Suggest
- Enhanced "Work appears complete" with 5-item completion checklist
- Added outcome capture step to Archive operation (ask user before archiving)
- Local and global skill directories in sync

**Remaining phases**:
- Phase 5: format-check.py INDEX Validation (6 tasks)

### Next Actions

1. **Phase 5.1**: Add `is_index()` function to detect INDEX.md files
2. **Phase 5.2**: Add `validate_index()` function for INDEX-specific validation
3. **Phase 5.3**: Check for quick reference table with correct headers
4. **Phase 5.4**: Check for summary sections matching table entries
5. **Phase 5.5**: Update `main()` to detect file type and route to correct validator
6. **Phase 5.6**: Test validation with sample INDEX.md

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

---

## Delta: 2025-12-20T20:14:48Z

### What Changed

Completed Phase 3: Added Fork Detection section to SKILL.md with strong/weak signals, not-a-fork cases, decision flow with 3 options, and advisory principles.

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Added Fork Detection section (72 lines) after Unified Command |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| Phase 3: Fork Detection | pending | complete |

---

## Delta: 2025-12-20T20:30:16Z

### What Changed

Completed Phase 4 (revised): Used dialectic self-criticism to identify redundancy in original plan. Integrated proactive archive functionality into existing sections instead of creating new section.

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `.claude/skills/coihuin-compress/SKILL.md` | modified | +18 lines across 3 locations: triggers, checklist, outcome capture |

### Key Revision

Original plan called for new "Proactive Archive" section. Dialectic review revealed:
- Existing "Proactive Advisory Triggers" section already covered general suggestions
- Explicit triggers already defined in Archive operation
- Creating new section would cause fragmentation

Revised approach: enhance existing sections (DRY principle).

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| Phase 4: Proactive Archive Suggestion | pending | complete |
