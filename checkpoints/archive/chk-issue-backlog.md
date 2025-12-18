---
checkpoint: chk-issue-backlog
created: 2025-12-17T15:21:36Z
anchor: post-dialectic-cleanup
last_delta: 2025-12-18T00:28:40Z
---

## Problem

After the dialectic audit, coihuin-compress has active issues that need implementation. These represent refinements and enhancements identified through critical self-examination of the skill.

## Session Intent

Track and implement the remaining issues from the dialectic audit to mature the coihuin-compress skill. Each issue has been discussed and either resolved (clear path forward), reframed (understanding shifted), or superseded by other work.

## Essential Information

### Decisions

- **ISSUE-005 invalidated**: Checkpoint self-containment concern was misdirected at structure; real issue is quality verification (handled by ISSUE-011)
- **ADR-001 created**: Documents why ISSUE-005 was invalidated—establishes precedent for issue invalidation decisions
- **Delta = intelligent merge**: Delta command/logic is valuable; delta artifact files are optional since Git provides history
- **Two-layer validation**: Structural (format-check.py) + Semantic (LLM in-skill)
- **Warnings not automation**: Proactive triggers should be advisory, user decides
- **Archive marker file**: Use `.archive-marker` (renamed from `.claudeignore` to avoid implying gitignore-style parsing)
- **Dialectic evaluation model**: Human interview (5 questions) → Agent investigation (3 parallel tasks) → Correlation & synthesis
- **Senior implementers for phases**: Used swarm of senior-implementer agents for parallel phase execution
- **Delta-as-operation model**: Based on real-world usage, simplify from 3 concepts (checkpoint, delta artifact, merge) to 2 operations (checkpoint, delta). "Delta" becomes a verb meaning "update checkpoint with what changed"
- **Subagent coherence validation**: Use 3 parallel Explore agents to validate issue-spec and tasks-spec coherence before implementation—catches misalignments early
- **Context-aware advisory**: Proactive triggers suggest checkpoint vs delta based on session state (no checkpoint loaded → suggest checkpoint; checkpoint loaded → suggest delta)

### Technical Context

- Project: coihuin-compress (Claude Code skill)
- Location: `/Users/mabrax/Documents/Projects/coihuin-compress`
- Spec format: YAML frontmatter + markdown body (cspec style)
- Issue tracking: `specs/issues/active/` and `specs/issues/done/`

### Play-By-Play

- Dialectic audit → Generated ISSUE-004 through ISSUE-012 → Complete
- Post-audit → ISSUE-004, ISSUE-009 closed during discussions → Complete
- 2025-12-17 → ISSUE-005 invalidated, ADR-001 created, DEPENDENCIES.md updated → Complete
- 2025-12-17 → ISSUE-011 spec created, reviewed, implemented via 4-phase plan → Complete
- 2025-12-17 → ISSUE-006 reframed, spec + tasks created, implemented → Complete
- 2025-12-17 → ISSUE-012 discussed, spec + tasks created, implemented → Complete
- 2025-12-17 → ISSUE-010 implemented directly (trivial scope) → Complete
- 2025-12-17 → ISSUE-007 spec'd and tasks created, validated via subagent swarm → Complete
- 2025-12-17 → ISSUE-007 implemented via senior-implementer, review analyzed, P1 fix applied → Complete
- 2025-12-17 → ISSUE-008 researched, spec'd, implemented directly (documentation-only) → Complete

### Artifact Trail

