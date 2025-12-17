---
id: spec-011
title: Checkpoint Quality Evaluation Specification
issue: ISSUE-011
version: 1.0.0
created: 2025-12-17
---

# Checkpoint Quality Evaluation Specification

## Overview

**Checkpoint evaluation** is a dialectic process combining human perspective with agent investigation. It answers the question: "Could a fresh agent resume work from this checkpoint alone?"

A **fresh agent** is defined as: an agent with no conversation history, but with access to the skill instructions and ability to read project files. It knows *how* to work but not *what* was happening.

The evaluation has three phases:
1. **Human Interview**: Agent asks structured questions about each dimension
2. **Agent Investigation**: Explore agents examine actual artifacts and changes
3. **Correlation & Synthesis**: Agent correlates human answers with evidence, produces final score

This dialectic approach ensures evaluation reflects both subjective experience (human) and objective evidence (agent exploration).

### Scope

**In scope**: Full state checkpoints created during real project work.

**Out of scope**:
- Delta checkpoints (incremental changes between states)
- Breadcrumb-only files
- Partial or work-in-progress checkpoints
- Synthetic/crafted example checkpoints

## Design Principles

1. **Dialectic over monologue**: Human perspective + agent investigation = synthesized truth
2. **Evidence-based correlation**: Every score backed by correlation between human answers and found evidence
3. **Real over synthetic**: Evaluate checkpoints from actual messy work, not crafted examples
4. **Structured inquiry**: Consistent questions enable comparable evaluations
5. **Manual collection**: User decides which checkpoints to evaluate (no automatic scraping)
6. **Promotion through quality**: Only high-scoring checkpoints become examples

## Design Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| How to trigger? | Slash command `/eval-checkpoint` | Explicit invocation; integrates with Claude Code command system |
| Who collects checkpoints? | User manually copies to `eval/inbox/` | Respects project boundaries; user knows which checkpoints are interesting |
| Evaluation approach | Dialectic: human interview + agent investigation | Neither alone is sufficient; human knows intent, agent verifies evidence |
| Interview format | AskUserQuestion with structured options | Consistent data collection; comparable across evaluations |
| Investigation method | Explore agents examine artifacts | Parallel investigation of files, changes, breadcrumbs |
| Scoring mechanism | Correlation-based synthesis | Score derived from matching human claims with agent findings |
| Score format | 1-5 per dimension + overall | Granular enough to differentiate, simple enough to interpret |
| Promotion threshold | Overall score >= 4.0 | High bar ensures only quality examples; can adjust based on experience |
| Eval output format | Markdown with correlations + scores | Shows reasoning chain from evidence to score |

## Rubric Structure

### Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| **Recoverability** | 30% | Could a fresh agent resume work from this alone? |
| **Completeness** | 20% | Are all required sections meaningfully filled? |
| **Clarity** | 20% | Is the language unambiguous without prior context? |
| **Token Efficiency** | 15% | Is information dense without unnecessary verbosity? |
| **Actionability** | 15% | Are Next Actions specific enough to execute? |

### Scoring Scale

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Exemplary; could be used as reference material |
| 4 | Good | Fully functional; minor improvements possible |
| 3 | Adequate | Works but has notable gaps or issues |
| 2 | Poor | Significant problems affecting recoverability |
| 1 | Failing | Missing critical information; unusable |

### Per-Dimension Criteria

#### Recoverability (30%)

| Score | Criteria |
|-------|----------|
| 5 | Agent can resume immediately; all context present; no questions needed |
| 4 | Agent can resume with minimal inference; intent clear |
| 3 | Agent can resume but would need to rediscover some context |
| 2 | Significant gaps; agent would struggle to understand state |
| 1 | Incomplete to point of being misleading or useless |

#### Completeness (20%)

| Score | Criteria |
|-------|----------|
| 5 | All sections filled with substantive content; nothing missing |
| 4 | All required sections present; optional sections used appropriately |
| 3 | Required sections present but some feel thin or templated |
| 2 | Missing sections or placeholder content |
| 1 | Skeleton only; most sections empty or boilerplate |

