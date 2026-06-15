---
name: python-code-quality
description: "Python code-quality anti-patterns and review checks: exception-hierarchy correctness, singleton identity comparison, narrow exception handling, wildcard-import avoidance, magic-number naming, and dead-local removal. Use when reviewing or self-reviewing Python code for correctness and readability defects that linters and reviewers should catch."
user-invocable: false
disable-model-invocation: true
version: 1.0.0
updated: "2026-06-15"
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Catch high-value Python code-quality anti-patterns in review: malformed exception classes, == None vs is None, bare except, wildcard imports, magic numbers, unused locals"
    when_to_use: "When reviewing or self-reviewing Python code for correctness/readability defects, configuring ruff/pylint rules, or writing code-quality guidance — not for testing mechanics (use pytest) or whole-codebase scoring (use code-quality-scoring)"
    quick_start: "1. Ensure custom exceptions derive from Exception 2. Compare None/True/False with is, not == 3. Catch the narrowest exception you can handle, never bare except 4. Replace wildcard imports with explicit names 5. Name magic numbers as constants 6. Remove unused locals — enforce all six with ruff/pylint/mypy in CI"
  references:
    - quality-antipatterns.md
context_limit: 600
tags:
  - python
  - code-quality
  - anti-patterns
  - code-review
  - pep8
  - ruff
  - pylint
  - static-analysis
requires_tools: []
---

# Python Code Quality

High-value Python code-quality anti-patterns to check during review or self-review.
This skill is **review-focused**: it covers correctness and readability defects that a
reviewer (or a linter) should flag, separate from testing mechanics (`pytest`) and
whole-codebase health scoring (`code-quality-scoring`).

> **Source note:** These anti-patterns are derived from CAST Highlight's Python code
> quality indicators (https://doc.casthighlight.com/), which reference **PEP 8** and the
> Python data model as primary sources. Where a rule mirrors PEP 8, the PEP is the
> authoritative source. All examples are original.

## When to Use This Skill

Use it when the task is **"is this Python code clean and correct?"** — for example:

- Reviewing a pull request and checking for the defects below.
- Self-reviewing before opening a PR.
- Configuring `ruff`/`pylint`/`mypy` rules so CI catches these automatically.
- Writing or updating a team's Python code-quality guidance.

Do **not** use it for testing mechanics (use the `pytest` skill) or for scoring a whole
codebase's health and technical debt (use the `code-quality-scoring` skill).

## Core Anti-Patterns (Summary)

Six highest-value Python anti-patterns. Each has a non-compliant/compliant example and a
"how to test" note in the reference doc:

- **Custom exceptions must derive from `Exception`** — a class meant to be raised that
  inherits from `object` fails at runtime and breaks every `except` clause.
- **Compare singletons with `is`, not `==`** — use `is`/`is not` for `None`/`True`/`False`
  (PEP 8); use `is` *only* for singletons, never for value comparison.
- **Avoid bare / overly broad `except`** — catch the narrowest type you can handle; a
  generic `except Exception` only as a last-position fallback that logs or re-raises.
- **Avoid wildcard imports** (`from x import *`) — they hide dependencies, risk silent
  name collisions, and defeat static analysis.
- **Replace magic numbers with named constants** — promote non-obvious literals to
  documented, named constants.
- **Remove unused local variables** — a dead assignment misleads readers and can hide a
  bug where a value was meant to be used.

## Best Practices

- **Gate these in CI.** Most are enforceable cheaply with `ruff` (F403/F405 wildcard,
  F841 unused locals, `E711`/`E712` singleton comparison), `pylint`, and `mypy`. Put the
  lint step in CI so review effort focuses on judgment, not mechanics.
- **Prefer specific exception handlers.** Order handlers narrowest-first; reserve a
  generic `except Exception` for a logging/re-raising last resort.
- **Name intent, not values.** A constant's *name* documents why a threshold exists; a
  bare literal documents nothing.

## Anti-Patterns (What to Avoid)

- Inheriting custom exceptions from `object` or directly from `BaseException`.
- `== None`, `== True`, or `is "some literal"`.
- Bare `except:` or `except BaseException:` that swallows control-flow signals.
- `from module import *` outside a curated `__init__.py` with explicit `__all__`.
- Unexplained numeric literals in business logic.
- Assigned-but-never-read locals left behind by a stale refactor.

## Navigation

- **[quality-antipatterns.md](references/quality-antipatterns.md)**: Full non-compliant
  vs compliant examples and a "how to test" note for each of the six anti-patterns.

## Related Skills

- **pytest** (`toolchains/python/testing/pytest`): testing mechanics — fixtures,
  parametrization, mocking. Several anti-patterns here (broad `except`, malformed
  exception classes) directly cause flaky tests.
- **code-review-standards** (`universal/process/code-review-standards`): the
  project-wide, severity-tagged review checklist that incorporates equivalents of these.
- **code-quality-scoring** (`universal/quality/code-quality-scoring`): whole-codebase
  health and technical-debt scoring, rather than individual findings.
