# Checkpoint Format Specification

Version: 1.0.0

## Overview

A **checkpoint** is a point-in-time snapshot of work state optimized for token-efficient session continuation. Checkpoints follow the "What Must Survive" principle: preserve only information critical for an agent to resume work seamlessly.

## Design Principles

1. **Self-contained**: A checkpoint alone is sufficient to continue work
2. **Token-efficient**: Minimize tokens while maximizing information density
3. **Proactive**: Created at natural breakpoints, not when forced by limits
4. **Recoverable**: Any checkpoint enables seamless work resumption

## Structure

```markdown
---
checkpoint: <id>
created: <ISO-8601 timestamp>
anchor: <reference to conversation point or phase>
---

## Problem
[Stable problem statement - rarely changes between checkpoints]

## Session Intent
[What the user wants to achieve, requirements, ideal outcome]

## Essential Information

### Decisions
[User decisions that are locked in and should not be re-asked]

### Technical Context
[Stack, configuration, environment - facts that inform implementation]

### Play-By-Play
[High-level sequence of major actions completed]
- Phase/Step → Action → Outcome

### Artifact Trail
[Files created, modified, or deleted with key changes]

| File | Status | Key Change |
|------|--------|------------|
| `path/to/file` | created/modified/deleted | Brief description |

### Current State
[What exists now - completed work, current status]

### Next Actions
[What comes next - pending work, blockers]

## User Rules
[Constraints and preferences the agent must follow]
```

## Field Definitions

### Header Fields

| Field | Required | Description |
|-------|----------|-------------|
| `checkpoint` | Yes | Unique identifier (e.g., `chk-001`, `session-abc-003`) |
| `created` | Yes | ISO-8601 timestamp of checkpoint creation |
| `anchor` | No | Reference to conversation turn or phase this summarizes up to |

### Body Sections

| Section | Required | Purpose | Compression Behavior |
|---------|----------|---------|---------------------|
| Problem | Yes | Stable problem statement | Rarely changes; copy forward |
| Session Intent | Yes | User's goal and requirements | Update only when goal shifts |
| Decisions | Yes | Locked-in choices | Accumulate; never drop |
| Technical Context | Yes | Stack, env, config | Update when changes occur |
| Play-By-Play | Yes | Action history | Summarize older entries; keep recent detailed |
| Artifact Trail | Yes | Files touched | Prune completed/irrelevant; keep active |
| Current State | Yes | What exists now | Replace entirely each checkpoint |
| Next Actions | Yes | Pending work | Replace entirely each checkpoint |
| User Rules | No | Constraints | Copy forward unless changed |

## Information Priority Hierarchy

When under token pressure, preserve in this order:

1. **Must Keep** (never drop)
   - Problem statement
   - Session intent
   - User decisions
   - Current state
   - Next actions

2. **Should Keep** (compress if needed)
   - Artifact trail (recent files)
   - Play-by-play (recent actions)
   - Technical context

3. **Can Summarize** (aggressive compression allowed)
   - Older play-by-play entries
   - Completed artifact entries
   - Historical decisions that led to current state

## Checkpoint Triggers

Create a new checkpoint when:

1. **Phase completion**: A distinct unit of work is done
2. **Major decision**: User makes a significant choice
3. **Context shift**: Work direction changes substantially
4. **Session break**: Before ending a session
5. **Pre-compression**: Before context window pressure

## Example

```markdown
---
checkpoint: chk-003
created: 2025-12-14T15:30:00Z
anchor: end-of-phase-2
---

## Problem
Build a paint-by-numbers game with AI-generated images.

## Session Intent
Create "Chromatic Quest" - web game where Gemini API generates images converted to paint-by-numbers format. Must work offline after initial generation.

## Essential Information

### Decisions
- Platform: Web (browser)
- Image generation: Gemini API
- Persistence: LocalStorage (no backend)
- Game name: Chromatic Quest

### Technical Context
- React 19.x + TypeScript 5.x
- Vite 7.x, Tailwind CSS 4.x
- HTML5 Canvas API
- @google/genai SDK

### Play-By-Play
- Phase 1 → Implemented core canvas + color quantization → Complete
- Phase 2 → Integrated Gemini API with retry logic → Complete

### Artifact Trail

| File | Status | Key Change |
|------|--------|------------|
| `src/services/gemini.ts` | created | Gemini client with exponential backoff |
| `src/services/imageProcessor.ts` | created | base64 → ImageData → PaintByNumbers pipeline |
| `src/hooks/useImageGeneration.ts` | created | React hook for image generation |

### Current State
- Phases 1-2 complete and working
- Dev server running at localhost:5173
- Build passing, lint clean

### Next Actions
- Phase 3: Implement game mechanics (timer, scoring, combos)
- Blocked: None

## User Rules
- Wait for user approval between phases
- Do not commit without explicit request
```

## References

- Factory.ai: "Compressing Context" - What Must Survive categories
- ReSum paper: Context Summarization for Long-Horizon Search Intelligence
- Example checkpoints: `docs/examples/chk-*.md`