#### Clarity (20%)

| Score | Criteria |
|-------|----------|
| 5 | Crystal clear to someone with zero prior context |
| 4 | Clear with minimal domain knowledge assumptions |
| 3 | Understandable but requires some inference |
| 2 | Ambiguous terms, unclear references, or jargon without explanation |
| 1 | Confusing or contradictory; would mislead a reader |

#### Token Efficiency (15%)

| Score | Criteria |
|-------|----------|
| 5 | Every sentence carries information; no redundancy |
| 4 | Dense with minor verbosity |
| 3 | Some filler or repetition; could be tighter |
| 2 | Noticeably wordy; buries key information |
| 1 | Bloated; wastes significant tokens on noise |

#### Actionability (15%)

| Score | Criteria |
|-------|----------|
| 5 | Next Actions are specific, sequenced, and immediately executable |
| 4 | Actions clear; minor ambiguity in sequencing or scope |
| 3 | Actions present but vague (e.g., "continue implementation") |
| 2 | Actions too broad or missing key steps |
| 1 | No actions, or actions that don't follow from checkpoint content |

## Directory Structure

```
eval/
├── inbox/              # Checkpoints awaiting evaluation
│   └── *.md            # Copied from real projects
├── scored/             # Evaluated checkpoints with scores
│   └── *.eval.md       # Original + evaluation results
├── promoted/           # High-scoring checkpoints ready for examples/
│   └── *.md            # Clean versions for skill use
└── rubric.md           # This rubric (canonical reference)
```

### File Naming

- **Inbox**: `{project}-{checkpoint-name}.md` (e.g., `pinta-feature-implementation.md`)
- **Scored**: `{original-name}.eval.md` (e.g., `pinta-feature-implementation.eval.md`)
- **Promoted**: Same as original, moved when score >= threshold

## Evaluation Workflow

```
1. User copies checkpoint to eval/inbox/
           │
           ▼
2. User runs: /eval-checkpoint <checkpoint-name>
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│ PHASE 1: Human Interview                                 │
│ Agent asks structured questions per dimension            │
│ Human provides perspective on checkpoint quality         │
└──────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│ PHASE 2: Agent Investigation                             │
│ Explore agents examine:                                  │
│ - Files mentioned in artifact trail                      │
│ - Breadcrumb references                                  │
│ - Git history for changes described                      │
│ - Current state vs checkpoint claims                     │
└──────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────┐
│ PHASE 3: Correlation & Synthesis                         │
│ Agent correlates human answers with evidence:            │
│ "Human said X → Found evidence Y → Conclusion Z"         │
│ Produces final scores with correlation rationale         │
└──────────────────────────────────────────────────────────┘
           │
           ▼
3. Results written to eval/scored/{name}.eval.md
           │
           ▼
4. If score >= 4.0, prompt user to promote
```

## Phase 1: Human Interview

The agent asks one question per dimension using AskUserQuestion. Questions are designed to capture the human's perspective on checkpoint quality.

### Interview Questions

#### Q1: Recoverability

**Question**: "If a fresh agent started tomorrow with only this checkpoint, how much context would they be missing?"

| Option | Label | Description |
|--------|-------|-------------|
| A | Nothing critical | Agent could resume immediately with full understanding |
| B | Minor gaps | Agent might need to re-read a file or two |
| C | Moderate gaps | Agent would need to rediscover some decisions or context |
| D | Significant gaps | Agent would struggle; key information is missing |
| E | Unusable | Agent would be completely lost; checkpoint is misleading or empty |

#### Q2: Completeness

**Question**: "Looking at the checkpoint sections (Problem, Essential Information, Artifact Trail, Next Actions), are there any that feel thin or missing?"

| Option | Label | Description |
|--------|-------|-------------|
| A | All solid | Every section has substantive, useful content |
| B | Mostly complete | One section could use more detail |
| C | Some gaps | A few sections feel thin or templated |
| D | Incomplete | Missing sections or placeholder content |
| E | Skeleton only | Most sections empty, boilerplate, or missing entirely |

