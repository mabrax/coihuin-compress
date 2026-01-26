---
checkpoint: chk-v170-cli-commands
created: 2026-01-03T14:53:01Z
anchor: v1.7.0 release
status: archived
---

## Problem
CLI onboarding friction: users had to manually create directories, understand structure, and remember to read checkpoints at session start.

## Session Intent
Add three CLI commands to eliminate setup friction and enable automatic context recovery:
- `init` - one-command project setup
- `doctor` - health check with `--fix` to repair
- `prime` - output current checkpoint for hooks

## Essential Information

### Decisions
- **Project-level hooks only**: `.claude/settings.json` in project, not user-level
- **Merge existing hooks**: Don't overwrite, append to SessionStart array
- **Silent fail for prime**: Exit 0 with no output if no current checkpoint (hooks-friendly)
- **Doctor --fix pattern**: Like eslint --fix, diagnose first, fix only when asked

### Technical Context
- Python 3.10+, pytest for tests
- CLI uses argparse with subparsers
- Existing modules: tree, validate, scaffold, archive, status, current

### Breadcrumbs
| Type | Reference | Hint |
|------|-----------|------|
| file | `chkcc/init.py` | Directory structure + hook installation |
| file | `chkcc/doctor.py` | Health checks + --fix logic |
| file | `chkcc/cli.py:169-199` | cmd_prime, cmd_init, cmd_doctor handlers |
| file | `chkcc/tests/` | 20 unit tests |

### Play-By-Play
- Feature request → planned prime command
- Implemented prime with --header flag
- User requested init + doctor commands
- Planned with tests, implemented all
- Added --fix flag to doctor per user feedback
- Released as v1.7.0, merged to main

### Artifact Trail
| File | Status | Key Change |
|------|--------|------------|
| `chkcc/init.py` | created | create_directory_structure, create_index_files, install_hook |
| `chkcc/doctor.py` | created | check_directory, check_file, check_hook, cmd_doctor with fix |
| `chkcc/cli.py` | modified | Added 3 command handlers + subparsers |
| `chkcc/tests/test_prime.py` | created | 4 tests |
| `chkcc/tests/test_init.py` | created | 6 tests |
| `chkcc/tests/test_doctor.py` | created | 10 tests |
| `chkcc/pyproject.toml` | modified | Added pytest dev dependency |
| `CHANGELOG.md` | modified | v1.7.0 release notes |
| `README.md` | modified | Updated CLI usage table |

### Current State
- v1.7.0 released and merged to main
- All 20 tests passing
- main and develop branches in sync
- Commands working: `chkcc init`, `chkcc doctor`, `chkcc doctor --fix`, `chkcc prime`

### Next Actions
- Run `chkcc init` on this project to install the hook (currently missing per doctor)
- Consider: migrate to slash command or plugin architecture

## User Rules
- Never commit without user approval
- No time estimates in plans
