---
name: typescript-core
description: "Advanced TypeScript patterns and best practices for 2025"
user-invocable: false
disable-model-invocation: true
progressive_disclosure:
  entry_point:
    summary: "Type-safe TypeScript patterns with optimal tsconfig, runtime validation, and modern TS 5.2+ features"
    when_to_use: "When working with TypeScript requiring advanced types, strict configuration, runtime validation, or modern language features (using, decorators)"
    quick_start: "1. Start with tsconfig baseline 2. Apply core type patterns (const, satisfies) 3. Integrate runtime validation (Zod/TypeBox) 4. Use modern features (using, decorators) as needed"
  references:
    - advanced-types.md
    - configuration.md
    - runtime-validation.md
    - advanced-patterns-2025.md
    - decision-trees.md
    - troubleshooting.md
---

# TypeScript Core Patterns

Modern TypeScript development patterns for type safety, runtime validation, and optimal configuration.

## Quick Start

**New Project:** Use 2025 tsconfig → Enable `strict` + `noUncheckedIndexedAccess` → Choose Zod for validation

**Existing Project:** Enable `strict: false` initially → Fix `any` with `unknown` → Add `noUncheckedIndexedAccess`

**API Development:** Zod schemas at boundaries → `z.infer<typeof Schema>` for types → `satisfies` for routes

**Library Development:** Enable `declaration: true` → Use `const` type parameters → See [advanced-patterns-2025.md](./references/advanced-patterns-2025.md)

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

## Local Baselines

See `references/configuration.md` for repo-specific tsconfig patterns (CommonJS CLI, NodeNext strict, Next.js bundler).

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

TypeScript types disappear at runtime. Use validation libraries for external data (APIs, forms, config files).

### Quick Comparison

| Library | Bundle Size | Speed | Best For |
|---------|-------------|-------|----------|
| **Zod** | ~13.5kB | Baseline | Full-stack apps, tRPC integration |
| **TypeBox** | ~8kB | ~10x faster | OpenAPI, performance-critical |
| **Valibot** | ~1.4kB | ~2x faster | Edge functions, minimal bundles |

### Basic Pattern (Zod)

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(["admin", "user", "guest"]),
});

type User = z.infer<typeof UserSchema>;

// Validate external data
function parseUser(input: unknown): User {
  return UserSchema.parse(input);
}
```

**→ See [runtime-validation.md](./references/runtime-validation.md) for complete Zod, TypeBox, and Valibot patterns**

## Decision Support

### Quick Decision Guide

**Need to choose between `type` vs `interface`?**
- Public API / library types → `interface`
- Union types / mapped types → `type`
- Simple object shapes → `interface` (default)

**Need generics or union types?**
- Output type depends on input type → Generics
- Fixed set of known types → Union types
- Building reusable data structures → Generics

**Dealing with unknown data?**
- External data (API, user input) → `unknown` (type-safe)
- Rapid prototyping / migration → `any` (temporarily)

**Need runtime validation?**
- Full-stack TypeScript with tRPC → Zod
- OpenAPI / high performance → TypeBox
- Edge functions / minimal bundle → Valibot

**→ See [decision-trees.md](./references/decision-trees.md) for comprehensive decision frameworks**

## Troubleshooting

### Common Issues Quick Reference

**Property does not exist on type** → Define proper interface or use optional properties

**Type is not assignable** → Fix property types or use runtime validation (Zod)

**Object is possibly 'undefined'** → Use optional chaining (`?.`) or type guards

**Cannot find module** → Check file extensions (.js for ESM) and module resolution

**Slow compilation** → Enable `incremental`, use `skipLibCheck`, consider esbuild/swc

**→ See [troubleshooting.md](./references/troubleshooting.md) for detailed solutions with examples**

## Navigation

### Detailed References

- **[📐 Advanced Types](./references/advanced-types.md)** - Conditional types, mapped types, infer keyword, recursive types. Load when building complex type utilities or generic libraries.

- **[⚙️ Configuration](./references/configuration.md)** - Complete tsconfig.json guide, project references, monorepo patterns. Load when setting up new projects or optimizing builds.

- **[🔒 Runtime Validation](./references/runtime-validation.md)** - Zod, TypeBox, Valibot deep patterns, error handling, integration strategies. Load when implementing API validation or form handling.

- **[✨ Advanced Patterns 2025](./references/advanced-patterns-2025.md)** - TypeScript 5.2+ features: `using` keyword, stable decorators, import type behavior, satisfies with generics. Load when using modern language features.

- **[🌳 Decision Trees](./references/decision-trees.md)** - Clear decision frameworks for `type` vs `interface`, generics vs unions, `unknown` vs `any`, validation library selection, type narrowing strategies, and module resolution. Load when making TypeScript design decisions.

- **[🔧 Troubleshooting](./references/troubleshooting.md)** - Common TypeScript errors and fixes, type inference issues, module resolution problems, tsconfig misconfigurations, build performance optimization, and type compatibility errors. Load when debugging TypeScript issues.

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
