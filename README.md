# Coihuin Compress

A **Claude Code skill** for proactive context compression in long coding sessions.

> **This is a skill, not a standalone tool.** Copy `.claude/skills/coihuin-compress/` to your project and it just works.

## The Problem

Long coding sessions lose critical context when automatic summarization occurs. Decisions get forgotten, file locations disappear, progress evaporates. You re-explain the same things multiple times.

## The Solution

**Proactive compression at natural breakpoints**, not reactive compression when forced by token limits.

Create **checkpoints** (state snapshots) at meaningful moments. Update them with **deltas** as work progresses. Archive when done.

## Core Operations

| Operation | When | What |
|-----------|------|------|
| **Checkpoint** | New work, fresh start | Create state snapshot from scratch |
| **Delta** | Continuing work | Update existing checkpoint with changes |
| **Archive** | Work complete | Move to `checkpoints/archive/` |

## Workflow

```
Session 1 (new work):
  → "checkpoint" → creates snapshot → save to checkpoints/active/

Session 2+ (continuing):
  → load checkpoint manually
  → work...
  → "delta" → updates checkpoint with what changed

Done:
  → move to checkpoints/archive/
```

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

| Action | Trigger |
|--------|---------|
| Create checkpoint | "checkpoint", "save state" |
| Update checkpoint | "delta", "update checkpoint" |

## Validation

```bash
uv run format-check.py <file>
```

Checks structure. Semantic quality is self-checked via guidance in SKILL.md.

## Project Structure

```
.claude/skills/coihuin-compress/
├── SKILL.md               # Skill instructions (source of truth)
├── checkpoint-format.md   # Checkpoint specification
├── format-check.py        # Format validator
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

## License

MIT
