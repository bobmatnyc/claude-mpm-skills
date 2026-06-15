---
name: rust-quality-gate
description: "PM-invocable protocol for running and interpreting Rust quality gates in the trusty-tools monorepo: fmt, clippy, and test in strict sequence before any merge"
user-invocable: false
disable-model-invocation: true
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Three-gate quality sequence (fmt → clippy → test) that must pass before any PR merge in a Rust workspace"
    when_to_use: "Before any PR merge, after implementation work, or when user says 'check quality', 'run tests', 'verify', or 'is this ready to merge'"
    quick_start: "1. cargo fmt --check  2. cargo clippy --workspace --all-targets -- -D warnings  3. cargo test -p <crate>  — stop on first failure"
  token_estimate:
    entry: 130
    full: 1600
context_limit: 750
tags:
  - rust
  - quality
  - testing
  - clippy
  - fmt
  - cargo
  - ci
  - monorepo
  - qa
requires_tools: []
---

# Rust Quality Gate Protocol

## When to Invoke

Invoke this protocol when:
- Any implementation task completes and code changes are ready to commit
- User asks "check quality", "run tests", "run clippy", "is this ready", or "verify"
- Before creating a pull request or merging to main
- After modifying a shared library crate (`trusty-common`, `trusty-mcp-core`, `trusty-embedder`, `trusty-symgraph`)
- After the rust-qa agent delivers a work product

## The Three-Gate Sequence

Run gates in this exact order. **Stop on first failure — do not proceed to the next gate.**

### Gate 1: Format Check (fastest — always run first)

```bash
cargo fmt --check
```

**Pass**: No output, exit code 0.

**Fail**: Lists files with formatting differences. Fix with:
```bash
cargo fmt
```
Then re-run `cargo fmt --check` to confirm clean.

**Why first**: Format failures are trivially fixable. Running it first avoids wasting clippy and test time on unformatted code.

### Gate 2: Clippy Lint Gate

```bash
cargo clippy --workspace --all-targets -- -D warnings
```

**Pass**: No warnings emitted, exit code 0.

**Fail**: One or more `error[clippy::]` lines. Fix each warning the compiler reports. Common patterns:

```bash
# Check a single crate faster during iteration
cargo clippy -p trusty-search -- -D warnings

# Check with a specific feature enabled
cargo clippy -p trusty-common --features axum-server -- -D warnings
```

**open-mpm exception**: `open-mpm` has 142 pre-existing clippy errors at HEAD (tracked separately). These errors **do not block other work**. When running workspace-wide clippy and `open-mpm` fails, confirm whether the failures are confined to `open-mpm` only:

```bash
# Run clippy on everything except open-mpm to confirm other crates are clean
cargo clippy --workspace --all-targets -- -D warnings 2>&1 | grep -v "open-mpm"
```

If all errors are in `open-mpm`, treat the gate as passing for the purpose of non-open-mpm work.

### Gate 3: Test Gate

**Single-crate (fast — use during iteration):**
```bash
cargo test -p <crate>
```

**Workspace-wide (required before commit):**
```bash
cargo test --workspace
```

**With ignored integration tests (full validation):**
```bash
cargo test -p <crate> -- --include-ignored
# or workspace-wide:
cargo test --workspace -- --include-ignored
```

## Crate Name vs Directory Name

Cargo `-p` flags use the **`name` field in `Cargo.toml`**, not the directory name. Exceptions:

| Directory | Cargo flag |
|---|---|
| `crates/trusty-git-analytics/` | `-p tga` |
| `crates/open-mpm/` | `-p open-mpm` |

All other crates: directory name = crate name (e.g. `crates/trusty-search/` → `-p trusty-search`).

## Reading Test Output

Cargo test output ends with a summary line:

```
test result: ok. 42 passed; 0 failed; 3 ignored; 0 measured; 0 filtered out
```

| Field | Meaning |
|---|---|
| `passed` | Tests that ran and succeeded |
| `failed` | Tests that ran and failed — **must be zero** |
| `ignored` | Tests tagged `#[ignore]` — skipped by default (ONNX/integration) |
| `measured` | Benchmark results (bench mode only) |

**`#[ignore]` tests**: These are slow ONNX-backed or environment-dependent integration tests. They are intentionally skipped in the default gate. Run them with `--include-ignored` for full local validation before releases.

**Evidence format required**: Report the literal summary line, not "tests pass". Example of acceptable evidence:

```
test result: ok. 87 passed; 0 failed; 5 ignored; 0 measured; 0 filtered out; finished in 3.42s
```

## Pre-existing vs New Failure Triage

If a gate fails, determine whether the failure existed before the current patch:

```bash
# Stash current changes
git stash

# Run the failing gate at clean HEAD
cargo test -p <crate>

# If it also fails at HEAD: pre-existing failure — do not block the patch
# If it passes at HEAD: the patch introduced the regression — must fix

# Restore patch
git stash pop
```

Report: "Failure is pre-existing at HEAD — not introduced by this change" or "Failure is new — introduced by this patch."

## Single-Crate vs Workspace Scope

| Scope | Command | When |
|---|---|---|
| Single crate | `cargo test -p <crate>` | Fast iteration during implementation |
| Single crate (check only) | `cargo check -p <crate>` | Fastest — confirms compilation, no test run |
| Single crate + features | `cargo test -p trusty-common --features axum-server` | When feature flag needed |
| Workspace | `cargo test --workspace` | Required before committing any change |
| Workspace + ignored | `cargo test --workspace -- --include-ignored` | Before tagging a release |

## After Modifying a Shared Library Crate

When `trusty-common`, `trusty-mcp-core`, `trusty-embedder`, or `trusty-symgraph` changes:

1. Run `cargo check` (workspace-wide) first — catches compilation errors in all dependents immediately.
2. Run `cargo test -p <lib>` for the modified library.
3. Run `cargo test -p <consumer>` for each crate that imports the modified library.
4. Only commit after all dependent tests pass.

## Gate Summary

```
cargo fmt --check          → Gate 1 (format)  — fix: cargo fmt
cargo clippy --workspace   → Gate 2 (lint)    — fix: address each warning
cargo test -p <crate>      → Gate 3 (tests)   — fix: repair failing tests
```

All three must be green before a PR is mergeable. Evidence must include the literal output from each gate.

## Anti-Patterns

- Running tests before format and clippy — wastes time if format fails.
- Reporting "tests pass" without showing the result summary line.
- Treating `ignored` count as failures — they are intentionally skipped.
- Blocking work on `open-mpm` clippy errors that are pre-existing at HEAD.
- Using `cargo build` as a substitute for `cargo test` — build success does not validate behavior.
- Running `cargo test` workspace-wide without confirming crate name aliases (e.g., use `-p tga` not `-p trusty-git-analytics`).
