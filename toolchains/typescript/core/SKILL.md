---
name: typescript-core
description: Advanced TypeScript patterns and best practices for 2025. Use when working with TypeScript projects requiring type system mastery (generics, conditional types, mapped types), tsconfig optimization, runtime validation integration (Zod, TypeBox, Valibot), or type-safe API patterns. Essential for Next.js, Node.js, and full-stack TypeScript development.
---

# TypeScript Core Patterns

Modern TypeScript development patterns for type safety, runtime validation, and optimal configuration.

## Quick Reference

### tsconfig.json 2025 Baseline

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

### Key Compiler Options

| Option | Purpose | When to Enable |
|--------|---------|----------------|
| `noUncheckedIndexedAccess` | Forces null checks on array/object access | Always for safety |
| `exactOptionalPropertyTypes` | Distinguishes `undefined` from missing | APIs with optional fields |
| `verbatimModuleSyntax` | Enforces explicit type-only imports | ESM projects |
| `erasableSyntaxOnly` | Node.js 22+ native TS support | Type stripping environments |

## Core Type Patterns

### Const Type Parameters

Preserve literal types through generic functions:

```typescript
function createConfig<const T extends Record<string, unknown>>(config: T): T {
  return config;
}

const config = createConfig({ 
  apiUrl: "https://api.example.com", 
  timeout: 5000 
});
// Type: { readonly apiUrl: "https://api.example.com"; readonly timeout: 5000 }
```

### Satisfies Operator

Validate against a type while preserving literal inference:

```typescript
type Route = { path: string; children?: Routes };
type Routes = Record<string, Route>;

const routes = {
  AUTH: { path: "/auth" },
  HOME: { path: "/" }
} satisfies Routes;

routes.AUTH.path;     // Type: "/auth" (literal preserved)
routes.NONEXISTENT;   // ❌ Type error
```

### Template Literal Types

Type-safe string manipulation and route extraction:

```typescript
type ExtractParams<T extends string> = 
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type Params = ExtractParams<"/users/:id/posts/:postId">; // "id" | "postId"
```

### Discriminated Unions with Exhaustiveness

```typescript
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>): T {
  if (result.success) return result.data;
  throw result.error;
}

// Exhaustiveness checking
type Action = 
  | { type: 'create'; payload: string }
  | { type: 'delete'; id: number };

function handle(action: Action) {
  switch (action.type) {
    case 'create': return action.payload;
    case 'delete': return action.id;
    default: {
      const _exhaustive: never = action;
      throw new Error(`Unhandled: ${_exhaustive}`);
    }
  }
}
```

## Runtime Validation

### Choosing a Library

| Feature | **Zod** | **TypeBox** | **Valibot** |
|---------|---------|-------------|-------------|
| Bundle Size | ~13.5kB | ~8kB | **~1.4kB** |
| Runtime Speed | Baseline | **~10x faster** | ~2x faster |
| JSON Schema | Via converter | **Native** | Via converter |
| Best For | Full-stack, tRPC | OpenAPI, Fastify | Edge functions |

### Zod Patterns (Default Choice)

```typescript
import { z } from "zod";

// Basic schema with inference
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(["admin", "user", "guest"]),
  metadata: z.record(z.unknown()).optional(),
});

type User = z.infer<typeof UserSchema>;

// Transform and refine
const ApiResponseSchema = z.object({
  data: z.array(UserSchema),
  pagination: z.object({
    page: z.coerce.number().positive(),
    total: z.coerce.number().nonnegative(),
  }),
});

// Parse with error handling
function parseUser(input: unknown): User {
  return UserSchema.parse(input); // Throws ZodError
}

function safeParseUser(input: unknown): Result<User, z.ZodError> {
  const result = UserSchema.safeParse(input);
  return result.success 
    ? { success: true, data: result.data }
    : { success: false, error: result.error };
}
```

### TypeBox Patterns (Performance-Critical)

```typescript
import { Type, Static } from "@sinclair/typebox";
import { TypeCompiler } from "@sinclair/typebox/compiler";

const UserSchema = Type.Object({
  id: Type.String({ format: "uuid" }),
  email: Type.String({ format: "email" }),
  role: Type.Union([
    Type.Literal("admin"),
    Type.Literal("user"),
    Type.Literal("guest"),
  ]),
});

type User = Static<typeof UserSchema>;

// Compile for 10x faster validation
const CompiledUser = TypeCompiler.Compile(UserSchema);

function validateUser(input: unknown): input is User {
  return CompiledUser.Check(input);
}

// Get JSON Schema for OpenAPI
const jsonSchema = UserSchema; // Already JSON Schema compliant
```

## Navigation

### Detailed References

- **[📐 Advanced Types](./references/advanced-types.md)** - Conditional types, mapped types, infer keyword, recursive types. Load when building complex type utilities or generic libraries.

- **[⚙️ Configuration](./references/configuration.md)** - Complete tsconfig.json guide, project references, monorepo patterns. Load when setting up new projects or optimizing builds.

- **[🔒 Runtime Validation](./references/runtime-validation.md)** - Zod, TypeBox, Valibot deep patterns, error handling, integration strategies. Load when implementing API validation or form handling.

## Red Flags

**Stop and reconsider if:**
- Using `any` instead of `unknown` for external data
- Casting with `as` without runtime validation
- Disabling strict mode for convenience
- Using `@ts-ignore` without clear justification
- Index access without `noUncheckedIndexedAccess`

## Integration with Other Skills

- **nextjs-core**: Type-safe Server Actions and route handlers
- **nextjs-v16**: Async API patterns and Cache Components typing
- **mcp-builder**: Zod schemas for MCP tool inputs

## Related Skills

When using Core, these skills enhance your workflow:
- **react**: TypeScript with React: component typing, hooks, generics
- **nextjs**: TypeScript in Next.js: Server Components, Server Actions typing
- **drizzle**: Type-safe database queries with Drizzle ORM
- **prisma**: Prisma's generated TypeScript types for database schemas

[Full documentation available in these skills if deployed in your bundle]
