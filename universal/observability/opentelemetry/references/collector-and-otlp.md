# Collector and OTLP

## Why Use the Collector

The Collector provides:
- A stable OTLP endpoint for all services
- Vendor-neutral export (swap backends without app changes)
- Centralized processing (batching, filtering, sampling, redaction)

## Minimal Collector Config (Example)

```yaml
receivers:
  otlp:
    protocols:
      grpc: {}
      http: {}

processors:
  batch: {}

exporters:
  otlphttp:
    endpoint: https://telemetry-backend.example/v1/otlp

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp]
```

## Deployment Patterns

- **Agent/DaemonSet**: per-node collection (common in Kubernetes).
- **Gateway**: centralized Collector (good for tail sampling and heavy processing).
- **Sidecar**: per-pod Collector (less common; increases resource usage).

## Tail Sampling (High-Value Traces)

Tail sampling keeps important traces while dropping noise:
- Sample errors at 100%
- Sample slow traces above a latency threshold
- Sample a small percentage of normal traffic

Use a gateway Collector for tail sampling to ensure full trace visibility.

## Security and Reliability

Checklist:
- TLS for OTLP endpoints
- Auth at the Collector ingress (mTLS, token, or network isolation)
- Memory limits and backpressure (batch + memory limiter)
- Redact sensitive attributes at the Collector

