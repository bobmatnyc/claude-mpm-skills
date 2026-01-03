---
name: hono-cloudflare
description: Hono on Cloudflare Workers - bindings, KV, D1, R2, Durable Objects, and edge deployment patterns
skill_version: 1.0.0
updated_at: 2025-01-03T00:00:00Z
tags: [hono, cloudflare-workers, edge, kv, d1, r2, durable-objects, serverless]
progressive_disclosure:
  entry_point:
    summary: "Deploy Hono to Cloudflare Workers with KV, D1, R2, and Durable Objects bindings"
    when_to_use: "Building edge applications on Cloudflare with Workers, Pages, or serverless functions"
    quick_start: "1. npm create hono@latest (cloudflare-workers) 2. Configure wrangler.toml 3. npx wrangler deploy"
  references: []
context_limit: 800
---

# Hono on Cloudflare Workers

## Overview

Hono was originally built for Cloudflare Workers and provides first-class support for the entire Cloudflare ecosystem including KV, D1, R2, Durable Objects, Queues, and more.

**Key Features**:
- Native Workers support
- Type-safe bindings access
- KV, D1, R2, Durable Objects integration
- Static asset serving
- Cloudflare Pages support
- Queue and scheduled handlers

## When to Use This Skill

Use Hono on Cloudflare when:
- Building edge APIs with global distribution
- Need serverless SQLite with D1
- Building real-time apps with Durable Objects
- Storing files with R2
- Need fast key-value storage with KV
- Deploying full-stack apps to Pages

## Quick Start

### Create New Project

```bash
npm create hono@latest my-app

# Select: cloudflare-workers

cd my-app
npm install
npm run dev
```

### Project Structure

```
my-app/
├── src/
│   └── index.ts         # Main entry point
├── wrangler.toml        # Cloudflare configuration
├── package.json
└── tsconfig.json
```

### Basic Application

```typescript
// src/index.ts
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.text('Hello Cloudflare Workers!'))

export default app
```

### Deploy

```bash
# Deploy to Cloudflare
npx wrangler deploy

# Local development
npx wrangler dev
```

## Environment Bindings

### Typed Bindings

```typescript
import { Hono } from 'hono'

// Define your bindings
type Bindings = {
  // Environment variables
  API_KEY: string
  DATABASE_URL: string

  // KV Namespaces
  MY_KV: KVNamespace

  // D1 Databases
  DB: D1Database

  // R2 Buckets
  BUCKET: R2Bucket

  // Durable Objects
  COUNTER: DurableObjectNamespace

  // Queues
  MY_QUEUE: Queue
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/config', (c) => {
  // Fully typed access
  const apiKey = c.env.API_KEY
  return c.json({ configured: !!apiKey })
})

export default app
```

### wrangler.toml Configuration

```toml
name = "my-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[vars]
API_KEY = "your-api-key"  # pragma: allowlist secret

[[kv_namespaces]]
binding = "MY_KV"
id = "your-kv-id"

[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-d1-id"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"

[[queues.producers]]
binding = "MY_QUEUE"
queue = "my-queue"
```

## KV Storage

### Basic Operations

```typescript
type Bindings = {
  CACHE: KVNamespace
}

const app = new Hono<{ Bindings: Bindings }>()

// Get value
app.get('/cache/:key', async (c) => {
  const key = c.req.param('key')
  const value = await c.env.CACHE.get(key)

  if (!value) {
    return c.json({ error: 'Not found' }, 404)
  }

  return c.json({ key, value })
})

// Get JSON value
app.get('/cache/:key/json', async (c) => {
  const key = c.req.param('key')
  const value = await c.env.CACHE.get(key, 'json')

  return c.json({ key, value })
})

// Set value
app.put('/cache/:key', async (c) => {
  const key = c.req.param('key')
  const body = await c.req.json()

  await c.env.CACHE.put(key, JSON.stringify(body), {
    expirationTtl: 3600  // 1 hour
  })

  return c.json({ success: true })
})

// Delete value
app.delete('/cache/:key', async (c) => {
  const key = c.req.param('key')
  await c.env.CACHE.delete(key)

  return c.json({ success: true })
})

// List keys
app.get('/cache', async (c) => {
  const prefix = c.req.query('prefix') || ''
  const list = await c.env.CACHE.list({ prefix, limit: 100 })

  return c.json({ keys: list.keys })
})
```

### KV with Metadata

```typescript
interface UserMeta {
  createdAt: string
  role: string
}

app.put('/users/:id', async (c) => {
  const id = c.req.param('id')
  const user = await c.req.json()

  await c.env.CACHE.put(`user:${id}`, JSON.stringify(user), {
    metadata: {
      createdAt: new Date().toISOString(),
      role: user.role
    } as UserMeta
  })

  return c.json({ success: true })
})

app.get('/users/:id', async (c) => {
  const id = c.req.param('id')
  const { value, metadata } = await c.env.CACHE.getWithMetadata<UserMeta>(`user:${id}`, 'json')

  if (!value) {
    return c.json({ error: 'Not found' }, 404)
  }

  return c.json({ user: value, metadata })
})
```

