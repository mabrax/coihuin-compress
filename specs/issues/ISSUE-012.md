---
id: ISSUE-012
title: "Clean up checkpoint-format.md—remove noise, relocate example"
nature: refactor
impact: invisible
version: patch
status: draft
created: 2025-12-16
updated: 2025-12-16

context:
  required: []
  recommended: []

depends_on: []
blocks: []
---

## Problem

The `checkpoint-format.md` spec contains noise that doesn't serve its purpose:

1. **Stale references**: Links to Factory.ai article, ReSum paper, and example files that aren't actively used
2. **Inline example**: A full example checkpoint bloats the spec; examples should live in `examples/` folder

The spec should be lean—focused on structure and rules, not tutorial content.

## Scope

### In Scope

- [ ] Remove References section from checkpoint-format.md
- [ ] Move inline example to examples/ folder (if not redundant with existing examples)
- [ ] Review delta-format.md for similar noise
- [ ] Ensure examples/ folder has adequate coverage
- [ ] Update any cross-references if needed

### Out of Scope

- Restructuring the format itself
- Adding new sections
- Changing validation rules

## Acceptance Criteria

- [ ] checkpoint-format.md has no References section
- [ ] Inline example removed or relocated
- [ ] delta-format.md reviewed and cleaned if needed
- [ ] examples/ folder contains representative examples
- [ ] Spec remains complete and usable without the removed content

## Notes

### Current Noise

**References section** (to remove):
```markdown
## References

- Factory.ai: "Compressing Context" - What Must Survive categories
- ReSum paper: Context Summarization for Long-Horizon Search Intelligence
- Example checkpoints: `docs/examples/chk-*.md`
```

These were useful during initial design but are now stale. The skill is self-contained.

**Inline example** (to relocate):
The full checkpoint example in the spec is ~50 lines. This belongs in `examples/checkpoint.md`, not inline.

### Audit Origin

Identified during Discussion 2 in dialectic audit.

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 2
