# Changelog

All notable changes to the coihuin-compress skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

Nothing yet.

## [1.8.0] - 2026-01-06

### Added

- **`chkcc update` command** - Sync skill files from package to project
  - Checksum-based comparison detects local modifications
  - `--force` flag overwrites locally modified files
  - `--dry-run` flag shows what would change without writing
  - Requires `chkcc init` first (validates setup)

- **`chkcc stop-hook` command** - Portable Stop hook for Claude Code
  - Reads JSON from stdin, outputs decision to stdout
  - Detects meaningful work (Write/Edit/NotebookEdit) in transcript
  - Excludes checkpoint file operations from "work" detection
  - Blocks session end with reminder to checkpoint if work detected
  - No more hardcoded script paths in hook configuration

- **Skill file packaging** - Canonical source moved to CLI package
  - Skill files now live in `chkcc/data/skill/` (package owns them)
  - `chkcc init` installs skill files to project `.claude/skills/`
  - `chkcc update` syncs changes after package updates
  - `chkcc doctor` validates skill files match package

- **Stop hook in `chkcc init`** - Full hook setup
  - Installs both SessionStart and Stop hooks
  - Uses new matcher-based hook format
  - Detects existing hooks (old and new formats) to avoid duplicates

- **Enhanced `chkcc doctor`** - Comprehensive health checks
  - Validates Stop hook installation
  - Validates skill files match package (with checksum)
  - Reports missing/modified skill files
  - `--fix` repairs skill files and hooks

### Changed

- **Skill files removed from repo** - No longer in `.claude/skills/`
  - Canonical source is now `chkcc/data/skill/`
  - Projects get skill files via `chkcc init` or `chkcc update`
  - Eliminates sync issues between repo and installed versions

- **Hook format** - Now uses matcher-based structure
  - Old: `{"type": "command", "command": "..."}`
  - New: `{"matcher": "", "hooks": [{"type": "command", "command": "..."}]}`
  - Both formats detected for backward compatibility

### Rationale

The skill files lived in two places: the repo (`.claude/skills/`) and projects where they were copied. Updates required manual copying, and versions drifted. The solution: make the CLI package the single source of truth.

`chkcc init` now does complete setup: directories, INDEX files, skill files, AND hooks (both SessionStart and Stop). `chkcc update` syncs skill files after package updates—like `apt upgrade` for your skill.

The Stop hook solves context loss: users forget to checkpoint before ending sessions. Now Claude gets a reminder when meaningful work was done. The hook is portable (`chkcc stop-hook`) instead of a hardcoded script path, so it works across machines and after reinstalls.

Doctor got smarter: it validates the full setup including skill files and Stop hook. One command to know if everything's configured correctly.

## [1.7.0] - 2026-01-03

### Added

- **`chkcc init` command** - One-command project setup
  - Creates `checkpoints/active/` and `checkpoints/archive/` directories
  - Creates `INDEX.md` files in both directories
  - Installs `SessionStart` hook into `.claude/settings.json`
  - Merges with existing hooks if settings.json already exists
  - Idempotent: skips what already exists

- **`chkcc doctor` command** - Health check for setup
  - Validates directory structure exists
  - Validates INDEX.md exists
  - Validates SessionStart hook is installed
  - Reports status with checkmarks/crosses
  - Returns exit code 1 if issues found
  - `--fix` flag automatically repairs all issues

- **`chkcc prime` command** - Context recovery for hooks
  - Outputs current checkpoint content to stdout
  - Silent exit (code 0, no output) if no current checkpoint
  - `--header` flag prepends `# Context Recovery: {checkpoint-name}`
  - Designed for Claude Code `SessionStart` hooks

- **Unit test suite** - pytest-based tests for CLI
  - `tests/test_prime.py` - 4 tests for prime command
  - `tests/test_init.py` - 6 tests for init command
  - `tests/test_doctor.py` - 10 tests for doctor command (including --fix)
  - pytest added as dev dependency

### Rationale

The skill and CLI work great once set up, but onboarding friction remained: manually creating directories, understanding the structure, remembering to read the checkpoint at session start. The `init` command eliminates setup friction—one command creates everything including the hook that primes context on session start.

The `prime` command enables automatic context recovery. When installed as a `SessionStart` hook, it outputs the current checkpoint at the start of every session. Claude reads this and immediately has full context. No manual "read the checkpoint" step needed.

