# Kubernetes Security Hardening

## Pod Security (Baseline)

Prefer restrictive defaults:
- Run as non-root
- Drop Linux capabilities
- Use a read-only root filesystem where possible
- Set a seccomp profile

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
  seccompProfile:
    type: RuntimeDefault
```

## RBAC (Least Privilege)

Checklist:
- Grant namespace-scoped roles where possible.
- Avoid `cluster-admin` and broad wildcard rules.
- Separate “read” roles from “write” roles.

## Network Policy (Default Deny)

If the CNI supports NetworkPolicy, adopt a default-deny stance and allow only required traffic between namespaces and workloads.

Key patterns:
- Allow ingress only from the ingress controller namespace.
- Allow egress only to required dependencies (DB/cache) and DNS.

## Secrets Handling

Assume the cluster can read Secrets; treat cluster access as secret access.

Checklist:
- Restrict Secrets with RBAC and namespace boundaries
- Prefer external secret managers (external-secrets, CSI drivers) for high-value secrets
- Avoid logging environment values and full config dumps

## Supply Chain

Checklist:
- Pin images by digest for critical workloads (`image@sha256:...`)
- Scan images in CI and block known critical CVEs
- Use minimal base images and drop unused packages

