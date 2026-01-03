---
name: hono-validation
description: Hono request validation with Zod, TypeBox, Valibot - type-safe input validation for JSON, forms, query params, and headers
skill_version: 1.0.0
updated_at: 2025-01-03T00:00:00Z
tags: [hono, validation, zod, typebox, valibot, typescript, type-safety]
progressive_disclosure:
  entry_point:
    summary: "Type-safe request validation with Zod, TypeBox, or Valibot integration"
    when_to_use: "Validating JSON bodies, form data, query parameters, headers, or path parameters"
    quick_start: "1. npm install @hono/zod-validator zod 2. Create schema 3. Apply zValidator middleware"
  references: []
context_limit: 800
---

# Hono Validation Patterns

## Overview

Hono provides a lightweight built-in validator and integrates seamlessly with popular validation libraries like Zod, TypeBox, and Valibot. Validation happens as middleware, providing type-safe access to validated data in handlers.

**Key Features**:
- Built-in lightweight validator
- First-class Zod integration via `@hono/zod-validator`
- Standard Schema support (works with any validation library)
- Type inference from validation schemas
- Validates: JSON, forms, query params, headers, cookies, path params

## When to Use This Skill

Use Hono validation when:
- Validating API request bodies (JSON, form data)
- Ensuring query parameters meet requirements
- Validating authentication headers
- Type-safe path parameter parsing
- Cookie validation

## Installation

```bash
# Zod (recommended)
npm install @hono/zod-validator zod

# TypeBox
npm install @hono/typebox-validator @sinclair/typebox

# Valibot
npm install @hono/valibot-validator valibot

# Standard Schema (any compatible library)
npm install @hono/standard-validator
```

## Zod Validation (Recommended)

### Basic Usage

```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

// Define schema
const createUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional()
})

// Apply validation
app.post(
  '/users',
  zValidator('json', createUserSchema),
  (c) => {
    // Fully typed! { name: string; email: string; age?: number }
    const data = c.req.valid('json')
    return c.json({ user: data }, 201)
  }
)
```

### Validation Targets

```typescript
// JSON body
app.post('/api', zValidator('json', schema), handler)

// Form data (multipart or urlencoded)
app.post('/form', zValidator('form', schema), handler)

// Query parameters
app.get('/search', zValidator('query', z.object({
  q: z.string(),
  page: z.coerce.number().default(1),
  limit: z.coerce.number().max(100).default(20)
})), handler)

// Path parameters
app.get('/users/:id', zValidator('param', z.object({
  id: z.string().uuid()
})), handler)

// Headers (use lowercase!)
app.post('/api', zValidator('header', z.object({
  'authorization': z.string().startsWith('Bearer '),
  'x-request-id': z.string().uuid().optional()
})), handler)

// Cookies
app.get('/dashboard', zValidator('cookie', z.object({
  session: z.string().min(1)
})), handler)
```

### Custom Error Handling

```typescript
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

// Custom error response
app.post(
  '/users',
  zValidator('json', createUserSchema, (result, c) => {
    if (!result.success) {
      return c.json({
        error: 'Validation failed',
        details: result.error.flatten()
      }, 400)
    }
  }),
  (c) => {
    const data = c.req.valid('json')
    return c.json({ user: data }, 201)
  }
)
```

### Multiple Validators

```typescript
const paramsSchema = z.object({
  userId: z.string().uuid()
})

const bodySchema = z.object({
  name: z.string().optional(),
  email: z.string().email().optional()
})

const querySchema = z.object({
  fields: z.string().optional()
})

app.patch(
  '/users/:userId',
  zValidator('param', paramsSchema),
  zValidator('json', bodySchema),
  zValidator('query', querySchema),
  (c) => {
    const { userId } = c.req.valid('param')
    const body = c.req.valid('json')
    const { fields } = c.req.valid('query')

    return c.json({ updated: { userId, ...body } })
  }
)
```

## Common Zod Patterns

### Coercion for Query/Form Data

```typescript
// Query params come as strings - use coerce
const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['asc', 'desc']).default('desc')
})

app.get('/items', zValidator('query', paginationSchema), (c) => {
  const { page, limit, sort } = c.req.valid('query')
  // page: number, limit: number, sort: 'asc' | 'desc'
})
```

