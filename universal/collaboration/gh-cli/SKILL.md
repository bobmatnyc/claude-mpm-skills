---
name: gh-cli
description: Reliably drive the GitHub gh CLI for issue, PR, and label operations in automation and subagent environments, with pre-flight verification so you never fabricate a success or a fake issue URL.
user-invocable: false
disable-model-invocation: true
license: Apache-2.0
compatibility: claude-code
metadata:
  updated_at: 2026-05-29T00:00:00Z
tags: [github, gh, cli, issues, pull-requests, labels, automation, ci, troubleshooting]
progressive_disclosure:
  entry_point:
    summary: "Reliably drive the GitHub gh CLI for issue/PR/label work, with pre-flight auth verification so you never fabricate a success."
    when_to_use: "When creating, listing, editing, or closing GitHub issues/PRs/labels via gh, especially inside automation or a subagent shell."
    quick_start: "1. Run gh auth status and gh repo view BEFORE any op. 2. If auth fails, STOP and report the exact error. 3. Use --json/--jq to parse and confirm results."
---
# GitHub `gh` CLI

Reliable patterns for using the GitHub `gh` CLI for issue, PR, and label operations — built for automation and subagent environments where silent auth failures are common and fabricating a result is the worst outcome.

**When to Use**: Any time you create, list, view, edit, or close GitHub issues / PRs / labels through `gh`, particularly inside a sandboxed shell or a delegated subagent.

---

## The One Rule: Never Fabricate

If you cannot verify that an operation succeeded, **report the failure with the exact error**. Never invent an issue number, a URL, or a "created successfully" message. A loud, accurate failure is always better than a fake success — downstream agents and humans act on what you report.

---

## 1. Pre-flight Verification (run BEFORE any operation)

Always confirm authentication and repo access first. These are cheap, read-only, and catch the overwhelming majority of failures before you mutate anything.

```bash
# 1. Confirm you are authenticated and see which account/scopes are active
gh auth status

# 2. Confirm you can actually reach the target repo (proves token + SSO + network)
gh repo view <org>/<repo> --json name,url
```

- If `gh auth status` reports **"not logged into any GitHub hosts"** or any error, **STOP**. Do not run create/edit/close. Diagnose using the sections below, then report the exact error verbatim.
- If `gh repo view` fails (404, SAML, Bad credentials), **STOP**. The token may be valid but lack access to this org/repo. Report the exact error.
- Only proceed to mutating operations once both commands succeed.

> In a subagent: treat a failed pre-flight as a hard stop. Returning "I created issue #42" when auth failed is the failure mode this skill exists to prevent.

---

## 2. Gotcha: Sandbox / OS keychain access

`gh`'s OAuth (keyring) tokens are stored in the OS keychain (macOS Keychain, Linux Secret Service). A **sandboxed shell cannot read the keychain**, so `gh` falls back to "no credentials found" and reports **"not logged into any GitHub hosts"** — even though valid credentials exist.

**Symptom**: `gh auth status` says not logged in, but the same command works in a normal terminal.

**Fix**: Run `gh` with the sandbox disabled so it can reach the keychain.

- In Claude Code, set `dangerouslyDisableSandbox: true` on the Bash tool call that runs `gh`.
- Re-run the pre-flight (`gh auth status`) with the sandbox disabled to confirm before proceeding.

---

## 3. Gotcha: stale `GH_CONFIG_DIR`

`gh` reads its config (including which `hosts.yml` holds credentials) from `GH_CONFIG_DIR` if that env var is set, otherwise from `~/.config/gh`. A **stale or wrong `GH_CONFIG_DIR` pointing at a nonexistent directory** makes `gh` report "not logged in" even when valid keyring credentials exist elsewhere.

**Diagnose**:

```bash
echo "$GH_CONFIG_DIR"        # Is it set? To what?
ls "$GH_CONFIG_DIR"          # Does the directory exist? Has hosts.yml?
```

**Find the config dir that actually has credentials**:

```bash
find ~ -maxdepth 5 -name hosts.yml -path '*gh*'
```

**Fix** — point `GH_CONFIG_DIR` at the real config dir, or unset it to fall back to the default:

```bash
# Option A: point at the working config explicitly
GH_CONFIG_DIR=/path/to/real/gh-config gh auth status

# Option B: unset to use ~/.config/gh
unset GH_CONFIG_DIR && gh auth status
```

---

## 4. Multiple accounts

`gh auth status` may list **several accounts**, with one marked active. `gh` uses the active account. If the active one lacks access to your target org/repo, switch:

```bash
gh auth status                 # see all accounts; note which is "Active account: true"
gh auth switch -u <username>   # make the correct account active
gh repo view <org>/<repo> --json name,url   # re-verify after switching
```

---

## 5. Gotcha: Org SAML SSO rejects PATs

Personal Access Tokens pulled from `.env` files are frequently rejected by orgs that enforce SAML SSO:

```
HTTP 403: Resource protected by organization SAML enforcement.
You must grant your Personal Access token access to this organization.
```

**Why**: Even a valid PAT must be **SSO-authorized for that specific org** via a browser grant. Tokens injected from `.env` in a headless environment usually have never been through that grant.

**Preferred fix**: Use a **keyring OAuth token** (`gh auth login`) that has already been SSO-authorized for the org — OAuth logins prompt for the SSO grant interactively. To authorize an existing PAT, complete the org's SSO browser grant in GitHub settings (Developer settings → PATs → Configure SSO).

**Rule of thumb**: For SSO-enforced orgs, prefer keyring OAuth over `.env` PATs.

---

## 6. Server-side fallback for CI / bulk operations

