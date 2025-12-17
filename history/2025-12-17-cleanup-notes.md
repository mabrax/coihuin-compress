# Cleanup Notes - 2025-12-17

## Summary

Removed accumulated noise from the coihuin-compress skill as identified during the dialectic audit (Discussion 2, 2025-12-16).

## What Was Removed

### From checkpoint-format.md

1. **Example section (lines 128-190)**
   - ~60 lines of inline example checkpoint
   - Moved to `examples/checkpoint-example.md` for reference
   - The Structure section already shows the format clearly

2. **References section (lines 192-196)**
   - External links to Factory.ai article and ReSum paper
   - Link to `docs/examples/chk-*.md`
   - Not actionable within the skill context

### Historical artifacts deleted

**Folder: `docs/examples/`** (entire directory removed)

| File | Description |
|------|-------------|
| `chk-001.md` | Initial design checkpoint |
| `chk-002.md` | Design iteration |
| `chk-003.md` | Design iteration |
| `chk-003-breadcrumbs.md` | Breadcrumbs feature development artifact |
| `chk-004.md` | Design iteration |
| `chk-005.md` | Final design checkpoint |

## Why Removed

1. **Stale references**: External links (Factory.ai, ReSum paper) are not actionable from within the skill. The principles have been internalized into the format specification.

2. **Inline example bloat**: The spec's Structure section provides sufficient format guidance. The example was moved to a dedicated file for those who want a complete reference.

3. **Historical design artifacts**: The `docs/examples/chk-*.md` files were iterative design checkpoints created during initial skill development. They served their purpose for:
   - Testing the delta operation workflow
   - Iterating on the format structure
   - Validating the checkpoint-to-checkpoint merge logic

   Now that the skill is stable, these are noise. Real checkpoints in `checkpoints/active/` serve as living examples.

## What Remains

- **Lean spec**: `checkpoint-format.md` now focuses purely on structure and rules
- **Reference examples**: `examples/checkpoint-example.md` and `examples/checkpoint.md` provide complete checkpoint references
- **Living examples**: Real checkpoints in `checkpoints/active/` demonstrate practical usage

## Audit Reference

This cleanup was identified during Discussion 2 of the dialectic audit.

See: `history/2025-12-16-dialectic-audit.md`, Appendix A, Discussion 2
