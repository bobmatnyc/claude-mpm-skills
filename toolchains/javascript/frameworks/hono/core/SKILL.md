---
name: hono-core
description: Hono ultrafast web framework fundamentals - routing, context, handlers, and response patterns for multi-runtime deployment
skill_version: 1.0.0
updated_at: 2025-01-03T00:00:00Z
tags: [hono, web-framework, routing, typescript, cloudflare-workers, deno, bun, nodejs]
progressive_disclosure:
  entry_point:
    summary: "Ultrafast web framework built on Web Standards for Cloudflare Workers, Deno, Bun, Node.js"
    when_to_use: "Building APIs/web apps that need multi-runtime deployment, edge computing, or lightweight performance"
    quick_start: "1. npm create hono@latest 2. Define routes with app.get/post 3. Return responses via context"
  references: []
context_limit: 800
---

# Hono - Ultrafast Web Framework

## Overview

Hono is a small, simple, and ultrafast web framework built on Web Standards. It runs on Cloudflare Workers, Deno, Bun, Node.js, and more with the same codebase. The name means "flame" in Japanese.

**Key Features**:
- Built on Web Standards (Request/Response/fetch)
- Multi-runtime: Cloudflare Workers, Deno, Bun, Node.js, Vercel, AWS Lambda
- Ultrafast routing with RegExpRouter
- First-class TypeScript support
- Lightweight (~14KB minified)
- Rich middleware ecosystem

**Installation**:
```bash
# Create new project (recommended)
npm create hono@latest my-app

# Or install in existing project
npm install hono

# Runtime-specific adapters
npm install @hono/node-server  # Node.js
```

## When to Use This Skill

Use Hono when:
- Building APIs for edge/serverless environments (Cloudflare Workers, Vercel Edge)
- Need multi-runtime portability (same code on Bun, Deno, Node.js)
- Want TypeScript-first development with excellent type inference
- Building lightweight, high-performance APIs
- Need built-in middleware for common patterns (CORS, auth, compression)

**Hono vs Other Frameworks**:
- **Hono**: Multi-runtime, Web Standards, ultrafast, edge-optimized
- **Express**: Node.js only, larger ecosystem, slower
- **Fastify**: Node.js only, schema-based, good performance
- **Elysia**: Bun only, excellent performance, different API style

## Core Concepts

### Creating an Application

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.text('Hello Hono!'))

export default app
```

**With TypeScript Generics** (for bindings/variables):
```typescript
type Bindings = {
  DATABASE_URL: string
  API_KEY: string
}

type Variables = {
  user: { id: string; name: string }
}

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>()
```

### The Context Object (c)

The context `c` provides access to request data and response methods:

```typescript
app.get('/users/:id', async (c) => {
  // Request data
  const id = c.req.param('id')           // Path parameter
  const query = c.req.query('sort')       // Query parameter ?sort=asc
  const queries = c.req.queries('tags')   // Multiple: ?tags=a&tags=b
  const header = c.req.header('Authorization')
  const body = await c.req.json()         // JSON body
  const form = await c.req.formData()     // Form data

  // Environment (Cloudflare Workers bindings)
  const db = c.env.DATABASE_URL

  // Custom variables (set by middleware)
  const user = c.get('user')

  // Response methods
  return c.text('Plain text')
  return c.json({ id, name: 'User' })
  return c.html('<h1>Hello</h1>')
  return c.redirect('/login')
  return c.notFound()
})
```

### Response Methods

```typescript
// Text response
c.text('Hello', 200)

// JSON response
c.json({ message: 'Success' }, 201)
c.json({ error: 'Not found' }, 404)

// HTML response
c.html('<h1>Hello</h1>')

// Redirect
c.redirect('/login')           // 302 default
c.redirect('/login', 301)      // Permanent redirect

// Headers
c.header('X-Custom', 'value')
c.header('Cache-Control', 'max-age=3600')

// Streaming
c.streamText(async (stream) => {
  await stream.write('Hello ')
  await stream.write('World!')
})

