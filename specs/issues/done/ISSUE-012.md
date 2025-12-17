---
id: ISSUE-012
title: "Clean up checkpoint-format.md and remove historical examples"
nature: refactor
impact: invisible
version: patch
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

The skill has accumulated noise from the initial design phase:

1. **Stale references in checkpoint-format.md**: Links to Factory.ai article, ReSum paper—not actionable within the skill
2. **Inline example in checkpoint-format.md**: ~60 lines of example bloats the spec
3. **Historical examples in docs/examples/**: The `chk-001.md` through `chk-005.md` files were iterative design artifacts from the initial proposal, not reference documentation. They're now noise.

The spec should be lean—focused on structure and rules. Historical artifacts should be removed or documented in history.

## Scope

### In Scope

- [x] Remove References section from checkpoint-format.md
- [x] Remove inline example from checkpoint-format.md (spec is self-explanatory)
- [x] Delete docs/examples/ folder (historical design artifacts)
- [x] Add brief note to history documenting the examples' origin and removal

### Out of Scope

- Restructuring the format itself
- Adding new sections
- Changing validation rules
- ~~Review delta-format.md~~ (deleted in ISSUE-006)

## Acceptance Criteria

- [x] checkpoint-format.md has no References section
- [x] checkpoint-format.md has no inline example section
- [x] docs/examples/ folder deleted
- [x] History documents the removal decision
- [x] Spec remains complete and usable without the removed content

## Notes

### Content to Remove

**References section** (checkpoint-format.md lines 192-196):
```markdown
## References

- Factory.ai: "Compressing Context" - What Must Survive categories
- ReSum paper: Context Summarization for Long-Horizon Search Intelligence
- Example checkpoints: `docs/examples/chk-*.md`
```

**Inline example** (checkpoint-format.md lines 128-190):
~60 lines of example checkpoint. The spec's Structure section (lines 18-68) already shows the format clearly.

**Historical examples** (docs/examples/):
- `chk-001.md` through `chk-005.md`: Iterative design checkpoints from initial proposal
- `chk-003-breadcrumbs.md`: Breadcrumbs feature development artifact

These were used to iterate on the skill design by creating deltas. They served their purpose during development but are now noise.

### Audit Origin

Identified during Discussion 2 in dialectic audit.

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 2
