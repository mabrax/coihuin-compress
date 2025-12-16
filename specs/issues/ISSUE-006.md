---
id: ISSUE-006
title: "Clarify delta purpose—documentation not reconstruction"
nature: enhancement
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

The delta format specification implies deltas enable state reconstruction:

> "Deltas capture incremental changes between two checkpoints... enabling efficient state reconstruction"

But the delta model's assumptions don't hold:

1. **Clean boundaries assumed**: Checkpoints are fuzzy—work doesn't have clean boundaries
2. **Deterministic diffing assumed**: "What changed" requires interpretation, not computation
3. **Mechanical merge assumed**: "Replace Current State entirely" isn't a delta merge—it's a full rewrite

**Reality**: If you lost chk-002, you can't apply delta-001-002 to chk-001 and get chk-002. You'd get an approximation at best.

Deltas serve **documentation** (audit trail, change history) not **computation** (state reconstruction). They're git commit messages, not git diffs.

## Scope

### In Scope

- [ ] Revise delta-format.md to accurately describe purpose
- [ ] Remove or qualify "state reconstruction" claims
- [ ] Clarify deltas are audit trails / change documentation
- [ ] Update SKILL.md delta description
- [ ] Consider renaming "Merge Instructions" to "Change Summary" or removing
- [ ] Add honest "Limitations" section to delta spec

### Out of Scope

- Redesigning deltas to actually enable reconstruction
- Removing delta functionality
- Adding computational diff capabilities

## Acceptance Criteria

- [ ] Delta purpose clearly stated as documentation/audit, not reconstruction
- [ ] No misleading claims about mechanical applicability
- [ ] "Merge Instructions" section renamed or purpose clarified
- [ ] Users understand deltas are narrative, not algorithmic
- [ ] Spec includes honest limitations section

## Notes

### Proposed Delta Reframing

**Current**: "Deltas capture incremental changes... enabling efficient state reconstruction"

**Proposed**: "Deltas document what changed between checkpoints, providing an audit trail for understanding how work evolved. They are narrative summaries, not computational diffs—they help humans understand progression but don't mechanically reconstruct state."

### On "Merge Instructions"

The current "Merge Instructions" section reads like executable steps but can't actually be executed mechanically. Options:

1. **Remove**: Section adds false precision
2. **Rename to "Change Summary"**: Descriptive, not prescriptive
3. **Keep but caveat**: "These are guidelines, not algorithmic instructions"

### Audit Origin

Dialectic audit tension #3: Delta's Theoretical Promise vs Practical Complexity

### Severity

Medium—misleading but deltas still useful for audit trails

---

## Reframing (2025-12-16)

**Discussion outcome**: The audit misunderstood delta's purpose. Delta isn't about "reconstruction"—it's about **intelligent merging**.

### What Delta Actually Does

When you say "merge," you're telling the system: "Figure out what changed and add only the valuable new stuff to the checkpoint. Don't repeat, don't bloat."

```
Session 1: Create checkpoint (fresh state)
    ↓
Session 2: Load checkpoint → work → "merge"
    ↓
System: Identifies what changed → adds only new valuable info
    ↓
Checkpoint grows without redundancy
```

### Git Already Provides Delta Artifacts

| Need | Git Solution |
|------|--------------|
| Version history | `git log checkpoints/active/chk-feature.md` |
| Diffs between versions | `git diff HEAD~1 checkpoints/active/chk-feature.md` |
| Full state at any point | `git show <commit>:path/to/checkpoint.md` |

**The delta as a separate artifact file is redundant with Git.**

### Revised Scope

| Component | Action |
|-----------|--------|
| Delta **command** ("merge") | Keep—valuable for intelligent updates |
| Delta **logic** | Keep—avoids redundancy in checkpoints |
| Delta **artifact files** | Make optional—Git provides this |
| Delta **format spec** | Simplify—only for edge cases outside Git |

### New Actions

1. ~~Clarify delta purpose~~ → Delta purpose is intelligent merging, not reconstruction
2. Make delta file generation optional in SKILL.md
3. Add guidance for using Git to track checkpoint progression
4. Simplify delta-format.md (optional artifact, not required workflow)

**Insight**: Don't duplicate what Git already does. Focus on intelligent state management, not artifact generation.

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 3
