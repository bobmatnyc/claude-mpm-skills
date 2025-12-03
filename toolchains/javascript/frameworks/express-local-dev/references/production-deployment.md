# Production Deployment Strategies

> Comprehensive deployment guide for Express applications

## Deployment Architecture Patterns

### Single Server Deployment

**Use Case**: Small applications, MVP, development staging

```
┌─────────────────────────────────────┐
│     Load Balancer / NGINX           │
│     (SSL Termination)               │
└─────────────┬───────────────────────┘
              │
    ┌─────────▼─────────┐
    │   PM2 Cluster     │
    │  (4 instances)    │
    ├───────────────────┤
    │  Express App      │
    │  + MongoDB        │
    │  + Redis          │
    └───────────────────┘
```

**Implementation**:
```bash
# Install PM2
npm install -g pm2

# Start cluster
pm2 start ecosystem.config.js --env production

# Save PM2 config
pm2 save

# Auto-start on boot
pm2 startup
```

### Multi-Server Deployment

**Use Case**: Medium-high traffic, high availability required

```
              ┌────────────────┐
              │ Load Balancer  │
              │   (HAProxy)    │
              └───────┬────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
    ┌─────▼──────┐         ┌─────▼──────┐
    │  Server 1  │         │  Server 2  │
    │ PM2 Cluster│         │ PM2 Cluster│
    │(4 instances)│         │(4 instances)│
    └─────┬──────┘         └─────┬──────┘
          │                       │
          └───────────┬───────────┘
                      │
         ┌────────────▼────────────┐
         │  Shared Services        │
         ├─────────────────────────┤
         │  PostgreSQL (Primary)   │
         │  PostgreSQL (Replica)   │
         │  Redis (Sentinel)       │
         └─────────────────────────┘
```

### Microservices Architecture

**Use Case**: Large applications, team scalability

```
                    ┌──────────────┐
                    │ API Gateway  │
                    │   (Kong)     │
                    └──────┬───────┘
                           │
     ┌─────────────────────┼─────────────────────┐
     │                     │                     │
┌────▼─────┐      ┌───────▼──────┐     ┌───────▼──────┐
│  Auth    │      │    Users     │     │   Posts      │
│ Service  │      │   Service    │     │  Service     │
│ (Express)│      │  (Express)   │     │ (Express)    │
└──────────┘      └──────────────┘     └──────────────┘
     │                   │                     │
     └───────────────────┼─────────────────────┘
                         │
              ┌──────────▼───────────┐
              │  Message Queue       │
              │  (RabbitMQ/Redis)    │
              └──────────────────────┘
```

## Container Deployment

### Docker Configuration

**Multi-Stage Dockerfile**:
```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source
COPY . .

# Production stage
FROM node:18-alpine

# Security: Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy from builder
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Start application
CMD ["node", "src/server.js"]
```

**healthcheck.js**:
```javascript
const http = require('http');

const options = {
  host: 'localhost',
  port: process.env.PORT || 3000,
  path: '/health',
  timeout: 2000
};

const healthCheck = http.request(options, (res) => {
  if (res.statusCode === 200) {
    process.exit(0);
  } else {
    process.exit(1);
  }
});

healthCheck.on('error', () => {
  process.exit(1);
});

healthCheck.end();
```

### Docker Compose (Development/Staging)

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      target: builder
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

## Kubernetes Deployment

### Deployment Manifest

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: express-app
  labels:
    app: express-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: express-app
  template:
    metadata:
      labels:
        app: express-app
    spec:
      containers:
      - name: express-app
        image: myregistry/express-app:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: express-app-service
spec:
  selector:
    app: express-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer

---
# hpa.yaml (Horizontal Pod Autoscaler)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: express-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: express-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### ConfigMap and Secrets

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  redis-url: "redis://redis-service:6379"
  log-level: "info"

---
# secrets.yaml (base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  database-url: <base64-encoded-url>
  jwt-secret: <base64-encoded-secret>
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Run security audit
        run: npm audit --production

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ secrets.DOCKER_REGISTRY }}
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_REGISTRY }}/express-app:latest
            ${{ secrets.DOCKER_REGISTRY }}/express-app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
            k8s/hpa.yaml
          images: |
            ${{ secrets.DOCKER_REGISTRY }}/express-app:${{ github.sha }}
          kubectl-version: 'latest'
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

test:
  stage: test
  image: node:18-alpine
  before_script:
    - npm ci
  script:
    - npm run lint
    - npm test
    - npm audit --production
  cache:
    paths:
      - node_modules/

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/express-app express-app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - kubectl rollout status deployment/express-app
  only:
    - main
```

## Blue-Green Deployment

### Strategy

```yaml
# blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: express-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: express-app
      version: blue
  template:
    metadata:
      labels:
        app: express-app
        version: blue
    spec:
      containers:
      - name: express-app
        image: myregistry/express-app:v1.0.0

---
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: express-app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: express-app
      version: green
  template:
    metadata:
      labels:
        app: express-app
        version: green
    spec:
      containers:
      - name: express-app
        image: myregistry/express-app:v2.0.0

