# coihuin-compress

A **Claude Code skill** for proactive context compression in long coding sessions.

> **This is a skill, not a standalone tool.** Copy `.claude/skills/coihuin-compress/` to your project and it just works.

## The Problem

Long coding sessions with Claude lose critical context when automatic summarization occurs. Decisions get forgotten, file locations disappear, and progress evaporates. You end up re-explaining the same things multiple times.

## The Solution

**Proactive compression at natural breakpoints**, not reactive compression when forced by token limits.

Instead of waiting for context to overflow and get summarized away, create explicit **checkpoints** (state snapshots) at meaningful moments—phase complete, major decision made, session end. When continuing work, load the checkpoint and **merge** new progress into it.

## Core Concepts

| Concept | Definition |
|---------|------------|
| **Checkpoint** | Point-in-time snapshot of work state. Self-contained, loadable, resumable. |
| **Delta** | Incremental changes between checkpoints. Shows what changed without full regeneration. |
| **Merge** | Apply delta to existing checkpoint, producing updated state. |

## What Must Survive

Based on [Factory.ai's research](https://factory.ai/news/compressing-context), checkpoints preserve:

- **Session Intent** — What you're trying to achieve
- **Decisions** — Locked-in choices (never re-ask these)
- **Play-By-Play** — High-level action history
- **Artifact Trail** — Files created/modified/deleted
- **Current State** — What exists now
- **Next Actions** — What comes next

## Workflow

```
Session 1 (new work):
  → "checkpoint" → creates new checkpoint → save to checkpoints/active/

Session 2+ (continuing):
  → load checkpoint manually
  → work...
  → "merge" → generates delta + merges into checkpoint

Done:
  → move checkpoint to checkpoints/archive/
```

## Installation

Copy the skill directory to your project:

```bash
cp -r .claude/skills/coihuin-compress /path/to/your/project/.claude/skills/
```

That's it. Claude Code will discover and use the skill automatically.

## Usage

**Create new checkpoint:**
```
"checkpoint" or "create checkpoint" or "save state"
```

**See what changed (without merging):**
```
"delta" or "what changed"
```

**Merge changes into loaded checkpoint:**
```
"merge" or "merge checkpoint"
```

## Validation

Validate checkpoint/delta format with the included Python script:

```bash
uv run validate.py checkpoint <file>
uv run validate.py delta <file>
uv run validate.py <file>  # auto-detect type
```

## Project Structure

```
.claude/skills/coihuin-compress/
├── SKILL.md               # Skill instructions
├── checkpoint-format.md   # Checkpoint specification
├── delta-format.md        # Delta specification
├── validate.py            # Format validator
└── examples/
    ├── checkpoint.md      # Reference example
    └── delta.md           # Reference example

checkpoints/
├── active/                # Currently active work
└── archive/               # Completed, historical
```

## Background

This Claude Code skill formalizes a workflow I'd been using informally. Two sources shaped the design:

1. **[ReSum](https://arxiv.org/pdf/2509.13313)** (Alibaba NLP) — Context summarization for long-horizon search intelligence
2. **[Factory.ai](https://factory.ai/news/compressing-context)** — "What Must Survive" categories, proactive vs reactive compression

The name comes from the [coihue](https://en.wikipedia.org/wiki/Nothofagus_dombeyi) (Nothofagus dombeyi), a southern beech tree native to Patagonia.

## License

MIT
