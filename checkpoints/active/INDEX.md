# Active Checkpoints

| Checkpoint | Description | Last Updated |
|------------|-------------|--------------|
| chk-checkpoint-branches-plan | Git-like branching for checkpoints with tree visualization | 2025-12-21 |

---

## chk-checkpoint-branches-plan

**Problem**: Add parent-child relationships between checkpoints and a CLI tool to visualize lineage as ASCII tree, enabling tracking of parallel development streams.

**Scope**: `.claude/skills/coihuin-compress/` (checkpoint-format.md, format-check.py, SKILL.md, new compress-tree.py), `~/.claude/plans/checkpoint-branches/`

**Status**: Phase 1 complete. Format spec updated with `parent` field (v1.2.0). Next: Phase 2 (validation).
