---
name: datadog-observability
description: Full-stack observability with Datadog APM, logs, metrics, synthetics, and RUM. Use when implementing monitoring, tracing, alerting, or cost optimization for production systems.
version: 1.0.0
category: platform
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Unified observability platform for APM, logs, metrics, synthetics, and RUM with 1000+ integrations."
    when_to_use: "When implementing production monitoring, distributed tracing, log aggregation, custom metrics, or cost optimization."
    quick_start: "1. Install Datadog Agent. 2. Enable APM with automatic instrumentation. 3. Configure log collection. 4. Set up alerts."
  references:
    - agent-installation.md
    - apm-instrumentation.md
    - log-management.md
    - custom-metrics.md
    - alerting.md
    - cost-optimization.md
    - kubernetes.md
context_limit: 800
tags:
  - observability
  - monitoring
  - apm
  - logging
  - metrics
  - tracing
  - datadog
  - alerting
requires_tools: []
---

# Datadog Observability

## Overview

Datadog is a SaaS observability platform providing unified monitoring across infrastructure, applications, logs, and user experience. It offers AI-powered anomaly detection, 1000+ integrations, and OpenTelemetry compatibility.

**Core Capabilities:**
- **APM**: Distributed tracing with automatic instrumentation for 8+ languages
- **Infrastructure**: Host, container, and cloud service monitoring
- **Logs**: Centralized collection with processing pipelines and 15-month retention
- **Metrics**: Custom metrics via DogStatsD with cardinality management
- **Synthetics**: Proactive API and browser testing from 29+ global locations
- **RUM**: Frontend performance with Core Web Vitals and session replay

## When to Use This Skill

**Activate when:**
- Setting up production monitoring and observability
- Implementing distributed tracing across microservices
- Configuring log aggregation and analysis pipelines
- Creating custom metrics and dashboards
- Setting up alerting and anomaly detection
- Optimizing Datadog costs

**Do not use when:**
- Building with open-source stack (use Prometheus/Grafana instead)
- Cost is primary concern and budget is limited
- Need maximum customization over managed solution

## Quick Start

### 1. Install Datadog Agent

**Docker (simplest):**
```bash
docker run -d --name dd-agent \
  -e DD_API_KEY=<YOUR_API_KEY> \
  -e DD_SITE="datadoghq.com" \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  gcr.io/datadoghq/agent:7
```

**Kubernetes (Helm):**
```bash
helm repo add datadog https://helm.datadoghq.com
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=<YOUR_API_KEY> \
  --set datadog.apm.enabled=true \
  --set datadog.logs.enabled=true
```

### 2. Instrument Your Application

**Python:**
```python
from ddtrace import tracer, patch_all

# Automatic instrumentation for common libraries
patch_all()

# Manual span for custom operations
with tracer.trace("custom.operation", service="my-service") as span:
    span.set_tag("user.id", user_id)
    # your code here
```

**Node.js:**
```javascript
// Must be first import
const tracer = require('dd-trace').init({
  service: 'my-service',
  env: 'production',
  version: '1.0.0',
});
```

### 3. Verify in Datadog UI

1. Go to Infrastructure > Host Map to verify agent
2. Go to APM > Services to see traced services
3. Go to Logs > Search to verify log collection

## Core Concepts

### Tagging Strategy

Tags enable filtering, aggregation, and cost attribution. Use consistent tags across all telemetry.

**Required Tags:**
| Tag | Purpose | Example |
|-----|---------|---------|
| `env` | Environment | `env:production` |
| `service` | Service name | `service:api-gateway` |
| `version` | Deployment version | `version:1.2.3` |
| `team` | Owning team | `team:platform` |

**Avoid High-Cardinality Tags:**
- User IDs, request IDs, timestamps
- Pod IDs in Kubernetes
- Build numbers, commit hashes

### Unified Observability

Datadog correlates metrics, traces, and logs automatically:
- Traces include span tags that link to metrics
- Logs inject trace IDs for correlation
- Dashboards combine all data sources

## Best Practices

### Start Simple
1. Install Agent with basic configuration
2. Enable automatic instrumentation
3. Verify data in Datadog UI
4. Add custom spans/metrics as needed

### Progressive Enhancement
```
Basic → APM tracing → Custom spans → Custom metrics → Profiling → RUM
```

### Key Instrumentation Points
- HTTP entry/exit points
- Database queries
- External service calls
- Message queue operations
- Business-critical flows

## Common Mistakes

1. **High-cardinality tags**: Using user IDs or request IDs as tags creates millions of unique metrics
2. **Missing log index quotas**: Leads to unexpected bills from log volume spikes
3. **Over-alerting**: Creates alert fatigue; alert on symptoms, not causes
4. **Missing service tags**: Prevents correlation between metrics, traces, and logs
5. **No sampling for high-volume traces**: Ingests everything, causing cost explosion

## Navigation

For detailed implementation:

- **[Agent Installation](references/agent-installation.md)**: Docker, Kubernetes, Linux, Windows, and cloud-specific setup
- **[APM Instrumentation](references/apm-instrumentation.md)**: Python, Node.js, Go, Java instrumentation with code examples
- **[Log Management](references/log-management.md)**: Pipelines, Grok parsing, standard attributes, archives
- **[Custom Metrics](references/custom-metrics.md)**: DogStatsD patterns, metric types, tagging best practices
- **[Alerting](references/alerting.md)**: Monitor types, anomaly detection, alert hygiene
- **[Cost Optimization](references/cost-optimization.md)**: Metrics without Limits, sampling, index quotas
- **[Kubernetes](references/kubernetes.md)**: DaemonSet, Cluster Agent, autodiscovery

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **docker**: Container instrumentation patterns
- **kubernetes**: K8s-native monitoring patterns
- **python/nodejs/go**: Language-specific APM setup

## Resources

**Official Documentation:**
- APM: https://docs.datadoghq.com/tracing/
- Logs: https://docs.datadoghq.com/logs/
- Metrics: https://docs.datadoghq.com/metrics/
- DogStatsD: https://docs.datadoghq.com/developers/dogstatsd/

**Cost Management:**
- Billing: https://docs.datadoghq.com/account_management/billing/
- Usage Attribution: https://docs.datadoghq.com/account_management/billing/usage_attribution/
