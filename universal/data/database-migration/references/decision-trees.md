# Database Migration Decision Trees

This guide helps you make critical database migration decisions through clear decision trees and selection criteria.

## Table of Contents

- [Schema Migration Strategy](#schema-migration-strategy)
- [Zero-Downtime Deployment Patterns](#zero-downtime-deployment-patterns)
- [Rollback Strategy Selection](#rollback-strategy-selection)
- [Migration Tool Choice](#migration-tool-choice)
- [Data Migration Approach](#data-migration-approach)

---

## Schema Migration Strategy

### Decision Tree

```
Making a schema change?
│
├─ Breaking change (drops data or incompatible)?
│   │
│   ├─ YES → Multi-phase migration required
│   │   │
│   │   ├─ Phase 1: Add new (nullable)
│   │   ├─ Phase 2: Dual-write old + new
│   │   ├─ Phase 3: Backfill data
│   │   ├─ Phase 4: Migrate reads to new
│   │   ├─ Phase 5: Remove old
│   │   │
│   │   ✅ Zero downtime maintained
│   │   ✅ Can rollback at each phase
│   │   ✅ Production-safe
│   │
│   └─ NO → Additive change?
│       │
│       ├─ YES → Single-phase migration
│       │   ✅ Add columns as nullable initially
│       │   ✅ Set defaults after data loaded
│       │   ✅ Safe and simple
│       │
│       └─ NO → Data-only change (no schema)?
│           └─ Use data migration script
│               ✅ No schema changes
│               ✅ Easier rollback
│
└─ Creating new table/index?
    │
    ├─ Large table (millions of rows)?
    │   └─ Use CONCURRENTLY for indexes
    │       ✅ No table locks (PostgreSQL)
    │       ⚠️  Takes longer but zero downtime
    │
    └─ Small table?
        └─ Standard CREATE
            ✅ Fast and simple
```

### When to Use Multi-Phase Migrations

✅ **Use multi-phase when:**
- Renaming columns or tables
- Changing column types
- Removing columns or tables
- Adding NOT NULL constraints
- Changing foreign key relationships

**Example: Renaming a column**

```sql
-- ❌ Bad: Breaking change in one step
ALTER TABLE users RENAME COLUMN email TO email_address;
-- Breaks running application immediately!

-- ✅ Good: Multi-phase approach
-- Phase 1: Add new column
ALTER TABLE users ADD COLUMN email_address VARCHAR(255) NULL;

-- Phase 2: Deploy code that writes to both columns
UPDATE users SET email_address = email WHERE email_address IS NULL;

-- Phase 3: Migrate reads to new column (code deploy)

-- Phase 4: Remove old column (after new code deployed)
ALTER TABLE users DROP COLUMN email;
```

### When to Use Single-Phase Migrations

✅ **Use single-phase when:**
- Adding new nullable columns
- Adding new tables
- Adding indexes (use CONCURRENTLY)
- Adding new foreign keys to nullable columns

```sql
-- ✅ Safe: Additive changes
ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Can safely deploy with running application
```

---

## Zero-Downtime Deployment Patterns

### Decision Tree

```
Need zero-downtime deployment?
│
├─ Schema change required?
│   │
│   ├─ YES → Expand-Contract pattern
│   │   │
│   │   ├─ Step 1: EXPAND schema (add new)
│   │   ├─ Step 2: Deploy NEW code (dual-write)
│   │   ├─ Step 3: MIGRATE data (backfill)
│   │   ├─ Step 4: Deploy NEW code (read from new)
│   │   ├─ Step 5: CONTRACT schema (remove old)
│   │   │
│   │   ✅ Zero downtime guaranteed
│   │   ✅ Rollback at each step
│   │
│   └─ NO → Code-only deployment?
│       └─ Standard rolling deployment
│           ✅ Simple and fast
│
├─ Data migration required?
│   │
│   ├─ Large dataset (millions of rows)?
│   │   └─ Background worker pattern
│   │       ✅ Batch processing
│   │       ✅ No blocking
│   │       ✅ Progress tracking
│   │
│   └─ Small dataset?
│       └─ Synchronous migration
│           ✅ Simple and fast
│
└─ Index creation?
    │
    ├─ PostgreSQL?
    │   └─ CREATE INDEX CONCURRENTLY
    │       ✅ No locks
    │       ⚠️  Slower than regular CREATE
    │
    └─ MySQL?
        └─ ALGORITHM=INPLACE, LOCK=NONE (5.6+)
            ✅ Online DDL
```

### Expand-Contract Pattern (Best Practice)

**Phase 1: EXPAND**
```sql
-- Add new schema elements
ALTER TABLE products ADD COLUMN price_cents INTEGER NULL;
```

**Phase 2: Deploy Code (Dual Write)**
```python
# Application writes to BOTH old and new
product.price = Decimal("19.99")
product.price_cents = 1999  # New field
product.save()
```

**Phase 3: MIGRATE Existing Data**
```sql
-- Backfill in batches
UPDATE products
SET price_cents = CAST(price * 100 AS INTEGER)
WHERE price_cents IS NULL
LIMIT 1000;
-- Repeat until all migrated
```

**Phase 4: Deploy Code (Read New)**
```python
# Application now reads from new field
price = Decimal(product.price_cents) / 100
```

**Phase 5: CONTRACT**
```sql
-- Remove old schema
ALTER TABLE products DROP COLUMN price;
ALTER TABLE products RENAME COLUMN price_cents TO price;
```

### Blue-Green Deployment Pattern

✅ **Use blue-green when:**
- Complete database swap needed
- Testing production-like data required
- Instant rollback critical

```
┌─────────────────┐      ┌─────────────────┐
│   Blue (Live)   │      │  Green (New)    │
│                 │      │                 │
│  App v1         │      │  App v2         │
│  DB Schema v1   │      │  DB Schema v2   │
└────────┬────────┘      └────────┬────────┘
         │                        │
         │  1. Replicate data     │
         │  2. Apply migrations   │
         │  3. Test green         │
         │  4. Switch traffic ────▶
         │                        │
         │  5. Monitor            │
         │  6. Rollback if needed │
```

---

## Rollback Strategy Selection

### Decision Tree

```
Planning rollback strategy?
│
├─ Migration added new schema only?
│   │
│   ├─ YES → Simple rollback
│   │   │
│   │   └─ Run DOWN migration
│   │       ✅ Removes new additions
│   │       ✅ Safe (no data loss)
│   │
│   └─ NO → Migration modified/removed schema?
│       │
│       └─ Complex rollback needed
│           │
│           ├─ Data was migrated?
│           │   └─ Restore from backup + replay transactions
│           │       ⚠️  Complex, test thoroughly
│           │
│           └─ No data migration yet?
│               └─ Reverse migration safe
│                   ✅ Schema-only rollback
│
├─ Can tolerate data loss?
│   │
│   ├─ YES → Snapshot rollback
│   │   └─ Restore from backup
│   │       ⚠️  Loses recent data
│   │
│   └─ NO → Point-in-time recovery required
│       └─ Use transaction log replay
│           ✅ No data loss
│           ⚠️  Complex setup
│
└─ How fast must rollback be?
    │
    ├─ Immediate (< 1 minute)?
    │   └─ Blue-green deployment
    │       ✅ Traffic switch only
    │       ✅ Instant rollback
    │
    └─ Can wait (5-30 minutes)?
        └─ Reverse migration
            ✅ Standard approach
```

### Rollback Strategies

**Strategy 1: Reverse Migration (Default)**

```python
# Alembic example
def upgrade():
    op.add_column('users', sa.Column('full_name', sa.String(255)))

def downgrade():
    op.drop_column('users', 'full_name')
```

**When to use:**
- Additive changes only
- No data migration performed
- Testing/staging environments

**Strategy 2: Multi-Phase Rollback**

```
Migration in progress:
  Phase 1: ✅ Add new column       → Rollback: Drop new column
  Phase 2: ✅ Dual-write deployed  → Rollback: Deploy old code
  Phase 3: 🔄 Backfilling data     → Rollback: Stop backfill, drop new column
  Phase 4: ❌ Not started          → Cannot rollback beyond this point safely

Rule: Can only rollback to phases already completed
```

**Strategy 3: Snapshot Rollback**

```bash
# Take snapshot before migration
pg_dump -Fc mydb > backup_before_migration.dump

# If rollback needed
pg_restore -d mydb backup_before_migration.dump
```

**When to use:**
- Development/staging only
- Data loss acceptable
- Need fast rollback

**⚠️ Warning:** Loses all data created after snapshot

**Strategy 4: Point-in-Time Recovery (Production)**

```sql
-- PostgreSQL PITR
-- 1. Enable WAL archiving
archive_mode = on
archive_command = 'cp %p /archive/%f'

-- 2. Take base backup
pg_basebackup -D /backup/base

-- 3. If rollback needed
# Restore base backup
# Replay WAL up to migration point
recovery_target_time = '2025-12-03 10:00:00'
```

**When to use:**
- Production databases
- Zero data loss required
- Have WAL archiving setup

---

## Migration Tool Choice

### Decision Tree

```
Choosing migration tool for project?
│
├─ What's your tech stack?
│   │
│   ├─ Python (Django)?
│   │   └─ Django Migrations (built-in)
│   │       ✅ Integrated with ORM
│   │       ✅ Auto-generates migrations
│   │       ✅ Schema + data migrations
│   │
│   ├─ Python (other frameworks)?
│   │   └─ Alembic
│   │       ✅ Works with SQLAlchemy
│   │       ✅ Auto-detection
│   │       ✅ Flask, FastAPI compatible
│   │
│   ├─ Node.js / TypeScript?
│   │   │
│   │   ├─ Using Prisma ORM?
│   │   │   └─ Prisma Migrate
│   │   │       ✅ Type-safe
│   │   │       ✅ Schema as code
│   │   │
│   │   ├─ Using Drizzle ORM?
│   │   │   └─ Drizzle Kit
│   │   │       ✅ TypeScript-first
│   │   │       ✅ Zero dependencies
│   │   │
│   │   └─ Framework-agnostic?
│   │       └─ Knex.js or node-pg-migrate
│   │           ✅ Simple and flexible
│   │           ✅ No ORM required
│   │
│   ├─ Ruby (Rails)?
│   │   └─ ActiveRecord Migrations (built-in)
│   │       ✅ Integrated with Rails
│   │       ✅ DSL for schema changes
│   │
│   ├─ Go?
│   │   └─ golang-migrate or goose
│   │       ✅ Fast and simple
│   │       ✅ No ORM dependency
│   │
│   └─ Language-agnostic?
│       └─ Flyway or Liquibase
│           ✅ Works with any language
│           ✅ Enterprise features
│           ✅ Team tracking
│
└─ Database-specific needs?
    │
    ├─ PostgreSQL-only?
    │   └─ Sqitch or dbmate
    │       ✅ PostgreSQL optimized
    │
    └─ Multi-database support?
        └─ Flyway or Liquibase
            ✅ Supports 20+ databases
```

### Comparison Matrix

| Tool | Language | Auto-Gen | Zero-Downtime | Best For |
|------|----------|----------|---------------|----------|
| **Django Migrations** | Python | ✅ Yes | ⚠️  Manual | Django projects |
| **Alembic** | Python | ✅ Yes | ⚠️  Manual | SQLAlchemy, Flask, FastAPI |
| **Prisma Migrate** | TypeScript | ✅ Yes | ⚠️  Manual | Prisma ORM, type-safe apps |
| **Drizzle Kit** | TypeScript | ✅ Yes | ⚠️  Manual | Drizzle ORM, lightweight |
| **Knex.js** | JavaScript | ❌ No | ⚠️  Manual | Node.js, framework-agnostic |
| **ActiveRecord** | Ruby | ✅ Yes | ⚠️  Manual | Rails applications |
| **Flyway** | Any | ❌ No | ✅ Patterns | Enterprise, multi-DB |
| **Liquibase** | Any | ❌ No | ✅ Patterns | Enterprise, XML/YAML |
| **golang-migrate** | Go | ❌ No | ⚠️  Manual | Go microservices |

### When to Use Each Tool

**Django Migrations**
```python
# Auto-generate from models
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

✅ **Use when:** Building Django applications with ORM

**Alembic (SQLAlchemy)**
```bash
# Auto-generate from models
alembic revision --autogenerate -m "add user table"

# Apply
alembic upgrade head
```

✅ **Use when:** Flask, FastAPI, or any Python with SQLAlchemy

**Prisma Migrate**
```bash
# Generate migration from schema
npx prisma migrate dev --name add_user_table

# Apply to production
npx prisma migrate deploy
```

✅ **Use when:** TypeScript projects with type-safe database access

**Flyway (Enterprise)**
```sql
-- migrations/V1__create_users.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL
);
```

```bash
flyway migrate
```

✅ **Use when:** Multi-language teams, enterprise requirements

---

## Data Migration Approach

### Decision Tree

```
Migrating data between schemas?
│
├─ How much data?
│   │
│   ├─ Small (< 10,000 rows)?
│   │   └─ Synchronous in-migration approach
│   │       ✅ Simple UPDATE statement
│   │       ✅ Runs during migration
│   │       ✅ Fast enough
│   │
│   ├─ Medium (10k - 1M rows)?
│   │   └─ Batched migration approach
│   │       ✅ Process in chunks (1000 rows)
│   │       ✅ Avoid long locks
│   │       ✅ Resumable if interrupted
│   │
│   └─ Large (> 1M rows)?
│       └─ Background worker approach
│           ✅ Process asynchronously
│           ✅ Track progress
│           ✅ Zero downtime
│
├─ Complex transformations needed?
│   │
│   ├─ YES → Application-level migration
│   │   │
│   │   └─ Use background jobs
│   │       ✅ Business logic in code
│   │       ✅ Easy to test
│   │       ✅ Can retry failures
│   │
│   └─ NO → SQL-level migration
│       └─ Direct UPDATE/INSERT
│           ✅ Faster
│           ✅ Less code
│
└─ Can tolerate temporary inconsistency?
    │
    ├─ YES → Lazy migration
    │   │
    │   └─ Migrate on read/write
    │       ✅ Zero downtime
    │       ✅ Gradual migration
    │       ✅ No batch jobs needed
    │
    └─ NO → Eager migration required
        └─ Backfill before switching reads
            ✅ Consistent data
            ⚠️  Requires coordination
```

### Data Migration Patterns

**Pattern 1: Synchronous (Small Data)**

```sql
-- Simple one-shot migration
UPDATE products
SET price_cents = CAST(price * 100 AS INTEGER)
WHERE price_cents IS NULL;
```

**When to use:**
- < 10,000 rows
- Fast transformation
- No locks concern

**Pattern 2: Batched (Medium Data)**

```python
def migrate_in_batches(batch_size=1000):
    while True:
        updated = db.execute("""
            UPDATE products
            SET price_cents = CAST(price * 100 AS INTEGER)
            WHERE price_cents IS NULL
            LIMIT :batch_size
        """, batch_size=batch_size)

        if updated == 0:
            break  # All migrated

        time.sleep(0.1)  # Breather between batches
```

**When to use:**
- 10k - 1M rows
- Want to avoid long locks
- Need progress tracking

**Pattern 3: Background Worker (Large Data)**

```python
# Celery task example
@celery.task
def backfill_price_cents():
    products = Product.objects.filter(price_cents__isnull=True)[:1000]

    for product in products:
        product.price_cents = int(product.price * 100)
        product.save()

    if products.count() == 1000:
        # More to process, schedule next batch
        backfill_price_cents.apply_async(countdown=1)
```

**When to use:**
- > 1M rows
- Complex transformations
- Need monitoring/retry

**Pattern 4: Lazy Migration (Zero Downtime)**

```python
class Product(models.Model):
    price = models.DecimalField()
    price_cents = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        # Migrate on write
        if self.price_cents is None:
            self.price_cents = int(self.price * 100)
        super().save(*args, **kwargs)

    @property
    def current_price_cents(self):
        # Migrate on read
        if self.price_cents is None:
            self.price_cents = int(self.price * 100)
            self.save()
        return self.price_cents
```

**When to use:**
- True zero downtime needed
- Gradual migration acceptable
- No batch processing infrastructure

---

## Migration Checklist

Before executing migrations, verify:

1. **Backup Taken** → Full database backup exists
2. **Tested on Staging** → Migration tested on production-like data
3. **Rollback Plan** → Know how to reverse the migration
4. **Monitoring Ready** → Can detect issues quickly
5. **Team Notified** → Coordinate with team on timing
6. **Load Tested** → Tested with production-scale data
7. **Read-Only Mode** → Can enable read-only if issues
8. **Runbook Created** → Step-by-step execution guide

---

## Related References

- **[Troubleshooting](./troubleshooting.md)** - Common migration failures and recovery procedures
- **[Zero-Downtime Patterns](./zero-downtime-patterns.md)** - Detailed zero-downtime deployment strategies (coming soon)
- **[Tool Guides](./tool-guides.md)** - Framework-specific migration tool guides (coming soon)
