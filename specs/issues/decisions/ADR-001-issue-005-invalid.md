# ADR-001: ISSUE-005 Marked Invalid

**Date**: 2025-12-17
**Status**: Accepted
**Supersedes**: ISSUE-005 (Address checkpoint self-containment illusion)

## Context

ISSUE-005 raised concerns about checkpoints being "lossy summaries masquerading as state" and proposed adding coverage questions, recoverability tests, and quality checklists to the checkpoint format.

## Decision

ISSUE-005 is invalid and has been deleted.

### Rationale

1. **Format already covers the concerns**: The checkpoint format structure already addresses the proposed coverage questions:
   - What → `## Problem` + `## Session Intent`
   - Why → `### Decisions`
   - How → `### Technical Context` + `### Artifact Trail` + `### Play-By-Play`
   - What's next → `### Current State` + `### Next Actions`

2. **Misdirected criticism**: The audit's criticism targeted structure when the real issue was quality verification of actual outputs.

3. **Superseded by ISSUE-011**: The eval mechanism approach (collecting real checkpoints, LLM-as-judge evaluation, promoting good examples) addresses quality through evaluation rather than more prescriptive rules.

4. **Adding more prescription is counterproductive**: More format rules don't improve quality—evaluation of real outputs does.

## Consequences

- ISSUE-005 removed from active issues
- Quality verification delegated to ISSUE-011 (eval mechanism)
- No changes to checkpoint format structure
- Acknowledge that checkpoints are inherently lossy—this is a feature, not a bug (compression requires information loss)

## References

- `history/2025-12-16-dialectic-audit.md`, Appendix A, Discussion 2
- ISSUE-011: Eval mechanism for checkpoint quality
