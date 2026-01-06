# Active Checkpoints

| Checkpoint | Description | Last Updated |
|------------|-------------|--------------|
| chk-stop-hook-auto-checkpoint | Stop hook for auto-checkpointing | 2026-01-06 |

---

## chk-stop-hook-auto-checkpoint

**Problem**: Users forget to checkpoint before ending sessions

**Scope**: Stop hook that detects meaningful work and triggers compress skill

**Status**: Working - hook blocks on Write/Edit detection
