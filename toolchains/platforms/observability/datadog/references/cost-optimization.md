# Cost Optimization

Datadog costs can grow quickly without proper controls. This guide covers strategies to manage and optimize spending.

## Primary Cost Drivers

| Category | Pricing Model | Cost Driver |
|----------|---------------|-------------|
| **Infrastructure** | Per host/month | Number of hosts |
| **APM** | Per host/month | Traced hosts |
| **Logs** | Per GB ingested + indexed | Log volume |
| **Custom Metrics** | Per metric/month | Unique metric + tag combinations |
| **Synthetics** | Per 10K test runs | Test frequency x locations |
| **RUM** | Per 1K sessions | User session volume |

## Metrics Without Limits

Decouple metric ingestion from queryable tags to control custom metric costs.

### How It Works

1. **Ingest all tags**: Full cardinality sent to Datadog
2. **Configure allowlist**: Select which tags are queryable
3. **Pay for queryable**: Only queryable tag combinations count as custom metrics

### Configuration

**Via UI:**
1. Go to Metrics > Summary
2. Select your metric
3. Click "Configure Tags"
4. Select only needed tags

**Via API:**
```python
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client import Configuration, ApiClient

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api = MetricsApi(api_client)

    api.update_tag_configuration(
        metric_name="myapp.http.requests",
        body={
            "data": {
                "type": "manage_tags",
                "id": "myapp.http.requests",
                "attributes": {
                    "tags": ["env", "service", "endpoint", "status_class"],
                    "include_percentiles": True,
                    "metric_type": "count"
                }
            }
        }
    )
```

### Example Savings

**Before (all tags queryable):**
```
3 envs x 10 services x 100 endpoints x 10 status codes x 50 hosts
= 1,500,000 custom metrics
```

**After (limited tags):**
```
3 envs x 10 services x 100 endpoints x 5 status_classes
= 15,000 custom metrics (99% reduction)
```

## Log Index Quotas

Prevent unexpected log volume spikes from causing cost overruns.

### Set Daily Quota

```json
{
  "name": "production-logs",
  "filter": {
    "query": "env:production"
  },
  "daily_limit": 5000000000,
  "daily_limit_reset": {
    "reset_time": "00:00",
    "reset_utc_offset": "+00:00"
  },
  "daily_limit_warning_threshold_percentage": 80
}
```

### Quota Alerting

Create a monitor for quota warnings:

```json
{
  "name": "Log Index Quota Warning",
  "type": "logs alert",
  "query": "logs(\"*\").index(\"production-logs\").rollup(\"count\").last(\"1d\") > 4000000000",
  "message": "Log index nearing daily quota (80% threshold).\n\nConsider:\n- Adding exclusion filters\n- Reducing log verbosity\n- Increasing quota\n\n@slack-platform-alerts"
}
```

## Exclusion Filters

Drop logs before indexing to reduce costs.

### Common Exclusion Patterns

```json
{
  "exclusion_filters": [
    {
      "name": "Exclude health checks",
      "filter": {
        "query": "http.url:(\"/health\" OR \"/ready\" OR \"/live\")"
      },
      "is_enabled": true
    },
    {
      "name": "Exclude debug logs",
      "filter": {
        "query": "level:debug"
      },
      "is_enabled": true
    },
    {
      "name": "Sample verbose service (10%)",
      "filter": {
        "query": "service:verbose-service",
        "sample_rate": 0.1
      },
      "is_enabled": true
    },
    {
      "name": "Exclude bot traffic",
      "filter": {
        "query": "@http.useragent:(*bot* OR *crawler* OR *spider*)"
      },
      "is_enabled": true
    }
  ]
}
```

### Agent-Side Exclusion (More Efficient)

Drop logs before sending to Datadog:

```yaml
# /etc/datadog-agent/conf.d/app.d/conf.yaml
logs:
  - type: file
    path: /var/log/app/*.log
    source: myapp
    log_processing_rules:
      - type: exclude_at_match
        name: exclude_healthchecks
        pattern: GET /health

      - type: exclude_at_match
        name: exclude_debug
        pattern: '"level":"debug"'
```

## APM Sampling Strategies

### Ingestion Controls

Configure sampling to reduce trace volume while maintaining visibility.

**Head-Based Sampling (Agent):**
```yaml
# datadog.yaml
apm_config:
  max_traces_per_second: 100  # Per agent

  # Rule-based sampling
  filter_tags:
    require:
      - env:production
    reject:
      - http.url:/health
```

**Library-Level Sampling:**
```python
from ddtrace import tracer

tracer.configure(
    sampler=DatadogSampler(
        default_sample_rate=0.1,  # 10% default
        rules=[
            SamplingRule(sample_rate=1.0, service="critical-service"),
            SamplingRule(sample_rate=0.01, service="high-volume-service"),
        ]
    )
)
```

### Retention Filters

Keep only valuable traces in long-term storage:

**Via UI:**
1. Go to APM > Setup & Configuration > Data Retention
2. Create retention filters

**Recommended Filters:**
```json
[
  {
    "name": "Errors",
    "query": "@_top_level:1 @error.type:*",
    "rate": 1.0
  },
  {
    "name": "Slow requests (>1s)",
    "query": "@duration:>1000000000",
    "rate": 1.0
  },
  {
    "name": "Sample successful requests",
    "query": "@http.status_code:2* @duration:<1000000000",
    "rate": 0.1
  }
]
```

## Custom Metrics Cardinality Control

### Audit High-Cardinality Metrics

