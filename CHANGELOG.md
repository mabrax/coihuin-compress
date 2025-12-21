# Changelog

All notable changes to the coihuin-compress skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

Nothing yet.

## [1.3.0] - 2025-12-21

### Added

- **Checkpoint branching** - Git-like parent-child relationships between checkpoints
  - New `parent` field in checkpoint frontmatter tracks lineage
  - Forking from a checkpoint automatically sets parent reference
  - Parent checkpoint remains active (enables parallel development)

- **Tree visualization CLI** - `compress-tree.py` renders checkpoint lineage as ASCII tree
  - Unicode symbols: `⦿` root, `○` active, `◉` archived
  - Scans both `active/` and `archive/` directories
  - Shows checkpoint name, date, and status

- **Fork workflow updated** - Option A now creates child checkpoint instead of archiving
  - Fork creates new checkpoint with `parent: <source-checkpoint-id>`
  - Both checkpoints remain active for parallel work streams

### Rationale

When working on multiple features from the same starting point, users need to "fork" into different lines of development without losing track of relationships. The original fork detection identified divergence but treated it as a binary choice: archive current work or expand scope. Neither captured the reality of parallel development.

The branching model enables tracking cognitive lineage—where did this line of thought come from? The tree visualization (inspired by SourceTree) makes these relationships visible at a glance. Implementation stayed minimal: one field, one script, four edits to the skill. Natural evolution, not feature creep.

## [1.2.0] - 2025-12-20

### Fixed

- **Re-incorporated INDEX integration** - Lost during global/local skill sync
  - Added INDEX maintenance instructions back to SKILL.md
  - Created `index-format.md` specification
  - Added INDEX.md validation to `format-check.py`

### Added

- **Unified command: "use compress skill"** - Single intelligent entry point
  - Skill analyzes context and decides: create checkpoint, add delta, or suggest archive
  - Removes cognitive overhead of choosing the right operation manually
  - User no longer needs to track "should I checkpoint or delta?"

- **Fork detection** - Identify when work diverges into parallel line of work
  - Detects when a "small fix" becomes significant parallel work
  - Signals: needs implementation plan, multi-issue fix, user says unrelated
  - Suggests creating separate checkpoint to avoid contaminating main work stream
  - Keeps original checkpoint focused on its intended scope

- **Proactive archive suggestion** - Skill suggests archiving when work complete
  - Explicit: User says "archive this"
  - Proactive: Skill notices work appears done, asks to confirm archive
  - Captures outcome before archiving

- **INDEX.md validation in format-check.py** - Validates INDEX files
  - Detects file type automatically (checkpoint vs INDEX)
  - Validates table headers, date formats, summary sections
  - Checks for matching entries between table and sections

### Rationale

After using the skill across multiple Claude Code instances, a pattern emerged: the user still carries mental overhead tracking the checkpoint lifecycle. Questions like "Do I need a checkpoint or delta?", "Is this a separate line of work?", and "Should I archive now?" shouldn't require user judgment for every interaction.

The fork detection need arose from real usage: while working on a feature, a bug fix surfaces. Sometimes it's trivial (just fix and delta). But sometimes that fix expands—needs an implementation plan, touches multiple issues, becomes its own coherent work stream. Without fork detection, this parallel work contaminates the original checkpoint, making it harder to understand either line of work.

The unified command philosophy: the skill should be smart enough to assess the situation and act appropriately, asking only when genuinely ambiguous (like confirming a fork or archive).

## [1.1.0] - 2025-12-19

### Added

- **INDEX.md** for active checkpoints inventory
  - Quick reference table with checkpoint name, description, last updated date
  - Summary sections for each checkpoint (Problem, Scope, Status)
  - Format validation in `format-check.py`

- INDEX maintenance integrated into checkpoint workflow:
  - Checkpoint creation: Add new entry to INDEX
  - Delta updates: Refresh "Last Updated" date, update status if changed
  - Archive: Remove entry from INDEX

### Rationale

While using the skill on a real project (moby-planner), discovered the need to quickly see what active checkpoints exist and their purpose. With multiple concurrent work streams, an index allows easy identification of which checkpoint to load without reading each file individually.

## [1.0.0] - Initial Release

### Added

- Checkpoint format specification
- Delta format (inline sections)
- Format validation script (`format-check.py`)
- Proactive advisory triggers
- Archive workflow
- Semantic quality self-check guidelines
