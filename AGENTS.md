# AGENTS.md

This document provides coding agents with the context needed to work effectively in this project.

---

## Project Overview

**coihuin-compress** is a Claude Code skill for proactive context window compression. It helps maintain critical work state during long coding sessions by intelligently compressing context before automatic summarization occurs, preventing information loss.

---

## Tech Stack

- **Languages**: Markdown (skill definition), Python (CLI)
- **Framework**: Claude Code Skills system
- **CLI**: `chkcc` - Python package managed with uv
- **Dependencies**: Claude Code CLI, pyyaml

---

## Architecture

```
coihuin-compress/
├── .claude/skills/coihuin-compress/  # Skill definition
│   ├── SKILL.md                      # Main skill file
│   ├── checkpoint-format.md          # Format specification
│   └── index-format.md               # INDEX format specification
├── chkcc/                            # CLI package (flat layout)
│   ├── pyproject.toml                # Package config
│   ├── cli.py                        # Entry point
│   └── *.py                          # Commands
├── checkpoints/
│   ├── active/                       # Active checkpoints + INDEX.md
│   └── archive/                      # Completed work
└── scripts/                          # Utility scripts
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
| `chkcc/` | CLI package - install with `uv tool install ./chkcc` |
| `checkpoints/active/INDEX.md` | Active checkpoint inventory |
| `CHANGELOG.md` | Version history |
| `README.md` | User documentation |
