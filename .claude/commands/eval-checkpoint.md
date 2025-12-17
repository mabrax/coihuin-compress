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

**Question 1 - Recoverability**:
"If a fresh agent started tomorrow with only this checkpoint, how much context would they be missing?"

| Option | Label | Description |
|--------|-------|-------------|
| A | Nothing critical | Agent could resume immediately with full understanding |
| B | Minor gaps | Agent might need to re-read a file or two |
| C | Moderate gaps | Agent would need to rediscover some decisions or context |
| D | Significant gaps | Agent would struggle; key information is missing |
| E | Unusable | Agent would be completely lost; checkpoint is misleading or empty |

**Question 2 - Completeness**:
"Looking at the checkpoint sections (Problem, Essential Information, Artifact Trail, Next Actions), are there any that feel thin or missing?"

| Option | Label | Description |
|--------|-------|-------------|
| A | All solid | Every section has substantive, useful content |
| B | Mostly complete | One section could use more detail |
| C | Some gaps | A few sections feel thin or templated |
| D | Incomplete | Missing sections or placeholder content |
| E | Skeleton only | Most sections empty, boilerplate, or missing entirely |

**Question 3 - Clarity**:
"Could a developer unfamiliar with this project understand the checkpoint?"

| Option | Label | Description |
|--------|-------|-------------|
| A | Crystal clear | Understandable with only general programming knowledge |
| B | Mostly clear | Minor assumptions about domain knowledge |
| C | Requires inference | Some terms or references need explanation |
| D | Confusing | Would mislead someone without context |
| E | Incomprehensible | Contradictory, incoherent, or assumes undocumented context |

**Question 4 - Token Efficiency**:
"How would you describe the information density of this checkpoint?"

| Option | Label | Description |
|--------|-------|-------------|
| A | Very dense | Every sentence carries weight; no wasted tokens |
| B | Mostly efficient | Minor wordiness in places |
| C | Adequate | Some filler or repetition; could be tighter |
| D | Verbose | Noticeably wordy; buries key information |
| E | Bloated | Excessive redundancy; wastes significant tokens |

**Question 5 - Actionability**:
"Are the Next Actions specific enough to execute without clarification?"

| Option | Label | Description |
|--------|-------|-------------|
| A | Immediately executable | Clear sequence, specific tasks |
| B | Mostly clear | Minor ambiguity in scope or order |
| C | Vague | Actions present but not specific |
| D | Not actionable | Actions too broad or missing key steps |
| E | Missing or incoherent | No actions, or actions contradict checkpoint content |

**Answer Mapping**:
Record answers and map to preliminary scores:
- A=5, B=4, C=3, D=2, E=1

### Phase 2: Agent Investigation

Launch 3 investigation tasks in parallel using Task tool with
subagent_type: Explore:

**Task 1 - Artifact Verification**:
Extract artifact trail from checkpoint, verify each file exists and matches description using Glob/Read.

Prompt: "Verify the artifact trail from this checkpoint. For each file listed:
1. Check if file exists at the stated path (use Glob)
2. Read the file and verify it matches the description
3. Report: file path, claimed state, actual state, match (true/false/partial)

Return structured findings with: item, claimed, found, match, confidence (high/medium/low), severity (major/minor/info if mismatch)"

**Task 2 - Breadcrumb Validation**:
Extract breadcrumbs, verify references using Read/Grep/WebFetch as appropriate.

Prompt: "Validate breadcrumb references from this checkpoint. For each breadcrumb:
- file: Check file exists (Glob/Read)
- function: Grep for function definition
- external: WebFetch to check URL accessibility (200 = valid, 404 = broken)
- decision: Mark as 'no verification possible'

Return: type, reference, status (valid/broken/unverifiable)"

**Task 3 - Git Correlation**:
Extract play-by-play, run git log to find matching commits.

Prompt: "Correlate play-by-play entries with git history.
1. Run: git log --oneline -20 --since='7 days ago'
2. For each play-by-play entry that describes a change, check if a matching commit exists (keyword matching)
3. Return: play-by-play entry, matching commit (if any), status"

**Evidence Collection Format**:
Each task returns structured findings:
```yaml
task: "<task_name>"
status: complete  # complete | partial | failed
findings:
  - item: "<path or reference>"
    claimed: "<what checkpoint says>"
    found: "<what was actually found>"
    match: true|false|partial
    confidence: high|medium|low
    severity: major|minor|info  # only for mismatches
summary:
  total: N
  verified: N
  failed: N
  partial: N
notes: "<any relevant observations>"
```

