---
id: ISSUE-009
title: "Add edge case examples—failures, pivots, ambiguous state"
nature: enhancement
impact: additive
version: minor
status: done
created: 2025-12-16
updated: 2025-12-16

context:
  required: []
  recommended: []

depends_on: []
blocks: []
---

## Problem

Current examples show only the **happy path**:
- Clean phases
- Successful completions
- Linear progress

Real sessions have:
- **Failed experiments**: "I tried X, it didn't work"
- **Pivots**: User changes direction mid-work
- **Ambiguous state**: Partially working code, unclear next steps
- **Exploration sessions**: No clear phases, discovery-oriented
- **Debugging sessions**: Non-linear investigation

Without pathological case examples, users don't know how to apply the format to messy reality. They either:
1. Force messy reality into happy-path templates (losing information)
2. Abandon the skill when it doesn't fit their situation

## Scope

### In Scope

- [ ] Create example: checkpoint after failed experiment
- [ ] Create example: delta documenting a pivot/direction change
- [ ] Create example: checkpoint with ambiguous/partial state
- [ ] Create example: exploration session without clear phases
- [ ] Add guidance in SKILL.md for handling edge cases
- [ ] Document anti-patterns (what NOT to do with edge cases)

### Out of Scope

- Exhaustive coverage of all possible scenarios
- Fundamental format changes to accommodate edge cases

## Acceptance Criteria

- [ ] At least 3 pathological case examples added
- [ ] Each example includes commentary on what's different
- [ ] SKILL.md includes edge case handling guidance
- [ ] Users can find relevant example for non-linear work
- [ ] Format shown to be flexible enough for messy reality

## Notes

### Proposed Edge Case Examples

#### 1. Failed Experiment Checkpoint

```markdown
---
checkpoint: chk-auth-experiment-failed
created: 2025-12-16T14:00:00Z
anchor: after-oauth-attempt
---

## Problem
Add user authentication to the application.

## Session Intent
Implement auth with minimal complexity, evaluating OAuth vs custom JWT.

## Essential Information

### Decisions
- REJECTED: OAuth2 with Google provider
  - Reason: Complexity overhead for MVP, callback URL issues in dev
  - Learning: Would need ngrok or similar for local dev
- PENDING: Evaluate custom JWT approach next

### Technical Context
- Next.js 14 App Router
- No auth library installed yet

### Play-By-Play
- Attempt 1 → Implemented Google OAuth → Failed (callback complexity)
- Attempt 1 → Rolled back OAuth code → Clean slate

### Artifact Trail
| File | Status | Key Change |
|------|--------|------------|
| (none) | - | All experimental code removed |

### Current State
- Back to pre-auth state
- OAuth evaluated and rejected
- Ready to try alternative approach

### Next Actions
- Research JWT implementation patterns
- Evaluate jose vs jsonwebtoken libraries
- Implement custom auth if simpler
```

#### 2. Pivot Delta

```markdown
---
delta: chk-002-to-chk-003-pivot
created: 2025-12-16T15:00:00Z
from: chk-002
to: chk-003
---

## Summary
Direction change: Abandoned server-side rendering approach, pivoting to client-side SPA.

## Changes

### Added
- New architectural decision: SPA over SSR
- Rationale documentation for pivot

### Modified
| Field | Before | After |
|-------|--------|-------|
| Session Intent | "Build SSR app with Next.js" | "Build client-side SPA with Vite" |
| Technical Context | Next.js 14, server components | Vite + React, client-only |
| Next Actions | Implement server components | Set up Vite, migrate components |

### Removed
- All server-component related decisions
- SSR-specific technical context
- Server-side data fetching patterns

### Status Transitions
| Item | Before | After |
|------|--------|-------|
| SSR Implementation | In Progress | Abandoned |
| SPA Setup | N/A | Ready |

## Pivot Rationale
User discovered SSR complexity exceeded project needs. Client-side rendering
sufficient for use case. Decision to cut scope and ship faster.
```

#### 3. Ambiguous State Checkpoint

```markdown
---
checkpoint: chk-debugging-session
created: 2025-12-16T16:00:00Z
anchor: mid-investigation
---

## Problem
Application crashes intermittently on user login.

## Session Intent
Find and fix the root cause of login crashes.

## Essential Information

### Decisions
- HYPOTHESIS: Race condition in auth state initialization
- NOT YET CONFIRMED: Need more evidence

### Technical Context
- React 18 with Concurrent Mode
- Auth context with useEffect initialization
- Crash occurs ~30% of login attempts

### Play-By-Play
- Investigation → Added logging to AuthContext → Inconclusive
- Investigation → Reviewed React 18 strict mode behavior → Possible lead
- Investigation → Found double-mount in dev mode → Explains some symptoms

### Artifact Trail
| File | Status | Key Change |
|------|--------|------------|
| `src/contexts/AuthContext.tsx` | modified | Added debug logging |
| `debug-notes.md` | created | Investigation notes |

### Current State
- Bug not yet fixed
- Strong hypothesis: useEffect cleanup not handling unmount
- Evidence: Double initialization logs in strict mode
- Uncertainty: May be different issue in production

### Next Actions
- Test hypothesis: Add cleanup function to useEffect
- If fix works: Remove debug logging, close issue
- If fix fails: Investigate network timing next
- BLOCKER: Need to reproduce in production build

## User Rules
- Don't commit debug logging
- Test fix in prod build before declaring victory
```

### Audit Origin

Dialectic audit tension #6: Examples vs Edge Cases

### Severity

Medium—limits skill applicability to clean scenarios

---

## Resolution (2025-12-16)

**Status**: Closed—superseded by ISSUE-011.

**Reason**: The eval mechanism (ISSUE-011) solves this naturally:

1. Real work includes edge cases (failures, pivots, ambiguity)
2. Dogfooding collects real checkpoints from real projects
3. Eval rubric curates good examples, including edge cases

No need to artificially create edge case examples—they emerge from real usage and get promoted through the eval system.

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 6