| File | Status | Key Change |
|------|--------|------------|
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Two-layer validation, semantic self-check section |
| `.claude/skills/coihuin-compress/format-check.py` | created | Renamed from validate.py, added 8 advisory heuristics |
| `.claude/skills/coihuin-compress/validate.py` | deleted | Replaced by format-check.py |
| `checkpoints/archive/.archive-marker` | renamed | From .claudeignore (clearer naming) |
| `specs/issues/done/ISSUE-007.md` | moved | Two-layer validation complete |
| `specs/issues/done/spec-007.md` | moved | Preserved with issue |
| `specs/issues/done/TASKS-007.md` | moved | 6-phase implementation plan |
| `specs/issues/done/ISSUE-010.md` | done | Archive lifecycle complete |
| `README.md` | modified | Updated validation section, archive marker reference |
| `STATUS.md` | modified | Updated validation script path |
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Proactive Advisory Triggers section added |
| `specs/issues/done/ISSUE-008.md` | moved | Proactive triggers complete |
| `specs/issues/done/spec-008.md` | moved | Advisory triggers specification |

### Breadcrumbs

| Type | Reference | Hint |
|------|-----------|------|
| file | `eval/rubric.md` | Canonical scoring rubric |
| file | `.claude/commands/eval-checkpoint.md` | Full dialectic eval command |
| file | `.claude/skills/coihuin-compress/SKILL.md:112-144` | Semantic Quality Self-Check section |
| file | `.claude/skills/coihuin-compress/format-check.py` | Two-layer validation script |
| commit | `8032abe` | ISSUE-007 implementation commit |
| commit | `eaf17bf` | Checkpoint update and ISSUE-010 finalization |
| file | `specs/issues/done/spec-007.md` | Two-layer validation spec with heuristics table |
| file | `specs/issues/done/TASKS-007.md` | 6-phase implementation plan |
| file | `.claude/skills/coihuin-compress/SKILL.md:85-118` | Proactive Advisory Triggers section |
| file | `specs/issues/done/spec-008.md` | Advisory triggers specification |

### Current State

**All issues complete.** The dialectic audit backlog is fully resolved.

**Done issues:** ISSUE-001, 002, 003, 004, 006, 007, 008, 009, 010, 011, 012
**Invalid issues:** ISSUE-005 (see ADR-001)
**Active issues:** None

### Next Actions

1. **Archive this checkpoint**—all issues resolved, backlog complete
2. **Update README**—compress to match current reality (delta-as-operation model)

## User Rules

- Never commit without explicit approval
- No time estimates in plans
- Check date with `date` command for date-related tasks

---

## Delta: 2025-12-17T19:02:30Z

### What Changed

**ISSUE-006 implemented** - Simplified coihuin-compress from three concepts to two operations.

### Implementation

Executed TASKS-006.md via 4 parallel senior-implementer agents:
- **Phase 1**: Deleted delta-format.md specs (2 files)
- **Phase 2**: Updated SKILL.md (new delta definition, removed merge section)
- **Phase 3**: Updated checkpoint-format.md (added `last_delta` field)
- **Phase 4**: Validated and moved ISSUE-006 to done/

Post-review fixes:
- Deleted 4 stale delta examples from `docs/examples/`
- Restored spec-006.md to `specs/issues/done/` per AGENTS.md guidelines

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Delta = "update checkpoint", merge section removed |
| `.claude/skills/coihuin-compress/checkpoint-format.md` | modified | Added optional `last_delta` frontmatter field |
| `.claude/skills/coihuin-compress/delta-format.md` | deleted | Artifact spec eliminated |
| `specs/delta-format.md` | deleted | Duplicate removed |
| `docs/examples/delta-001-002.md` | deleted | Stale example |
| `docs/examples/delta-002-003.md` | deleted | Stale example |
| `docs/examples/delta-003-004.md` | deleted | Stale example |
| `docs/examples/delta-004-005.md` | deleted | Stale example |
| `specs/issues/done/ISSUE-006.md` | moved | From active/, all criteria checked |
| `specs/issues/done/spec-006.md` | created | Restored for historical record |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| ISSUE-006 | Ready | Done |
| Active issues | 4 (with 006 ready) | 4 (all draft) |
| Done issues | 6 | 7 |

---

## Delta: 2025-12-17T19:47:09Z

### What Changed

**ISSUE-012 spec'd and ready** - Created specification and implementation tasks for format spec cleanup.

