---
name: prisma-orm
description: Prisma ORM for TypeScript - Type-safe database toolkit with schema-first development, auto-generated client, migrations, relations, and Prisma Studio. Use when building Node.js or Next.js apps requiring database access with full type safety, complex relations, transactions, or when both development tools (Studio) and production performance are needed.
---

# Prisma ORM - Type-Safe Database Toolkit

Modern database toolkit for TypeScript with schema-first development, auto-generated type-safe client, and powerful migration system.

## Quick Reference

### Installation

```bash
npm install prisma @prisma/client
npx prisma init
```

### Basic Workflow

```bash
# 1. Define schema
# Edit prisma/schema.prisma

# 2. Create migration
npx prisma migrate dev --name init

# 3. Generate client
npx prisma generate

# 4. Open Studio
npx prisma studio
```

### Core Schema Pattern

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
}
```

### Type-Safe CRUD

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Create
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
    posts: {
      create: { title: 'First Post', content: 'Hello World' }
    }
  },
  include: { posts: true }
});

// Read with filters
const users = await prisma.user.findMany({
  where: { email: { contains: '@example.com' } },
  include: { posts: { where: { published: true } } },
  orderBy: { createdAt: 'desc' },
  take: 10
});

// Update
await prisma.user.update({
  where: { id: userId },
  data: { name: 'Bob' }
});

// Delete
await prisma.user.delete({ where: { id: userId } });
```

## Schema Design Patterns

### Field Types and Attributes

```prisma
model Product {
  id          Int      @id @default(autoincrement())
  sku         String   @unique
  name        String
  description String?  // Optional field
  price       Decimal  @db.Decimal(10, 2)
  inStock     Boolean  @default(true)
  quantity    Int      @default(0)
  tags        String[] // Array field (PostgreSQL)
  metadata    Json?    // JSON field
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([sku])
  @@index([name, inStock])
}
```

### Relations

**One-to-Many:**
```prisma
model User {
  id    String @id @default(cuid())
  posts Post[]
}

model Post {
  id       String @id @default(cuid())
  author   User   @relation(fields: [authorId], references: [id])
  authorId String

  @@index([authorId])
}
```

**Many-to-Many:**
```prisma
model Post {
  id         String     @id @default(cuid())
  categories Category[] @relation("PostCategories")
}

model Category {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[] @relation("PostCategories")
}
```

**One-to-One:**
```prisma
model User {
  id      String   @id @default(cuid())
  profile Profile?
}

model Profile {
  id     String @id @default(cuid())
  bio    String
  user   User   @relation(fields: [userId], references: [id])
  userId String @unique
}
```

**Self-Relations:**
```prisma
model User {
  id        String @id @default(cuid())
  following User[] @relation("UserFollows")
  followers User[] @relation("UserFollows")
}
```

## Client Operations

### Nested Writes

```typescript
// Create with nested relations
const user = await prisma.user.create({
  data: {
    email: 'bob@example.com',
    profile: {
      create: { bio: 'Software Engineer' }
    },
    posts: {
      create: [
        { title: 'Post 1', content: 'Content 1' },
        { title: 'Post 2', content: 'Content 2' }
      ]
    }
  }
});

// Update with nested operations
await prisma.user.update({
  where: { id: userId },
  data: {
    posts: {
      create: { title: 'New Post' },
      update: {
        where: { id: postId },
        data: { published: true }
      },
      delete: { id: oldPostId }
    }
  }
});
```

### Transactions

**Sequential (Interactive):**
```typescript
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'alice@example.com' }
  });

  await tx.post.create({
    data: { title: 'Post', authorId: user.id }
  });

  // Rollback if error thrown
  if (someCondition) {
    throw new Error('Rollback transaction');
  }
});
```

**Batch (Parallel):**
```typescript
const [deletedPosts, updatedUser] = await prisma.$transaction([
  prisma.post.deleteMany({ where: { published: false } }),
  prisma.user.update({
    where: { id: userId },
    data: { name: 'Updated' }
  })
]);
```

