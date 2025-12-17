# State and Environments

## State Safety Rules

- Use a remote backend with locking for any shared environment.
- Treat state as sensitive; it often contains resource attributes and secrets.
- Separate state for production vs non-production to limit blast radius.

## Backends and Locking

Patterns:
- Remote object store backend + lock table (common)
- Managed backend with built-in locking and history (common)

Checklist:
- Enable encryption at rest
- Restrict IAM access to the backend (read/write only for CI and break-glass operators)
- Enable versioning for state history

## Environments: Workspaces vs Separate State

Prefer **separate state** per environment for most teams:
- Clear separation of prod vs staging
- Independent locking, permissions, and retention
- Fewer workspace foot-guns

Use workspaces when:
- A single root module is intentionally shared
- Workspace isolation is well understood and enforced in tooling

## Drift, Imports, and State Ops

Drift:
- Run `plan` regularly in CI to detect drift (or scheduled checks).

Imports:
- Use `terraform import` for adopting existing resources.
- Follow with a `plan` to confirm parity.

State commands (use carefully):

```bash
terraform state list
terraform state show <addr>
terraform state mv <from> <to>
terraform state rm <addr>
```

Avoid manual edits of the state file.

## Secrets

If a provider returns a secret value, it can land in state.

Patterns:
- Use secret managers for secret generation and distribution
- Prefer references (ARN/ID/path) over raw secret values
- Restrict state access and audit reads

