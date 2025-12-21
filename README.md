# Coihuin Compress

A **Claude Code skill** for proactive context compression in long coding sessions.

> **This is a skill, not a standalone tool.** Copy `.claude/skills/coihuin-compress/` to your project and it just works.

## The Problem

Long coding sessions lose critical context when automatic summarization occurs. Decisions get forgotten, file locations disappear, progress evaporates. You re-explain the same things multiple times.

## The Solution

**Proactive compression at natural breakpoints**, not reactive compression when forced by token limits.

Create **checkpoints** (state snapshots) at meaningful moments. Update them with **deltas** as work progresses. Archive when done.

## You Drive It

**You** know when you've achieved something important. You're the one who decides when to checkpoint or delta.

Think of it like saving a game — you don't wait for the game to tell you. You save when you've made progress you don't want to lose.

## Scope

One checkpoint = one focused task. A feature, a phase, a research question. Not an entire project—just the thing you're working on right now.

## Workflow

```
1. Working on something     → "checkpoint"      → Claude creates file
2. New session              → read the file     → Claude has full context
3. Continue working         → "delta"           → checkpoint updated
4. Done                     → "archive"         → moved to archive/
```

That's it. The checkpoint file IS the context—Claude reads it and knows exactly where you left off.

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

```bash
cp -r .claude/skills/coihuin-compress /path/to/your/project/.claude/skills/
```

Claude Code discovers and uses the skill automatically.

## Usage

Talk to Claude Code. Invoke the skill explicitly:

| Action | Say |
|--------|-----|
| Create checkpoint | "use compress skill to create checkpoint" |
| Update checkpoint | "use compress skill to add delta" |
| Finish & archive | "use compress skill to archive" |
| View checkpoint tree | `uv run compress-tree.py` |

The skill handles everything: format, naming, file location.

## Project Structure

```
.claude/skills/coihuin-compress/
├── SKILL.md               # Skill instructions (source of truth)
├── checkpoint-format.md   # Checkpoint specification
├── format-check.py        # Format validator
├── compress-tree.py       # Tree visualization CLI
└── examples/              # Reference checkpoints

checkpoints/
├── active/                # Work in progress
└── archive/               # Completed (.archive-marker)
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

Branching solves this: fork creates a child checkpoint with a `parent` reference. Both remain active. The tree visualization (`uv run compress-tree.py`) shows the lineage:

```
⦿ chk-auth-system (2025-12-20) [active]
└── ○ chk-payment-fix (2025-12-21) [active]
```

One field, one script. Natural evolution, not feature creep.

## License

MIT
