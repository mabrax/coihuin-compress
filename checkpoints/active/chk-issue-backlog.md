---
checkpoint: chk-issue-backlog
created: 2025-12-17T15:21:36Z
anchor: post-dialectic-cleanup
last_delta: 2025-12-17T18:40:14Z
---

## Problem

After the dialectic audit, coihuin-compress has active issues that need implementation. These represent refinements and enhancements identified through critical self-examination of the skill.

## Session Intent

Track and implement the remaining issues from the dialectic audit to mature the coihuin-compress skill. Each issue has been discussed and either resolved (clear path forward), reframed (understanding shifted), or superseded by other work.

## Essential Information

### Decisions

- **ISSUE-005 invalidated**: Checkpoint self-containment concern was misdirected at structure; real issue is quality verification (handled by ISSUE-011)
- **ADR-001 created**: Documents why ISSUE-005 was invalidated—establishes precedent for issue invalidation decisions
- **Delta = intelligent merge**: Delta command/logic is valuable; delta artifact files are optional since Git provides history
- **Two-layer validation**: Structural (format-check.py) + Semantic (LLM in-skill)
- **Warnings not automation**: Proactive triggers should be advisory, user decides
- **Archive marker file**: Use `.claudeignore` to prevent Claude loading stale checkpoints
- **Dialectic evaluation model**: Human interview (5 questions) → Agent investigation (3 parallel tasks) → Correlation & synthesis
- **Senior implementers for phases**: Used swarm of senior-implementer agents for parallel phase execution
- **Delta-as-operation model**: Based on real-world usage, simplify from 3 concepts (checkpoint, delta artifact, merge) to 2 operations (checkpoint, delta). "Delta" becomes a verb meaning "update checkpoint with what changed"

### Technical Context

- Project: coihuin-compress (Claude Code skill)
- Location: `/Users/mabrax/Documents/Projects/coihuin-compress`
- Spec format: YAML frontmatter + markdown body (cspec style)
- Issue tracking: `specs/issues/active/` and `specs/issues/done/`

### Play-By-Play

- Dialectic audit → Generated ISSUE-004 through ISSUE-012 → Complete
- Post-audit → ISSUE-004, ISSUE-009 closed during discussions → Complete
- 2025-12-17 → ISSUE-005 invalidated, ADR-001 created, DEPENDENCIES.md updated → Complete
- 2025-12-17 → ISSUE-011 spec created and reviewed (spec-011.md) → Complete
- 2025-12-17 → ISSUE-011 implemented via 4-phase plan with senior implementers → Complete
- 2025-12-17 → ISSUE-006 reframed based on real-world usage feedback → Complete
- 2025-12-17 → spec-006.md created, validated against issue → Complete
- 2025-12-17 → TASKS-006.md created, validated against spec, fixes applied → Complete

### Artifact Trail

| File | Status | Key Change |
|------|--------|------------|
| `specs/issues/active/ISSUE-006.md` | modified | Reframed: "Simplify to delta-as-operation model", status=ready |
| `specs/issues/active/spec-006.md` | created | Full specification for delta-as-operation model |
| `specs/issues/active/TASKS-006.md` | created | 4-phase implementation plan with validation hooks |

### Breadcrumbs

| Type | Reference | Hint |
|------|-----------|------|
| file | `specs/issues/active/spec-006.md` | Delta-as-operation specification |
| file | `specs/issues/active/TASKS-006.md` | Implementation plan for ISSUE-006 |
| file | `eval/rubric.md` | Canonical scoring rubric |
| file | `.claude/commands/eval-checkpoint.md` | Full dialectic eval command |
| file | `.claude/skills/coihuin-compress/SKILL.md:121-172` | Checkpoint Evaluation section |

### Current State

**4 active issues remaining:**

| Issue | Title | Status |
|-------|-------|--------|
| ISSUE-006 | Simplify to delta-as-operation model | Ready (spec + tasks complete) |
| ISSUE-007 | Validation layers | Draft |
| ISSUE-008 | Cognitive load / warnings | Draft |
| ISSUE-010 | Archive lifecycle | Draft |
| ISSUE-012 | Clean up format spec | Draft |

**Done issues:** ISSUE-001, 002, 003, 004, 009, 011
**Invalid issues:** ISSUE-005 (see ADR-001)

### Next Actions

1. **Implement ISSUE-006** - Execute TASKS-006.md (4 phases: delete delta files, update SKILL.md, update checkpoint-format.md, validate)
2. **Implement ISSUE-012** (Format spec cleanup)—quick win, low risk
3. **Implement ISSUE-007** (Validation rename + LLM semantic checks)
4. **Implement ISSUE-008** (Warning guidance in SKILL.md)
5. **Implement ISSUE-010** (Add .claudeignore to archive/)

## User Rules

- Never commit without explicit approval
- No time estimates in plans
- Check date with `date` command for date-related tasks

---

## Delta: 2025-12-17T18:40:14Z

### What Changed

**ISSUE-006 fully specified and ready for implementation** based on user's real-world feedback from using the skill.

### Key Insight

User reported: "I always say do not write the delta and only add it." This revealed that the three-concept model (checkpoint, delta artifact, merge) was overcomplicated. The new model has two operations:
- `checkpoint` = create fresh snapshot
- `delta` = update existing checkpoint with what changed

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `specs/issues/active/ISSUE-006.md` | modified | Reframed title and scope to delta-as-operation model |
| `specs/issues/active/spec-006.md` | created | Full spec with design decisions, removals, SKILL.md changes, implementation steps |
| `specs/issues/active/TASKS-006.md` | created | 4-phase plan: delete files, update SKILL.md, update checkpoint-format, validate |

### Validations Performed

1. **spec vs issue**: 5/5 scope items PASS, 5/5 acceptance criteria PASS
2. **tasks vs spec**: 100% coverage, correct order, all files listed, 3 minor fixes applied

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| ISSUE-006 | Draft | Ready (spec + tasks complete) |
| Active issues | 5 | 4 (ISSUE-006 ready to implement) |
