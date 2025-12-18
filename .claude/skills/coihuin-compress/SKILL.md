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

## Operations

### Checkpoint

Create new state snapshot from scratch.

**Trigger**: "checkpoint", "create checkpoint", "save state"

**When**: New work, fresh start, or no existing checkpoint to merge into.

**How**:
1. Read `checkpoint-format.md` for structure
2. Extract "What Must Survive" from conversation
3. Generate checkpoint following the format
4. Save to `checkpoints/active/<name>.md`
5. Validate: `uv run format-check.py <file>`

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

> **Note**: Git tracks checkpoint file history, so separate delta artifacts are unnecessary. The checkpoint itself evolves, with Git providing the audit trail of changes.

### Archive

Move completed checkpoint to historical storage.

**When**: Feature/epic complete, work finished.

**How**:
1. Move from `checkpoints/active/` to `checkpoints/archive/`
2. Git history provides the audit trail of checkpoint evolution

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

### What to Suggest

Adapt the suggestion to session state:

**No checkpoint loaded:**
> You've completed [milestone]. This is a natural checkpoint moment—would you like me to create one?

**Checkpoint loaded:**
> You've made significant progress since loading the checkpoint. Would you like me to update it with a delta?

**Before risky operation:**
> Before starting this [operation], you might want to preserve the current state. Should I create/update the checkpoint?

### Advisory Principles

- **Suggest, don't execute**: Wait for user confirmation
- **Be specific**: Name the milestone or trigger reason
- **Don't nag**: One suggestion per trigger moment, not repeated reminders
- **Accept "no"**: If user declines, continue without further prompting

## Directory Structure

```
checkpoints/
├── active/                    # Currently loaded into context
│   └── chk-feature-name.md    # One per active feature/epic
└── archive/                   # Historical, not loaded
    ├── .archive-marker        # Marker: ignore for context purposes
    ├── chk-auth-system.md
    └── chk-payment-flow.md
```

## Reference Files

| File | Purpose |
|------|---------|
| `checkpoint-format.md` | Checkpoint structure specification |
| `examples/checkpoint-example.md` | Reference example for first-time checkpoint creation |
| `examples/checkpoint.md` | Additional checkpoint example |
| `format-check.py` | Format validation script |

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