### Session Work

1. Discussed ISSUE-012 scope refinement:
   - Removed obsolete delta-format.md review (deleted in ISSUE-006)
   - Added docs/examples/ deletion (historical design artifacts)
   - Clarified examples were iterative design checkpoints, not reference docs

2. Created spec-012.md:
   - Design principles for lean specs
   - Content analysis with line numbers
   - 4 implementation steps
   - 7 validation checks

3. Agent review of issue-spec coherence (3 parallel Explore agents):
   - Scope coverage: PASS
   - Acceptance criteria: PASS
   - Internal consistency: PASS (line numbers verified)

4. Created TASKS-012.md:
   - Phase 1: Clean checkpoint-format.md
   - Phase 2: Delete historical examples
   - Phase 3: Document removal in history
   - Phase 4: Validate and finalize

5. Agent review of tasks (3 parallel Explore agents):
   - Tasks-spec alignment: 100% coverage
   - Tasks-issue alignment: 95% (all criteria mapped)
   - Executability: PASS (minor recommendations only)

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `specs/issues/active/ISSUE-012.md` | modified | Refined scope, updated date |
| `specs/issues/active/spec-012.md` | created | Format cleanup specification |
| `specs/issues/active/TASKS-012.md` | created | 4-phase implementation plan |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| ISSUE-012 | Draft | Ready |
| Active issues (ready) | 0 | 1 |

---

## Delta: 2025-12-17T20:22:08Z

### What Changed

**ISSUE-012 implemented and review findings fixed** - Cleaned up format spec, extracted example to separate file, fixed stale references.

### Session Work

1. **Revised Phase 1 of TASKS-012.md**:
   - Changed from "delete Example section" to "move Example to separate file"
   - Validated approach against claude-code-guide (examples in separate files recommended)
   - Added task 1.4: Update SKILL.md to reference example

2. **Executed TASKS-012.md** via senior-implementer agent:
   - Phase 1: Extracted example to `.claude/skills/coihuin-compress/examples/checkpoint-example.md`
   - Phase 2: Deleted `docs/examples/` (6 historical artifacts)
   - Phase 3: Created `history/2025-12-17-cleanup-notes.md`
   - Phase 4: Validated, moved issue to `done/`

3. **Fixed review findings** (from review-issue-012.md):
   - Updated AGENTS.md Architecture section (removed `docs/examples/` reference)
   - Updated AGENTS.md Important Files table
   - Deleted duplicate `specs/checkpoint-format.md`
   - Updated checkpoint status and breadcrumbs

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `specs/issues/active/TASKS-012.md` | modified | Revised Phase 1 to move example instead of delete |
| `.claude/skills/coihuin-compress/examples/checkpoint-example.md` | created | Extracted example for first checkpoint reference |
| `.claude/skills/coihuin-compress/checkpoint-format.md` | modified | Removed Example and References sections |
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Added reference to examples/ |
| `docs/examples/` | deleted | 6 historical checkpoint files removed |
| `history/2025-12-17-cleanup-notes.md` | created | Documents removal decision |
| `AGENTS.md` | modified | Updated Architecture and Important Files |
| `specs/checkpoint-format.md` | deleted | Duplicate of skill version |
| `specs/issues/done/ISSUE-012.md` | moved | From active/, all criteria checked |
| `specs/issues/done/spec-012.md` | moved | From active/ |
| `specs/issues/done/TASKS-012.md` | moved | From active/ |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| ISSUE-012 | Ready | Done |
| Active issues | 4 | 3 |
| Done issues | 7 | 8 |

---

## Delta: 2025-12-17T20:29:37Z

### What Changed

**Global skill synced** - Updated `/Users/mabrax/.claude/skills/coihuin-compress/` to match local repo.

### Session Work

