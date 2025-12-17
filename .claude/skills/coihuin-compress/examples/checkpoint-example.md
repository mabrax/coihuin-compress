# Checkpoint Example

Reference example for first-time checkpoint creation. This shows a complete checkpoint with all required sections properly filled.

```markdown
---
checkpoint: chk-003
created: 2025-12-14T15:30:00Z
anchor: end-of-phase-2
last_delta: 2025-12-14T16:45:00Z  # optional
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

### Breadcrumbs

| Type | Reference | Hint |
|------|-----------|------|
| file | `src/services/gemini.ts` | Gemini API client with exponential backoff retry logic |
| function | `imageProcessor.convertToRegions()` | Converts quantized image to paintable regions |
| decision | Phase 2, exponential backoff | Why exponential over linear backoff for API retries |

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
