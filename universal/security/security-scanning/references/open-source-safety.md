# Open Source Safety — License Risk, CVE Weighting, and Obsolescence

A structured way to reason about third-party / open-source component risk beyond a
binary "vulnerable: yes/no". An overall **Open Source Safety** posture combines three
independent dimensions, each scored 0 (worst) to 100 (best):

1. **Security** — vulnerability load, weighted by CVE severity
2. **License Compliance** — legal/IP risk from component license types
3. **Obsolescence** — how far behind latest each component is

Treat these as three separate gates: a component can be CVE-clean but a license
liability, or fully permissive but dangerously out of date. The aggregate is only as
useful as the worst dimension you ignore.

> **Source note:** This framework is derived from CAST Highlight's Open Source Safety
> methodology (https://doc.casthighlight.com/). License-tier groupings follow CAST's
> out-of-the-box risk profile, which itself maps to the copyleft/permissive
> distinctions summarized at https://choosealicense.com/appendix/. Tier assignments and
> scoring weights here are presented as reference guidance, not normative standards —
> calibrate to your own distribution model and legal policy.

---

## 1. License risk tiers

The driving question is **IP disclosure risk**: if your team modifies (or, for strong
copyleft, merely links/distributes) the component, what are you obligated to disclose?

### HIGH risk — strong copyleft (proprietary-disclosure risk)

If the license can force disclosure of **your own application's** source code, it is
HIGH risk. Strong copyleft licenses condition their permissions on releasing the
complete source of larger works that incorporate the licensed code, under the same
license.

- **Examples:** `GPL-2.0`, `GPL-3.0`, `AGPL-3.0`, `LGPL-2.1`, `LGPL-3.0`, `EUPL-1.1`
- **Why it matters most for:** distributed software, mobile apps, embedded, and any
  product you ship to customers. AGPL extends obligations to network/SaaS use, so it is
  especially consequential for hosted services.
- **Action:** block by default in distributed/commercial products; require explicit
  legal sign-off and an architectural isolation plan (separate process, no linking)
  before any exception.

### MEDIUM risk — weak copyleft (library-modification disclosure risk)

If the license only forces disclosure of **modifications to the component's own files**
(not your whole application), it is MEDIUM risk. The scope is bounded — but still real,
because business logic embedded in those edits would have to be published.

- **Examples:** `MPL-2.0` (Mozilla Public License), `EPL-1.0` (Eclipse Public License)
- **Action:** allowed if you use the component **unmodified**; if you must patch it,
  keep changes minimal and isolated, and disclose those file-level modifications.

### LOW risk — permissive

If neither proprietary-disclosure nor modification-disclosure obligations apply, it is
LOW risk. These permit use, modification, and redistribution with attribution only.

- **Examples:** `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `BSL-1.0`,
  `Unlicense`
- **Action:** generally safe; still record attribution/NOTICE obligations (Apache-2.0
  requires preserving NOTICE files).

### Unknown / unmatched licenses

Components whose license cannot be confidently identified (often tagged `NOASSERTION`)
should be treated as **HIGH risk until resolved** — you cannot accept a risk you cannot
classify. Investigate the upstream project's actual license before shipping.

| Tier | Disclosure trigger | Representative SPDX IDs | Default policy |
|------|--------------------|--------------------------|----------------|
| HIGH | Whole-app source disclosure (strong copyleft) | GPL-2.0/3.0, AGPL-3.0, LGPL-2.1/3.0, EUPL-1.1 | Block in distributed products; legal sign-off for exceptions |
| MEDIUM | Component-file modifications only (weak copyleft) | MPL-2.0, EPL-1.0 | Allowed unmodified; isolate & disclose any patches |
| LOW | None (permissive) | MIT, Apache-2.0, BSD-2/3-Clause, BSL-1.0, Unlicense | Allowed; honor attribution/NOTICE |
| UNKNOWN | Unclassifiable (`NOASSERTION`) | — | Treat as HIGH until identified |

> Risk depends on **your distribution context**. The same LGPL component may be low
> concern for an internal tool and high concern for a shipped binary. Build a license
> profile that reflects how your software is delivered.

---

## 2. CVE weighting (the Security dimension)

A raw vulnerability count is misleading — one critical RCE outweighs twenty low-severity
informational findings. Weight findings by severity so the score reflects exploitable
risk, not noise.

**Weighting model (illustrative — tune to your policy):**

| Severity | Suggested weight | Rationale |
|----------|------------------|-----------|
| Critical | 10 | RCE, auth bypass, actively exploited — same-day response |
| High     | 5  | Serious, exploitable under realistic conditions |
| Medium   | 2  | Conditional or limited impact |
| Low      | 1  | Informational / hard to exploit |

**Weighted risk per component** ≈ Σ(count_severity × weight_severity), then normalize
against component count so a large portfolio isn't penalized purely for size. A higher
weighted load → lower Security sub-score.

**Use it to prioritize**, mirroring the skill's triage gate: critical/high block the
build; medium/low are tracked with an owner and expiry. Combine weighting with
*reachability* where possible — a critical CVE in a code path you never call is lower
real risk than a high CVE on your request path.

---

## 3. Obsolescence scoring

Out-of-date components accumulate unpatched bugs and drift away from the security fixes
that only land in current releases. Score the **version gap** between what you ship and
the latest known release of each component.

A practical obsolescence signal per component:

- **Current / one minor behind** → low obsolescence (good)
- **Several minors behind, same major** → moderate; schedule an update
- **One or more majors behind** → high obsolescence; plan a migration (breaking changes
  likely), and treat as elevated risk because security backports to old majors are rare
  to nonexistent
- **Unmaintained upstream** (no release in a long window, archived repo) → highest
  concern; begin sourcing a replacement

Obsolescence is a *leading* indicator: a component falling behind today is where
tomorrow's unpatched CVE will sit.

---

## 4. Transitive dependencies — "friends of your friends"

Most of your real dependency surface is **transitive**: the components your direct
dependencies pull in. They carry their own CVEs and licenses, which become yours at
runtime. A direct dependency can quietly introduce a strong-copyleft license or a
critical CVE three layers down.

You will not fix every transitive issue — you don't control them — but you must have
**visibility** and act on the worst:

- If a direct component pulls in **critical transitive CVEs**, upgrade that direct
  component first; maintainers usually patch their own dependency tree in newer releases.
- If a direct component drags in **many** transitive vulnerabilities that don't shrink
  over its release timeline, treat that as a signal to find an alternative component.
- Scope matters: **test-scope** transitive deps are lower runtime risk than
  **compile/runtime-scope** ones. Prioritize what actually executes in production.

Generate an SBOM **including transitive dependencies** so "are we affected?" queries
during a CVE event can be answered in minutes, not days (see
`supply-chain-and-sbom.md`).

---

## 5. Putting it together — a gate

At ingestion and in CI, evaluate each new or updated component on all three axes:

1. **License** — is the tier acceptable for our distribution model? (HIGH → block /
   legal review; UNKNOWN → resolve before merge)
2. **Security** — does the severity-weighted CVE load cross the gate? (critical/high →
   block; medium/low → track with owner + expiry)
3. **Obsolescence** — is it current enough, and is upstream alive?

Ratchet the gate: start by blocking only regressions (new critical CVEs, new HIGH-tier
licenses), then tighten thresholds over time to avoid churn — consistent with the
skill's exception model (reason, owner, expiry).
