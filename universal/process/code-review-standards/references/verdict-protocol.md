# Verdict Protocol — Full PM Behavior

## Overview

The verdict protocol defines exactly what PM does after receiving a critic verdict.
PM MUST NOT use judgment to soften, override, or reinterpret the verdict. The protocol
is deterministic: verdict in → PM action out.

---

## APPROVE

**Condition:** Zero CRITICAL findings AND zero HIGH findings.

**PM Actions:**

1. Proceed to Stage 5 (Security) — dispatch security agent immediately
2. Pass any MEDIUM/LOW findings from the finding table to the Documentation agent
   handoff message as "notes for future reference — not blocking"
3. No further action required from engineer

**Critic output may include MEDIUM/LOW findings in an APPROVE.** Those findings are
informational only and do not affect the pipeline continuation.

**PM handoff template to Security agent:**
```
Security review task — implementation cleared Stage 4 (Critic: APPROVE).

[paste Stage 3 source files verbatim]

Critic APPROVE finding table (MEDIUM/LOW only, FYI):
[paste table if non-empty, or omit if empty]

Apply OWASP Top 10 security review. Output SECURITY VERDICT as first line.
```

---

## WARN

**Condition:** Zero CRITICAL findings AND one or more HIGH findings.

**PM Actions:**

1. Proceed to Stage 5 (Security) — do NOT halt the pipeline
2. Append the full critic finding table to the Documentation agent handoff message
   (not just a summary — the full table with file+line citations)
3. Log the findings in a persistent note:
   - KB entry with topic "code-review-findings", or
   - Todo tracker entry for the implementing engineer
4. PM MUST NOT silently discard HIGH findings — they must appear somewhere persistent

**WARN does not require engineer action before Stage 5.** If user later requests
fixes for the HIGH findings, engineer resolves them without a re-critic pass.

**PM session log entry (required for WARN):**
```
WARN logged: critic found HIGH issues in [task name], [date].
High findings: [brief description of each HIGH item]
Tracked in: [KB entry ID or todo ID]
```

**PM handoff template to Security agent:**
```
Security review task — implementation cleared Stage 4 (Critic: WARN — HIGH findings logged).

[paste Stage 3 source files verbatim]

Critic WARN finding table (HIGH findings — logged for follow-up, not blocking):
[paste full finding table]

Apply OWASP Top 10 security review. Output SECURITY VERDICT as first line.
```

---

## BLOCK

**Condition:** Any CRITICAL finding (one or more).

**PM Actions:**

1. Halt the pipeline immediately — do NOT dispatch security agent
2. Surface the critic finding table verbatim to the user
3. State exactly:

```
Critic has blocked this implementation. The following CRITICAL issue(s) must be
resolved before the pipeline can continue. Please confirm your direction:

[paste full finding table, CRITICAL items highlighted]

Options:
A) Fix and retry — return to Stage 3 with these findings as input
B) Override with justification — provide written justification; PM logs and proceeds
C) Abandon — discard this implementation

Awaiting your direction.
```

4. Await explicit user response — do NOT auto-retry

**PM MUST NOT auto-delegate to engineer after a BLOCK without user input.** This is
the key safeguard: the user must consciously decide to retry, not have PM silently
loop.

**When user selects "Fix and retry":**

Return to Stage 3. Dispatch the engineer with this additional input alongside the
original Stage 1 spec and Stage 2 interface:

```
PIPELINE GATE FAILURE — Return to Stage 3

Critic verdict: BLOCK
CRITICAL findings requiring resolution:

[paste finding table, CRITICAL rows only]

Instructions:
- Fix ALL CRITICAL items above
- Re-run pytest (must pass green)
- Re-run mypy --strict (must pass)
- Return updated source files with fresh test output

Do NOT return until all CRITICAL findings are resolved and tests pass.
If fixing a CRITICAL item requires changing the Stage 2 interface, flag to PM
before proceeding — do not change the public API unilaterally.
```

**When user selects "Override with justification":**

PM logs the override in a KB entry:
```
Override logged: critic BLOCK bypassed for [task], [date].
Justification: [user's stated justification verbatim]
CRITICAL findings overridden: [list]
```

PM then proceeds to Stage 5 (Security) — a BLOCK override does not skip security.

---

## Return-to-Stage-2 Condition

If the CRITICAL finding reveals a fundamental flaw in the Stage 2 interface itself
(not just the implementation), PM returns to Stage 2, not Stage 3.

**Example:** Critic flags that the authentication interface has no mechanism to
represent authentication failure (returns `User | None` but the type system allows
`None` to propagate silently to callers). This is an interface design flaw — the
Stage 2 interface needs to be amended before Stage 3 can be re-done correctly.

PM judgment call: interface design flaw vs. implementation bug. When uncertain, ask
the user before proceeding.

---

## TODO: Expand with case studies

<!-- TODO: Add real examples of BLOCK → fix → APPROVE cycles with before/after diffs -->
<!-- TODO: Add guidance on distinguishing interface flaws from implementation bugs -->
<!-- TODO: Add template for multi-CRITICAL BLOCK responses (prioritizing which to fix first) -->
<!-- TODO: Add KB entry format for tracking override decisions -->
