# Implementation Plan: Enhanced Coihuin-Compress Skill

## Overview

Enhance the coihuin-compress skill with:
1. Re-incorporate INDEX.md integration (lost during sync)
2. Unified command "use compress skill" as intelligent entry point
3. Fork detection for diverging work streams
4. Proactive archive suggestions
5. INDEX.md validation in format-check.py

---

## Phase 1: INDEX.md Foundation

### Tasks

- [ ] **1.1** Create `index-format.md` specification file
- [ ] **1.2** Add INDEX step to Checkpoint operation in SKILL.md
- [ ] **1.3** Add INDEX step to Delta operation in SKILL.md
- [ ] **1.4** Add INDEX step to Archive operation in SKILL.md
- [ ] **1.5** Update Directory Structure section to show INDEX.md

### Checkpoints

- After 1.1: `index-format.md` exists with table structure and summary section format defined
- After 1.5: All three operations (checkpoint, delta, archive) have INDEX integration steps

### Success Criteria

- [ ] `index-format.md` defines: table columns (Checkpoint, Description, Last Updated), summary section format (Problem, Scope, Status)
- [ ] SKILL.md Checkpoint operation includes step to add entry to INDEX
- [ ] SKILL.md Delta operation includes step to update Last Updated date
- [ ] SKILL.md Archive operation includes step to remove entry from INDEX
- [ ] Directory Structure section shows `checkpoints/active/INDEX.md`

---

## Phase 2: Unified Command Workflow

### Tasks

- [ ] **2.1** Add "Unified Command" section to SKILL.md after Workflow section
- [ ] **2.2** Define trigger phrases ("use compress skill", "compress", etc.)
- [ ] **2.3** Write decision tree logic (no checkpoint → create, checkpoint loaded → delta, etc.)
- [ ] **2.4** Define context detection rules (what "checkpoint loaded" means, what "significant work" means)
- [ ] **2.5** Add backward compatibility note (explicit commands still work)

### Checkpoints

- After 2.3: Decision tree is complete with all branches defined
- After 2.5: Section is complete and integrated into SKILL.md

### Success Criteria

- [ ] Unified command section exists in SKILL.md
- [ ] Decision tree covers: no checkpoint, checkpoint loaded + work, work complete, work diverging
- [ ] Context detection clearly defines when checkpoint is "loaded" and when work is "significant"
- [ ] Backward compatibility is documented (checkpoint/delta/archive still work)

---

## Phase 3: Fork Detection

### Tasks

- [ ] **3.1** Add "Fork Detection" section to SKILL.md after Unified Command
- [ ] **3.2** Define strong fork signals (user says unrelated, needs impl plan, multi-issue)
- [ ] **3.3** Define weak fork signals (different files, scope creep)
- [ ] **3.4** Define what is NOT a fork (trivial fixes, config changes)
- [ ] **3.5** Write fork decision flow with user prompt options (A/B/C)
- [ ] **3.6** Add advisory principles (always ask, never auto-fork)

### Checkpoints

- After 3.4: All signal categories defined (strong, weak, not-a-fork)
- After 3.6: Section complete with decision flow and user interaction defined

### Success Criteria

- [ ] Strong signals are defined and any single one triggers fork suggestion
- [ ] Weak signals are defined and 2+ together trigger fork suggestion
- [ ] "Not a fork" cases are clearly listed
- [ ] User prompt shows 3 options: create separate, continue existing, abandon
- [ ] Advisory principles state: never auto-fork, always confirm, respect "no"

---

## Phase 4: Proactive Archive Suggestion

### Tasks

- [ ] **4.1** Add "Proactive Archive" section to SKILL.md after Fork Detection
- [ ] **4.2** Define explicit triggers (user says "archive this")
- [ ] **4.3** Define proactive triggers (all Next Actions complete, user says "done")
- [ ] **4.4** Write suggestion format (checklist of completion indicators)
- [ ] **4.5** Add outcome capture prompt (ask user what was achieved before archiving)

### Checkpoints

- After 4.3: Both trigger types (explicit, proactive) are defined
- After 4.5: Section complete with suggestion format and outcome capture

### Success Criteria

- [ ] Explicit triggers listed (archive this, archive checkpoint, we're done)
- [ ] Proactive triggers listed (Next Actions complete, user says done/finished)
- [ ] Suggestion format shows checklist (Next Actions done, no blockers, etc.)
- [ ] Outcome capture asks: what was achieved, any learnings to preserve

---

## Phase 5: format-check.py INDEX Validation

### Tasks

- [ ] **5.1** Add `is_index()` function to detect INDEX.md files
- [ ] **5.2** Add `validate_index()` function for INDEX-specific validation
- [ ] **5.3** Check for quick reference table with correct headers
- [ ] **5.4** Check for summary sections matching table entries
- [ ] **5.5** Update `main()` to detect file type and route to correct validator
- [ ] **5.6** Test validation with sample INDEX.md

### Checkpoints

- After 5.2: INDEX validation functions exist
- After 5.5: main() routes to correct validator based on file type
- After 5.6: Validation tested and working

### Success Criteria

- [ ] `is_index()` correctly identifies INDEX.md files
- [ ] `validate_index()` checks: table exists, headers correct (Checkpoint, Description, Last Updated)
- [ ] Cross-validation: table entries have matching summary sections
- [ ] `main()` auto-detects file type (checkpoint vs INDEX)
- [ ] Running `uv run format-check.py checkpoints/active/INDEX.md` produces valid output

---

## Files to Modify

| File | Action |
|------|--------|
| `.claude/skills/coihuin-compress/index-format.md` | Create |
| `.claude/skills/coihuin-compress/SKILL.md` | Modify |
| `.claude/skills/coihuin-compress/format-check.py` | Modify |

---

## Implementation Order

Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5

Each phase builds on the previous. Complete all tasks and verify success criteria before moving to next phase.
