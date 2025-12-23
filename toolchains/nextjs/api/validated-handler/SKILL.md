---
name: validated-handler
description: "Type-safe API route handler with automatic Zod validation for Next.js App Router..."
version: 1.0.0
tags: []
---

# Next.js Validated Handler Pattern

Type-safe API route handler with automatic Zod validation for Next.js App Router.

## When to Use This Skill

Use this skill when:
- Building Next.js API routes (App Router)
- Want automatic input validation with Zod
- Need consistent error handling across API routes
- Want to eliminate boilerplate validation code
- Building type-safe APIs with TypeScript

## The Problem

Without a validated handler, every API route has repetitive validation code:

```typescript
// ❌ REPETITIVE - Every route looks like this
export async function GET(request: NextRequest) {
  try {
    // 1. Parse query params
    const { searchParams } = new URL(request.url);
    const rawPage = searchParams.get('page');
    const rawLimit = searchParams.get('limit');

    // 2. Validate each param manually
    if (!rawPage || isNaN(Number(rawPage))) {
      return NextResponse.json(
        { error: 'Invalid page parameter' },
        { status: 400 }
      );
    }

    if (!rawLimit || isNaN(Number(rawLimit))) {
      return NextResponse.json(
        { error: 'Invalid limit parameter' },
        { status: 400 }
      );
    }

    const page = Number(rawPage);
    const limit = Number(rawLimit);

    // 3. Validate ranges
    if (page < 1) {
      return NextResponse.json(
        { error: 'Page must be >= 1' },
        { status: 400 }
      );
    }

    if (limit < 1 || limit > 100) {
      return NextResponse.json(
        { error: 'Limit must be between 1 and 100' },
        { status: 400 }
      );
    }

    // 4. Finally, business logic
    const data = await fetchData(page, limit);
    return NextResponse.json(data);

  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

**Problems**:
- 30+ lines of boilerplate per route
- Error-prone manual validation
- Inconsistent error messages
- No type safety
- Hard to maintain across 100+ routes

## The Solution: validatedHandler

Create a reusable handler that combines Zod validation with Next.js API routes:

```typescript
// src/lib/api/handler.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

type ValidationSource = 'query' | 'body';

export function validatedHandler<T extends z.ZodType>(
  config: {
    input: { schema: T; source: ValidationSource };
  },
  handler: (ctx: { input: z.infer<T>; request: NextRequest }) => Promise<Response>,
) {
  return async (request: NextRequest): Promise<Response> => {
    try {
      // 1. Parse input based on source
      const rawInput = config.input.source === 'query'
        ? Object.fromEntries(new URL(request.url).searchParams)
        : await request.json();

      // 2. Validate with Zod schema
      const result = config.input.schema.safeParse(rawInput);

      if (!result.success) {
        return NextResponse.json({
          error: "Validation failed",
          details: result.error.issues.map(err => ({
            path: err.path.join("."),
            message: err.message,
          })),
        }, { status: 400 });
      }

      // 3. Call handler with typed data
      return await handler({ input: result.data, request });

    } catch (error) {
      console.error('API Error:', error);
      return NextResponse.json(
        { error: "Internal server error" },
        { status: 500 }
      );
    }
  };
}
```

### Usage Example

With validatedHandler, routes become clean and type-safe:

```typescript
// src/app/api/schools/route.ts
import { validatedHandler } from '@/lib/api/handler';
import { paginationInputSchema } from '@/lib/api/pagination';
import { z } from 'zod';
import { db } from '@/lib/db';
import { schools } from '@/lib/db/schema';
import { ilike } from 'drizzle-orm';

// Define schema
const getSchoolsSchema = paginationInputSchema.extend({
  keyword: z.string().optional(),
  districtId: z.string().uuid().optional(),
});

// Use validatedHandler - clean and type-safe!
export const GET = validatedHandler({
  input: { source: 'query', schema: getSchoolsSchema }
}, async ({ input }) => {
  // input is fully typed: { page: number, limit: number, keyword?: string, districtId?: string }

  const schoolList = await db.query.schools.findMany({
    where: input.keyword
      ? ilike(schools.name, `%${input.keyword}%`)
      : undefined,
    limit: input.limit,
    offset: (input.page - 1) * input.limit,
  });

  return NextResponse.json(schoolList);
});
```

**Benefits**:
- ✅ Only 15 lines vs 50+ lines
- ✅ Automatic validation with Zod
- ✅ Full TypeScript type inference
- ✅ Consistent error responses
- ✅ No manual parsing
- ✅ Single place to maintain validation logic

## Core Implementation

### Complete Handler Implementation

```typescript
// src/lib/api/handler.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

type ValidationSource = 'query' | 'body';

interface HandlerConfig<T extends z.ZodType> {
  input: {
    schema: T;
    source: ValidationSource;
  };
}

interface HandlerContext<T extends z.ZodType> {
  input: z.infer<T>;
  request: NextRequest;
}

