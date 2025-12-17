---
id: spec-007
title: Two-Layer Validation System
issue: ISSUE-007
version: 1.0.0
created: 2025-12-17
---

# Two-Layer Validation System

## Overview

This specification implements the two-layer validation model decided in ISSUE-007's Resolution:

| Layer | Tool | Responsibility |
|-------|------|----------------|
| **Structural** | `format-check.py` | Fields, sections, syntax |
| **Semantic** | LLM in SKILL.md | Meaning, recoverability, drift |

**Current problem**: `validate.py` says "Valid checkpoint" but only checks structure—users assume quality when they get semantic garbage wrapped in correct format.

**Solution**:
1. Rename to honest `format-check.py` (structural layer)
2. Add advisory heuristics as warnings in the format checker output (convenience, not a separate layer)
3. Embed self-check guidance in SKILL.md for runtime semantic quality (semantic layer)

## Design Principles

1. **Honest naming**: Scripts should do what their name says—format checker checks format, not quality
2. **Warnings over errors**: Semantic heuristics are advisory; passing structure is sufficient for format validity
3. **Two concerns, two tools**: Structural validation (script) and semantic validation (LLM) are different responsibilities
4. **No false confidence**: Output must clarify what "valid" means and doesn't mean

## Design Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| Rename validate.py? | Yes → format-check.py | Honest naming principle; "validate" implies quality |
| Semantic heuristics in script? | Yes, as warnings | Provides actionable feedback without blocking |
| Block on heuristic failures? | No | Heuristics are fuzzy; structural validity is binary |
| LLM self-check in SKILL.md? | Yes | Runtime semantic validation during checkpoint creation |
| Integrate with eval rubric? | Reference only | ISSUE-011 provides external semantic evaluation |

## Two-Layer Validation Model

Per ISSUE-007 Resolution, validation uses two distinct layers with different tools:

| Layer | Tool | What it checks |
|-------|------|----------------|
| **Structural** | `format-check.py` | Fields, sections, syntax |
| **Semantic** | LLM in-skill | Meaning, recoverability, drift |

### Layer 1: Structural (format-check.py)

Checks format correctness—fields exist, sections present, syntax valid.

**Required Checks (errors):**

| Check | Type | Failure Mode |
|-------|------|--------------|
| YAML frontmatter parseable | Required | Error |
| Required fields present (checkpoint, created, anchor) | Required | Error |
| Required sections exist (Problem, Essential Information, etc.) | Required | Error |
| Markdown structure valid | Required | Error |

**Advisory Heuristics (warnings):**

The structural tool also outputs heuristic warnings as advisory feedback. These are NOT a separate validation layer—they are convenience output from the format checker to surface potential quality issues without blocking.

| Check | Trigger | Warning Message |
|-------|---------|-----------------|
| Problem length | < 20 words | "Problem statement may be too brief for standalone understanding" |
| Decisions count | < 2 entries | "Few decisions recorded—are key choices captured?" |
| Play-By-Play entries | < 2 entries | "Limited history—is progression clear?" |
| Artifact Trail | Empty | "No artifacts tracked—is this intentional?" |
| Next Actions | Empty or vague | "Next actions may not be actionable" |
| Current State | < 30 words | "Current state may lack sufficient detail" |
| Checkpoint age | `created` > 7 days old | "Checkpoint may be stale—is it still current?" |
| Last delta recency | `last_delta` > 3 days old | "No recent updates—is the checkpoint still accurate?" |

**Output format:**
```
STRUCTURAL VALIDATION: ✓ Pass
  All required sections and fields present

ADVISORY HEURISTICS: ⚠ N warnings
  ⚠ <warning 1>
  ⚠ <warning 2>

Note: This tool checks format, not content quality.
A valid checkpoint may still be insufficient for work resumption.
```

### Layer 2: Semantic (LLM in SKILL.md)

Semantic validation happens at runtime during checkpoint creation, guided by documentation in SKILL.md. This is NOT AI-powered analysis (which is out of scope)—it is self-check guidance that the LLM follows when creating checkpoints.

**Self-check guidance (embedded in SKILL.md):**

Before finalizing any checkpoint, the LLM should consider:

1. **Problem Clarity**: Can someone with zero context understand the problem from this description alone?
2. **Decision Rationale**: Does each decision explain WHY, not just WHAT was chosen?
3. **State Specificity**: Is Current State concrete enough that you could resume right now?
4. **Action Actionability**: Are Next Actions specific tasks, not vague directions?
5. **Fresh Agent Test**: Could a different agent continue this work from only this checkpoint?

This guidance shapes checkpoint quality during creation, complementing the post-hoc format checking.

## Implementation