### Advanced Queries

**Aggregations:**
```typescript
const result = await prisma.post.aggregate({
  _count: { id: true },
  _avg: { views: true },
  _sum: { likes: true },
  _max: { createdAt: true },
  where: { published: true }
});

const grouped = await prisma.post.groupBy({
  by: ['authorId'],
  _count: { id: true },
  _avg: { views: true },
  having: { views: { _avg: { gt: 100 } } }
});
```

**Raw SQL:**
```typescript
// Raw query
const users = await prisma.$queryRaw<User[]>`
  SELECT * FROM "User" WHERE email LIKE ${`%${search}%`}
`;

// Execute
await prisma.$executeRaw`
  UPDATE "Post" SET views = views + 1 WHERE id = ${postId}
`;
```

## Migrations

### Development Workflow

```bash
# Create and apply migration
npx prisma migrate dev --name add_user_role

# Reset database (WARNING: deletes all data)
npx prisma migrate reset

# View migration status
npx prisma migrate status
```

### Production Deployment

```bash
# Apply pending migrations
npx prisma migrate deploy

# Generate client (in CI/CD)
npx prisma generate
```

### Schema Prototyping

```bash
# Push schema without migrations (dev only)
npx prisma db push

# Pull schema from existing database
npx prisma db pull
```

## Integration Patterns

### Next.js App Router

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

**Server Component:**
```typescript
// app/users/page.tsx
import { prisma } from '@/lib/prisma';

export default async function UsersPage() {
  const users = await prisma.user.findMany({
    include: { posts: { take: 5 } }
  });

  return (
    <ul>
      {users.map(u => (
        <li key={u.id}>{u.name} - {u.posts.length} posts</li>
      ))}
    </ul>
  );
}
```

**Server Action:**
```typescript
// app/actions.ts
'use server';

import { prisma } from '@/lib/prisma';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const authorId = formData.get('authorId') as string;

  await prisma.post.create({
    data: { title, authorId }
  });

  revalidatePath('/posts');
}
```

### Node.js Middleware

```typescript
import { PrismaClient } from '@prisma/client';
import express from 'express';

const app = express();
const prisma = new PrismaClient();

app.get('/users/:id', async (req, res) => {
  const user = await prisma.user.findUnique({
    where: { id: req.params.id },
    include: { posts: true }
  });

  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});

app.listen(3000);
```

## Performance Optimization

### Query Optimization

```typescript
// ❌ N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({
    where: { authorId: user.id }
  });
}

// ✅ Single query with include
const users = await prisma.user.findMany({
  include: { posts: true }
});

// ✅ Select specific fields
const users = await prisma.user.findMany({
  select: { id: true, email: true, posts: { select: { title: true } } }
});
```

### Pagination

```typescript
// Cursor-based (recommended for large datasets)
const posts = await prisma.post.findMany({
  take: 10,
  cursor: lastPostId ? { id: lastPostId } : undefined,
  skip: lastPostId ? 1 : 0,
  orderBy: { createdAt: 'desc' }
});

// Offset-based (simple but slower)
const posts = await prisma.post.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize
});
```

