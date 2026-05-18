# Stage 5: Security Review — Detailed Protocol

## Purpose

Security review is a distinct pass from code quality review. Where Stage 4 (Critic)
checks structure, style, and correctness, Stage 5 checks for exploitable vulnerabilities.
A clean critic APPROVE does not guarantee security — the security agent applies a different
lens and terminates the pipeline if CRITICAL or HIGH vulnerabilities are found.

## Agent

- **Agent:** `security`
- **Skills loaded:** none required beyond agent's built-in security knowledge

## Scope

The security agent reviews ONLY for security vulnerabilities. It MUST NOT re-flag issues
already addressed by the critic (code style, coverage, type hints). Scope is:

### OWASP Top 10 Mapping

| OWASP Category | What to Check |
|----------------|---------------|
| A01 Broken Access Control | Auth checks on every protected path; no privilege escalation paths |
| A02 Cryptographic Failures | No MD5/SHA1 for passwords; TLS enforced; no plaintext secrets |
| A03 Injection | SQL, shell, template, LDAP, XPath — parameterized only |
| A04 Insecure Design | Business logic flaws; missing rate limits on sensitive endpoints |
| A05 Security Misconfiguration | Debug flags off in prod; no default credentials; no directory listing |
| A06 Vulnerable Components | Dependencies with known CVEs (check `pip-audit` or `safety` output) |
| A07 Auth Failures | Session management; token expiry; brute-force protection |
| A08 Software/Data Integrity | Deserialization of untrusted data (`pickle.loads`, `yaml.load`) |
| A09 Logging Failures | Secrets logged; PII logged; insufficient audit trail |
| A10 SSRF | User-controlled URLs fetched server-side without validation |

### Additional Security Checks

- **Hardcoded secrets:** grep for `api_key`, `password`, `secret`, `token` in literals
- **Arbitrary code execution:** `eval`, `exec`, `subprocess` with shell=True + user input
- **Path traversal:** user-controlled filenames used in `open()`, `os.path.join()`
- **XML vulnerabilities:** XXE in `lxml`, `xml.etree` with external entity loading
- **Timing attacks:** non-constant-time comparison for secrets/tokens

## Dispatch Prompt Template

```
Security review task.

Review the following implementation for security vulnerabilities.
Scope: OWASP Top 10, secrets exposure, injection, auth bypass, code execution paths.
Do NOT flag code style, coverage, or type hint issues — focus only on exploitable flaws.

== IMPLEMENTATION (source files) ==
[paste source file(s) verbatim]

Required output format:
1. SECURITY VERDICT: PASS / WARN / BLOCK (first line)
   - PASS: zero CRITICAL or HIGH security findings
   - WARN: zero CRITICAL, one or more HIGH (pipeline proceeds with findings logged)
   - BLOCK: any CRITICAL finding (pipeline halts)
2. Finding table:
   | Severity | File | Line | Vulnerability | Remediation |
3. Summary paragraph
```

## Gate

Zero CRITICAL or HIGH security findings. If any CRITICAL or HIGH:
- PM halts pipeline
- PM surfaces finding table verbatim to user
- Same protocol as a critic BLOCK (see Verdict Protocol in SKILL.md)

## TODO: Expand with tooling integration

<!-- TODO: Add pip-audit / safety command for dependency vulnerability scanning -->
<!-- TODO: Add bandit static analysis configuration and interpretation -->
<!-- TODO: Add patterns for common false positives (crypto in tests, test hardcoded secrets) -->
<!-- TODO: Add SSRF validation patterns for URL-fetching code -->
