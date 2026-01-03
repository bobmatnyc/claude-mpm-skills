---
name: hono-rpc
description: Hono RPC - end-to-end type-safe API client generation with hc client and TypeScript inference
skill_version: 1.0.0
updated_at: 2025-01-03T00:00:00Z
tags: [hono, rpc, type-safety, typescript, api-client, full-stack]
progressive_disclosure:
  entry_point:
    summary: "End-to-end type-safe API client with automatic TypeScript inference from server routes"
    when_to_use: "Building full-stack TypeScript apps where client needs type-safe API access"
    quick_start: "1. Export AppType from server 2. Import hc client 3. Use typed client methods"
  references: []
context_limit: 800
---

# Hono RPC - Type-Safe Client

## Overview

Hono RPC enables sharing API specifications between server and client through TypeScript's type system. Export your server's type, and the client automatically knows all routes, request shapes, and response types - no code generation required.

**Key Features**:
- Zero-codegen type-safe client
- Automatic TypeScript inference
- Works with Zod validators
- Status code-aware response types
- Supports path params, query, headers

## When to Use This Skill

Use Hono RPC when:
- Building full-stack TypeScript applications
- Need type-safe API consumption without OpenAPI/codegen
- Want compile-time validation of API calls
- Sharing types between client and server in monorepos

## Basic Setup

### Server Side

```typescript
// server/index.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

// Define routes with validation
const route = app
  .get('/users', async (c) => {
    const users = [{ id: '1', name: 'Alice' }]
    return c.json({ users })
  })
  .post(
    '/users',
    zValidator('json', z.object({
      name: z.string(),
      email: z.string().email()
    })),
    async (c) => {
      const data = c.req.valid('json')
      return c.json({ id: '1', ...data }, 201)
    }
  )
  .get('/users/:id', async (c) => {
    const id = c.req.param('id')
    return c.json({ id, name: 'Alice' })
  })

// Export type for client
export type AppType = typeof route

export default app
```

### Client Side

```typescript
// client/api.ts
import { hc } from 'hono/client'
import type { AppType } from '../server'

// Create typed client
const client = hc<AppType>('http://localhost:3000')

// All methods are type-safe!
async function examples() {
  // GET /users
  const usersRes = await client.users.$get()
  const { users } = await usersRes.json()
  // users: { id: string; name: string }[]

  // POST /users - body is typed
  const createRes = await client.users.$post({
    json: {
      name: 'Bob',
      email: 'bob@example.com'
    }
  })
  const created = await createRes.json()
  // created: { id: string; name: string; email: string }

  // GET /users/:id - params are typed
  const userRes = await client.users[':id'].$get({
    param: { id: '123' }
  })
  const user = await userRes.json()
  // user: { id: string; name: string }
}
```

## Route Chaining for Type Export

**Important**: Chain routes for proper type inference:

```typescript
// CORRECT: Chain all routes
const route = app
  .get('/a', handlerA)
  .post('/b', handlerB)
  .get('/c', handlerC)

export type AppType = typeof route

// WRONG: Separate statements lose type info
app.get('/a', handlerA)
app.post('/b', handlerB)  // Types lost!

export type AppType = typeof app  // Missing routes!
```

## Request Patterns

### Path Parameters

```typescript
// Server
const route = app.get('/posts/:postId/comments/:commentId', async (c) => {
  const { postId, commentId } = c.req.param()
  return c.json({ postId, commentId })
})

// Client
const res = await client.posts[':postId'].comments[':commentId'].$get({
  param: {
    postId: '1',
    commentId: '42'
  }
})
```

### Query Parameters

```typescript
// Server
const route = app.get(
  '/search',
  zValidator('query', z.object({
    q: z.string(),
    page: z.coerce.number().optional(),
    limit: z.coerce.number().optional()
  })),
  async (c) => {
    const { q, page, limit } = c.req.valid('query')
    return c.json({ query: q, page, limit })
  }
)

// Client
const res = await client.search.$get({
  query: {
    q: 'typescript',
    page: 1,
    limit: 20
  }
})
```