### Step 1: Rename validate.py → format-check.py

```bash
git mv tools/validate.py tools/format-check.py
```

Update any references in:
- SKILL.md
- AGENTS.md
- README.md (if exists)

### Step 2: Add advisory heuristics to format-check.py

Add heuristic checking functions (these produce warnings, not errors):

```python
from datetime import datetime, timedelta

def check_advisory_heuristics(content: dict, frontmatter: dict) -> list[str]:
    """Return list of warning messages for potential quality issues."""
    warnings = []

    # Problem length check
    problem = content.get('problem', '')
    if len(problem.split()) < 20:
        warnings.append("Problem statement may be too brief for standalone understanding")

    # Decisions count check
    decisions = content.get('decisions', [])
    if len(decisions) < 2:
        warnings.append("Few decisions recorded—are key choices captured?")

    # Play-By-Play check
    play_by_play = content.get('play_by_play', [])
    if len(play_by_play) < 2:
        warnings.append("Limited history—is progression clear?")

    # Artifact Trail check
    artifacts = content.get('artifact_trail', [])
    if not artifacts:
        warnings.append("No artifacts tracked—is this intentional?")

    # Next Actions check
    next_actions = content.get('next_actions', [])
    if not next_actions:
        warnings.append("Next actions may not be actionable")

    # Current State check
    current_state = content.get('current_state', '')
    if len(current_state.split()) < 30:
        warnings.append("Current state may lack sufficient detail")

    # Recency checks
    now = datetime.now()

    # Checkpoint age check
    created = frontmatter.get('created')
    if created:
        created_date = datetime.fromisoformat(created.replace('Z', '+00:00'))
        if (now - created_date.replace(tzinfo=None)) > timedelta(days=7):
            warnings.append("Checkpoint may be stale—is it still current?")

    # Last delta recency check
    last_delta = frontmatter.get('last_delta')
    if last_delta:
        delta_date = datetime.fromisoformat(last_delta.replace('Z', '+00:00'))
        if (now - delta_date.replace(tzinfo=None)) > timedelta(days=3):
            warnings.append("No recent updates—is the checkpoint still accurate?")

    return warnings
```

### Step 3: Update output format

Change output from:
```
✓ Valid checkpoint
```

To:
```
STRUCTURAL VALIDATION: ✓ Pass
  All required sections and fields present

ADVISORY HEURISTICS: ⚠ 2 warnings
  ⚠ Play-By-Play has only 1 entry—is progression captured?
  ⚠ Checkpoint may be stale—is it still current?

Note: This tool checks format, not content quality.
A valid checkpoint may still be insufficient for work resumption.
```

### Step 4: Add semantic self-check guidance to SKILL.md

Add new section to SKILL.md providing guidance (not automated analysis) for the LLM to follow during checkpoint creation:

```markdown
## Semantic Quality Self-Check

Before finalizing any checkpoint, consider these questions:

1. **Problem Clarity**: Can someone with zero context understand the problem from this description alone?
2. **Decision Rationale**: Does each decision explain WHY, not just WHAT was chosen?
3. **State Specificity**: Is Current State concrete enough that you could resume right now?
4. **Action Actionability**: Are Next Actions specific tasks, not vague directions?
5. **Fresh Agent Test**: Could a different agent continue this work from only this checkpoint?

If any answer is "no", improve that section before declaring the checkpoint complete.

Note: This is guidance for checkpoint authors, not automated validation.
For external quality evaluation, see eval/rubric.md and the eval-checkpoint command.
```

### Step 5: Update references

Update these files to reference `format-check.py` instead of `validate.py`:
- `.claude/skills/coihuin-compress/SKILL.md`
- `AGENTS.md` (if applicable)
- Any other documentation mentioning validate.py

## Validation

| Check | Method | Expected |
|-------|--------|----------|
| Script renamed | `ls tools/` | format-check.py exists, validate.py doesn't |
| Heuristics work | Run on minimal checkpoint | Warnings generated |
| Heuristics advisory | Run with warnings | Exit code 0 (not failure) |
| Output format correct | Run on real checkpoint | Two-section output with disclaimer |
| SKILL.md updated | Read SKILL.md | Self-check section present |
| No broken refs | Grep for "validate.py" | Zero matches in active docs |

## References

- [ISSUE-007](ISSUE-007.md): Issue driving this change
- [ISSUE-011](../done/ISSUE-011.md): Related eval mechanism with dialectic rubric
- [eval/rubric.md](../../eval/rubric.md): Semantic quality rubric for external evaluation
- [history/2025-12-16-dialectic-audit.md](../../history/2025-12-16-dialectic-audit.md): Discussion 4 where two-layer model was decided