---
# service.yaml (switch by changing selector)
apiVersion: v1
kind: Service
metadata:
  name: express-app-service
spec:
  selector:
    app: express-app
    version: blue  # Change to 'green' for deployment
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
```

### Deployment Script

```bash
#!/bin/bash
# deploy-blue-green.sh

CURRENT_COLOR=$(kubectl get svc express-app-service -o jsonpath='{.spec.selector.version}')
NEW_COLOR="green"

if [ "$CURRENT_COLOR" = "green" ]; then
  NEW_COLOR="blue"
fi

echo "Current: $CURRENT_COLOR, Deploying: $NEW_COLOR"

# Deploy new version
kubectl apply -f ${NEW_COLOR}-deployment.yaml

# Wait for deployment
kubectl rollout status deployment/express-app-${NEW_COLOR}

# Run smoke tests
./smoke-tests.sh http://express-app-${NEW_COLOR}:3000

if [ $? -eq 0 ]; then
  echo "Smoke tests passed, switching traffic"

  # Switch service to new version
  kubectl patch svc express-app-service -p "{\"spec\":{\"selector\":{\"version\":\"${NEW_COLOR}\"}}}"

  echo "Deployment complete. Old version ($CURRENT_COLOR) still running for rollback."
else
  echo "Smoke tests failed, keeping current version"
  exit 1
fi
```

## Monitoring and Observability

### Prometheus Metrics

```javascript
// middleware/metrics.js
const promClient = require('prom-client');

// Register default metrics
const register = new promClient.Registry();
promClient.collectDefaultMetrics({ register });

// Custom metrics
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

const httpRequestTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

exports.metricsMiddleware = (req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route?.path || req.path;

    httpRequestDuration
      .labels(req.method, route, res.statusCode)
      .observe(duration);

    httpRequestTotal
      .labels(req.method, route, res.statusCode)
      .inc();
  });

  next();
};

// Metrics endpoint
exports.metricsEndpoint = async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
};
```

### Application Performance Monitoring (APM)

```javascript
// apm.js (New Relic example)
require('newrelic');

// Or Datadog
const tracer = require('dd-trace').init({
  service: 'express-app',
  env: process.env.NODE_ENV
});

// Or Elastic APM
const apm = require('elastic-apm-node').start({
  serviceName: 'express-app',
  serverUrl: process.env.APM_SERVER_URL
});
```

## Zero-Downtime Deployment Checklist

- [ ] Implement health checks (liveness + readiness)
- [ ] Configure graceful shutdown (SIGTERM handling)
- [ ] Use rolling updates (not recreate)
- [ ] Set appropriate readiness probe delays
- [ ] Implement database migration strategy
- [ ] Use feature flags for breaking changes
- [ ] Configure proper resource requests/limits
- [ ] Test rollback procedure
- [ ] Monitor metrics during deployment
- [ ] Have rollback plan ready

## Database Migration Strategy

### Migrate-then-Deploy

```javascript
// migrations/20250101_add_user_fields.js
exports.up = async (db) => {
  // Add new column (backward compatible)
  await db.schema.table('users', (table) => {
    table.string('phone_number').nullable();
  });
};

exports.down = async (db) => {
  await db.schema.table('users', (table) => {
    table.dropColumn('phone_number');
  });
};
```

**Deployment Process**:
1. Run migration (add nullable column)
2. Deploy new code (uses new column)
3. Backfill data
4. Make column non-nullable (if needed)

### Pre-Deployment Script

```bash
#!/bin/bash
# pre-deploy.sh

# Run migrations
npm run migrate:up

# Verify migration
if [ $? -ne 0 ]; then
  echo "Migration failed"
  exit 1
fi

# Continue with deployment
```

## Performance Optimization

### NGINX Configuration

```nginx
# /etc/nginx/nginx.conf
upstream express_app {
    least_conn;
    server 127.0.0.1:3000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3002 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3003 max_fails=3 fail_timeout=30s;
    keepalive 64;
}

server {
    listen 80;
    server_name example.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API proxy
    location / {
        proxy_pass http://express_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## Disaster Recovery

### Backup Strategy

```bash
#!/bin/bash
# backup.sh

# Database backup
pg_dump -U user -h localhost myapp > backup_$(date +%Y%m%d_%H%M%S).sql

# Upload to S3
aws s3 cp backup_*.sql s3://mybucket/backups/

# Retain only last 30 days
find /backups -name "backup_*.sql" -mtime +30 -delete
```

### Restore Procedure

```bash
#!/bin/bash
# restore.sh

# Download from S3
aws s3 cp s3://mybucket/backups/backup_20250101_120000.sql .

# Restore database
psql -U user -h localhost myapp < backup_20250101_120000.sql
```

## Related Resources

- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [PM2 Production Guide](https://pm2.keymetrics.io/docs/usage/deployment/)
- [NGINX Optimization](https://nginx.org/en/docs/)