### JSON Body

```typescript
// Server
const route = app.post(
  '/posts',
  zValidator('json', z.object({
    title: z.string(),
    content: z.string(),
    tags: z.array(z.string()).optional()
  })),
  async (c) => {
    const data = c.req.valid('json')
    return c.json({ id: '1', ...data }, 201)
  }
)

// Client
const res = await client.posts.$post({
  json: {
    title: 'Hello World',
    content: 'My first post',
    tags: ['typescript', 'hono']
  }
})
```

### Form Data

```typescript
// Server
const route = app.post(
  '/upload',
  zValidator('form', z.object({
    file: z.instanceof(File),
    description: z.string().optional()
  })),
  async (c) => {
    const { file, description } = c.req.valid('form')
    return c.json({ filename: file.name })
  }
)

// Client
const formData = new FormData()
formData.append('file', file)
formData.append('description', 'My file')

const res = await client.upload.$post({
  form: formData
})
```

### Headers

```typescript
// Server
const route = app.get(
  '/protected',
  zValidator('header', z.object({
    authorization: z.string()
  })),
  async (c) => {
    return c.json({ authenticated: true })
  }
)

// Client
const res = await client.protected.$get({
  header: {
    authorization: 'Bearer token123'
  }
})
```

## Response Type Inference

### Status Code-Aware Types

```typescript
// Server
const route = app.get('/user', async (c) => {
  const user = await getUser()

  if (!user) {
    return c.json({ error: 'Not found' }, 404)
  }

  return c.json({ id: user.id, name: user.name }, 200)
})

// Client - use InferResponseType
import { InferResponseType } from 'hono/client'

type SuccessResponse = InferResponseType<typeof client.user.$get, 200>
// { id: string; name: string }

type ErrorResponse = InferResponseType<typeof client.user.$get, 404>
// { error: string }

// Handle different status codes
const res = await client.user.$get()

if (res.status === 200) {
  const data = await res.json()
  // data: { id: string; name: string }
} else if (res.status === 404) {
  const error = await res.json()
  // error: { error: string }
}
```

### Request Type Inference

```typescript
import { InferRequestType } from 'hono/client'

type CreateUserRequest = InferRequestType<typeof client.users.$post>['json']
// { name: string; email: string }

// Use for form validation, state management, etc.
const [formData, setFormData] = useState<CreateUserRequest>({
  name: '',
  email: ''
})
```

## Multi-File Route Organization

### Organize Routes

```typescript
// server/routes/users.ts
import { Hono } from 'hono'

export const users = new Hono()
  .get('/', async (c) => c.json({ users: [] }))
  .post('/', async (c) => c.json({ created: true }, 201))
  .get('/:id', async (c) => c.json({ id: c.req.param('id') }))

// server/routes/posts.ts
export const posts = new Hono()
  .get('/', async (c) => c.json({ posts: [] }))
  .post('/', async (c) => c.json({ created: true }, 201))

// server/index.ts
import { Hono } from 'hono'
import { users } from './routes/users'
import { posts } from './routes/posts'

const app = new Hono()

const route = app
  .route('/users', users)
  .route('/posts', posts)

export type AppType = typeof route
export default app
```

### Client Usage

```typescript
import { hc } from 'hono/client'
import type { AppType } from '../server'

const client = hc<AppType>('http://localhost:3000')

// Routes are nested
await client.users.$get()         // GET /users
await client.users[':id'].$get()  // GET /users/:id
await client.posts.$get()         // GET /posts
```

## Error Handling

### Handle Fetch Errors

```typescript
async function fetchUser(id: string) {
  try {
    const res = await client.users[':id'].$get({
      param: { id }
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.message || 'Failed to fetch user')
    }

    return await res.json()
  } catch (error) {
    if (error instanceof TypeError) {
      // Network error
      throw new Error('Network error')
    }
    throw error
  }
}
```

