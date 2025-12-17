# Implementation Plan: ISSUE-012

**Issue**: Clean up checkpoint-format.md and remove historical examples
**Spec**: spec-012
**Status**: Ready for implementation

---

## Summary

Remove accumulated noise from the coihuin-compress skill: stale references and inline example from checkpoint-format.md, historical design artifacts from docs/examples/, and document the removal in history.

---

## Phase 1: Clean checkpoint-format.md

**Goal**: Extract the Example section to a standalone file and remove References.

### Tasks

- [ ] **1.1** Move Example section to examples directory
  - Create `.claude/skills/coihuin-compress/examples/checkpoint-example.md`
  - Copy content from lines 128-190 (the example checkpoint)
  - Add brief header explaining this is a reference for first checkpoint creation

- [ ] **1.2** Remove Example section from checkpoint-format.md (lines 128-190)
  - Delete from `## Example` header through closing code fence
  - Example now lives in examples/checkpoint-example.md

- [ ] **1.3** Remove References section (lines 192-196)
  - Delete `## References` header and all bullet points
  - These external links are not actionable within the skill

- [ ] **1.4** Update SKILL.md to reference the example
  - Add reference to `examples/checkpoint-example.md` for first-time checkpoint creation

- [ ] **1.5** Verify file ends cleanly
  - Last content should be Checkpoint Triggers list item 5
  - No trailing blank sections or orphaned content

---

## Phase 2: Delete Historical Examples

**Goal**: Remove design-phase artifacts that are now noise.

### Tasks

- [ ] **2.1** Delete docs/examples/ folder
  - Remove all 6 files: chk-001.md through chk-005.md, chk-003-breadcrumbs.md
  - Command: `rm -rf docs/examples/`

- [ ] **2.2** Remove docs/ directory if empty
  - Command: `rmdir docs/ 2>/dev/null || true`
  - Only removes if empty; safe if other content exists

---

## Phase 3: Document Removal

**Goal**: Preserve historical context about what was removed and why.

### Tasks

- [ ] **3.1** Create or append to history file
  - File: `history/2025-12-17-cleanup-notes.md`
  - Document what was removed (examples folder, spec sections)
  - Document why (design-phase artifacts, non-actionable references)
  - Note that real checkpoints in checkpoints/active/ serve as living examples

---

## Phase 4: Validate and Finalize

**Goal**: Verify all changes and close out the issue.

### Tasks

- [ ] **4.1** Run validation checks
  - Grep for "## Example" in checkpoint-format.md → zero matches
  - Grep for "## References" in checkpoint-format.md → zero matches
  - Grep for "docs/examples" in skill files → zero matches
  - Grep for "Factory.ai" in skill files → zero matches
  - ls docs/examples/ → "No such file or directory"
  - Read history file → removal note present

- [ ] **4.2** Verify spec completeness
  - checkpoint-format.md still contains: Overview, Design Principles, Structure, Field Definitions, Information Priority, Checkpoint Triggers

- [ ] **4.3** Update ISSUE-012.md acceptance criteria
  - Check off all 5 acceptance criteria items

- [ ] **4.4** Update ISSUE-012.md scope items
  - Check off all 4 scope items

- [ ] **4.5** Validate issue using cspec
  - Run `cspec validate specs/issues/active/ISSUE-012.md`
  - Ensure no validation errors

- [ ] **4.6** Move issue to done/
  - Move ISSUE-012.md to `specs/issues/done/`
  - Move spec-012.md to `specs/issues/done/`

---

## Dependencies

- **Requires**: spec-012.md (complete)
- **Blocked by**: None

## Files to Modify

| File | Action |
|------|--------|
| `.claude/skills/coihuin-compress/checkpoint-format.md` | Modify - remove Example and References sections |
| `.claude/skills/coihuin-compress/examples/checkpoint-example.md` | Create - moved example for first checkpoint reference |
| `.claude/skills/coihuin-compress/SKILL.md` | Modify - add reference to examples/checkpoint-example.md |
| `docs/examples/chk-001.md` | Delete - historical artifact |
| `docs/examples/chk-002.md` | Delete - historical artifact |
| `docs/examples/chk-003.md` | Delete - historical artifact |
| `docs/examples/chk-003-breadcrumbs.md` | Delete - historical artifact |
| `docs/examples/chk-004.md` | Delete - historical artifact |
| `docs/examples/chk-005.md` | Delete - historical artifact |
| `history/2025-12-17-cleanup-notes.md` | Create - document removal decision |
| `specs/issues/active/ISSUE-012.md` | Modify - check acceptance criteria and scope |

## Validation Hooks

- [ ] No "## Example" in checkpoint-format.md
- [ ] No "## References" in checkpoint-format.md
- [ ] No "docs/examples" references in skill files
- [ ] No "Factory.ai" references in skill files
- [ ] docs/examples/ directory does not exist
- [ ] `.claude/skills/coihuin-compress/examples/checkpoint-example.md` exists
- [ ] SKILL.md references `examples/checkpoint-example.md`
- [ ] History file documents removal
- [ ] checkpoint-format.md has all required sections
- [ ] cspec validate passes for ISSUE-012.md
