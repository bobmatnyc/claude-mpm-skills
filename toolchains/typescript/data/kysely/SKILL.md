---
name: kysely
description: Kysely type-safe SQL query builder - End-to-end type safety from schema to queries, migrations, transactions, plugins
version: 1.0.0
category: development
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Type-safe SQL query builder: full TypeScript inference, schema generation, migrations, no ORM overhead, raw SQL when needed"
    when_to_use: "Building type-safe database layers, migrating from ORMs, need raw SQL control with types, PostgreSQL/MySQL/SQLite apps"
    quick_start: "1. Define schema types 2. Create Kysely instance 3. Chain .selectFrom().where().execute() 4. Full type inference"
context_limit: 700
tags:
  - typescript
  - database
  - sql
  - query-builder
  - type-safe
  - kysely
  - orm-alternative
requires_tools: []
---

# Kysely - Type-Safe SQL Query Builder

## Overview

Kysely is a type-safe TypeScript SQL query builder that provides end-to-end type safety from database schema to query results. Unlike ORMs, it generates plain SQL and gives you full control while maintaining perfect TypeScript inference.

**Key Features**:
- Complete type inference (schema → queries → results)
- Zero runtime overhead (compiles to SQL)
- Database-agnostic (PostgreSQL, MySQL, SQLite, MSSQL)
- Migration system included
- Plugin ecosystem (CTEs, JSON, geospatial)
- Raw SQL integration when needed

**Installation**:
```bash
npm install kysely
# Database driver (choose one)
npm install pg              # PostgreSQL
npm install mysql2          # MySQL
npm install better-sqlite3  # SQLite
```

## Quick Start

### 1. Define Database Schema Types

```typescript
import { Generated, Selectable, Insertable, Updateable } from 'kysely';

// Table interface (all columns)
interface UserTable {
  id: Generated<number>;
  email: string;
  name: string | null;
  created_at: Generated<Date>;
  updated_at: Date;
}

interface PostTable {
  id: Generated<number>;
  user_id: number;
  title: string;
  content: string;
  published: Generated<boolean>;
  created_at: Generated<Date>;
}

// Database interface
interface Database {
  users: UserTable;
  posts: PostTable;
}

// Type-safe query result types
type User = Selectable<UserTable>;
type NewUser = Insertable<UserTable>;
type UserUpdate = Updateable<UserTable>;
```

### 2. Create Database Instance

```typescript
import { Kysely, PostgresDialect } from 'kysely';
import { Pool } from 'pg';

const db = new Kysely<Database>({
  dialect: new PostgresDialect({
    pool: new Pool({
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      max: 10,
    }),
  }),
});
```

### 3. Type-Safe Queries

```typescript
// SELECT with full type inference
const users = await db
  .selectFrom('users')
  .select(['id', 'email', 'name'])
  .where('created_at', '>', new Date('2024-01-01'))
  .execute();
// Type: Array<{ id: number; email: string; name: string | null }>

// INSERT with type checking
const newUser: NewUser = {
  email: 'alice@example.com',
  name: 'Alice',
  updated_at: new Date(),
};

const inserted = await db
  .insertInto('users')
  .values(newUser)
  .returningAll()
  .executeTakeFirstOrThrow();
// Type: User

// UPDATE
await db
  .updateTable('users')
  .set({ name: 'Alice Updated', updated_at: new Date() })
  .where('id', '=', 1)
  .execute();

// DELETE
await db
  .deleteFrom('users')
  .where('email', 'like', '%@spam.com')
  .execute();
```

## Advanced Query Patterns

### Joins with Type Safety

```typescript
// INNER JOIN
const usersWithPosts = await db
  .selectFrom('users')
  .innerJoin('posts', 'posts.user_id', 'users.id')
  .select([
    'users.id',
    'users.name',
    'posts.title',
    'posts.content',
  ])
  .execute();
// Type: Array<{ id: number; name: string | null; title: string; content: string }>

// LEFT JOIN with null handling
const usersWithOptionalPosts = await db
  .selectFrom('users')
  .leftJoin('posts', 'posts.user_id', 'users.id')
  .select([
    'users.id',
    'users.email',
    'posts.title',  // Type: string | null (from LEFT JOIN)
  ])
  .execute();

// Multiple joins
const complexQuery = await db
  .selectFrom('posts')
  .innerJoin('users', 'users.id', 'posts.user_id')
  .leftJoin('comments', 'comments.post_id', 'posts.id')
  .select([
    'posts.id as postId',
    'posts.title',
    'users.name as authorName',
    'comments.id as commentId',
  ])
  .execute();
```

