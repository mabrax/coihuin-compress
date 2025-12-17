---
id: ISSUE-002
title: "Add breadcrumbs system for context reconstruction"
nature: feature
impact: additive
version: minor
status: ready
created: 2025-12-14
updated: 2025-12-17

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

- [x] Define breadcrumb data structure (what a breadcrumb contains)
- [x] Define breadcrumb categories (files, decisions, actions, external refs)
- [x] Specify how breadcrumbs integrate with checkpoint format
- [x] Specify breadcrumb lifecycle (when created, when pruned)
- [x] Define reconstruction protocol (how agent uses breadcrumbs to fetch context)
- [ ] Add breadcrumbs section to checkpoint format spec

### Out of Scope

- Automatic breadcrumb generation (implementation detail)
- Integration with specific tools (MCP, file readers, etc.)
- Breadcrumb storage outside checkpoints

## Acceptance Criteria

- [x] Breadcrumb format specification documented (spec-002)
- [ ] Integration with checkpoint-format.md complete
- [x] At least 3 breadcrumb categories defined with examples (file, function, decision, external)
- [x] Reconstruction protocol documented
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

### Key Questions (Resolved 2025-12-17)

1. **How many breadcrumbs before they become as expensive as full context?**
   - **Answer**: No hard limit. Breadcrumbs cost ~10-20 tokens each; 50+ signals checkpoint design problem, not breadcrumb problem.

2. **Should breadcrumbs have priority levels (always keep vs. can prune)?**
   - **Answer**: No, not for v1. Breadcrumbs are already the compressed form. Add if real usage shows need.

3. **How does the agent decide when to follow a breadcrumb vs. continue without?**
   - **Answer**: Agent autonomy. Agent follows when needed, ignores when not. No rigid rules.

4. **Should breadcrumbs be validated (check if reference still exists)?**
   - **Answer**: No. Stale breadcrumbs are acceptable; cleanup happens via normal merge workflow. Staleness may be transient.

### Design Constraints

- Breadcrumbs must be cheaper than storing full content
- Reconstruction must be possible without user intervention
- Format must be human-readable for debugging

### References

- Factory.ai: "Compressing Context" - Breadcrumbs concept
- specs/checkpoint-format.md - Current checkpoint structure
- specs/delta-format.md - Delta/incremental update structure
- **spec-002** - Breadcrumbs format specification (created 2025-12-17)