### Type-Safe Error Responses

```typescript
// Server
const route = app.get('/resource', async (c) => {
  try {
    const data = await fetchData()
    return c.json({ success: true, data })
  } catch (e) {
    return c.json({ success: false, error: 'Failed' }, 500)
  }
})

// Client
type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string }

const res = await client.resource.$get()
const result: ApiResponse<DataType> = await res.json()

if (result.success) {
  console.log(result.data)  // Typed!
} else {
  console.error(result.error)
}
```

## Configuration Options

### Custom Fetch

```typescript
const client = hc<AppType>('http://localhost:3000', {
  // Custom fetch (for testing, logging, etc.)
  fetch: async (input, init) => {
    console.log('Fetching:', input)
    return fetch(input, init)
  }
})
```

### Default Headers

```typescript
const client = hc<AppType>('http://localhost:3000', {
  headers: {
    'Authorization': 'Bearer token',
    'X-Custom-Header': 'value'
  }
})
```

### Dynamic Headers

```typescript
const getClient = (token: string) =>
  hc<AppType>('http://localhost:3000', {
    headers: () => ({
      'Authorization': `Bearer ${token}`
    })
  })

// Or with a function that returns headers
const client = hc<AppType>('http://localhost:3000', {
  headers: () => {
    const token = getAuthToken()
    return token ? { 'Authorization': `Bearer ${token}` } : {}
  }
})
```

## Best Practices

### 1. Enable Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true  // Required for proper type inference!
  }
}
```

### 2. Use Explicit Status Codes

```typescript
// CORRECT: Explicit status enables type discrimination
return c.json({ data }, 200)
return c.json({ error: 'Not found' }, 404)

// AVOID: c.notFound() doesn't work well with RPC
return c.notFound()  // Response type is not properly inferred
```

### 3. Split Large Apps

```typescript
// For large apps, split routes to reduce IDE overhead
const v1 = new Hono()
  .route('/users', usersRoute)
  .route('/posts', postsRoute)

const v2 = new Hono()
  .route('/users', usersV2Route)

// Export separate types
export type V1Type = typeof v1
export type V2Type = typeof v2
```

### 4. Consistent Response Shapes

```typescript
// Define standard response wrapper
type ApiSuccess<T> = { ok: true; data: T }
type ApiError = { ok: false; error: string; code?: string }
type ApiResponse<T> = ApiSuccess<T> | ApiError

// Use consistently
const route = app.get('/users/:id', async (c) => {
  const user = await findUser(c.req.param('id'))

  if (!user) {
    return c.json({ ok: false, error: 'User not found' } as ApiError, 404)
  }

  return c.json({ ok: true, data: user } as ApiSuccess<User>, 200)
})
```

## Quick Reference

### Client Methods

| HTTP Method | Client Method |
|-------------|---------------|
| GET | `client.path.$get()` |
| POST | `client.path.$post()` |
| PUT | `client.path.$put()` |
| DELETE | `client.path.$delete()` |
| PATCH | `client.path.$patch()` |

### Request Options

```typescript
client.path.$method({
  param: { id: '1' },           // Path parameters
  query: { page: 1 },           // Query parameters
  json: { name: 'Alice' },      // JSON body
  form: formData,               // Form data
  header: { 'X-Custom': 'v' }   // Headers
})
```

### Type Utilities

```typescript
import { InferRequestType, InferResponseType } from 'hono/client'

// Extract request type
type ReqType = InferRequestType<typeof client.users.$post>

// Extract response type by status
type Res200 = InferResponseType<typeof client.users.$get, 200>
type Res404 = InferResponseType<typeof client.users.$get, 404>
```

## Related Skills

- **hono-core** - Framework fundamentals
- **hono-validation** - Request validation
- **typescript-core** - TypeScript patterns

---

**Version**: Hono 4.x
**Last Updated**: January 2025
**License**: MIT
