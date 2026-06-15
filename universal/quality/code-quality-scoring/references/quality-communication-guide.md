# Quality Communication Guide

## Overview

A health score nobody acts on is wasted work. This reference covers two things: how to
**prioritize** remediation by business impact, and how to **present** quality and debt to
people who do not read code.

> **Source note:** The business-impact weighting and ROAR-style prioritization are derived
> from CAST Highlight's Business Impact and ROAR (Ranking of Application Risks) indicators
> (https://doc.casthighlight.com/). The exact ROAR weighting formula is CAST's proprietary
> calibration and is described here as reference context, not reproduced as a normative
> standard.

---

## 1. Prioritize by business-weighted risk, not defect count

The mistake teams make is fixing the application with the most findings. The right target
is the application where **technical risk × business importance** is highest.

**Business Impact** captures how much the organization depends on an application. Score it
from factors the code cannot reveal (a short survey):

- Would failure cause service disruption, revenue loss, or reputational harm?
- Would failure erode customer confidence?
- Internal users, external users, or both? How many?
- How many major releases and how much maintenance effort in the last 12 months?
- Is the app aligned with the company's future technology direction?

Combine the answers into a single 0–100 Business Impact score (weighted average).

**Risk ranking (ROAR-style).** CAST blends the three health factors — weighting
**Resiliency most heavily**, then Elegance, then Agility — and multiplies by Business
Impact. The vendor-neutral takeaway you can carry without copying the formula:

```
Priority ≈ (technical_risk, weighted toward Resiliency) × business_impact
```

- **High risk + high impact** → urgent; investigate now.
- **High risk + low impact** → schedule; not urgent.
- **Low risk + high impact** → monitor; keep it healthy.
- **Low risk + low impact** → leave it; possibly a retirement candidate.

This is why Resiliency is weighted heaviest: a reliability defect in a revenue-critical
app is the worst combination — likely to fail *and* expensive when it does.

---

## 2. Present scores to non-technical stakeholders

### Lead with risk and money, not rule names

| Don't say | Say |
|-----------|-----|
| "We have 600 `alt_genericcatches` violations." | "Error handling is below standard in our most-used app; this raises the odds of an outage we can't diagnose quickly." |
| "Software Agility is 49." | "Changes to this app are slow and risky to make — onboarding a new engineer takes weeks, and small features take longer than they should." |
| "Debt density is 3.3 h/kLOC." | "Clearing the known issues is roughly one engineer-month; left alone, every change keeps costing extra." |

### Use the traffic-light bands

Red/orange/green maps cleanly to executive dashboards. Pair each color with one sentence
of consequence and one recommended action. Never present a number without a "so what."

### Always state assumptions for money figures

When you convert debt to dollars, show the inputs: LOC, debt-density range (attributed),
hourly cost, and a confidence band (±50% at low fidelity). Unqualified dollar figures
invite false precision and erode trust.

### Frame paying down debt as reducing run-cost

The strongest business case: higher Agility/Elegance scores reduce the steady-state
maintenance effort (the COCOMO II linkage — see
[technical-debt-estimation.md](technical-debt-estimation.md)). "Fixing this lowers what it
costs us to own this app every quarter" lands better than "the code is cleaner."

---

## 3. A one-page application scorecard template

```
Application: <name>          Business Impact: <0-100>  🟢/🟠/🔴
------------------------------------------------------------------
Software Health:  <0-100> 🟠   (Resiliency <n> / Agility <n> / Elegance <n>)
Open Source Safety: <0-100> 🔴  (worst sub-score: License Compliance)
Cloud Maturity:   <0-100> 🟠   (Scan <n> / Survey <n>)
------------------------------------------------------------------
Top risk:     <one sentence, business framed>
Recommended:  <one action> — est. <effort range, ±band>
Priority:     <urgent / scheduled / monitor / retire>
```

Map scores to team actions consistently across the portfolio so two reviewers reach the
same recommendation from the same numbers.

## References

- CAST Highlight Business Impact & ROAR indicators — https://doc.casthighlight.com/
- COCOMO II (maintenance-effort basis) — https://en.wikipedia.org/wiki/COCOMO
