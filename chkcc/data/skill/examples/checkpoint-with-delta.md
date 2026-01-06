# Checkpoint with Deltas Example

This example shows how deltas accumulate within a checkpoint file. Deltas are `## Delta:` sections appended inline—not separate files.

```markdown
---
checkpoint: auth-system
created: 2025-12-14T14:00:00Z
anchor: end-of-phase-1
last_delta: 2025-12-14T18:30:00Z
---

## Problem

Add user authentication to the web application.

## Session Intent

Implement JWT-based auth with login/logout, protected routes, and session persistence.

## Essential Information

### Decisions

- Auth method: JWT with refresh tokens
- Storage: HttpOnly cookies (not localStorage)
- Password hashing: bcrypt with 12 rounds

### Technical Context

- Next.js 14 App Router
- Prisma + PostgreSQL
- jose for JWT handling

### Play-By-Play

- Phase 1 → Set up Prisma User model → Complete
- Phase 2 → Implemented auth endpoints → Complete
- Phase 2 → Created AuthContext with useAuth hook → Complete

### Artifact Trail

| File | Status | Key Change |
|------|--------|------------|
| `prisma/schema.prisma` | modified | Added User model |
| `src/app/api/auth/login/route.ts` | created | JWT login endpoint |
| `src/contexts/AuthContext.tsx` | created | Auth state management |

### Current State

- Login/logout endpoints working
- Protected routes enforced via middleware
- Build passing, no lint errors

### Next Actions

- Add registration endpoint
- Implement password reset flow

## User Rules

- No commits without explicit approval

---

## Delta: 2025-12-14T16:30:00Z

### What Changed

Completed auth endpoints: login, logout, and middleware for route protection.

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `src/app/api/auth/login/route.ts` | created | JWT login with cookie setting |
| `src/app/api/auth/logout/route.ts` | created | Cookie clearing endpoint |
| `src/middleware.ts` | created | Route protection logic |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| Phase 2: Auth Endpoints | In Progress | Complete |

---

## Delta: 2025-12-14T18:30:00Z

### What Changed

Added React auth context and useAuth hook for client-side state.

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `src/contexts/AuthContext.tsx` | created | Auth state management |
| `src/hooks/useAuth.ts` | created | Custom hook wrapping context |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| Phase 2: Client Auth | In Progress | Complete |
| Phase 3: Registration | Blocked | Ready |
```

## Key Points

1. **One file**: The checkpoint and its deltas live in the same file
2. **Deltas append**: Each `## Delta:` section is added below the previous one
3. **`last_delta` field**: Updated in frontmatter when deltas are added
4. **Git provides history**: No need for separate delta files—Git tracks the evolution
