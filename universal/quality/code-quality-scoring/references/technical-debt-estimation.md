# Technical Debt Estimation

## Overview

Technical debt is most useful when expressed as **estimated remediation effort** — the
hours (or FTE-days, or money) it would take to bring code up to standard. This turns an
abstract "the code is bad" into a number a manager can act on.

```
Estimated debt ≈ violation_count × avg_effort_per_violation
                ≈ LOC × debt_density(language)
```

> **Source note:** The effort-to-fix model and per-language debt-density concept are
> derived from CAST Highlight's Technical Debt and Software Maintenance methodology
> (https://doc.casthighlight.com/), which itself builds on the **COCOMO II** cost model
> (Constructive Cost Model — Post Architecture, https://en.wikipedia.org/wiki/COCOMO).
> The specific debt-density figures are CAST-proprietary, drawn from their AppMarq
> benchmark dataset. **Do not copy CAST's exact per-LOC values.** Use the *relative*
> ranges below and always state your own assumptions.

---

## Per-language debt density — as attributed relative ranges

CAST's benchmark data shows debt-per-LOC varies substantially by technology. The pattern
worth carrying forward is the **relative ordering**, not the absolute numbers:

| Tier | Languages (illustrative) | Relative debt density per LOC |
|------|--------------------------|-------------------------------|
| Higher | Java, JavaScript, PHP, JSP | Roughly **3–4× the lower tier's median**, per industry benchmarks |
| Mid | C#, VB/VB.Net, C++, Objective-C | Roughly **2–2.5× the lower tier** |
| Lower | Python, shell/bash, ABAP | Baseline |
| Database | PL/SQL, Transact-SQL | Narrow band, mid-range median |

**How to phrase this honestly:** *"Per industry benchmarks (CAST AppMarq), Java's median
technical-debt density is on the order of 3–4× Python's. We applied the upper end as a
conservative estimate."* Never state a precise dollars-per-line figure as if it were a
law of nature.

**Why the ordering holds:** more verbose, boilerplate-heavy languages accumulate more
remediable patterns per line; concise scripting languages pack more intent per line and
have fewer ceremonial constructs to get wrong. Treat this as a directional prior, not a
precise multiplier.

---

## Building a back-of-envelope estimate

1. **Count violations** by severity from your scanners (or estimate violation density per
   kLOC if you only have a sample).
2. **Assign an average fix-effort** per severity. A defensible default set:
   - Critical/security: ~2–8 h each
   - High: ~1–4 h each
   - Medium: ~0.25–1 h each
   - Low/cosmetic: ~0.1 h each (often batch-fixable, so cap the total)
3. **Sum** to total hours; divide by working hours/FTE-day to get FTE effort.
4. **Apply the language prior** as a sanity check: if your bottom-up estimate for a Java
   service comes out far below the Python prior, re-examine — you likely under-counted.
5. **State assumptions inline**: LOC, density source, hourly cost, and that estimates are
   ±50% at this fidelity.

### Worked example (illustrative)

A 50k-LOC Java service, scanner reports: 12 high, 140 medium, 600 low violations.

```
high:    12 × 3 h   =   36 h
medium: 140 × 0.5 h =   70 h
low:    600 × 0.1 h =   60 h (cap if batch-fixable)
                       --------
total  ≈ 166 h ≈ ~1 FTE-month
```

Sanity check against language prior: Java is in the higher debt tier, so ~3 h/kLOC of
remediable debt is plausible (166 h / 50 kLOC ≈ 3.3 h/kLOC). The estimate is internally
consistent.

**Present it as:** *"Roughly one FTE-month (±50%) to clear the current backlog, assuming
$X/hour and the violation effort defaults stated above."*

---

## Maintenance effort (COCOMO II linkage)

For ongoing maintenance rather than one-time remediation, CAST's model derives a
*recommended* maintenance FTE from COCOMO II cost drivers plus the quality scores: higher
Agility/Elegance scores → lower recommended maintenance effort. The actionable takeaway:
**improving Agility and Elegance scores reduces the steady-state cost of owning the code**,
which is the business case for paying down debt. Cite COCOMO II as the primary source for
any effort math, not CAST's calibration.

---

## Caveats

- Estimates are directional, not precise — communicate confidence bands.
- Violation counts depend on scanner configuration; hold it constant across comparisons.
- Debt density is a prior, not a measurement — a clean Java service can beat a messy
  Python one. Use bottom-up counts as the primary estimate and the prior as a check.
- Never present CAST's exact per-LOC dollar figures verbatim; they are proprietary.

## References

- CAST Highlight Technical Debt & Software Maintenance methodology —
  https://doc.casthighlight.com/
- COCOMO II — https://en.wikipedia.org/wiki/COCOMO
- For OSS-component debt (obsolescence), see [open-source-safety.md](open-source-safety.md).
