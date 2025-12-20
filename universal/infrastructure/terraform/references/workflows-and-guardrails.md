# Workflows and Guardrails

## Standard Workflow

1) Format + validate (`fmt`, `validate`)
2) Plan in CI and publish the plan output
3) Review the plan (including diffs to sensitive resources)
4) Apply from a trusted runner after approval

Avoid ad-hoc local applies for shared environments.

## Guardrails in Code

Lifecycle protections:

```hcl
lifecycle {
  prevent_destroy = true
  create_before_destroy = true
}
```

Change management:
- Require explicit approvals for production applies
- Require plan-only for PRs and apply-only for protected branches

## Policy and Security Checks

Common additions:
- `tflint` (linting)
- `trivy config`, `tfsec`, or `checkov` (IaC security)
- Conftest/OPA or Sentinel for policy-as-code
- Cost estimation gates (where applicable)

## Migrations and Renames

Safer patterns:
- Use `moved` blocks for refactors
- Apply in small steps
- Avoid `-target` except for recovery and controlled migrations

## Disaster Recovery

Checklist:
- Versioned remote state
- Backend access logs enabled
- Document break-glass procedure for state recovery and unlocks

