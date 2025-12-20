# Changelog

All notable changes to the coihuin-compress skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- **Re-incorporate INDEX integration** - Lost during global/local skill sync
  - INDEX maintenance instructions were in global skill but not local project
  - Local sync overwrote global, losing the feature
  - Need to add INDEX workflow back to SKILL.md

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
