# Rollouts, Probes, and Graceful Shutdown

## Health Probes

**Readiness**
- Gate traffic.
- Fail readiness when dependencies are unavailable (DB down, migrations running) if serving requests would fail.

**Liveness**
- Restart stuck/crashed processes.
- Avoid liveness probes that depend on external services; prefer process health only.

**Startup**
- Prevent liveness/readiness from failing during slow boot.

### Minimal Probe Example

```yaml
containers:
  - name: app
    image: example/app:1.2.3
    ports:
      - containerPort: 8080
    startupProbe:
      httpGet: { path: /healthz, port: 8080 }
      failureThreshold: 30
      periodSeconds: 2
    readinessProbe:
      httpGet: { path: /readyz, port: 8080 }
      periodSeconds: 5
      timeoutSeconds: 2
    livenessProbe:
      httpGet: { path: /healthz, port: 8080 }
      periodSeconds: 10
      timeoutSeconds: 2
```

## Rolling Updates

Prefer `RollingUpdate` for stateless services.

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```

### Rollout Commands

```bash
kubectl rollout status deploy/<name> -n <ns>
kubectl rollout history deploy/<name> -n <ns>
kubectl rollout undo deploy/<name> -n <ns>
```

## Graceful Shutdown

Kubernetes sends `SIGTERM` and waits `terminationGracePeriodSeconds`.

Checklist:
- Handle `SIGTERM` in the app (stop accepting new work, drain connections, flush buffers).
- Keep readiness failing during shutdown so traffic drains.
- Use `preStop` only when an explicit delay is required (prefer app-level drains).

```yaml
terminationGracePeriodSeconds: 30
containers:
  - name: app
    lifecycle:
      preStop:
        exec:
          command: ["sh", "-c", "sleep 5"]
```

## Disruption and Availability

Use a Pod Disruption Budget (PDB) to keep at least N replicas available during voluntary disruptions:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: app
```

