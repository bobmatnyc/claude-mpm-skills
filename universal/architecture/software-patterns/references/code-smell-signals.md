# Code-Smell Signals That Should Trigger Architectural Review

This appendix maps low-level code smells — the kind a linter or quality scanner counts —
to the *architectural* problems they usually indicate. A single occurrence is a code
smell; a high *density* of these signals across a module is a signal that a structural
pattern is missing or being violated. Use this as a bridge between "the scanner flagged
N violations" and "which pattern should we apply."

> **Source note:** The detection signals below are derived from CAST Highlight's
> language-agnostic (`_multi`) code-quality indicators (https://doc.casthighlight.com/),
> which span the Changeability, Efficiency, and Transferability families. CAST in turn
> references established complexity literature (cyclomatic complexity, Fowler's
> *Refactoring* code smells). The architectural interpretations and remedies here are our
> synthesis. Counting thresholds quoted as ranges are CAST's calibration, presented as
> attributed reference, not universal standards.

---

## 1. Large `switch` / long `if-else` chains → missing polymorphism

**Signal:** A `switch` (or `if/elif`) statement with many branches keying off a type tag
or enum, often duplicated in several places that switch on the *same* tag. (CAST flags
files whose average cases-per-switch exceeds a low single-digit threshold.)

**What it usually means:** Two sets of data are being mapped imperatively where a real
map structure or polymorphic dispatch belongs. When the same multi-branch switch recurs,
adding a new case means editing every copy — an Open/Closed Principle violation.

**Architectural remedy:** Replace the type-tag switch with **polymorphism** (a Strategy
or a registry/map of handlers keyed by the tag). See `foundational-patterns.md` (DI) and
`situational-patterns.md` (Strategy). The cross-cutting variants often want a
**Factory** or **table-driven dispatch** instead.

**When *not* to refactor:** A single, localized switch over a closed, stable set (e.g.,
parsing a wire-format byte) is fine. The signal is *recurrence* and *growth*, not the
construct itself.

---

## 2. Deeply nested loops → data-modelling or algorithmic problem

**Signal:** A loop immediately nested inside another loop (CAST counts each nesting).
Two-dimensional nesting implies O(n²) work; deeper nesting compounds it.

**What it usually means:** The data is being joined or grouped in application code that a
better data structure (a hash map for O(1) lookup) or a query (a database join) should do
once. It also frequently hides an N+1 query when the inner loop issues I/O.

**Architectural remedy:** Push the join into the data layer (see the SQL anti-patterns in
the `sqlalchemy` skill), or pre-index one collection into a map before the outer loop.
When the nesting is genuine combinatorics, isolate it behind a well-named **service
boundary** so its cost is explicit and cacheable.

---

## 3. Parameters reassigned inside a routine → missing immutability

**Signal:** A function/method body reassigns its own parameters (`=`, `+=`, `++`, etc.).

**What it usually means:** Mutable in/out parameters make data flow hard to follow and
break referential transparency — a small-scale symptom of the broader problem that the
module lacks clear **immutable value objects** and instead threads mutable state through
calls.

**Architectural remedy:** Introduce a local variable for the transformed value and keep
parameters read-only; at the design level, prefer **immutable value objects / DTOs**
crossing boundaries. This is foundational to the **Anti-Corruption Layer** and
**Domain Events** patterns, both of which assume messages are immutable.

---

## 4. High structural / cyclomatic complexity → unit doing too much (God object / SRP)

**Signal:** A method or class with high cyclomatic complexity, many responsibilities,
many methods/fields, or a very long body. CAST treats rising complexity as the
"arthritis of software" and correlates it with defect density.

**What it usually means:** A **God object** / **too-many-responsibilities** violation of
the Single Responsibility Principle. High coupling (the unit reaches into many others)
and low cohesion (its methods don't relate) typically travel together.

**Architectural remedy:** Decompose along responsibilities into focused services
(**SOA / service decomposition**), inject collaborators (**DI**), and put a **Repository**
between domain logic and persistence so the God object stops owning data access. See
`decision-trees.md` for choosing the decomposition.

---

## 5. High coupling / many cross-module references → missing boundary

**Signal:** A module that imports or calls into a large fan-out of other modules, or many
modules that all depend on one central type (a "hub").

**What it usually means:** Absent or leaky boundaries — changes ripple because there is no
seam. This is the structural precondition that **Anti-Corruption Layer**, **Domain
Events**, and **Circuit Breaker** patterns exist to address.

**Architectural remedy:** Introduce an explicit boundary (interface + DI) so the hub
depends on abstractions, not concretions; route cross-context communication through events
or a translation layer rather than direct calls.

---

## How to use these signals

1. **Run a quality scanner** (or linter) and look at *densities*, not single hits.
2. **Map the dominant smell** to its row above to get a candidate architectural cause.
3. **Confirm before refactoring** — a smell is a hypothesis. Read the code (see the
   `systematic-debugging` discipline) before applying a pattern.
4. **Apply the pattern** from `foundational-patterns.md` / `situational-patterns.md` and
   re-measure; the smell density should drop.

For the project-wide, severity-tagged efficiency/transferability checklist that counts
many of these signals, see the `code-review-standards` skill.
