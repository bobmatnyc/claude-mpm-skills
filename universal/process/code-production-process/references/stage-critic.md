# Stage 4: Critic Review — Detailed Protocol

## Purpose

The Critic stage provides an independent adversarial review of the implementation. By
dispatching a separate agent with context isolation, the pipeline catches issues that
the implementer — who already understands why they made each choice — cannot see
objectively. The critic's job is to find real problems, not to approve work.

## Agent and Skills

- **Agent:** `code-critic`
- **Skills loaded:** `code-review-standards`, `code-production-process`

## Context Isolation Requirement

The critic prompt MUST be constructed by PM, not by the engineer. See
`references/critic-isolation.md` for full rules. Short version:

- Include: Stage 1 spec, Stage 2 interface, Stage 3 source files, pytest output
- Exclude: engineer's commit message, stated rationale, design notes, PM summaries

## Dispatch Prompt Template

```
Code review task.

You are reviewing an implementation for correctness, quality, and security.
Apply the code-review-standards checklist (CRITICAL, HIGH, MEDIUM, LOW).

== SPEC (Stage 1 output) ==
[paste Stage 1 spec document verbatim]

== INTERFACE (Stage 2 output) ==
[paste Stage 2 interface specification verbatim]

== IMPLEMENTATION (Stage 3 source files) ==
[paste source file(s) verbatim — no paraphrasing, no summaries]

== TEST RESULTS (Stage 3 pytest output) ==
[paste pytest output verbatim]

Required output format:
1. VERDICT: APPROVE / WARN / BLOCK (first line of response)
2. Finding table (may be empty):
   | Severity | File | Line | Issue | Required Fix |
3. Summary paragraph explaining the verdict
```

## Verdict Definitions

| Verdict | Condition | PM Action |
|---------|-----------|-----------|
| APPROVE | Zero CRITICAL, zero HIGH | Proceed to Stage 5 |
| WARN | Zero CRITICAL, one or more HIGH | Proceed to Stage 5 with findings logged |
| BLOCK | Any CRITICAL | Halt pipeline, surface to user |

## Gate Checklist

Before accepting the critic output:

- [ ] Verdict is stated at the top (APPROVE / WARN / BLOCK)
- [ ] Finding table is present (even if empty)
- [ ] Each finding has file + line citation
- [ ] Summary paragraph explains the verdict
- [ ] No findings manufactured without >80% confidence (see code-review-standards)

## TODO: Expand with critic calibration guidance

<!-- TODO: Add examples of well-formed vs poorly-formed findings -->
<!-- TODO: Add guidance on how PM should evaluate suspiciously clean APPROVE verdicts -->
<!-- TODO: Add patterns for multi-file implementations (how to cite cross-file issues) -->
<!-- TODO: Add notes on the optional Phase 2 design critic pass (interface review before Stage 3) -->
