# Kubernetes Monitoring

Datadog provides comprehensive Kubernetes monitoring through the DaemonSet Agent and Cluster Agent.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Kubernetes Cluster                       │
│                                                              │
│  ┌──────────────┐     ┌──────────────────────────────────┐  │
│  │ Cluster Agent│────▶│ Kubernetes API Server            │  │
│  │  (Deployment)│     │ - Cluster-level metrics          │  │
│  └──────────────┘     │ - Events, HPA metrics            │  │
│         │             └──────────────────────────────────┘  │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Node Agent  │  │  Node Agent  │  │  Node Agent  │      │
│  │  (DaemonSet) │  │  (DaemonSet) │  │  (DaemonSet) │      │
│  │              │  │              │  │              │      │
│  │ - Pod metrics│  │ - Pod metrics│  │ - Pod metrics│      │
│  │ - Container  │  │ - Container  │  │ - Container  │      │
│  │ - Logs       │  │ - Logs       │  │ - Logs       │      │
│  │ - Traces     │  │ - Traces     │  │ - Traces     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │   Datadog    │
                       │   Backend    │
                       └──────────────┘
```

## DaemonSet Deployment

### Helm Installation

**Add Datadog Helm repository:**
```bash
helm repo add datadog https://helm.datadoghq.com
helm repo update
```

**Create values file:**
```yaml
# datadog-values.yaml
datadog:
  apiKey: <YOUR_API_KEY>
  appKey: <YOUR_APP_KEY>  # Optional, for Cluster Agent
  site: datadoghq.com

  # Cluster name for grouping
  clusterName: my-production-cluster

  # Global tags
  tags:
    - env:production
    - team:platform

  # Collect Kubernetes events
  collectEvents: true

  # Leader election for cluster-level checks
  leaderElection: true

  # APM configuration
  apm:
    portEnabled: true
    socketEnabled: true

  # Log collection
  logs:
    enabled: true
    containerCollectAll: true

  # Process monitoring
  processAgent:
    enabled: true
    processCollection: true

  # Network Performance Monitoring
  networkMonitoring:
    enabled: true

  # Orchestrator Explorer
  orchestratorExplorer:
    enabled: true

# Cluster Agent
clusterAgent:
  enabled: true
  replicas: 2

  # HPA metrics
  metricsProvider:
    enabled: true
    useDatadogMetrics: true

  # Admission Controller for auto-instrumentation
  admissionController:
    enabled: true
    mutateUnlabelled: false

# Node Agent resources
agents:
  image:
    repository: gcr.io/datadoghq/agent
    tag: 7

  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 200m
      memory: 256Mi

  # Tolerations for running on all nodes
  tolerations:
    - operator: Exists
```

**Install:**
```bash
helm install datadog-agent datadog/datadog -f datadog-values.yaml -n datadog --create-namespace
```

### Verify Installation

```bash
# Check DaemonSet
kubectl get daemonset -n datadog
kubectl get pods -n datadog -l app=datadog

# Check Cluster Agent
kubectl get deployment -n datadog datadog-cluster-agent
kubectl get pods -n datadog -l app=datadog-cluster-agent

# Check agent status
kubectl exec -it $(kubectl get pods -n datadog -l app=datadog -o jsonpath='{.items[0].metadata.name}') -n datadog -- agent status
```

## Cluster Agent Setup

The Cluster Agent provides:
- Cluster-level metrics collection
- HPA custom metrics
- Kubernetes events
- Reduced API server load

### Configuration

```yaml
clusterAgent:
  enabled: true
  replicas: 2  # HA for production

  # Token for agent-cluster communication
  token: ""  # Auto-generated if empty

  # RBAC
  rbac:
    create: true
    serviceAccountName: datadog-cluster-agent

  # Metrics provider for HPA
  metricsProvider:
    enabled: true
    useDatadogMetrics: true
    wpaController: true  # Watermark Pod Autoscaler

  # Admission Controller
  admissionController:
    enabled: true
    mutateUnlabelled: false  # Only annotated pods

  resources:
    requests:
      cpu: 200m
      memory: 256Mi
```

### Custom Metrics HPA

Use Datadog metrics for Horizontal Pod Autoscaler:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: External
      external:
        metric:
          name: datadogmetric@my-namespace:my-app-requests-per-second
          selector:
            matchLabels:
              service: my-app
        target:
          type: AverageValue
          averageValue: 100
```

