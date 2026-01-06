# INDEX.md Format Specification

The INDEX.md file provides a quick inventory of all active checkpoints, enabling fast navigation without reading individual checkpoint files.

## Location

```
checkpoints/active/INDEX.md
```

## Structure

### Quick Reference Table

A markdown table at the top for at-a-glance overview:

```markdown
# Active Checkpoints

| Checkpoint | Description | Last Updated |
|------------|-------------|--------------|
| chk-feature-auth | User authentication system | 2024-01-15 |
| chk-api-refactor | REST API restructuring | 2024-01-14 |
```

**Columns**:
- **Checkpoint**: Filename (without `.md` extension)
- **Description**: One-line summary of the work (from checkpoint's Problem section)
- **Last Updated**: ISO-8601 date of last modification

### Summary Sections

Below the table, one section per checkpoint with essential context:

```markdown
---

## chk-feature-auth

**Problem**: Implement JWT-based authentication with refresh token support.

**Scope**: `src/auth/`, `src/middleware/`, API endpoints `/login`, `/logout`, `/refresh`.

**Status**: In progress - login working, refresh token implementation next.

---

## chk-api-refactor

**Problem**: Migrate from REST to GraphQL while maintaining backward compatibility.

**Scope**: `src/api/`, `src/resolvers/`, schema definitions.

**Status**: Schema defined, resolvers 60% complete.
```

**Fields**:
- **Problem**: Condensed version of checkpoint's Problem section (1-2 sentences)
- **Scope**: Key files, directories, or components involved
- **Status**: Current state and immediate next step

## Maintenance Rules

### On Checkpoint Creation

1. Add new row to the Quick Reference Table
2. Add new Summary Section at the end
3. Set Last Updated to current date

### On Delta Update

1. Update Last Updated date in the table
2. Update Status in the Summary Section if changed
3. Optionally update Scope if it expanded

### On Archive

1. Remove row from the Quick Reference Table
2. Remove the Summary Section
3. (The checkpoint itself moves to `checkpoints/archive/`)

## Empty State

When no active checkpoints exist:

```markdown
# Active Checkpoints

| Checkpoint | Description | Last Updated |
|------------|-------------|--------------|

*No active checkpoints. Create one with "checkpoint" command.*
```

## Validation

The `format-check.py` script validates INDEX.md files:
- Table has correct headers
- Each table entry has a matching Summary Section
- Each Summary Section has required fields (Problem, Scope, Status)
- Last Updated dates are valid ISO-8601 format
