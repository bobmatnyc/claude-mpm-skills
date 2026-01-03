---
name: hono-testing
description: Hono testing patterns - app.request(), test client, mocking environment, and integration testing strategies
skill_version: 1.0.0
updated_at: 2025-01-03T00:00:00Z
tags: [hono, testing, vitest, jest, integration-testing, mocking]
progressive_disclosure:
  entry_point:
    summary: "Testing Hono apps with app.request(), typed test client, and environment mocking"
    when_to_use: "Writing unit and integration tests for Hono APIs"
    quick_start: "1. Create app instance 2. Use app.request() or testClient 3. Assert response"
  references: []
context_limit: 800
---

# Hono Testing Patterns

## Overview

Hono provides a simple testing approach: create a Request, pass it to your app, and validate the Response. The framework includes a typed test client for even better DX.

**Key Features**:
- Simple `app.request()` API
- Typed test client with full inference
- Environment mocking for Workers
- Works with Vitest, Jest, or any test runner

## When to Use This Skill

Use Hono testing when:
- Writing unit tests for route handlers
- Integration testing API endpoints
- Testing middleware behavior
- Mocking Cloudflare Workers bindings
- Validating request/response cycles

## Basic Testing

### Using app.request()

```typescript
import { Hono } from 'hono'
import { describe, it, expect } from 'vitest'

const app = new Hono()

app.get('/hello', (c) => c.text('Hello!'))
app.get('/json', (c) => c.json({ message: 'Hello' }))

describe('Basic routes', () => {
  it('should return text', async () => {
    const res = await app.request('/hello')

    expect(res.status).toBe(200)
    expect(await res.text()).toBe('Hello!')
  })

  it('should return JSON', async () => {
    const res = await app.request('/json')

    expect(res.status).toBe(200)
    expect(res.headers.get('Content-Type')).toContain('application/json')
    expect(await res.json()).toEqual({ message: 'Hello' })
  })
})
```

### Request Options

```typescript
// GET with query params
const res = await app.request('/search?q=hono&page=1')

// POST with JSON body
const res = await app.request('/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ name: 'Alice', email: 'alice@example.com' })
})

// POST with form data
const formData = new FormData()
formData.append('name', 'Alice')
formData.append('email', 'alice@example.com')

const res = await app.request('/users', {
  method: 'POST',
  body: formData
})

// With custom headers
const res = await app.request('/protected', {
  headers: {
    'Authorization': 'Bearer token123',
    'X-Custom-Header': 'value'
  }
})

// DELETE request
const res = await app.request('/users/123', {
  method: 'DELETE'
})
```

## Typed Test Client

The test client provides full type inference:

```typescript
import { Hono } from 'hono'
import { testClient } from 'hono/testing'
import { describe, it, expect } from 'vitest'

const app = new Hono()
  .get('/users', (c) => c.json({ users: [] }))
  .post('/users', async (c) => {
    const body = await c.req.json()
    return c.json({ id: '1', ...body }, 201)
  })
  .get('/users/:id', (c) => {
    return c.json({ id: c.req.param('id'), name: 'Alice' })
  })

describe('Users API', () => {
  const client = testClient(app)

  it('should list users', async () => {
    const res = await client.users.$get()

    expect(res.status).toBe(200)
    const data = await res.json()
    expect(data.users).toEqual([])
  })

  it('should create user', async () => {
    const res = await client.users.$post({
      json: { name: 'Alice', email: 'alice@example.com' }
    })

    expect(res.status).toBe(201)
    const data = await res.json()
    expect(data.name).toBe('Alice')
  })

  it('should get user by id', async () => {
    const res = await client.users[':id'].$get({
      param: { id: '123' }
    })

    expect(res.status).toBe(200)
    const data = await res.json()
    expect(data.id).toBe('123')
  })
})
```

## Testing with Validation

```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email()
})

app.post('/users', zValidator('json', createUserSchema), async (c) => {
  const data = c.req.valid('json')
  return c.json({ id: '1', ...data }, 201)
})

describe('Validation', () => {
  it('should accept valid data', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Alice',
        email: 'alice@example.com'
      })
    })

    expect(res.status).toBe(201)
  })

  it('should reject invalid email', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Alice',
        email: 'invalid-email'
      })
    })

    expect(res.status).toBe(400)
  })

  it('should reject missing name', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'alice@example.com'
      })
    })

    expect(res.status).toBe(400)
  })
})
```

