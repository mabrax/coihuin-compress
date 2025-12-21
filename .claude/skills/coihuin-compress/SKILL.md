---
name: coihuin-compress
description: Proactive context compression for long coding sessions. Creates checkpoints (state snapshots) and deltas (incremental changes). Use when the user asks to checkpoint/delta, OR when suggesting checkpointing at phase completions, major decisions, before risky operations, or after extended work sessions.
---

# Coihuin Compress

Proactive context compression at natural breakpoints, not reactive to token limits.

> **What "proactive" means**: The skill proactively suggests checkpointing at natural moments (phase completion, major decisions, before risky operations), but the user always decides whether to act. This contrasts with *reactive* compression where the system forces summarization when limits are hit.

## Workflow

```
Session 1 (new work):
  → "checkpoint" → creates new checkpoint

Session 2+ (continuing):
  → User loads checkpoint manually
  → work...
  → "delta" → updates checkpoint with what changed

Done:
  → move checkpoint to archive/
```

**Key principle**: User controls the flow. Load checkpoint manually, then tell the skill what to do.

## Unified Command

A single entry point that intelligently routes to the appropriate operation based on context.

### Trigger Phrases

| Phrase | Effect |
|--------|--------|
| "use compress skill" | Unified command - auto-detect operation |
| "compress" | Unified command - auto-detect operation |
| "compress skill" | Unified command - auto-detect operation |

### Decision Tree

When the unified command is invoked, evaluate context and route:

```
Is a checkpoint loaded in context?
├─ NO → Suggest: Create new checkpoint
│       "No checkpoint is loaded. Would you like me to create one for the current work?"
│
└─ YES → Has significant work been done since loading?
         ├─ NO → Inform: Nothing to update
         │       "The checkpoint is loaded but no significant changes detected yet."
         │
         └─ YES → Does work appear complete?
                  ├─ YES → Suggest: Archive
                  │       "Work appears complete. Would you like to archive this checkpoint?"
                  │
                  └─ NO → Is work diverging into unrelated streams?
                          ├─ YES → Suggest: Fork (see Fork Detection)
                          │       "Work seems to be diverging. Should we create a separate checkpoint?"
                          │
                          └─ NO → Suggest: Delta
                                  "You've made progress. Would you like me to update the checkpoint with a delta?"
```

### Context Detection

**"Checkpoint loaded"** means:
- User attached a checkpoint file to the conversation (via `@` notation or file read)
- The checkpoint content is visible in the current context
- Detection: Look for checkpoint frontmatter (`---\ncheckpoint: <name>\n...`) in recent context

**"Significant work"** means any of:
- 2+ files modified or created
- A decision was made and discussed
- A task from Next Actions was completed
- User explicitly says work was done

**"Work appears complete"** means:
- All items in Next Actions are done
- User says "done", "finished", "complete", or similar
- No pending blockers remain

Completion checklist (verify before suggesting archive):
- [ ] Every Next Action item addressed or explicitly deferred
- [ ] No unresolved blockers in Current State
- [ ] Original Problem statement satisfied
- [ ] No "TODO" or "FIXME" mentions in recent work
- [ ] User sentiment indicates closure (not "one more thing")

**"Work diverging"** means:
- See Fork Detection section below

### Backward Compatibility

Explicit commands still work and take precedence:

| Command | Effect |
|---------|--------|
| "checkpoint", "create checkpoint" | Always creates new checkpoint |
| "delta", "update checkpoint" | Always updates existing checkpoint |
| "archive", "archive checkpoint" | Always archives checkpoint |

The unified command is a convenience—it doesn't replace explicit operations. Users who prefer direct control can continue using specific commands.

## Fork Detection

Identify when work diverges into parallel streams that warrant separate checkpoints.

### Strong Fork Signals

Any single strong signal suggests forking:

| Signal | Example |
|--------|---------|
| User explicitly says work is unrelated | "This is a different feature entirely" |
| Work needs its own implementation plan | "Let me plan how to approach this new subsystem" |
| Multiple issues/tickets involved | "While I'm here, let me also fix ISSUE-234" |
| Different milestone/epic | "Actually, let's work on the Q2 goals instead" |
| Fundamental context switch | "Forget auth—let's do the billing integration" |

### Weak Fork Signals

Two or more weak signals together suggest forking:

| Signal | Example |
|--------|---------|
| Working in entirely different files | From `src/auth/` to `src/payments/` |
| Scope expanding beyond original intent | "We should also add..." (repeatedly) |
| New dependencies introduced | Adding a library unrelated to current work |
| Different stakeholders affected | "This will need review from the payments team" |
| Time gap with context shift | "I was working on X, but now I want to do Y" |

### Not a Fork

These do NOT indicate a fork—continue with the current checkpoint:

| Pattern | Why It's Not a Fork |
|---------|---------------------|
| Trivial fixes in passing | Typo corrections, lint fixes, small cleanup |
| Config/tooling changes | Adjusting build config, updating deps, CI tweaks |
| Supporting changes for main work | Adding a utility function needed by the feature |
| Refactoring to enable the goal | Restructuring code to implement the main objective |
| Test additions for current work | Writing tests for the feature being built |

### Fork Decision Flow

When fork signals are detected, prompt the user with options:

```
Work seems to be diverging from the current checkpoint scope.

Current checkpoint: chk-auth-system
  Scope: User authentication and session management

Detected: [describe the divergent work]

Options:
  A) Create separate checkpoint for new work
     → Creates new checkpoint with `parent: <current-checkpoint-id>`
     → Current checkpoint remains active (parallel development)

  B) Continue with current checkpoint
     → Expands scope to include new work (update Problem section)

  C) Abandon divergent work
     → Set aside new work, refocus on original scope

Which would you prefer?
```

### Fork Advisory Principles

- **Never auto-fork**: Always present options to the user; never automatically create checkpoints
- **Always confirm**: Even with strong signals, the user decides what constitutes a "fork"
- **Respect "no"**: If user chooses to continue with current checkpoint, don't re-suggest
- **Explain the signal**: Tell the user why you think work is diverging
- **Low friction**: If user says "just continue", update the checkpoint scope rather than nagging

### Branch Lineage

When forking creates a new checkpoint, the system automatically:

1. Sets the `parent` field to the current checkpoint's ID
2. The parent checkpoint remains active (enables parallel development)
3. Use `uv run compress-tree.py` to visualize the lineage

Example: Forking from `chk-auth-system` to work on payments:
```yaml
---
checkpoint: chk-payment-flow
created: 2025-12-21T14:00:00Z
parent: chk-auth-system
---
```

This creates a branch visible in the checkpoint tree:
```
⦿ chk-auth-system (2025-12-20) [active]
└── ○ chk-payment-flow (2025-12-21) [active]
```

## Operations

### Checkpoint

Create new state snapshot from scratch.

**Trigger**: "checkpoint", "create checkpoint", "save state"

**When**: New work, fresh start, or no existing checkpoint to merge into.

**How**:
1. Read `checkpoint-format.md` for structure
2. Extract "What Must Survive" from conversation
3. Generate checkpoint following the format
   - If forking from existing checkpoint, set `parent: <source-checkpoint-id>`
4. Save to `checkpoints/active/<name>.md`
5. Validate: `uv run format-check.py <file>`
6. Update `checkpoints/active/INDEX.md`:
   - Add row to Quick Reference Table
   - Add Summary Section (see `index-format.md`)

### Delta

Update an existing checkpoint with changes from the current session.

**Trigger**: "delta", "update checkpoint", "add delta"

**Prerequisite**: User has loaded existing checkpoint into context.

