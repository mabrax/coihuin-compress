# Active Checkpoints

| Checkpoint | Description | Last Updated |
|------------|-------------|--------------|
| chk-stop-hook-auto-checkpoint | Stop hook for auto-checkpointing | 2026-01-06 |
| chk-v170-cli-commands | init, doctor, prime commands + v1.7.0 release | 2026-01-03 |

---

## chk-stop-hook-auto-checkpoint

**Problem**: Users forget to checkpoint before ending sessions

**Scope**: Stop hook that detects meaningful work and triggers compress skill

**Status**: Working - hook blocks on Write/Edit detection

---

## chk-v170-cli-commands

**Problem**: CLI onboarding friction - manual setup, no auto context recovery

**Scope**: Add init, doctor (with --fix), prime commands

**Status**: Complete - v1.7.0 released and merged to main
