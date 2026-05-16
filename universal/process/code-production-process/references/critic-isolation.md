# Critic Isolation — Prompt Construction Rules

## Why Isolation Matters

Anchoring bias is the primary failure mode of code review in multi-agent systems.
When the critic receives the implementer's stated rationale alongside the code, the
critic unconsciously anchors to that framing and evaluates whether the rationale is
valid rather than whether the code is correct and safe.

An engineer who writes "I used a list here because the dataset is small" has
pre-argued against the critic raising memory complexity concerns. The critic must
encounter the code cold — with no context about why choices were made — so that
the critic's job is pure evaluation, not arbitration of the implementer's intent.

## What PM Includes in the Critic Prompt

PM constructs the critic dispatch from scratch. Include ONLY:

1. **Stage 1 spec document** — verbatim, unmodified
2. **Stage 2 interface specification** — verbatim, unmodified
3. **Stage 3 source files** — verbatim, unmodified (code only, not the engineer's response text)
4. **Stage 3 pytest output** — verbatim (the raw terminal output, not a summary)

## What PM MUST NOT Include

The following are explicitly prohibited from the critic prompt:

- The engineer's commit message
- The engineer's stated design rationale ("I chose X because Y")
- Any notes the engineer included about trade-offs or alternatives considered
- PM's own summary of what the engineer did or what changed
- Phrases like:
  - "The engineer explained that..."
  - "According to the implementer..."
  - "The engineer noted that this approach was chosen because..."
  - "Note: this is a simplified version because..."

## Extraction Procedure

When the engineer's Stage 3 response mixes code with explanatory text:

1. Identify code blocks (between ` ``` ` fences or clearly indented source)
2. Extract code blocks only — discard all surrounding prose
3. Do the same for pytest output: extract the raw output block, discard the engineer's commentary about what it means
4. Assemble critic prompt from extracted content only

If the engineer did not use code fences, PM should request the engineer re-submit
with clear code block delimiters before proceeding to Stage 4.

## Correct Critic Prompt Structure

```
Code review task.

Apply the code-review-standards checklist. Output verdict as first line.

== SPEC ==
[verbatim Stage 1 spec — no modifications]

== INTERFACE ==
[verbatim Stage 2 interface document — no modifications]

== SOURCE: path/to/file.py ==
```python
[verbatim source code — no modifications]
```

== SOURCE: path/to/tests/test_file.py ==
```python
[verbatim test code — no modifications]
```

== TEST RESULTS ==
```
[verbatim pytest terminal output]
```
```

## Incorrect Critic Prompt (Anti-Pattern)

```
The engineer implemented the FetchService as requested. They noted that they
used a synchronous fallback because the async version was causing issues in
the test environment. Here is the code for your review:

[code follows]
```

The phrase "they noted that they used a synchronous fallback because..." gives the
critic a ready-made excuse to accept what would otherwise be a HIGH finding
(synchronous I/O inside an async function). This version is a process violation.

## PM Self-Check Before Dispatch

Before dispatching the critic, PM answers these questions:

- [ ] Does my critic prompt contain the word "engineer"? (If yes, remove the sentence)
- [ ] Does my critic prompt contain "because" or "since" explaining any code choice? (If yes, remove it)
- [ ] Is the source code verbatim from the files, not paraphrased? (Verify)
- [ ] Is the pytest output verbatim terminal output, not a summary? (Verify)

All four must be clean before critic dispatch.

## TODO: Expand with isolation verification patterns

<!-- TODO: Add automated check script that scans critic prompt for prohibited phrases -->
<!-- TODO: Add examples of edge cases: engineer-added inline comments that explain rationale -->
<!-- TODO: Add guidance for multi-engineer sessions where Stage 3 had multiple iterations -->