### Aggregations and Grouping

```typescript
import { sql } from 'kysely';

// COUNT, AVG, SUM
const stats = await db
  .selectFrom('posts')
  .select([
    'user_id',
    db.fn.count<number>('id').as('post_count'),
    db.fn.avg<number>('views').as('avg_views'),
  ])
  .groupBy('user_id')
  .having(db.fn.count('id'), '>', 5)
  .execute();
// Type: Array<{ user_id: number; post_count: number; avg_views: number }>

// Complex aggregations with raw SQL
const advanced = await db
  .selectFrom('users')
  .select([
    'users.id',
    sql<number>`COUNT(DISTINCT posts.id)`.as('total_posts'),
    sql<Date>`MAX(posts.created_at)`.as('latest_post'),
  ])
  .leftJoin('posts', 'posts.user_id', 'users.id')
  .groupBy('users.id')
  .execute();
```

### Subqueries

```typescript
// Scalar subquery
const usersWithPostCount = await db
  .selectFrom('users')
  .select([
    'users.id',
    'users.name',
    (eb) =>
      eb
        .selectFrom('posts')
        .select(eb.fn.count<number>('id').as('count'))
        .whereRef('posts.user_id', '=', 'users.id')
        .as('post_count'),
  ])
  .execute();

// EXISTS subquery
const activeUsers = await db
  .selectFrom('users')
  .selectAll()
  .where((eb) =>
    eb.exists(
      eb
        .selectFrom('posts')
        .select('id')
        .whereRef('posts.user_id', '=', 'users.id')
        .where('created_at', '>', new Date('2024-01-01'))
    )
  )
  .execute();

// IN subquery
const usersInTopTier = await db
  .selectFrom('users')
  .selectAll()
  .where(
    'id',
    'in',
    db.selectFrom('posts')
      .select('user_id')
      .groupBy('user_id')
      .having(db.fn.count('id'), '>', 100)
  )
  .execute();
```

### Common Table Expressions (CTEs)

```typescript
// WITH clause
const result = await db
  .with('popular_posts', (db) =>
    db
      .selectFrom('posts')
      .select(['id', 'user_id', 'title'])
      .where('views', '>', 1000)
  )
  .with('active_users', (db) =>
    db
      .selectFrom('users')
      .select(['id', 'email'])
      .where('last_login', '>', new Date('2024-01-01'))
  )
  .selectFrom('popular_posts')
  .innerJoin('active_users', 'active_users.id', 'popular_posts.user_id')
  .selectAll()
  .execute();

// Recursive CTE (organizational hierarchy)
interface OrgNode {
  id: number;
  name: string;
  parent_id: number | null;
  level: number;
}

const hierarchy = await db
  .withRecursive('org_tree', (db) =>
    db
      .selectFrom('departments')
      .select(['id', 'name', 'parent_id', sql<number>`0`.as('level')])
      .where('parent_id', 'is', null)
      .unionAll(
        db
          .selectFrom('departments')
          .innerJoin('org_tree', 'org_tree.id', 'departments.parent_id')
          .select([
            'departments.id',
            'departments.name',
            'departments.parent_id',
            sql<number>`org_tree.level + 1`.as('level'),
          ])
      )
  )
  .selectFrom('org_tree')
  .selectAll()
  .execute();
```

## Schema Generation from Database

### Using kysely-codegen

```bash
# Install
npm install --save-dev kysely-codegen

# Generate types from existing database
npx kysely-codegen --url "postgresql://user:pass@localhost:5432/mydb"
```

Generated output:
```typescript
// Generated by kysely-codegen
import type { ColumnType, Generated } from 'kysely';

export interface Database {
  users: UsersTable;
  posts: PostsTable;
  comments: CommentsTable;
}

export interface UsersTable {
  id: Generated<number>;
  email: string;
  name: string | null;
  created_at: Generated<Date>;
}

export interface PostsTable {
  id: Generated<number>;
  user_id: number;
  title: string;
  content: string;
  published: Generated<boolean>;
  created_at: Generated<Date>;
}
```

