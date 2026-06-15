# Stage 3: Implement — Detailed Protocol

## Purpose

Implementation fills the Stage 2 interface with working code and validates it with tests.
The engineer does not invent new public APIs — they implement the ones designed in Stage 2.
Any deviation from the Stage 2 interface must be flagged to PM before proceeding.

## Agent and Skills

- **Agent:** `python-engineer`
- **Skills loaded:** `software-patterns`, `asyncio` (if async code), `pytest`

## Scope

The engineer implements:
1. The source file(s) implementing the Stage 2 interface
2. Pytest unit tests with minimum 90% coverage on new code
3. Type-correct code that passes `mypy --strict` with zero errors

## Engineer Self-Check (Before Returning to PM)

The engineer MUST perform these checks and include output in the response:

```bash
# 1. Run mypy strict
mypy --strict path/to/new_module.py

# 2. Run pytest with coverage
pytest tests/test_new_module.py -v --cov=path/to/new_module --cov-report=term-missing

# 3. Verify no bare except
grep -n "except:" path/to/new_module.py  # should return nothing

# 4. Verify no eval/exec
grep -n "\beval\b\|\bexec\b" path/to/new_module.py  # should return nothing
```

All four checks MUST return clean output before the engineer declares the implementation done.

## Implementation Standards

- Functions: ≤20 lines preferred, ≤50 lines maximum before extraction
- No mutable default arguments (`def foo(items=[])` is forbidden)
- No global mutable state
- No bare `except:` — always catch specific exceptions or `Exception` with logging
- Async functions: no synchronous I/O inside (no `requests.get`, `open()` in `async def`)
- Error paths: every exception must be either re-raised, logged and re-raised, or converted to a domain error type — never silently swallowed

## Dispatch Prompt Template

```
Implementation task for: [task description]

Inputs:
- Stage 1 spec: [attached]
- Stage 2 interface specification: [attached]

Implement the interface exactly as designed. Do NOT modify the public API.
If you find the interface is unimplementable as specified, flag the issue
to PM before proceeding — do not silently work around it.

Required deliverables:
1. Source file(s) implementing the Stage 2 interface
2. Pytest test file(s) with ≥90% coverage on new code
3. mypy --strict output (zero errors required)
4. pytest output (zero failures required)

Standards:
- All functions: complete type annotations
- All exceptions: explicitly handled, not swallowed
- All async functions: no synchronous I/O inside
```

## TODO: Expand with implementation patterns

<!-- TODO: Add async HTTP implementation patterns (aiohttp, httpx) -->
<!-- TODO: Add database access patterns (SQLAlchemy async, psycopg3) -->
<!-- TODO: Add test fixture patterns for common dependencies (DB, HTTP, filesystem) -->
<!-- TODO: Add coverage threshold enforcement (conftest.py settings) -->
