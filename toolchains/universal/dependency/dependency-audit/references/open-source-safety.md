# Open Source Safety — License Risk, CVE Weighting, and Obsolescence

This audit skill already covers *finding* outdated and vulnerable packages. This
reference adds the **risk-classification** layer: how to decide which findings matter
most, using three independent dimensions that together describe a component's safety.

Score each on a 0 (worst) to 100 (best) mental scale, and gate on the **worst**
dimension — a component can be CVE-clean yet a license liability, or permissively
licensed yet dangerously out of date.

| Dimension | Question it answers | Where it surfaces in this skill |
|-----------|--------------------|--------------------------------|
| **Security** | How much exploitable vulnerability load? | `npm audit`, `pip-audit`, Snyk |
| **License Compliance** | What IP/legal exposure from licenses? | new audit step (below) |
| **Obsolescence** | How far behind latest is it? | `npm outdated`, `pip list --outdated` |

> **Source note:** Framework derived from CAST Highlight's Open Source Safety
> methodology (https://doc.casthighlight.com/). License tiers follow CAST's
> out-of-the-box risk profile, aligned with the copyleft/permissive distinctions at
> https://choosealicense.com/appendix/. Tier groupings and weights are reference
> guidance — calibrate to your own distribution model and legal policy.

---

## 1. License risk tiers

The driving question is **IP-disclosure risk**: if you modify or distribute the
component, what must you disclose?

### HIGH — strong copyleft (whole-application disclosure risk)

Permissions are conditioned on releasing the complete source of the larger work that
incorporates the component, under the same license. This puts your proprietary source
at risk.

- **Examples:** `GPL-2.0`, `GPL-3.0`, `AGPL-3.0`, `LGPL-2.1`, `LGPL-3.0`, `EUPL-1.1`
- **AGPL** extends obligations to network/SaaS use — especially consequential for hosted
  services.
- **Policy:** block by default in distributed/commercial products; require legal sign-off
  and process isolation for any exception.

### MEDIUM — weak copyleft (component-modification disclosure risk)

Only modifications to the component's **own files** must be disclosed, not your whole
app. Bounded, but real if you embed business logic in those edits.

- **Examples:** `MPL-2.0`, `EPL-1.0`
- **Policy:** fine if used **unmodified**; if patched, isolate and disclose the changes.

### LOW — permissive

No disclosure obligation; use/modify/redistribute with attribution.

- **Examples:** `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `BSL-1.0`,
  `Unlicense`
- **Policy:** safe; honor attribution/NOTICE (Apache-2.0 requires preserving NOTICE).

### UNKNOWN / `NOASSERTION`

License could not be confidently matched. **Treat as HIGH until resolved** — never ship
a risk you cannot classify.

| Tier | Disclosure trigger | SPDX examples | Default policy |
|------|--------------------|---------------|----------------|
| HIGH | Whole-app (strong copyleft) | GPL-2.0/3.0, AGPL-3.0, LGPL-2.1/3.0, EUPL-1.1 | Block in distributed products |
| MEDIUM | Component files (weak copyleft) | MPL-2.0, EPL-1.0 | OK unmodified; isolate patches |
| LOW | None (permissive) | MIT, Apache-2.0, BSD-2/3-Clause, BSL-1.0 | OK; honor NOTICE |
| UNKNOWN | Unclassifiable | `NOASSERTION` | Treat as HIGH until identified |

**Auditing licenses in practice:**
```bash
# JavaScript / TypeScript
npx license-checker --summary
npx license-checker --failOn "GPL-3.0;AGPL-3.0;LGPL-3.0"

# Python
pip-licenses --format=markdown
pip-licenses --fail-on "GPL-3.0;AGPL-3.0"
```

Risk is **context-dependent**: an LGPL component may be low concern for an internal tool
and high concern for a shipped binary. Maintain a license policy that reflects how you
deliver software.

---

## 2. CVE weighting — prioritize the Security dimension

A raw vulnerability count misleads. Weight by severity so triage reflects exploitable
risk, not noise. This refines the skill's existing P0–P4 priority matrix.

| Severity | Suggested weight | Maps to priority |
|----------|------------------|------------------|
| Critical | 10 | P0 — patch same day |
| High     | 5  | P1 — plan update (1–2 weeks) |
| Medium   | 2  | P2/P3 — batch / track |
| Low      | 1  | P3/P4 — track with expiry |

Weighted load per component ≈ Σ(count × weight). Pair with **reachability**: a critical
CVE in code you never call is lower real risk than a high CVE on a request path. Gate
critical/high in CI; track medium/low with an owner and expiry date.

---

## 3. Obsolescence scoring

The version gap between what you ship and the latest release is a *leading* risk
indicator — old majors rarely receive security backports.

- **Current / one minor behind** → low obsolescence (good)
- **Several minors behind** → moderate; schedule an update
- **One+ majors behind** → high; plan migration (expect breaking changes), elevated risk
- **Unmaintained upstream** (archived, no recent release) → highest; source a replacement

`npm outdated` / `pip list --outdated` give the raw gap; the obsolescence lens turns it
into a prioritized signal.

---

## 4. Transitive dependencies — "friends of your friends"

Most of your dependency surface is transitive. Those components carry their own CVEs and
licenses, which become yours at runtime — a direct dependency can introduce a
strong-copyleft license or a critical CVE several layers down.

You can't fix what you don't control, but you must have **visibility** and act on the
worst cases:

- If a direct package pulls in **critical transitive CVEs**, upgrade the direct package
  first — maintainers usually patch their own tree in newer releases.
- If a direct package drags in **many** transitive vulnerabilities that don't shrink over
  its release history, find an alternative.
- **Scope matters:** test-scope transitive deps are lower runtime risk than
  compile/runtime-scope ones.

```bash
npm ls vulnerable-package        # locate it in the transitive tree
npm why vulnerable-package       # explain why it's present
```

Generate an SBOM including transitive deps so CVE "are we affected?" queries take minutes.

---

## 5. Adding OSS Safety to the audit workflow

Extend the monthly maintenance checklist with a license + obsolescence pass:

```markdown
### Open Source Safety
- [ ] License scan: no new HIGH-tier (GPL/AGPL/LGPL) or UNKNOWN licenses introduced
- [ ] Severity-weighted CVE review: critical/high blocked; medium/low have owner + expiry
- [ ] Obsolescence: no dependency more than one major behind without a migration plan
- [ ] Transitive review: critical transitive CVEs traced to a direct package to upgrade
```

Ratchet the gate: block regressions first (new critical CVEs, new HIGH-tier licenses),
then tighten thresholds over time to limit churn.