1. Identified global skill was stale (missing ISSUE-006 and ISSUE-012 changes)
2. Synced files from local repo to global skill installation

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `~/.claude/skills/coihuin-compress/SKILL.md` | updated | Delta-as-operation model |
| `~/.claude/skills/coihuin-compress/checkpoint-format.md` | updated | Removed Example/References sections |
| `~/.claude/skills/coihuin-compress/examples/checkpoint-example.md` | created | New reference example |
| `~/.claude/skills/coihuin-compress/examples/checkpoint.md` | updated | Added Breadcrumbs section |
| `~/.claude/skills/coihuin-compress/delta-format.md` | deleted | Per ISSUE-006 simplification |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| Global skill | Stale (pre-ISSUE-006) | Synced with local repo |

---

## Delta: 2025-12-17T20:37:56Z

### What Changed

**ISSUE-010 implemented** - Archive lifecycle defined with marker file and documentation.

### Session Work

1. Compared remaining issues (007, 008, 010) for quick win
2. ISSUE-010 identified as trivial—implemented directly without spec
3. Created `.claudeignore` marker file in `checkpoints/archive/`
4. Added Archive Limitations section to SKILL.md
5. Updated directory structure documentation
6. Synced global skill

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `checkpoints/archive/.claudeignore` | created | Marker file with usage guidance |
| `checkpoints/archive/.gitkeep` | deleted | Replaced by .claudeignore |
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Archive Limitations + directory structure |
| `specs/issues/done/ISSUE-010.md` | moved | From active/, all criteria checked |
| `~/.claude/skills/coihuin-compress/SKILL.md` | synced | Global skill updated |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| ISSUE-010 | Draft | Done |
| Active issues | 3 | 2 |
| Done issues | 8 | 9 |

---

## Delta: 2025-12-17T20:56:59Z

### What Changed

**ISSUE-007 spec'd and tasks created** - Two-layer validation system fully specified with implementation plan.

### Session Work

1. **Created spec-007.md**:
   - Two-layer validation model (structural + semantic)
   - 8 advisory heuristics including 2 recency checks
   - Output format specification
   - LLM self-check guidance for SKILL.md

2. **Ran 3 parallel Explore agents for issue-spec coherence**:
   - Scope coverage: Found missing recency indicators
   - Acceptance criteria: PARTIAL (needed framing fixes)
   - Internal consistency: MAJOR ISSUES (3 layers vs 2, out-of-scope violation)

3. **Fixed coherence issues**:
   - Changed from 3 layers to 2 layers per issue Resolution
   - Removed out-of-scope AI analysis framing
   - Added recency heuristics (checkpoint age >7 days, last_delta >3 days)
   - Reframed heuristics as "advisory output" not separate layer

4. **Created TASKS-007.md**:
   - Phase 1: Rename script + update references
   - Phase 2: Remove stale delta validation
   - Phase 3: Add advisory heuristics
   - Phase 4: Update output format
   - Phase 5: Add SKILL.md self-check guidance
   - Phase 6: Validate and finalize

5. **Ran 3 parallel Explore agents for tasks validation**:
   - Tasks→Spec alignment: 73% direct, 27% valid additions
   - Spec→Tasks coverage: FULL (all 5 steps covered)
   - Junior readiness: 90% (3 clarifications needed)

6. **Fixed junior implementer clarity issues**:
   - Task 1.3: Made conditional explicit
   - Task 3.4: Added parsing examples + date format spec
   - Task 6.2: Added cleanup step

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `specs/issues/active/spec-007.md` | created | Two-layer validation specification |
| `specs/issues/active/TASKS-007.md` | created | 6-phase, 26-task implementation plan |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| ISSUE-007 | Draft | Ready |
| Active issues (ready) | 0 | 1 |
| Active issues (draft) | 2 | 1 |

---

## Delta: 2025-12-17T21:17:46Z

### What Changed

**ISSUE-007 implemented** - Two-layer validation system complete with advisory heuristics and semantic self-check guidance.

### Session Work

