---
id: spec-008
title: Proactive Advisory Triggers
issue: ISSUE-008
version: 1.0.0
created: 2025-12-17
---

# Proactive Advisory Triggers

## Overview

This specification implements the "warnings not automation" approach decided in ISSUE-008's Resolution:

| Approach | Status | Description |
|----------|--------|-------------|
| Full automation | Rejected | Violates "user controls the flow" principle |
| No assistance | Current | Cognitive load problem |
| **Advisory warnings** | Proposed | Helps without taking control |

**Current problem**: The skill relies entirely on user initiative to checkpoint/delta. Users forget, context fills, work is lost.

**Solution**: Add guidance for the skill to recognize natural checkpoint moments and suggest action—while user always decides.

## Design Principles

1. **Advisory, not automatic**: Suggestions guide; user decides
2. **Context-aware**: Recommend checkpoint vs delta based on session state
3. **Natural language**: Conversational suggestions, not commands
4. **Non-intrusive**: Suggest at natural moments, not constantly

## Context-Aware Advisory Logic

The suggested action depends on session state:

| Session State | Advisory Action |
|---------------|-----------------|
| No checkpoint loaded | Suggest creating checkpoint |
| Working from loaded checkpoint | Suggest delta (update) |

## Trigger Conditions

Suggest checkpointing/delta when these moments occur:

| Trigger | Description | Example |
|---------|-------------|---------|
| Phase completion | A milestone or phase is done | "Phase 2 implementation complete" |
| Major decision | Significant architectural or design choice made | "Decided to use JWT over sessions" |
| Before risky operations | About to do refactor, migration, or major change | "Before starting this refactor..." |
| Extended work session | 5+ file modifications accumulated | Multiple edits across files |
| Context shift | Work direction changing substantially | "Now let's switch to the API layer" |
| Session end signals | User indicates ending or pausing | "Let's continue tomorrow" |

## Advisory Message Format

Use natural, conversational suggestions:

### No checkpoint loaded:
> You've completed the authentication implementation. This is a natural checkpoint moment—would you like me to create one?

### Checkpoint loaded (suggest delta):
> You've made significant progress since loading the checkpoint. Would you like me to update it with a delta?

### Before risky operation:
> Before starting this refactor, you might want to preserve the current state. Should I update the checkpoint with a delta?

## Implementation

### Step 1: Update SKILL.md description

Expand the description field to include advisory triggers:

**Current:**
```yaml
description: Proactive context compression for long coding sessions. Creates checkpoints (state snapshots) and deltas (incremental changes). Use when the user asks to "create checkpoint", "checkpoint", "save state", "compress context", "create delta", "delta", "update checkpoint", or "what changed".
```

**New:**
```yaml
description: Proactive context compression for long coding sessions. Creates checkpoints (state snapshots) and deltas (incremental changes). Use when the user asks to checkpoint/delta, OR when suggesting checkpointing at phase completions, major decisions, before risky operations, or after extended work sessions.
```

### Step 2: Update "proactive" explanation

Revise the blockquote to reflect skill-advisory behavior:

**Current (line 10):**
```markdown
> **What "proactive" means**: The proactiveness is *human* proactiveness—the user consciously recognizes milestones and chooses to preserve state before context fills...
```

**New:**
```markdown
> **What "proactive" means**: The skill proactively suggests checkpointing at natural moments (phase completion, major decisions, before risky operations), but the user always decides whether to act. This contrasts with *reactive* compression where the system forces summarization when limits are hit.
```

### Step 3: Add Proactive Advisory Triggers section

Add new section after "Operations" (before "Directory Structure"):

```markdown
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
```

### Step 4: Update reference documentation

Update any references that describe when the skill activates:

- AGENTS.md (if it mentions skill triggers)
- README.md (if applicable)

## Validation

| Check | Method | Expected |
|-------|--------|----------|
| Description updated | Read SKILL.md frontmatter | Advisory triggers mentioned |
| Proactive explanation revised | Read line ~10 | Skill-advisory language |
| New section added | Grep for "Proactive Advisory Triggers" | Section exists |
| Trigger table complete | Read section | 6 triggers documented |
| Context-aware logic | Read section | Both checkpoint and delta paths |
| Advisory principles | Read section | 4 principles documented |

## References

- [ISSUE-008](ISSUE-008.md): Issue driving this change
- [history/2025-12-16-dialectic-audit.md](../../history/2025-12-16-dialectic-audit.md): Discussion 5 where warnings approach was decided
- [SKILL.md](../../.claude/skills/coihuin-compress/SKILL.md): Target file for changes