**Create DatadogMetric resource:**
```yaml
apiVersion: datadoghq.com/v1alpha1
kind: DatadogMetric
metadata:
  name: my-app-requests-per-second
  namespace: my-namespace
spec:
  query: sum:http.requests{service:my-app}.rollup(avg, 60)
```

## Autodiscovery Annotations

Autodiscovery configures integrations using pod annotations.

### Basic Pattern

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  annotations:
    # Log collection
    ad.datadoghq.com/my-container.logs: '[{"source": "python", "service": "my-app"}]'

    # Check integration
    ad.datadoghq.com/my-container.checks: |
      {
        "http_check": {
          "instances": [{"url": "http://%%host%%:%%port%%/health"}]
        }
      }

    # Custom tags
    ad.datadoghq.com/tags: '{"team": "platform", "version": "1.2.3"}'
spec:
  containers:
    - name: my-container
      image: my-app:latest
```

### Log Collection

```yaml
annotations:
  # Basic log collection
  ad.datadoghq.com/my-container.logs: '[{"source": "python", "service": "my-app"}]'

  # With processing rules
  ad.datadoghq.com/my-container.logs: |
    [{
      "source": "python",
      "service": "my-app",
      "log_processing_rules": [{
        "type": "exclude_at_match",
        "name": "exclude_healthchecks",
        "pattern": "GET /health"
      }]
    }]

  # Multi-container pod
  ad.datadoghq.com/app.logs: '[{"source": "python", "service": "my-app"}]'
  ad.datadoghq.com/sidecar.logs: '[{"source": "nginx", "service": "my-app-proxy"}]'
```

### APM Trace Collection

```yaml
annotations:
  # Enable APM for container
  ad.datadoghq.com/my-container.tags: '{"service": "my-app", "env": "production"}'
```

### Integration Checks

```yaml
annotations:
  # Redis check
  ad.datadoghq.com/redis.checks: |
    {
      "redisdb": {
        "instances": [{
          "host": "%%host%%",
          "port": "%%port%%",
          "password": "%%env_REDIS_PASSWORD%%"
        }]
      }
    }

  # PostgreSQL check
  ad.datadoghq.com/postgres.checks: |
    {
      "postgres": {
        "instances": [{
          "host": "%%host%%",
          "port": "5432",
          "username": "datadog",
          "password": "%%env_PG_PASSWORD%%",
          "dbname": "mydb"
        }]
      }
    }
```

### Template Variables

| Variable | Description |
|----------|-------------|
| `%%host%%` | Container IP |
| `%%port%%` | First exposed port |
| `%%port_<name>%%` | Named port |
| `%%env_<VAR>%%` | Environment variable |
| `%%hostname%%` | Container hostname |
| `%%pid%%` | Container PID |

## Container Tagging

### Automatic Tags

Datadog automatically adds:
- `kube_namespace`
- `kube_deployment`
- `kube_daemon_set`
- `kube_replica_set`
- `kube_stateful_set`
- `kube_job`
- `kube_cronjob`
- `pod_name`
- `container_name`
- `container_id`
- `image_name`
- `image_tag`

### Label-Based Tags

Extract tags from Kubernetes labels:

```yaml
# datadog-values.yaml
datadog:
  # Convert labels to tags
  podLabelsAsTags:
    app.kubernetes.io/name: kube_app_name
    app.kubernetes.io/version: kube_app_version
    app.kubernetes.io/component: kube_app_component

  # Convert annotations to tags
  podAnnotationsAsTags:
    custom.company.com/team: team
```

### Unified Service Tagging

Use standard labels for automatic service tagging:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    tags.datadoghq.com/env: production
    tags.datadoghq.com/service: my-app
    tags.datadoghq.com/version: "1.2.3"
spec:
  template:
    metadata:
      labels:
        tags.datadoghq.com/env: production
        tags.datadoghq.com/service: my-app
        tags.datadoghq.com/version: "1.2.3"
    spec:
      containers:
        - name: my-app
          env:
            - name: DD_ENV
              valueFrom:
                fieldRef:
                  fieldPath: metadata.labels['tags.datadoghq.com/env']
            - name: DD_SERVICE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.labels['tags.datadoghq.com/service']
            - name: DD_VERSION
              valueFrom:
                fieldRef:
                  fieldPath: metadata.labels['tags.datadoghq.com/version']
```

## Pod-Level Metrics

### Key Metrics

