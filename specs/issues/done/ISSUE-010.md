---
id: ISSUE-010
title: "Define archive lifecycle—prevent orphaned artifacts"
nature: enhancement
impact: invisible
version: patch
status: done
created: 2025-12-16
updated: 2025-12-17

context:
  required: []
  recommended: []

depends_on: []
blocks: []
---

## Problem

The archive strategy is undefined:

- When exactly is work "complete"?
- Can archived checkpoints ever be loaded?
- Do archived checkpoints decay in usefulness?
- What's the retention strategy?

Checkpoints reference code files that evolve. An archived checkpoint saying "src/auth/login.ts - created" becomes misleading when that file is later modified or deleted. The checkpoint is frozen but the codebase isn't.

This creates **false permanence**—artifact graveyards that look useful but provide outdated or misleading information.

## Scope

### In Scope

- [ ] Define "complete" criteria for archiving
- [ ] Document archive purpose (historical record vs loadable state)
- [ ] Add decay/staleness acknowledgment
- [ ] Consider retention policy (keep forever? prune after N months?)
- [ ] Add archive guidance to SKILL.md
- [ ] Document when to delete vs archive

### Out of Scope

- Automated staleness detection
- Reference tracking (updating checkpoints when files change)
- Integration with git history

## Acceptance Criteria

- [x] Clear criteria for when to archive
- [x] Archive purpose documented (audit trail vs active use)
- [x] Staleness/decay acknowledged in documentation
- [x] Retention guidance provided
- [x] Users understand archived checkpoints may be outdated

## Notes

### Proposed Archive Lifecycle

```
ACTIVE CHECKPOINT
    │
    ├─── Work continues ───► Merge/Update cycle
    │
    ▼
COMPLETION CRITERIA MET
    │
    ├─── Feature shipped?
    ├─── Epic closed?
    ├─── User explicitly marks done?
    │
    ▼
ARCHIVE DECISION
    │
    ├─── Archive: Historical value, may reference later
    │       └── Move to checkpoints/archive/
    │
    └─── Delete: No historical value, was temporary
            └── Remove file entirely
```

### Completion Criteria

A checkpoint should be archived (not deleted) when:

1. **Feature shipped**: The work it tracked is in production
2. **Learning value**: Contains decisions/rationale worth preserving
3. **Audit requirements**: May need to reference how work evolved
4. **Cross-reference**: Other documents or issues link to it

A checkpoint should be deleted when:

1. **Exploratory work**: Was temporary investigation
2. **Superseded**: A newer checkpoint completely replaces it
3. **Failed experiment**: The approach was abandoned
4. **No historical value**: Would never need to reference again

### Staleness Warning

Add to SKILL.md:

```markdown
## Archive Limitations

Archived checkpoints are **historical snapshots**, not live state:

- File references may be outdated (files moved, renamed, deleted)
- Technical context may no longer apply (dependencies updated)
- Decisions may have been revisited in later work

Use archived checkpoints for:
- Understanding how decisions were made
- Auditing project evolution
- Onboarding (with staleness caveat)

Do NOT use archived checkpoints for:
- Resuming active work
- Current state reference
- Up-to-date technical context
```

### Retention Policy Options

| Policy | Description | Tradeoff |
|--------|-------------|----------|
| Keep forever | Never delete archives | Clutter, false authority |
| Time-based | Delete after 6 months | Lose historical value |
| Reference-based | Keep if referenced elsewhere | Complexity |
| Manual | User decides on archive | Cognitive load |

**Recommendation**: Manual with guidance. User archives what has value, deletes what doesn't. Skill provides criteria, user decides.

### Audit Origin

Dialectic audit tension #7: Archive Strategy vs Information Decay

### Severity

Low—archives are optional feature, not core workflow

---

## Resolution (2025-12-16)

**Discussion outcome**: Archives serve two different contexts.

### Two Contexts

**1. This project (coihuin-compress workspace)**
- Archived checkpoints feed the eval system (ISSUE-011)
- They ARE useful—for improving the skill itself

**2. Other projects using the skill**
- Archived checkpoints are stale/ephemeral
- Should NOT be used as reference by Claude
- Need marker to prevent accidental loading

### Solution: Marker File

```
checkpoints/
├── active/           # Load these, work with these
└── archive/          # DO NOT LOAD
    └── .claudeignore # Marker: "ignore for context purposes"
```

The marker file tells Claude: "These files exist for eval/historical purposes. Do not use them as reference."

### Revised Actions

1. Keep `archive/` name (clear meaning)
2. Add `.claudeignore` or similar marker file to archive directories
3. Document in SKILL.md that archived checkpoints are eval-only, not context
4. Archived checkpoints are for: humans learning, eval system, historical record
5. Archived checkpoints are NOT for: Claude context, resuming work, current truth

**Insight**: Ephemeral artifacts can still have value—for eval, learning, and historical understanding. The key is preventing misuse as "current truth."

**Reference**: history/2025-12-16-dialectic-audit.md, Appendix A, Discussion 7
