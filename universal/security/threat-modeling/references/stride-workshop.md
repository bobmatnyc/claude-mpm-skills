# STRIDE Workshop (Step-by-Step)

## 1) Define Scope and Assets

Inputs:
- What is in scope (feature/system boundary)?
- What data is handled (PII, credentials, payments, proprietary)?
- What is the availability requirement (SLO/SLA)?

Outputs:
- Asset list (data + capabilities)
- Success criteria (what must be protected)

## 2) Draw Data Flows + Trust Boundaries

Keep the diagram simple:
- Actors (users, admins, services)
- Entry points (APIs, UIs, webhooks, background jobs)
- Data stores (DB, cache, object store)
- External dependencies (IdP, payment, email)

Mark trust boundaries:
- Public internet → edge
- Edge → internal network
- Internal service → database
- Service → third-party

## 3) STRIDE Per Element

STRIDE categories:
- **S**poofing identity
- **T**ampering with data
- **R**epudiation
- **I**nformation disclosure
- **D**enial of service
- **E**levation of privilege

Use a table to force completeness:

| Element | STRIDE | Threat | Impact | Likelihood | Mitigation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| API Gateway | Spoofing | Stolen token reuse | Account takeover | Med | Short TTL + rotation + MFA | Security |

## 4) Score and Prioritize

Simple scoring:
- Likelihood: Low/Med/High
- Impact: Low/Med/High

Prioritize:
- High impact + Med/High likelihood
- High likelihood availability issues (DoS) for critical paths

## 5) Turn Mitigations Into Work

Convert mitigations into:
- Engineering tasks (RBAC, rate limiting, encryption)
- Verification tasks (tests, alerting, logging)
- Operational controls (incident runbooks, access reviews)

## 6) Validate and Iterate

Trigger updates:
- New data store or trust boundary
- Auth flow changes
- New third-party integrations
- Major scaling changes

