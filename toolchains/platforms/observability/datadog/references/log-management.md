# Log Management

Datadog Log Management provides centralized collection, processing, and analysis with 15-month retention options.

## Agent Log Collection

### Docker Container Logs

**Enable container log collection:**
```yaml
# docker-compose.yaml
datadog-agent:
  environment:
    - DD_LOGS_ENABLED=true
    - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
```

**Application container labels:**
```yaml
services:
  my-app:
    labels:
      com.datadoghq.ad.logs: '[{"source": "python", "service": "my-app"}]'
```

### File-Based Collection

**Configuration in conf.d:**
```yaml
# /etc/datadog-agent/conf.d/my-app.d/conf.yaml
logs:
  - type: file
    path: /var/log/my-app/*.log
    source: my-app
    service: my-app
    tags:
      - env:production
      - team:platform
```

**Multiple log files:**
```yaml
logs:
  - type: file
    path: /var/log/my-app/app.log
    source: my-app
    service: my-app

  - type: file
    path: /var/log/my-app/error.log
    source: my-app
    service: my-app
    log_processing_rules:
      - type: include_at_match
        name: only_errors
        pattern: (ERROR|CRITICAL)
```

### TCP/UDP Log Collection

```yaml
logs:
  - type: tcp
    port: 10514
    source: syslog
    service: my-app

  - type: udp
    port: 10515
    source: syslog
    service: my-app
```

## Pipeline Configuration

Pipelines process logs before indexing, enabling parsing, enrichment, and transformation.

### Creating a Pipeline

**Via Datadog UI:**
1. Go to Logs > Configuration > Pipelines
2. Click "New Pipeline"
3. Set filter query (e.g., `source:nginx`)
4. Add processors

**Pipeline Example (JSON API):**
```json
{
  "name": "NGINX Access Logs",
  "filter": {
    "query": "source:nginx"
  },
  "processors": [
    {
      "type": "grok-parser",
      "name": "Parse NGINX logs",
      "source": "message",
      "samples": [
        "192.168.1.1 - - [27/Jan/2026:10:00:00 +0000] \"GET /api/users HTTP/1.1\" 200 1234"
      ],
      "grok": {
        "matchRules": "%{_client_ip} - - \\[%{_date_access}\\] \"%{_method} %{_url} HTTP/%{_version}\" %{_status_code} %{_bytes_sent}"
      }
    },
    {
      "type": "status-remapper",
      "name": "Set log status",
      "sources": ["http.status_code"]
    }
  ]
}
```

## Grok Parsing Patterns

### Common Log Formats

**NGINX Access Log:**
```grok
%{_client_ip:network.client.ip} - %{_ident} \[%{_date_access}\] "%{_method:http.method} %{_url:http.url} HTTP/%{_version:http.version}" %{_status_code:http.status_code} %{_bytes_sent:network.bytes_written}
```

**Apache Combined Log:**
```grok
%{_client_ip:network.client.ip} %{_ident} %{_auth} \[%{_date_access}\] "%{_method:http.method} %{_url:http.url} HTTP/%{_version}" %{_status_code:http.status_code} %{_bytes_sent:network.bytes_written} "%{_referer:http.referer}" "%{_user_agent:http.useragent}"
```

**JSON Logs:**
```grok
%{data::json}
```

**Python Exception:**
```grok
%{word:level} %{date("yyyy-MM-dd HH:mm:ss,SSS"):timestamp} %{notSpace:logger} - %{data:message}
```

### Helper Patterns

| Pattern | Description | Example Match |
|---------|-------------|---------------|
| `%{_client_ip}` | IP address | `192.168.1.1` |
| `%{_date_access}` | Common log date | `27/Jan/2026:10:00:00 +0000` |
| `%{_method}` | HTTP method | `GET`, `POST` |
| `%{_status_code}` | HTTP status | `200`, `404` |
| `%{word}` | Single word | `ERROR` |
| `%{data}` | Any characters | Everything else |
| `%{notSpace}` | Non-whitespace | `my.module.name` |

### Grok Parser Configuration

```yaml
processors:
  - type: grok-parser
    name: Parse application logs
    source: message
    grok:
      supportRules: |
        _timestamp %{date("yyyy-MM-dd HH:mm:ss.SSS"):timestamp}
        _level %{word:level}
        _logger %{notSpace:logger}
      matchRules: |
        app_log %{_timestamp} %{_level} %{_logger} - %{data:message}
    samples:
      - "2026-01-27 10:30:45.123 INFO my.app.handler - Request processed successfully"
```

## Standard Attributes

Map parsed fields to Datadog standard attributes for consistent querying and correlation.

### Core Attributes

