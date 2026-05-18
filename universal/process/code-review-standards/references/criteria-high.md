# HIGH Criteria — Detailed Explanations

## Overview

HIGH findings block delivery (WARN verdict). Zero CRITICAL and one or more HIGH = WARN.
PM proceeds to Stage 5 but logs findings. If user directs fixes, engineer resolves
HIGH findings and re-runs tests — no re-critic required for WARN resolutions.

HIGH criteria represent conditions that, if left unfixed, will cause correctness failures,
type safety breakdowns, or silent errors that are difficult to debug in production.

---

## 1. Type hints on all public functions and classes

**What to check:**
Every public function (not prefixed `_`) must have type annotations on:
- All parameters (including `self` — skip, it's implied)
- Return type

**Violation example:**
```python
def process(data, timeout):  # no annotations
    return data
```

**Required fix:**
```python
def process(data: list[dict], timeout: float) -> list[dict]:
    return data
```

---

## 2. mypy --strict passes with zero errors

Engineer must provide `mypy --strict` output in Stage 3 response. If output is absent
or shows errors, this is a HIGH finding.

Check for: `error:` lines in mypy output, `Found X errors in Y files`.

---

## 3. pytest passes with zero failures

Engineer must provide pytest output. Any `FAILED` or `ERROR` lines are a HIGH finding.
The Stage 3.5 gate should have caught this — if it reaches critic, it's a process error,
but the critic still flags it.

---

## 4. Test coverage >= 90% on new code

Check `--cov-report=term-missing` output. If new files show coverage below 90%, flag
as HIGH. Note the specific files and their actual coverage percentages.

---

## 5. No bare except clauses

**Violation:**
```python
try:
    result = fetch()
except:  # catches KeyboardInterrupt, SystemExit, etc.
    pass
```

**Required fix:**
```python
try:
    result = fetch()
except (TimeoutError, ConnectionError) as e:
    logger.error("fetch failed: %s", e)
    raise
```

---

## 6. No mutable default arguments

**Violation:**
```python
def append_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items
```

The default `[]` is created once and shared across all calls. This is a classic Python
footgun that causes state leakage between calls.

**Required fix:**
```python
def append_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

---

## 7. No global mutable state

Module-level mutable variables shared across function calls create implicit state
dependencies that cause non-deterministic behavior and test pollution.

**Violation:**
```python
_cache: dict[str, str] = {}  # module-level mutable dict

def get_cached(key: str) -> str | None:
    return _cache.get(key)
```

**Required fix:**
Pass state through function arguments or use a class with explicit lifecycle
management. If a module-level cache is required by design, flag as a question
(not a finding) — it may be intentional.

---

## 8. No synchronous I/O inside async functions

**Violation:**
```python
async def fetch_user(user_id: int) -> dict:
    response = requests.get(f"/users/{user_id}")  # blocks event loop
    return response.json()
```

**Required fix:**
```python
async def fetch_user(user_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
    return response.json()
```

Also check: `open()` for file I/O in async context — use `aiofiles`.
Database calls: `psycopg2` in async context — use `asyncpg` or `psycopg3` async.

---

## 9. No N+1 query patterns

**Violation:**
```python
users = db.query(User).all()
for user in users:
    user.orders = db.query(Order).filter_by(user_id=user.id).all()  # N queries
```

**Required fix:**
Use eager loading or a JOIN: `db.query(User).options(joinedload(User.orders)).all()`

---

## 10. Error cases handled explicitly (not silently swallowed)

**Violation:**
```python
try:
    result = parse(data)
except Exception:
    result = None  # error swallowed — caller doesn't know what went wrong
```

**Required fix:**
Either re-raise, log and re-raise, or convert to a domain exception:
```python
try:
    result = parse(data)
except ParseError as e:
    logger.error("parse failed for data=%r: %s", data, e)
    raise ProcessingError("failed to parse input") from e
```

---

## TODO: Expand with framework-specific patterns

<!-- TODO: Add Django ORM N+1 patterns (select_related, prefetch_related) -->
<!-- TODO: Add FastAPI sync-in-async patterns (run_in_executor, BackgroundTasks) -->
<!-- TODO: Add SQLAlchemy async session patterns -->
<!-- TODO: Add coverage exception annotations (@pragma: no cover) guidance -->