// Raw Response
return new Response('Raw', { status: 200 })
```

## Routing Patterns

### Basic Routing

```typescript
const app = new Hono()

// HTTP methods
app.get('/users', getUsers)
app.post('/users', createUser)
app.put('/users/:id', updateUser)
app.delete('/users/:id', deleteUser)
app.patch('/users/:id', patchUser)

// All methods
app.all('/webhook', handleWebhook)

// Custom methods
app.on('PURGE', '/cache', purgeCache)
app.on(['GET', 'POST'], '/form', handleForm)
```

### Path Parameters

```typescript
// Single parameter
app.get('/users/:id', (c) => {
  const id = c.req.param('id')
  return c.json({ id })
})

// Multiple parameters
app.get('/posts/:postId/comments/:commentId', (c) => {
  const { postId, commentId } = c.req.param()
  return c.json({ postId, commentId })
})

// Optional parameter
app.get('/api/animal/:type?', (c) => {
  const type = c.req.param('type') || 'all'
  return c.json({ type })
})

// Regex validation
app.get('/posts/:id{[0-9]+}', (c) => {
  const id = c.req.param('id')  // Only numeric IDs
  return c.json({ id })
})

// Wildcards
app.get('/files/*', (c) => {
  const path = c.req.param('*')  // Everything after /files/
  return c.text(`File: ${path}`)
})
```

### Route Grouping

```typescript
// Using app.route()
const api = new Hono()
api.get('/users', getUsers)
api.get('/posts', getPosts)

const app = new Hono()
app.route('/api/v1', api)  // /api/v1/users, /api/v1/posts

// Using basePath()
const v2 = new Hono().basePath('/api/v2')
v2.get('/users', getUsers)  // /api/v2/users

// Chaining
app
  .get('/a', handlerA)
  .post('/b', handlerB)
  .delete('/c', handlerC)
```

### Route Organization (Multi-File)

```typescript
// routes/users.ts
import { Hono } from 'hono'

const users = new Hono()

users.get('/', async (c) => {
  return c.json({ users: [] })
})

users.post('/', async (c) => {
  const body = await c.req.json()
  return c.json({ created: body }, 201)
})

users.get('/:id', async (c) => {
  const id = c.req.param('id')
  return c.json({ id })
})

export default users

// app.ts
import { Hono } from 'hono'
import users from './routes/users'
import posts from './routes/posts'

const app = new Hono()

app.route('/users', users)
app.route('/posts', posts)

export default app
```

## Handler Patterns

### Inline Handlers

```typescript
// Simple handler
app.get('/hello', (c) => c.text('Hello!'))

// Async handler
app.get('/users', async (c) => {
  const users = await fetchUsers()
  return c.json({ users })
})

// Multiple handlers (middleware chain)
app.get('/admin', authenticate, authorize, (c) => {
  return c.json({ admin: true })
})
```

### Using Factory for Type-Safe Handlers

```typescript
import { createFactory } from 'hono/factory'

const factory = createFactory<{ Bindings: Bindings }>()

// Create typed handler
const getUser = factory.createHandlers(async (c) => {
  const id = c.req.param('id')
  const db = c.env.DATABASE_URL  // Typed!
  return c.json({ id })
})

app.get('/users/:id', ...getUser)
```

## Error Handling

### Built-in Error Handling

```typescript
import { HTTPException } from 'hono/http-exception'

app.get('/users/:id', async (c) => {
  const user = await findUser(c.req.param('id'))

  if (!user) {
    throw new HTTPException(404, { message: 'User not found' })
  }

  return c.json(user)
})

// Global error handler
app.onError((err, c) => {
  console.error(`${err}`)

  if (err instanceof HTTPException) {
    return err.getResponse()
  }

  return c.json({ error: 'Internal Server Error' }, 500)
})

