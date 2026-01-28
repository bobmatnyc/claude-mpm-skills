# Custom Metrics

DogStatsD enables submitting custom metrics from applications to Datadog.

## DogStatsD Setup

### Agent Configuration

DogStatsD runs on port 8125 by default. Enable non-local traffic for containerized apps:

```yaml
# datadog.yaml
dogstatsd_non_local_traffic: true
dogstatsd_port: 8125
dogstatsd_origin_detection: true  # For container tagging
```

**Docker:**
```bash
docker run -d --name dd-agent \
  -e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true \
  -p 8125:8125/udp \
  gcr.io/datadoghq/agent:7
```

**Kubernetes:**
```yaml
# Helm values
datadog:
  dogstatsd:
    nonLocalTraffic: true
    useHostPort: true
```

## Metric Types

| Type | Description | Use Case |
|------|-------------|----------|
| **COUNT** | Incremental counter | Request count, events |
| **GAUGE** | Point-in-time value | Queue size, temperature |
| **HISTOGRAM** | Distribution (local aggregation) | Response time, payload size |
| **DISTRIBUTION** | Distribution (global aggregation) | Latency percentiles across hosts |
| **SET** | Count unique values | Unique users, sessions |

## Python Examples

### Installation

```bash
pip install datadog
```

### Basic Usage

```python
from datadog import DogStatsd

statsd = DogStatsd(host="localhost", port=8125)

# COUNT - increment a counter
statsd.increment('page.views', tags=['page:home', 'env:production'])
statsd.increment('api.requests', value=1, tags=['endpoint:/api/users', 'method:GET'])
statsd.decrement('queue.jobs')

# GAUGE - set a point-in-time value
statsd.gauge('queue.size', 42, tags=['queue:orders'])
statsd.gauge('cache.hit_ratio', 0.85, tags=['cache:redis'])
statsd.gauge('system.memory_used_percent', 73.5)

# HISTOGRAM - track value distribution
statsd.histogram('request.latency', 0.123, tags=['endpoint:/api/users'])
statsd.histogram('payload.size', 4096, tags=['type:upload'])

# DISTRIBUTION - global percentile aggregation
statsd.distribution('payment.amount', 99.99, tags=['currency:usd'])
statsd.distribution('response.time', 45.2, tags=['service:api'])

# SET - count unique values
statsd.set('users.uniques', 'user123', tags=['source:web'])
statsd.set('sessions.active', session_id)
```

### Context Manager for Timing

```python
from datadog import DogStatsd

statsd = DogStatsd()

# Time a code block
with statsd.timed('database.query.duration', tags=['db:postgres']):
    result = db.execute(query)

# Time a function
@statsd.timed('api.endpoint.latency')
def process_request(request):
    return handle(request)
```

### Flask Integration

```python
from flask import Flask, request, g
from datadog import DogStatsd
import time

app = Flask(__name__)
statsd = DogStatsd()

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - g.start_time

    statsd.increment('http.requests', tags=[
        f'method:{request.method}',
        f'endpoint:{request.endpoint}',
        f'status:{response.status_code}',
    ])

    statsd.histogram('http.latency', latency, tags=[
        f'method:{request.method}',
        f'endpoint:{request.endpoint}',
    ])

    return response
```

## Node.js Examples

### Installation

```bash
npm install hot-shots
```

### Basic Usage

```javascript
const StatsD = require('hot-shots');

const statsd = new StatsD({
  host: 'localhost',
  port: 8125,
  prefix: 'myapp.',
  globalTags: ['env:production'],
});

// COUNT
statsd.increment('page.views', ['page:home']);
statsd.increment('api.requests', 1, ['endpoint:/users', 'method:GET']);
statsd.decrement('queue.jobs');

// GAUGE
statsd.gauge('queue.size', 42, ['queue:orders']);
statsd.gauge('cache.hit_ratio', 0.85);

// HISTOGRAM
statsd.histogram('request.latency', 123, ['endpoint:/users']);

// DISTRIBUTION
statsd.distribution('payment.amount', 99.99, ['currency:usd']);

// SET
statsd.set('users.uniques', 'user123');

// TIMING
statsd.timing('db.query.time', 45, ['query:select']);
```

### Express Middleware

```javascript
const StatsD = require('hot-shots');
const statsd = new StatsD();

function metricsMiddleware(req, res, next) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    const tags = [
      `method:${req.method}`,
      `path:${req.route?.path || req.path}`,
      `status:${res.statusCode}`,
    ];

    statsd.increment('http.requests', tags);
    statsd.histogram('http.latency', duration, tags);
  });

  next();
}

app.use(metricsMiddleware);
```

## Go Examples

### Installation

```bash
go get github.com/DataDog/datadog-go/v5/statsd
```

### Basic Usage

```go
package main

import (
    "github.com/DataDog/datadog-go/v5/statsd"
    "time"
)

func main() {
    client, err := statsd.New("localhost:8125",
        statsd.WithNamespace("myapp."),
        statsd.WithTags([]string{"env:production"}),
    )
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    // COUNT
    client.Incr("page.views", []string{"page:home"}, 1)
    client.Count("api.requests", 1, []string{"endpoint:/users"}, 1)
    client.Decr("queue.jobs", []string{}, 1)

    // GAUGE
    client.Gauge("queue.size", 42, []string{"queue:orders"}, 1)

    // HISTOGRAM
    client.Histogram("request.latency", 0.123, []string{"endpoint:/users"}, 1)

    // DISTRIBUTION
    client.Distribution("payment.amount", 99.99, []string{"currency:usd"}, 1)

    // SET
    client.Set("users.uniques", "user123", []string{}, 1)

    // TIMING
    start := time.Now()
    // ... operation
    client.Timing("operation.duration", time.Since(start), []string{}, 1)
}
```

