---
name: Testing Anti-Patterns
description: Never test mock behavior. Never add test-only methods to production classes. Understand dependencies before mocking. Language-agnostic principles with TypeScript/Jest and Python/pytest examples.
when_to_use: when writing or changing tests, adding mocks, or tempted to add test-only methods to production code
version: 3.0.0
tags:
  - testing
  - typescript
  - javascript
  - python
  - pytest
  - jest
  - mocking
  - tdd
  - anti-patterns
progressive_disclosure:
  entry_point:
    summary: "Avoid testing mocks, test-only production methods, and incomplete mocking. Test real behavior, not mock behavior. Covers TypeScript/Jest and Python/pytest."
    when_to_use: "When writing tests, adding mocks, reviewing test failures, or tempted to add test-only methods to production code."
    quick_start: "1. Ask: 'Am I testing real behavior?' 2. Check: 'Is this method only for tests?' 3. Verify: 'Do I understand what I'm mocking?' 4. Confirm: 'Is my mock complete?' 5. Apply: TDD prevents these patterns"
  references:
    - core-anti-patterns.md
    - completeness-anti-patterns.md
    - detection-guide.md
    - tdd-connection.md
    - python-examples.md
related_skills:
  - toolchains-typescript-testing-jest
  - toolchains-typescript-testing-vitest
  - toolchains-python-testing-pytest
  - universal-debugging-systematic-debugging
  - universal-debugging-verification-before-completion
---

# Testing Anti-Patterns

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested.

**Core principle:** Test what the code does, not what the mocks do.

**Following strict TDD prevents these anti-patterns.** See the Test-Driven Development skill (available in the skill library) for the complete TDD workflow.

## When to Use This Skill

Activate this skill when:
- **Writing or changing tests** - Verify tests cover real behavior
- **Adding mocks** - Ensure mocking is necessary and correct
- **Reviewing test failures** - Check if mock behavior is the issue
- **Tempted to add test-only methods** - STOP and reconsider
- **Tests feel overly complex** - Sign of over-mocking

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
4. NEVER create incomplete mocks
5. NEVER treat tests as afterthought
```

## Core Anti-Pattern Categories

### 1. Testing Mock Behavior
Asserting on mock elements instead of real behavior. **Fix:** Test real component or don't mock it.
**→** [core-anti-patterns.md](references/core-anti-patterns.md#anti-pattern-1-testing-mock-behavior)

### 2. Test-Only Methods in Production
Methods in production classes only used by tests. **Fix:** Move to test utilities.
**→** [core-anti-patterns.md](references/core-anti-patterns.md#anti-pattern-2-test-only-methods-in-production)

### 3. Mocking Without Understanding
Mocking without understanding dependencies/side effects. **Fix:** Understand first, mock minimally.
**→** [core-anti-patterns.md](references/core-anti-patterns.md#anti-pattern-3-mocking-without-understanding)

### 4. Incomplete Mocks
Partial mocks missing fields downstream code needs. **Fix:** Mirror complete API structure.
**→** [completeness-anti-patterns.md](references/completeness-anti-patterns.md#anti-pattern-4-incomplete-mocks)

### 5. Tests as Afterthought
Implementation "complete" without tests. **Fix:** TDD - write test first.
**→** [completeness-anti-patterns.md](references/completeness-anti-patterns.md#anti-pattern-5-tests-as-afterthought)

## Quick Detection Checklist

Run this checklist before committing any test:

**Language-agnostic checks:**
```
□ Am I asserting on mock behavior instead of real behavior?
  → TypeScript: testId='*-mock', expect(mock).toHaveBeenCalled()
  → Python: mock.assert_called(), mock.call_count
  → If yes: STOP - Test real behavior or unmock

□ Does this method only exist for tests?
  → TypeScript: destroy(), reset(), clear() only in *.test.ts
  → Python: _set_mock_*, _for_testing only in test_*.py
  → If yes: STOP - Move to test utilities