export function validatedHandler<T extends z.ZodType>(
  config: HandlerConfig<T>,
  handler: (ctx: HandlerContext<T>) => Promise<Response>,
) {
  return async (request: NextRequest): Promise<Response> => {
    try {
      // Parse input based on source
      let rawInput: unknown;

      if (config.input.source === 'query') {
        const { searchParams } = new URL(request.url);
        rawInput = Object.fromEntries(searchParams);
      } else if (config.input.source === 'body') {
        rawInput = await request.json();
      }

      // Validate with Zod
      const result = config.input.schema.safeParse(rawInput);

      if (!result.success) {
        return NextResponse.json({
          error: "Validation failed",
          details: result.error.issues.map(err => ({
            path: err.path.join("."),
            message: err.message,
          })),
        }, { status: 400 });
      }

      // Call handler with typed data
      return await handler({
        input: result.data,
        request,
      });

    } catch (error) {
      // Log error for debugging
      console.error('API Error:', error);

      // Return generic error to client
      return NextResponse.json(
        { error: "Internal server error" },
        { status: 500 }
      );
    }
  };
}
```

### Pagination Schema (Reusable)

```typescript
// src/lib/api/pagination.ts
import { z } from 'zod';

export const paginationInputSchema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(10),
});

export type PaginationInput = z.infer<typeof paginationInputSchema>;

export type PaginatedResponse<T> = {
  data: T[];
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  nextPage: number | null;
  previousPage: number | null;
};

export function createPaginatedResponse<T>(
  data: T[],
  total: number,
  page: number,
  limit: number
): PaginatedResponse<T> {
  const totalPages = Math.ceil(total / limit);
  return {
    data,
    page,
    limit,
    total,
    totalPages,
    nextPage: page < totalPages ? page + 1 : null,
    previousPage: page > 1 ? page - 1 : null,
  };
}
```

## Common Patterns

### GET Route with Query Params

```typescript
// src/app/api/providers/route.ts
import { validatedHandler } from '@/lib/api/handler';
import { paginationInputSchema } from '@/lib/api/pagination';
import { z } from 'zod';

const getProvidersSchema = paginationInputSchema.extend({
  status: z.enum(['active', 'inactive']).optional(),
  specialty: z.string().optional(),
});

export const GET = validatedHandler({
  input: { source: 'query', schema: getProvidersSchema }
}, async ({ input }) => {
  const providers = await db.query.providers.findMany({
    where: buildWhereClause(input),
    limit: input.limit,
    offset: (input.page - 1) * input.limit,
  });

  return NextResponse.json(providers);
});
```

### POST Route with Body Validation

```typescript
// src/app/api/providers/route.ts
import { validatedHandler } from '@/lib/api/handler';
import { z } from 'zod';

const createProviderSchema = z.object({
  name: z.string().min(1).max(255),
  email: z.string().email(),
  specialty: z.string().min(1),
  licenseNumber: z.string().optional(),
});

export const POST = validatedHandler({
  input: { source: 'body', schema: createProviderSchema }
}, async ({ input }) => {
  const newProvider = await db.insert(providers)
    .values(input)
    .returning();

  return NextResponse.json(newProvider[0], { status: 201 });
});
```

### Route with Path Parameters

```typescript
// src/app/api/providers/[id]/route.ts
import { validatedHandler } from '@/lib/api/handler';
import { z } from 'zod';

const updateProviderSchema = z.object({
  name: z.string().min(1).max(255).optional(),
  email: z.string().email().optional(),
  specialty: z.string().min(1).optional(),
});

export const PATCH = validatedHandler({
  input: { source: 'body', schema: updateProviderSchema }
}, async ({ input, request }) => {
  // Extract path param manually
  const url = new URL(request.url);
  const id = url.pathname.split('/').pop();

  if (!id) {
    return NextResponse.json({ error: 'Invalid ID' }, { status: 400 });
  }

  const updated = await db.update(providers)
    .set(input)
    .where(eq(providers.id, id))
    .returning();

  return NextResponse.json(updated[0]);
});
```

### Route with Authentication

```typescript
// src/app/api/providers/route.ts
import { validatedHandler } from '@/lib/api/handler';
import { auth } from '@/lib/auth';
import { z } from 'zod';

const getProvidersSchema = paginationInputSchema.extend({
  status: z.enum(['active', 'inactive']).optional(),
});

export const GET = validatedHandler({
  input: { source: 'query', schema: getProvidersSchema }
}, async ({ input, request }) => {
  // Authentication check
  const session = await auth(request);
  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // Authorization check
  if (!session.user.roles.includes('admin')) {
    return NextResponse.json(
      { error: 'Forbidden' },
      { status: 403 }
    );
  }

  // Business logic
  const providers = await db.query.providers.findMany({
    where: buildWhereClause(input),
    limit: input.limit,
    offset: (input.page - 1) * input.limit,
  });

  return NextResponse.json(providers);
});
```

## Advanced Patterns

### Multiple Validation Sources

```typescript
// Validate both query and body
const searchSchema = z.object({
  query: z.string(),
});

const filtersSchema = z.object({
  category: z.string().optional(),
  priceMin: z.number().optional(),
  priceMax: z.number().optional(),
});

