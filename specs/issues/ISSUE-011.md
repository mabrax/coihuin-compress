---
id: ISSUE-011
title: "Implement eval mechanism for checkpoint quality (dogfooding + LLM-as-judge)"
nature: feature
impact: additive
version: minor
status: draft
created: 2025-12-16
updated: 2025-12-16

context:
  required: []
  recommended: []

depends_on: []
blocks: []
---

## Problem

How do we know checkpoints are "good enough" for recoverability? The current approach relies on:
- Structural validation (format checker)
- Human judgment at creation time

Neither provides systematic quality assurance. Synthetic examples show happy paths but don't represent real messy work.

## Proposed Solution

Create a **dogfooding + evaluation pipeline** that:
1. Collects real checkpoints from actual project work
2. Evaluates them using LLM-as-judge with a rubric
3. Promotes high-quality examples to feed back into the skill

```
Real work (using the skill)
    │
    ▼
Checkpoints created in actual projects
    │
    ▼
Copy promising checkpoints to eval/ folder
    │
    ▼
LLM-as-judge with rubric scores them
    │
    ▼
High-scoring checkpoints → examples/
    │
    ▼
Examples feed back into skill improvement
```

## Scope

### In Scope

- [ ] Design evaluation rubric for checkpoint quality
- [ ] Define rubric dimensions (recoverability, completeness, clarity, token efficiency)
- [ ] Create eval/ directory structure
- [ ] Implement eval command or script (LLM-as-judge)
- [ ] Define scoring thresholds for "good" checkpoints
- [ ] Document the dogfooding workflow
- [ ] Create process for promoting examples

### Out of Scope

- Automatic checkpoint collection from other projects
- Real-time evaluation during checkpoint creation
- Integration with external eval frameworks

## Acceptance Criteria

- [ ] Evaluation rubric documented with clear dimensions and criteria
- [ ] eval/ directory structure defined
- [ ] Eval script/command functional (can score a checkpoint)
- [ ] At least one real checkpoint evaluated as proof of concept
- [ ] Workflow documented for collecting → evaluating → promoting examples

## Notes

### Proposed Rubric Dimensions

| Dimension | What it measures |
|-----------|-----------------|
| **Recoverability** | Could a fresh agent resume work from this alone? |
| **Completeness** | Are all required sections meaningfully filled? |
| **Clarity** | Is the language unambiguous without prior context? |
| **Token Efficiency** | Is information dense without unnecessary verbosity? |
| **Actionability** | Are Next Actions specific enough to execute? |

### Proposed Directory Structure

```
eval/
├── inbox/           # Checkpoints to evaluate
├── scored/          # Evaluated checkpoints with scores
└── rubric.md        # The evaluation rubric
```

### Why This Approach

The solution to "how do we know checkpoints are good enough?" isn't more prescription—it's evaluation of real outputs. Benefits:

1. **Real over synthetic**: Examples from actual messy work
2. **Quality through evaluation**: Rubric-based selection, not gut feeling
3. **Natural edge case discovery**: Real work includes failures, pivots
4. **Continuous improvement**: Skill improves through use
5. **Self-documenting**: Good checkpoints demonstrate what works

### Audit Origin

Emerged from Discussion 2 in dialectic audit (Tension 2 resolution).

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 2