### Custom Type Mapping

```typescript
// Map database types to TypeScript types
interface CustomTypes {
  timestamp: Date;
  jsonb: unknown;
  numeric: string; // Preserve precision
  uuid: string;
}

interface ProductTable {
  id: ColumnType<string, string | undefined, string>; // SELECT, INSERT, UPDATE types
  metadata: ColumnType<Record<string, unknown>, string, string>; // JSON column
  price: ColumnType<number, number, number | undefined>; // Numeric
}
```

## Migrations

### Migration Setup

```typescript
import { Kysely, Migrator, FileMigrationProvider } from 'kysely';
import { promises as fs } from 'fs';
import * as path from 'path';

const migrator = new Migrator({
  db,
  provider: new FileMigrationProvider({
    fs,
    path,
    migrationFolder: path.join(__dirname, 'migrations'),
  }),
});

// Run all pending migrations
async function migrateToLatest() {
  const { error, results } = await migrator.migrateToLatest();

  results?.forEach((it) => {
    if (it.status === 'Success') {
      console.log(`Migration "${it.migrationName}" executed successfully`);
    } else if (it.status === 'Error') {
      console.error(`Migration "${it.migrationName}" failed`);
    }
  });

  if (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  }
}

// Rollback last migration
async function migrateDown() {
  const { error, results } = await migrator.migrateDown();
  // Handle results...
}
```

### Migration Files

```typescript
// migrations/001_create_users.ts
import { Kysely, sql } from 'kysely';

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('users')
    .addColumn('id', 'serial', (col) => col.primaryKey())
    .addColumn('email', 'varchar(255)', (col) => col.notNull().unique())
    .addColumn('name', 'varchar(255)')
    .addColumn('created_at', 'timestamp', (col) =>
      col.defaultTo(sql`CURRENT_TIMESTAMP`).notNull()
    )
    .execute();

  await db.schema
    .createIndex('users_email_idx')
    .on('users')
    .column('email')
    .execute();
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('users').execute();
}
```

### Complex Migration Examples

```typescript
// Add foreign key
export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('posts')
    .addColumn('id', 'serial', (col) => col.primaryKey())
    .addColumn('user_id', 'integer', (col) =>
      col.references('users.id').onDelete('cascade').notNull()
    )
    .addColumn('title', 'varchar(500)', (col) => col.notNull())
    .addColumn('content', 'text')
    .execute();
}

// Alter table
export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .alterTable('users')
    .addColumn('bio', 'text')
    .execute();

  await db.schema
    .alterTable('users')
    .modifyColumn('email', 'varchar(320)')
    .execute();
}

// Add enum column (PostgreSQL)
export async function up(db: Kysely<any>): Promise<void> {
  await sql`CREATE TYPE user_role AS ENUM ('admin', 'user', 'guest')`.execute(db);

  await db.schema
    .alterTable('users')
    .addColumn('role', sql`user_role`, (col) => col.defaultTo('user'))
    .execute();
}
```

## Transactions

### Basic Transactions

```typescript
// Automatic rollback on error
await db.transaction().execute(async (trx) => {
  await trx
    .insertInto('users')
    .values({ email: 'alice@example.com', name: 'Alice', updated_at: new Date() })
    .execute();

  await trx
    .insertInto('posts')
    .values({ user_id: 1, title: 'First Post', content: 'Hello' })
    .execute();
});

// Manual transaction control
const trx = await db.transaction().execute(async (trx) => {
  const user = await trx
    .insertInto('users')
    .values({ email: 'bob@example.com', name: 'Bob', updated_at: new Date() })
    .returningAll()
    .executeTakeFirstOrThrow();

  const post = await trx
    .insertInto('posts')
    .values({
      user_id: user.id,
      title: 'Bob\'s Post',
      content: 'Content',
    })
    .returningAll()
    .executeTakeFirstOrThrow();

  return { user, post };
});
```

### Isolation Levels

```typescript
import { IsolationLevel } from 'kysely';

// Read committed (default)
await db.transaction()
  .setIsolationLevel('read committed')
  .execute(async (trx) => {
    // Transaction logic
  });

// Serializable (strongest isolation)
await db.transaction()
  .setIsolationLevel('serializable')
  .execute(async (trx) => {
    const balance = await trx
      .selectFrom('accounts')
      .select('balance')
      .where('id', '=', accountId)
      .executeTakeFirstOrThrow();

    await trx
      .updateTable('accounts')
      .set({ balance: balance.balance - amount })
      .where('id', '=', accountId)
      .execute();
  });
```