export const POST = async (request: NextRequest) => {
  // Validate query params
  const queryResult = searchSchema.safeParse(
    Object.fromEntries(new URL(request.url).searchParams)
  );

  if (!queryResult.success) {
    return NextResponse.json({ error: 'Invalid query' }, { status: 400 });
  }

  // Validate body
  const body = await request.json();
  const bodyResult = filtersSchema.safeParse(body);

  if (!bodyResult.success) {
    return NextResponse.json({ error: 'Invalid filters' }, { status: 400 });
  }

  // Use both
  const results = await search(queryResult.data.query, bodyResult.data);
  return NextResponse.json(results);
};
```

### Custom Error Responses

```typescript
// src/lib/api/handler.ts (enhanced)
export function validatedHandler<T extends z.ZodType>(
  config: {
    input: { schema: T; source: ValidationSource };
    errorTransform?: (error: z.ZodError) => { error: string; details?: unknown };
  },
  handler: (ctx: { input: z.infer<T>; request: NextRequest }) => Promise<Response>,
) {
  return async (request: NextRequest): Promise<Response> => {
    try {
      const rawInput = config.input.source === 'query'
        ? Object.fromEntries(new URL(request.url).searchParams)
        : await request.json();

      const result = config.input.schema.safeParse(rawInput);

      if (!result.success) {
        const errorResponse = config.errorTransform
          ? config.errorTransform(result.error)
          : {
              error: "Validation failed",
              details: result.error.issues.map(err => ({
                path: err.path.join("."),
                message: err.message,
              })),
            };

        return NextResponse.json(errorResponse, { status: 400 });
      }

      return await handler({ input: result.data, request });
    } catch (error) {
      console.error('API Error:', error);
      return NextResponse.json(
        { error: "Internal server error" },
        { status: 500 }
      );
    }
  };
}
```

## Testing

### Unit Tests for Handler

```typescript
// src/lib/api/handler.test.ts
import { validatedHandler } from './handler';
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

describe('validatedHandler', () => {
  it('should validate query params successfully', async () => {
    const schema = z.object({
      page: z.coerce.number(),
    });

    const handler = validatedHandler({
      input: { source: 'query', schema }
    }, async ({ input }) => {
      return NextResponse.json({ page: input.page });
    });

    const request = new NextRequest('http://localhost?page=2');
    const response = await handler(request);
    const data = await response.json();

    expect(data).toEqual({ page: 2 });
  });

  it('should return 400 for invalid input', async () => {
    const schema = z.object({
      page: z.coerce.number().min(1),
    });

    const handler = validatedHandler({
      input: { source: 'query', schema }
    }, async ({ input }) => {
      return NextResponse.json({ page: input.page });
    });

    const request = new NextRequest('http://localhost?page=0');
    const response = await handler(request);

    expect(response.status).toBe(400);
    const data = await response.json();
    expect(data.error).toBe('Validation failed');
  });
});
```

### Integration Tests for API Routes

```typescript
// src/app/api/schools/route.test.ts
import { GET } from './route';
import { NextRequest } from 'next/server';

describe('GET /api/schools', () => {
  it('should return paginated schools', async () => {
    const request = new NextRequest('http://localhost/api/schools?page=1&limit=10');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toHaveProperty('data');
    expect(data).toHaveProperty('page', 1);
    expect(data).toHaveProperty('limit', 10);
  });

  it('should validate pagination parameters', async () => {
    const request = new NextRequest('http://localhost/api/schools?page=-1');
    const response = await GET(request);

    expect(response.status).toBe(400);
  });
});
```

## Benefits Summary

### Code Reduction
- **Before**: 50+ lines per route with validation
- **After**: 10-15 lines per route
- **Savings**: 70% code reduction

### Type Safety
- ✅ Input types automatically inferred from Zod schema
- ✅ No `any` types or type assertions
- ✅ Compile-time validation of schema usage

### Developer Experience
- ✅ Single place to define validation
- ✅ Consistent error messages
- ✅ Clear separation of validation and business logic
- ✅ Easy to test

### Maintainability
- ✅ DRY principle applied
- ✅ Changes to validation logic in one place
- ✅ Reusable schemas across routes
- ✅ Framework-agnostic pattern (works with Express, Fastify, Hono)

## Pattern Variations

### For Express.js/Fastify

```typescript
export function validatedHandler<T extends z.ZodType>(
  schema: T,
  handler: (input: z.infer<T>, req: Request, res: Response) => Promise<void>
) {
  return async (req: Request, res: Response) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ error: result.error });
    }
    await handler(result.data, req, res);
  };
}
```

### For Hono

```typescript
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';

const app = new Hono();

app.get('/schools', zValidator('query', getSchoolsSchema), async (c) => {
  const input = c.req.valid('query');
  const schools = await fetchSchools(input);
  return c.json(schools);
});
```

## Related Skills

- `toolchains-typescript-validation-zod` - Zod validation patterns
- `toolchains-nextjs-core` - Next.js App Router patterns
- `toolchains-universal-security-api-review` - API security testing
- `universal-verification-pre-merge` - Pre-merge verification workflows