**How**:
1. Identify what changed since the checkpoint was created
2. Update the relevant checkpoint sections:
   - **Decisions**: Append new decisions
   - **Play-By-Play**: Append new entries, summarize old
   - **Artifact Trail**: Update file statuses, add new files
   - **Current State**: Replace entirely
   - **Next Actions**: Replace entirely
3. Optionally add inline delta markers for visibility
4. Output updated checkpoint for user to save
5. Update `checkpoints/active/INDEX.md`:
   - Update Last Updated date in table
   - Update Status in Summary Section if changed

> **Note**: Git tracks checkpoint file history, so separate delta artifacts are unnecessary. The checkpoint itself evolves, with Git providing the audit trail of changes.

### Archive

Mark checkpoint as complete and move to historical storage.

**Trigger**: "archive", "archive checkpoint"

**When**: Feature/epic complete, work finished.

**How**:
1. Capture outcome from user before archiving:
   > Before archiving, let me capture the outcome:
   > - What was achieved? (1-2 sentences)
   > - Any learnings or gotchas worth preserving?
2. Add `## Completion` section to the checkpoint:
   ```markdown
   ## Completion
   - **Status**: Archived
   - **Outcome**: [User's description of what was achieved]
   - **Learnings**: [Any gotchas or insights, or "None noted"]
   - **Date**: [ISO-8601 timestamp]
   ```
3. Move from `checkpoints/active/` to `checkpoints/archive/`
4. Update `checkpoints/active/INDEX.md`:
   - Remove row from Quick Reference Table
   - Remove Summary Section
5. Git history provides the audit trail of checkpoint evolution

**Archive Limitations**: Archived checkpoints are historical snapshots, not live state:
- File references may be outdated (files moved, renamed, deleted)
- Technical context may no longer apply (dependencies updated)
- Decisions may have been revisited in later work

Use for: understanding decisions, auditing evolution, onboarding context.
Do NOT use for: resuming work, current state, Claude context loading.

## Proactive Advisory Triggers

The skill should suggest checkpointing/delta at natural moments. These are advisory—user always decides.

### When to Suggest

| Trigger | Suggest When |
|---------|--------------|
| Phase completion | A milestone, phase, or significant task completes |
| Major decision | An architectural or design decision is made |
| Before risky ops | About to start refactor, migration, or major change |
| Extended session | 5+ file modifications accumulated |
| Context shift | Work direction changing substantially |
| Session end | User indicates ending ("let's continue tomorrow") |
| Work complete | All Next Actions done, user says "done/finished", no blockers remain |

### What to Suggest

Adapt the suggestion to session state:

**No checkpoint loaded:**
> You've completed [milestone]. This is a natural checkpoint moment—would you like me to create one?

**Checkpoint loaded:**
> You've made significant progress since loading the checkpoint. Would you like me to update it with a delta?

**Before risky operation:**
> Before starting this [operation], you might want to preserve the current state. Should I create/update the checkpoint?

**Work complete:**
> All Next Actions appear done and no blockers remain. Would you like to archive this checkpoint? Before archiving, I'll ask what was achieved and any learnings to preserve.

### Advisory Principles

- **Suggest, don't execute**: Wait for user confirmation
- **Be specific**: Name the milestone or trigger reason
- **Don't nag**: One suggestion per trigger moment, not repeated reminders
- **Accept "no"**: If user declines, continue without further prompting

## Directory Structure

```
checkpoints/
├── active/                    # Currently loaded into context
│   ├── INDEX.md               # Quick inventory of active checkpoints
│   └── chk-feature-name.md    # One per active feature/epic
└── archive/                   # Historical, not loaded
    ├── .archive-marker        # Marker: ignore for context purposes
    ├── chk-auth-system.md
    └── chk-payment-flow.md
```

## Reference Files

