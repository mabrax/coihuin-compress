# Implementation Plan: ISSUE-007

**Issue**: Enhance validation with semantic heuristics—structure isn't enough
**Spec**: spec-007
**Status**: Ready for implementation

---

## Summary

Implement the two-layer validation model: rename `validate.py` to `format-check.py`, add advisory heuristics (including recency checks), update output format to distinguish structural validation from advisory warnings, and embed semantic self-check guidance in SKILL.md.

---

## Phase 1: Rename Script and Update References

**Goal**: Rename validate.py to format-check.py and update all references.

### Tasks

- [ ] **1.1** Rename the script
  - Rename `.claude/skills/coihuin-compress/validate.py` → `.claude/skills/coihuin-compress/format-check.py`
  - Update shebang and docstring to reflect new name

- [ ] **1.2** Update SKILL.md references
  - Search for "validate.py" in `.claude/skills/coihuin-compress/SKILL.md`
  - Replace with "format-check.py"

- [ ] **1.3** Update AGENTS.md references (conditional)
  - Search for "validate.py" in `AGENTS.md`
  - If found: Replace with "format-check.py"
  - If not found: Skip this task (no action needed)

- [ ] **1.4** Verify no broken references
  - Grep for "validate.py" across the project
  - Ensure zero matches in active documentation

---

## Phase 2: Remove Stale Delta Validation

**Goal**: Remove delta validation code since ISSUE-006 eliminated delta artifacts.

### Tasks

- [ ] **2.1** Remove delta-related constants
  - Delete `DELTA_REQUIRED_SECTIONS`
  - Delete `DELTA_FRONTMATTER_REQUIRED`

- [ ] **2.2** Remove `validate_delta()` function
  - Delete the entire function (lines 146-185 in current file)

- [ ] **2.3** Update `detect_type()` function
  - Remove delta detection logic
  - Simplify to checkpoint detection only (or remove if unnecessary)

- [ ] **2.4** Update `main()` function
  - Remove delta validation branch
  - Simplify CLI to checkpoint-only validation

- [ ] **2.5** Update script docstring
  - Remove delta usage examples
  - Update to reflect checkpoint-only validation

---

## Phase 3: Add Advisory Heuristics

**Goal**: Add content and recency heuristics as advisory warnings.

### Tasks

- [ ] **3.1** Add datetime import
  - Add `from datetime import datetime, timedelta` to imports

- [ ] **3.2** Create `check_advisory_heuristics()` function
  - Implement per spec-007 Step 2:
    - Problem length check (< 20 words)
    - Decisions count check (< 2 entries)
    - Play-By-Play check (< 2 entries)
    - Artifact Trail check (empty)
    - Next Actions check (empty)
    - Current State check (< 30 words)
    - Checkpoint age check (created > 7 days)
    - Last delta recency check (last_delta > 3 days)

- [ ] **3.3** Integrate heuristics into `validate_checkpoint()`
  - Call `check_advisory_heuristics()` after structural validation
  - Add heuristic warnings to the result

- [ ] **3.4** Add content parsing helpers
  - Extract Problem section content for word count
  - Extract Decisions entries for count
  - Extract Play-By-Play entries for count
  - Extract Current State content for word count
  - Extract Artifact Trail for empty check
  - Extract Next Actions for empty check

  **Parsing approach** (extend existing `extract_sections()` pattern):
  ```python
  # Problem length: Find "## Problem" → extract until next "##" → count words
  problem_text = extract_section_content(body, "Problem")
  word_count = len(problem_text.split())  # Trigger if < 20

  # Decisions count: Find "### Decisions" → count list items (lines starting with "- " or "1.")
  decisions_text = extract_subsection_content(body, "Essential Information", "Decisions")
  entry_count = len([l for l in decisions_text.split('\n') if l.strip().startswith(('-', '1.', '2.'))])

  # Same pattern for Play-By-Play, Artifact Trail, Next Actions, Current State
  ```

  **Date format** (ISO 8601 with Z timezone):
  ```yaml
  created: 2025-12-17T10:30:00Z
  last_delta: 2025-12-15T14:22:00Z  # Optional field
  ```
  If `last_delta` is missing from frontmatter, skip that recency check (no warning).

---

## Phase 4: Update Output Format

**Goal**: Separate structural validation from advisory heuristics in output.

### Tasks

