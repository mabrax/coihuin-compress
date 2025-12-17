---
id: ISSUE-004
title: "Reframe 'proactive' positioning—skill is passive, not proactive"
nature: enhancement
impact: invisible
version: patch
status: done
created: 2025-12-16
updated: 2025-12-16

context:
  required: []
  recommended: []

depends_on: []
blocks: []
---

## Problem

The skill is described as "proactive context compression" but the actual workflow is entirely **reactive to user commands**:

- User must manually recognize when to checkpoint
- User must manually trigger "checkpoint", "delta", or "merge"
- User must manually load checkpoints into context

There is no proactive mechanism—no signal when context is growing, no automatic suggestion to compress. The skill waits passively for user invocation.

This creates a gap between marketing and reality that undermines trust.

## Scope

### In Scope

- [ ] Audit all skill documentation for "proactive" claims
- [ ] Decide: rename skill OR add actual proactive features
- [ ] If rename: update SKILL.md description, README, AGENTS.md
- [ ] If proactive features: design trigger mechanism (see ISSUE-008)
- [ ] Update skill trigger phrases to match actual behavior

### Out of Scope

- Implementing proactive triggers (separate issue ISSUE-008)
- Fundamental skill redesign

## Acceptance Criteria

- [ ] Skill description accurately reflects actual behavior
- [ ] No false claims about "proactive" behavior unless implemented
- [ ] User expectations match skill capabilities
- [ ] Documentation internally consistent

## Notes

### Options

**Option A: Rename/Reframe**
- Change "proactive context compression" to "structured context compression" or "context compression protocol"
- Honest about what it is: a format specification with manual triggers

**Option B: Keep Name, Add Proactive Features**
- Implement ISSUE-008 first (proactive triggers)
- Then the name becomes accurate

### Audit Origin

Dialectic audit tension #1: "Proactive" vs Actual Workflow

### Severity

Medium—misleading but not broken

---

## Resolution

**Status**: Closed as invalid (2025-12-16)

**Reason**: The audit's criticism conflated two meanings of "proactive":
1. Proactive philosophy (compress before forced, at natural breakpoints)
2. Proactive mechanism (system automatically triggers)

The skill implements (1), which is the design intent. "Proactive" accurately describes *when* compression happens (before forced, by conscious choice) even though it's manually triggered.

**Actions Taken**:
- Added clarification to SKILL.md explaining the philosophical meaning of "proactive"
- ISSUE-008 (proactive triggers) remains valid as an enhancement

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 1