The `doctor` command provides visibility into setup state. "Is everything configured correctly?" becomes a single command instead of manually checking multiple files and directories.

## [1.6.0] - 2025-12-27

### Added

- **Learnings extraction** - Knowledge persists beyond archived checkpoints
  - On archive, learnings auto-extracted from `## Completion` section
  - Appended to `checkpoints/LEARNINGS.md` with date and checkpoint name
  - Read at session start for project-level insights

- **Continuous Maintenance model** - Checkpoints as living working state
  - Update checkpoint sections immediately as you work, not in batches
  - Decision made → update Decisions; file changed → update Artifact Trail
  - Small, frequent updates keep checkpoint in Claude's active awareness

### Changed

- **SKILL.md compressed** - 505 → 153 lines (70% reduction)
  - Removed proactive advisory triggers (they diluted over long sessions)
  - Removed checkpoint evaluation section
  - Simplified fork detection
  - Core focus: continuous maintenance

### Removed

- **Proactive advisory triggers** - Replaced by continuous maintenance model
  - Old: "suggest checkpointing at phase completion, major decisions..."
  - New: maintain the checkpoint as you work, no suggestions needed

### Rationale

Through daily usage across projects, a friction surfaced: checkpoints are read once at session start but fade from Claude's awareness as conversations grow. The skill instructions said "update when there's progress" but that got lost in the noise.

The insight came from comparing to TodoWrite: it stays alive because Claude touches it constantly. Checkpoints were designed as documentation—read once, update occasionally. The evolution: treat checkpoints as working state, updated continuously like a todo list.

The proactive triggers were well-intentioned but added cognitive load to the instructions. With continuous maintenance, Claude doesn't need to be told when to update—it's woven into the workflow.

Learnings extraction solves a different problem: insights get buried in archived checkpoints. Now they accumulate in one place, readable at session start.

## [1.5.0] - 2025-12-26

### Added

- **Current state** - Mark exactly ONE checkpoint as immediate focus
  - New `status` field in frontmatter: `current` or `active`
  - Only one checkpoint can be `current` at a time
  - Distinguishes "working on right now" from "parked but in progress"

- **`chkcc status` command** - Quick orientation view
  - Shows checkpoint summaries with problem context and next actions
  - Current checkpoint displayed first
  - `--all` flag includes archived checkpoints

- **`chkcc current` command** - Manage current checkpoint
  - `chkcc current <checkpoint>` - Set checkpoint as current
  - `chkcc current` - Show current checkpoint
  - `chkcc current --clear` - Clear current marker

- **Archive validation** - Prevent orphaning child checkpoints
  - Cannot archive a checkpoint with active children
  - `--force` flag to override validation
  - Ensures leaves-first archive order for branched checkpoints

- **Scaffold `--current` flag** - Create checkpoint as current immediately
  - `chkcc scaffold checkpoint <name> --current`
  - Clears any existing current before setting new one

### Rationale

Working across multiple projects revealed a gap: with several active checkpoints, which one am I actually working on right now? The original active/archived distinction wasn't enough. You might have three checkpoints in `active/` but only one is your immediate focus—the others are parked.

The `current` state solves this. Like `git checkout`, it marks your working context. The `status` command provides quick orientation: "What am I working on and what's next?" without opening files. Archive validation prevents accidentally orphaning child checkpoints when using branching workflows.

Design stayed minimal: one frontmatter field, two new commands, validation at archive time. The status field lives in frontmatter (not directory structure) to keep the filesystem simple while enabling richer state tracking.

## [1.4.0] - 2025-12-25

### Added

- **CLI package (`chkcc`)** - Direct command-line interface for checkpoint management
  - `chkcc tree` - Visualize checkpoint lineage
  - `chkcc validate <file>` - Check checkpoint format
  - `chkcc scaffold checkpoint <name>` - Create new checkpoint
  - `chkcc scaffold delta <file>` - Add delta to checkpoint
  - `chkcc archive <file>` - Archive completed checkpoint

- **Tree status filter** - Filter tree view by checkpoint status
  - `-s active` / `--status active` shows only active checkpoints
  - `-s archive` / `--status archive` shows only archived checkpoints
  - `-s all` / `--status all` shows all (default)

### Rationale

The skill works great for conversational workflows, but power users and scripts need direct access. The CLI provides the same functionality without requiring Claude Code—useful for automation, CI/CD, or quick terminal checks. Both interfaces coexist: skill for natural interaction, CLI for direct control.

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
