# Performance Monitoring

Comprehensive guide to measuring, tracking, and maintaining web performance over time.

---

## Table of Contents

1. [Lighthouse CI Setup](#lighthouse-ci-setup)
2. [Real User Monitoring (RUM)](#real-user-monitoring-rum)
3. [Backend Monitoring](#backend-monitoring)
4. [Performance Budgets](#performance-budgets)
5. [Debugging Tools](#debugging-tools)

---

## Lighthouse CI Setup

**Continuous performance testing in CI/CD pipeline**

### Installation

```bash
# Install Lighthouse CI
npm install --save-dev @lhci/cli

# Initialize configuration
npx lhci init
```

### Configuration

**lighthouserc.json:**

```json
{
    "ci": {
        "collect": {
            "numberOfRuns": 3,
            "startServerCommand": "npm run serve",
            "url": [
                "http://localhost:3000/",
                "http://localhost:3000/about",
                "http://localhost:3000/products"
            ]
        },
        "assert": {
            "assertions": {
                "categories:performance": ["error", {"minScore": 0.9}],
                "categories:accessibility": ["warn", {"minScore": 0.9}],
                "first-contentful-paint": ["error", {"maxNumericValue": 2000}],
                "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
                "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
                "total-blocking-time": ["error", {"maxNumericValue": 300}],
                "interactive": ["error", {"maxNumericValue": 3500}]
            }
        },
        "upload": {
            "target": "temporary-public-storage"
        }
    }
}
```

### GitHub Actions Integration

**.github/workflows/lighthouse.yml:**

```yaml
name: Lighthouse CI
on: [push, pull_request]

jobs:
    lighthouse:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v3

            - name: Setup Node.js
              uses: actions/setup-node@v3
              with:
                  node-version: '18'

            - name: Install dependencies
              run: npm ci

            - name: Build
              run: npm run build

            - name: Run Lighthouse CI
              uses: treosh/lighthouse-ci-action@v10
              with:
                  urls: |
                      http://localhost:3000
                      http://localhost:3000/about
                  uploadArtifacts: true
                  temporaryPublicStorage: true

            - name: Comment PR with results
              uses: actions/github-script@v6
              with:
                  github-token: ${{secrets.GITHUB_TOKEN}}
                  script: |
                      // Post Lighthouse results as PR comment
```

### GitLab CI Integration

**.gitlab-ci.yml:**

```yaml
lighthouse:
    image: node:18
    stage: test
    script:
        - npm ci
        - npm run build
        - npm install -g @lhci/cli@0.12.x
        - lhci autorun --collect.numberOfRuns=3
    artifacts:
        paths:
            - .lighthouseci/
        expire_in: 1 week
```

### Local Usage

```bash
# Run Lighthouse CI locally
npx lhci autorun

# Run specific URL
npx lhci collect --url=http://localhost:3000

# Assert against budgets
npx lhci assert
```

**Impact:** Catch performance regressions before deployment

---

## Real User Monitoring (RUM)

**Measure actual user experience in production**

### web-vitals Library Setup

```bash
npm install web-vitals
```

### Implementation

```javascript
// analytics.js
import { onCLS, onFCP, onINP, onLCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
    const body = JSON.stringify({
        name: metric.name,
        value: metric.value,
        rating: metric.rating,
        delta: metric.delta,
        id: metric.id,
        navigationType: metric.navigationType,
        // Custom context
        path: window.location.pathname,
        userAgent: navigator.userAgent,
        connectionType: navigator.connection?.effectiveType,
    });

    // Send via Beacon API (survives page unload)
    if (navigator.sendBeacon) {
        navigator.sendBeacon('/analytics', body);
    } else {
        // Fallback to fetch
        fetch('/analytics', {
            body,
            method: 'POST',
            keepalive: true,
        });
    }
}

// Measure all Core Web Vitals
onCLS(sendToAnalytics);
onFCP(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

### Analytics Integration

**Google Analytics 4:**

```javascript
import { onCLS, onFCP, onINP, onLCP, onTTFB } from 'web-vitals';

function sendToGoogleAnalytics(metric) {
    gtag('event', metric.name, {
        event_category: 'Web Vitals',
        value: Math.round(metric.value),
        event_label: metric.id,
        non_interaction: true,
    });
}

onCLS(sendToGoogleAnalytics);
onFCP(sendToGoogleAnalytics);
onINP(sendToGoogleAnalytics);
onLCP(sendToGoogleAnalytics);
onTTFB(sendToGoogleAnalytics);
```

**Vercel Analytics:**

```javascript
import { Analytics } from '@vercel/analytics/react';

export default function App() {
    return (
        <>
            <YourApp />
            <Analytics />  {/* Automatic Web Vitals tracking */}
        </>
    );
}
```

**Custom Backend:**

```javascript
// server.js (Express)
app.post('/analytics', express.json(), (req, res) => {
    const { name, value, rating, path, userAgent } = req.body;

    // Store in database
    db.metrics.insert({
        metric_name: name,
        value: value,
        rating: rating,
        page_path: path,
        user_agent: userAgent,
        timestamp: new Date(),
    });

    res.sendStatus(200);
});
```

### Attribution Data

**Get detailed context about metrics:**

```javascript
import { onLCP } from 'web-vitals/attribution';

onLCP((metric) => {
    console.log('LCP:', metric.value);
    console.log('Attribution:', metric.attribution);
    console.log('LCP element:', metric.attribution.element);
    console.log('LCP resource URL:', metric.attribution.url);
    console.log('TTFB:', metric.attribution.timeToFirstByte);
    console.log('Resource load time:', metric.attribution.resourceLoadTime);
    console.log('Render time:', metric.attribution.renderTime);
});
```

**Impact:** Understand root causes of poor performance

---

## Backend Monitoring

**Monitor server-side performance (critical for TTFB)**

### Application Performance Monitoring (APM)

**New Relic:**

```javascript
// newrelic.js
'use strict';

exports.config = {
    app_name: ['Your App'],
    license_key: 'your_license_key',
    logging: {
        level: 'info',
    },
    distributed_tracing: {
        enabled: true,
    },
};

// app.js
require('newrelic');
const express = require('express');
// ... rest of your app
```

**Datadog:**

```javascript
// tracer.js
const tracer = require('dd-trace').init({
    logInjection: true,
    analytics: true,
});

// app.js
require('./tracer');
const express = require('express');
// ... rest of your app
```

**Sentry Performance:**

```javascript
const Sentry = require('@sentry/node');

Sentry.init({
    dsn: 'your_dsn',
    tracesSampleRate: 0.1,  // Sample 10% of transactions
    integrations: [
        new Sentry.Integrations.Http({ tracing: true }),
        new Sentry.Integrations.Express({ app }),
    ],
});

app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.tracingHandler());

// ... routes

app.use(Sentry.Handlers.errorHandler());
```

---

### Database Query Monitoring

**PostgreSQL slow query log:**

```sql
-- Enable slow query log (queries >100ms)
ALTER SYSTEM SET log_min_duration_statement = 100;
SELECT pg_reload_conf();

-- View slow queries
SELECT
    query,
    mean_exec_time,
    calls,
    total_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC
LIMIT 10;
```

**MySQL slow query log:**

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.1;  -- 100ms
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow-query.log';

-- Analyze slow queries
SELECT * FROM mysql.slow_log
WHERE query_time > 0.1
ORDER BY query_time DESC
LIMIT 10;
```

---

### Cache Monitoring

**Redis monitoring:**

```bash
# Monitor cache hit/miss ratio
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses"

# Real-time monitoring
redis-cli MONITOR
```

**Application-level cache monitoring:**

```javascript
// cache-monitor.js
class CacheMonitor {
    constructor() {
        this.hits = 0;
        this.misses = 0;
    }

    recordHit() {
        this.hits++;
    }

    recordMiss() {
        this.misses++;
    }

    getHitRate() {
        const total = this.hits + this.misses;
        return total > 0 ? (this.hits / total) * 100 : 0;
    }

    getStats() {
        return {
            hits: this.hits,
            misses: this.misses,
            hitRate: this.getHitRate(),
        };
    }
}

const cacheMonitor = new CacheMonitor();

function getFromCache(key) {
    const cached = redis.get(key);
    if (cached) {
        cacheMonitor.recordHit();
        return cached;
    }
    cacheMonitor.recordMiss();
    return null;
}

// Expose metrics endpoint
app.get('/metrics/cache', (req, res) => {
    res.json(cacheMonitor.getStats());
});
```

---

### Server Response Time Tracking

**Express middleware:**

```javascript
const responseTime = require('response-time');

app.use(responseTime((req, res, time) => {
    // Log slow requests (>1000ms)
    if (time > 1000) {
        console.log({
            method: req.method,
            url: req.url,
            responseTime: time,
            timestamp: new Date(),
        });
    }

    // Send to metrics backend
    metrics.record('http_request_duration', time, {
        method: req.method,
        path: req.path,
        status: res.statusCode,
    });
}));
```

---

### Infrastructure Monitoring

**CloudWatch (AWS):**

```javascript
const AWS = require('aws-sdk');
const cloudwatch = new AWS.CloudWatch();

function publishMetric(metricName, value) {
    const params = {
        Namespace: 'YourApp',
        MetricData: [
            {
                MetricName: metricName,
                Value: value,
                Unit: 'Milliseconds',
                Timestamp: new Date(),
            },
        ],
    };

    cloudwatch.putMetricData(params, (err, data) => {
        if (err) console.error(err);
    });
}

// Track TTFB
app.use((req, res, next) => {
    const start = Date.now();
    res.on('finish', () => {
        const duration = Date.now() - start;
        publishMetric('ResponseTime', duration);
    });
    next();
});
```

**Google Cloud Monitoring:**

```javascript
const { Monitoring } = require('@google-cloud/monitoring');
const client = new Monitoring.MetricServiceClient();

async function writeMetric(metricType, value) {
    const projectId = 'your-project-id';
    const dataPoint = {
        interval: {
            endTime: {
                seconds: Date.now() / 1000,
            },
        },
        value: {
            doubleValue: value,
        },
    };

    const timeSeriesData = {
        metric: {
            type: `custom.googleapis.com/${metricType}`,
        },
        resource: {
            type: 'global',
        },
        points: [dataPoint],
    };

    const request = {
        name: client.projectPath(projectId),
        timeSeries: [timeSeriesData],
    };

    await client.createTimeSeries(request);
}
```

---

## Performance Budgets

**Define and enforce performance limits**

### webpack-bundle-analyzer

```bash
npm install --save-dev webpack-bundle-analyzer

# package.json
{
    "scripts": {
        "analyze": "webpack-bundle-analyzer build/stats.json"
    }
}
```

### Performance Budget Configuration

**webpack.config.js:**

```javascript
module.exports = {
    performance: {
        maxAssetSize: 250000,  // 250KB
        maxEntrypointSize: 250000,
        hints: 'error',  // Fail build if exceeded
    },
};
```

**lighthouserc.json budgets:**

```json
{
    "ci": {
        "assert": {
            "budgets": [
                {
                    "path": "/*",
                    "resourceSizes": [
                        {
                            "resourceType": "script",
                            "budget": 300
                        },
                        {
                            "resourceType": "stylesheet",
                            "budget": 50
                        },
                        {
                            "resourceType": "image",
                            "budget": 500
                        },
                        {
                            "resourceType": "total",
                            "budget": 1000
                        }
                    ],
                    "timings": [
                        {
                            "metric": "first-contentful-paint",
                            "budget": 2000
                        },
                        {
                            "metric": "largest-contentful-paint",
                            "budget": 2500
                        },
                        {
                            "metric": "interactive",
                            "budget": 3500
                        }
                    ]
                }
            ]
        }
    }
}
```

---

## Debugging Tools

### Chrome DevTools

**Performance Panel:**
1. Open DevTools (F12)
2. Go to Performance panel
3. Click Record (Cmd+E)
4. Reload page
5. Stop recording
6. Analyze timeline

**What to look for:**
- Long tasks (>50ms) in Main section
- Layout shifts in Experience section
- Network waterfall
- JavaScript execution time

**Coverage Tool:**
1. Open DevTools
2. Cmd+Shift+P → "Show Coverage"
3. Click Record
4. Reload page
5. See unused CSS/JS (red = unused)

---

### WebPageTest

**URL:** https://www.webpagetest.org

**Features:**
- Test from multiple locations
- Connection speed simulation (3G, 4G, Cable)
- Filmstrip view
- Waterfall chart
- Video comparison
- Advanced metrics

**API usage:**

```bash
# Run test via API
curl "https://www.webpagetest.org/runtest.php?url=https://example.com&k=YOUR_API_KEY&f=json"
```

---

### PageSpeed Insights

**URL:** https://pagespeed.web.dev

**Features:**
- Real user data (CrUX - Chrome User Experience Report)
- Lab data (Lighthouse)
- Field vs lab comparison
- Mobile vs desktop
- Core Web Vitals status

**API usage:**

```javascript
const fetch = require('node-fetch');

async function getPageSpeedInsights(url) {
    const apiKey = 'YOUR_API_KEY';
    const apiUrl = `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${url}&key=${apiKey}`;

    const response = await fetch(apiUrl);
    const data = await response.json();

    return {
        fcp: data.lighthouseResult.audits['first-contentful-paint'].numericValue,
        lcp: data.lighthouseResult.audits['largest-contentful-paint'].numericValue,
        cls: data.lighthouseResult.audits['cumulative-layout-shift'].numericValue,
        tbt: data.lighthouseResult.audits['total-blocking-time'].numericValue,
    };
}
```

---

### Custom Performance Dashboard

**Simple monitoring dashboard:**

```javascript
// dashboard.js - Backend
const express = require('express');
const app = express();

// Store metrics in memory (use Redis/DB in production)
const metrics = [];

app.post('/analytics', express.json(), (req, res) => {
    metrics.push({
        ...req.body,
        timestamp: new Date(),
    });
    res.sendStatus(200);
});

app.get('/dashboard', (req, res) => {
    const last24h = metrics.filter(m =>
        new Date(m.timestamp) > new Date(Date.now() - 24 * 60 * 60 * 1000)
    );

    const stats = {
        lcp: calculateP75(last24h.filter(m => m.name === 'LCP')),
        cls: calculateP75(last24h.filter(m => m.name === 'CLS')),
        inp: calculateP75(last24h.filter(m => m.name === 'INP')),
    };

    res.json(stats);
});

function calculateP75(values) {
    const sorted = values.map(v => v.value).sort((a, b) => a - b);
    const index = Math.floor(sorted.length * 0.75);
    return sorted[index] || 0;
}

app.listen(3000);
```

---

## Monitoring Checklist

### CI/CD
- [ ] Lighthouse CI running on every PR
- [ ] Performance budgets enforced
- [ ] Bundle size tracked
- [ ] Regression alerts configured

### Real User Monitoring
- [ ] web-vitals library integrated
- [ ] Core Web Vitals tracked in analytics
- [ ] Attribution data collected
- [ ] Slow page alerts configured

### Backend Monitoring
- [ ] APM tool installed (New Relic, Datadog, Sentry)
- [ ] Slow query logging enabled
- [ ] Cache hit/miss tracking
- [ ] Server response time monitoring
- [ ] Infrastructure metrics (CPU, memory, disk)

### Debugging
- [ ] Chrome DevTools performance traces collected
- [ ] WebPageTest used for detailed analysis
- [ ] PageSpeed Insights checked regularly
- [ ] Coverage tool used to identify unused code

### Dashboards
- [ ] Performance dashboard created
- [ ] Metrics visualized (Grafana, Datadog, custom)
- [ ] Alerts configured for regressions
- [ ] Weekly performance reports automated

---

**Target Metrics:**
- **TTFB:** <800ms (backend monitoring critical)
- **LCP:** <2.5s (RUM + Lighthouse CI)
- **CLS:** <0.1 (RUM + Layout Shift tracking)
- **INP:** <200ms (RUM + interaction logging)
- **Bundle Size:** <250KB (webpack budgets)
- **Cache Hit Ratio:** >80% (Redis monitoring)

---

**Next:** See [core-web-vitals.md](core-web-vitals.md) for metric optimization strategies.
