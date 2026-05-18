# Skip Rules — Decision Tree and Examples

## Overview

The pipeline has two legitimate skip paths. Everything else is a violation.
Stages 3 through 5 are NEVER skippable.

## Decision Tree

```
Is this a code change?
  NO → Documentation-only path (all stages skipped)
  YES → Continue

Is it a confirmed production bug fix ≤20 lines across ≤2 files?
  YES → Does it touch auth/crypto/serialization?
    YES → Standard path (all 6 stages)
    NO → Hotfix path (skip stages 1-2, run 3-5)
  NO → Standard path (all 6 stages)
```

## Standard Path (All 6 Stages)

Required for:
- New features (any size)
- Refactors >20 lines of net new code
- Any change touching:
  - Authentication or authorization logic
  - Cryptographic operations
  - Data serialization/deserialization
  - Database schema or migration
  - External API contracts
- Any change across >2 source files

## Hotfix Path (Skip Stages 1 and 2)

Allowed only when ALL of the following are true:

1. The bug is **confirmed in production** — not a hypothetical, not a local-only failure
2. The fix scope is **≤20 lines of net new code** across **≤2 files** (verify with `git diff --stat`)
3. The fix does **NOT touch**: authentication, authorization, cryptography, data serialization
4. PM explicitly logs "hotfix path" in the session record

On hotfix path: Stage 3 (Implement + Tests), Stage 3.5 (Tests-Must-Pass Gate),
Stage 4 (Critic), and Stage 5 (Security) remain mandatory.

## Documentation-Only Path (All Stages Skipped)

Allowed only when ALL changes are:
- Markdown, RST, or plain text documentation
- Configuration values (no logic — e.g., updating a port number in `config.yaml`)
- Dependency version bumps with no code changes

PM MUST verify via `git diff --stat` that no `.py`, `.ts`, `.js`, `.go`, `.rs`,
or other source files were modified. If any source file appears in the diff — even
with one line changed — the documentation-only path is disqualified.

## Examples

| Change Description | Correct Path |
|-------------------|--------------|
| New REST endpoint implementation | Standard (all 6 stages) |
| Fix TypeError in production payment handler, 3-line change | Hotfix path |
| Update README with new environment variable | Documentation-only |
| Refactor auth middleware to add rate limiting | Standard (auth = always standard) |
| Bump `requests` from 2.31 to 2.32 (no code changes) | Documentation-only |
| Fix SQL query bug in production, changes 25 lines | Standard (>20 lines) |
| Add logging to existing error handler, 5-line change | Hotfix path |
| Update `config.yaml` database URL | Documentation-only |

## Violations

The following are process violations — if caught mid-session, PM must restart from
the last valid stage:

- Skipping Stage 3 (Implement + Tests) for any reason
- Skipping Stage 4 (Critic) for any reason
- Skipping Stage 5 (Security) for any reason
- Declaring hotfix path for a change that modifies auth/crypto code
- Declaring documentation-only path without verifying `git diff --stat`

## TODO: Expand with edge cases

<!-- TODO: Add guidance on changes that are "mostly config" but include one-line logic changes -->
<!-- TODO: Add examples for migration files (schema change = standard path) -->
<!-- TODO: Add handling for test-only changes (tests are source files — standard path applies) -->
