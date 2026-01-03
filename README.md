# Coihuin Compress

Proactive context compression for long coding sessions.

> **Two ways to use it:** As a Claude Code skill (conversational) or via CLI (direct commands).

## The Problem

Long coding sessions lose critical context when automatic summarization occurs. Decisions get forgotten, file locations disappear, progress evaporates. You re-explain the same things multiple times.

## The Solution

**Continuous maintenance**, not reactive documentation.

Create **checkpoints** at meaningful moments. **Maintain them as you work** — decisions, artifacts, state updates happen immediately, not in batches. Archive when done, with learnings extracted automatically.

## You Drive It

**You** know when you've achieved something important. You're the one who decides when to checkpoint or delta.

Think of it like saving a game — you don't wait for the game to tell you. You save when you've made progress you don't want to lose.

## Scope

One checkpoint = one focused task. A feature, a phase, a research question. Not an entire project—just the thing you're working on right now.

## When to Use (and When Not To)

Checkpoints have overhead. Sometimes you just want Claude to keep working, not stop to document.

**Checkpoints shine when:**
- Work spans multiple sessions
- Many decisions accumulate that you'd hate to re-explain
- You might context-switch away and come back cold
- The task has branches, dead ends, or complex state

**`/compact` is enough when:**
- Single session, linear progress
- Clear next steps that don't need preservation
- Simple tasks where context loss isn't painful

This isn't a failure mode—it's the right tool for the right job.

## Workflow

```
1. Start work              → "checkpoint"           → Claude creates file
2. Work continues          → continuous updates     → checkpoint stays current
3. New session             → read the file          → Claude has full context
4. Done                    → "archive"              → learnings extracted
```

The checkpoint IS the context. Claude maintains it as you work, not as a separate documentation step.

## Checkpoint States

| State | Meaning |
|-------|---------|
| **current** | The ONE checkpoint you're working on right now |
| **active** | In-progress but not immediate focus (parked) |
| **archived** | Completed work (in `archive/` directory) |

Use `chkcc status` to see all active checkpoints with their problem context and next actions.

## What Gets Preserved

Based on [Factory.ai's research](https://factory.ai/news/compressing-context):

- **Problem** — What you're solving
- **Decisions** — Locked-in choices (never re-ask these)
- **Play-By-Play** — High-level action history
- **Artifact Trail** — Files created/modified/deleted
- **Current State** — What exists now
- **Next Actions** — What comes next
- **Breadcrumbs** — Lightweight references for navigation

## Installation

### Skill (Claude Code)

```bash
cp -r .claude/skills/coihuin-compress /path/to/your/project/.claude/skills/
```

Claude Code discovers and uses the skill automatically.

### CLI

```bash
uv tool install ./chkcc
```

Then initialize in your project:

```bash
chkcc init
```

This creates the checkpoint directories and installs a `SessionStart` hook that automatically loads context at session start.

## Usage

### Via Skill (conversational)

Talk to Claude Code naturally:

| Action | Say |
|--------|-----|
| Create checkpoint | "checkpoint" or "create checkpoint" |
| Finish & archive | "archive" |

Updates happen automatically as you work — Claude maintains the checkpoint continuously. The skill handles format, naming, and file location.

### Via CLI (direct commands)

| Action | Command |
|--------|---------|
| **Setup** | |
| Initialize project | `chkcc init` |
| Check setup health | `chkcc doctor` |
| **Context** | |
| Output current checkpoint | `chkcc prime` |
| Output with header | `chkcc prime --header` |
| **Navigation** | |
| View checkpoint tree | `chkcc tree` |
| View only active | `chkcc tree -s active` |
| View only archived | `chkcc tree -s archive` |
| Show status summaries | `chkcc status` |
| Set current checkpoint | `chkcc current <checkpoint>` |
| Show current checkpoint | `chkcc current` |
| Clear current | `chkcc current --clear` |
| **Checkpoint management** | |
| Validate format | `chkcc validate <file>` |
| Create checkpoint | `chkcc scaffold checkpoint <name>` |
| Create as current | `chkcc scaffold checkpoint <name> --current` |
| Add delta | `chkcc scaffold delta <file>` |
| Archive checkpoint | `chkcc archive <file>` |

## Project Structure

```
.claude/skills/coihuin-compress/
├── SKILL.md               # Skill instructions
├── checkpoint-format.md   # Checkpoint specification
└── index-format.md        # INDEX format specification

chkcc/                     # CLI package (flat layout)
├── pyproject.toml         # Package config
├── cli.py                 # Entry point
├── tree.py                # Tree visualization
├── validate.py            # Format validation
├── scaffold.py            # Checkpoint/delta creation
├── archive.py             # Archive functionality
├── status.py              # Status summaries
├── current.py             # Current checkpoint management
├── init.py                # Project initialization
├── doctor.py              # Setup health check
└── tests/                 # Unit tests
    ├── test_prime.py
    ├── test_init.py
    └── test_doctor.py

checkpoints/
├── active/                # Work in progress
├── archive/               # Completed
└── LEARNINGS.md           # Accumulated insights from archives
```

## Background

Two sources shaped the design:
1. **[ReSum](https://arxiv.org/pdf/2509.13313)** (Alibaba NLP) — Context summarization research
2. **[Factory.ai](https://factory.ai/news/compressing-context)** — "What Must Survive" categories

The name comes from the [coihue](https://en.wikipedia.org/wiki/Nothofagus_dombeyi), a southern beech tree native to Patagonia.

## Author

Built by [Felipe Valenzuela Beck](https://mabrax.ai) — Production AI Toolsmith.

This skill exists because I got tired of re-explaining context to Claude after long sessions. Now I use it daily on every project.

## Why Branching?

Real work isn't linear. You're deep in authentication when a payment bug surfaces. Sometimes it's a quick fix—delta and move on. But sometimes that fix expands into its own work stream with its own decisions, its own artifacts.

The original fork detection asked: archive current work, or expand scope? Neither fit. You don't want to archive incomplete work, and you don't want to pollute a focused checkpoint with unrelated context.

Branching solves this: fork creates a child checkpoint with a `parent` reference. Both remain active. The tree visualization (`chkcc tree`) shows the lineage:

```
⦿ chk-auth-system (2025-12-20) [active]
└── ○ chk-payment-fix (2025-12-21) [current]
```

The `[current]` marker shows which checkpoint is your immediate focus. Use `chkcc current <checkpoint>` to switch focus between checkpoints.

One field, one script. Natural evolution, not feature creep.

## License

MIT
