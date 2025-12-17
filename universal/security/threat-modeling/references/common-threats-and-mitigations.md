# Common Threats and Mitigations

## Authentication and Sessions

Threats:
- Credential stuffing and brute force
- Token theft and replay
- Session fixation

Mitigations:
- Rate limiting and IP/device risk checks
- Short-lived tokens + refresh rotation
- Secure cookie settings (`HttpOnly`, `Secure`, `SameSite`)
- MFA for privileged actions

## Authorization (IDOR / Privilege Escalation)

Threats:
- Insecure direct object reference (accessing another tenant’s data)
- Missing authorization checks on internal APIs

Mitigations:
- Centralized authorization checks (policy layer)
- Tenant isolation (row-level security, scoped queries)
- Audit access to privileged endpoints

## Input Handling (Injection)

Threats:
- SQL/NoSQL injection
- Command injection
- Template injection

Mitigations:
- Parameterized queries
- Strict input validation and schema enforcement
- Avoid dynamic eval/templating with untrusted input

## Web Threats

Threats:
- XSS
- CSRF
- SSRF

Mitigations:
- Output encoding + CSP
- CSRF tokens and SameSite cookies
- Egress allowlists, metadata service protections, URL validation

## Secrets and Key Management

Threats:
- Secrets in logs, builds, or repos
- Over-privileged keys

Mitigations:
- Secret scanning in CI
- Secret manager integration + rotation
- Least-privilege IAM and scoped credentials

## Supply Chain

Threats:
- Dependency confusion / typosquatting
- Compromised build pipeline

Mitigations:
- Pin dependencies and verify integrity
- Use lockfiles and provenance (SBOM, SLSA levels where feasible)
- Restrict CI tokens and sign artifacts

## Availability (DoS)

Threats:
- Resource exhaustion (CPU/memory/DB connections)
- Hot endpoints and cache misses

Mitigations:
- Rate limiting and quotas
- Timeouts, retries with backoff, circuit breakers
- Caching and bulkheads (separate resource pools)

## Logging and Repudiation

Threats:
- Missing audit trail for sensitive actions
- Log tampering

Mitigations:
- Append-only audit logs for authz and data access
- Centralized log storage with access controls
- Include request IDs and actor identity in audit events

