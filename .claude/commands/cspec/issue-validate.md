---
description: Validate an issue meets all requirements for its nature
argument-hint: <issue-id or path to issue file>
---

# Issue Validation

Validate that an issue meets all requirements to move from `draft` to `ready` status.

## Target Issue

$ARGUMENTS

## Reference Documentation

- **Validation Rules**: @docs/issue-validation.md
- **Taxonomy**: @docs/change-taxonomy-system.md

## Validation Process

### Step 1: Run Schema Validation (Deterministic)

First, run the deterministic schema validation using cspec:

```bash
cspec validate specs/issues/ISSUE-XXX.md
```

If this fails, fix the schema errors before proceeding. Schema validation checks:
- YAML frontmatter structure
- Required fields present
- Valid enum values
- Version matches impact
- Date formats

### Step 2: Load the Issue

Find and read the issue file from `specs/issues/ISSUE-XXX.md`

### Step 3: Universal Requirements

Check ALL issues against these rules:

| Field | Rule |
|-------|------|
| `id` | Unique, pattern `ISSUE-XXX` |
| `title` | Non-empty, max 100 characters |
| `nature` | Valid: feature, enhancement, bug, refactor, optimization, security, hotfix, migration, configuration, deprecation, removal |
| `impact` | Valid: breaking, additive, invisible |
| `version` | Must match impact: breaking→major, additive→minor, invisible→patch |
| `status` | Valid: draft, ready, in-progress, blocked, done |
| `created` | Valid ISO date (YYYY-MM-DD) |
| `updated` | Valid ISO date, >= created |
| Problem section | Non-empty, explains why this matters |
| Scope section | At least one in-scope item |
| Acceptance Criteria | At least one measurable criterion |

### Step 4: Nature-Specific Requirements

Based on the issue's `nature`, check required context:

| Nature | Required Context |
|--------|------------------|
| bug | RCA document referenced |
| feature | Problem statement (in body or referenced) |
| enhancement | Current behavior reference, delta description |
| refactor | Architecture scope, behavioral equivalence statement |
| optimization | Baseline metrics, target metrics, measurement method |
| security | Vulnerability report, attack vector, severity, affected versions |
| hotfix | Incident reference, impact assessment, rollback plan |
| migration | Current state, target state, transformation rules, rollback plan |
| configuration | Current config, new config, impact assessment |
| deprecation | Sunset timeline, migration path, consumer impact |
| removal | Deprecation reference, migration confirmation, impact assessment |

### Step 5: Generate Report

Output a validation report:

```
## Validation Report: ISSUE-XXX

**Status**: ✅ PASS | ❌ FAIL

### Universal Requirements
- [x] ID format valid
- [x] Title present and under 100 chars
- [x] Nature valid
- [x] Impact valid
- [x] Version matches impact
- [ ] Problem section non-empty     ← FAIL: Section is empty
- [x] At least one in-scope item
- [x] At least one acceptance criterion

### Nature-Specific Requirements (bug)
- [ ] RCA document referenced       ← FAIL: Missing in context.required
- [x] Reproduction steps present

### Summary
2 issues found. Fix these before moving to `ready`:
1. Add problem description explaining why this matters
2. Create RCA document and add to context.required

### Next Steps
- Fix the issues above
- Run `/issue-validate ISSUE-XXX` again
- When passing, update status to `ready`
```

### Step 6: Offer to Fix

If validation fails, offer to help fix the issues:
- Missing sections: offer to draft content
- Missing context docs: explain what's needed
- Version mismatch: suggest correct version

If validation passes:
- Offer to update status from `draft` to `ready`
- Remind that `/spec-create` is the next step