```python
from datadog_api_client.v1.api.metrics_api import MetricsApi

api = MetricsApi(api_client)

# List all custom metrics
metrics = api.list_active_metrics(from_time=int(time.time()) - 86400)

# Find high-cardinality culprits
for metric in metrics.metrics:
    details = api.get_metric_metadata(metric)
    print(f"{metric}: {details}")
```

### Dashboard for Cardinality Monitoring

Create widget with query:
```
count:datadog.estimated_usage.metrics.custom{*} by {metric_name}
```

### Common Cardinality Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| User IDs as tags | `user_id:{id}` tag | Remove or aggregate |
| Request IDs | `request_id:{id}` tag | Remove entirely |
| Timestamps | `timestamp:{ts}` tag | Never use timestamps |
| Pod names | `pod:{name}` in K8s | Use deployment/service |
| Build numbers | `build:{num}` tag | Use version ranges |

## Usage Attribution API

Track costs by team, service, or project.

### Query Usage

```python
from datadog_api_client.v1.api.usage_metering_api import UsageMeteringApi
from datetime import datetime, timedelta

api = UsageMeteringApi(api_client)

# Get monthly usage summary
usage = api.get_usage_summary(
    start_month=datetime(2026, 1, 1),
    end_month=datetime(2026, 1, 31)
)

print(f"Hosts: {usage.usage[0].host_count}")
print(f"APM Hosts: {usage.usage[0].apm_host_top99p}")
print(f"Custom Metrics: {usage.usage[0].custom_ts_avg}")
print(f"Indexed Logs: {usage.usage[0].indexed_events_count}")
```

### Usage Attribution by Tag

```python
# Get usage attributed by 'team' tag
attribution = api.get_monthly_usage_attribution(
    start_month=datetime(2026, 1, 1),
    fields="*",
    tag_breakdown_keys="team"
)

for org in attribution.usage:
    print(f"Team: {org.tags.get('team')}")
    print(f"  Infra hosts: {org.infra_host_percentage}%")
    print(f"  Custom metrics: {org.custom_ts_percentage}%")
```

### Create Cost Allocation Dashboard

```json
{
  "title": "Datadog Cost Attribution",
  "widgets": [
    {
      "title": "Custom Metrics by Team",
      "type": "toplist",
      "query": "sum:datadog.estimated_usage.metrics.custom{*} by {team}"
    },
    {
      "title": "Log Volume by Service",
      "type": "toplist",
      "query": "sum:datadog.estimated_usage.logs.ingested_bytes{*} by {service}"
    },
    {
      "title": "APM Spans by Service",
      "type": "toplist",
      "query": "sum:datadog.estimated_usage.apm.indexed_spans{*} by {service}"
    }
  ]
}
```

## Committed Contracts

### Potential Savings

| Commitment | Typical Discount |
|------------|-----------------|
| 1 year | 20-30% |
| 2 year | 30-40% |
| 3 year | 40-50% |

### When to Commit

**Good candidates:**
- Stable host count (predictable infrastructure)
- Consistent log volume
- Established custom metrics footprint

**Wait before committing:**
- New to Datadog (need baseline)
- Rapid growth phase
- Major architecture changes planned

### Negotiation Tips

1. **Bundle products**: Combine APM, logs, infra for better rates
2. **Use current spend**: Leverage existing usage as baseline
3. **Multi-year**: Longer terms = bigger discounts
4. **Volume tiers**: Higher volume = better per-unit pricing
5. **Timing**: End of quarter/year often has best deals

## Cost Monitoring Alerts

### Budget Alerting

```json
{
  "name": "Datadog Daily Cost Alert",
  "type": "metric alert",
  "query": "sum(last_1d):sum:datadog.estimated_usage.hosts{*} * 15 + sum:datadog.estimated_usage.logs.ingested_bytes{*} / 1000000000 * 0.10 > 1000",
  "message": "Estimated daily Datadog cost exceeds $1000.\n\nBreakdown:\n- Hosts: {{value}}\n- Logs: {{value}} GB\n\nReview usage: https://app.datadoghq.com/billing/usage\n\n@finance-alerts"
}
```

### Anomaly on Usage

```json
{
  "name": "Anomalous Custom Metric Growth",
  "type": "metric alert",
  "query": "avg(last_1d):anomalies(sum:datadog.estimated_usage.metrics.custom{*}, 'basic', 3) >= 1",
  "message": "Unusual growth in custom metrics detected.\n\nThis may indicate:\n- New high-cardinality tags\n- New service with many metrics\n- Misconfigured instrumentation\n\n@platform-team"
}
```

## Optimization Checklist

### Weekly Review

- [ ] Check current month usage vs. budget
- [ ] Review top 10 custom metrics by cardinality
- [ ] Check log exclusion filter effectiveness
- [ ] Review any new high-volume services

### Monthly Review

- [ ] Analyze usage attribution by team
- [ ] Audit unused monitors and dashboards
- [ ] Review APM sampling effectiveness
- [ ] Check for orphaned metrics (no queries)

### Quarterly Review

- [ ] Evaluate committed contract vs. actual usage
- [ ] Review Metrics without Limits configurations
- [ ] Assess new product needs
- [ ] Plan capacity for next quarter

## Quick Wins

| Action | Effort | Impact |
|--------|--------|--------|
| Exclude health check logs | Low | Medium |
| Remove high-cardinality tags | Low | High |
| Set log index quotas | Low | High (prevents spikes) |
| Enable Metrics without Limits | Medium | High |
| Configure APM sampling | Medium | Medium |
| Agent-side log filtering | Medium | Medium |
| Committed contract | High | High (20-50% savings) |
