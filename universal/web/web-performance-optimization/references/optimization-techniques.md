# Performance Optimization Techniques

Comprehensive guide to web performance optimization techniques across backend, frontend, and infrastructure.

---

## Table of Contents

1. [Backend Optimization](#backend-optimization) - CRITICAL FOR TTFB
2. [Image Optimization](#image-optimization)
3. [JavaScript Optimization](#javascript-optimization)
4. [CSS Optimization](#css-optimization)
5. [Resource Loading Optimization](#resource-loading-optimization)
6. [Caching Strategies](#caching-strategies)

---

## Backend Optimization

**Critical for:** TTFB (Time to First Byte) optimization

**Target:** TTFB <800ms (Good), <1800ms (Acceptable)

### Diagnostic Workflow

#### Step 1: Measure TTFB Components

Use curl to break down TTFB into phases:

```bash
# Create curl timing format file
cat > curl-format.txt << 'EOF'
time_namelookup:    %{time_namelookup}s\n
time_connect:       %{time_connect}s\n
time_appconnect:    %{time_appconnect}s\n
time_pretransfer:   %{time_pretransfer}s\n
time_starttransfer: %{time_starttransfer}s (TTFB)\n
time_total:         %{time_total}s\n
EOF

# Measure TTFB
curl -w "@curl-format.txt" -o /dev/null -s https://yoursite.com
```

**Interpretation:**
- `time_namelookup` >100ms: DNS is slow → Switch DNS provider or use CDN
- `time_connect - time_namelookup` >100ms: TCP connection is slow → Enable Keep-Alive
- `time_appconnect - time_connect` >200ms: TLS handshake is slow → Enable TLS 1.3
- `time_starttransfer - time_pretransfer` >500ms: **Server processing is slow** ← Most common

#### Step 2: Profile Backend (If Server Processing is Slow)

**Use Application Performance Monitoring (APM) tools:**
- New Relic
- Datadog
- Sentry Performance
- AWS X-Ray (for AWS services)
- Google Cloud Profiler

**What to look for:**
- Slow database queries (>100ms)
- N+1 query problems
- Missing database indexes
- Cache miss ratios
- External API call latency
- Cold start penalties (serverless)

#### Step 3: Optimize Bottleneck

---

### Database Query Optimization

#### Problem 1: N+1 Query Problem

**Symptom:** Making 1 query to fetch parent records, then N queries to fetch related data

**Python (Django ORM) Example:**

```python
# ❌ BAD: N+1 query problem
posts = Post.objects.all()  # 1 query
for post in posts:
    print(post.author.name)  # N queries (one per post)
    print(post.category.name)  # Another N queries

# Query count: 1 + N + N = 1 + 2N queries for N posts
# For 100 posts: 201 queries! (Execution time: ~2000ms)

# ✅ GOOD: Use select_related() for foreign keys
posts = Post.objects.select_related('author', 'category').all()  # 1 query with JOIN
for post in posts:
    print(post.author.name)  # No additional query
    print(post.category.name)  # No additional query

# Query count: 1 query for 100 posts (Execution time: ~50ms)
# Performance improvement: 40x faster

# ✅ ALSO GOOD: Use prefetch_related() for many-to-many
posts = Post.objects.prefetch_related('tags').all()  # 2 queries total
for post in posts:
    print([tag.name for tag in post.tags.all()])  # No additional queries
```

**Node.js (Sequelize) Example:**

```javascript
// ❌ BAD: N+1 query problem
const posts = await Post.findAll();
for (const post of posts) {
  const author = await post.getAuthor();  // N queries
  console.log(author.name);
}

// ✅ GOOD: Use include to eager load
const posts = await Post.findAll({
  include: [{
    model: Author,
    attributes: ['name']
  }]
});
for (const post of posts) {
  console.log(post.Author.name);  // No additional query
}
```

**Ruby (Rails) Example:**

```ruby
# ❌ BAD: N+1 query problem
posts = Post.all
posts.each do |post|
  puts post.author.name  # N queries
end

# ✅ GOOD: Use includes to eager load
posts = Post.includes(:author)
posts.each do |post|
  puts post.author.name  # No additional query
end
```

**Impact:** 10-100x faster (depends on number of records)

---

#### Problem 2: Missing Database Indexes

**Symptom:** Slow queries doing full table scans instead of index lookups

**Identify missing indexes:**

```sql
-- PostgreSQL: Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100  -- Queries slower than 100ms
ORDER BY mean_exec_time DESC
LIMIT 10;

-- MySQL: Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.1;  -- Log queries >100ms
```

**Analyze query execution plan:**

```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 123 AND created_at > '2025-01-01';

-- Output shows "Seq Scan" (full table scan) = BAD
-- Want to see "Index Scan" = GOOD
```

**Add appropriate indexes:**

```sql
-- ❌ BAD: No index, full table scan
-- Query time: 2300ms for 1M rows

-- ✅ GOOD: Composite index for common query pattern
CREATE INDEX idx_orders_user_created
ON orders(user_id, created_at);

-- Query time: 15ms (153x faster!)

-- For filtering and sorting
CREATE INDEX idx_orders_status_created
ON orders(status, created_at DESC);

-- For covering index (all needed columns in index)
CREATE INDEX idx_orders_covering
ON orders(user_id, status)
INCLUDE (created_at, total);  -- PostgreSQL 11+
```

**Index best practices:**

1. **Index columns used in WHERE clauses:**
   ```sql
   -- Query: WHERE user_id = ? AND status = ?
   CREATE INDEX idx_user_status ON orders(user_id, status);
   ```

2. **Index foreign keys:**
   ```sql
   -- Always index foreign key columns
   CREATE INDEX idx_orders_user_id ON orders(user_id);
   ```

3. **Composite index order matters:**
   ```sql
   -- Query: WHERE user_id = ? AND created_at > ?
   -- CORRECT: user_id first (equality), then created_at (range)
   CREATE INDEX idx_user_created ON orders(user_id, created_at);

   -- WRONG: created_at first makes user_id filter less efficient
   CREATE INDEX idx_created_user ON orders(created_at, user_id);
   ```

4. **Don't over-index:**
   - Each index slows down INSERT/UPDATE/DELETE
   - Maximum 5-7 indexes per table
   - Monitor index usage and remove unused indexes

**Impact:** 10-1000x faster (depends on table size)

---

#### Problem 3: Fetching Too Much Data

**Symptom:** Fetching all columns when only a few are needed

```python
# ❌ BAD: Fetching all columns (including large text/blob fields)
users = User.objects.all()
# Fetches: id, email, name, bio (TEXT), avatar (BLOB), created_at, etc.
# Query size: 50KB for 100 users

for user in users:
    print(f"{user.name}: {user.email}")

# ✅ GOOD: Only fetch needed columns
users = User.objects.only('id', 'name', 'email')
# Query size: 5KB for 100 users (10x smaller)
# Query time: 70% faster

for user in users:
    print(f"{user.name}: {user.email}")

# ✅ ALSO GOOD: Use values() for even better performance
users = User.objects.values('id', 'name', 'email')
# Returns list of dicts instead of model instances
# Query time: 80% faster than fetching all columns
```

**SQL optimization:**

```sql
-- ❌ BAD: SELECT * fetches unnecessary data
SELECT * FROM users WHERE status = 'active';

-- ✅ GOOD: Only select needed columns
SELECT id, name, email FROM users WHERE status = 'active';
```

**Impact:** 50-80% faster for queries with large text/blob columns

---

#### Problem 4: Slow Aggregations

**Symptom:** Aggregating large datasets without optimization

```sql
-- ❌ BAD: Aggregating without index
SELECT user_id, COUNT(*) as order_count
FROM orders
WHERE created_at > '2025-01-01'
GROUP BY user_id;
-- Query time: 3000ms for 1M rows

-- ✅ GOOD: Add index on aggregation columns
CREATE INDEX idx_orders_created_user
ON orders(created_at, user_id);
-- Query time: 150ms (20x faster)

-- ✅ BETTER: Precompute aggregations (materialized view)
CREATE MATERIALIZED VIEW user_order_stats AS
SELECT
  user_id,
  COUNT(*) as order_count,
  SUM(total) as total_spent,
  MAX(created_at) as last_order_date
FROM orders
GROUP BY user_id;

-- Refresh periodically (e.g., hourly)
REFRESH MATERIALIZED VIEW user_order_stats;

-- Query the materialized view (1-2ms)
SELECT * FROM user_order_stats WHERE user_id = 123;
```

**Impact:** 20-100x faster for complex aggregations

---

### Server-Side Caching (Redis/Memcached)

**When to use caching:**
- Data that's read frequently but changes infrequently
- Expensive computations (e.g., aggregations, ML predictions)
- External API responses
- Session data
- Rate limiting counters

#### Redis Setup

```bash
# Install Redis
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
redis-server

# Test connection
redis-cli ping  # Should return "PONG"
```

#### Pattern 1: Cache-Aside (Lazy Loading)

**Most common pattern: Check cache first, load from DB on miss**

**Python (Flask + Redis) Example:**

```python
import redis
import json
from flask import Flask, jsonify

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/api/user/<int:user_id>')
def get_user_profile(user_id):
    # Step 1: Check cache first
    cache_key = f"user_profile:{user_id}"
    cached = redis_client.get(cache_key)

    if cached:
        # Cache hit (1-2ms)
        print("Cache HIT")
        return jsonify(json.loads(cached))

    # Step 2: Cache miss - fetch from database
    print("Cache MISS - querying database")
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")  # 50-200ms

    # Step 3: Store in cache for 5 minutes
    redis_client.setex(cache_key, 300, json.dumps(user))

    return jsonify(user)

# Performance:
# - First request: 150ms (database query + cache write)
# - Subsequent requests: 2ms (cache hit)
# - 75x faster for cached requests
```

**Node.js (Express + Redis) Example:**

```javascript
const express = require('express');
const redis = require('redis');

const app = express();
const redisClient = redis.createClient();

app.get('/api/user/:userId', async (req, res) => {
  const userId = req.params.userId;
  const cacheKey = `user_profile:${userId}`;

  try {
    // Check cache
    const cached = await redisClient.get(cacheKey);
    if (cached) {
      console.log('Cache HIT');
      return res.json(JSON.parse(cached));
    }

    // Cache miss - query database
    console.log('Cache MISS');
    const user = await db.query('SELECT * FROM users WHERE id = ?', [userId]);

    // Cache for 5 minutes
    await redisClient.setEx(cacheKey, 300, JSON.stringify(user));

    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

**Cache invalidation (when data changes):**

```python
@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    # Update database
    db.update_user(user_id, request.json)

    # Invalidate cache
    cache_key = f"user_profile:{user_id}"
    redis_client.delete(cache_key)

    return jsonify({"status": "updated"})
```

**Impact:** 50-100x faster for frequently accessed data

---

#### Pattern 2: Write-Through Cache

**Write to cache and database simultaneously**

```python
def update_user_profile(user_id, data):
    # Write to database
    db.update_user(user_id, data)

    # Write to cache immediately
    cache_key = f"user_profile:{user_id}"
    redis_client.setex(cache_key, 300, json.dumps(data))

    return data
```

**Pros:** Cache is always up-to-date
**Cons:** Slower writes (two operations)

---

#### Pattern 3: Session Storage

**Use Redis for fast session storage**

**Python (Flask-Session):**

```python
from flask import Flask, session
from flask_session import Session
import redis

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379)
Session(app)

@app.route('/login', methods=['POST'])
def login():
    # Store session in Redis (not database)
    session['user_id'] = 123
    session['username'] = 'john'
    return jsonify({"status": "logged in"})

# Impact: 20x faster than database-backed sessions
```

**Node.js (connect-redis):**

```javascript
const session = require('express-session');
const RedisStore = require('connect-redis')(session);
const redisClient = require('redis').createClient();

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 86400000 }  // 24 hours
}));
```

**Impact:** 10-20x faster than database sessions

---

#### Pattern 4: Rate Limiting

**Use Redis to track API request counts**

```python
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379)