#### Q3: Clarity

**Question**: "Could a developer unfamiliar with this project understand the checkpoint?"

| Option | Label | Description |
|--------|-------|-------------|
| A | Crystal clear | Understandable with only general programming knowledge |
| B | Mostly clear | Minor assumptions about domain knowledge |
| C | Requires inference | Some terms or references need explanation |
| D | Confusing | Would mislead someone without context |
| E | Incomprehensible | Contradictory, incoherent, or assumes undocumented context |

#### Q4: Token Efficiency

**Question**: "How would you describe the information density of this checkpoint?"

| Option | Label | Description |
|--------|-------|-------------|
| A | Very dense | Every sentence carries weight; no wasted tokens |
| B | Mostly efficient | Minor wordiness in places |
| C | Adequate | Some filler or repetition; could be tighter |
| D | Verbose | Noticeably wordy; buries key information |
| E | Bloated | Excessive redundancy; wastes significant tokens |

#### Q5: Actionability

**Question**: "Are the Next Actions specific enough to execute without clarification?"

| Option | Label | Description |
|--------|-------|-------------|
| A | Immediately executable | Clear sequence, specific tasks |
| B | Mostly clear | Minor ambiguity in scope or order |
| C | Vague | Actions present but not specific |
| D | Not actionable | Actions too broad or missing key steps |
| E | Missing or incoherent | No actions, or actions contradict checkpoint content |

### Answer Mapping

| Answer | Preliminary Score |
|--------|-------------------|
| A | 5 |
| B | 4 |
| C | 3 |
| D | 2 |
| E | 1 |

Note: Preliminary scores are adjusted in Phase 3 based on evidence correlation.

## Phase 2: Agent Investigation

After collecting human answers, the agent launches investigation tasks to gather evidence. All investigations are read-only and can safely run in parallel.

### Investigation Tasks

The evaluation spawns 3 parallel investigation tasks using the Task tool with `subagent_type: Explore`:

| Task | Target Sections | Tools Used | Evidence Sought |
|------|-----------------|------------|-----------------|
| **Artifact Verification** | Artifact Trail | Read, Glob | Do files exist? Match description? |
| **Breadcrumb Validation** | Breadcrumbs | Read, Grep, WebFetch | Are references valid and accessible? |
| **Git Correlation** | Play-by-Play | Bash (git log) | Do commits match described changes? |

### Task Specifications

**Task 1: Artifact Verification**
```
Prompt: "Verify the artifact trail from this checkpoint. For each file listed:
1. Check if file exists at the stated path (use Glob)
2. Read the file and verify it matches the description
3. Report: file path, claimed state, actual state, match (true/false/partial)

Checkpoint artifact trail:
[extracted from checkpoint]"
```

**Task 2: Breadcrumb Validation**
```
Prompt: "Validate breadcrumb references from this checkpoint. For each breadcrumb:
- file: Check file exists (Glob/Read)
- function: Grep for function definition
- external: WebFetch to check URL accessibility (200 = valid, 404 = broken)
- decision: Mark as 'no verification possible'

Report: type, reference, status (valid/broken/unverifiable)

Checkpoint breadcrumbs:
[extracted from checkpoint]"
```

**Task 3: Git Correlation**
```
Prompt: "Correlate play-by-play entries with git history.
1. Run: git log --oneline -20 --since='7 days ago'
2. For each play-by-play entry that describes a change, check if a
   matching commit exists (keyword matching)
3. Report: play-by-play entry, matching commit (if any), status

Checkpoint play-by-play:
[extracted from checkpoint]"
```

### Evidence Collection Format

Each task returns structured findings with confidence and severity:

