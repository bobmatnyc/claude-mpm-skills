# Concepts: Traces, Metrics, Logs

## Signals

- **Traces**: end-to-end request flow across services, represented as spans.
- **Metrics**: numeric time series (counters, gauges, histograms).
- **Logs**: discrete events; correlate with traces via `trace_id` and `span_id`.

## Tracing Terms

- **Trace**: tree of spans for a single request/operation.
- **Span**: timed operation with attributes and events.
- **Span kind**: server/client/producer/consumer/internal (helps topology and analysis).
- **Attributes**: key/value metadata for filtering and grouping.
- **Events**: timestamped annotations on a span.

Prefer:
- Low-cardinality attributes (status codes, route names)
- High-detail information as span events or structured logs

## Context Propagation

Distributed tracing relies on propagation of context across process boundaries:
- HTTP headers (W3C Trace Context)
- Messaging metadata (producer → consumer)

Propagation breaks when:
- Requests are queued without copying context
- Background tasks start without parent context
- Async boundaries drop context

## Resources vs Span Attributes

**Resource attributes** describe the emitter:
- `service.name`
- `service.version`
- `deployment.environment`
- `cloud.region` (if applicable)

**Span attributes** describe the operation:
- HTTP: route, method, status code
- DB: system, statement name (avoid raw queries), duration

## Sampling

Sampling controls cost and overhead:
- **Head sampling**: decide at trace start (simple, may miss rare errors)
- **Tail sampling**: decide after seeing span data (requires Collector, better for “keep errors”)

Common patterns:
- Parent-based sampling (respect upstream decision)
- Always sample error traces (tail sampling policy)

## Cardinality (Common Pitfall)

Avoid high-cardinality labels/attributes in metrics (user IDs, request IDs).
For traces, high-cardinality attributes are less harmful but still increase storage/search costs.

