# APM Instrumentation

Datadog APM provides distributed tracing with automatic instrumentation for 8+ languages and 176+ integrations.

## Python Instrumentation

### Automatic Instrumentation

**Installation:**
```bash
pip install ddtrace
```

**Option 1: ddtrace-run (Recommended)**
```bash
# Automatically patches all supported libraries
DD_SERVICE=my-service \
DD_ENV=production \
DD_VERSION=1.0.0 \
ddtrace-run python app.py
```

**Option 2: Programmatic patching**
```python
from ddtrace import tracer, patch_all

# Patch all supported libraries
patch_all()

# Or selective patching
from ddtrace import patch
patch(requests=True, flask=True, sqlalchemy=True, redis=True)
```

### Manual Instrumentation

```python
from ddtrace import tracer

# Basic span
with tracer.trace("custom.operation", service="my-service") as span:
    span.set_tag("user.id", user_id)
    span.set_tag("order.total", order_total)
    result = perform_operation()
    span.set_tag("result.status", result.status)

# Decorator
@tracer.wrap(service="my-service", resource="process_order")
def process_order(order_id):
    # Automatically traced
    pass

# Async support
async def async_operation():
    with tracer.trace("async.operation"):
        await some_async_call()
```

### Flask Example

```python
from flask import Flask
from ddtrace import tracer, patch_all

patch_all()

app = Flask(__name__)

@app.route('/api/users/<user_id>')
def get_user(user_id):
    # Automatically traced
    with tracer.trace("db.query", service="postgres") as span:
        span.set_tag("sql.query", "SELECT * FROM users WHERE id = ?")
        user = db.query_user(user_id)
    return jsonify(user)
```

### FastAPI Example

```python
from fastapi import FastAPI
from ddtrace import tracer, patch_all
from ddtrace.contrib.asgi import TraceMiddleware

patch_all()

app = FastAPI()
app = TraceMiddleware(app, tracer, service="my-fastapi-app")

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    with tracer.trace("fetch.item"):
        item = await get_item(item_id)
    return item
```

## Node.js Instrumentation

### Automatic Instrumentation

**Installation:**
```bash
npm install dd-trace
```

**Initialization (must be first import):**
```javascript
// tracer.js - import this FIRST in your app
const tracer = require('dd-trace').init({
  service: 'my-service',
  env: 'production',
  version: '1.0.0',
  logInjection: true,      // Inject trace IDs into logs
  runtimeMetrics: true,    // Collect runtime metrics
  profiling: true,         // Enable continuous profiler
});

module.exports = tracer;
```

```javascript
// app.js
require('./tracer');  // Must be first!
const express = require('express');
const app = express();
// ... rest of app
```

### Manual Instrumentation

```javascript
const tracer = require('dd-trace');

// Basic span
const span = tracer.startSpan('custom.operation', {
  tags: {
    'service.name': 'my-service',
    'user.id': userId,
  }
});

try {
  const result = await performOperation();
  span.setTag('result.status', result.status);
} catch (error) {
  span.setTag('error', true);
  span.setTag('error.message', error.message);
  throw error;
} finally {
  span.finish();
}

// Using scope
tracer.trace('parent.operation', (span) => {
  // Child spans are automatically linked
  return tracer.trace('child.operation', (childSpan) => {
    return doWork();
  });
});
```

### Express Example

```javascript
require('./tracer');
const express = require('express');
const tracer = require('dd-trace');

const app = express();

app.get('/api/users/:id', async (req, res) => {
  const span = tracer.scope().active();
  span.setTag('user.id', req.params.id);

  const user = await tracer.trace('db.query', async (dbSpan) => {
    dbSpan.setTag('db.type', 'postgresql');
    return await db.getUser(req.params.id);
  });

  res.json(user);
});
```

## Go Instrumentation

### Installation

```bash
go get gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer
go get gopkg.in/DataDog/dd-trace-go.v1/contrib/...
```

### Basic Setup

```go
package main

import (
    "gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

func main() {
    // Start tracer
    tracer.Start(
        tracer.WithService("my-service"),
        tracer.WithEnv("production"),
        tracer.WithServiceVersion("1.0.0"),
    )
    defer tracer.Stop()

    // Your application code
}
```

### Manual Instrumentation

```go
import (
    "context"
    "gopkg.in/DataDog/dd-trace-go.v1/ddtrace/tracer"
)

func processOrder(ctx context.Context, orderID string) error {
    span, ctx := tracer.StartSpanFromContext(ctx, "process.order",
        tracer.ResourceName("ProcessOrder"),
        tracer.Tag("order.id", orderID),
    )
    defer span.Finish()

    // Child span
    childSpan, _ := tracer.StartSpanFromContext(ctx, "db.query")
    result, err := db.Query(ctx, "SELECT * FROM orders WHERE id = ?", orderID)
    if err != nil {
        childSpan.SetTag("error", true)
        childSpan.SetTag("error.message", err.Error())
    }
    childSpan.Finish()

    return err
}
```

