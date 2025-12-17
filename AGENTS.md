# AGENTS.md

This document provides coding agents with the context needed to work effectively in this project.

---

## CLI Commands Reference

The `cspec` CLI provides the following commands:

| Command | Description |
|---------|-------------|
| `cspec init` | Initialize spec-driven development (creates directories + installs slash commands) |
| `cspec validate <path>` | Validate an issue file against the schema |
| `cspec validate <path> --strict` | Validate with strict mode (fail on warnings) |
| `cspec list` | List all issues in the project |
| `cspec list --status=<status>` | Filter issues by status (draft, ready, in-progress, blocked, done) |
| `cspec update` | Update slash commands to latest version |

---

## Slash Commands Reference

Slash commands are available in Claude Code and are namespaced as `cspec:<command>`.

| Command | Description | Usage |
|---------|-------------|-------|
| `/cspec/issue-create` | Interactive issue creation with proper structure | `/cspec/issue-create <description>` |
| `/cspec/issue-validate` | Full validation with suggestions and fixes | `/cspec/issue-validate <issue-id>` |

**Note**: Commands can also be invoked as `cspec:issue-create`, `cspec:issue-validate`, etc.

---

## Workflow Documentation

This project follows **spec-driven development** methodology.

### Development Flow

```
Issue --> Spec --> Implementation --> Verification --> Done
  ^                                        |
  |                                        |
  +-------- feedback loop -----------------+
```

### Phases

#### Phase 1: Issue Definition
**Goal**: Capture and validate the change request.

1. Create issue: `/cspec/issue-create <description>`
2. Classify: Determine nature (feature, bug, etc.) and impact (breaking, additive, invisible)
3. Define scope and acceptance criteria
4. Validate schema: `cspec validate specs/issues/ISSUE-XXX.md`
5. Full validation: `/cspec/issue-validate ISSUE-XXX`
6. When passing, update status to `ready`

#### Phase 2: Specification
**Goal**: Define detailed implementation approach before writing code.

1. Identify boundaries the change crosses
2. Create spec artifacts per boundary
3. Define validation hooks (how to verify implementation)
4. Review and approve specs

#### Phase 3: Implementation
**Goal**: Build according to specification.

1. Review spec thoroughly
2. Implement following spec exactly
3. Run validation hooks during development
4. Address all acceptance criteria

#### Phase 4: Verification
**Goal**: Confirm implementation matches specification.

1. Run all validation hooks
2. Check acceptance criteria
3. Update persistent artifacts
4. Sign-off and close issue

### Issue Natures

| Nature | When to Use |
|--------|-------------|
| `feature` | New capability |
| `enhancement` | Improvement to existing functionality |
| `bug` | Fix defective behavior |
| `refactor` | Code restructuring, no behavior change |
| `optimization` | Performance improvement |
| `security` | Vulnerability fix |
| `hotfix` | Urgent production fix |
| `migration` | Data/infrastructure move |
| `configuration` | Settings change |
| `deprecation` | Mark for future removal |
| `removal` | Delete deprecated functionality |

### Impact to Version Mapping

| Impact | Version | Meaning |
|--------|---------|---------|
| `breaking` | `major` | Consumers must change their code |
| `additive` | `minor` | New surface area, existing unchanged |
| `invisible` | `patch` | No external change visible to consumers |

### Issue Status Flow

```
draft --> ready --> in-progress --> done
                        |
                        v
                     blocked
```

---

## File Structure

```
specs/
├── PROJECT.yaml      # Project definition
├── CONSTITUTION.md   # Rules and philosophy
└── issues/
    ├── active/       # Ready, draft, in-progress, blocked
    │   ├── ISSUE-XXX.md
    │   └── spec-XXX.md   # Spec collocated with issue
    └── done/         # Completed issues
        ├── ISSUE-XXX.md
        └── spec-XXX.md   # Spec moves with issue when done

.claude/commands/cspec/  # Slash commands (namespaced)
```

---

## PROJECT CONTEXT

### Project Overview

**coihuin-compress** is a Claude Code skill for proactive context window compression. It helps maintain critical work state during long coding sessions by intelligently compressing context before automatic summarization occurs, preventing information loss.

### Tech Stack

- **Languages**: Markdown (skill definition)
- **Framework**: Claude Code Skills system
- **Dependencies**: Claude Code CLI
- **Package Manager**: N/A (skill-based project)

### Architecture

```
coihuin-compress/
├── specs/                    # Spec-driven development artifacts
│   ├── PROJECT.yaml          # Project definition
│   ├── CONSTITUTION.md       # Rules and philosophy
│   └── issues/               # Issue tracking
├── docs/
│   └── examples/             # Example checkpoints and deltas
├── .claude/
│   └── commands/cspec/       # cspec slash commands
└── [skill files]             # Skill definition (to be created)
```

**Key Components**:
- **Checkpoint Generator**: Creates point-in-time snapshots of work state
- **Delta Tracker**: Tracks changes between checkpoints
- **Compression Engine**: Reduces token count while preserving precision

### Key Conventions

- **Naming**: kebab-case for files, descriptive checkpoint IDs
- **Format**: Markdown for human-readable output, YAML for structured data
- **Patterns**: Checkpoint → Delta → Checkpoint cycle for state tracking
- **Checkpoints**: Named with `chk-XXX.md` pattern
- **Deltas**: Named with `delta-XXX-YYY.md` pattern (from → to)

### Important Files

| File | Purpose |
|------|---------|
| `specs/PROJECT.yaml` | Project definition and scope |
| `specs/CONSTITUTION.md` | Development rules and philosophy |
| `AGENTS.md` | Agent context (this file) |
| `docs/examples/` | Example checkpoint and delta formats |

### Testing

- **Framework**: Manual validation against spec
- **Validation**: `cspec validate <issue-path>`
- **Acceptance**: Checkpoint must be recoverable, deltas must be accurate

### Build & Deploy

- **Install**: Add skill to Claude Code user skills directory
- **Usage**: Invoke via skill trigger phrases
- **No build step**: Markdown-based skill definition

### Domain Knowledge

| Term | Definition |
|------|------------|
| **Checkpoint** | Point-in-time snapshot of work state (what exists now) |
| **Delta** | Changes between two checkpoints (what changed) |
| **Context Window** | Claude's available memory for conversation |
| **Compression** | Reducing token count while preserving critical information |
| **State Preservation** | Maintaining enough detail to resume work seamlessly |
| **Token Efficiency** | Maximizing information value per token |

---

## References

- [Methodology](docs/methodology.md) - Full spec-driven development methodology
- [Issue Template](docs/issue-template.md) - Issue file structure
- [Issue Validation](docs/issue-validation.md) - Validation rules
- [Change Taxonomy](docs/change-taxonomy-system.md) - Classification system
- [Cheatsheet](docs/cheatsheet.md) - Quick reference