def rate_limit(limit=100, window=60):
    """
    Rate limiter: Allow `limit` requests per `window` seconds
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            # Get client IP
            client_ip = request.remote_addr
            key = f"rate_limit:{client_ip}"

            # Increment counter
            current = redis_client.incr(key)

            # Set expiration on first request
            if current == 1:
                redis_client.expire(key, window)

            # Check if over limit
            if current > limit:
                return jsonify({"error": "Rate limit exceeded"}), 429

            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/data')
@rate_limit(limit=100, window=60)  # 100 requests per minute
def get_data():
    return jsonify({"data": "..."})
```

**Impact:** Prevents abuse, protects backend from overload

---

### CDN Configuration

**Problem:** Every request hits your origin server, even for static assets

**Solution:** Configure CDN to cache static assets at edge locations

#### Nginx Cache Headers

```nginx
# /etc/nginx/sites-available/yoursite

server {
    listen 443 ssl http2;
    server_name yoursite.com;

    # Static assets: Aggressive caching (1 year)
    location ~* \.(jpg|jpeg|png|gif|webp|avif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
        add_header Vary "Accept";  # For content negotiation (WebP/AVIF)
    }

    location ~* \.(css|js)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";

        # Enable compression
        gzip on;
        gzip_types text/css application/javascript;
        brotli on;
        brotli_types text/css application/javascript;
    }

    # Fonts: Long cache (1 year) + CORS
    location ~* \.(woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
        add_header Access-Control-Allow-Origin "*";  # Allow cross-origin
    }

    # HTML: No cache (always check server)
    location ~* \.(html)$ {
        expires -1;
        add_header Cache-Control "no-cache, must-revalidate";
        add_header Pragma "no-cache";
    }

    # API responses: Short cache with stale-while-revalidate
    location /api/ {
        add_header Cache-Control "max-age=60, stale-while-revalidate=600";
        # Cached for 60s, serve stale for up to 10 minutes while revalidating

        proxy_pass http://backend;
    }
}
```

#### Apache Cache Headers

```apache
# .htaccess

# Enable caching
<IfModule mod_expires.c>
    ExpiresActive On

    # Images
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"

    # CSS and JavaScript
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"

    # Fonts
    ExpiresByType font/woff2 "access plus 1 year"
    ExpiresByType font/woff "access plus 1 year"

    # HTML (no cache)
    ExpiresByType text/html "access plus 0 seconds"
</IfModule>

<IfModule mod_headers.c>
    # Add Cache-Control headers
    <FilesMatch "\.(jpg|jpeg|png|gif|webp|avif|svg)$">
        Header set Cache-Control "max-age=31536000, public, immutable"
    </FilesMatch>

    <FilesMatch "\.(css|js)$">
        Header set Cache-Control "max-age=31536000, public, immutable"
    </FilesMatch>

    <FilesMatch "\.(html)$">
        Header set Cache-Control "no-cache, must-revalidate"
    </FilesMatch>
</IfModule>
```

#### Cloudflare Page Rules

```
# Cloudflare Dashboard → Page Rules

# Cache everything for static assets
Pattern: *.yoursite.com/static/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
  - Browser Cache TTL: 1 year

# Bypass cache for API
Pattern: *.yoursite.com/api/*
Settings:
  - Cache Level: Bypass
```

**Impact:**
- 90-95% reduction in origin requests
- 50-200ms faster for users (served from edge)
- Lower server costs (fewer origin hits)

---

### HTTP/2 and HTTP/3 Adoption

**Benefits:**
- Multiplexing: Multiple requests over single connection
- Header compression: Smaller overhead
- Server push: Proactively send assets
- Faster TLS handshake (HTTP/3 with QUIC)

#### Enable HTTP/2 (Nginx)

```nginx
server {
    listen 443 ssl http2;  # Enable HTTP/2
    server_name yoursite.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # HTTP/2 Server Push (optional, use sparingly)
    location = /index.html {
        http2_push /styles/critical.css;
        http2_push /js/app.js;
    }
}
```

#### Enable HTTP/3 (Nginx with QUIC)

```nginx
server {
    listen 443 ssl http2;
    listen 443 http3 reuseport;  # Enable HTTP/3

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Advertise HTTP/3 support
    add_header Alt-Svc 'h3=":443"; ma=86400';
}
```

**Impact:** 30-50% faster for multiple resources (especially on high-latency networks)

---

### Cold Start Mitigation (Serverless)

**Problem:** AWS Lambda, Google Cloud Functions, Azure Functions have 1-3s cold start penalty

#### Solution 1: Reuse Connections

```javascript
// ❌ BAD: Create new database connection on every invocation
exports.handler = async (event) => {
    const db = await connectToDatabase();  // 1-2s cold start penalty
    const result = await db.query('SELECT * FROM users');
    await db.close();
    return result;
};

// ✅ GOOD: Reuse connection across invocations
let db;

exports.handler = async (event) => {
    if (!db) {
        db = await connectToDatabase();  // Only on cold start
    }
    const result = await db.query('SELECT * FROM users');
    return result;
    // Don't close connection - reuse on next invocation
};
```

#### Solution 2: Provisioned Concurrency (AWS Lambda)

```yaml
# serverless.yml
functions:
  api:
    handler: handler.main
    provisionedConcurrency: 5  # Keep 5 warm instances
```

**Cost:** ~$15/month per warm instance
**Benefit:** Eliminates cold starts for most requests

#### Solution 3: Keep Functions Warm

```javascript
// Scheduled pinger (runs every 5 minutes)
exports.pinger = async () => {
    // Invoke main function to keep it warm
    await lambda.invoke({
        FunctionName: 'myFunction',
        InvocationType: 'RequestResponse'
    });
};
```

**Impact:** Eliminates 1-3s cold start penalty

---

### Compression

**Enable Brotli (better than gzip)**

#### Nginx with Brotli

```nginx
http {
    # Brotli compression (install nginx-module-brotli)
    brotli on;
    brotli_comp_level 6;  # 1-11, higher = better compression but slower
    brotli_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        image/svg+xml;

    # Fallback to gzip for older browsers
    gzip on;
    gzip_vary on;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript;
}
```

#### Express.js with Compression

```javascript
const compression = require('compression');
const express = require('express');

const app = express();

// Enable compression (gzip)
app.use(compression({
    level: 6,  // Compression level (1-9)
    threshold: 1024,  // Only compress responses > 1KB
    filter: (req, res) => {
        // Don't compress images (already compressed)
        if (req.headers['x-no-compression']) {
            return false;
        }
        return compression.filter(req, res);
    }
}));
```

**Compression ratios:**
- **Brotli:** 20-30% smaller than gzip
- **Gzip:** 70-80% size reduction

**Impact:** 20-30% smaller transfer size, 5-10% faster TTFB

---

### Connection Pooling

**Problem:** Creating new database connections is expensive (50-200ms per connection)

**Solution:** Reuse a pool of connections

#### PostgreSQL (Node.js with pg)

```javascript
const { Pool } = require('pg');

// ❌ BAD: Create new connection for each query
async function getUser(userId) {
    const client = new Client({ connectionString: '...' });
    await client.connect();  // 50-200ms connection overhead
    const result = await client.query('SELECT * FROM users WHERE id = $1', [userId]);
    await client.end();
    return result.rows[0];
}

// ✅ GOOD: Use connection pool
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    max: 20,  // Maximum 20 connections in pool
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
});

async function getUser(userId) {
    // Reuse connection from pool (1-2ms)
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
    return result.rows[0];
}
```

#### Python (SQLAlchemy)

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Connection pool
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=20,  # Keep 20 connections
    max_overflow=10,  # Allow 10 additional connections if needed
    pool_recycle=3600,  # Recycle connections after 1 hour
)

# Reuse connections
def get_user(user_id):
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM users WHERE id = %s", user_id)
        return result.fetchone()
```

**Impact:** 50-200ms faster per query (eliminates connection overhead)

---

### Verification Checklist

After implementing backend optimizations:

**TTFB Breakdown:**
```bash
# Before optimization
$ curl -w "@curl-format.txt" -o /dev/null -s https://yoursite.com
time_starttransfer: 3.67s (TTFB) ❌

# After optimization
$ curl -w "@curl-format.txt" -o /dev/null -s https://yoursite.com
time_starttransfer: 0.42s (TTFB) ✅
# 88% improvement!
```

**Database Performance:**
- [ ] No N+1 queries (check with ORM query logging)
- [ ] All foreign keys have indexes
- [ ] Slow query log enabled and monitored
- [ ] Only fetching needed columns

**Caching:**
- [ ] Redis/Memcached installed and configured
- [ ] Cache hit ratio >80% for frequently accessed data
- [ ] Cache invalidation strategy implemented

**Infrastructure:**
- [ ] CDN configured for static assets
- [ ] Cache-Control headers set correctly
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] Compression (Brotli or gzip) enabled

**Serverless (if applicable):**
- [ ] Database connections reused across invocations
- [ ] Provisioned concurrency for critical functions
- [ ] Cold start monitoring in place

---

## Image Optimization

**Critical for:** LCP (Largest Contentful Paint) and page weight reduction

### Modern Image Formats

**Format comparison:**

| Format | File Size | Browser Support | Use Case |
|--------|-----------|-----------------|----------|
| JPEG   | Baseline  | 100%           | Photos (fallback) |
| WebP   | 30% smaller | 97%          | Modern browsers |
| AVIF   | 50% smaller | 89%          | Cutting edge (best quality/size) |
| SVG    | Tiny      | 100%           | Logos, icons |

#### Converting to Modern Formats

```bash
# Install tools
# Ubuntu/Debian
sudo apt-get install webp imagemagick libavif-bin

# macOS
brew install webp imagemagick libavif

# Convert JPEG → WebP (30% smaller)
cwebp -q 85 hero.jpg -o hero.webp

# Convert JPEG → AVIF (50% smaller than JPEG)
avifenc -s 5 hero.jpg hero.avif

# Batch conversion
for img in *.jpg; do
    cwebp -q 85 "$img" -o "${img%.jpg}.webp"
    avifenc -s 5 "$img" "${img%.jpg}.avif"
done

# ImageMagick (alternative)
magick hero.jpg -quality 85 hero.webp
magick hero.jpg -quality 85 hero.avif
```

#### Serving Modern Formats with `<picture>`

```html
<picture>
  <!-- Serve AVIF to browsers that support it (50% smaller) -->
  <source srcset="hero.avif" type="image/avif">

  <!-- Fallback to WebP for other modern browsers (30% smaller) -->
  <source srcset="hero.webp" type="image/webp">

  <!-- Fallback to JPEG for older browsers -->
  <img src="hero.jpg" alt="Hero" width="1200" height="600">
</picture>
```

**Impact:** 30-50% smaller file size, faster LCP

---

### Responsive Images

**Problem:** Serving desktop-sized images to mobile devices wastes bandwidth

**Solution:** Use `srcset` and `sizes` attributes

```html
<!-- ❌ BAD: Same image for all screen sizes -->
<img src="hero-large.jpg" alt="Hero">
<!-- Mobile users download 2MB desktop image for 375px screen -->

<!-- ✅ GOOD: Responsive images with srcset -->
<img
    src="hero-800.jpg"
    srcset="
        hero-400.jpg 400w,
        hero-800.jpg 800w,
        hero-1200.jpg 1200w,
        hero-1600.jpg 1600w
    "
    sizes="
        (max-width: 600px) 400px,
        (max-width: 900px) 800px,
        (max-width: 1200px) 1200px,
        1600px
    "
    alt="Hero"
    width="1600"
    height="900"
>
<!-- Mobile users download only 400px image (150KB vs 2MB) -->
```

**Generate responsive images:**

```bash
# Generate multiple sizes
convert hero.jpg -resize 400x hero-400.jpg
convert hero.jpg -resize 800x hero-800.jpg
convert hero.jpg -resize 1200x hero-1200.jpg
convert hero.jpg -resize 1600x hero-1600.jpg

# Optimize each size
jpegoptim --strip-all --max=85 hero-*.jpg
```

**Impact:** 70-90% smaller downloads for mobile users

---

### Image Dimensions (Prevents CLS)

**Problem:** Images without dimensions cause layout shift

```html
<!-- ❌ BAD: No dimensions, causes CLS -->
<img src="hero.jpg" alt="Hero">
<!-- Page loads → Text appears → Image loads → Text shifts down → CLS! -->

<!-- ✅ GOOD: Explicit dimensions prevent CLS -->
<img src="hero.jpg" alt="Hero" width="1200" height="600">
<!-- Browser reserves space before image loads → No shift -->

<!-- ✅ BETTER: Responsive with aspect-ratio -->
<img src="hero.jpg" alt="Hero" style="aspect-ratio: 16/9; width: 100%;">
```

**CSS for responsive images with dimensions:**

```css
img {
    max-width: 100%;
    height: auto;
    /* aspect-ratio preserved from width/height attributes */
}
```

**Impact:** Reduces CLS by 50-80%

---

### Lazy Loading

**Load images only when needed**

```html
<!-- Images above fold: Eager loading -->
<img src="hero.jpg" alt="Hero" loading="eager" fetchpriority="high">

<!-- Images below fold: Lazy loading -->
<img src="content-1.jpg" alt="Content 1" loading="lazy">
<img src="content-2.jpg" alt="Content 2" loading="lazy">
```

**JavaScript lazy loading (for older browsers):**

```javascript
// Intersection Observer for lazy loading
const images = document.querySelectorAll('img[data-src]');

const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
            observer.unobserve(img);
        }
    });
});

images.forEach(img => imageObserver.observe(img));
```

**Impact:** 40-60% reduction in initial page weight

---

### Image Compression

**Optimize images without quality loss**

```bash
# JPEG optimization (lossless)
jpegoptim --strip-all hero.jpg
# Removes metadata, ~10% size reduction

# JPEG optimization (lossy, better compression)
jpegoptim --max=85 --strip-all hero.jpg
# Quality 85 is visually identical, ~30% size reduction

# PNG optimization (lossless)
optipng -o7 logo.png
# Maximum optimization, ~20% size reduction

# PNG → JPEG for photos (huge savings)
convert photo.png -quality 85 photo.jpg
# 80-90% size reduction for photos

# WebP optimization
cwebp -q 85 -m 6 -mt hero.jpg -o hero.webp
# -m 6: Maximum compression effort
# -mt: Multi-threading
```

**Automated optimization (build process):**

```json
{
    "scripts": {
        "optimize-images": "find ./public/images -type f \\( -name '*.jpg' -o -name '*.png' \\) -exec imageoptim {} \\;"
    }
}
```

**Impact:** 20-50% size reduction (lossless), 50-80% (lossy)

---

### CDN for Images

**Use image CDN for automatic optimization**

**Cloudinary example:**

```html
<!-- Original image URL -->
<img src="https://yoursite.com/images/hero.jpg" alt="Hero">

<!-- Cloudinary: Automatic format, compression, and resizing -->
<img src="https://res.cloudinary.com/yourcloud/image/upload/f_auto,q_auto,w_800/hero.jpg" alt="Hero">
<!-- f_auto: Automatic format (WebP/AVIF for modern browsers)
     q_auto: Automatic quality optimization
     w_800: Resize to 800px width -->
```

**imgix example:**

```html
<img src="https://yoursite.imgix.net/hero.jpg?auto=format,compress&w=800" alt="Hero">
```

**Benefits:**
- Automatic format conversion (WebP/AVIF)
- Automatic compression
- Responsive images via URL parameters
- Global CDN delivery

**Impact:** 50-70% smaller images, 100-300ms faster loading

---

## JavaScript Optimization

### Code Splitting

**Problem:** Loading entire app bundle upfront (500KB+) slows initial load

**Solution:** Split code by route or component

#### React with Lazy Loading

```javascript
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// ❌ BAD: Loading everything upfront
import Dashboard from './Dashboard';
import Settings from './Settings';
import Reports from './Reports';

// Initial bundle: 500KB (all routes included)

// ✅ GOOD: Route-based code splitting
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));
const Reports = lazy(() => import('./Reports'));

// Initial bundle: 100KB (only shell + current route)
// Other routes loaded on demand

function App() {
    return (
        <BrowserRouter>
            <Suspense fallback={<LoadingSpinner />}>
                <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/settings" element={<Settings />} />
                    <Route path="/reports" element={<Reports />} />
                </Routes>
            </Suspense>
        </BrowserRouter>
    );
}
```

#### Next.js (Automatic Code Splitting)

```javascript
// Next.js automatically code splits by route

// pages/dashboard.tsx - Loaded only when visiting /dashboard
export default function Dashboard() {
    return <div>Dashboard</div>;
}

// Dynamic import for components
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('./HeavyChart'), {
    loading: () => <p>Loading chart...</p>,
    ssr: false  // Don't render on server (client-only)
});

export default function Analytics() {
    return (
        <div>
            <h1>Analytics</h1>
            <HeavyChart />  {/* Loaded only when component renders */}
        </div>
    );
}
```

**Impact:** 30-50% smaller initial bundle

---

### Tree Shaking

**Remove unused code from bundles**

#### Enable Tree Shaking

```json
// package.json
{
    "sideEffects": false  // Enable aggressive tree shaking
}

// Or specify files with side effects
{
    "sideEffects": ["*.css", "*.scss", "src/polyfills.js"]
}
```

#### Import Only What You Need

```javascript
// ❌ BAD: Imports entire library (200KB)
import _ from 'lodash';
const result = _.debounce(fn, 300);

// ✅ GOOD: Import only needed function (ES modules, 5KB)
import { debounce } from 'lodash-es';
const result = debounce(fn, 300);

// ✅ ALSO GOOD: Individual module import
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);
```

**Webpack Configuration:**

```javascript
// webpack.config.js
module.exports = {
    mode: 'production',  // Enables tree shaking
    optimization: {
        usedExports: true,  // Mark unused exports
        minimize: true,     // Remove unused code
        sideEffects: true,  // Respect package.json sideEffects
    }
};
```

**Impact:** 40-60% smaller bundles

---

### Bundle Analysis

**Identify large dependencies**

```bash
# Install webpack-bundle-analyzer
npm install --save-dev webpack-bundle-analyzer

# Run build with analysis
npm run build -- --analyze
```

**Webpack configuration:**

```javascript
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
    plugins: [
        new BundleAnalyzerPlugin({
            analyzerMode: 'static',
            openAnalyzer: true,
            reportFilename: 'bundle-report.html'
        })
    ]
};
```

**What to look for:**
- Large dependencies (>50KB) that are barely used
- Duplicate dependencies (same library, different versions)
- Unused exports
- Opportunities for code splitting

**Impact:** Helps identify 20-40% of unnecessary code

---

### Dynamic Imports

**Load code only when needed**

```javascript
// ❌ BAD: Loading heavy library upfront
import Chart from 'chart.js';  // 200KB

function Analytics() {
    const [showChart, setShowChart] = useState(false);

    return (
        <div>
            <button onClick={() => setShowChart(true)}>Show Chart</button>
            {showChart && <Chart data={data} />}
        </div>
    );
}

// ✅ GOOD: Dynamic import (load only when needed)
function Analytics() {
    const [showChart, setShowChart] = useState(false);
    const [ChartComponent, setChartComponent] = useState(null);

    const loadChart = async () => {
        const { default: Chart } = await import('chart.js');  // Load on click
        setChartComponent(() => Chart);
        setShowChart(true);
    };

    return (
        <div>
            <button onClick={loadChart}>Show Chart</button>
            {showChart && ChartComponent && <ChartComponent data={data} />}
        </div>
    );
}
```

**Impact:** Reduces initial bundle by size of dynamically loaded code

---

## CSS Optimization

### Critical CSS Extraction

**Inline above-fold CSS, defer below-fold CSS**

```html
<head>
    <!-- ✅ GOOD: Inline critical CSS -->
    <style>
        /* Critical above-fold styles (5-10KB) */
        body { margin: 0; font-family: sans-serif; }
        .header { background: #333; color: white; }
        .hero { height: 100vh; background: url('hero.jpg'); }
    </style>

    <!-- Load non-critical CSS asynchronously -->
    <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

**Extract critical CSS automatically:**

```bash
# Using Critical (Node.js tool)
npm install -g critical

critical index.html --base ./public --inline --minify > index-optimized.html
```

**Impact:** 100-300ms faster FCP (First Contentful Paint)

---

### Unused CSS Removal

**Remove CSS not used on page**

```bash
# Using PurgeCSS
npm install --save-dev @fullhuman/postcss-purgecss

# postcss.config.js
module.exports = {
    plugins: [
        require('@fullhuman/postcss-purgecss')({
            content: ['./src/**/*.html', './src/**/*.js'],
            defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
        })
    ]
};
```

**Tailwind CSS (built-in purging):**

```javascript
// tailwind.config.js
module.exports = {
    content: [
        './src/**/*.{html,js,jsx,ts,tsx}',
    ],
    // Tailwind automatically removes unused classes
};
```

**Impact:** 50-90% smaller CSS files

---

### CSS-in-JS Optimization

**Extract static CSS at build time**

```javascript
// ❌ BAD: Runtime CSS-in-JS (slower)
import styled from 'styled-components';

const Button = styled.button`
    background: blue;
    color: white;
`;
// Generates CSS at runtime in browser

// ✅ BETTER: Zero-runtime CSS-in-JS
import { styled } from '@linaria/react';

const Button = styled.button`
    background: blue;
    color: white;
`;
// CSS extracted at build time, no runtime overhead
```

**Impact:** 20-50ms faster initial render

---

## Resource Loading Optimization

### Preload Critical Resources

```html
<head>
    <!-- Preload LCP image -->
    <link rel="preload" as="image" href="hero.webp" fetchpriority="high">

    <!-- Preload critical fonts -->
    <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

    <!-- Preload critical CSS -->
    <link rel="preload" as="style" href="critical.css">
</head>
```

**Impact:** 100-300ms faster LCP

---

### Preconnect to Critical Origins

```html
<head>
    <!-- Preconnect to critical third-party origins -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://cdn.yoursite.com">

    <!-- DNS-prefetch for less critical origins -->
    <link rel="dns-prefetch" href="https://analytics.google.com">
</head>
```

**Impact:** 100-500ms saved per critical resource

---

### Priority Hints (fetchpriority)

```html
<!-- High priority for LCP image -->
<img src="hero.jpg" alt="Hero" fetchpriority="high" loading="eager">

<!-- Low priority for below-fold images -->
<img src="footer-logo.jpg" alt="Footer" fetchpriority="low" loading="lazy">

<!-- High priority for critical script -->
<script src="app.js" fetchpriority="high" defer></script>
```

**Impact:** 50-200ms faster LCP

---

## Caching Strategies

### HTTP Caching

See [CDN Configuration](#cdn-configuration) section for detailed cache headers.

### Service Worker Caching

**Basic service worker with caching:**

```javascript
// sw.js
const CACHE_NAME = 'v1';
const urlsToCache = [
    '/',
    '/styles.css',
    '/app.js',
    '/logo.png'
];

// Install: Cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

// Fetch: Cache-first strategy
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
```

**Advanced caching with Workbox:**

```javascript
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';

// Precache build assets
precacheAndRoute(self.__WB_MANIFEST);

// Images: CacheFirst
registerRoute(
    ({ request }) => request.destination === 'image',
    new CacheFirst({ cacheName: 'images', plugins: [/* expiration */] })
);

// API: NetworkFirst
registerRoute(
    ({ url }) => url.pathname.startsWith('/api/'),
    new NetworkFirst({ cacheName: 'api' })
);
```

**Impact:** Instant repeat visits, offline support

---

## Summary Checklist

### Backend Optimization
- [ ] No N+1 database queries
- [ ] All foreign keys indexed
- [ ] Redis/Memcached caching implemented
- [ ] CDN configured for static assets
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] Compression enabled (Brotli or gzip)
- [ ] Connection pooling configured
- [ ] TTFB <800ms

### Image Optimization
- [ ] Modern formats (WebP/AVIF) used
- [ ] Responsive images with srcset
- [ ] All images have width/height attributes
- [ ] Lazy loading for below-fold images
- [ ] LCP image preloaded with fetchpriority="high"

### JavaScript Optimization
- [ ] Code splitting by route
- [ ] Tree shaking enabled
- [ ] Bundle size analyzed
- [ ] Large dependencies identified and optimized
- [ ] Dynamic imports for heavy components

### CSS Optimization
- [ ] Critical CSS inlined
- [ ] Unused CSS removed
- [ ] CSS files minified
- [ ] Non-critical CSS deferred

### Resource Loading
- [ ] Critical resources preloaded
- [ ] Third-party origins preconnected
- [ ] Priority hints used for LCP resources

### Caching
- [ ] HTTP cache headers configured
- [ ] Service worker implemented
- [ ] CDN caching enabled
- [ ] Cache invalidation strategy in place

---

**Performance targets:**
- TTFB: <800ms ✅
- LCP: <2.5s ✅
- CLS: <0.1 ✅
- INP: <200ms ✅

**Next:** See [core-web-vitals.md](core-web-vitals.md) for detailed metric optimization strategies.
