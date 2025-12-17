# Checkpoint Quality Evaluation Rubric

This document defines the scoring criteria for evaluating checkpoint quality. It serves as the canonical reference during checkpoint evaluations.

## Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| **Recoverability** | 30% | Could a fresh agent resume work from this alone? |
| **Completeness** | 20% | Are all required sections meaningfully filled? |
| **Clarity** | 20% | Is the language unambiguous without prior context? |
| **Token Efficiency** | 15% | Is information dense without unnecessary verbosity? |
| **Actionability** | 15% | Are Next Actions specific enough to execute? |

## Scoring Scale

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Exemplary; could be used as reference material |
| 4 | Good | Fully functional; minor improvements possible |
| 3 | Adequate | Works but has notable gaps or issues |
| 2 | Poor | Significant problems affecting recoverability |
| 1 | Failing | Missing critical information; unusable |

## Per-Dimension Criteria

### Recoverability (30%)

| Score | Criteria |
|-------|----------|
| 5 | Agent can resume immediately; all context present; no questions needed |
| 4 | Agent can resume with minimal inference; intent clear |
| 3 | Agent can resume but would need to rediscover some context |
| 2 | Significant gaps; agent would struggle to understand state |
| 1 | Incomplete to point of being misleading or useless |

### Completeness (20%)

| Score | Criteria |
|-------|----------|
| 5 | All sections filled with substantive content; nothing missing |
| 4 | All required sections present; optional sections used appropriately |
| 3 | Required sections present but some feel thin or templated |
| 2 | Missing sections or placeholder content |
| 1 | Skeleton only; most sections empty or boilerplate |

### Clarity (20%)

| Score | Criteria |
|-------|----------|
| 5 | Crystal clear to someone with zero prior context |
| 4 | Clear with minimal domain knowledge assumptions |
| 3 | Understandable but requires some inference |
| 2 | Ambiguous terms, unclear references, or jargon without explanation |
| 1 | Confusing or contradictory; would mislead a reader |

### Token Efficiency (15%)

| Score | Criteria |
|-------|----------|
| 5 | Every sentence carries information; no redundancy |
| 4 | Dense with minor verbosity |
| 3 | Some filler or repetition; could be tighter |
| 2 | Noticeably wordy; buries key information |
| 1 | Bloated; wastes significant tokens on noise |

### Actionability (15%)

| Score | Criteria |
|-------|----------|
| 5 | Next Actions are specific, sequenced, and immediately executable |
| 4 | Actions clear; minor ambiguity in sequencing or scope |
| 3 | Actions present but vague (e.g., "continue implementation") |
| 2 | Actions too broad or missing key steps |
| 1 | No actions, or actions that don't follow from checkpoint content |

## Promotion Criteria

A checkpoint is recommended for promotion when:

1. **Overall score >= 4.0**
2. **No dimension below 3**: A single failing dimension disqualifies
3. **Recoverability >= 4**: Core purpose must be strong

Promotion is always manual - the skill recommends, user decides.

## Score Calculation

```
Final dimension score = Preliminary score + Evidence modifier

Constraints:
- Cap at 5 (no score above 5)
- Floor at 1 (no score below 1)

Overall score = Weighted average of final dimension scores

Rounding: Round to one decimal place (e.g., 3.95 -> 4.0, 3.94 -> 3.9)
```

### Rounding Rules

| Calculated | Rounded | Promotion Eligible? |
|------------|---------|---------------------|
| 3.94 | 3.9 | No |
| 3.95 | 4.0 | Yes |
| 4.04 | 4.0 | Yes |
| 4.05 | 4.1 | Yes |

Standard rounding: >=0.05 rounds up, <0.05 rounds down.