### Optional with Defaults

```typescript
const configSchema = z.object({
  theme: z.enum(['light', 'dark']).default('light'),
  notifications: z.boolean().default(true),
  language: z.string().default('en')
})
```

### Transformations

```typescript
const userSchema = z.object({
  email: z.string().email().toLowerCase(),
  name: z.string().trim(),
  tags: z.string().transform(s => s.split(',')),  // "a,b,c" → ["a","b","c"]
  createdAt: z.string().transform(s => new Date(s))
})
```

### Refinements

```typescript
const passwordSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword']
})

const dateRangeSchema = z.object({
  startDate: z.coerce.date(),
  endDate: z.coerce.date()
}).refine(data => data.endDate > data.startDate, {
  message: 'End date must be after start date'
})
```

### Discriminated Unions

```typescript
const eventSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('click'),
    x: z.number(),
    y: z.number()
  }),
  z.object({
    type: z.literal('scroll'),
    direction: z.enum(['up', 'down'])
  }),
  z.object({
    type: z.literal('keypress'),
    key: z.string()
  })
])

app.post('/events', zValidator('json', eventSchema), (c) => {
  const event = c.req.valid('json')

  if (event.type === 'click') {
    console.log(event.x, event.y)  // Typed correctly!
  }
})
```

## Built-in Validator

For simple cases without external dependencies:

```typescript
import { Hono } from 'hono'
import { validator } from 'hono/validator'

const app = new Hono()

app.post(
  '/posts',
  validator('json', (value, c) => {
    const { title, body } = value

    if (!title || typeof title !== 'string') {
      return c.json({ error: 'Title is required' }, 400)
    }

    if (!body || typeof body !== 'string') {
      return c.json({ error: 'Body is required' }, 400)
    }

    // Return validated data (shapes the type)
    return { title, body }
  }),
  (c) => {
    // data is typed as { title: string; body: string }
    const data = c.req.valid('json')
    return c.json({ post: data }, 201)
  }
)
```

## TypeBox Validation

```typescript
import { tbValidator } from '@hono/typebox-validator'
import { Type } from '@sinclair/typebox'

const UserSchema = Type.Object({
  name: Type.String({ minLength: 1 }),
  email: Type.String({ format: 'email' }),
  age: Type.Optional(Type.Integer({ minimum: 0 }))
})

app.post('/users', tbValidator('json', UserSchema), (c) => {
  const user = c.req.valid('json')
  return c.json({ user }, 201)
})
```

## Valibot Validation

```typescript
import { vValidator } from '@hono/valibot-validator'
import * as v from 'valibot'

const UserSchema = v.object({
  name: v.string([v.minLength(1)]),
  email: v.string([v.email()]),
  age: v.optional(v.number([v.integer(), v.minValue(0)]))
})

app.post('/users', vValidator('json', UserSchema), (c) => {
  const user = c.req.valid('json')
  return c.json({ user }, 201)
})
```

## Standard Schema Validator

Works with any validation library implementing the Standard Schema spec:

```typescript
import { standardValidator } from '@hono/standard-validator'
import { z } from 'zod'

// Works with Zod, Valibot, ArkType, etc.
app.post('/users', standardValidator('json', z.object({
  name: z.string(),
  email: z.string().email()
})), handler)
```

## File Upload Validation

```typescript
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const uploadSchema = z.object({
  file: z.instanceof(File).refine(
    (file) => file.size <= 5 * 1024 * 1024,
    'File must be less than 5MB'
  ).refine(
    (file) => ['image/jpeg', 'image/png'].includes(file.type),
    'Only JPEG and PNG allowed'
  ),
  description: z.string().optional()
})

app.post('/upload', zValidator('form', uploadSchema), async (c) => {
  const { file, description } = c.req.valid('form')

  const buffer = await file.arrayBuffer()
  // Process file...

  return c.json({ filename: file.name, size: file.size })
})
```

## Reusable Schema Patterns

### Create Schema Factory