1. **Implemented ISSUE-007** via senior-implementer agent:
   - Phase 1: Renamed validate.py → format-check.py
   - Phase 2: Removed stale delta validation code
   - Phase 3: Added 8 advisory heuristics (content + recency checks)
   - Phase 4: Updated output format (structural/advisory sections)
   - Phase 5: Added Semantic Quality Self-Check to SKILL.md
   - Phase 6: Validated and moved issue to done/

2. **Analyzed external review** (4 issues flagged):
   - P0 (Delta validation dropped): FALSE POSITIVE—intentionally removed per ISSUE-006
   - P1 (.claudeignore format): TRUE POSITIVE—renamed to .archive-marker
   - P2 (Untracked script): FALSE POSITIVE—by design, no auto-commit
   - P3 (Delta docs missing): FALSE POSITIVE—depends on P0

3. **Fixed P1**: Renamed `.claudeignore` → `.archive-marker`, updated SKILL.md and README.md

4. **Committed changes**:
   - `8032abe`: feat(ISSUE-007): Implement two-layer validation system
   - `eaf17bf`: chore: Update checkpoint and finalize ISSUE-010

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `.claude/skills/coihuin-compress/format-check.py` | created | Renamed from validate.py, 8 advisory heuristics |
| `.claude/skills/coihuin-compress/validate.py` | deleted | Replaced by format-check.py |
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Semantic Quality Self-Check section added |
| `checkpoints/archive/.archive-marker` | renamed | From .claudeignore |
| `specs/issues/done/ISSUE-007.md` | moved | All criteria checked |
| `specs/issues/done/spec-007.md` | moved | Preserved with issue |
| `specs/issues/done/TASKS-007.md` | moved | 6-phase plan |
| `README.md` | modified | Validation section, archive marker |
| `STATUS.md` | modified | Script path |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| ISSUE-007 | Ready | Done |
| Active issues | 2 | 1 |
| Done issues | 9 | 10 |

---

## Delta: 2025-12-18T00:28:40Z

### What Changed

**ISSUE-008 implemented** - Proactive advisory triggers added to SKILL.md. All dialectic audit issues now complete.

### Session Work

1. **Researched proactive triggers** via claude-code-guide agent:
   - Validated "warnings not automation" approach aligns with Claude Code skill philosophy
   - Skills should be advisory, not autonomous
   - Description field triggers Claude's attention; user decides action

2. **Refined ISSUE-008 requirements**:
   - Context-aware advisory: checkpoint vs delta based on session state
   - Natural language suggestions (not slash commands—this is a skill)
   - Corrected research output that incorrectly suggested `/checkpoint`

3. **Created spec-008.md**:
   - 6 trigger conditions (phase completion, major decision, risky ops, etc.)
   - Context-aware advisory logic table
   - Natural language message examples
   - 4 advisory principles

4. **Implemented directly** (documentation-only, no TASKS file needed):
   - Updated SKILL.md description with advisory triggers
   - Revised "proactive" explanation blockquote
   - Added "Proactive Advisory Triggers" section with triggers table, examples, principles
   - Synced global skill

5. **Committed**: `c9945c9` feat(ISSUE-008): Add proactive advisory triggers to skill

### Artifacts

| File | Action | Description |
|------|--------|-------------|
| `specs/issues/active/ISSUE-008.md` | modified | Status ready, added refinement section |
| `specs/issues/active/spec-008.md` | created | Advisory triggers specification |
| `.claude/skills/coihuin-compress/SKILL.md` | modified | Description, proactive explanation, new section |
| `~/.claude/skills/coihuin-compress/SKILL.md` | synced | Global skill updated |
| `specs/issues/done/ISSUE-008.md` | moved | From active/, all criteria checked |
| `specs/issues/done/spec-008.md` | moved | From active/ |

### Status Transitions

| Item | Before | After |
|------|--------|-------|
| ISSUE-008 | Draft | Done |
| Active issues | 1 | 0 |
| Done issues | 10 | 11 |
| Backlog status | In progress | **Complete** |