## D1 Database

### Basic Queries

```typescript
type Bindings = {
  DB: D1Database
}

const app = new Hono<{ Bindings: Bindings }>()

// Select all
app.get('/users', async (c) => {
  const { results } = await c.env.DB
    .prepare('SELECT * FROM users ORDER BY created_at DESC')
    .all()

  return c.json({ users: results })
})

// Select one
app.get('/users/:id', async (c) => {
  const id = c.req.param('id')
  const user = await c.env.DB
    .prepare('SELECT * FROM users WHERE id = ?')
    .bind(id)
    .first()

  if (!user) {
    return c.json({ error: 'Not found' }, 404)
  }

  return c.json({ user })
})

// Insert
app.post('/users', async (c) => {
  const { name, email } = await c.req.json()

  const result = await c.env.DB
    .prepare('INSERT INTO users (name, email) VALUES (?, ?)')
    .bind(name, email)
    .run()

  return c.json({
    success: result.success,
    id: result.meta.last_row_id
  }, 201)
})

// Update
app.put('/users/:id', async (c) => {
  const id = c.req.param('id')
  const { name, email } = await c.req.json()

  const result = await c.env.DB
    .prepare('UPDATE users SET name = ?, email = ? WHERE id = ?')
    .bind(name, email, id)
    .run()

  return c.json({ success: result.success })
})

// Delete
app.delete('/users/:id', async (c) => {
  const id = c.req.param('id')

  const result = await c.env.DB
    .prepare('DELETE FROM users WHERE id = ?')
    .bind(id)
    .run()

  return c.json({ success: result.success })
})
```

### Batch Operations

```typescript
app.post('/users/batch', async (c) => {
  const { users } = await c.req.json()

  const statements = users.map((user: { name: string; email: string }) =>
    c.env.DB
      .prepare('INSERT INTO users (name, email) VALUES (?, ?)')
      .bind(user.name, user.email)
  )

  const results = await c.env.DB.batch(statements)

  return c.json({
    success: results.every(r => r.success),
    count: results.length
  })
})
```

## R2 Object Storage

```typescript
type Bindings = {
  BUCKET: R2Bucket
}

const app = new Hono<{ Bindings: Bindings }>()

// Upload file
app.post('/files/:key', async (c) => {
  const key = c.req.param('key')
  const body = await c.req.arrayBuffer()
  const contentType = c.req.header('Content-Type') || 'application/octet-stream'

  await c.env.BUCKET.put(key, body, {
    httpMetadata: { contentType }
  })

  return c.json({ success: true, key })
})

// Download file
app.get('/files/:key', async (c) => {
  const key = c.req.param('key')
  const object = await c.env.BUCKET.get(key)

  if (!object) {
    return c.json({ error: 'Not found' }, 404)
  }

  const headers = new Headers()
  headers.set('Content-Type', object.httpMetadata?.contentType || 'application/octet-stream')
  headers.set('ETag', object.httpEtag)

  return new Response(object.body, { headers })
})

// Delete file
app.delete('/files/:key', async (c) => {
  const key = c.req.param('key')
  await c.env.BUCKET.delete(key)

  return c.json({ success: true })
})

// List files
app.get('/files', async (c) => {
  const prefix = c.req.query('prefix') || ''
  const list = await c.env.BUCKET.list({ prefix, limit: 100 })

  return c.json({
    objects: list.objects.map(obj => ({
      key: obj.key,
      size: obj.size,
      uploaded: obj.uploaded
    }))
  })
})
```

## Durable Objects

### Define Durable Object

```typescript
// src/counter.ts
export class Counter {
  private state: DurableObjectState
  private value: number = 0

  constructor(state: DurableObjectState) {
    this.state = state
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url)

    // Load value from storage
    this.value = await this.state.storage.get('value') || 0

    switch (url.pathname) {
      case '/increment':
        this.value++
        await this.state.storage.put('value', this.value)
        return new Response(String(this.value))

      case '/decrement':
        this.value--
        await this.state.storage.put('value', this.value)
        return new Response(String(this.value))

      case '/value':
        return new Response(String(this.value))

      default:
        return new Response('Not found', { status: 404 })
    }
  }
}
```

### Use in Hono

```typescript
import { Hono } from 'hono'

type Bindings = {
  COUNTER: DurableObjectNamespace
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/counter/:name/increment', async (c) => {
  const name = c.req.param('name')
  const id = c.env.COUNTER.idFromName(name)
  const stub = c.env.COUNTER.get(id)

  const response = await stub.fetch('http://counter/increment')
  const value = await response.text()

  return c.json({ name, value: parseInt(value) })
})

app.get('/counter/:name', async (c) => {
  const name = c.req.param('name')
  const id = c.env.COUNTER.idFromName(name)
  const stub = c.env.COUNTER.get(id)

  const response = await stub.fetch('http://counter/value')
  const value = await response.text()

  return c.json({ name, value: parseInt(value) })
})

export default app
export { Counter }
```

