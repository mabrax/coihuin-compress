---
id: ISSUE-005
title: "Address checkpoint self-containment illusion—lossy summaries need explicit coverage"
nature: enhancement
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

Checkpoints claim to be "self-contained" and "sufficient to continue work," but this is structurally impossible:

1. **Lossy extraction**: The agent generating a checkpoint uses judgment when context is rich. Later, when context is compressed, there's no guarantee the right information was captured.

2. **Context dependency**: Loading a checkpoint requires the agent to interpret it without original context. "Phase 2 complete" assumes shared understanding of what Phase 2 entailed—the checkpoint is a pointer to memory, not memory itself.

3. **No coverage verification**: There's no mechanism to verify a checkpoint actually captures recoverable state.

Checkpoints are **lossy summaries masquerading as state**. The format optimizes for looking complete rather than being recoverable.

## Scope

### In Scope

- [ ] Add explicit coverage questions to checkpoint generation workflow
- [ ] Define "recoverability test" criteria (can a fresh agent resume from this?)
- [ ] Add checkpoint quality checklist to SKILL.md
- [ ] Consider adding "self-check" section to checkpoint format
- [ ] Document the lossy nature honestly in format spec
- [ ] Add guidance for what detail level is needed per section

### Out of Scope

- Automated recoverability testing (would require multi-agent simulation)
- Fundamental format redesign
- Adding computational verification

## Acceptance Criteria

- [ ] Checkpoint format acknowledges lossy nature
- [ ] Generation workflow includes coverage verification step
- [ ] Explicit guidance on detail level for recoverability
- [ ] Users understand checkpoints require human verification
- [ ] Quality checklist available during checkpoint creation

## Notes

### Proposed Coverage Questions

Before finalizing a checkpoint, answer:

1. **What**: Could a fresh agent understand the problem from this?
2. **Why**: Are the key decisions and their rationale captured?
3. **How**: Is there enough technical context to continue implementation?
4. **What's next**: Are next actions specific enough to act on?
5. **Test**: If I deleted the conversation and loaded only this checkpoint, could I continue?

### Proposed Checkpoint Self-Check Section

```markdown
## Self-Check
- [ ] Problem statement is complete without conversation context
- [ ] Decisions include rationale, not just choices
- [ ] Technical context sufficient for implementation
- [ ] Current state describes what exists, not what was done
- [ ] Next actions are actionable without prior context
```

### Audit Origin

Dialectic audit tension #2: Checkpoint vs Context—Who Owns Truth?

### Severity

High—core value proposition depends on recoverability

---

## Reframing (2025-12-16)

**Discussion outcome**: The checkpoint format structure already covers the proposed questions:

| Question | Covered By |
|----------|------------|
| What | `## Problem` + `## Session Intent` |
| Why | `### Decisions` |
| How | `### Technical Context` + `### Artifact Trail` + `### Play-By-Play` |
| What's next | `### Current State` + `### Next Actions` |

The audit's criticism was misdirected at structure when the real issue is **quality verification**.

**New approach**: Instead of adding more prescription to the format, implement an eval mechanism (ISSUE-011) that:
- Collects real checkpoints from dogfooding
- Evaluates them with LLM-as-judge + rubric
- Promotes good examples to improve the skill

This addresses quality through evaluation of real outputs, not more rules.

**Status**: Scope items may be partially or fully superseded by ISSUE-011. Review after ISSUE-011 implementation.

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 2
