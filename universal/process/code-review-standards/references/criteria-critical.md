# CRITICAL Criteria — Detailed Explanations

## Overview

CRITICAL findings block delivery. Any CRITICAL in the critic output produces a BLOCK
verdict. The implementation must be returned to Stage 3 and the specific CRITICAL
issues fixed before the pipeline can proceed.

CRITICAL criteria represent conditions where the shipped code would create an
exploitable vulnerability, data breach risk, or unrecoverable system failure.

---

## 1. No hardcoded secrets, API keys, or credentials

**What to look for:**
- String literals matching patterns: `sk-`, `ghp_`, `AWS`, `AKIA`, `password=`, `secret=`, `api_key=`
- Credentials assigned directly in source: `API_KEY = "abc123"`, `DB_PASSWORD = "hunter2"`  <!-- pragma: allowlist secret -->
- Tokens committed in test fixtures or default config values

**Why CRITICAL:**
Hardcoded secrets are extracted from source control or deployed artifacts. They cannot
be rotated without a code change. Every developer who clones the repo has the credential.

**Required fix:**
Move to environment variable. Access via `os.environ["KEY_NAME"]` or a secrets manager.
Add the variable name (not value) to `.env.example`.

**False positive filter:**
Placeholder values like `"YOUR_API_KEY_HERE"` or `"<replace_me>"` are not findings.
Test fixtures that use obviously fake values (`"test-secret-abc"` alongside `@pytest.mark`)
may be acceptable — note as a question if confidence is below 80%.

---

## 2. No SQL injection vectors

**What to look for:**
- String formatting in SQL queries: `f"SELECT * FROM users WHERE id = {user_id}"`
- `.format()` in SQL strings
- String concatenation building SQL: `"SELECT * FROM " + table_name`

**Why CRITICAL:**
SQL injection allows attackers to read, modify, or delete arbitrary database data.

**Required fix:**
Use parameterized queries: `cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))`
or ORM query builders that handle parameterization automatically.

---

## 3. No arbitrary code execution paths

**What to look for:**
- `eval(user_input)` or `eval(f"...")`
- `exec(user_input)` or `exec(config_value)`
- `pickle.loads(data)` where `data` comes from an untrusted source (network, user upload, DB)
- `subprocess.run(user_input, shell=True)` or `os.system(user_controlled_string)`

**Why CRITICAL:**
These patterns allow remote code execution (RCE) — an attacker can run arbitrary commands
on the server.

**Required fix:**
Replace `eval`/`exec` with safe alternatives (AST parsing, allowed-list dispatch).
Replace `pickle` with `json` or `msgpack` for untrusted data. Use `subprocess.run`
with a list argument (not shell=True) and a validated allow-list of commands.

---

## 4. Authentication/authorization not bypassable

**What to look for:**
- Auth checks that only run on some code paths (missing decorator on one route)
- `if user_id == admin_id:` comparisons using user-supplied values without DB verification
- JWT validation that checks signature but not expiry, or expiry but not signature
- Role checks that can be bypassed by manipulating request parameters

**Why CRITICAL:**
Auth bypass allows unprivileged users to access privileged data or operations.

**Required fix:**
Ensure every protected endpoint has auth validation at the framework level (decorator,
middleware) — not inline. Verify tokens fully: signature, expiry, issuer, audience.

---

## 5. No infinite loops without escape conditions

**What to look for:**
- `while True:` without a `break` condition reachable under all inputs
- Recursive functions without a guaranteed base case
- Retry loops without a maximum attempt count and backoff

**Why CRITICAL:**
Infinite loops cause server hangs, CPU exhaustion, and denial-of-service conditions.

**Required fix:**
Add explicit termination: maximum iteration count, timeout, or guaranteed base case.
For retry loops: use exponential backoff with a maximum retry ceiling.

---

## TODO: Expand with language-specific patterns

<!-- TODO: Add TypeScript/JavaScript patterns (prototype pollution, XSS via innerHTML) -->
<!-- TODO: Add Go patterns (goroutine leaks, nil pointer dereference patterns) -->
<!-- TODO: Add examples for each criterion with before/after code snippets -->
<!-- TODO: Add guidance on ORM-level injection (e.g., SQLAlchemy raw() misuse) -->