**Edge Case Handling**:
- Empty section: Task returns status: complete with findings: [] and note "Section empty"
- No git history: Git task returns status: partial with note "No commits in range"
- Auth-required URL: Mark as unverifiable with note "Authentication required"
- Checkpoint has no breadcrumbs: Breadcrumb task returns status: complete, findings: []

### Phase 3: Correlation & Synthesis

For each dimension:
1. Start with human preliminary score
2. Aggregate evidence from relevant tasks
3. Calculate verification rate and count major issues
4. Apply modifier per thresholds:

| Modifier | Threshold | When to Apply |
|----------|-----------|---------------|
| +1 (Strong support) | >90% verified, 0 major issues | Evidence exceeds human claim |
| 0 (Supports) | 70-90% verified, <=1 major issue | Evidence matches human claim |
| -1 (Minor contradiction) | 50-70% verified, or 2 major issues | Evidence shows more issues than claimed |
| -2 (Major contradiction) | <50% verified, or >=3 major issues, or critical claim false | Evidence fundamentally contradicts claim |

**Verification Rate Calculation**:
```
verified_rate = (verified + 0.5 * partial) / total_findings
```

**Dimension-Specific Evidence Mapping**:

| Dimension | Primary Evidence Sources | Secondary Sources |
|-----------|-------------------------|-------------------|
| Recoverability | Artifact trail, breadcrumbs | Git correlation |
| Completeness | All sections present check | Artifact trail |
| Clarity | N/A (human-only) | - |
| Token Efficiency | N/A (human-only) | - |
| Actionability | Artifact trail (preconditions) | Git correlation |

Note: Clarity and Token Efficiency have no objective verification. Use modifier = 0 (accept human assessment) unless investigation reveals contradicting structural evidence.

5. Document correlation chain: "Human said X -> Found Y -> Final score Z because..."

**Score Calculation**:
```
Final dimension score = Preliminary score + Evidence modifier

Constraints:
- Cap at 5 (no score above 5)
- Floor at 1 (no score below 1)

Overall score = Weighted average of final dimension scores

Weights:
- Recoverability: 30%
- Completeness: 20%
- Clarity: 20%
- Token Efficiency: 15%
- Actionability: 15%

Rounding: Round to one decimal place (>=0.05 rounds up, <0.05 rounds down)
```

## Output

Write results to eval/scored/$ARGUMENTS.eval.md including:

**YAML Frontmatter**:
```yaml
---
[original frontmatter preserved]
eval:
  date: <current date>
  overall: <weighted score>
  scores:
    recoverability:
      option: <A-E>
      human: <1-5>
      modifier: <-2 to +1>
      final: <1-5>
    completeness:
      option: <A-E>
      human: <1-5>
      modifier: <-2 to +1>
      final: <1-5>
    clarity:
      option: <A-E>
      human: <1-5>
      modifier: <-2 to +1>
      final: <1-5>
    token_efficiency:
      option: <A-E>
      human: <1-5>
      modifier: <-2 to +1>
      final: <1-5>
    actionability:
      option: <A-E>
      human: <1-5>
      modifier: <-2 to +1>
      final: <1-5>
  evidence_summary:
    artifacts_verified: "X/Y"
    breadcrumbs_valid: "X/Y"
    git_commits_matched: "X/Y"
  recommendation: promote|no_promote
---
```

**Body Content**:
1. [Original checkpoint content]
2. Horizontal rule separator
3. Evaluation Results section:
   - Overall Score header with promote recommendation
   - Human Interview Responses table
   - Agent Investigation Findings (with checkmarks/X markers)
   - Correlation Analysis per dimension
   - Final Scores table with weights and weighted values
   - Suggestions for Improvement (based on issues found)

## Promotion

If overall score >= 4.0 AND no dimension below 3 AND Recoverability >= 4:
- Ask user: "This checkpoint scored X/5. Promote to eval/promoted/?"
- If yes: Copy to eval/promoted/$ARGUMENTS.md (without .eval suffix)
- If no: Evaluation complete

If criteria not met:
- Report which criteria failed
- Evaluation complete (no promotion prompt)
