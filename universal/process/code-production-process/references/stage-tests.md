# Stage 3.5: Tests-Must-Pass Gate — Detailed Protocol

## Purpose

This gate enforces a hard prerequisite: code-critic reviews working code only. Dispatching
the critic against code with failing tests wastes tokens on findings that may be artifacts
of the broken state, not real issues in the final implementation. The gate is a PM-level
evaluation — no agent dispatch needed.

## PM Decision Tree

```
Engineer returns from Stage 3
         |
         v
PM reads pytest output artifact
         |
   ┌─────┴─────┐
   |           |
FAILURES    ALL PASS
   |           |
   v           v
Return to   Proceed to
Stage 3     Stage 4
```

## What PM Checks

1. Open the pytest output artifact from the engineer's Stage 3 response
2. Look for the summary line: `X passed, Y failed` or `X passed` (no failures)
3. If ANY failures: stop. Do not proceed. Return to engineer with the failure template.
4. If zero failures: check mypy output (also required). If mypy has errors: return to engineer.
5. Only if BOTH pytest and mypy are clean: proceed to Stage 4.

## Return-to-Engineer Template

```
Tests failed — return to Stage 3.

Required: pytest passes with zero failures AND mypy --strict passes with zero errors
before critic review can be dispatched.

Pytest failures:
[paste failures verbatim]

Mypy errors (if any):
[paste mypy output verbatim]

Fix the above, re-run both checks, and return with clean output.
Do NOT guess at the fix — if the test logic itself is wrong, fix the test.
If the implementation is wrong, fix the implementation.
Report which was fixed.
```

## Test Quality Requirements

Tests returned from Stage 3 must meet these minimums to be accepted by this gate:

- **Coverage:** ≥90% on new code (check `--cov-report=term-missing` output)
- **Test types required:**
  - At least one happy-path test per public function
  - At least one error-condition test per documented exception
  - At least one edge-case test per function (empty input, None, boundary values)
- **Forbidden test patterns:**
  - Tests that only assert `True` or `is not None` — must assert specific values
  - Tests that call `pass` or have empty assertion blocks
  - Tests with `sleep()` for timing (use `asyncio.sleep` with `pytest-asyncio` or mock)
  - Tests that access production databases, external APIs, or network resources

## TODO: Expand with coverage tooling

<!-- TODO: Add conftest.py setting for minimum coverage threshold (fail-under=90) -->
<!-- TODO: Add pytest-asyncio configuration for async test functions -->
<!-- TODO: Add mock patterns for common external dependencies -->
<!-- TODO: Add guidance on when integration tests are required vs unit tests sufficient -->