- [ ] **4.1** Update output structure in `main()`
  - Section 1: "STRUCTURAL VALIDATION: ✓ Pass" or "✗ Fail"
  - Section 2: "ADVISORY HEURISTICS: ⚠ N warnings" (if any)
  - Footer: Disclaimer about format vs quality

- [ ] **4.2** Update success message format
  - Change from "✓ Valid checkpoint" to structured output per spec-007

- [ ] **4.3** Add disclaimer footer
  - "Note: This tool checks format, not content quality."
  - "A valid checkpoint may still be insufficient for work resumption."

- [ ] **4.4** Verify exit codes
  - Exit 0 on structural pass (even with heuristic warnings)
  - Exit 1 only on structural errors

---

## Phase 5: Add Semantic Self-Check Guidance to SKILL.md

**Goal**: Embed Layer 2 semantic validation guidance for LLM use during checkpoint creation.

### Tasks

- [ ] **5.1** Add "Semantic Quality Self-Check" section to SKILL.md
  - Add after checkpoint creation guidance
  - Include 5-question self-check per spec-007 Step 4:
    1. Problem Clarity
    2. Decision Rationale
    3. State Specificity
    4. Action Actionability
    5. Fresh Agent Test

- [ ] **5.2** Add note distinguishing guidance from automated validation
  - "This is guidance for checkpoint authors, not automated validation."
  - Reference eval/rubric.md for external evaluation

---

## Phase 6: Validate and Finalize

**Goal**: Verify all changes and close out the issue.

### Tasks

- [ ] **6.1** Test format-check.py on existing checkpoints
  - Run on `checkpoints/active/chk-issue-backlog.md`
  - Verify structural validation passes
  - Verify advisory heuristics generate expected warnings

- [ ] **6.2** Test format-check.py on minimal/weak checkpoint
  - Create temporary test file with minimal content (e.g., `/tmp/test-checkpoint.md`)
  - Verify heuristic warnings fire correctly
  - Verify exit code is 0 (structural pass with warnings)
  - Delete temporary test file after verification

- [ ] **6.3** Run validation hooks
  - Grep for "validate.py" → zero matches
  - Grep for "SEMANTIC HEURISTICS" in format-check.py → zero matches (should be ADVISORY)
  - Verify SKILL.md has "Semantic Quality Self-Check" section

- [ ] **6.4** Update ISSUE-007.md acceptance criteria
  - Check off all 5 acceptance criteria items

- [ ] **6.5** Update ISSUE-007.md scope items
  - Check off all 6 in-scope items

- [ ] **6.6** Validate issue using cspec
  - Run `cspec validate specs/issues/active/ISSUE-007.md`
  - Ensure no validation errors

- [ ] **6.7** Move issue to done/
  - Move ISSUE-007.md to `specs/issues/done/`
  - Move spec-007.md to `specs/issues/done/`
  - Move TASKS-007.md to `specs/issues/done/`

---

## Dependencies

- **Requires**: spec-007.md (complete)
- **Blocked by**: None
- **Note**: ISSUE-006 must be complete (delta artifacts removed) - already done

## Files to Modify

| File | Action |
|------|--------|
| `.claude/skills/coihuin-compress/validate.py` | Rename → format-check.py |
| `.claude/skills/coihuin-compress/format-check.py` | Modify - remove delta validation, add heuristics, update output |
| `.claude/skills/coihuin-compress/SKILL.md` | Modify - add Semantic Quality Self-Check section, update script reference |
| `AGENTS.md` | Modify - update script reference if present |
| `specs/issues/active/ISSUE-007.md` | Modify - check acceptance criteria and scope |

## Validation Hooks

- [ ] `validate.py` does not exist
- [ ] `format-check.py` exists and is executable
- [ ] No "validate.py" references in active documentation
- [ ] format-check.py output shows "STRUCTURAL VALIDATION" section
- [ ] format-check.py output shows "ADVISORY HEURISTICS" section (when warnings exist)
- [ ] format-check.py output includes disclaimer footer
- [ ] format-check.py exits 0 on structural pass with heuristic warnings
- [ ] SKILL.md contains "Semantic Quality Self-Check" section
- [ ] No delta validation code remains in format-check.py
- [ ] Recency heuristics (checkpoint age, last_delta) are implemented
- [ ] cspec validate passes for ISSUE-007.md
