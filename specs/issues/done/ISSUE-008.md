---
id: ISSUE-008
title: "Reduce cognitive load—add proactive compression triggers"
nature: feature
impact: additive
version: minor
status: done
created: 2025-12-16
updated: 2025-12-17

context:
  required: []
  recommended: []

depends_on: []
blocks: []
---

## Problem

The current design pushes significant cognitive burden onto the user:

- Remember to checkpoint before context fills
- Remember to load checkpoint at session start
- Remember the checkpoint naming convention
- Decide between checkpoint/delta/merge
- Verify checkpoint quality manually

For long sessions where cognitive load is already high, adding meta-cognitive overhead ("should I compress now?") creates friction that prevents actual use.

The skill optimizes for **agent simplicity** at the cost of **user complexity**. A skill that "just works" would be more valuable than one requiring users to manage the compression protocol.

## Scope

### In Scope

- [ ] Design proactive trigger mechanism
- [ ] Identify natural checkpoint moments (phase completion, major decision, etc.)
- [ ] Add skill guidance for when to suggest checkpointing
- [ ] Consider context-size awareness (if technically feasible)
- [ ] Add "checkpoint reminder" guidance to SKILL.md
- [ ] Document trigger conditions clearly

### Out of Scope

- Automatic checkpointing without user consent
- Integration with Claude Code internals (context size APIs)
- Full automation of compression workflow

## Acceptance Criteria

- [ ] Skill includes guidance on when to proactively suggest checkpointing
- [ ] Trigger conditions documented and clear
- [ ] User cognitive load reduced for compression timing
- [ ] Balance maintained between automation and user control
- [ ] Implementation validates "proactive" in skill name (relates to ISSUE-004)

## Notes

### Proposed Trigger Conditions

The skill should suggest checkpointing when:

1. **Phase completion**: "Phase X is complete. Would you like to create a checkpoint?"
2. **Major decision made**: "You've made a significant decision. Checkpoint to preserve it?"
3. **Extended work session**: After N major actions, suggest preservation
4. **Before risky operations**: "Before this refactor, consider checkpointing current state"
5. **Context shift**: When work direction changes substantially

### Implementation Approach

Since Claude Code skills can't access context size directly, triggers must be **heuristic-based**:

```markdown
## Proactive Triggers

After completing any of the following, consider suggesting a checkpoint:

- A phase or milestone completion
- A major architectural decision
- 5+ file modifications in sequence
- Resolving a significant blocker
- Before starting a new major task
- When user says "let's continue tomorrow" or similar
```

### Cognitive Load Reduction

Current workflow:
```
User thinks → User decides → User triggers → Skill executes
```

Proposed workflow:
```
Skill recognizes moment → Skill suggests → User approves → Skill executes
```

### Audit Origin

Dialectic audit tension #5: User Control vs Cognitive Load

### Severity

High—friction prevents adoption

---

## Resolution (2025-12-16)

**Discussion outcome**: Add warnings, not automation.

### The Middle Ground

| Approach | Status | Why |
|----------|--------|-----|
| Full automation | No | Human controls the flow (design principle) |
| No assistance | Current | Cognitive load problem |
| **Warnings/signals** | Proposed | Helps without taking control |

### Warnings Approach

- Skill suggests "consider checkpointing" at natural moments
- User decides whether to act
- No automation—just advisory signals

### Warnings as Learning Data

Warnings also serve development purposes:
- "Was this warning useful?"
- "Did I actually need to checkpoint here?"
- Helps refine what triggers are valuable
- Informs future improvements

### Revised Scope

Focus on **warnings**, not proactive triggers that automate:
1. Add warning trigger guidance to SKILL.md
2. Define what moments warrant a warning
3. Warnings are advisory—user always decides
4. Track warning usefulness over time

**Insight**: Warnings reduce cognitive load without removing human control. They also generate learning data for improving the system.

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 5

### Refinement (2025-12-17)

**Context-aware advisories**: The suggested action should adapt to session state:

| Session State | Advisory Action |
|---------------|-----------------|
| No active checkpoint | Suggest "create checkpoint" |
| Working from loaded checkpoint | Suggest "delta" (update) |

**Natural language format**: Since the skill is invoked by Claude, use conversational suggestions:

> You've completed Phase X. This is a natural checkpoint moment—would you like me to create one?

> You've made significant progress since loading the checkpoint. Would you like me to update it with a delta?

**Validation**: Research confirms this approach aligns with Claude Code skill design philosophy—advisory signals that guide without automating.