## Mocking Environment (Cloudflare Workers)

### Mock Bindings

```typescript
import { Hono } from 'hono'

type Bindings = {
  DB: D1Database
  KV: KVNamespace
  API_KEY: string
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/data', async (c) => {
  const result = await c.env.DB.prepare('SELECT * FROM users').all()
  return c.json(result)
})

app.get('/config', (c) => {
  return c.json({ apiKey: c.env.API_KEY.slice(0, 4) + '...' })
})

describe('With mocked bindings', () => {
  // Mock D1 database
  const mockDB = {
    prepare: () => ({
      all: async () => ({ results: [{ id: 1, name: 'Alice' }] }),
      first: async () => ({ id: 1, name: 'Alice' }),
      run: async () => ({ success: true })
    })
  }

  // Mock KV namespace
  const mockKV = {
    get: async (key: string) => 'cached-value',
    put: async (key: string, value: string) => {},
    delete: async (key: string) => {}
  }

  const mockEnv: Bindings = {
    DB: mockDB as unknown as D1Database,
    KV: mockKV as unknown as KVNamespace,
    API_KEY: 'test-api-key-12345'  // pragma: allowlist secret
  }

  it('should use mocked database', async () => {
    const res = await app.request('/data', {}, mockEnv)

    expect(res.status).toBe(200)
    const data = await res.json()
    expect(data.results).toHaveLength(1)
  })

  it('should use mocked API key', async () => {
    const res = await app.request('/config', {}, mockEnv)

    const data = await res.json()
    expect(data.apiKey).toBe('test...')
  })
})
```

### Using Miniflare

For more realistic Cloudflare Workers testing:

```typescript
import { Miniflare } from 'miniflare'
import { describe, it, expect, beforeAll, afterAll } from 'vitest'

describe('With Miniflare', () => {
  let mf: Miniflare

  beforeAll(async () => {
    mf = new Miniflare({
      script: `
        import app from './src/index'
        export default app
      `,
      modules: true,
      d1Databases: ['DB'],
      kvNamespaces: ['KV']
    })
  })

  afterAll(async () => {
    await mf.dispose()
  })

  it('should work with real bindings', async () => {
    const res = await mf.dispatchFetch('http://localhost/data')
    expect(res.status).toBe(200)
  })
})
```

## Testing Middleware

```typescript
import { Hono } from 'hono'
import { createMiddleware } from 'hono/factory'

// Middleware to test
const authMiddleware = createMiddleware(async (c, next) => {
  const token = c.req.header('Authorization')?.replace('Bearer ', '')

  if (!token) {
    return c.json({ error: 'Unauthorized' }, 401)
  }

  if (token !== 'valid-token') {
    return c.json({ error: 'Invalid token' }, 403)
  }

  c.set('userId', 'user-123')
  await next()
})

const app = new Hono()

app.use('/protected/*', authMiddleware)

app.get('/protected/data', (c) => {
  const userId = c.get('userId')
  return c.json({ userId, data: 'secret' })
})

describe('Auth middleware', () => {
  it('should reject request without token', async () => {
    const res = await app.request('/protected/data')

    expect(res.status).toBe(401)
    expect(await res.json()).toEqual({ error: 'Unauthorized' })
  })

  it('should reject invalid token', async () => {
    const res = await app.request('/protected/data', {
      headers: { 'Authorization': 'Bearer invalid' }
    })

    expect(res.status).toBe(403)
    expect(await res.json()).toEqual({ error: 'Invalid token' })
  })

  it('should allow valid token', async () => {
    const res = await app.request('/protected/data', {
      headers: { 'Authorization': 'Bearer valid-token' }
    })

    expect(res.status).toBe(200)
    const data = await res.json()
    expect(data.userId).toBe('user-123')
  })
})
```

## Testing Error Handling