## Raw SQL Integration

### Using sql Template Tag

```typescript
import { sql } from 'kysely';

// Raw SQL in SELECT
const result = await db
  .selectFrom('users')
  .select([
    'id',
    sql<string>`UPPER(name)`.as('uppercase_name'),
    sql<number>`EXTRACT(YEAR FROM created_at)`.as('year_created'),
  ])
  .execute();

// Raw SQL in WHERE
const filtered = await db
  .selectFrom('posts')
  .selectAll()
  .where(sql`LOWER(title)`, 'like', '%typescript%')
  .execute();

// Complex raw queries
const custom = await sql<{ total: number; avg_age: number }>`
  SELECT
    COUNT(*) as total,
    AVG(EXTRACT(YEAR FROM age(birth_date))) as avg_age
  FROM users
  WHERE active = true
`.execute(db);
```

### Full Raw Queries

```typescript
// Execute arbitrary SQL
const result = await sql`
  WITH ranked_posts AS (
    SELECT
      p.*,
      ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY views DESC) as rank
    FROM posts p
  )
  SELECT * FROM ranked_posts WHERE rank <= 3
`.execute(db);

// Parameterized raw queries
const email = 'alice@example.com';
const user = await sql<User>`
  SELECT * FROM users WHERE email = ${email}
`.execute(db);
```

## Plugin Ecosystem

### JSON Operations (PostgreSQL)

```typescript
import { jsonBuildObject, jsonArrayFrom } from 'kysely/helpers/postgres';

// Build JSON objects
const usersWithPosts = await db
  .selectFrom('users')
  .select([
    'users.id',
    'users.name',
    jsonArrayFrom(
      db
        .selectFrom('posts')
        .select(['posts.id', 'posts.title', 'posts.content'])
        .whereRef('posts.user_id', '=', 'users.id')
    ).as('posts'),
  ])
  .execute();
// Result: { id: 1, name: "Alice", posts: [{ id: 1, title: "..." }] }

// JSON aggregation
const nested = await db
  .selectFrom('users')
  .select([
    'users.id',
    jsonBuildObject({
      name: 'users.name',
      email: 'users.email',
      postCount: sql<number>`(SELECT COUNT(*) FROM posts WHERE user_id = users.id)`,
    }).as('user_data'),
  ])
  .execute();
```

### Pagination Plugin

```typescript
import { SelectQueryBuilder } from 'kysely';

function paginate<DB, TB extends keyof DB, O>(
  query: SelectQueryBuilder<DB, TB, O>,
  page: number,
  pageSize: number
) {
  return query.limit(pageSize).offset((page - 1) * pageSize);
}

// Usage
const page = 2;
const pageSize = 20;

const users = await paginate(
  db.selectFrom('users').selectAll(),
  page,
  pageSize
).execute();

// With total count
async function paginateWithCount<DB, TB extends keyof DB, O>(
  query: SelectQueryBuilder<DB, TB, O>,
  page: number,
  pageSize: number
) {
  const [items, { count }] = await Promise.all([
    query.limit(pageSize).offset((page - 1) * pageSize).execute(),
    query.select(db.fn.count<number>('id').as('count')).executeTakeFirstOrThrow(),
  ]);

  return {
    items,
    total: count,
    page,
    pageSize,
    totalPages: Math.ceil(count / pageSize),
  };
}
```

### Full-Text Search (PostgreSQL)

```typescript
// GIN index for full-text search
export async function up(db: Kysely<any>): Promise<void> {
  await sql`
    ALTER TABLE posts
    ADD COLUMN search_vector tsvector
    GENERATED ALWAYS AS (
      to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''))
    ) STORED
  `.execute(db);

  await sql`
    CREATE INDEX posts_search_idx ON posts USING GIN (search_vector)
  `.execute(db);
}

// Full-text search query
const searchResults = await db
  .selectFrom('posts')
  .selectAll()
  .where(
    sql`search_vector`,
    '@@',
    sql`to_tsquery('english', ${query})`
  )
  .execute();
```

## Kysely vs Drizzle vs Prisma