| Metric | Description |
|--------|-------------|
| `kubernetes.cpu.usage.total` | CPU usage (cores) |
| `kubernetes.cpu.requests` | CPU requests |
| `kubernetes.cpu.limits` | CPU limits |
| `kubernetes.memory.usage` | Memory usage (bytes) |
| `kubernetes.memory.requests` | Memory requests |
| `kubernetes.memory.limits` | Memory limits |
| `kubernetes.network.rx_bytes` | Network bytes received |
| `kubernetes.network.tx_bytes` | Network bytes sent |
| `kubernetes.containers.restarts` | Container restart count |

### Resource Utilization Queries

```
# CPU utilization (actual vs request)
kubernetes.cpu.usage.total{kube_deployment:my-app} / kubernetes.cpu.requests{kube_deployment:my-app} * 100

# Memory utilization (actual vs limit)
kubernetes.memory.usage{kube_deployment:my-app} / kubernetes.memory.limits{kube_deployment:my-app} * 100

# Pod restart rate
sum:kubernetes.containers.restarts{kube_namespace:production}.as_rate()
```

## Helm Chart Configuration Reference

### Complete Production Values

```yaml
# datadog-values.yaml - Production configuration
datadog:
  apiKey: <YOUR_API_KEY>
  appKey: <YOUR_APP_KEY>
  site: datadoghq.com
  clusterName: production-cluster

  tags:
    - env:production
    - team:platform

  # Features
  collectEvents: true
  leaderElection: true
  criSocketPath: /var/run/containerd/containerd.sock

  # APM
  apm:
    portEnabled: true
    socketEnabled: true
    socketPath: /var/run/datadog/apm.socket

  # Logs
  logs:
    enabled: true
    containerCollectAll: true

  # Process Agent
  processAgent:
    enabled: true
    processCollection: true

  # NPM
  networkMonitoring:
    enabled: true

  # Orchestrator Explorer
  orchestratorExplorer:
    enabled: true

  # Security
  securityAgent:
    compliance:
      enabled: false
    runtime:
      enabled: false

  # Label/annotation to tag mapping
  podLabelsAsTags:
    app.kubernetes.io/name: kube_app_name
    app.kubernetes.io/version: kube_app_version

# Cluster Agent
clusterAgent:
  enabled: true
  replicas: 2
  createPodDisruptionBudget: true

  metricsProvider:
    enabled: true
    useDatadogMetrics: true

  admissionController:
    enabled: true
    mutateUnlabelled: false

  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 200m
      memory: 256Mi

# Node Agent
agents:
  image:
    repository: gcr.io/datadoghq/agent
    tag: 7

  rbac:
    create: true

  tolerations:
    - operator: Exists

  podSecurity:
    seccompProfiles:
      - runtime/default

  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 200m
      memory: 256Mi

  # Volume mounts for logs
  volumes:
    - name: varlog
      hostPath:
        path: /var/log
    - name: containerlog
      hostPath:
        path: /var/lib/docker/containers

  volumeMounts:
    - name: varlog
      mountPath: /var/log
      readOnly: true
    - name: containerlog
      mountPath: /var/lib/docker/containers
      readOnly: true

# Kube State Metrics (if not already installed)
providers:
  kubeStateMetrics:
    enabled: true
```

## Troubleshooting

### Common Issues

**Agent not collecting pod metrics:**
```bash
# Check kubelet connectivity
kubectl exec -it <agent-pod> -n datadog -- agent check kubelet
```

**Missing container logs:**
```bash
# Verify log paths
kubectl exec -it <agent-pod> -n datadog -- ls /var/log/containers/

# Check agent log collection status
kubectl exec -it <agent-pod> -n datadog -- agent status | grep -A 20 "Logs Agent"
```

**Cluster Agent not syncing:**
```bash
# Check cluster agent logs
kubectl logs -n datadog -l app=datadog-cluster-agent

# Verify RBAC permissions
kubectl auth can-i list pods --as=system:serviceaccount:datadog:datadog-cluster-agent
```

### Diagnostic Commands

```bash
# Full agent status
kubectl exec -it <agent-pod> -n datadog -- agent status

# Check specific integration
kubectl exec -it <agent-pod> -n datadog -- agent check kubernetes

# Agent configuration
kubectl exec -it <agent-pod> -n datadog -- agent configcheck

# Cluster Agent status
kubectl exec -it <cluster-agent-pod> -n datadog -- datadog-cluster-agent status
```
