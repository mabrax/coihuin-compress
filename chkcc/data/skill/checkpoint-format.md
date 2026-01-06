# Checkpoint Format Specification

Version: 1.3.0

## Overview

A **checkpoint** is a point-in-time snapshot of work state optimized for token-efficient session continuation. Checkpoints follow the "What Must Survive" principle: preserve only information critical for an agent to resume work seamlessly.

## Design Principles

1. **Self-contained**: A checkpoint alone is sufficient to continue work
2. **Token-efficient**: Minimize tokens while maximizing information density
3. **Proactive**: Created at natural breakpoints, not when forced by limits
4. **Recoverable**: Any checkpoint enables seamless work resumption

## Structure

```markdown
---
checkpoint: <id>
created: <ISO-8601 timestamp>
anchor: <reference to conversation point or phase>
parent: <parent-checkpoint-id>  # optional, for forked checkpoints
status: <current|active>  # optional, defaults to 'active' if omitted
---

## Problem
[Stable problem statement - rarely changes between checkpoints]

## Session Intent
[What the user wants to achieve, requirements, ideal outcome]

## Essential Information

### Decisions
[User decisions that are locked in and should not be re-asked]

### Technical Context
[Stack, configuration, environment - facts that inform implementation]

### Breadcrumbs
[Minimal references for context reconstruction]

| Type | Reference | Hint |
|------|-----------|------|
| file | `path/to/file` | What this contains/does |
| function | `module.functionName()` | What this function does |
| decision | Phase N, topic | Why this decision was made |
| external | URL or identifier | What this resource provides |

### Play-By-Play
[High-level sequence of major actions completed]
- Phase/Step → Action → Outcome

### Artifact Trail
[Files created, modified, or deleted with key changes]

| File | Status | Key Change |
|------|--------|------------|
| `path/to/file` | created/modified/deleted | Brief description |

### Current State
[What exists now - completed work, current status]

### Next Actions
[What comes next - pending work, blockers]

## User Rules
[Constraints and preferences the agent must follow]

## Completion
[Only present when checkpoint is archived]
- **Status**: Archived
- **Outcome**: Brief description of what was achieved
- **Date**: ISO-8601 timestamp
```

## Field Definitions

### Header Fields

| Field | Required | Description |
|-------|----------|-------------|
| `checkpoint` | Yes | Unique identifier (e.g., `chk-001`, `session-abc-003`) |
| `created` | Yes | ISO-8601 timestamp of checkpoint creation |
| `anchor` | No | Reference to conversation turn or phase this summarizes up to |
| `last_delta` | No | ISO-8601 timestamp of last delta operation |
| `parent` | No | Checkpoint ID of the parent (for forked checkpoints) |
| `status` | No | Checkpoint status: `current` (immediate focus) or `active` (in-progress). Defaults to `active` if omitted. |

### Status Field Semantics

The `status` field indicates the operational state of a checkpoint:

- **`current`**: Exactly ONE checkpoint should have this status—it represents the checkpoint that is the immediate focus of work
- **`active`**: The checkpoint is in progress but not the immediate focus of work
- **Default behavior**: If the `status` field is omitted, the checkpoint is treated as `active` (backward compatible with existing checkpoints)
- **Archived checkpoints**: The `status` field only applies to checkpoints in the `active/` directory. Once archived (moved to `archive/` with a `## Completion` section), the `status` field is ignored—location determines archived state.

Note: Only one checkpoint should be marked as `current` in an active work session. When moving to a different checkpoint, update the old one from `current` to `active`.

### Validation Rules

1. Only one checkpoint in `active/` should have `status: current` at a time
2. Tools should warn if multiple `current` checkpoints are detected
3. Setting a new checkpoint as `current` should first clear the existing `current`

### Parent Field Semantics

The `parent` field establishes lineage between checkpoints:

- **Root checkpoints**: No `parent` field - represent independent work streams
- **Forked checkpoints**: `parent` contains the checkpoint ID from which this work diverged
- **Multiple children**: A parent can have multiple children (parallel forks)

Use `uv run compress-tree.py` to visualize checkpoint lineage.

### Body Sections

| Section | Required | Purpose | Compression Behavior |
|---------|----------|---------|---------------------|
| Problem | Yes | Stable problem statement | Rarely changes; copy forward |
| Session Intent | Yes | User's goal and requirements | Update only when goal shifts |
| Decisions | Yes | Locked-in choices | Accumulate; never drop |
| Technical Context | Yes | Stack, env, config | Update when changes occur |
| Play-By-Play | Yes | Action history | Summarize older entries; keep recent detailed |
| Artifact Trail | Yes | Files touched | Prune completed/irrelevant; keep active |
| Current State | Yes | What exists now | Replace entirely each checkpoint |
| Next Actions | Yes | Pending work | Replace entirely each checkpoint |
| Breadcrumbs | No | Minimal references for context reconstruction | Prune stale entries opportunistically during merge |
| User Rules | No | Constraints | Copy forward unless changed |
| Completion | No | Archive marker with outcome | Added only when archiving |

## Information Priority Hierarchy

When under token pressure, preserve in this order:

1. **Must Keep** (never drop)
   - Problem statement
   - Session intent
   - User decisions
   - Current state
   - Next actions

2. **Should Keep** (compress if needed)
   - Artifact trail (recent files)
   - Play-by-play (recent actions)
   - Technical context
   - Breadcrumbs (compress stale entries as needed)

3. **Can Summarize** (aggressive compression allowed)
   - Older play-by-play entries
   - Completed artifact entries
   - Historical decisions that led to current state

## Checkpoint Triggers

Create a new checkpoint when:

1. **Phase completion**: A distinct unit of work is done
2. **Major decision**: User makes a significant choice
3. **Context shift**: Work direction changes substantially
4. **Session break**: Before ending a session
5. **Pre-compression**: Before context window pressure

## Delta Format

Deltas are **not separate files**—they are `## Delta:` sections appended inline to the checkpoint file. This keeps all state in one place while Git tracks the evolution.

### Structure

```markdown
---

## Delta: <ISO-8601 timestamp>

### What Changed

[One-sentence summary of what was accomplished]

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `path/to/file` | created/modified/deleted | Brief description |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| Phase/Task name | Previous status | New status |
```

### Delta Fields

| Section | Required | Purpose |
|---------|----------|---------|
| What Changed | Yes | Brief summary of the session's work |
| Artifacts | Yes | Files created, modified, or deleted |
| Status Transitions | No | Track phase/task state changes |

### When to Add a Delta

Add a delta when:
- Significant work has been completed since checkpoint creation or last delta
- You want to preserve progress before ending a session
- Major artifacts have been created or modified

Update the `last_delta` field in the checkpoint frontmatter when adding a delta.

See `examples/checkpoint-with-delta.md` for a complete example.

## LEARNINGS.md

When a checkpoint is archived, learnings are automatically extracted and appended to `checkpoints/LEARNINGS.md`. This creates a cumulative knowledge base that doesn't get buried in archived checkpoints.

### Structure

```markdown
# Learnings

## 2025-12-27 — chk-auth-system
- JWT refresh tokens need 15min expiry, not 1hr
- Always validate on backend, frontend is just UX

## 2025-12-26 — chk-payment-fix
- Stripe webhooks retry 3x, must be idempotent
```

### Extraction

The archive process extracts the `**Learnings**:` field from the `## Completion` section. If learnings are "None noted" or similar, nothing is appended.

### Usage

Read `checkpoints/LEARNINGS.md` at session start to carry forward project-level insights without re-reading archived checkpoints.
