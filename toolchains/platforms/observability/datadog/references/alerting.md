# Alerting

Datadog monitors provide proactive alerting on metrics, logs, traces, and synthetic tests.

## Monitor Types

| Type | Use Case | Example |
|------|----------|---------|
| **Metric** | Threshold or anomaly on metric values | CPU > 90%, Error rate > 5% |
| **Log** | Pattern detection in logs | ERROR count > 100/5m |
| **APM** | Trace analytics alerts | P99 latency > 500ms |
| **Synthetic** | Proactive endpoint testing | API health check failing |
| **Composite** | Multiple conditions combined | High errors AND high latency |
| **Forecast** | Predict future threshold breach | Disk full in 24 hours |

## Metric Monitor Examples

### Basic Threshold Monitor

```json
{
  "name": "High CPU Usage on {{host.name}}",
  "type": "metric alert",
  "query": "avg(last_5m):avg:system.cpu.user{env:production} by {host} > 90",
  "message": "CPU usage is above 90% on {{host.name}}.\n\nCurrent value: {{value}}%\n\n@slack-platform-alerts",
  "tags": ["team:platform", "severity:warning"],
  "priority": 3,
  "options": {
    "thresholds": {
      "critical": 90,
      "warning": 80
    },
    "notify_no_data": true,
    "no_data_timeframe": 10,
    "notify_audit": false,
    "require_full_window": false,
    "include_tags": true
  }
}
```

### Error Rate Monitor

```json
{
  "name": "High Error Rate - {{service.name}}",
  "type": "metric alert",
  "query": "sum(last_5m):sum:http.requests.errors{env:production} by {service}.as_rate() / sum:http.requests{env:production} by {service}.as_rate() * 100 > 5",
  "message": "Error rate exceeds 5% for {{service.name}}.\n\nCurrent error rate: {{value}}%\n\nRunbook: https://wiki/runbook/high-errors\n\n@pagerduty-platform",
  "tags": ["team:platform", "severity:critical"],
  "priority": 1,
  "options": {
    "thresholds": {
      "critical": 5,
      "warning": 2
    },
    "notify_no_data": false,
    "renotify_interval": 60,
    "escalation_message": "Error rate still elevated after 1 hour. Escalating."
  }
}
```

### P99 Latency Monitor

```json
{
  "name": "High P99 Latency - {{service.name}}",
  "type": "metric alert",
  "query": "percentile(last_5m):p99:trace.http.request.duration{env:production} by {service} > 1000000000",
  "message": "P99 latency exceeds 1 second for {{service.name}}.\n\nCurrent P99: {{value}}ns\n\n@slack-platform-alerts",
  "tags": ["team:platform", "severity:warning"],
  "options": {
    "thresholds": {
      "critical": 1000000000,
      "warning": 500000000
    }
  }
}
```

## Anomaly Detection

Anomaly detection identifies deviations from historical patterns.

### Anomaly Detection Algorithms

| Algorithm | Best For | Characteristics |
|-----------|----------|-----------------|
| **Basic** | Stable metrics with clear trends | Simple, less adaptive |
| **Agile** | Rapidly changing metrics | Quick to adapt, may overfit |
| **Robust** | Metrics with outliers | Tolerant to spikes |

### Anomaly Monitor Example

```json
{
  "name": "Anomalous Request Rate - {{service.name}}",
  "type": "metric alert",
  "query": "avg(last_4h):anomalies(avg:http.requests{env:production} by {service}, 'agile', 3, direction='both', interval=60, alert_window='last_15m', count_default_zero='true') >= 1",
  "message": "Request rate is abnormally high/low for {{service.name}}.\n\nThis could indicate:\n- Traffic spike\n- Outage upstream\n- Bot activity\n\n@slack-platform-alerts",
  "tags": ["team:platform", "severity:warning"],
  "options": {
    "thresholds": {
      "critical": 1,
      "warning": 0.8
    },
    "threshold_windows": {
      "trigger_window": "last_15m",
      "recovery_window": "last_15m"
    }
  }
}
```

### Anomaly Detection Best Practices

1. **Require historical data**: Anomaly detection needs baseline (weeks/months)
2. **Use appropriate algorithm**:
   - Basic: Seasonal patterns (daily/weekly)
   - Agile: Fast-changing metrics
   - Robust: Noisy metrics with outliers
3. **Set evaluation delay**: 300+ seconds for cloud metrics
4. **Start with wider bounds**: Tighten after observing behavior
5. **Avoid for new metrics**: No baseline = false positives

## Composite Monitors

Combine multiple monitors with boolean logic.

```json
{
  "name": "Critical Service Degradation",
  "type": "composite",
  "query": "( high_error_rate && high_latency ) || service_down",
  "message": "Critical service degradation detected.\n\nMultiple signals indicate a major issue:\n- High errors: {{#is_alert}}YES{{/is_alert}}\n- High latency: {{#is_alert}}YES{{/is_alert}}\n- Service down: {{#is_alert}}YES{{/is_alert}}\n\n@pagerduty-critical",
  "tags": ["team:platform", "severity:critical"],
  "options": {
    "notify_no_data": false
  }
}
```

