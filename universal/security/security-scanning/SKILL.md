---
name: security-scanning
description: "CI security scanning: secrets, deps, SAST, triage, expiring exceptions"
user-invocable: false
disable-model-invocation: true
license: MIT
compatibility: claude-code
metadata:
  version: 1.2.0
  category: universal
  author: Claude MPM Team
  updated: "2026-06-15"
progressive_disclosure:
  entry_point:
    summary: "Baseline CI scans (secrets, deps, SAST) with triage and expiring exceptions"
tags: [security, scanning]
---

# Security Scanning

## Quick Start

- Secrets: fail fast; rotate on exposure.
- Dependencies: gate critical/high; automate updates.
- SAST: start high-signal; ratchet over time.
- Open Source Safety: score components on three axes — license tier, severity-weighted CVEs, obsolescence.
- Exceptions: require reason, owner, and expiry.

## Open Source Safety

Third-party component risk is more than "vulnerable: yes/no". Evaluate each component on
three independent dimensions and gate on the worst:

- **License risk:** HIGH = strong copyleft / GPL/AGPL/LGPL (whole-app disclosure risk);
  MEDIUM = weak copyleft / MPL, EPL (modification disclosure only); LOW = permissive /
  MIT, Apache-2.0, BSD. Unknown/`NOASSERTION` → treat as HIGH until identified.
- **CVE weighting:** weight by severity (critical ≫ high ≫ medium ≫ low) rather than raw
  counts; critical/high block, medium/low track with owner + expiry.
- **Obsolescence:** score the gap to latest version; majors-behind or unmaintained
  upstream is elevated risk.

See `references/open-source-safety.md` for the full framework, tier tables, the CVE
weighting model, obsolescence scoring, and the transitive-dependency trust model.

## Load Next (References)

- `references/tooling-matrix.md`
- `references/ci-workflows.md`
- `references/triage-and-remediation.md`
- `references/common-findings-and-fixes.md`
- `references/supply-chain-and-sbom.md`
- `references/open-source-safety.md`
