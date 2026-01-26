---
name: coihuin-compress
description: Context compression for long coding sessions. Creates checkpoints (state snapshots) and maintains them as you work. Invoke at session start to auto-load the current checkpoint.
---

# Coihuin Compress

Context compression at natural breakpoints, not reactive to token limits.

## Workflow

```
Session Start (invoke skill):
  → /coihuin-compress
  → Auto-detect: run `chkcc current`
  → If current exists: read checkpoint file, resume work
  → If no current: offer to create or set one

During Session:
  → Continuous maintenance (update checkpoint as you work)
  → "delta" for explicit progress markers
  → "archive" when work complete

Checkpoint Operations (create/delta/archive):
  → Write checkpoint files
  → Auto-commit: security scan → atomic commits → checkpoint always included
```

## Continuous Maintenance

**This is the core principle.** Don't wait for "delta" commands. Update the checkpoint as you work:

| When This Happens | Update This Section |
|-------------------|---------------------|
| Decision made | → Decisions |
| File created/modified/deleted | → Artifact Trail |
| Task completed | → Play-By-Play, Current State |
| Blocker hit | → Breadcrumbs, Next Actions |
| Direction changes | → Session Intent, Next Actions |

**Update immediately, not in batches.** Small, frequent updates keep the checkpoint alive in your working memory.

## Checkpoint States

| State | Location | Meaning |
|-------|----------|---------|
| **current** | `checkpoints/active/` | The ONE checkpoint being actively worked on |
| **active** | `checkpoints/active/` | In-progress work (not immediate focus) |
| **archived** | `checkpoints/archive/` | Completed work |

```bash
chkcc current <checkpoint>  # Set as current
chkcc current               # Show current
chkcc current --clear       # Clear current
chkcc status                # Show all active with summaries
```

## Operations

### Session Start

Auto-detect and load current checkpoint when skill is invoked.

**Trigger**: `/coihuin-compress` at session start (no arguments)

**How**:
1. Run `chkcc current` to check for existing current checkpoint
2. If current checkpoint exists:
   - Read the checkpoint file
   - Acknowledge loaded context to user
   - Ready to continue work with continuous maintenance
3. If no current checkpoint:
   - Check `checkpoints/active/INDEX.md` for available checkpoints
   - If checkpoints exist: ask user which to set as current
   - If no checkpoints: offer to create a new one

### Checkpoint

Create new state snapshot.

**Trigger**: "checkpoint", "create checkpoint"

**How**:
1. Read `checkpoint-format.md` for structure
2. Extract "What Must Survive" from conversation
3. Generate checkpoint following the format
4. Save to `checkpoints/active/<name>.md`
5. Update `checkpoints/active/INDEX.md`
6. **Run Auto-Commit Flow** (see Auto-Commit Integration)

### Delta (Explicit)

Force a structured update when you want visibility into what changed.

**Trigger**: "delta", "update checkpoint"

**How**:
1. Add `## Delta: <timestamp>` section to checkpoint
2. Summarize what changed since last delta
3. Update main sections with current state
4. **Run Auto-Commit Flow** (see Auto-Commit Integration)

Note: With continuous maintenance, explicit deltas are less necessary. Use when you want a clear marker of progress.

### Archive

Complete work and move to historical storage.

**Trigger**: "archive"

**How**:
1. Capture outcome from user:
   > What was achieved? Any learnings worth preserving?
2. Add `## Completion` section with status, outcome, learnings, date
3. Move to `checkpoints/archive/`
4. Update `checkpoints/active/INDEX.md`
5. Learnings auto-extracted to `checkpoints/LEARNINGS.md`
6. **Run Auto-Commit Flow** (see Auto-Commit Integration)

**Validation**: Cannot archive checkpoints with active children (use `--force` to override).

## Auto-Commit Integration

Checkpoint operations (create, delta, archive) trigger automatic commits. The checkpoint and commit are paired — when work is significant enough to checkpoint, it's significant enough to commit.

### Philosophy

- **Atomic commits tell the story**: Each logical change gets its own commit. If there are 10 distinct changes, make 10 commits.
- **Checkpoint folder always committed**: Checkpoints are artifacts with value (learnings, context). Always stage and commit `checkpoints/`.
- **Use judgment, minimize interruption**: Auto-split changes into atomic units. Only ask human when genuinely ambiguous.

### Commit Flow (after checkpoint file is written)

1. **Security scan**
   - Check for uncommitted sensitive files: `.env`, credentials, API keys, tokens
   - Check for files that should be gitignored but aren't
   - If found: **STOP and alert user** — do not proceed with commit

2. **Analyze uncommitted changes**
   - Run `git status` to see all staged and unstaged changes
   - Group changes into logical atomic units based on:
     - Related files (same module/feature)
     - Same type of change (all tests, all docs, etc.)
     - Checkpoint files as their own unit (or with directly related code)

3. **Auto-commit each atomic unit**
   - Stage files for each logical group
   - Derive commit message (see below)
   - Execute commit
   - Repeat for each group

4. **Checkpoint commit message derivation**
   - **Type**: Usually `chore` for checkpoint maintenance, or match the work type (`feat`, `fix`, etc.)
   - **Scope**: From checkpoint anchor or primary module affected
   - **Subject**: From session intent or current state
   - **Body**: Problem being solved + key decisions (the "WHY")

### Commit Message Template (for checkpoint commits)

```
<type>(<scope>): <subject from session intent/current state>

<Problem statement — what this solves>

<Key decisions or trade-offs if relevant>

Checkpoint: <checkpoint-id>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### When to Ask Human

Only interrupt when:
- Security concern detected (sensitive files)
- Genuinely ambiguous grouping that could go multiple valid ways
- Changes seem unrelated to checkpoint scope (possible forgotten work)

Do NOT ask for:
- Confirmation of atomic splits (use judgment)
- Commit message approval (derive from checkpoint)
- Routine checkpoint commits

## Fork Detection

When work diverges into parallel streams, offer options:

**Strong signals** (any one suggests fork):
- User says work is unrelated
- Different issue/ticket involved
- Fundamental context switch

**Weak signals** (two+ together suggest fork):
- Working in entirely different files
- Scope expanding beyond original intent
- New dependencies unrelated to current work

**When detected**, present options:
- A) Create separate checkpoint (sets `parent` for lineage)
- B) Continue with current (expand scope)
- C) Set aside divergent work

**Not a fork**: Trivial fixes, config changes, supporting changes for main work.

## Directory Structure

```
checkpoints/
├── active/
│   ├── INDEX.md
│   └── chk-*.md
├── archive/
│   └── chk-*.md
└── LEARNINGS.md          # Accumulated insights from archives
```

## Reference Files

| File | Purpose |
|------|---------|
| `checkpoint-format.md` | Checkpoint structure specification |
| `index-format.md` | INDEX.md structure specification |
| `LEARNINGS.md` | Accumulated learnings from archived checkpoints |

## Priority Hierarchy (token pressure)

1. **Must Keep**: Problem, session intent, decisions, current state, next actions
2. **Should Keep**: Recent artifacts, recent play-by-play, technical context, breadcrumbs
3. **Can Summarize**: Older play-by-play, completed artifacts, historical decisions

## Quality Self-Check

Before finalizing updates, verify:

1. **Problem Clarity**: Could a fresh agent understand without the conversation?
2. **Decision Rationale**: Is the "why" captured, not just the "what"?
3. **State Specificity**: Concrete progress, not vague status?
4. **Action Actionability**: Can someone execute Next Actions immediately?
5. **Fresh Agent Test**: Loading this cold, would you know exactly what to do?