## Forecast Monitors

Predict future threshold breaches.

```json
{
  "name": "Disk Space Forecast - {{host.name}}",
  "type": "metric alert",
  "query": "max(next_1w):forecast(avg:system.disk.used{env:production} by {host}, 'linear', 1, interval='60m', history='1w', model='default') > 90",
  "message": "Disk usage predicted to exceed 90% within 1 week on {{host.name}}.\n\nCurrent usage: {{value}}%\n\nConsider:\n- Cleaning up old logs\n- Expanding storage\n- Archiving data\n\n@slack-infrastructure",
  "tags": ["team:infrastructure", "severity:warning"]
}
```

## Log Monitors

Alert on log patterns and counts.

```json
{
  "name": "High Error Log Volume",
  "type": "log alert",
  "query": "logs(\"status:error env:production\").index(\"main\").rollup(\"count\").last(\"5m\") > 100",
  "message": "More than 100 error logs in the last 5 minutes.\n\nSearch logs: https://app.datadoghq.com/logs?query=status:error%20env:production\n\n@slack-platform-alerts",
  "tags": ["team:platform", "severity:warning"],
  "options": {
    "thresholds": {
      "critical": 100,
      "warning": 50
    },
    "enable_logs_sample": true
  }
}
```

## Alert Configuration Best Practices

### Message Templates

```markdown
{{#is_alert}}
ALERT: {{name}} triggered.

Current Value: {{value}}
Threshold: {{threshold}}
Host: {{host.name}}
Service: {{service.name}}
Environment: {{env.name}}

Runbook: https://wiki/runbook/{{name}}
Dashboard: https://app.datadoghq.com/dashboard/xxx

@pagerduty-{{team.name}}
{{/is_alert}}

{{#is_recovery}}
RECOVERED: {{name}} is back to normal.

Previous Value: {{value}}
{{/is_recovery}}
```

### Thresholds

```json
"options": {
  "thresholds": {
    "critical": 95,
    "critical_recovery": 85,
    "warning": 80,
    "warning_recovery": 70
  }
}
```

**Recovery thresholds** prevent flapping (rapid alert/recovery cycles).

### Evaluation Windows

| Metric Type | Recommended Window |
|-------------|-------------------|
| Real-time metrics | 5 minutes |
| Cloud provider metrics | 10-15 minutes |
| Log counts | 5-15 minutes |
| Anomaly detection | 15-60 minutes |

### No Data Handling

```json
"options": {
  "notify_no_data": true,
  "no_data_timeframe": 10
}
```

Use `notify_no_data: true` for:
- Critical services that should always emit data
- Synthetic monitors

Use `notify_no_data: false` for:
- Metrics that legitimately stop (batch jobs)
- Sparse event-based metrics

## Alert Hygiene

### Priority Levels

| Priority | Response Time | Notification |
|----------|---------------|--------------|
| P1 | Immediate | PagerDuty, phone |
| P2 | 15 minutes | PagerDuty, Slack |
| P3 | 1 hour | Slack, email |
| P4 | Next day | Email, ticket |
| P5 | Best effort | Dashboard only |

### Alert on Symptoms, Not Causes

**Good (symptoms):**
- Error rate > 5%
- P99 latency > 1s
- Checkout failures > 10/min

**Avoid (causes):**
- CPU > 90% (may not affect users)
- Memory > 80% (system may handle it)
- Deployment started (not actionable)

### Review Cadence

1. **Weekly**: Review all firing alerts
2. **Monthly**: Audit alert noise (alerts with no action taken)
3. **Quarterly**: Delete or tune unused monitors

## Downtime Management

### Scheduled Downtime

```json
{
  "scope": "env:production AND service:api-gateway",
  "start": 1706400000,
  "end": 1706403600,
  "message": "Scheduled maintenance window for API gateway upgrade",
  "timezone": "America/New_York",
  "monitor_id": null,
  "recurrence": null
}
```

### Recurring Downtime

```json
{
  "scope": "env:staging",
  "message": "Weekly staging environment reset",
  "timezone": "UTC",
  "recurrence": {
    "type": "weeks",
    "period": 1,
    "week_days": ["Sun"],
    "until_date": null
  }
}
```

## Runbook Integration

### Runbook Template

Include in alert messages:

```markdown
## Runbook: {{name}}

### Symptoms
- [What the alert indicates]

### Impact
- [User/business impact]

### Investigation Steps
1. Check dashboard: [link]
2. Check logs: [query link]
3. Check traces: [APM link]

### Mitigation
1. [Immediate actions]
2. [Rollback steps if needed]

### Escalation
- L1: @slack-platform
- L2: @pagerduty-platform (after 15 min)
- L3: @pagerduty-oncall-manager (after 1 hour)
```

## Notification Integrations

### Slack

```markdown
@slack-channel-name
@slack-private-channel-name
```

### PagerDuty

```markdown
@pagerduty-service-name
```

### Email

```markdown
@user@company.com
@team-distribution-list@company.com
```

### Webhooks

Configure in Integrations > Webhooks, then reference:
```markdown
@webhook-my-webhook
```
