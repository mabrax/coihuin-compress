---
id: ISSUE-007
title: "Enhance validation with semantic heuristics—structure isn't enough"
nature: enhancement
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

The `validate.py` script checks structural correctness:
- Frontmatter fields exist
- Required sections exist
- Keywords present

It **cannot check semantic correctness**:
- Is the "Problem" statement actually the problem?
- Are the "Decisions" actually the decisions that matter?
- Is "Current State" accurate?
- Will "Next Actions" make sense in a fresh context?

A passing validation means "this looks like a checkpoint" not "this will work as a checkpoint."

This creates **false confidence**. Users see "Valid checkpoint" and assume quality, but the validator is blind to semantic drift—checkpoints that technically pass but fail to preserve recoverable state.

## Scope

### In Scope

- [x] Add semantic heuristic warnings (not errors) to validate.py
- [x] Implement minimum content checks per section
- [x] Add recency/completeness indicators
- [x] Rename output to clarify what's being validated
- [x] Add "semantic quality" vs "structural validity" distinction
- [x] Consider adding interactive quality prompts

### Out of Scope

- AI-powered semantic analysis
- Full recoverability testing
- Breaking changes to validation API

## Acceptance Criteria

- [x] Validator distinguishes structural validity from semantic quality
- [x] Heuristic warnings for potentially weak checkpoints
- [x] Users understand what passing validation means (and doesn't mean)
- [x] Output clearly labels checks as "structural" vs "heuristic"
- [x] No false confidence from passing validation

## Notes

### Proposed Semantic Heuristics

**For Checkpoints:**

| Check | Warning Trigger |
|-------|-----------------|
| Problem length | < 20 words → "Problem statement may be too brief for standalone understanding" |
| Decisions count | < 2 entries → "Few decisions recorded—are key choices captured?" |
| Play-By-Play entries | < 2 entries → "Limited history—is progression clear?" |
| Artifact Trail | Empty → "No artifacts tracked—is this intentional?" |
| Next Actions | Empty or 1 vague item → "Next actions may not be actionable" |
| Current State | < 30 words → "Current state may lack sufficient detail" |

**For Deltas:**

| Check | Warning Trigger |
|-------|-----------------|
| Changes sections | All empty → "No changes documented" |
| Summary length | < 10 words → "Summary may be too brief" |

### Output Reframing

**Current output:**
```
✓ Valid checkpoint
```

**Proposed output:**
```
STRUCTURAL VALIDATION: ✓ Pass
  All required sections and fields present

SEMANTIC HEURISTICS: ⚠ 2 warnings
  ⚠ Play-By-Play has only 1 entry—is progression captured?
  ⚠ Current State is brief (18 words)—sufficient for resumption?

Note: Structural validation checks format, not content quality.
A valid checkpoint may still be insufficient for work resumption.
```

### Audit Origin

Dialectic audit tension #4: Validation vs Semantic Correctness

### Severity

High—false confidence undermines skill reliability

---

## Resolution (2025-12-16)

**Discussion outcome**: Accept the tension. Implement two-layer validation.

### Two Validation Layers

| Layer | Tool | What it checks |
|-------|------|----------------|
| **Structural** | `validate.py` → `format-check.py` | Fields, sections, syntax |
| **Semantic** | LLM in-skill | Meaning, recoverability, drift |

### Revised Actions

1. **Rename script**: `validate.py` → `format-check.py` (honest naming)
2. **Add LLM semantic checks**: In SKILL.md, add self-check guidance during checkpoint creation
3. **Eval mechanism**: ISSUE-011 provides external semantic validation via rubric

### Semantic Validation (LLM Self-Check)

During checkpoint creation, the LLM should verify:
- Problem statement understandable without prior context?
- Decisions meaningful with rationale?
- Current State specific enough to resume?
- Next Actions actionable?
- Fresh agent could continue from this?

**Insight**: Structural and semantic validation are different concerns. A format checker should not pretend to do semantic validation.

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 4
