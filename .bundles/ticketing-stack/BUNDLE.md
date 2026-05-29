# Ticketing Stack

**Version:** 1.0.0
**Category:** Universal
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Everything the **ticketing agent** needs to reliably create, update, and verify
GitHub issues, PRs, and labels — especially from automation and subagent shells
where silent auth failures are common. The defining principle of this bundle is
**never fabricate a result**: every ticket operation is pre-flight verified and
its real outcome (URL or error) is reported.

## Included Skills

- **gh-cli** (universal/collaboration/gh-cli) - Drive the GitHub `gh` CLI for issue/PR/label ops with pre-flight auth verification; documents sandbox/keychain, `GH_CONFIG_DIR`, multi-account, and SAML SSO gotchas plus a server-side App-token fallback.
- **git-workflow** (universal/collaboration/git-workflow) - Conventional commits, branching, and PR hygiene for ticket-linked branches.
- **verification-before-completion** (universal/debugging/verification-before-completion) - Quality gate: confirm output before claiming a ticket was created/closed.

## Use Cases

**When to Deploy This Bundle:**
- Bundling with the ticketing agent so it ships with reliable `gh` usage
- Subagents that file issues/PRs in SSO-enforced orgs
- CI/automation that creates tickets and must not fabricate URLs
- Any workflow that links commits/PRs to issues

**What You Get:**
- Pre-flight auth verification (`gh auth status` + `gh repo view`) before any mutation
- Diagnosis recipes for the four common `gh` auth failure modes
- Server-side GitHub App installation-token fallback for SSO-exempt automation
- Upsert-by-title pattern for idempotent issue creation
- A verification gate so no ticket is reported done without proof

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate

# Alternative: Hierarchical (preserves paths)
./deploy.sh --hierarchical ~/.claude/
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| gh-cli | ✅ Yes | 🚀 Enhanced | None |
| git-workflow | ✅ Yes | 🚀 Enhanced | None |
| verification-before-completion | ✅ Yes | 🚀 Enhanced | None (methodology) |

**Bundle Synergies:**
- gh-cli + verification-before-completion: pre-flight + post-op confirmation means a ticket is only "done" when the returned URL is verified.
- gh-cli + git-workflow: link branches/PRs to issues using conventional commits.

## Integration Example

```bash
# 1. Pre-flight (gh-cli): never operate on unverified auth
gh auth status
gh repo view <org>/<repo> --json name,url   # STOP on failure, report exact error

# 2. Create the ticket and capture the REAL url (gh-cli: never fabricate)
url=$(gh issue create --repo <org>/<repo> --title "Fix flaky test" --body "...")

# 3. Verify before reporting done (verification-before-completion)
gh issue view "${url##*/}" --repo <org>/<repo> --json number,state,url

# 4. Link the fix branch (git-workflow)
git checkout -b fix/flaky-test && git commit -m "fix: stabilize flaky test (#${url##*/})"
```

## Version History

- **1.0.0** (2026-05-29): Initial release with gh-cli, git-workflow, and verification-before-completion.

## Related Bundles

- **universal-development**: Broader development practices (TDD, debugging, verification).