| File | Purpose |
|------|---------|
| `checkpoint-format.md` | Checkpoint and delta structure specification |
| `index-format.md` | INDEX.md structure specification |
| `examples/checkpoint.md` | Initial checkpoint example (no deltas yet) |
| `examples/checkpoint-with-delta.md` | Checkpoint with deltas example (shows accumulation) |
| `format-check.py` | Format validation script |
| `compress-tree.py` | Checkpoint tree visualization script |

## Priority Hierarchy (token pressure)

1. **Must Keep**: Problem, session intent, decisions, current state, next actions
2. **Should Keep**: Recent artifact trail, recent play-by-play, technical context, breadcrumbs
3. **Can Summarize**: Older play-by-play, completed artifacts, historical decisions

## Semantic Quality Self-Check

Before finalizing a checkpoint, verify it would enable a fresh agent to resume work effectively. Ask yourself these five questions:

### 1. Problem Clarity
> Could a fresh agent understand what we're trying to solve without reading the conversation?

The Problem section should stand alone. If it references "the issue" or "what we discussed" without explanation, it fails this check.

### 2. Decision Rationale
> For each decision, is the "why" captured—not just the "what"?

Decisions without rationale force future agents to re-debate resolved questions. Include: what was decided, why, and what alternatives were rejected.

### 3. State Specificity
> Does Current State describe concrete progress, not vague status?

Bad: "Made good progress on the feature"
Good: "Implemented user authentication with JWT tokens; login endpoint working, logout not started"

### 4. Action Actionability
> Could someone execute Next Actions without asking clarifying questions?

Each action should be specific enough to start immediately. "Fix the bug" fails; "Fix null pointer in UserService.validate() when email is empty" passes.

### 5. Fresh Agent Test
> If I imagine loading this checkpoint tomorrow with no memory, would I know exactly what to do?

This is the ultimate test. Read the checkpoint as if you've never seen the project. Does it work?

---

**Note**: This self-check is guidance for checkpoint authors—it is not automated validation. The `format-check.py` script validates structure; this section helps ensure semantic quality. For formal evaluation, see `eval/rubric.md`.

## Checkpoint Evaluation

Evaluate checkpoint quality using a dialectic process that combines human judgment with agent verification.

### Usage

```
/eval-checkpoint <name>
```

Place checkpoints to evaluate in `eval/inbox/`. The command expects a checkpoint filename (with or without `.md` extension).

### The 3-Phase Dialectic Process

1. **Human Interview**: User answers 5 questions (one per quality dimension) about the checkpoint. Answers map to preliminary scores (A=5, B=4, C=3, D=2, E=1).

2. **Agent Investigation**: Three parallel verification tasks:
   - Artifact verification (files exist and match descriptions)
   - Breadcrumb validation (references are valid)
   - Git correlation (play-by-play matches commit history)

3. **Correlation & Synthesis**: Agent evidence modifies human scores. Strong supporting evidence can raise scores; contradictions lower them. Final weighted score determines quality.

### Quality Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Recoverability | 30% | Could a fresh agent resume work from this alone? |
| Completeness | 20% | Are all required sections meaningfully filled? |
| Clarity | 20% | Is the language unambiguous without prior context? |
| Token Efficiency | 15% | Is information dense without unnecessary verbosity? |
| Actionability | 15% | Are Next Actions specific enough to execute? |

See `eval/rubric.md` for detailed scoring criteria per dimension.

### Dogfooding Workflow

The evaluation system supports continuous improvement through example collection:

```
eval/
├── inbox/      # Checkpoints awaiting evaluation
├── scored/     # Evaluated checkpoints with scores
└── promoted/   # High-quality examples (score >= 4.0)
```

**Workflow**:
1. **Collect**: Copy checkpoints into `eval/inbox/` for evaluation
2. **Evaluate**: Run `/eval-checkpoint <name>` to score
3. **Promote**: Checkpoints scoring >= 4.0 (with no dimension below 3 and Recoverability >= 4) can be promoted to `eval/promoted/` as reference examples

Promoted checkpoints serve as canonical examples of well-structured state snapshots.
