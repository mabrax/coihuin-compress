---
id: spec-002
title: Breadcrumbs Format Specification
issue: ISSUE-002
version: 1.0.0
created: 2025-12-17
---

# Breadcrumbs Format Specification

## Overview

**Breadcrumbs** are minimal references (pointers, not content) that allow an agent to reconstruct context that was compressed away from a checkpoint. They tell the agent *where to look* rather than *what was there*.

## Design Principles

1. **Pointers, not content**: Breadcrumbs reference information; they don't duplicate it
2. **Token-efficient**: A breadcrumb costs ~10-20 tokens vs hundreds/thousands for full content
3. **Agent autonomy**: Agent decides when to follow a breadcrumb based on need
4. **No validation**: Stale breadcrumbs are acceptable; cleanup happens via normal merge workflow

## Design Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| Token budget | No hard limit | Breadcrumbs are cheap (~10-20 tokens). 50+ signals checkpoint design problem, not breadcrumb problem |
| Priority levels | None for v1 | Breadcrumbs are already the compressed form. Add if real usage shows need |
| Follow decision | Agent autonomy | Agent follows when needed, ignores when not. No rigid rules |
| Validation | None | Stale breadcrumbs cleaned up during merge. Transient staleness is fine |

## Structure

Breadcrumbs appear as a section within a checkpoint:

```markdown
### Breadcrumbs
[Minimal references for context reconstruction]

| Type | Reference | Hint |
|------|-----------|------|
| file | `path/to/file.ts` | What this file contains/does |
| function | `module.functionName()` | What this function does |
| decision | Phase N, context | Why this decision was made |
| external | URL or identifier | What this resource provides |
```

## Breadcrumb Categories

### 1. File Breadcrumbs

Reference to a file in the codebase.

| Field | Example | Purpose |
|-------|---------|---------|
| Type | `file` | Category identifier |
| Reference | `src/services/gemini.ts` | File path (relative to project root) |
| Hint | Gemini API client with retry logic | What the file contains |

**When to create**: When a file is mentioned in play-by-play or artifact trail but full implementation details are compressed.

**Reconstruction**: Agent reads the file using standard file tools.

### 2. Function Breadcrumbs

Reference to a specific function or method.

| Field | Example | Purpose |
|-------|---------|---------|
| Type | `function` | Category identifier |
| Reference | `colorQuantizer.quantize()` | Fully qualified function name |
| Hint | K-means clustering for color reduction | What the function does |

**When to create**: When algorithm details or implementation logic is compressed away but may be needed.

**Reconstruction**: Agent reads the file containing the function, searches for the function definition.

### 3. Decision Breadcrumbs

Reference to a decision made during the session.

| Field | Example | Purpose |
|-------|---------|---------|
| Type | `decision` | Category identifier |
| Reference | Phase 2, exponential backoff | Decision identifier and topic |
| Hint | Why we chose exponential over linear backoff | What rationale exists |

**When to create**: When the *reasoning* behind a decision is compressed, but the decision itself is kept.

**Reconstruction**: If the original conversation is unavailable, the hint provides enough context. If more detail is needed, agent may ask user (rare case).

### 4. External Breadcrumbs

Reference to external resources (papers, docs, URLs).

| Field | Example | Purpose |
|-------|---------|---------|
| Type | `external` | Category identifier |
| Reference | `arxiv:2509.13313` | URL, DOI, or identifier |
| Hint | ReSum paper on context summarization | What the resource covers |

**When to create**: When external research or documentation informed decisions but full content isn't stored.

**Reconstruction**: Agent fetches the URL or searches for the resource.

## Integration with Checkpoint Format

Breadcrumbs section is **optional** and appears within `## Essential Information`:

```markdown
## Essential Information

### Decisions
...

### Technical Context
...

### Breadcrumbs
| Type | Reference | Hint |
|------|-----------|------|
| file | `src/services/gemini.ts` | Gemini API client with retry logic |
| decision | Phase 2, retry strategy | Why exponential backoff over linear |
| external | https://factory.ai/news/compressing-context | Factory.ai compression article |

### Play-By-Play
...
```

## Breadcrumb Lifecycle

### Creation

Breadcrumbs are created when:
1. **Compression occurs**: Information is being pruned but a reference would help recovery
2. **External reference**: A resource informed the work but isn't embedded
3. **Implementation detail**: Code exists but details aren't in the checkpoint

### Maintenance

During merge operations:
- New breadcrumbs are added for newly compressed content
- Breadcrumbs for information now in the checkpoint can be removed
- Stale breadcrumbs are cleaned up opportunistically (not required)

### No explicit pruning rules

Breadcrumbs are cheap. If a checkpoint has too many, that's a signal to restructure the checkpoint, not to prune breadcrumbs.

## Reconstruction Protocol

When an agent needs context referenced by a breadcrumb:

```
1. Agent encounters need for more context
2. Agent checks Breadcrumbs section
3. Agent finds relevant breadcrumb
4. Agent follows reference:
   - file → Read file
   - function → Read file, find function
   - decision → Use hint, or ask user if insufficient
   - external → Fetch URL or search
5. Agent continues with recovered context
```

**Key principle**: The agent decides when to follow. Breadcrumbs are *available*, not *mandatory*.

## Stale Breadcrumb Handling

When a breadcrumb reference no longer exists (file deleted, URL dead):

1. Agent attempts reconstruction
2. Reconstruction fails
3. Agent continues without that context
4. Breadcrumb remains in checkpoint (may be cleaned up at next merge)

**No automatic deletion**: Staleness may be transient (different branch, temporarily moved file). Normal merge workflow handles cleanup.

## Example

```markdown
### Breadcrumbs
| Type | Reference | Hint |
|------|-----------|------|
| file | `src/services/gemini.ts` | Gemini API client with exponential backoff |
| file | `src/lib/colorQuantizer.ts` | K-means color quantization algorithm |
| function | `imageProcessor.convertToRegions()` | Converts quantized image to paintable regions |
| decision | Phase 1, color algorithm | Why K-means over median cut (speed vs accuracy tradeoff) |
| external | arxiv:2509.13313 | ReSum paper - context summarization patterns |
| external | https://factory.ai/news/compressing-context | Factory.ai - What Must Survive categories |
```

## Token Economics

| Item | Approximate Tokens |
|------|-------------------|
| One breadcrumb row | 10-20 tokens |
| 10 breadcrumbs | 100-200 tokens |
| Full file content | 500-5000 tokens |

**Break-even**: ~25-250 breadcrumbs equals one file read. In practice, checkpoints have 5-15 breadcrumbs.

## References

- Factory.ai: "Compressing Context" - Breadcrumbs concept origin
- specs/checkpoint-format.md: Checkpoint structure (breadcrumbs integrate here)
