---
checkpoint: chk-stop-hook-auto-checkpoint
created: 2026-01-06T03:25:50Z
anchor: Stop hook implementation
status: current
---

## Problem
Users forget to checkpoint before ending sessions, losing context. Need automatic reminder/trigger when meaningful work was done.

## Session Intent
Implement a Stop hook that detects meaningful work (code changes) and prompts Claude to use the compress skill before ending.

## Essential Information

### Decisions
- **Command hook, not prompt hook**: Prompt-type hooks don't receive session context (only metadata). Must use command hook with script that reads transcript.
- **Transcript parsing**: Detect Write/Edit/NotebookEdit tool usage as "meaningful work"
- **Loop prevention**: Check `stop_hook_active` flag to prevent infinite blocking
- **Absolute paths**: Hook command must use absolute path to script (relative paths fail)

### Technical Context
- Claude Code hooks: `~/.claude/settings.json` (user) and `.claude/settings.json` (project)
- Both user and project hooks run in parallel (not override)
- Hooks captured at session start, require restart to reload
- Stop hook input: `{"session_id", "transcript_path", "stop_hook_active", ...}`

### Breadcrumbs
| Type | Reference | Hint |
|------|-----------|------|
| file | `.claude/hooks/stop-checkpoint.py` | Script that reads transcript, detects changes |
| file | `.claude/settings.json` | Project hooks config with Stop hook |
| file | `~/.claude/settings.json` | User-level hooks (has `coihuin-hook` for Stop) |
| docs | claude-code-guide research | Hooks don't auto-load transcript into prompt |

### Play-By-Play
- Research: Can Stop hooks trigger skills? → Yes, via blocking reason
- Attempt 1: Prompt-type hook → Failed (LLM has no session context)
- Attempt 2: Command hook with Python script → Works
- Debug: Hooks need session restart to reload
- Debug: Relative paths don't resolve, use absolute
- Success: Hook blocks, Claude uses compress skill
- Added "already checkpointed" detection to prevent re-trigger loops
- Bug fix: Project path contained "coihuin-compress", falsely matching checkpoint detection
- Fix: Require both `"Skill"` AND `"coihuin-compress"` in same line for actual invocation
- Bug fix: Checkpoint edits triggered re-block (Edit after Skill invocation)
- Fix: Exclude `checkpoints/` paths from "meaningful work" detection

### Artifact Trail
| File | Status | Key Change |
|------|--------|------------|
| `.claude/hooks/stop-checkpoint.py` | created | Reads transcript, detects Write/Edit, returns block/approve |
| `.claude/settings.json` | modified | Added Stop hook with command type |

### Current State
- Stop hook fully working with edge cases handled
- Excludes checkpoint file edits from "work" detection
- Matches actual Skill invocation (not path strings)
- Debug logging at `/tmp/stop-checkpoint-debug.log`

### Next Actions
- Disable debug logging for production
- Clean up test-final.md after successful test
- Consider: integrate with `coihuin-hook` binary (user-level)

## User Rules
- Never commit without user approval
- No time estimates in plans
