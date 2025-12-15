---
id: ISSUE-002
title: "Add breadcrumbs system for context reconstruction"
nature: feature
impact: additive
version: minor
status: ready
created: 2025-12-14
updated: 2025-12-14

context:
  required:
    - specs/checkpoint-format.md
    - specs/delta-format.md
  recommended:
    - docs/examples/chk-*.md

depends_on:
  - ISSUE-001
blocks: []
---

## Problem

Checkpoints compress context aggressively to save tokens, but sometimes the agent needs to recover full details that were pruned. Currently, if critical information was compressed away, the agent must either:

1. Ask the user to re-explain (poor UX)
2. Search blindly through the codebase (inefficient)
3. Fail to continue properly (broken workflow)

**Breadcrumbs** solve this by storing minimal references (not full content) that allow the agent to reconstruct context on-demand.

## Concept

From Factory.ai's "Compressing Context":

> **Breadcrumbs**: References for reconstructing context for truncated artifacts. File paths, function names, and key identifiers, which the agent can query to re-access outputs from previous actions.

Breadcrumbs are **pointers, not content**. They tell the agent *where to look* rather than *what was there*.

## Scope

### In Scope

- [ ] Define breadcrumb data structure (what a breadcrumb contains)
- [ ] Define breadcrumb categories (files, decisions, actions, external refs)
- [ ] Specify how breadcrumbs integrate with checkpoint format
- [ ] Specify breadcrumb lifecycle (when created, when pruned)
- [ ] Define reconstruction protocol (how agent uses breadcrumbs to fetch context)
- [ ] Add breadcrumbs section to checkpoint format spec

### Out of Scope

- Automatic breadcrumb generation (implementation detail)
- Integration with specific tools (MCP, file readers, etc.)
- Breadcrumb storage outside checkpoints

## Acceptance Criteria

- [ ] Breadcrumb format specification documented
- [ ] Integration with checkpoint-format.md complete
- [ ] At least 3 breadcrumb categories defined with examples
- [ ] Reconstruction protocol documented
- [ ] Example checkpoint with breadcrumbs section created

## Proposed Structure

```markdown
### Breadcrumbs
[Minimal references for context reconstruction]

| Type | Reference | Reconstruction Hint |
|------|-----------|---------------------|
| file | `src/services/gemini.ts` | Gemini API client implementation |
| decision | Phase 2, Turn 47 | Why we chose exponential backoff |
| function | `colorQuantizer.quantize()` | K-means clustering algorithm |
| external | arxiv:2509.13313 | ReSum paper on context summarization |
```

## Notes

### Key Questions

1. How many breadcrumbs before they become as expensive as full context?
2. Should breadcrumbs have priority levels (always keep vs. can prune)?
3. How does the agent decide when to follow a breadcrumb vs. continue without?
4. Should breadcrumbs be validated (check if reference still exists)?

### Design Constraints

- Breadcrumbs must be cheaper than storing full content
- Reconstruction must be possible without user intervention
- Format must be human-readable for debugging

### References

- Factory.ai: "Compressing Context" - Breadcrumbs concept
- specs/checkpoint-format.md - Current checkpoint structure
- specs/delta-format.md - Delta/incremental update structure
