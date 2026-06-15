# EFFICIENCY Criteria — Detailed Explanations

## Overview

EFFICIENCY findings cover algorithmic and data-access patterns that waste CPU,
memory, or I/O at scale. Most are **MEDIUM** by default: they rarely break
correctness, but they degrade performance as input size grows and they signal that
a different data model or algorithm was warranted. Escalate to **HIGH** only when the
pattern sits on a hot path with unbounded input (e.g., a request handler iterating an
attacker-controllable collection).

These criteria add an Efficiency dimension to the checklist, complementing the
existing Security and Robustness items.

> **Source note:** The Efficiency families below are derived from CAST Highlight code
> quality indicators (https://doc.casthighlight.com/). Patterns are paraphrased with
> original examples; thresholds are presented as guidance, not CAST's proprietary
> calibration.

---

## 1. Nested loops over two collections (O(n*m))

**Severity: MEDIUM** (HIGH on a hot path with large/unbounded inputs)

A loop nested directly inside another loop to correlate two collections produces
O(n*m) behavior. For small fixed ranges this is fine; for data-driven collections it
is usually a missing index/hash-map, and occasionally a sign the data model itself is
wrong (the correlation should have been a join or a precomputed mapping).

**Violation:**
```python
for user in users:
    for order in orders:               # O(n*m)
        if order.user_id == user.id:
            link(user, order)
```

**Required fix — build a lookup once, then iterate once (O(n+m)):**
```python
orders_by_user: dict[int, list[Order]] = {}
for order in orders:
    orders_by_user.setdefault(order.user_id, []).append(order)

for user in users:
    for order in orders_by_user.get(user.id, []):
        link(user, order)
```

**False-positive filter:** Nested iteration over genuinely small fixed dimensions
(a 3x3 grid, a fixed matrix) is not a violation. A nested loop where the inner range
is bounded by a small constant is acceptable — flag only when both ranges scale with
input. An inner loop guarded by an `if`/branch, or a loop calling a helper that itself
loops, is weaker evidence — note as a question rather than a finding.

---

## 2. Query or fetch inside a loop (the N+1 pattern, generalized)

**Severity: HIGH** (this is the existing "N+1 query patterns" item, broadened)

Issuing a database query, RPC, or remote fetch once per iteration multiplies round
trips. The HIGH checklist already flags ORM N+1; this entry generalizes it to *any*
per-iteration I/O — a cursor advanced inside a loop, a `requests.get` per element, a
cache read per row.

**Violation:**
```python
for order in orders:
    customer = db.query(Customer).get(order.customer_id)  # 1 query per order
    enrich(order, customer)
```

**Required fix — batch the access outside the loop:**
```python
ids = {o.customer_id for o in orders}
customers = {c.id: c for c in db.query(Customer).filter(Customer.id.in_(ids))}
for order in orders:
    enrich(order, customers[order.customer_id])
```

**False-positive filter:** A loop that legitimately must call out per item (e.g., a
fan-out where each call targets a different host and batching is impossible) is not a
violation — but it should then use bounded concurrency and timeouts (see MEDIUM async
items). Flag the unbatched serial case; question the unavoidable fan-out case.

---

## 3. Greedy data access — repeated deep property/selector resolution

**Severity: MEDIUM**

Re-resolving a deep member chain or re-running a selector/query on every use forces
the runtime to walk the resolution path each time. If a deeply nested value or a
DOM/ORM selector result is read more than once in a scope, cache it in a local.

**Violation:**
```javascript
if (config.services.auth.tokens.refresh.enabled) {
  rotate(config.services.auth.tokens.refresh.ttl);   // path walked twice
}
```

**Required fix:**
```javascript
const refresh = config.services.auth.tokens.refresh;
if (refresh.enabled) {
  rotate(refresh.ttl);
}
```

The same applies to repeated `document.querySelector(...)`, repeated ORM relationship
access that triggers lazy loads, and repeated dictionary lookups of the same key.

**False-positive filter:** A property read once, or reads separated by a mutation that
could change the value, are not violations. Only flag when the same path is read 2+
times in one scope with no intervening write.

---

## 4. String concatenation accumulated in a loop

**Severity: MEDIUM**

Because strings are immutable in Python, Java, JavaScript, and most managed runtimes,
`+=` inside a loop allocates a new string each iteration, yielding O(n²) work and
churning the allocator.

**Violation:**
```python
html = "<table>"
for last, first in employees:
    html += f"<tr><td>{last}, {first}</td></tr>"   # new string each pass
html += "</table>"
```

**Required fix — accumulate in a list, join once:**
```python
parts = ["<table>"]
for last, first in employees:
    parts.append(f"<tr><td>{last}, {first}</td></tr>")
parts.append("</table>")
html = "".join(parts)
```

(Java: `StringBuilder`. JavaScript: push to an array and `join`.)

**False-positive filter:** A handful of concatenations outside a loop, or building a
short fixed-size string, is not a violation. Flag only accumulation inside a loop whose
trip count scales with input.

---

## 5. `SELECT *` and over-fetching

**Severity: MEDIUM**

Retrieving all columns when only a few are needed inflates network payload, defeats
covering indexes, and couples the caller to column order. Name the columns required.

**Violation:** `SELECT * FROM orders WHERE status = 'open'`
**Required fix:** `SELECT id, customer_id, total FROM orders WHERE status = 'open'`

**False-positive filter:** Ad-hoc diagnostics, small parameter/reference tables, and
ORM models that genuinely use every column are acceptable. Flag `SELECT *` in
production query paths that return wide rows or large result sets.

---

## How Efficiency findings affect the verdict

Efficiency items are MEDIUM unless they sit on a hot path with unbounded input, in
which case the N+1/fetch-in-loop case is HIGH (consistent with the existing HIGH "No
N+1 query patterns" item). MEDIUM Efficiency findings are logged in the documentation
handoff and do not block delivery. As with all criteria, apply the 80% confidence
filter — a nested loop over two small fixed ranges is not a finding.
