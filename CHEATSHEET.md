# Coihuin Compress Cheat Sheet

## Setup (once per machine)
```bash
git clone <repo> && cd coihuin-compress
uv tool install ./chkcc
```

## Setup (once per project)
```bash
chkcc init          # Creates everything: dirs, skill, hooks
chkcc doctor        # Verify setup
```

## Daily Workflow

```
┌─────────────────────────────────────────────────────────┐
│  START SESSION                                          │
│  → Context loads automatically (SessionStart hook)      │
└─────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│  WORK                                                   │
│  → Claude maintains checkpoint as you go                │
│  → Say "checkpoint" to create one if none exists        │
└─────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│  END SESSION                                            │
│  → Stop hook reminds to checkpoint if work was done     │
│  → Say "archive" when task complete                     │
└─────────────────────────────────────────────────────────┘
```

## Quick Commands

| Do this | Command |
|---------|---------|
| Start a checkpoint | "checkpoint" (to Claude) |
| See what's active | `chkcc status` |
| Switch focus | `chkcc current <name>` |
| Finish work | "archive" (to Claude) |
| Check health | `chkcc doctor` |
| Fix issues | `chkcc doctor --fix` |
| Update skill files | `chkcc update` |

## Checkpoint States

| State | Meaning |
|-------|---------|
| `current` | Working on RIGHT NOW |
| `active` | In progress, parked |
| `archived` | Done |

## When to Checkpoint

**Yes:**
- Multi-session work
- Many decisions to remember
- Complex state / branches
- Might context-switch away

**No (use `/compact`):**
- Single session
- Linear progress
- Simple task

## File Locations

```
checkpoints/
├── active/           # Current work
├── archive/          # Completed
└── LEARNINGS.md      # Extracted insights

.claude/
├── settings.json     # Hooks config
└── skills/coihuin-compress/  # Skill files
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "skill not found" | `chkcc init` |
| Skill outdated | `chkcc update` |
| Hook not working | Restart session |
| Something broken | `chkcc doctor --fix` |