### HTTP Server Example

```go
import (
    "net/http"
    httptrace "gopkg.in/DataDog/dd-trace-go.v1/contrib/net/http"
)

func main() {
    tracer.Start(tracer.WithService("my-api"))
    defer tracer.Stop()

    mux := httptrace.NewServeMux()
    mux.HandleFunc("/api/users", handleUsers)

    http.ListenAndServe(":8080", mux)
}
```

## Java Instrumentation

### Automatic Instrumentation (Agent)

**Download Agent:**
```bash
wget -O dd-java-agent.jar https://dtdg.co/latest-java-tracer
```

**Run with Agent:**
```bash
java -javaagent:dd-java-agent.jar \
  -Ddd.service=my-service \
  -Ddd.env=production \
  -Ddd.version=1.0.0 \
  -jar my-app.jar
```

### Spring Boot Example

```java
import datadog.trace.api.Trace;
import datadog.trace.api.DDTags;
import io.opentracing.Span;
import io.opentracing.util.GlobalTracer;

@RestController
public class UserController {

    @GetMapping("/api/users/{id}")
    @Trace(operationName = "get.user", resourceName = "UserController.getUser")
    public User getUser(@PathVariable String id) {
        Span span = GlobalTracer.get().activeSpan();
        span.setTag("user.id", id);

        return userService.findById(id);
    }
}
```

### Manual Instrumentation

```java
import datadog.trace.api.DDTags;
import io.opentracing.Scope;
import io.opentracing.Span;
import io.opentracing.Tracer;
import io.opentracing.util.GlobalTracer;

public class OrderService {
    private final Tracer tracer = GlobalTracer.get();

    public Order processOrder(String orderId) {
        Span span = tracer.buildSpan("process.order")
            .withTag(DDTags.SERVICE_NAME, "order-service")
            .withTag(DDTags.RESOURCE_NAME, "processOrder")
            .withTag("order.id", orderId)
            .start();

        try (Scope scope = tracer.activateSpan(span)) {
            // Your code here
            return doProcessOrder(orderId);
        } catch (Exception e) {
            span.setTag("error", true);
            span.setTag("error.message", e.getMessage());
            throw e;
        } finally {
            span.finish();
        }
    }
}
```

## OpenTelemetry Integration

Datadog supports OpenTelemetry for vendor-neutral instrumentation.

### Python with OpenTelemetry

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

# Configure to send to Datadog Agent OTLP endpoint
resource = Resource.create({
    "service.name": "my-otel-service",
    "deployment.environment": "production",
})

otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True
)

provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-service")

# Use OpenTelemetry API
with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("user.id", user_id)
    # Your code
```

### Node.js with OpenTelemetry

```javascript
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { Resource } = require('@opentelemetry/resources');

const provider = new NodeTracerProvider({
  resource: new Resource({
    'service.name': 'my-otel-service',
    'deployment.environment': 'production',
  }),
});

const exporter = new OTLPTraceExporter({
  url: 'http://localhost:4317',
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();
```

### Enable OTLP in Datadog Agent

```yaml
# datadog.yaml
otlp_config:
  receiver:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
```

## Environment Variables

Common environment variables for all languages:

| Variable | Description | Example |
|----------|-------------|---------|
| `DD_SERVICE` | Service name | `my-service` |
| `DD_ENV` | Environment | `production` |
| `DD_VERSION` | Service version | `1.0.0` |
| `DD_AGENT_HOST` | Agent hostname | `localhost` |
| `DD_TRACE_AGENT_PORT` | Agent trace port | `8126` |
| `DD_TRACE_ENABLED` | Enable/disable tracing | `true` |
| `DD_LOGS_INJECTION` | Inject trace IDs into logs | `true` |
| `DD_TRACE_SAMPLE_RATE` | Sampling rate (0.0-1.0) | `1.0` |
| `DD_PROFILING_ENABLED` | Enable profiling | `true` |

## Best Practices

1. **Always set service, env, version**: Enables correlation and filtering
2. **Use automatic instrumentation first**: Add manual spans only when needed
3. **Add meaningful tags**: Business context, user IDs (if low cardinality), request metadata
4. **Handle errors properly**: Set error tags and capture stack traces
5. **Propagate context**: Pass context through async operations and service calls
