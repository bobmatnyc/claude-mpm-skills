# MEDIUM Criteria — Detailed Explanations

## Overview

MEDIUM findings do not block delivery. Critic includes them in the finding table,
PM logs them in the documentation handoff, and the pipeline continues. If user
requests fixes, engineer resolves them — no re-critic required.

MEDIUM criteria represent maintainability and performance issues that will cause
problems at scale or make the codebase harder to maintain, but do not create
immediate correctness failures.

---

## 1. Functions <= 20 lines (prefer <= 10)

**What to check:**
Count lines from `def` to the last line of the function body. Exclude blank lines
between logical sections. Flag functions over 20 lines.

**Why this matters:**
Functions longer than 20 lines are difficult to test in isolation, harder to reason
about, and usually doing more than one thing (violating Single Responsibility).

**Required fix:**
Extract sub-operations into helper functions with descriptive names. If a function
is long because it handles many error conditions, consider a result type or
exception hierarchy that lets each error case be short.

**False positive filter:**
State machine dispatch tables and match/case blocks with many short arms may
legitimately exceed 20 lines — use judgment. Flag as a question if uncertain.

---

## 2. No nested loops where hash map would reduce complexity

**Violation:**
```python
for user in users:
    for order in orders:
        if order.user_id == user.id:  # O(n*m)
            process(user, order)
```

**Required fix:**
```python
orders_by_user: dict[int, list[Order]] = {}
for order in orders:
    orders_by_user.setdefault(order.user_id, []).append(order)

for user in users:
    for order in orders_by_user.get(user.id, []):  # O(n+m)
        process(user, order)
```

---

## 3. list.pop(0) replaced with deque.popleft() where relevant

`list.pop(0)` is O(n) because it shifts all remaining elements. If the code is
implementing a queue pattern (FIFO), use `collections.deque` with `popleft()`.

**Only flag when:** the list is used as a queue (items appended to one end,
popped from the other). Random-access lists are fine with `pop(0)` if used rarely.

---

## 4. asyncio.gather uses return_exceptions=True where appropriate

**When to flag:**
`asyncio.gather(*tasks)` without `return_exceptions=True` raises the first exception
and cancels remaining tasks. If the caller wants to process partial results or
collect all errors, it should use `return_exceptions=True`.

**Only flag when:** the gather call processes heterogeneous tasks where partial
failure is a realistic scenario. Do not flag gather calls where all tasks are
equivalent and failure of any = failure of all.

---

## 5. Async operations have explicit timeouts

**What to check:**
`await some_client.get(url)` without a `timeout` parameter.
`asyncio.wait_for(coroutine, timeout=...)` — if timeout is absent.

**Required fix:**
```python
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url)
```

---

## 6. Docstrings on public methods (Google or NumPy style)

Public methods (not prefixed `_`) on classes should have docstrings explaining:
- What the method does (one line)
- Parameters (if non-obvious)
- Return value (if non-obvious)
- Exceptions raised (if relevant)

**Only flag for:** public API methods. Internal helpers and private methods are
optional. Do not flag for trivial getters/setters where the name is self-documenting.

---

## 7. No Any types in production code paths

`Any` disables type checking for a variable and propagates to callers, undermining
the value of type annotations. Flag `Any` in production code — test files may use
`Any` for mock objects if needed.

**Common false positive:** `cast(Any, ...)` used deliberately at an integration
boundary with an untyped library — note as a question if the usage looks intentional.

---

## TODO: Expand with examples

<!-- TODO: Add complexity examples with Big O analysis -->
<!-- TODO: Add deque vs list benchmark numbers for queue patterns -->
<!-- TODO: Add Google docstring format template -->
<!-- TODO: Add NumPy docstring format template -->
<!-- TODO: Add guidance on when "no docstring" is acceptable (trivial property) -->
