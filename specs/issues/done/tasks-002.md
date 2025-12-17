# Implementation Plan: ISSUE-002

**Issue**: Add breadcrumbs system for context reconstruction
**Spec**: spec-002
**Status**: Ready for implementation

---

## Summary

The breadcrumbs format specification (spec-002) is complete. Remaining work integrates breadcrumbs into the checkpoint format spec and creates an example checkpoint demonstrating the feature.

---

## Phase 1: Integrate Breadcrumbs into checkpoint-format.md

**Goal**: Update the checkpoint format specification to include breadcrumbs as an official section.

### Tasks

- [x] **1.1** Add `Breadcrumbs` row to the Body Sections table in checkpoint-format.md
  - Required: No (optional section)
  - Purpose: Minimal references for context reconstruction
  - Compression Behavior: Prune stale entries opportunistically during merge

- [x] **1.2** Update the Structure template to include the Breadcrumbs section
  - Add `### Breadcrumbs` section under `## Essential Information`
  - Add table placeholder with Type, Reference, Hint columns

- [x] **1.3** Add Breadcrumbs to the Information Priority Hierarchy
  - Category: "Should Keep" (compress if needed)
  - Rationale: Breadcrumbs are cheap but not critical; stale ones can be cleaned

- [x] **1.4** Update the example checkpoint in checkpoint-format.md
  - Add a `### Breadcrumbs` section with 2-3 sample entries
  - Include file, decision, and external breadcrumb types

---

## Phase 2: Create Example Checkpoint with Breadcrumbs

**Goal**: Create a new example checkpoint file that demonstrates breadcrumbs usage.

### Tasks

- [x] **2.1** Create `docs/examples/chk-003-breadcrumbs.md`
  - Use the same Chromatic Quest scenario for continuity
  - Position checkpoint at end of Phase 2 (Gemini integration)

- [x] **2.2** Include comprehensive breadcrumbs section
  - At least one of each category: file, function, decision, external
  - Hints should be actionable (tell agent what the reference provides)

- [x] **2.3** Ensure checkpoint follows full format specification
  - All required sections present
  - Demonstrates how breadcrumbs fit naturally into checkpoint flow

---

## Phase 3: Finalize and Validate

**Goal**: Mark acceptance criteria complete and validate the issue.

### Tasks

- [x] **3.1** Update ISSUE-002.md acceptance criteria
  - Check off: "Integration with checkpoint-format.md complete"
  - Check off: "Example checkpoint with breadcrumbs section created"

- [x] **3.2** Update scope items in ISSUE-002.md
  - Check off: "Add breadcrumbs section to checkpoint format spec"

- [x] **3.3** Validate issue using cspec
  - Run `cspec validate specs/issues/active/ISSUE-002.md`
  - Ensure no validation errors

- [x] **3.4** Update issue status to `in-progress` (implementation started)

---

## Dependencies

- **Requires**: spec-002 complete (done)
- **Requires**: ISSUE-001 complete (assumed done per depends_on)

## Files to Modify

| File | Action |
|------|--------|
| `specs/checkpoint-format.md` | Modify - add breadcrumbs integration |
| `docs/examples/chk-003-breadcrumbs.md` | Create - new example |
| `specs/issues/active/ISSUE-002.md` | Modify - update acceptance criteria |

## Validation Hooks

- [ ] checkpoint-format.md includes Breadcrumbs in structure
- [ ] checkpoint-format.md includes Breadcrumbs in Body Sections table
- [ ] checkpoint-format.md includes Breadcrumbs in priority hierarchy
- [ ] Example checkpoint renders as valid markdown
- [ ] Example checkpoint has all required sections
- [ ] cspec validate passes for ISSUE-002.md