```typescript
import { Hono } from 'hono'
import { HTTPException } from 'hono/http-exception'

const app = new Hono()

app.get('/error', () => {
  throw new HTTPException(500, { message: 'Something went wrong' })
})

app.get('/not-found', (c) => {
  return c.notFound()
})

app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status)
  }
  return c.json({ error: 'Internal error' }, 500)
})

app.notFound((c) => {
  return c.json({ error: 'Not found' }, 404)
})

describe('Error handling', () => {
  it('should handle HTTPException', async () => {
    const res = await app.request('/error')

    expect(res.status).toBe(500)
    expect(await res.json()).toEqual({ error: 'Something went wrong' })
  })

  it('should handle not found', async () => {
    const res = await app.request('/unknown-route')

    expect(res.status).toBe(404)
    expect(await res.json()).toEqual({ error: 'Not found' })
  })
})
```

## Testing File Uploads

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.post('/upload', async (c) => {
  const formData = await c.req.formData()
  const file = formData.get('file') as File

  if (!file) {
    return c.json({ error: 'No file provided' }, 400)
  }

  return c.json({
    filename: file.name,
    size: file.size,
    type: file.type
  })
})

describe('File upload', () => {
  it('should handle file upload', async () => {
    const file = new File(['hello world'], 'test.txt', { type: 'text/plain' })
    const formData = new FormData()
    formData.append('file', file)

    const res = await app.request('/upload', {
      method: 'POST',
      body: formData
    })

    expect(res.status).toBe(200)
    const data = await res.json()
    expect(data.filename).toBe('test.txt')
    expect(data.size).toBe(11)
    expect(data.type).toBe('text/plain')
  })

  it('should reject missing file', async () => {
    const formData = new FormData()

    const res = await app.request('/upload', {
      method: 'POST',
      body: formData
    })

    expect(res.status).toBe(400)
  })
})
```

## Test Setup Patterns

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'dist/']
    }
  }
})
```

### Test Utilities

```typescript
// test/utils.ts
import { Hono } from 'hono'
import type { Bindings } from '../src/types'

export function createTestApp() {
  // Return fresh app instance for each test
  return new Hono<{ Bindings: Bindings }>()
}

export function createMockEnv(overrides: Partial<Bindings> = {}): Bindings {
  return {
    DB: createMockDB(),
    KV: createMockKV(),
    API_KEY: 'test-key',  // pragma: allowlist secret
    ...overrides
  }
}

export function createMockDB() {
  return {
    prepare: (sql: string) => ({
      bind: (...args: any[]) => ({
        all: async () => ({ results: [] }),
        first: async () => null,
        run: async () => ({ success: true })
      }),
      all: async () => ({ results: [] }),
      first: async () => null,
      run: async () => ({ success: true })
    })
  }
}

export function createMockKV() {
  const store = new Map<string, string>()

  return {
    get: async (key: string) => store.get(key) ?? null,
    put: async (key: string, value: string) => { store.set(key, value) },
    delete: async (key: string) => { store.delete(key) }
  }
}
```

### Using Test Utilities

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { createTestApp, createMockEnv } from './utils'
import { setupRoutes } from '../src/routes'

describe('API Tests', () => {
  let app: ReturnType<typeof createTestApp>
  let env: ReturnType<typeof createMockEnv>

  beforeEach(() => {
    app = createTestApp()
    env = createMockEnv()
    setupRoutes(app)
  })

  it('should work with fresh instances', async () => {
    const res = await app.request('/api/health', {}, env)
    expect(res.status).toBe(200)
  })
})
```

## Quick Reference

### app.request() Signature

```typescript
app.request(
  path: string,
  options?: RequestInit,
  env?: Bindings
): Promise<Response>
```

### Common Assertions

```typescript
// Status
expect(res.status).toBe(200)
expect(res.ok).toBe(true)

// Headers
expect(res.headers.get('Content-Type')).toContain('application/json')
expect(res.headers.get('X-Custom')).toBe('value')

// Body
expect(await res.text()).toBe('Hello')
expect(await res.json()).toEqual({ key: 'value' })

// Response properties
expect(res.redirected).toBe(false)
expect(res.url).toBe('http://localhost/path')
```

### Test Client Methods

```typescript
const client = testClient(app)

client.path.$get()
client.path.$post({ json: {} })
client.path[':id'].$get({ param: { id: '1' } })
client.path.$get({ query: { page: 1 } })
client.path.$post({ header: { 'X-Custom': 'v' } })
```

## Related Skills

- **hono-core** - Framework fundamentals
- **hono-middleware** - Middleware patterns
- **hono-validation** - Request validation

---

**Version**: Hono 4.x
**Last Updated**: January 2025
**License**: MIT
