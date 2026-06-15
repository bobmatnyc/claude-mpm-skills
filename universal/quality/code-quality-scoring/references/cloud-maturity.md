# Cloud Maturity / Cloud Readiness

## Overview

Cloud Maturity measures how well an application is suited to run in (or move to) a cloud
environment. Score it 0 (low maturity) to 100 (high maturity) as the average of two
independent parts:

```
Cloud Maturity = avg(Cloud Scan, Cloud Survey)
```

> **Source note:** This model is derived from CAST Highlight's Cloud Maturity indicator
> (https://doc.casthighlight.com/). It is paraphrased and re-expressed vendor-neutrally;
> the blocker/booster examples below are original, illustrating the concept rather than
> reproducing CAST's catalog.

---

## Cloud Scan — what the code reveals (0–100)

Computed from **blockers** (patterns that resist cloud deployment) and **boosters**
(patterns that ease it) detected in source code. The principle: cloud-native code is
stateless, externally configured, and makes no assumptions about the host.

**Common blockers (lower the score):**

| Blocker | Why it resists the cloud |
|---------|--------------------------|
| Hard-coded file paths (`/var/app/...`, `C:\...`) | Ephemeral containers have no stable local filesystem |
| Hard-coded host names / IPs / ports | Services move; addresses must be injected, not baked in |
| Local session / in-memory state assumed sticky | Horizontal scaling needs externalized session state |
| Writing to local disk for persistence | Container filesystems are ephemeral; use object storage |
| OS-specific calls, local scheduled jobs (cron), GUI/console assumptions | Tie the app to a specific host |
| Heavyweight, slow startup | Fights autoscaling and fast restarts |

**Common boosters (raise the score):**

| Booster | Why it helps |
|---------|--------------|
| Config read from environment variables / config service | 12-factor; portable across environments |
| Stateless request handling | Scales horizontally without sticky sessions |
| External datastore / object storage for persistence | Survives container restarts |
| Health/readiness endpoints | Orchestrators can manage lifecycle |
| Graceful shutdown handling | Clean draining during rescheduling |

---

## Cloud Survey — what the code cannot reveal (0–100)

A questionnaire covering team and operational factors that static analysis cannot see:
CI/CD maturity, observability, deployment automation, team cloud experience,
licensing/compliance constraints, data-residency requirements. Even perfectly
cloud-native code scores low overall if the surrounding organization cannot operate it in
the cloud.

---

## How to read and act on the score

1. **Low Cloud Scan, adequate Survey** → the *code* is the bottleneck. Prioritize
   removing blockers (externalize config, remove local-disk persistence, add health
   endpoints).
2. **Adequate Cloud Scan, low Survey** → the *organization* is the bottleneck. Invest in
   CI/CD, observability, and team enablement before migrating.
3. **Both low** → re-platforming is a multi-quarter effort; sequence code remediation and
   org enablement deliberately.

Use Cloud Maturity as a **migration-readiness gate**, not a code-quality grade: a clean,
well-tested monolith can still score low if it assumes a fixed host.

## References

- CAST Highlight Cloud Maturity indicator — https://doc.casthighlight.com/
- The Twelve-Factor App (open standard for cloud-native config/state) —
  https://12factor.net/
