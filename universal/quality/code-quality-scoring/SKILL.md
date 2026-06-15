---
name: code-quality-scoring
description: "Vendor-neutral framework for scoring software health, estimating technical debt, assessing cloud readiness and open-source safety, and communicating quality to business stakeholders. Use when you need to quantify code health at the application or portfolio level rather than fix individual findings."
user-invocable: false
disable-model-invocation: true
version: 1.0.0
updated: "2026-06-15"
category: universal
author: bobmatnyc
license: Apache-2.0
progressive_disclosure:
  entry_point:
    summary: "Score software health (Resiliency + Agility + Elegance), estimate technical debt, assess cloud readiness and open-source safety, and frame all of it for business stakeholders"
    when_to_use: "When assessing a whole codebase for health/debt/cloud-readiness, prioritizing remediation across a portfolio, or translating quality metrics into business language — not when fixing a single lint finding"
    quick_start: "1. Compute Software Health as the average of Resiliency, Agility, Elegance sub-scores 2. Apply the red/orange/green bands 3. Convert violation density into an effort-to-fix estimate 4. Weight by business impact to prioritize 5. Present using the stakeholder framing in quality-communication-guide.md"
  references:
    - software-health-framework.md
    - technical-debt-estimation.md
    - cloud-maturity.md
    - open-source-safety.md
    - quality-communication-guide.md
context_limit: 800
tags:
  - code-quality
  - software-health
  - technical-debt
  - cloud-readiness
  - open-source-safety
  - metrics
  - portfolio
requires_tools: []
---

# Code Quality Scoring

A vendor-neutral framework for **quantifying and communicating** software quality at the
application and portfolio level. Most quality skills tell you how to fix one finding;
this skill tells you how to *score* an entire codebase, *estimate* the cost of its debt,
and *explain* both to people who do not read code.