### Feature Comparison

| Feature | **Kysely** | **Drizzle** | **Prisma** |
|---------|-----------|-------------|------------|
| **Type Safety** | Full (schema → queries) | Full (schema → queries) | Full (generated client) |
| **SQL Control** | ✅ Raw SQL friendly | ✅ Raw SQL friendly | ❌ Limited |
| **Bundle Size** | ~50kB | ~30kB | ~500kB+ |
| **Migration System** | ✅ Built-in | ✅ Built-in | ✅ Powerful CLI |
| **Query Performance** | ✅ Plain SQL | ✅ Plain SQL | ❌ Slower (abstraction) |
| **Schema Definition** | TypeScript types | TypeScript schema | Prisma schema |
| **Codegen Required** | Optional | No | ✅ Required |
| **ORM Features** | ❌ Query builder only | Partial (relational) | ✅ Full ORM |
| **Learning Curve** | Medium (SQL knowledge) | Medium | Easy (abstracts SQL) |
| **Best For** | SQL-first, complex queries | Type-safe schemas | Rapid prototyping |

### When to Choose Kysely

✅ **Choose Kysely when:**
- You know SQL and want full control
- Complex queries (CTEs, window functions, subqueries)
- Performance is critical (no ORM overhead)
- Migrating from raw SQL
- Need raw SQL escape hatch frequently
- Working with existing databases
- Bundle size matters (edge functions)

❌ **Choose Drizzle when:**
- Want declarative TypeScript schemas
- Need relational query capabilities
- Prefer ORM-like ergonomics with SQL control
- Working with new greenfield projects

❌ **Choose Prisma when:**
- Team unfamiliar with SQL
- Rapid prototyping and iteration
- Need powerful migration tooling
- Want automatic relation handling
- Prefer declarative schema language

### Migration from Prisma

```typescript
// Prisma
const users = await prisma.user.findMany({
  where: { createdAt: { gte: new Date('2024-01-01') } },
  include: { posts: true },
});

// Kysely equivalent
const users = await db
  .selectFrom('users')
  .select([
    'users.id',
    'users.email',
    jsonArrayFrom(
      db.selectFrom('posts')
        .selectAll()
        .whereRef('posts.user_id', '=', 'users.id')
    ).as('posts'),
  ])
  .where('created_at', '>=', new Date('2024-01-01'))
  .execute();
```

## Best Practices

1. **Define schema types first** - Use `Generated`, `Selectable`, `Insertable`, `Updateable`
2. **Use kysely-codegen** - Generate types from existing databases
3. **Leverage type inference** - Let TypeScript infer result types
4. **Use transactions** - For multi-step operations
5. **Raw SQL when needed** - Don't fight the query builder
6. **Paginate large results** - Use LIMIT/OFFSET or cursor-based
7. **Index frequently queried columns** - Performance is your responsibility
8. **Test migrations** - Both up and down
9. **Use CTEs for readability** - Complex queries become maintainable
10. **Connection pooling** - Configure database pool appropriately

## Common Pitfalls

❌ **Forgetting to execute queries**:
```typescript
// WRONG - returns query builder, not results
const users = db.selectFrom('users').selectAll();

// CORRECT
const users = await db.selectFrom('users').selectAll().execute();
```

❌ **Not handling null from LEFT JOIN**:
```typescript
// TypeScript knows posts.title can be null from LEFT JOIN
const result = await db
  .selectFrom('users')
  .leftJoin('posts', 'posts.user_id', 'users.id')
  .select(['users.name', 'posts.title'])
  .execute();
// posts.title type: string | null
```

❌ **Missing Generated for auto-increment columns**:
```typescript
// WRONG - TypeScript will require 'id' in INSERT
interface UserTable {
  id: number;  // Bad!
}

// CORRECT
interface UserTable {
  id: Generated<number>;  // INSERT doesn't require id
}
```

## Resources

- **Documentation**: https://kysely.dev
- **GitHub**: https://github.com/kysely-org/kysely
- **Discord**: https://discord.gg/kysely
- **kysely-codegen**: https://github.com/RobinBlomberg/kysely-codegen
- **Playground**: https://kysely-org.github.io/kysely-playground/

## Related Skills

When using Kysely, consider these complementary skills:

