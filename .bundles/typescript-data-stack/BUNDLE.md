# TypeScript Data Stack

**Version:** 1.0.0
**Category:** TypeScript
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Type-safe database access layer for TypeScript projects with multiple ORM options and migration strategies. Ideal for Node.js backends, Next.js applications, and full-stack TypeScript projects requiring robust data persistence.

## Included Skills

- **kysely** (toolchains/typescript/data/kysely) - Type-safe SQL query builder
- **drizzle** (toolchains/typescript/data/drizzle) - TypeScript-first ORM with migrations
- **prisma** (toolchains/typescript/data/prisma) - Next-gen ORM with client generation
- **zod** (toolchains/typescript/validation/zod) - Schema validation with type inference
- **database-migration** (universal/data/database-migration) - Migration best practices

## Use Cases

**When to Deploy This Bundle:**
- Building Node.js backends with TypeScript
- Next.js full-stack applications with database
- Projects requiring type-safe database queries
- Teams evaluating ORM options (Kysely vs Drizzle vs Prisma)
- Applications with complex data validation requirements

**What You Get:**
- Multiple ORM patterns and comparison guidance
- Type-safe query builders with IntelliSense
- Schema migration strategies across ORMs
- Zod integration for runtime validation
- Database connection pooling patterns

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| kysely | ✅ Yes | 🚀 Enhanced | None (choose one ORM) |
| drizzle | ✅ Yes | 🚀 Enhanced | None (choose one ORM) |
| prisma | ✅ Yes | 🚀 Enhanced | None (choose one ORM) |
| zod | ✅ Yes | 🚀 Enhanced | None |
| database-migration | ✅ Yes | 🚀 Enhanced | Any ORM above |

**Bundle Synergies:**
- Kysely/Drizzle/Prisma + Zod: Runtime validation with compile-time types
- Drizzle + Zod: Shared schema definitions
- Any ORM + database-migration: Consistent migration patterns

**ORM Selection Guide:**
- **Kysely**: Maximum control, raw SQL-like, minimal magic
- **Drizzle**: Balance of type safety and DX, Zod-like API
- **Prisma**: Fastest setup, great for rapid prototyping, opinionated

## Integration Example

```typescript
// Drizzle + Zod example
import { drizzle } from 'drizzle-orm/node-postgres';
import { pgTable, serial, text } from 'drizzle-orm/pg-core';
import { z } from 'zod';

// Drizzle schema
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull(),
  name: text('name'),
});

// Zod validation schema
export const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).optional(),
});

// Type-safe insert
const newUser = userSchema.parse(input);
await db.insert(users).values(newUser);
```

## Version History

- **1.0.0** (2025-11-30): Initial release with 5 data layer skills
