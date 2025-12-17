# Implementation Plan: ISSUE-006

**Issue**: Simplify to delta-as-operation model
**Spec**: spec-006
**Status**: Ready for implementation

---

## Summary

Simplify coihuin-compress from three concepts (checkpoint, delta artifact, merge) to two operations (checkpoint, delta). Remove delta artifact files, eliminate the "merge" command, and redefine "delta" as the operation that updates an existing checkpoint with what changed.

---

## Phase 1: Delete Delta Artifact Files

**Goal**: Remove all delta-related specs and examples that are no longer needed.

### Tasks

- [ ] **1.1** Delete `.claude/skills/coihuin-compress/delta-format.md`
  - This is the spec for delta artifacts we're eliminating

- [ ] **1.2** Delete `specs/delta-format.md`
  - Duplicate delta spec

- [ ] **1.3** Check and delete `examples/delta.md` if it exists
  - Example of eliminated artifact

---

## Phase 2: Update SKILL.md

**Goal**: Replace the three-concept model with the two-operation model.

### Tasks

- [ ] **2.1** Update Workflow diagram
  - Remove "merge" reference
  - Change to: checkpoint (create) → delta (update)
  - New diagram:
    ```
    Session 1 (new work):
      → "checkpoint" → creates new checkpoint

    Session 2+ (continuing):
      → User loads checkpoint manually
      → work...
      → "delta" → updates checkpoint with what changed

    Done:
      → move checkpoint to archive/
    ```

- [ ] **2.2** Replace Delta operation section
  - Remove current: "Show incremental changes since loaded checkpoint (without merging)"
  - Add new definition per spec-006:
    - Trigger: "delta", "update checkpoint", "add delta"
    - Prerequisite: User has loaded existing checkpoint
    - How: Identify changes, update sections, optionally add inline delta, output updated checkpoint
    - Add Git history note

- [ ] **2.3** Delete Merge operation section entirely
  - Search for heading `### Merge` and delete until next heading (`### Archive`)

- [ ] **2.4** Update Reference Files table
  - Remove `delta-format.md` row
  - Remove `examples/delta.md` row

---

## Phase 3: Update Checkpoint Format (Optional)

**Goal**: Add optional `last_delta` frontmatter field to checkpoint-format.md.

### Tasks

- [ ] **3.1** Update checkpoint-format.md Header Fields table
  - Add row: `last_delta` | No | ISO-8601 timestamp of last delta operation

- [ ] **3.2** Update example checkpoint in checkpoint-format.md
  - Add `last_delta` field to frontmatter example (optional)

---

## Phase 4: Validate and Finalize

**Goal**: Verify implementation works and mark issue complete.

### Tasks

- [ ] **4.1** Test skill loading
  - Trigger the skill and verify no errors
  - Confirm "checkpoint" and "delta" triggers work

- [ ] **4.2** Functional test
  - Create a test checkpoint
  - Load it, simulate work (add a decision, update current state)
  - Run "delta" and verify checkpoint gets updated with changes

- [ ] **4.3** Update ISSUE-006.md scope items
  - Check off: Update SKILL.md
  - Check off: Archive or remove delta-format.md
  - Check off: Update checkpoint format if needed
  - Check off: Update any references to "merge" command

- [ ] **4.4** Update ISSUE-006.md acceptance criteria
  - Check off: SKILL.md describes only two operations
  - Check off: No references to delta artifact files
  - Check off: No references to "merge" as separate command
  - Check off: delta-format.md archived or removed
  - Check off: User can say "delta" and checkpoint gets updated

- [ ] **4.5** Move ISSUE-006.md to done
  - Move from `specs/issues/active/` to `specs/issues/done/`

---

## Dependencies

- **Requires**: spec-006.md (complete)
- **Blocked by**: None

## Files to Modify

| File | Action |
|------|--------|
| `.claude/skills/coihuin-compress/delta-format.md` | Delete |
| `specs/delta-format.md` | Delete |
| `examples/delta.md` | Delete (if exists) |
| `.claude/skills/coihuin-compress/SKILL.md` | Modify - new delta definition, remove merge |
| `.claude/skills/coihuin-compress/checkpoint-format.md` | Modify - add last_delta field (optional) |
| `specs/issues/active/ISSUE-006.md` | Modify - check scope and acceptance criteria |

## Validation Hooks

- [ ] No delta-format.md files exist in project
- [ ] SKILL.md has no "Merge" section
- [ ] SKILL.md Delta section describes "update checkpoint with what changed"
- [ ] Reference Files table has no delta entries
- [ ] Skill triggers correctly on "checkpoint" and "delta"
- [ ] Git tracks checkpoint updates (`git log checkpoints/active/<file>.md` shows history)