### HTTP Middleware

```go
func metricsMiddleware(statsd *statsd.Client) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()

            // Wrap response writer to capture status
            wrapped := &statusResponseWriter{ResponseWriter: w, status: 200}

            next.ServeHTTP(wrapped, r)

            tags := []string{
                fmt.Sprintf("method:%s", r.Method),
                fmt.Sprintf("path:%s", r.URL.Path),
                fmt.Sprintf("status:%d", wrapped.status),
            }

            statsd.Incr("http.requests", tags, 1)
            statsd.Timing("http.latency", time.Since(start), tags, 1)
        })
    }
}
```

## Naming Conventions

### Rules

1. **Must start with a letter**
2. **Alphanumeric, underscores, periods only** (ASCII)
3. **Maximum 200 characters** (prefer under 100)
4. **Case-sensitive**
5. **No spaces**

### Recommended Pattern

```
<namespace>.<category>.<metric_name>
```

**Examples:**
```
myapp.api.request.count
myapp.api.request.latency
myapp.db.query.duration
myapp.cache.hit_ratio
myapp.queue.size
myapp.payment.amount
```

### Avoid

```
MyApp.API.Request.Count     # Wrong: uppercase, dots instead of underscores
my-app.api.request-count    # Wrong: hyphens
1_request_count             # Wrong: starts with number
request count               # Wrong: spaces
```

## Tagging Best Practices

### Good Tags (Low Cardinality)

```python
# Environment and service context
tags = [
    'env:production',
    'service:api-gateway',
    'version:1.2.3',
    'team:platform',
    'region:us-east-1',
]

# Request metadata
tags = [
    'method:GET',
    'endpoint:/api/users',
    'status_class:2xx',
]

# Business context (bounded values)
tags = [
    'plan:enterprise',
    'feature:checkout',
    'payment_method:credit_card',
]
```

### Bad Tags (High Cardinality)

```python
# AVOID - creates millions of unique metrics
tags = [
    f'user_id:{user_id}',           # Unbounded user IDs
    f'request_id:{request_id}',     # Unique per request
    f'timestamp:{timestamp}',        # Always unique
    f'pod:{pod_name}',              # Ephemeral in K8s
    f'transaction_id:{tx_id}',      # Unbounded
    f'session_id:{session_id}',     # Unbounded
]
```

## Cardinality Management

### Understanding Cardinality

Each unique combination of metric name + tag values = 1 custom metric.

**Example:**
```python
# 3 endpoints x 3 methods x 5 status classes = 45 custom metrics
statsd.increment('http.requests', tags=[
    f'endpoint:{endpoint}',   # 3 values
    f'method:{method}',       # 3 values
    f'status_class:{class}',  # 5 values
])
```

### Cardinality Explosion Example

```python
# BAD: 1M users x 100 endpoints = 100M custom metrics = $$$
statsd.increment('requests', tags=[
    f'user_id:{user_id}',
    f'endpoint:{endpoint}',
])

# GOOD: 100 endpoints x 10 plans = 1000 custom metrics
statsd.increment('requests', tags=[
    f'plan:{user.plan}',
    f'endpoint:{endpoint}',
])
```

### Metrics Without Limits

Configure tag allowlists to control cardinality at the Datadog level:

1. Go to Metrics > Summary
2. Select metric
3. Click "Configure Tags"
4. Add only tags you want to query by

**API Configuration:**
```python
from datadog_api_client.v2.api.metrics_api import MetricsApi

api = MetricsApi(api_client)
api.update_tag_configuration(
    metric_name="myapp.http.requests",
    body={
        "data": {
            "type": "manage_tags",
            "id": "myapp.http.requests",
            "attributes": {
                "tags": ["env", "service", "endpoint"],
                "include_percentiles": True
            }
        }
    }
)
```

## Cost Monitoring

### Track Custom Metric Usage

```python
from datadog_api_client.v1.api.usage_metering_api import UsageMeteringApi
from datetime import datetime

api = UsageMeteringApi(api_client)

# Get hourly custom metrics usage
usage = api.get_usage_top_avg_metrics(
    month=datetime(2026, 1, 1),
    names=["myapp.*"]
)

for metric in usage.usage:
    print(f"{metric.metric_name}: {metric.avg_metric_hour} avg/hour")
```

### Dashboard for Metric Cardinality

Create a dashboard widget with:
```
count:datadog.estimated_usage.metrics.custom{*} by {metric_name}
```

## Best Practices Summary

1. **Use consistent naming**: `namespace.category.metric`
2. **Keep cardinality low**: Bounded tag values only
3. **Add business context**: Plan, feature, region
4. **Avoid user-level tags**: Use aggregations instead
5. **Monitor usage**: Track custom metric counts
6. **Use Metrics without Limits**: Control queryable tags
7. **Prefer DISTRIBUTION over HISTOGRAM**: Global percentiles
