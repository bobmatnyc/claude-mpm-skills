# Open Source Safety Index (scoring view)

## Overview

Open Source Safety expresses third-party / dependency risk as a single 0 (low safety) to
100 (high safety) index — the average of three independent sub-scores. This reference
covers the **scoring and aggregation** angle. The detailed remediation mechanics (license
tier definitions, CVE-weighting math, audit commands) already live in the Phase 1
references — **cross-reference them, do not duplicate**.

```
Open Source Safety = avg(Security, License Compliance, Obsolescence)
```

> **Source note:** Derived from CAST Highlight's Open Source Safety methodology
> (https://doc.casthighlight.com/). License tiers follow CAST's out-of-the-box profile,
> aligned with https://choosealicense.com/appendix/; CVE weighting follows CVSS/NVD
> severity. Presented as reference guidance, not proprietary calibration.

---

## The three sub-scores

| Sub-score | 0 means | 100 means | Driven by |
|-----------|---------|-----------|-----------|
| **Security** | Many critical CVEs across components | No known CVEs | CVE count **weighted by criticality** (critical > high > medium > low) |
| **License Compliance** | Many high-risk (strong-copyleft) licenses | All permissive | Share of low- vs medium- vs high-risk licenses |
| **Obsolescence** | Components far behind latest | All current | Version gap between detected and latest release |

**Aggregation rule:** average for the headline number, but **gate on the worst
sub-score**. A component can be CVE-clean yet a license liability, or permissively
licensed yet dangerously stale. A high blended score hides a single fatal dimension.

---

## Where the detail lives (do not re-document here)

| You need… | Go to |
|-----------|-------|
| License risk tiers (HIGH = GPL/AGPL/LGPL, MEDIUM = EPL/MPL, LOW = MIT/Apache/BSD) | `toolchains/universal/dependency/audit/references/open-source-safety.md` |
| CVE weighting and obsolescence signals, with `npm audit` / `pip-audit` commands | same audit reference |
| OSS safety as a *security gate* in scanning pipelines | `universal/security/security-scanning/references/open-source-safety.md` |
| Transitive-dependency trust model | CAST methodology `transitive-dependencies-...` (research dir) |

---

## Using the index in a portfolio scorecard

1. Compute the three sub-scores per application from your SCA tooling.
2. Average for the headline OSS Safety number; record the **worst** sub-score alongside it.
3. Feed the OSS Safety number into the overall application scorecard next to Software
   Health and Cloud Maturity (see [quality-communication-guide.md](quality-communication-guide.md)).
4. For prioritization, weight by business impact: a stale, CVE-heavy dependency in a
   revenue-critical app outranks the same in an internal tool.

## References

- CAST Highlight Open Source Safety — https://doc.casthighlight.com/
- License summary — https://choosealicense.com/appendix/
- CVE severity — https://nvd.nist.gov/ (CVSS)