> **Source note:** The scoring frameworks below are derived from CAST Highlight's code
> quality indicators and methodology (https://doc.casthighlight.com/). They are
> paraphrased and re-expressed as a vendor-neutral model. Threshold bands and
> debt-density figures are CAST's proprietary calibration from their AppMarq benchmark
> dataset; they are presented here as **attributed reference ranges**, not as universal
> standards. Where CAST defers to open standards (COCOMO II for effort, SPDX/choosealicense
> for licenses, CWE/CVE for security), cite those primary sources.

## When to Use This Skill

Use it when the question is **"how healthy is this codebase, and what should we do
first?"** — for example:

- Onboarding to an unfamiliar codebase and needing a health baseline.
- Deciding whether to refactor, rewrite, or retire an application.
- Prioritizing remediation across many applications (a portfolio).
- Estimating the effort/cost a backlog of quality defects represents.
- Presenting a quality/debt position to a manager, product owner, or executive.

Do **not** reach for it to fix a single defect — for that, use the language-specific
quality skills (Python/Java/PHP/TS quality anti-patterns) and `code-review-standards`.

## Core Concept 1 — Software Health is a composite

Treat overall code health as the straight average of three independent dimensions, each
scored 0–100. This decomposition (derived from CAST Highlight) is useful because each
dimension maps to a *different* class of fix and a *different* stakeholder concern:

| Dimension | A.k.a. | Measures | Maps to checklist family |
|-----------|--------|----------|--------------------------|
| **Resiliency / Robustness** | Software Resiliency | Will it break in production? Error handling, defensive coding, reliability | Robustness, Security |
| **Agility / Changeability** | Software Agility | Can a team understand and change it quickly? Documentation, readability, naming | Changeability, Transferability |
| **Elegance / Efficiency** | Software Elegance | Is it lean? Complexity, dead code, algorithmic/data-access efficiency | Efficiency |

```
Software Health = avg(Resiliency, Agility, Elegance)
```

**Threshold bands** (attributed to CAST's calibration — use as guidance, not gospel):

| Band | Health | Agility (note the different cutoffs per dimension) |
|------|--------|-----------------------------------------------------|
| 🔴 Low / Red | below ~53 | below ~54 |
| 🟠 Medium / Orange | ~53–75 | ~54–69 |
| 🟢 High / Green | above ~75 | above ~69 |

The key insight is *not* the exact numbers — it is that each dimension has its own
distribution and its own remediation strategy, so a single blended grade hides the story.
A codebase can be green on Resiliency (rarely crashes) yet red on Agility (nobody can
change it safely). See **[software-health-framework.md](references/software-health-framework.md)**.

## Core Concept 2 — Technical debt is an effort-to-fix estimate

Express debt as **estimated remediation effort**, derived from violation density scaled
by a per-line-of-code debt factor that varies by language. Higher-level / verbose
languages (Java, JavaScript, PHP) tend to carry more debt per LOC than concise scripting
languages (Python, shell). Always present these as **attributed ranges** ("Java's median
debt density is roughly 3–4× Python's per industry benchmarks") rather than copied exact
figures, and convert to money/time only with explicit assumptions stated. CAST's
maintenance-effort model itself builds on **COCOMO II**. See
**[technical-debt-estimation.md](references/technical-debt-estimation.md)**.

## Core Concept 3 — Cloud readiness is scan + survey

Cloud maturity is the average of a **code-scan** score (blockers and boosters detected in
source — e.g. hard-coded file paths and host names are blockers; statelessness and
externalized config are boosters) and a **survey** score (team/operational factors the
code cannot reveal). See **[cloud-maturity.md](references/cloud-maturity.md)**.

## Core Concept 4 — Open-source safety is a three-part index

Third-party risk is the average of **Security** (CVE count weighted by criticality),
**License Compliance** (share of low- vs medium- vs high-risk licenses), and
**Obsolescence** (version gap to latest). This cross-references the Phase 1 OSS Safety
work — do not duplicate it. See **[open-source-safety.md](references/open-source-safety.md)**,
and for remediation mechanics use `universal/security/security-scanning` and
`toolchains/universal/dependency/audit`, which already carry the license-risk tiers and
CVE-weighting framing.

## Core Concept 5 — Prioritize by business impact

A defect-dense application nobody depends on is lower priority than a moderately-flawed
revenue-critical one. Blend a technical risk score with a **business impact** score
(failure consequences, audience size, release/maintenance effort) so remediation is
ranked by *risk to the business*, not by raw defect count. CAST formalizes this as a
ROAR-style index (risk weighted by business impact). See
**[quality-communication-guide.md](references/quality-communication-guide.md)**.

## How to Apply (quick workflow)

1. **Score the three health dimensions** from your existing linters/scanners — map each
   tool's findings into Resiliency / Agility / Elegance, average to a Health score, place
   on the red/orange/green band.
2. **Estimate debt** — multiply violation density by the language's debt factor (as an
   attributed range), express as effort (hours/FTE) with assumptions stated.
3. **Score OSS safety and cloud readiness** if relevant to the decision.
4. **Weight by business impact** to rank applications/modules.
5. **Communicate** using the stakeholder framing — lead with risk and money, not rule
   names.

## Anti-Patterns

- **Reporting a single blended grade** and hiding the dimension that is actually red.
- **Quoting debt in exact dollars** without stating the LOC, hourly rate, and density
  assumptions — present ranges and assumptions.
- **Treating CAST's threshold numbers as universal law** — they are one vendor's
  calibration; cite them as reference context.
- **Ranking remediation by defect count** instead of by business-weighted risk.
- **Duplicating the OSS license tiers here** — cross-reference the Phase 1 references.

## Navigation

- **[Software Health Framework](references/software-health-framework.md)** — the
  Resiliency/Agility/Elegance decomposition, bands, and how to map linter output onto it.
- **[Technical Debt Estimation](references/technical-debt-estimation.md)** — effort-to-fix
  model, per-language debt-density ranges (attributed), COCOMO II linkage, worked example.
- **[Cloud Maturity](references/cloud-maturity.md)** — scan vs survey, code blockers and
  boosters, how to read a cloud-readiness score.
- **[Open Source Safety](references/open-source-safety.md)** — the Security/License/
  Obsolescence index; cross-references to the dependency-audit and security-scanning skills.
- **[Quality Communication Guide](references/quality-communication-guide.md)** — business-
  impact framing, ROAR-style prioritization, presenting scores to non-technical stakeholders.

## Related Skills

- **code-review-standards** — per-finding checklist with Efficiency + Transferability
  dimensions (Phase 1); this skill aggregates those families into scores.
- **security-scanning** / **dependency-audit** — OSS safety remediation mechanics.
- **software-patterns** — architectural signals that low Elegance/Agility scores point to.