// Not found handler
app.notFound((c) => {
  return c.json({ error: 'Route not found' }, 404)
})
```

### Custom Error Classes

```typescript
class ValidationError extends HTTPException {
  constructor(errors: string[]) {
    super(400, {
      message: 'Validation failed',
      cause: errors
    })
  }
}

class AuthenticationError extends HTTPException {
  constructor() {
    super(401, { message: 'Authentication required' })
  }
}
```

## Runtime-Specific Exports

### Cloudflare Workers

```typescript
// src/index.ts
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Cloudflare!'))

export default app
```

### Node.js

```typescript
// src/index.ts
import { serve } from '@hono/node-server'
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Node!'))

serve({
  fetch: app.fetch,
  port: 3000
})
```

### Bun

```typescript
// src/index.ts
import { Hono } from 'hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Bun!'))

export default {
  port: 3000,
  fetch: app.fetch
}
```

### Deno

```typescript
// main.ts
import { Hono } from 'npm:hono'

const app = new Hono()
app.get('/', (c) => c.text('Hello Deno!'))

Deno.serve(app.fetch)
```

## Best Practices

### Write Handlers Inline (Not Controllers)

```typescript
// CORRECT: Inline handlers with proper type inference
app.get('/users/:id', async (c) => {
  const id = c.req.param('id')  // Type: string
  return c.json({ id })
})

// AVOID: Controller-style (loses type inference)
class UserController {
  getUser(c: Context) {
    const id = c.req.param('id')  // Type: string | undefined
    return c.json({ id })
  }
}
```

### Use Modular Routes

```typescript
// CORRECT: Split routes by domain
// routes/users.ts
export const users = new Hono()
  .get('/', listUsers)
  .post('/', createUser)
  .get('/:id', getUser)

// app.ts
app.route('/users', users)
```

### Type Everything

```typescript
// Define your environment bindings
type Bindings = {
  DATABASE_URL: string
  JWT_SECRET: string
  MY_KV: KVNamespace
}

// Pass to Hono
const app = new Hono<{ Bindings: Bindings }>()

// Now c.env is fully typed
app.get('/', (c) => {
  const url = c.env.DATABASE_URL  // string
  const kv = c.env.MY_KV          // KVNamespace
})
```

## Quick Reference

### Common Context Methods

| Method | Description | Example |
|--------|-------------|---------|
| `c.req.param(name)` | Get path parameter | `c.req.param('id')` |
| `c.req.query(name)` | Get query parameter | `c.req.query('page')` |
| `c.req.header(name)` | Get request header | `c.req.header('Authorization')` |
| `c.req.json()` | Parse JSON body | `await c.req.json()` |
| `c.req.formData()` | Parse form data | `await c.req.formData()` |
| `c.text(str, status)` | Text response | `c.text('OK', 200)` |
| `c.json(obj, status)` | JSON response | `c.json({}, 201)` |
| `c.html(str)` | HTML response | `c.html('<h1>Hi</h1>')` |
| `c.redirect(url)` | Redirect | `c.redirect('/login')` |
| `c.header(k, v)` | Set response header | `c.header('X-Custom', 'val')` |
| `c.set(key, val)` | Set context variable | `c.set('user', user)` |
| `c.get(key)` | Get context variable | `c.get('user')` |
| `c.env` | Environment bindings | `c.env.API_KEY` |

### HTTP Methods

```typescript
app.get(path, ...handlers)
app.post(path, ...handlers)
app.put(path, ...handlers)
app.delete(path, ...handlers)
app.patch(path, ...handlers)
app.options(path, ...handlers)
app.head(path, ...handlers)
app.all(path, ...handlers)
app.on(method, path, ...handlers)
```

## Related Skills

- **hono-middleware** - Middleware patterns and composition
- **hono-validation** - Request validation with Zod
- **hono-rpc** - Type-safe RPC client
- **hono-testing** - Testing patterns
- **hono-jsx** - Server-side JSX rendering
- **hono-cloudflare** - Cloudflare Workers deployment

---

**Version**: Hono 4.x
**Last Updated**: January 2025
**License**: MIT
