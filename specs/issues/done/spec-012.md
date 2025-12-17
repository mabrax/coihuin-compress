---
id: spec-012
title: Format Spec Cleanup and Historical Examples Removal
issue: ISSUE-012
version: 1.0.0
created: 2025-12-17
---

# Format Spec Cleanup and Historical Examples Removal

## Overview

This specification removes accumulated noise from the coihuin-compress skill:

1. **Stale references** in checkpoint-format.md (Factory.ai, ReSum paper)
2. **Inline example** that bloats the spec (~60 lines)
3. **Historical examples** in docs/examples/ that were design-phase artifacts

The goal is a lean spec focused on structure and rules, with historical context documented in history/ rather than cluttering active documentation.

## Design Principles

1. **Specs are reference, not tutorial**: Format specs define structure; examples belong elsewhere (or nowhere if redundant)
2. **Remove non-actionable references**: External links that can't be followed or acted upon are noise
3. **History preserves, active documents guide**: Historical artifacts belong in history/, not active directories
4. **Lean over comprehensive**: If the Structure section already shows the format, a full example is redundant

## Design Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| Keep References section? | No | Factory.ai and ReSum links are not actionable within the skill |
| Keep inline example? | No | Structure section (lines 18-68) already shows format clearly |
| Keep docs/examples/? | No | Historical design artifacts, not reference documentation |
| Document removal? | Yes | Brief note in history/ explains what was removed and why |
| Create new examples? | No | Real checkpoints in checkpoints/active/ serve as living examples |

## Content Analysis

### checkpoint-format.md Current State

| Section | Lines | Content | Action |
|---------|-------|---------|--------|
| Header + Overview | 1-8 | Title, version, overview | Keep |
| Design Principles | 10-16 | 4 principles | Keep |
| Structure | 17-68 | Format template with all sections | Keep |
| Field Definitions | 70-95 | Header and body field tables | Keep |
| Information Priority | 97-117 | Compression hierarchy | Keep |
| Checkpoint Triggers | 119-127 | When to create checkpoints | Keep |
| Example | 128-190 | Full 60-line example checkpoint | **Remove** |
| References | 192-196 | Factory.ai, ReSum, examples/ | **Remove** |

After cleanup: ~127 lines (down from ~196).

### docs/examples/ Contents

| File | Origin | Purpose | Action |
|------|--------|---------|--------|
| chk-001.md | Initial proposal | Design iteration #1 | **Delete** |
| chk-002.md | Initial proposal | Design iteration #2 | **Delete** |
| chk-003.md | Initial proposal | Design iteration #3 | **Delete** |
| chk-003-breadcrumbs.md | ISSUE-002 | Breadcrumbs development artifact | **Delete** |
| chk-004.md | Initial proposal | Design iteration #4 | **Delete** |
| chk-005.md | Initial proposal | Design iteration #5 | **Delete** |

These files were used to iterate on the skill design by creating deltas between versions. They served their purpose during initial development but are now noise.

## Implementation

### Step 1: Remove sections from checkpoint-format.md

Delete the Example section (lines 128-190) and References section (lines 192-196).

**Before** (end of file):
```markdown
## Checkpoint Triggers

Create a new checkpoint when:
...

## Example

```markdown
---
checkpoint: chk-003
...
```

## References

- Factory.ai: "Compressing Context" - What Must Survive categories
- ReSum paper: Context Summarization for Long-Horizon Search Intelligence
- Example checkpoints: `docs/examples/chk-*.md`
```

**After** (end of file):
```markdown
## Checkpoint Triggers

Create a new checkpoint when:

1. **Phase completion**: A distinct unit of work is done
2. **Major decision**: User makes a significant choice
3. **Context shift**: Work direction changes substantially
4. **Session break**: Before ending a session
5. **Pre-compression**: Before context window pressure
```

### Step 2: Delete docs/examples/ folder

```bash
rm -rf docs/examples/
```

If docs/ is now empty, remove it too:
```bash
rmdir docs/ 2>/dev/null || true
```

### Step 3: Document removal in history

Create or append to history note documenting what was removed:

**File**: `history/2025-12-17-cleanup-notes.md` (or append to existing daily history)

```markdown
## Historical Examples Removed (ISSUE-012)

The `docs/examples/` folder contained design-phase artifacts:
- `chk-001.md` through `chk-005.md`: Iterative checkpoints from initial proposal
- `chk-003-breadcrumbs.md`: Breadcrumbs feature development artifact

These were used during skill design to iterate by creating deltas between versions.
They served their purpose and are now removed as noise.

Real checkpoints in `checkpoints/active/` serve as living examples.

Also removed from checkpoint-format.md:
- References section (Factory.ai, ReSum paper links—not actionable)
- Inline example (~60 lines—redundant with Structure section)
```

### Step 4: Verify spec completeness

After removal, verify checkpoint-format.md still contains:
- [ ] Overview explaining what a checkpoint is
- [ ] Design Principles (4 items)
- [ ] Structure template showing all sections
- [ ] Field Definitions (header and body tables)
- [ ] Information Priority Hierarchy
- [ ] Checkpoint Triggers

The Structure section (lines 17-68) provides a complete template that serves as both documentation and example.

## Validation

| Check | Method | Expected |
|-------|--------|----------|
| Spec is complete | Read checkpoint-format.md | All required sections present |
| No Example section | Grep for "## Example" in checkpoint-format.md | Zero matches |
| No References section | Grep for "## References" in checkpoint-format.md | Zero matches |
| No broken references | Grep for "docs/examples" in skill files | Zero matches |
| No broken references | Grep for "Factory.ai" in skill files | Zero matches |
| docs/examples/ deleted | ls docs/examples/ | "No such file or directory" |
| History documented | Read history file | Removal note present |

## References

- [ISSUE-012](ISSUE-012.md): Issue driving this change
- [checkpoint-format.md](../../.claude/skills/coihuin-compress/checkpoint-format.md): Target file for cleanup
- [history/2025-12-16-dialectic-audit.md](../../history/2025-12-16-dialectic-audit.md): Discussion 2 where this was identified
