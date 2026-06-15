# TRANSFERABILITY Criteria — Detailed Explanations

## Overview

TRANSFERABILITY findings cover how easily a new engineer can read, understand, and
take ownership of the code. These are maintainability concerns: dead code that misleads
readers, inconsistent naming that slows comprehension, and control-flow shapes (long
`if/else if` chains, nested `switch`) that obscure intent. Most are **MEDIUM** or
**LOW** — they do not break correctness, but they raise the cost of every future change.

This adds a Transferability dimension to the checklist, complementing the existing
Security, Robustness, and (new) Efficiency dimensions.

> **Source note:** The Transferability families below are derived from CAST Highlight
> code quality indicators (https://doc.casthighlight.com/), which themselves reference
> open standards (SonarSource, CodeNarc, CWE-561 for dead code). Patterns are
> paraphrased with original examples.

---

## 1. Dead code — unreachable statements

**Severity: MEDIUM**

Dead code is any statement that can never execute: code after an unconditional
`return`/`break`/`continue`/`raise` in the same block, branches whose condition is a
constant, or private methods with no callers. It misleads readers into thinking
behavior exists that does not, and it rots silently because no test exercises it.

**Violation:**
```python
def fee(amount: float) -> float:
    return amount * RATE
    log.debug("computed fee")   # unreachable — never runs
```

**Required fix:** Delete it. Git history preserves anything that might be restored;
leaving "just in case" code in place is the anti-pattern.

**False-positive filter:** Code after a `return` inside a *conditional* branch is not
dead. Platform-specific branches guarded by a runtime check are not dead. Flag only
genuinely unreachable statements and provably uncalled private members. This overlaps
with the LOW "no commented-out code" item — actual unreachable *active* code is MEDIUM
(it compiles and misleads), commented-out code is LOW.

(Reference: CWE-561 Dead Code.)

---

## 2. Long `if / else if` chains that should be a switch or dispatch map

**Severity: MEDIUM**

Three or more `else if` branches selecting on the same variable are hard to scan and
easy to extend incorrectly (a forgotten branch, a duplicated condition). Prefer a
`switch`/`match`, or — better — a dispatch dictionary mapping keys to handlers.

**Violation:**
```python
if kind == "circle":
    area = pi * r * r
elif kind == "square":
    area = s * s
elif kind == "triangle":      # 3rd branch — readability degrades
    area = 0.5 * b * h
else:
    raise ValueError(kind)
```

**Required fix (dispatch map — most extensible):**
```python
AREA = {
    "circle":   lambda: pi * r * r,
    "square":   lambda: s * s,
    "triangle": lambda: 0.5 * b * h,
}
try:
    area = AREA[kind]()
except KeyError:
    raise ValueError(kind)
```

**False-positive filter:** Two branches do not warrant a switch. Chains where each
branch tests a *different* variable (genuine sequential logic, not a single-key
dispatch) are not violations. (Threshold guidance — three or more branches on one
key — derived from CAST/CodeNarc conventions.)

---

## 3. Nested `switch` / `match` statements

**Severity: MEDIUM**

A `switch` inside a `switch` is hard to read: a reader can mistake an inner `case` for
an outer one, and missing `break`s become invisible. Extract the inner switch into its
own well-named function.

**Violation:**
```javascript
switch (state) {
  case "open":
    switch (event) {        // nested — extract this
      case "close": ...
      case "expire": ...
    }
  case "closed": ...
}
```

**Required fix:** Move the inner switch into `handleOpen(event)` and call it from the
outer `case`. The outer switch now reads as a flat state table.

**False-positive filter:** A single inner switch that is trivially short (two cases)
may be acceptable inline — use judgment, note as a question if uncertain.

---

## 4. Naming consistency and hygiene

**Severity: MEDIUM for actively misleading names; LOW for merely terse names**

Names are the primary documentation a future maintainer reads. Two concerns:

- **Consistency:** the same concept should have the same name everywhere
  (`user_id` vs `uid` vs `userIdentifier` for one thing forces the reader to prove they
  are equal). Casing should follow the project convention (snake_case in Python,
  camelCase in JS/TS) uniformly.
- **Descriptiveness:** identifiers should be long enough to convey intent. Single-letter
  names are acceptable only for loop indices (`i`, `j`), coordinates (`x`, `y`), and
  standard mathematical notation.

**Violation (misleading — MEDIUM):**
```python
users = get_orders()        # name says users, value is orders
```

**Violation (terse — LOW):**
```python
def p(d, l): ...            # unclear params
```

**False-positive filter:** Established domain abbreviations (`url`, `db`, `id`) and
project-local conventions are fine. Naming rarely causes bugs — keep it LOW unless the
name actively contradicts the value it holds. This overlaps with the existing LOW
"variable naming is clear" item; escalate to MEDIUM only for actively misleading names.

---

## 5. Module/file managing too many responsibilities

**Severity: LOW**

A single file that imports and coordinates an unusually large number of other
modules/files is a transferability smell: it concentrates knowledge and is hard to
hand off. This pairs with the repo's 800-line file limit (plan modularization at 600).

**What to check:** A file at or over the size limit, or one whose import block spans
dozens of unrelated modules. Suggest extracting cohesive sub-modules.

**False-positive filter:** Aggregator/`__init__.py` barrel files and dependency-
injection composition roots legitimately reference many modules — not a violation.

---

## How Transferability findings affect the verdict

Transferability items are MEDIUM or LOW; none block delivery on its own. They are
logged to the documentation handoff. In a BLOCK or WARN verdict, keep these out of the
finding table (per the LOW-criteria guidance about not burying high-signal findings)
and mention them in the summary paragraph instead. Apply the 80% confidence filter —
do not flag intentional, idiomatic patterns as transferability problems.