| Standard Attribute | Description | Source Field Example |
|-------------------|-------------|---------------------|
| `http.method` | HTTP method | `method`, `request_method` |
| `http.status_code` | HTTP status | `status`, `response_code` |
| `http.url` | Request URL | `url`, `request_uri` |
| `network.client.ip` | Client IP | `client_ip`, `remote_addr` |
| `duration` | Request duration (ns) | `response_time` |
| `usr.id` | User identifier | `user_id`, `customer_id` |
| `error.message` | Error message | `error_msg`, `exception` |
| `error.stack` | Stack trace | `stacktrace`, `traceback` |

### Attribute Remapper

```yaml
processors:
  - type: attribute-remapper
    name: Remap to standard attributes
    sources:
      - request_method
    target: http.method
    targetType: string
    preserveSource: false

  - type: attribute-remapper
    name: Remap status code
    sources:
      - status
      - response_code
    target: http.status_code
    targetType: number
```

## Processing Rules (Agent-Side)

Filter and transform logs before sending to Datadog.

### Exclude Logs

```yaml
# conf.d/my-app.d/conf.yaml
logs:
  - type: file
    path: /var/log/my-app/*.log
    source: my-app
    log_processing_rules:
      # Exclude health checks
      - type: exclude_at_match
        name: exclude_healthchecks
        pattern: '"path":"/health"'

      # Exclude debug logs in production
      - type: exclude_at_match
        name: exclude_debug
        pattern: DEBUG
```

### Include Only Specific Logs

```yaml
log_processing_rules:
  - type: include_at_match
    name: only_errors
    pattern: (ERROR|CRITICAL|FATAL)
```

### Mask Sensitive Data

```yaml
log_processing_rules:
  - type: mask_sequences
    name: mask_credit_cards
    pattern: \d{4}-\d{4}-\d{4}-\d{4}
    replace_placeholder: "[MASKED_CC]"

  - type: mask_sequences
    name: mask_ssn
    pattern: \d{3}-\d{2}-\d{4}
    replace_placeholder: "[MASKED_SSN]"
```

### Multi-line Aggregation

```yaml
log_processing_rules:
  # Java stack traces
  - type: multi_line
    name: java_stacktrace
    pattern: ^\d{4}-\d{2}-\d{2}
```

## Archive and Rehydration

### Configure Log Archive

**Archive to S3:**
```json
{
  "type": "archives",
  "data": {
    "type": "archives",
    "attributes": {
      "name": "production-logs-archive",
      "query": "env:production",
      "destination": {
        "type": "s3",
        "bucket": "my-datadog-logs-archive",
        "path": "/logs",
        "region": "us-east-1",
        "integration": {
          "account_id": "123456789012",
          "role_name": "DatadogLogsArchiveRole"
        }
      },
      "rehydration_max_scan_size_in_gb": 100,
      "rehydration_tags": ["team:platform", "archived:true"]
    }
  }
}
```

### Rehydrate Archived Logs

1. Go to Logs > Configuration > Rehydrate from Archives
2. Select archive and time range
3. Set rehydration query filter
4. Configure destination index
5. Submit rehydration request

## Index Configuration

### Create Index with Quotas

```json
{
  "name": "production-index",
  "filter": {
    "query": "env:production"
  },
  "daily_limit": 5000000000,
  "daily_limit_reset": {
    "reset_time": "14:00",
    "reset_utc_offset": "-05:00"
  },
  "exclusion_filters": [
    {
      "name": "Exclude debug logs",
      "filter": {
        "query": "level:debug"
      },
      "is_enabled": true
    },
    {
      "name": "Sample high-volume service",
      "filter": {
        "query": "service:high-volume-svc",
        "sample_rate": 0.1
      },
      "is_enabled": true
    }
  ],
  "retention_days": 15
}
```

## Best Practices

### Pipeline Design

1. **Limit processors**: Maximum 20 processors per pipeline
2. **Limit parsing rules**: Maximum 10 rules per Grok processor
3. **Use specific filters**: Narrow pipeline scope with precise queries
4. **Test with samples**: Always include sample logs in Grok parsers

### Log Size

1. **Keep logs under 25KB**: Larger logs are truncated
2. **Avoid logging large payloads**: Use references/IDs instead
3. **Structure JSON logs**: Easier to parse and query

### Cost Control

1. **Set daily quotas**: Prevent unexpected volume spikes
2. **Use exclusion filters**: Drop unnecessary logs before indexing
3. **Archive for compliance**: Use archives instead of long retention
4. **Sample high-volume logs**: Reduce storage for noisy sources

### Correlation

1. **Inject trace IDs**: Enable log-to-trace linking
2. **Use standard attributes**: Consistent querying across services
3. **Add service/env/version tags**: Match APM telemetry
