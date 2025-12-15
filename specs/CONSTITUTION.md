# Constitution

## Philosophy

This project follows **spec-driven development**:

1. **Issue first**: Every change starts with an issue (the "what and why")
2. **Spec before code**: Specs define the "how" before implementation
3. **Source of truth**: Specs are authoritative; code implements specs
4. **Validate against spec**: Implementation correctness = spec compliance
5. **Clean exit**: Delete transient artifacts; keep persistent ones updated

### Context Compression Philosophy

- **Precision over brevity**: Compressed state must preserve critical details, not just summarize
- **Proactive preservation**: Compress before context limits are reached, not after
- **Recoverable state**: Any compressed checkpoint should allow resuming work seamlessly
- **Token efficiency**: Every token in compressed output should carry maximum information value

## Rules

### Issues

- Every change requires an issue
- Issues must have: nature, impact, scope, acceptance criteria
- Issues must be validated before moving to spec phase

### Specs

- Specs must cover every boundary a change crosses
- Specs must be machine-readable where possible
- Specs include validation hooks (how to verify implementation)

### Implementation

- Implementation follows spec, not the other way around
- Deviations from spec require spec update first
- Feedback loops return to appropriate phase (issue or spec)

### Skill-Specific Rules

- No external API calls - skill must work offline
- State compression must be deterministic and reproducible
- Checkpoint format must be human-readable (Markdown)
- Delta tracking must clearly show what changed between checkpoints

## Quality Standards

- Compressed state must be parseable back to structured data
- Checkpoint generation should take < 1 second
- Compressed output should achieve > 70% token reduction vs raw context
- All checkpoints must include timestamp and context hash

## Anti-patterns

- Avoid lossy compression that drops critical state
- Avoid over-abstraction that obscures what happened
- Avoid vague summaries like "made progress on feature"
- Avoid storing redundant information across checkpoints

## Artifacts

| Type | Lifecycle |
|------|-----------|
| Checkpoints, deltas, state snapshots | Transient (delete when session ends or context resets) |
| Skill definition, compression algorithms, format specs | Persistent (source of truth) |

## Versioning

- **Breaking** changes to Major version (checkpoint format incompatibility)
- **Additive** changes to Minor version (new compression features)
- **Invisible** changes to Patch version (internal optimizations)
