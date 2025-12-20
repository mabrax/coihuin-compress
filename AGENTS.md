# AGENTS.md

This document provides coding agents with the context needed to work effectively in this project.

---

## Project Overview

**coihuin-compress** is a Claude Code skill for proactive context window compression. It helps maintain critical work state during long coding sessions by intelligently compressing context before automatic summarization occurs, preventing information loss.

---

## Tech Stack

- **Languages**: Markdown (skill definition)
- **Framework**: Claude Code Skills system
- **Dependencies**: Claude Code CLI

---

## Architecture

```
coihuin-compress/
├── .claude/skills/coihuin-compress/  # Skill definition
│   ├── SKILL.md                      # Main skill file
│   ├── checkpoint-format.md          # Format specification
│   ├── index-format.md               # INDEX format specification
│   └── format-check.py               # Validation script
├── checkpoints/
│   ├── active/                       # Active checkpoints + INDEX.md
│   └── archive/                      # Completed work
├── eval/                             # Checkpoint quality evaluation
└── journal/                          # Daily session journals
```

---

## Domain Knowledge

| Term | Definition |
|------|------------|
| **Checkpoint** | Point-in-time snapshot of work state (what exists now) |
| **Delta** | Inline section tracking changes since last checkpoint |
| **INDEX.md** | Inventory of active checkpoints with summaries |
| **Context Window** | Claude's available memory for conversation |
| **Compression** | Reducing token count while preserving critical information |
| **Archive** | Completed checkpoint moved out of active work |

---

## Key Conventions

- **Naming**: kebab-case for files, descriptive checkpoint IDs
- **Format**: Markdown for human-readable output
- **Workflow**: Checkpoint → Delta → Archive lifecycle
- **Checkpoints**: Named descriptively (e.g., `feature-auth-flow.md`)

---

## Important Files

| File | Purpose |
|------|---------|
| `.claude/skills/coihuin-compress/SKILL.md` | Main skill definition |
| `checkpoints/active/INDEX.md` | Active checkpoint inventory |
| `CHANGELOG.md` | Version history |
| `README.md` | User documentation |
