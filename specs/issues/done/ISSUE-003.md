---
id: ISSUE-003
title: "Design and implement coihuin-compress Claude Code skill"
nature: feature
impact: additive
version: minor
status: done
created: 2025-12-14
updated: 2025-12-17

context:
  required:
    - specs/checkpoint-format.md
    - specs/delta-format.md
    - specs/CONSTITUTION.md
  recommended:
    - docs/examples/chk-*.md
    - docs/examples/delta-*.md

depends_on:
  - ISSUE-001
blocks: []
---

## Problem

Long Claude Code sessions lose critical context when automatic summarization occurs. Users must re-explain decisions, file locations, and progress - breaking flow and wasting tokens.

**Solution**: A proactive context compression skill that creates token-efficient checkpoints at natural breakpoints, allowing seamless session continuation.

## Background

### Research Completed (ISSUE-001)

Two key sources informed the design:

1. **ReSum Paper** (arxiv:2509.13313): Context summarization for long-horizon search intelligence
2. **Factory.ai** "Compressing Context": What Must Survive categories, incremental updates, breadcrumbs

### Core Concepts

| Concept | Definition |
|---------|------------|
| **Checkpoint** | Point-in-time snapshot of work state (self-contained, resumable) |
| **Delta** | Incremental changes between checkpoints (avoids re-summarization) |
| **Proactive** | Compress at natural breakpoints, not when forced by limits |
| **What Must Survive** | Session intent, decisions, play-by-play, artifact trail, current state |

### Formats Defined

- **Checkpoint format**: `specs/checkpoint-format.md`
- **Delta format**: `specs/delta-format.md`

## Scope

### In Scope

- [x] Define skill trigger phrases (when skill activates)
- [x] Define skill output format (checkpoint markdown)
- [x] Create checkpoint generation prompt/logic
- [x] Create delta generation prompt/logic
- [x] Write skill definition file
- [x] Test with example scenarios
- [x] Document usage in skill file

### Out of Scope

- Breadcrumbs system (ISSUE-002 - future enhancement)
- Automatic trigger detection (user-invoked only for v1)
- Integration with external storage

## Acceptance Criteria

- [x] Skill file created and functional
- [x] `/checkpoint` or similar trigger generates checkpoint following `specs/checkpoint-format.md`
- [x] `/delta` or similar trigger generates delta following `specs/delta-format.md`
- [x] Skill can be installed in Claude Code user skills directory
- [x] Generated checkpoints are self-contained (can resume work from checkpoint alone)
- [x] Generated deltas accurately capture changes between checkpoints
- [x] Skill works offline (no external API calls)

## Technical Design

### Skill Type

Claude Code user skill (markdown-based, installed in `~/.claude/skills/` or project `.claude/skills/`)

### Proposed Triggers

| Trigger | Action |
|---------|--------|
| "create checkpoint", "checkpoint", "save state" | Generate checkpoint |
| "create delta", "delta", "what changed" | Generate delta from previous checkpoint |
| "compress context", "summarize session" | Generate checkpoint (alias) |

### Checkpoint Generation Logic

1. Analyze conversation history
2. Extract per "What Must Survive" categories:
   - **Problem**: Stable problem statement
   - **Session Intent**: User's goal, requirements, ideal outcome
   - **Decisions**: Locked-in choices (never re-ask)
   - **Technical Context**: Stack, config, environment
   - **Play-By-Play**: High-level action sequence
   - **Artifact Trail**: Files created/modified/deleted
   - **Current State**: What exists now
   - **Next Actions**: What comes next
   - **User Rules**: Constraints to follow
3. Output formatted checkpoint per `specs/checkpoint-format.md`

### Delta Generation Logic

1. Identify previous checkpoint (user provides or infer from context)
2. Analyze changes since that checkpoint
3. Categorize into: Added / Modified / Removed / Status Transitions
4. Output formatted delta per `specs/delta-format.md`

### Output Location

Checkpoints and deltas should be output as:
1. **Primary**: Direct text output in conversation (for immediate use)
2. **Optional**: User can copy to file (e.g., `checkpoints/chk-001.md`)

## Example Usage

```
User: We've finished implementing the auth system. Create a checkpoint.

Agent: [Invokes coihuin-compress skill]

---
checkpoint: auth-complete
created: 2025-12-14T18:30:00Z
---

## Problem
Add user authentication to the application.

## Session Intent
Implement JWT-based auth with login/logout, protected routes, and session persistence.

## Essential Information

### Decisions
- Auth method: JWT with refresh tokens
- Storage: HttpOnly cookies
- Provider: Custom (no OAuth for v1)

### Technical Context
- Next.js 14 App Router
- Prisma + PostgreSQL
- bcrypt for password hashing

### Play-By-Play
- Set up Prisma schema with User model → Complete
- Implemented /api/auth/login endpoint → Complete
- Implemented /api/auth/logout endpoint → Complete
- Created AuthContext with useAuth hook → Complete
- Added middleware for protected routes → Complete

### Artifact Trail
| File | Status | Key Change |
|------|--------|------------|
| prisma/schema.prisma | modified | Added User model |
| src/app/api/auth/login/route.ts | created | JWT login endpoint |
| src/app/api/auth/logout/route.ts | created | Cookie clearing |
| src/contexts/AuthContext.tsx | created | Auth state management |
| src/middleware.ts | created | Route protection |

### Current State
- Auth system fully functional
- All endpoints tested manually
- Protected routes working

### Next Actions
- Add registration endpoint
- Implement password reset flow
- Add rate limiting

## User Rules
- No commits without approval
- Test each endpoint before moving on
```

## Notes

### Design Decisions

1. **User-invoked only**: v1 requires explicit trigger (no auto-detection of "good checkpoint moments")
2. **Conversation output**: Checkpoints appear in chat, not auto-saved to files
3. **No state persistence**: Skill doesn't remember previous checkpoints (user manages files)

### Future Enhancements (not this issue)

- ISSUE-002: Breadcrumbs for context reconstruction
- Auto-detect checkpoint triggers (phase completion, major decisions)
- Checkpoint diff viewer
- Token count estimation

### References

- Checkpoint format: `specs/checkpoint-format.md`
- Delta format: `specs/delta-format.md`
- Constitution: `specs/CONSTITUTION.md`
- Examples: `docs/examples/chk-*.md`, `docs/examples/delta-*.md`
- ReSum paper: https://arxiv.org/pdf/2509.13313
- Factory.ai article: https://factory.ai/news/compressing-context

---

## Resolution

**Status**: Completed (2025-12-17)

**Deliverables**:
- `.claude/skills/coihuin-compress/SKILL.md` — skill definition with triggers and workflow
- `.claude/skills/coihuin-compress/checkpoint-format.md` — checkpoint specification
- `.claude/skills/coihuin-compress/delta-format.md` — delta specification
- `.claude/skills/coihuin-compress/validate.py` — format validation script
- `.claude/skills/coihuin-compress/examples/checkpoint.md` — reference checkpoint
- `.claude/skills/coihuin-compress/examples/delta.md` — reference delta

**Notes**: Skill is functional and installable. Real-world testing recommended as next step.