```yaml
task: "artifact_verification"
status: complete  # complete | partial | failed
findings:
  - item: "src/services/auth.ts"
    claimed: "Added retry logic"
    found: "File exists, contains retryWithBackoff function at line 45"
    match: true
    confidence: high  # high | medium | low
  - item: "src/lib/utils.ts"
    claimed: "New helper functions"
    found: "File not found at path"
    match: false
    confidence: high
    severity: major  # major | minor | info
  - item: "config/settings.json"
    claimed: "Updated configuration"
    found: "File exists but no obvious config changes visible"
    match: partial
    confidence: medium
    severity: minor
summary:
  total: 3
  verified: 1
  failed: 1
  partial: 1
notes: "One file missing, one inconclusive"
```

### Confidence Levels

| Level | When to Use |
|-------|-------------|
| **high** | Objective verification (file exists/doesn't, URL returns 404) |
| **medium** | Subjective match (description matches content but requires interpretation) |
| **low** | Unable to fully verify (e.g., "improved performance" claim) |

### Severity Levels

| Level | When to Use |
|-------|-------------|
| **major** | Core artifact missing or fundamentally wrong |
| **minor** | Secondary artifact issue or partial mismatch |
| **info** | Observation that may or may not indicate a problem |

### Edge Case Handling

| Edge Case | Handling |
|-----------|----------|
| **Empty section** | Task returns `status: complete` with `findings: []` and note "Section empty" |
| **No git history** | Git task returns `status: partial` with note "No commits in range" |
| **Auth-required URL** | Mark as `unverifiable` with note "Authentication required" |
| **Renamed/moved file** | Report as `match: false` with note suggesting possible rename |
| **Checkpoint has no breadcrumbs** | Breadcrumb task returns `status: complete`, `findings: []` |
| **Task timeout/failure** | Return `status: failed` with error message; correlation uses "no evidence" |

## Phase 3: Correlation & Synthesis

The agent correlates human answers with investigation evidence to produce final scores.

### Correlation Logic

For each dimension:

1. **Start with human preliminary score** (from interview)
2. **Aggregate evidence** from all relevant investigation tasks
3. **Apply evidence modifier** based on thresholds below
4. **Document correlation chain**: "Human said X → Found Y → Final score Z because..."

### Modifier Decision Rules

| Modifier | Threshold | When to Apply |
|----------|-----------|---------------|
| **+1 (Strong support)** | >90% verified, 0 major issues | Evidence exceeds human claim |
| **0 (Supports)** | 70-90% verified, ≤1 major issue | Evidence matches human claim |
| **-1 (Minor contradiction)** | 50-70% verified, or 2 major issues | Evidence shows more issues than claimed |
| **-2 (Major contradiction)** | <50% verified, or ≥3 major issues, or critical claim false | Evidence fundamentally contradicts claim |

**Calculation for "% verified"**:
```
verified_rate = (verified + 0.5 * partial) / total_findings
```

### Handling Mixed Evidence

When evidence is mixed (some good, some bad):

1. **Count issues by severity**: major issues weigh more than minor
2. **Calculate verification rate** across all findings
3. **Apply the most conservative modifier** that fits the thresholds
4. **Document the conflict** in correlation analysis

Example:
```
Evidence: 3/5 artifacts verified, 1 partial, 1 missing (major)
Calculation: (3 + 0.5×1) / 5 = 70% → borderline
Major issues: 1
Result: Modifier = 0 (supports) — 70% verified with 1 major issue
```

### Handling Ambiguous Evidence

When evidence is unclear or conflicting:

1. **Default to 0 modifier** (trust human assessment)
2. **Flag uncertainty** in correlation notes
3. **For borderline promotion cases (3.8-4.2)**, recommend manual review

### Dimension-Specific Evidence Mapping

| Dimension | Primary Evidence Sources | Secondary Sources |
|-----------|-------------------------|-------------------|
| Recoverability | Artifact trail, breadcrumbs | Git correlation |
| Completeness | All sections present check | Artifact trail |
| Clarity | N/A (human-only) | — |
| Token Efficiency | N/A (human-only) | — |
| Actionability | Artifact trail (preconditions) | Git correlation |

Note: Clarity and Token Efficiency have no objective verification. These dimensions use modifier = 0 (accept human assessment) unless investigation reveals contradicting structural evidence (e.g., Next Actions section is empty).

### Correlation Examples

**Recoverability**:
```
Human answer: B (Minor gaps) → Preliminary: 4
Evidence:
- Artifact trail: 5/5 files verified (100%) ✓
- Breadcrumbs: 3/4 valid, 1 stale reference (75%)
- Combined: 8/9 = 89% verified, 0 major issues
Correlation: Human's "minor gaps" assessment aligns with evidence.
One stale breadcrumb is indeed a minor gap.
Modifier: 0 (supports) — 89% verified, within 70-90% range
Final score: 4
```

**Completeness**:
```
Human answer: A (All solid) → Preliminary: 5
Evidence:
- Artifact trail: 2/3 files verified (67%)
- Missing: config/settings.json (major)
- Broken: external URL (major)
- Combined: 67% verified, 2 major issues
Correlation: Human claimed "all solid" but multiple artifacts
are missing or broken. Evidence contradicts assessment.
Modifier: -2 (major contradiction) — <70% verified with 2 major issues
Final score: 3
```

### Score Calculation

```
Final dimension score = Preliminary score + Evidence modifier

Constraints:
- Cap at 5 (no score above 5)
- Floor at 1 (no score below 1)

Overall score = Weighted average of final dimension scores

Rounding: Round to one decimal place (e.g., 3.95 → 4.0, 3.94 → 3.9)
```

### Rounding Rules

| Calculated | Rounded | Promotion Eligible? |
|------------|---------|---------------------|
| 3.94 | 3.9 | No |
| 3.95 | 4.0 | Yes |
| 4.04 | 4.0 | Yes |
| 4.05 | 4.1 | Yes |

Standard rounding: ≥0.05 rounds up, <0.05 rounds down.

## Evaluation Output Format

Scored checkpoints include the original content plus an evaluation section with correlation analysis:

```markdown
---
[original frontmatter]
eval:
  date: 2025-12-17
  overall: 4.0
  scores:
    recoverability:
      option: B
      human: 4
      modifier: 0
      final: 4
    completeness:
      option: A
      human: 5
      modifier: -2
      final: 3
    clarity:
      option: B
      human: 4
      modifier: 0
      final: 4
    token_efficiency:
      option: B
      human: 4
      modifier: 0
      final: 4
    actionability:
      option: B
      human: 4
      modifier: 1
      final: 5
  evidence_summary:
    artifacts_verified: "2/3"
    breadcrumbs_valid: "2/3"
    git_commits_matched: "1/2"
  recommendation: promote
---

[original checkpoint content]

---

## Evaluation Results

**Overall Score: 4.0/5** (Promote: Yes)

### Human Interview Responses

| Dimension | Response | Preliminary Score |
|-----------|----------|-------------------|
| Recoverability | B - Minor gaps | 4 |
| Completeness | A - All solid | 5 |
| Clarity | B - Mostly clear | 4 |
| Token Efficiency | B - Mostly efficient | 4 |
| Actionability | B - Mostly clear | 4 |

### Agent Investigation Findings

**Artifact Trail Verification**:
- `src/services/auth.ts`: Found, matches description ✓
- `src/lib/retry.ts`: Found, matches description ✓
- `config/settings.json`: NOT FOUND ✗

**Breadcrumb Validation**:
- `file: src/middleware/cors.ts`: Valid ✓
- `function: authService.validateToken()`: Valid ✓
- `external: https://docs.example.com/auth`: 404 Not Found ✗

**Git Correlation**:
- Play-by-play mentions "added retry logic" → commit abc123 confirms ✓
- Play-by-play mentions "updated config" → no matching commit ✗

### Correlation Analysis

**Recoverability (Human: 4 → Final: 4)**
- Human said: "Minor gaps - agent might need to re-read a file or two"
- Evidence: 2/3 artifact files verified, 2/3 breadcrumbs valid
- Correlation: Human assessment accurate. Minor gaps exist but recoverable.
- Modifier: 0 (supports)

**Completeness (Human: 5 → Final: 3)**
- Human said: "All solid - every section has substantive content"
- Evidence: Missing config file, one broken external link, no commit for "updated config"
- Correlation: Human overestimated. Multiple artifacts don't match claimed state.
- Modifier: -2 (major contradiction)

**Clarity (Human: 4 → Final: 4)**
- Human said: "Mostly clear - minor assumptions about domain knowledge"
- Evidence: Technical context accurately describes architecture. Terms well-defined.
- Correlation: Human assessment accurate.
- Modifier: 0 (supports)

**Token Efficiency (Human: 4 → Final: 4)**
- Human said: "Mostly efficient - minor wordiness in places"
- Evidence: N/A (no objective verification possible for this dimension)
- Correlation: Accepting human assessment; no contradicting evidence.
- Modifier: 0 (no evidence)

**Actionability (Human: 4 → Final: 5)**
- Human said: "Mostly clear - minor ambiguity in scope or order"
- Evidence: All preconditions for next actions are met. Files exist, tests pass.
- Correlation: Human underestimated. Actions are more executable than claimed.
- Modifier: +1 (strong support)

### Final Scores

| Dimension | Human | Evidence | Final | Weight | Weighted |
|-----------|-------|----------|-------|--------|----------|
| Recoverability | 4 | supports | 4 | 30% | 1.20 |
| Completeness | 5 | contradicts | 3 | 20% | 0.60 |
| Clarity | 4 | supports | 4 | 20% | 0.80 |
| Token Efficiency | 4 | no evidence | 4 | 15% | 0.60 |
| Actionability | 4 | strong support | 5 | 15% | 0.75 |
| **Total** | | | | | **3.95 → 4.0** |

### Suggestions for Improvement

1. Add missing `config/settings.json` or remove from artifact trail
2. Update external breadcrumb URL (currently 404)
3. Either add commit for "updated config" or remove from play-by-play
```

## Slash Command

The evaluation is triggered via a slash command:

```
/eval-checkpoint <checkpoint-name>
```

### Command File

Location: `.claude/commands/eval-checkpoint.md`

```markdown
Evaluate a checkpoint using the dialectic eval process.

## Arguments

$ARGUMENTS: Name of checkpoint file in eval/inbox/
- Strip .md extension if provided
- Example: Both "pinta-auth-feature" and "pinta-auth-feature.md" work

## Error Handling

Before starting evaluation, verify preconditions:

1. **File not found**: If eval/inbox/$ARGUMENTS.md doesn't exist:
   - List available files in eval/inbox/
   - Ask user to confirm correct filename
   - Do not proceed until valid file provided

2. **Malformed checkpoint**: If checkpoint is missing required sections:
   - Note missing sections as evidence (affects Completeness score)
   - Continue evaluation with available content
   - Flag structural issues in output

3. **Investigation failures**:
   - If git history unavailable: Note "no git data" in findings
   - If external URL auth-required: Mark as "unverifiable"
   - If task times out: Use "no evidence" for that task
   - Never fail entire evaluation due to single task failure

4. **Empty eval/inbox/**: If directory is empty:
   - Inform user: "No checkpoints in eval/inbox/"
   - Provide instructions for adding checkpoints

## Process

### Phase 1: Human Interview

Read the checkpoint from eval/inbox/$ARGUMENTS.md, then ask the user
5 questions using AskUserQuestion (one per dimension). Each question
has 5 options (A-E) with labels and descriptions per the rubric.

Questions:
1. Recoverability: "If a fresh agent started tomorrow with only this
   checkpoint, how much context would they be missing?"
2. Completeness: "Looking at the checkpoint sections (Problem, Essential
   Information, Artifact Trail, Next Actions), are there any that feel
   thin or missing?"
3. Clarity: "Could a developer unfamiliar with this project understand
   the checkpoint?"
4. Token Efficiency: "How would you describe the information density
   of this checkpoint?"
5. Actionability: "Are the Next Actions specific enough to execute
   without clarification?"

Record answers and map to preliminary scores:
- A=5, B=4, C=3, D=2, E=1

### Phase 2: Agent Investigation

Launch 3 investigation tasks in parallel using Task tool with
subagent_type: Explore:

1. **Artifact Verification**: Extract artifact trail from checkpoint,
   verify each file exists and matches description using Glob/Read
2. **Breadcrumb Validation**: Extract breadcrumbs, verify references
   using Read/Grep/WebFetch as appropriate
3. **Git Correlation**: Extract play-by-play, run git log to find
   matching commits

Each task returns structured findings with:
- item, claimed, found, match, confidence, severity

### Phase 3: Correlation & Synthesis

For each dimension:
1. Start with human preliminary score
2. Aggregate evidence from relevant tasks
3. Calculate verification rate and count major issues
4. Apply modifier per thresholds:
   - >90% verified, 0 major: +1
   - 70-90% verified, ≤1 major: 0
   - 50-70% verified, or 2 major: -1
   - <50% verified, or ≥3 major: -2
5. Document correlation chain

Calculate weighted overall score (round to 1 decimal).

### Output

Write results to eval/scored/$ARGUMENTS.eval.md including:
- YAML frontmatter with scores and evidence summary
- Human interview responses table
- Agent investigation findings (with ✓/✗ markers)
- Correlation analysis per dimension
- Final scores table with weights
- Suggestions for improvement

### Promotion

If overall score >= 4.0 AND no dimension below 3 AND Recoverability >= 4:
- Ask user: "This checkpoint scored X/5. Promote to eval/promoted/?"
- If yes: Copy to eval/promoted/$ARGUMENTS.md (without .eval suffix)
- If no: Evaluation complete
```

### Usage Examples

```bash
# Evaluate a specific checkpoint
/eval-checkpoint pinta-auth-feature

# The command will:
# 1. Read eval/inbox/pinta-auth-feature.md
# 2. Ask you 5 interview questions (A-E options each)
# 3. Launch 3 parallel investigation tasks
# 4. Correlate answers with evidence
# 5. Produce eval/scored/pinta-auth-feature.eval.md
# 6. Offer promotion if score qualifies
```

## Promotion Criteria

A checkpoint is recommended for promotion when:

1. **Overall score >= 4.0**
2. **No dimension below 3**: A single failing dimension disqualifies
3. **Recoverability >= 4**: Core purpose must be strong

Promotion is always manual—the skill recommends, user decides.

## Integration with Skill

### SKILL.md Updates

Add reference to the eval command:

```markdown
## Checkpoint Evaluation

Use `/eval-checkpoint <name>` to evaluate checkpoints in eval/inbox/.

The evaluation process:
1. Asks you 5 questions about checkpoint quality (one per dimension)
2. Launches agents to verify artifacts, breadcrumbs, and git history
3. Correlates your answers with evidence found
4. Produces scored output with correlation analysis

See eval/rubric.md for scoring criteria.
```

### Feedback Loop

High-quality evaluated checkpoints inform skill improvement:

1. Patterns in 5-score checkpoints → reinforce in guidance
2. Common issues in low scores → add warnings or examples
3. Dimension score distributions → adjust rubric weights if needed
4. Correlation patterns → identify where human perception diverges from evidence

## Token Economics

| Item | Approximate Tokens |
|------|-------------------|
| Phase 1: Interview | ~200 tokens (questions + responses) |
| Phase 2: Investigation | ~1000-2000 tokens (agent exploration) |
| Phase 3: Correlation | ~500-800 tokens (analysis + scoring) |
| Rubric (reference) | ~800 tokens |
| Checkpoint (input) | ~500-1500 tokens |
| Evaluation output | ~800-1200 tokens |
| **Total per evaluation** | **~3800-6500 tokens** |

The dialectic process is more expensive than simple LLM-as-judge but produces more reliable, evidence-backed scores. Evaluation remains an occasional operation.

## References

- ISSUE-011: Original issue defining the eval mechanism
- history/2025-12-16-dialectic-audit.md: Dialectic audit where this emerged (Discussion 2)
- Factory.ai: "Compressing Context" - Quality verification concepts
