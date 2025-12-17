# Implementation Plan: ISSUE-011

**Issue**: Implement eval mechanism for checkpoint quality (dogfooding + LLM-as-judge)
**Spec**: spec-011
**Status**: Ready for implementation

---

## Summary

Implement the checkpoint quality evaluation system defined in spec-011. This creates a dialectic evaluation process (human interview + agent investigation) triggered via `/eval-checkpoint` command, with directory structure for checkpoint collection, scoring, and promotion.

---

## Phase 1: Directory Structure and Rubric

**Goal**: Create the eval/ directory hierarchy and canonical rubric document.

### Tasks

- [ ] **1.1** Create eval/ directory structure
  - Create `eval/inbox/` - checkpoints awaiting evaluation
  - Create `eval/scored/` - evaluated checkpoints with scores
  - Create `eval/promoted/` - high-scoring checkpoints ready for examples/
  - Add `.gitkeep` files to preserve empty directories

- [ ] **1.2** Create eval/rubric.md
  - Extract rubric content from spec-011 (Rubric Structure section)
  - Include dimensions table with weights
  - Include scoring scale (1-5)
  - Include per-dimension criteria tables
  - Include promotion criteria

---

## Phase 2: Create Slash Command

**Goal**: Implement the `/eval-checkpoint` slash command that orchestrates the 3-phase dialectic evaluation.

### Tasks

- [ ] **2.1** Create `.claude/commands/eval-checkpoint.md`
  - Use command file content from spec-011 "Slash Command" section
  - Include argument handling ($ARGUMENTS for checkpoint name)
  - Include error handling (file not found, malformed checkpoint, etc.)
  - Document the 3-phase process inline

- [ ] **2.2** Ensure .claude/commands/ directory exists
  - Create directory if missing
  - Verify Claude Code can discover the command

---

## Phase 3: Integration and Documentation

**Goal**: Update SKILL.md to reference the evaluation system and document the workflow.

### Tasks

- [ ] **3.1** Update SKILL.md with eval command reference
  - Add "Checkpoint Evaluation" section
  - Document `/eval-checkpoint <name>` usage
  - Explain the 3-phase dialectic process briefly
  - Reference eval/rubric.md for scoring criteria

- [ ] **3.2** Document the dogfooding workflow in SKILL.md or eval/
  - Collecting checkpoints from real projects
  - Copying to eval/inbox/
  - Running evaluation
  - Promotion process for high-scoring checkpoints

---

## Phase 4: Finalize and Validate

**Goal**: Mark acceptance criteria complete, validate the issue, and optionally test with a real checkpoint.

### Tasks

- [ ] **4.1** Update ISSUE-011.md acceptance criteria
  - Check off: Evaluation rubric documented
  - Check off: eval/ directory structure defined
  - Check off: Eval script/command functional
  - Check off: Workflow documented

- [ ] **4.2** Update scope items in ISSUE-011.md
  - Check off completed scope items

- [ ] **4.3** Validate issue using cspec
  - Run `cspec validate specs/issues/active/ISSUE-011.md`
  - Ensure no validation errors

- [ ] **4.4** (Optional) Test with real checkpoint
  - Copy chk-issue-backlog.md to eval/inbox/
  - Run `/eval-checkpoint chk-issue-backlog`
  - Verify end-to-end flow produces eval/scored/chk-issue-backlog.eval.md

- [ ] **4.5** Update issue status to reflect completion

---

## Dependencies

- **Requires**: spec-011.md (complete)
- **Blocked by**: None

## Files to Modify

| File | Action |
|------|--------|
| `eval/inbox/.gitkeep` | Create - preserve directory |
| `eval/scored/.gitkeep` | Create - preserve directory |
| `eval/promoted/.gitkeep` | Create - preserve directory |
| `eval/rubric.md` | Create - canonical rubric document |
| `.claude/commands/eval-checkpoint.md` | Create - slash command |
| `SKILL.md` | Modify - add eval section |
| `specs/issues/active/ISSUE-011.md` | Modify - check acceptance criteria |

## Validation Hooks

- [ ] eval/ directory structure exists with subdirectories
- [ ] eval/rubric.md contains all 5 dimensions with criteria
- [ ] `/eval-checkpoint` command is discoverable by Claude Code
- [ ] SKILL.md references checkpoint evaluation
- [ ] cspec validate passes for ISSUE-011.md