### wrangler.toml for Durable Objects

```toml
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"

[[migrations]]
tag = "v1"
new_classes = ["Counter"]
```

## Queues

### Producer

```typescript
type Bindings = {
  MY_QUEUE: Queue
}

const app = new Hono<{ Bindings: Bindings }>()

app.post('/tasks', async (c) => {
  const task = await c.req.json()

  await c.env.MY_QUEUE.send({
    type: 'process',
    data: task
  })

  return c.json({ queued: true })
})

// Batch send
app.post('/tasks/batch', async (c) => {
  const { tasks } = await c.req.json()

  await c.env.MY_QUEUE.sendBatch(
    tasks.map((task: any) => ({
      body: { type: 'process', data: task }
    }))
  )

  return c.json({ queued: tasks.length })
})
```

### Consumer

```typescript
export default {
  fetch: app.fetch,

  async queue(batch: MessageBatch, env: Bindings): Promise<void> {
    for (const message of batch.messages) {
      const { type, data } = message.body as { type: string; data: any }

      try {
        // Process message
        console.log(`Processing ${type}:`, data)
        message.ack()
      } catch (error) {
        message.retry()
      }
    }
  }
}
```

## Static Assets

### wrangler.toml

```toml
name = "my-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Serve static files from public directory
assets = { directory = "public" }
```

### With Route Handler

```typescript
import { Hono } from 'hono'
import { serveStatic } from 'hono/cloudflare-workers'

const app = new Hono()

// Serve static files
app.use('/static/*', serveStatic({ root: './' }))

// API routes
app.get('/api/hello', (c) => c.json({ hello: 'world' }))

export default app
```

## Scheduled Events (Cron)

```typescript
import { Hono } from 'hono'

const app = new Hono()

// Regular routes...

export default {
  fetch: app.fetch,

  async scheduled(
    event: ScheduledEvent,
    env: Bindings,
    ctx: ExecutionContext
  ): Promise<void> {
    switch (event.cron) {
      case '0 * * * *':  // Every hour
        await hourlyTask(env)
        break

      case '0 0 * * *':  // Daily at midnight
        await dailyTask(env)
        break
    }
  }
}

async function hourlyTask(env: Bindings) {
  console.log('Running hourly task')
}

async function dailyTask(env: Bindings) {
  console.log('Running daily task')
}
```

### wrangler.toml for Cron

```toml
[triggers]
crons = ["0 * * * *", "0 0 * * *"]
```

## Cloudflare Pages

### pages/functions Directory

```
my-app/
├── public/              # Static assets
│   ├── index.html
│   └── styles.css
└── functions/
    └── [[path]].ts      # Catch-all function
```

### Catch-All Handler

```typescript
// functions/[[path]].ts
import { Hono } from 'hono'
import { handle } from 'hono/cloudflare-pages'

const app = new Hono().basePath('/api')

app.get('/hello', (c) => c.json({ hello: 'world' }))
app.post('/echo', async (c) => c.json(await c.req.json()))

export const onRequest = handle(app)
```

## Middleware with Bindings

```typescript
import { createMiddleware } from 'hono/factory'

type Bindings = {
  API_KEY: string
}

// Access env in middleware
const authMiddleware = createMiddleware<{ Bindings: Bindings }>(
  async (c, next) => {
    // Don't access env at module level - access in handler!
    const apiKey = c.req.header('X-API-Key')

    if (apiKey !== c.env.API_KEY) {
      return c.json({ error: 'Unauthorized' }, 401)
    }

    await next()
  }
)

app.use('/api/*', authMiddleware)
```

## Quick Reference

### Bindings Types

```typescript
type Bindings = {
  // Variables
  MY_VAR: string

  // KV
  MY_KV: KVNamespace

  // D1
  DB: D1Database

  // R2
  BUCKET: R2Bucket

  // Durable Objects
  MY_DO: DurableObjectNamespace

  // Queues
  MY_QUEUE: Queue

  // Service Bindings
  OTHER_WORKER: Fetcher
}
```

### Common Commands

```bash
# Local development
npx wrangler dev

# Deploy
npx wrangler deploy

# Create D1 database
npx wrangler d1 create my-database

# Execute D1 SQL
npx wrangler d1 execute my-database --file=schema.sql

# Create KV namespace
npx wrangler kv:namespace create MY_KV

# Create R2 bucket
npx wrangler r2 bucket create my-bucket

# Tail logs
npx wrangler tail
```

## Related Skills

- **hono-core** - Framework fundamentals
- **hono-middleware** - Middleware patterns
- **hono-testing** - Testing with mocked bindings

---

**Version**: Hono 4.x, Wrangler 3.x
**Last Updated**: January 2025
**License**: MIT