### Connection Pooling

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")

  // Connection pool settings
  directUrl = env("DIRECT_URL")

  // Serverless connection limit
  relationMode = "prisma" // For PlanetScale, Neon
}
```

```bash
# .env
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=10&pool_timeout=20"
```

## Prisma Studio

```bash
# Launch visual database browser
npx prisma studio
```

**Features:**
- Visual data browser and editor
- Create, read, update, delete records
- Filter and search data
- View relations visually
- Runs on `localhost:5555`

## Prisma vs Drizzle

| Feature | **Prisma** | **Drizzle** |
|---------|------------|-------------|
| Schema Definition | Custom DSL | TypeScript code |
| Type Safety | Generated types | Inferred types |
| Migrations | Built-in (migrate) | drizzle-kit |
| Query Builder | Fluent API | SQL-like builders |
| Relations | Automatic | Manual joins |
| Studio | Built-in GUI | No GUI |
| Bundle Size | ~300kB | ~50kB |
| Raw SQL | Supported | First-class |
| Edge Runtime | Limited | Full support |
| Learning Curve | Moderate | Steeper |
| **Best For** | Full-stack apps, rapid development, teams | Edge functions, SQL experts, bundle-sensitive |

**Choose Prisma when:**
- Team prefers schema-first development
- Need visual database tools (Studio)
- Want automatic relation handling
- Building full-stack monoliths
- Rapid prototyping and migrations

**Choose Drizzle when:**
- Need minimal bundle size (edge functions)
- Prefer SQL-like syntax
- Edge runtime deployment (Cloudflare Workers)
- Want full control over SQL generation
- Team has strong SQL expertise

## Best Practices

1. **Singleton Pattern** - Reuse `PrismaClient` instance (especially in dev)
2. **Connection Management** - Configure pool size for serverless
3. **Select Specific Fields** - Use `select` to reduce payload size
4. **Use Transactions** - For multi-step operations requiring atomicity
5. **Index Strategically** - Add `@@index` on frequently queried fields
6. **Migration Discipline** - Never edit migrations after deployment
7. **Schema Versioning** - Use descriptive migration names
8. **Soft Deletes** - Add `deletedAt` field instead of hard deletes
9. **Validate Before Saving** - Use Zod schemas before Prisma operations
10. **Monitor Queries** - Use `prisma.$on('query')` for logging

## Common Pitfalls

❌ **Creating multiple PrismaClient instances:**
```typescript
// WRONG - creates connection leak
function getUser() {
  const prisma = new PrismaClient(); // New instance every call
  return prisma.user.findMany();
}

// CORRECT - singleton pattern
const prisma = new PrismaClient();
function getUser() {
  return prisma.user.findMany();
}
```

❌ **N+1 queries:**
```typescript
// WRONG - multiple queries
const users = await prisma.user.findMany();
for (const user of users) {
  user.posts = await prisma.post.findMany({ where: { authorId: user.id } });
}

// CORRECT - single query with include
const users = await prisma.user.findMany({ include: { posts: true } });
```

❌ **Missing transaction for multi-step operations:**
```typescript
// WRONG - not atomic, can leave inconsistent state
await prisma.user.delete({ where: { id: userId } });
await prisma.post.deleteMany({ where: { authorId: userId } }); // May fail

// CORRECT - atomic transaction
await prisma.$transaction([
  prisma.post.deleteMany({ where: { authorId: userId } }),
  prisma.user.delete({ where: { id: userId } })
]);
```

## Red Flags

**Stop and reconsider if:**
- Creating new `PrismaClient` in request handlers
- Not using transactions for multi-step operations
- Missing indexes on foreign keys or frequently queried fields
- Using `findMany` without pagination on large tables
- Fetching entire objects when only specific fields needed
- Not handling connection errors in production
- Using `migrate dev` in production (use `migrate deploy`)

## Integration with Other Skills

- **typescript-core**: Zod validation, type safety patterns
- **nextjs-core**: Server Actions, Server Components integration
- **nextjs-v16**: App Router data fetching, caching
- **database-migration**: Safe schema evolution patterns

## Resources

- **Documentation**: https://www.prisma.io/docs
- **Schema Reference**: https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference
- **Client API**: https://www.prisma.io/docs/reference/api-reference/prisma-client-reference
- **Examples**: https://github.com/prisma/prisma-examples

## Related Skills

When using Prisma, these skills enhance your workflow:
- **drizzle**: Drizzle ORM as lightweight alternative to Prisma
- **typescript**: TypeScript best practices for Prisma generated types
- **nextjs**: Prisma with Next.js: connection pooling, edge runtime considerations
- **test-driven-development**: Testing Prisma models, migrations, and queries

[Full documentation available in these skills if deployed in your bundle]
