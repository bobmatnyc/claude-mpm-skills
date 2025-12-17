# Modules and Composition

## Module Design Principles

- Keep module interfaces small and stable (inputs/outputs).
- Avoid over-abstraction; start with a root module, extract modules when duplication appears.
- Version modules and pin versions in consumers.

Recommended structure:
- Root module per environment (or per stack)
- Reusable modules for common building blocks (network, compute, database)

## Inputs and Outputs

Patterns:
- Use typed variables with validation
- Expose only what downstream consumers need

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment (dev/staging/prod)"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod"
  }
}
```

## Iteration and Addressing

Prefer `for_each` over `count` when stable addressing matters:
- `for_each` uses keys (more stable across inserts)
- `count` shifts indexes when items are inserted/deleted

## Safe Refactors

When renaming resources or moving them into modules:
- Use `moved` blocks (Terraform 1.1+) where possible
- Or use `terraform state mv` with care and review

## Testing

Practical baseline:
- `terraform fmt`, `validate`, and `plan` in CI on every PR
- Add policy checks (security/cost) for production stacks

Optional:
- Terratest (Go) for integration tests
- `terraform test` (if standardised in the repo and tooling)