When local auth is unavailable, unreliable, or you need robust bulk operations, run `gh` from a **server that holds a GitHub App installation token**. App installation tokens are **SSO-exempt** and scoped to the installation, making them the most reliable path for automation.

A common pattern is to dispatch the command to a server via AWS SSM:

```bash
aws ssm send-command \
  --instance-ids <instance-id> --region <region> \
  --document-name "AWS-RunShellScript" \
  --parameters '{"commands":["gh issue create --repo <org>/<repo> --title \"...\" --body \"...\""]}'
```

Treat this as the **robust path for automation / CI** when keychain-backed local auth cannot be guaranteed.

---

## 7. Common commands cheat-sheet

Use `--json <fields> --jq <filter>` to get machine-parseable output and to **confirm** results rather than trusting exit codes alone.

### Issues

```bash
# Create — capture the returned URL; do not invent it
gh issue create --repo <org>/<repo> --title "Title" --body "Body" --label bug

# List (parseable)
gh issue list --repo <org>/<repo> --state open --json number,title,url --jq '.[]'

# View a specific issue
gh issue view <number> --repo <org>/<repo> --json number,title,state,url

# Close
gh issue close <number> --repo <org>/<repo> --comment "Resolved"

# Edit (also the basis of upsert-by-title — see below)
gh issue edit <number> --repo <org>/<repo> --add-label triaged --body "Updated body"
```

### Upsert-by-title pattern (idempotent issue creation)

Avoid duplicate issues by checking for an existing open issue with the same title before creating:

```bash
existing=$(gh issue list --repo <org>/<repo> --state open \
  --search "in:title \"My exact title\"" \
  --json number,title --jq '.[] | select(.title=="My exact title") | .number' | head -n1)

if [ -n "$existing" ]; then
  gh issue edit "$existing" --repo <org>/<repo> --body "Refreshed body"
else
  gh issue create --repo <org>/<repo> --title "My exact title" --body "..."
fi
```

### Pull requests

```bash
gh pr view <number> --repo <org>/<repo> --json number,title,state,url,mergeable
gh pr list --repo <org>/<repo> --state open --json number,title,headRefName --jq '.[]'
```

### Labels

```bash
gh label create "code-intelligence" --repo <org>/<repo> --color BFD4F2 --description "..."
gh label list --repo <org>/<repo> --json name,color --jq '.[].name'
```

---

## Troubleshooting / Environment-specific notes

This section documents a concrete, worked example of the failure modes above — diagnosed while ticketing subagents could not create issues in `duettoresearch/code-intelligence`. The generic instructions above are what you apply; this is the case study showing how they combine in practice.

### Symptom

Ticketing subagents reported **"not logged into any GitHub hosts"** and **"Bad credentials"** and could not create issues in `duettoresearch/code-intelligence`. Some runs would otherwise have been tempted to report a fabricated issue URL — do not.

### Root causes found (multiple, compounding)

1. **Stale `GH_CONFIG_DIR`** — subagents inherited `GH_CONFIG_DIR=/Users/masa/.config/gh-duetto`, a directory that **does not exist**, so `gh` saw no credentials. (See §3.)
2. **Sandbox blocked keychain** — the Bash sandbox prevented reading the OS keychain, producing the false "not logged in." (See §2.)
3. **`.env.local` PAT blocked by SAML SSO** — the PAT in `.env.local` is rejected by `duettoresearch` org SAML enforcement. (See §5.)
4. **Stale keychain token** — a leftover keychain token for account `bobmatnyc` returned **HTTP 401 Bad credentials**. (See §4 — wrong active account.)

### Working configuration (verified)

```
GH_CONFIG_DIR=/Users/masa/.config/gh-personal   # real config dir with valid hosts.yml
sandbox: disabled                                # so gh can read the keychain
active account: bob-duetto                       # scopes: gist, read:org, repo, workflow
result: gh repo view duettoresearch/code-intelligence  → succeeds
```

### Canonical fix recipe

```bash
# Run gh with the real config dir AND the sandbox disabled
# (in Claude Code: dangerouslyDisableSandbox: true on the Bash call)
GH_CONFIG_DIR=/Users/masa/.config/gh-personal gh auth status

# If the wrong account is active, switch first:
GH_CONFIG_DIR=/Users/masa/.config/gh-personal gh auth switch -u bob-duetto

# Then re-verify before any mutation:
GH_CONFIG_DIR=/Users/masa/.config/gh-personal gh repo view duettoresearch/code-intelligence --json name,url
```

Only after that pre-flight succeeds should the subagent run `gh issue create` etc. — and it must report the real returned URL, never a fabricated one.

---

## Anti-Patterns

### ❌ Don't: report success without verifying
```bash
gh issue create ...   # exit code ignored
# "Created issue #42!"  ← fabricated; the command may have failed silently
```

### ✅ Do: capture and confirm the result
```bash
url=$(gh issue create --repo <org>/<repo> --title "T" --body "B")
echo "Created: $url"   # report the actual returned URL, or the actual error
```

### ❌ Don't: assume "not logged in" means no credentials
It usually means sandbox/keychain or a stale `GH_CONFIG_DIR` — diagnose first (§2, §3).

### ❌ Don't: rely on `.env` PATs for SSO-enforced orgs
Prefer keyring OAuth or a server-side App installation token (§5, §6).

---

## Summary

- **Pre-flight first**: `gh auth status` + `gh repo view` before any op.
- **Never fabricate**: report the exact error on failure; report the real URL on success.
- **Know the four failure modes**: sandbox/keychain, stale `GH_CONFIG_DIR`, multiple accounts, SAML SSO PAT rejection.
- **Automation path**: server-side GitHub App installation token (SSO-exempt) for CI/bulk.
