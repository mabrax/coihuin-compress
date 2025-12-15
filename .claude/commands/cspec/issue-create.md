---
description: Create a new issue with proper YAML frontmatter structure
argument-hint: <title or description of what you want to create>
---

# Issue Creation Task

You are creating a new issue following the spec-driven development methodology.

## User Request

$ARGUMENTS

## Reference Documentation

Use these project documents as your source of truth:

- **Template**: @docs/issue-template.md
- **Taxonomy**: @docs/change-taxonomy-system.md
- **Validation Rules**: @docs/issue-validation.md

## Process

### Step 1: Gather Information

Ask the user clarifying questions to determine:

1. **Title**: Clear, descriptive (max 100 chars)
2. **Nature**: Which type of change?
   - `feature` - New capability
   - `enhancement` - Improvement to existing
   - `bug` - Defective behavior correction
   - `refactor` - Code restructuring, no behavior change
   - `optimization` - Performance improvement
   - `security` - Vulnerability fix
   - `hotfix` - Urgent production fix
   - `migration` - Data/infrastructure move
   - `configuration` - Settings change
   - `deprecation` - Mark for future removal
   - `removal` - Eliminate deprecated functionality

3. **Impact**: Consumer impact level
   - `breaking` - Consumers must change (→ major version)
   - `additive` - New surface area, existing unchanged (→ minor version)
   - `invisible` - No external change (→ patch version)

4. **Problem/Motivation**: Why does this matter?
5. **Scope**: What's in and out of scope?
6. **Acceptance Criteria**: How do we know it's done?
7. **Dependencies**: Does this depend on or block other issues?

### Step 2: Determine Required Context

Based on the nature, identify what context documents are required:

| Nature | Required Context |
|--------|------------------|
| bug | RCA document |
| feature | Problem statement |
| enhancement | Current behavior reference, delta description |
| refactor | Architecture scope, behavioral equivalence statement |
| optimization | Baseline metrics, target metrics, measurement method |
| security | Vulnerability report, attack vector, severity, affected versions |
| hotfix | Incident reference, impact assessment, rollback plan |
| migration | Current state, target state, transformation rules, rollback plan |
| configuration | Current config, new config, impact assessment |
| deprecation | Sunset timeline, migration path, consumer impact |
| removal | Deprecation reference, migration confirmation, impact assessment |

### Step 3: Generate Issue ID

Check existing issues and generate the next sequential ID:
- Pattern: `ISSUE-XXX` (zero-padded, e.g., ISSUE-001)
- Look in `/specs/issues/` directory for existing issues

### Step 4: Create the Issue File

Create the issue file at: `/specs/issues/ISSUE-XXX.md`

Use this structure:

```markdown
---
id: ISSUE-XXX
title: "<title>"
nature: <nature>
impact: <impact>
version: <major|minor|patch>
status: draft
created: <today's date YYYY-MM-DD>
updated: <today's date YYYY-MM-DD>

context:
  required: []
  recommended: []

depends_on: []
blocks: []
---

## Problem

<Why does this matter? What problem are we solving?>

## Scope

### In Scope

- [ ] <Specific deliverable 1>
- [ ] <Specific deliverable 2>

### Out of Scope

- <Explicitly excluded item 1>
- <Explicitly excluded item 2>

## Acceptance Criteria

- [ ] <Measurable criterion 1>
- [ ] <Measurable criterion 2>

## Notes

<Additional context, constraints, or considerations>
```

### Step 5: Inform About Next Steps

After creating the issue, remind the user:

1. The issue is in `draft` status
2. Required context documents may need to be created based on nature
3. Run `/issue-validate` to check if the issue is ready to move to `ready` status
4. Once validated, the issue can proceed to spec creation

## Output

Provide the full path to the created issue file and summarize:
- Issue ID and title
- Classification (nature + impact → version)
- Required context that still needs to be created (if any)
- Next steps