```typescript
// schemas/common.ts
import { z } from 'zod'

export const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20)
})

export const idParamSchema = z.object({
  id: z.string().uuid()
})

export const timestampSchema = z.object({
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime()
})

// Usage
app.get('/items/:id',
  zValidator('param', idParamSchema),
  zValidator('query', paginationSchema),
  handler
)
```

### Extend Schemas

```typescript
const baseUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email()
})

const createUserSchema = baseUserSchema.extend({
  password: z.string().min(8)
})

const updateUserSchema = baseUserSchema.partial()

const userResponseSchema = baseUserSchema.extend({
  id: z.string().uuid(),
  createdAt: z.string().datetime()
})
```

## Best Practices

### 1. Validate Early

```typescript
// CORRECT: Validation before any processing
app.post('/users',
  zValidator('json', createUserSchema),  // Validate first
  async (c) => {
    const data = c.req.valid('json')     // Safe to use
    return c.json({ user: data })
  }
)
```

### 2. Use Appropriate Targets

```typescript
// JSON for API bodies
zValidator('json', schema)

// Form for HTML forms
zValidator('form', schema)

// Query for URL parameters (remember coercion!)
zValidator('query', z.object({ page: z.coerce.number() }))

// Param for route parameters
zValidator('param', z.object({ id: z.string() }))
```

### 3. Content-Type Matters

```typescript
// JSON validation requires Content-Type: application/json
// Form validation requires Content-Type: application/x-www-form-urlencoded
// or Content-Type: multipart/form-data

// Handle both:
const schema = z.object({ name: z.string() })

app.post('/data',
  async (c, next) => {
    const contentType = c.req.header('content-type')
    if (contentType?.includes('application/json')) {
      return zValidator('json', schema)(c, next)
    } else {
      return zValidator('form', schema)(c, next)
    }
  },
  handler
)
```

### 4. Lowercase Headers

```typescript
// Headers must be lowercase in validation
zValidator('header', z.object({
  'authorization': z.string(),        // ✓ lowercase
  'x-custom-header': z.string(),      // ✓ lowercase
  // 'Authorization': z.string(),     // ✗ won't work
}))
```

## Error Response Format

### Zod Flatten Format

```typescript
app.post('/users', zValidator('json', schema, (result, c) => {
  if (!result.success) {
    return c.json({
      success: false,
      error: result.error.flatten()
    }, 400)
  }
}), handler)

// Response:
{
  "success": false,
  "error": {
    "formErrors": [],
    "fieldErrors": {
      "email": ["Invalid email address"],
      "age": ["Number must be greater than 0"]
    }
  }
}
```

### Zod Issues Format

```typescript
app.post('/users', zValidator('json', schema, (result, c) => {
  if (!result.success) {
    return c.json({
      success: false,
      errors: result.error.issues.map(issue => ({
        field: issue.path.join('.'),
        message: issue.message
      }))
    }, 400)
  }
}), handler)

// Response:
{
  "success": false,
  "errors": [
    { "field": "email", "message": "Invalid email address" },
    { "field": "age", "message": "Number must be greater than 0" }
  ]
}
```

## Quick Reference

### Zod Validator Targets

| Target | Use Case | Example |
|--------|----------|---------|
| `json` | JSON body | `zValidator('json', schema)` |
| `form` | Form data | `zValidator('form', schema)` |
| `query` | URL query params | `zValidator('query', schema)` |
| `param` | Route params | `zValidator('param', schema)` |
| `header` | Request headers | `zValidator('header', schema)` |
| `cookie` | Cookies | `zValidator('cookie', schema)` |

### Common Zod Types

```typescript
z.string()                  // String
z.number()                  // Number
z.boolean()                 // Boolean
z.date()                    // Date
z.enum(['a', 'b'])          // Enum
z.array(z.string())         // Array
z.object({})                // Object
z.optional(z.string())      // Optional
z.nullable(z.string())      // Nullable
z.coerce.number()           // Coerce to number
z.string().default('val')   // With default
```

## Related Skills

- **hono-core** - Framework fundamentals
- **hono-rpc** - Type-safe RPC with validation
- **typescript-core** - TypeScript patterns

---

**Version**: Hono 4.x, @hono/zod-validator 0.2.x
**Last Updated**: January 2025
**License**: MIT
