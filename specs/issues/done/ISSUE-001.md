---
id: ISSUE-001
title: "Research context compression problem space for Claude Code skill"
nature: feature
impact: invisible
version: patch
status: done
created: 2025-12-14
updated: 2025-12-14

context:
  required: []
  recommended:
    - specs/checkpoint-format.md
    - specs/delta-format.md

depends_on: []
blocks:
  - ISSUE-002
---

## Problem

During long Claude Code sessions, critical work state is lost when context summarization occurs. This manifests as:

1. **Lost context mid-session**: Important decisions, file locations, and work progress disappear after automatic summarization
2. **Repeated explanations**: Users must re-explain the same context multiple times within a single session
3. **Large codebase navigation**: Difficulty tracking what has been explored, what was decided, and what remains to be done

A proactive context compression skill could preserve essential state with minimal token overhead, allowing seamless continuation of work even after context resets.

## Scope

### In Scope

- [x] ~~Research how Claude Code handles context summarization~~ (N/A - proactive approach replaces reactive summarization)
- [x] Identify what information is most critical to preserve
- [x] Analyze the example checkpoint/delta format in `docs/examples/`
- [x] Define categories of compressible information (decisions, file state, progress, blockers)
- [x] Determine optimal checkpoint frequency/triggers
- [x] Document information priority hierarchy (must-keep vs nice-to-have vs droppable)
- [x] Research existing compression/summarization approaches

### Out of Scope

- Implementation of the skill itself (separate issue)
- Integration with external tools or APIs
- Performance benchmarking (will be done during implementation)

## Acceptance Criteria

- [x] Problem statement document created with clear definition of the problem
- [x] Information taxonomy defined (what types of state need preservation)
- [x] Checkpoint format specification drafted → `specs/checkpoint-format.md`
- [x] Delta format specification drafted → `specs/delta-format.md`
- [x] Trigger conditions documented (when to compress)
- [x] Priority hierarchy established (what to keep vs. drop under pressure)
- [x] Ready to proceed to skill design issue

## Notes

### Key Questions to Answer

1. What does Claude Code's automatic summarization preserve/lose?
2. What's the minimal checkpoint that allows work resumption?
3. How do checkpoints and deltas interact (full snapshot vs incremental)?
4. Should compression be user-triggered, automatic, or both?
5. What's the target token reduction ratio?

### Reference Materials

- Example checkpoints: `docs/examples/chk-*.md`
- Example deltas: `docs/examples/delta-*.md`
- ReSum paper: [arxiv.org/pdf/2509.13313](https://arxiv.org/pdf/2509.13313) - Context Summarization for Long-Horizon Search
- Factory.ai: [factory.ai/news/compressing-context](https://factory.ai/news/compressing-context) - What Must Survive categories, incremental updates, breadcrumbs
