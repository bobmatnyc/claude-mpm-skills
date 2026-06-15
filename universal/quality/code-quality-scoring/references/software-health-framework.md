# Software Health Framework

## Overview

Software Health is a composite score that answers a single question: **how well does this
codebase comply with the practices that keep it reliable, changeable, and lean?** It is
the straight average of three independent 0–100 sub-scores.

```
Software Health = avg(Resiliency, Agility, Elegance)
```

> **Source note:** This decomposition and the threshold bands are derived from CAST
> Highlight's Software Health, Software Resiliency, Software Agility, and Software Elegance
> indicators (https://doc.casthighlight.com/). The numeric cutoffs are CAST's proprietary
> calibration from their AppMarq benchmark dataset and are reproduced here as **attributed
> reference ranges**, not as a universal standard.

---

## The three dimensions

### 1. Resiliency / Robustness — "will it break?"

Searches for defensive-coding and reliability practices: error handling that does not
swallow failures, no raw exceptions thrown across boundaries, no fall-through in
`switch`, no missing `default`/`else`, no risky catches. A low Resiliency score predicts
production incidents.

**Maps to:** the Robustness and Security families in `code-review-standards`, and the
per-language quality-anti-pattern references (Python `riskycatches`/`illegalexception`,
Java `genericcatches`/`nestedtrycatches`, PHP empty-catch, JS `errormanagement`/`eval`).

**Remediation owner:** engineers fixing error-handling and edge-case defects.

### 2. Agility / Changeability — "can we change it quickly?"

Searches for the presence of embedded documentation and readability practices:
consistent naming, commented closings, no over-long `if/else if` chains that should be a
`switch`, no useless overriding methods, no functions used before declaration. A low
Agility score predicts slow, error-prone changes and onboarding pain.

> Agility uses *different* band cutoffs than Health overall (red below ~54, green above
> ~69 per CAST's calibration) because its score distribution differs. Do not assume one
> set of cutoffs applies to every dimension.

**Maps to:** the Transferability and Changeability families (naming consistency, dead
code, switch nesting in `code-review-standards`'s `criteria-transferability.md`).

**Remediation owner:** engineers improving readability, documentation, structure.

### 3. Elegance / Efficiency — "is it lean?"

Searches for complexity and waste: nested loops, large switch statements, repetitive
deep-member access, dead code, over-fetching. A low Elegance score predicts performance
problems and a code model that resists simplification.

**Maps to:** the Efficiency family in `code-review-standards`'s `criteria-efficiency.md`.

**Remediation owner:** engineers reducing complexity and algorithmic/data-access waste.

---

## Threshold bands (attributed to CAST calibration)

| Band | Software Health | Software Agility |
|------|-----------------|------------------|
| 🔴 Low / Red | below ~53 | below ~54 |
| 🟠 Medium / Orange | ~53 to ~75 | ~54 to ~69 |
| 🟢 High / Green | above ~75 | above ~69 |

The bands matter less than the **per-dimension breakdown**. Two applications can share a
Health score of 64 (orange) for opposite reasons: one is green on Resiliency but red on
Agility (stable but unmaintainable), the other red on Resiliency but green on Agility
(easy to read, prone to crash). Their remediation plans are completely different.

---

## Mapping your existing tooling onto the dimensions

You do not need CAST to compute a Health-style score. Map the findings your existing
linters already produce:

| Your tool output | Dimension |
|------------------|-----------|
| Bare/broad except, swallowed errors, missing default, fall-through, `eval`, unsafe casts | Resiliency |
| Naming violations, missing docstrings, dead code, deep nesting, long if/else chains, magic numbers | Agility |
| Cyclomatic complexity, nested loops, N+1 / fetch-in-loop, repeated deep-member access, over-fetching | Elegance |

Compute each sub-score as `100 * (1 - weighted_violations / opportunities)` or simply as a
normalized rank against a baseline — the exact formula is less important than applying it
**consistently** across the applications you compare.

---

## Worked example (illustrative)

A service with 50k LOC:

- Resiliency: 81 🟢 (good error handling; a few missing defaults)
- Agility: 49 🔴 (sparse docs, inconsistent naming, several god-functions)
- Elegance: 70 🟠 (some nested loops and dead code)

```
Health = (81 + 49 + 70) / 3 = 66.7  → 🟠 Orange
```

**Reading:** the blended grade is "orange," but the actionable story is *Agility is red*.
The remediation plan should prioritize documentation, naming, and decomposition — not
error handling (already green) or performance (acceptable). A single grade would have
buried this.

---

## References

- CAST Highlight Software Health / Resiliency / Agility / Elegance indicators —
  https://doc.casthighlight.com/
- For per-finding criteria feeding each dimension, see the
  `universal/process/code-review-standards` references `criteria-efficiency.md` and
  `criteria-transferability.md`.
