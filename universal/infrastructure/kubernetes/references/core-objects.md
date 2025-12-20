# Kubernetes Core Objects (Cheat Sheet)

## Mental Model

- Control plane stores desired state; controllers reconcile actual state toward it.
- Pods are ephemeral; prefer controllers (Deployment/StatefulSet/DaemonSet/Job).
- Selectors bind things together (Service → Pods, Deployment → ReplicaSet → Pods).

## Workload Controllers

| Controller | Use When | Notes |
| --- | --- | --- |
| Deployment | Stateless services | Rolling updates, easy rollback |
| StatefulSet | Stateful workloads | Stable identity + per-replica PVCs |
| DaemonSet | One Pod per node | Agents, log collectors, CNI addons |
| Job / CronJob | Batch and scheduled work | Retries, backoff, completions |

## Networking

**Service types**
- `ClusterIP`: internal service discovery (default)
- `NodePort`: exposes a port on every node (often avoided in production)
- `LoadBalancer`: cloud LB integration (when available)
- Ingress: HTTP routing (path/host TLS termination) to Services

**Selector sanity check**

```bash
kubectl get svc/<svc> -n <ns>
kubectl get endpoints/<svc> -n <ns> -o wide
kubectl get pods -n <ns> -l app=<label>
```

If `endpoints` is empty, check:
- Service selector matches Pod labels
- Pods pass readiness checks (not ready ⇒ not in endpoints)

## Configuration

- `ConfigMap`: non-secret configuration (mounted files or env vars)
- `Secret`: sensitive configuration (protect etcd + RBAC; treat cluster access as secret access)

Prefer mounted files for large configs; prefer env vars for small values.

## Scheduling and Scaling

- **Resources**: set `requests` and `limits` for CPU/memory
- **Placement**: `nodeSelector`, `affinity`, `taints/tolerations`
- **Autoscaling**: HPA based on CPU/memory/custom metrics (avoid scaling on high-cardinality metrics)

## Minimal Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: example/app:1.2.3
          ports:
            - containerPort: 8080
```

## Labels (Recommended)

Use the standard label keys to keep tooling compatible:
- `app.kubernetes.io/name`
- `app.kubernetes.io/instance`
- `app.kubernetes.io/version`
- `app.kubernetes.io/component`
- `app.kubernetes.io/part-of`
- `app.kubernetes.io/managed-by`

