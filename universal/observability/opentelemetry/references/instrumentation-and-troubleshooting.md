# Instrumentation Patterns and Troubleshooting

## Start Strategy

1) Enable auto-instrumentation for HTTP server/client and common libraries.
2) Add manual spans around business operations (checkout, sync, provision).
3) Add metrics for SLOs (latency histograms, error rate counters).
4) Correlate logs with trace context.

## Manual Span Pattern

Prefer naming spans by operation, not by URL or dynamic IDs:
- Good: `db.query.users_by_email`, `payment.charge`, `cache.get`
- Avoid: `GET /users/123` (high cardinality)

Attach attributes:
- route templates, not raw paths
- stable identifiers (tenant tier, feature flag name), not user IDs

## Log Correlation

Emit structured fields in logs:
- `trace_id`
- `span_id`
- `service.name`
- `deployment.environment`

Avoid copying full baggage into logs.

## Troubleshooting Checklist

### No telemetry arrives

- Verify exporter endpoint and protocol (OTLP gRPC vs HTTP)
- Confirm the Collector receiver is enabled and reachable
- Validate TLS settings and auth requirements

### Spans exist but traces look broken

- Propagation missing (headers stripped, message metadata lost)
- Background work detached from parent context
- Async context lost across task boundaries

### High CPU/memory or backend cost

- High-cardinality metric labels
- Too many span attributes/events
- Sampling too permissive

Fixes:
- Move detail from attributes to logs/events
- Apply sampling and filtering at the Collector
- Add batch processing

### Incorrect service grouping

If services appear merged or fragmented:
- Standardize `service.name` and `service.version`
- Avoid environment suffixes in `service.name` (use `deployment.environment` instead)