□ Do I fully understand what I'm mocking?
  → If no: STOP - Run with real impl first, then mock minimally

□ Is my mock missing fields the real API has?
  → TypeScript: Partial<T>, incomplete objects
  → Python: Mock() with few attributes, missing nested fields
  → If yes: STOP - Mirror complete API structure

□ Did I write implementation before test?
  → If yes: STOP - Delete impl, write test first (TDD)

□ Is mock setup >50% of test code?
  → If yes: Consider integration test with real components
```

**See:** [detection-guide.md](references/detection-guide.md) for comprehensive red flags and warning signs.

## The Bottom Line

**Mocks are tools to isolate, not things to test.**

Testing mock behavior indicates a problem. Fix: Test real behavior or question why mocking is necessary.

**TDD prevents these patterns.** Write test first → Watch fail → Minimal implementation → Pass → Refactor.

## Navigation

### Detailed Anti-Pattern Analysis
- **[Core Anti-Patterns](references/core-anti-patterns.md)** - Patterns 1-3: Mock behavior, test-only methods, uninformed mocking
- **[Completeness Anti-Patterns](references/completeness-anti-patterns.md)** - Patterns 4-5: Incomplete mocks, tests as afterthought

### Detection & Prevention
- **[Detection Guide](references/detection-guide.md)** - Red flags, warning signs, gate functions
- **[TDD Connection](references/tdd-connection.md)** - How test-driven development prevents these patterns

### Language-Specific Examples
- **[Python Examples](references/python-examples.md)** - Complete Python/pytest guide covering all 5 anti-patterns with unittest.mock and pytest-mock patterns, fixture best practices, and pytest-specific detection. Load when working with Python tests.

### Related Skills

When using this skill, consider these complementary skills (if deployed in your skill bundle):

- **test-driven-development**: Complete TDD workflow and red-green-refactor cycle
  - *Use case*: Implementing TDD discipline to prevent anti-patterns
  - *Integration*: TDD workflow prevents most anti-patterns by design
  - *Status*: Recommended - basic anti-patterns covered in this skill

- **verification-before-completion**: Definition of "done" and verification protocols
  - *Use case*: Ensuring tests are part of completion criteria
  - *Integration*: Tests must pass before work is considered complete
  - *Status*: Recommended - testing mindset reinforcement

*Note: All skills are independently deployable. This skill is fully functional without them.*

## Key Reminders

1. **Mocks isolate, don't prove** - Test real code, not mocks
2. **Production ignores tests** - No test-only methods
3. **Understand before mocking** - Know dependencies and side effects
4. **Complete mocks only** - Mirror full API structure
5. **Tests ARE implementation** - Not optional afterthought

## Red Flags - STOP

**STOP immediately when:**
- **Testing mock behavior**
  - TypeScript: Asserting on `*-mock` test IDs, `expect(mock).toHaveBeenCalled()`
  - Python: `mock.assert_called()`, `mock.call_count` without real behavior checks
- **Adding test-only methods**
  - TypeScript: `destroy()`, `reset()` only in `*.test.ts`
  - Python: `_set_mock_*`, `_for_testing` with "For testing only" docstrings
- **Mocking without understanding**
  - Adding `@patch` or `vi.mock()` "just to be safe"
  - Creating mocks from memory instead of API docs
- **Incomplete mocks**
  - TypeScript: `Partial<T>`, missing nested objects
  - Python: `Mock()` for data objects, missing required fields
- **Tests as afterthought**
  - Saying "tests can wait" or "ready for testing"
  - Implementation commits before test commits

**When mocks become too complex:** Consider integration tests with real components. Often simpler and more valuable.

## Integration with Other Skills

**Prerequisite:** Test-Driven Development skill - TDD prevents anti-patterns (recommended for complete workflow)
**Complementary:** Verification-Before-Completion skill - Tests = done (ensures proper testing discipline)
**Domain-specific:** webapp-testing, backend-testing for framework patterns (see skill library if available)