- **typescript-core**: TypeScript type system, advanced patterns, and tsconfig optimization
- **database-migration**: Safe schema evolution patterns for production databases
- **Node.js backend**: Server setup, connection pooling, and database configuration

### Quick TypeScript Type System Reference (Inlined for Standalone Use)

```typescript
// Kysely leverages advanced TypeScript features
import { Kysely, Generated, ColumnType } from 'kysely';

// Database interface with Generated types
interface Database {
  users: {
    id: Generated<number>;  // Auto-generated by database
    email: string;
    created_at: ColumnType<Date, string | undefined, never>;
    // ColumnType<SelectType, InsertType, UpdateType>
  };
}

// Type inference in queries
const db = new Kysely<Database>({ /* config */ });

// Full type safety - TypeScript knows return type
const users = await db
  .selectFrom('users')
  .select(['id', 'email'])
  .where('created_at', '>', new Date('2025-01-01'))
  .execute();
// Type: Array<{ id: number; email: string }>

// Conditional types for dynamic queries
type SelectFields<T> = {
  [K in keyof T]: T[K] extends ColumnType<infer S, any, any> ? S : T[K];
};
```

### Quick Database Migration Patterns (Inlined for Standalone Use)

**Safe Migration Principles:**
1. **Backward compatible** - New code works with old schema
2. **Reversible** - Can rollback migrations if needed
3. **Zero downtime** - No service interruption
4. **Incremental** - Small changes, not big-bang rewrites

**Kysely Migration Example:**

```typescript
// migrations/001_add_full_name.ts
import { Kysely, sql } from 'kysely';

export async function up(db: Kysely<any>): Promise<void> {
  // Phase 1: Add new column (nullable initially)
  await db.schema
    .alterTable('users')
    .addColumn('full_name', 'varchar(255)')
    .execute();

  // Phase 2: Backfill data
  await db
    .updateTable('users')
    .set({
      full_name: sql`concat(first_name, ' ', last_name)`
    })
    .execute();

  // Phase 3: Make required (separate migration recommended)
  // await db.schema
  //   .alterTable('users')
  //   .alterColumn('full_name', (col) => col.setNotNull())
  //   .execute();
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema
    .alterTable('users')
    .dropColumn('full_name')
    .execute();
}
```

**Common Safe Migrations:**

```typescript
// Add index (concurrently for PostgreSQL)
await db.schema
  .createIndex('idx_users_email')
  .on('users')
  .column('email')
  .execute();

// Rename column (multi-phase approach)
// Phase 1: Add new column
await db.schema
  .alterTable('users')
  .addColumn('email_address', 'varchar(255)')
  .execute();

// Phase 2: Copy data
await db
  .updateTable('users')
  .set({ email_address: sql`email` })
  .execute();

// Phase 3: Drop old column (after deploy)
// await db.schema
//   .alterTable('users')
//   .dropColumn('email')
//   .execute();

// Change column type (add new, migrate, drop old)
await db.schema
  .alterTable('products')
  .addColumn('price_cents', 'integer')
  .execute();

await db
  .updateTable('products')
  .set({ price_cents: sql`cast(price * 100 as integer)` })
  .execute();
```

**Running Migrations:**

```typescript
// migrate.ts
import { Kysely, Migrator, FileMigrationProvider } from 'kysely';
import { promises as fs } from 'fs';
import path from 'path';

const migrator = new Migrator({
  db,
  provider: new FileMigrationProvider({
    fs,
    path,
    migrationFolder: path.join(__dirname, 'migrations'),
  }),
});

// Migrate to latest
const { error, results } = await migrator.migrateToLatest();

// Migrate up/down
await migrator.migrateUp();
await migrator.migrateDown();

// List pending migrations
const migrations = await migrator.getMigrations();
```

[Full TypeScript patterns and migration workflows available in respective skills if deployed together]

## Summary

- **Kysely** is a type-safe SQL query builder, not an ORM
- **Full type inference** from schema definitions to query results
- **Zero runtime overhead** - compiles to plain SQL
- **Migration system** included with up/down support
- **Raw SQL integration** when query builder isn't enough
- **Plugin ecosystem** for JSON, pagination, full-text search
- **Best for** developers who know SQL and want type safety
- **Alternative to** Prisma (full ORM) and Drizzle (schema-first)
- **Perfect for** complex queries, existing databases, performance-critical apps
