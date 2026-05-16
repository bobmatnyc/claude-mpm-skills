---
name: code-review-standards
description: "Severity-tagged code review checklist (CRITICAL/HIGH/MEDIUM/LOW) used by code-critic agent"
user-invocable: false
disable-model-invocation: true
license: Apache-2.0
compatibility: claude-code
progressive_disclosure:
  entry_point:
    summary: "Severity-tagged checklist for code review. CRITICAL/HIGH block delivery; MEDIUM is flagged; LOW is noted. Critic outputs APPROVE (zero CRITICAL/HIGH), WARN (some HIGH, no CRITICAL), or BLOCK (any CRITICAL). 80% confidence filter — don't manufacture findings."
    when_to_use: "Loaded by code-critic agent to apply structured review criteria. Also loaded by engineers to self-check before requesting review."
    quick_start: "Apply checklist top-to-bottom: CRITICAL first, then HIGH, MEDIUM, LOW. For each finding: cite file+line, explain why it's a problem, provide the fix. Filter to >80% confidence. Output verdict with finding table."
  references:
    - criteria-critical.md
    - criteria-high.md
    - criteria-medium.md
    - criteria-low.md
    - verdict-protocol.md
---

# Code Review Standards

## Purpose

This skill defines the structured checklist that the `code-critic` agent applies during
Stage 4 of the code production pipeline. The checklist is severity-tagged so that PM
and engineer both know exactly which findings block delivery and which are advisory.
Engineers may load this skill for self-review before requesting a critic pass.

The checklist exists because unstructured code review in multi-agent systems produces
inconsistent signal: one critic dispatch flags naming; another flags security; neither
flags the same things. Severity tagging makes the review deterministic across dispatches.

## The Severity-Tagged Checklist

### CRITICAL (must fix, blocks delivery)

- [ ] No secrets, API keys, or credentials hardcoded
- [ ] No SQL injection vectors (parameterized queries only)
- [ ] No arbitrary code execution paths (no `eval`, `exec`, unrestricted `pickle.loads`)
- [ ] Authentication/authorization not bypassable
- [ ] No infinite loops without escape conditions

### HIGH (must fix, blocks delivery)

- [ ] Type hints on all public functions and classes
- [ ] mypy --strict passes with zero errors
- [ ] pytest passes with zero failures
- [ ] Test coverage >= 90% on new code
- [ ] No bare except clauses
- [ ] No mutable default arguments
- [ ] No global mutable state
- [ ] No synchronous I/O inside async functions
- [ ] No N+1 query patterns
- [ ] Error cases handled explicitly (not silently swallowed)

### MEDIUM (flag, note in report, proceed)

- [ ] Functions <= 20 lines (prefer <= 10)
- [ ] No nested loops where hash map would reduce complexity
- [ ] list.pop(0) replaced with deque.popleft() where relevant
- [ ] asyncio.gather uses return_exceptions=True where appropriate
- [ ] Async operations have explicit timeouts
- [ ] Docstrings on public methods (Google or NumPy style)
- [ ] No Any types in production code paths

### LOW (note only)

- [ ] PEP 8 compliance (black + isort handles this automatically)
- [ ] Variable naming is clear and descriptive
- [ ] No commented-out code left in
- [ ] Import ordering is clean

## Verdict Format

Critic output MUST begin with the verdict on the first line, followed by the finding
table, followed by a summary paragraph.

**First line format:**
```
VERDICT: APPROVE
```
or
```
VERDICT: WARN
```
or
```
VERDICT: BLOCK
```

**Finding table format:**

| Severity | File | Line | Issue | Required Fix |
|----------|------|------|-------|--------------|
| CRITICAL | auth.py | 47 | Hardcoded API key `sk-...` | Move to env var; add to `.env.example` |
| HIGH | fetcher.py | 23 | `requests.get()` called inside `async def` | Replace with `await httpx.AsyncClient().get()` |
| MEDIUM | parser.py | 88 | Function is 34 lines | Extract `_parse_headers()` helper |

**Verdict definitions:**

| Verdict | Condition | PM Action |
|---------|-----------|-----------|
| APPROVE | Zero CRITICAL, zero HIGH findings | Proceed to Stage 5 (Security) |
| WARN | Zero CRITICAL, one or more HIGH findings | Proceed to Stage 5 with findings logged to docs handoff |
| BLOCK | Any CRITICAL finding (one or more) | Halt pipeline; surface findings to user; await user direction |

**APPROVE** means the implementation is ready for security review. MEDIUM and LOW findings
in an APPROVE review are passed to the Documentation agent as notes — they do not block
delivery but are preserved for future reference.

**WARN** means the implementation has structural issues that should be fixed but do not
represent exploitable defects or correctness failures. PM proceeds to security review
and appends the WARN finding table to the documentation handoff message. PM also logs
the findings (KB entry or todo) so they are not silently dropped.

**BLOCK** means the implementation has at least one defect that, if shipped, creates a
security vulnerability, data loss risk, or silent failure mode. PM halts the pipeline
immediately, presents the critic finding table verbatim to the user, and awaits explicit
direction. PM MUST NOT auto-retry the engineer without user input.

## 80% Confidence Filter

A clean review is a valid review. Do not manufacture findings.

Only report issues with >80% confidence they are real problems. Do not flag:
- Style preferences as HIGH or CRITICAL
- "This could theoretically be an issue in an edge case" without specific evidence
- Patterns that look unusual but may be intentional and correct
- Missing features that were not in scope (check the Stage 1 spec)

When confidence is below 80%, note the concern as a question in the summary paragraph
rather than as a finding in the table. Example: "The `process_batch()` function did not
appear to handle empty input — verify whether the caller guarantees non-empty batches."

This filter prevents the critic from becoming a noise generator that trains PM to
ignore findings. Each finding in the table should be actionable: engineer reads it,
knows exactly what to fix, and can do so without asking for clarification.

## Navigation

For detailed criteria with examples:
- **[CRITICAL Criteria](references/criteria-critical.md)**: Detailed explanations and examples for each CRITICAL item
- **[HIGH Criteria](references/criteria-high.md)**: Detailed explanations and examples for each HIGH item
- **[MEDIUM Criteria](references/criteria-medium.md)**: Detailed explanations and examples for each MEDIUM item
- **[LOW Criteria](references/criteria-low.md)**: Detailed explanations and examples for each LOW item
- **[Verdict Protocol](references/verdict-protocol.md)**: Full PM behavior for each verdict, failure loop templates
