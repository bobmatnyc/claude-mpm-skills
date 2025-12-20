# Kubernetes Debugging Runbook

## Triage Flow (Fast)

1) Identify what is failing (Pod, Service routing, Ingress, dependency, node capacity).
2) Inspect events and current state before changing manifests.
3) Verify labels/selectors and readiness gating.

### Snapshot the state

```bash
kubectl get deploy,rs,po,svc,ing -n <ns> -o wide
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -n 50
```

### Drill into a single Pod

```bash
kubectl describe pod/<pod> -n <ns>
kubectl logs pod/<pod> -n <ns> --tail=200
kubectl logs pod/<pod> -n <ns> --previous --tail=200
kubectl exec -it pod/<pod> -n <ns> -- sh
```

## Common Failure Modes

### Pending

Signals:
- `kubectl describe pod` shows scheduling errors.

Likely causes:
- Insufficient CPU/memory on nodes
- Node selectors/affinity too strict
- Missing tolerations for taints
- PVC not bound

Next actions:
- Inspect `Events:` in `describe`
- Check cluster capacity: `kubectl top nodes` (if metrics-server exists)
- Validate PVC: `kubectl get pvc -n <ns>`

### ImagePullBackOff / ErrImagePull

Likely causes:
- Wrong image name/tag
- Registry auth missing (`imagePullSecrets`)
- Rate limits or network egress blocked

Next actions:
- Check events for registry error details
- Confirm pull secret exists and is referenced in the Pod spec

### CrashLoopBackOff

Likely causes:
- App exits on startup (config/secrets/migrations)
- Liveness probe too aggressive
- OOM kills or file permission issues

Next actions:
- Read `--previous` logs first
- Check container exit code and `Reason:` in `describe`
- Look for `OOMKilled` and memory limits

### Service returns 503/504

Likely causes:
- No ready endpoints (readiness failing)
- Service selector mismatch
- Ingress routes to wrong Service/port

Next actions:
- Verify endpoints:

```bash
kubectl get endpoints/<svc> -n <ns> -o wide
kubectl get pods -n <ns> -l app=<label> -o wide
```

### Ingress not routing

Likely causes:
- Ingress controller missing or misconfigured
- TLS secret missing/invalid
- Path/host rules mismatch

Next actions:
- Inspect Ingress events and controller logs
- Validate DNS/host rule and backend Service port mapping

## Debugging Without Changing the Image

If the image lacks tooling, use ephemeral containers (requires cluster support):

```bash
kubectl debug -it pod/<pod> -n <ns> --image=busybox:1.36 --target=<container-name>
```

Use this for DNS checks, curl, and filesystem inspection without rebuilding.

