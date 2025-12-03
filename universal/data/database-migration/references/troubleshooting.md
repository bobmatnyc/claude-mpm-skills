# Database Migration Troubleshooting Guide

Comprehensive troubleshooting guide for database migration failures, recovery procedures, and common issues.

## Table of Contents

- [Failed Migrations Recovery](#failed-migrations-recovery)
- [Schema Drift Detection](#schema-drift-detection)
- [Migration Conflicts Resolution](#migration-conflicts-resolution)
- [Rollback Failures](#rollback-failures)
- [Data Integrity Issues](#data-integrity-issues)
- [Performance Problems](#performance-problems)

---

## Failed Migrations Recovery

### Issue: Migration failed halfway through

**Problem:**
```bash
$ alembic upgrade head
...
sqlalchemy.exc.OperationalError: (psycopg2.errors.UndefinedColumn)
column "email" does not exist

Migration failed at version abc123
```

**Diagnosis:**
- Migration script has errors
- Database state is inconsistent
- Previous migration didn't complete

**Solutions:**

**Solution 1: Check migration state**
```bash
# Check current database version
alembic current

# Check migration history
alembic history
```

**Solution 2: Fix forward (preferred)**
```python
# Create a repair migration
alembic revision -m "repair_failed_migration"

# In the upgrade() function, handle the incomplete state
def upgrade():
    # Check if column exists before adding
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('users')]

    if 'email' not in columns:
        op.add_column('users', sa.Column('email', sa.String(255)))

def downgrade():
    pass  # No-op since we're repairing
```

**Solution 3: Manual database repair**
```sql
-- Identify what state the database is in
SELECT column_name FROM information_schema.columns
WHERE table_name = 'users';

-- Manually complete the migration
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- Mark migration as complete
-- (Framework-specific, for Alembic:)
UPDATE alembic_version SET version_num = 'abc123';
```

**Solution 4: Rollback and retry**
```bash
# Roll back to last known good state
alembic downgrade -1

# Fix the migration script
# Edit migrations/abc123_add_email.py

# Retry migration
alembic upgrade head
```

---

### Issue: Migration table is corrupted

**Problem:**
```bash
$ python manage.py migrate
django.db.utils.ProgrammingError:
relation "django_migrations" does not exist
```

**Diagnosis:**
- Migration tracking table deleted or corrupted
- Database was restored from old backup
- Manual database changes

**Solutions:**

**Solution 1: Recreate migration table (Django)**
```python
# In Django shell
from django.db import connection
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE django_migrations (
        id SERIAL PRIMARY KEY,
        app VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        applied TIMESTAMP NOT NULL
    )
""")
```

**Solution 2: Fake migrations to current state (Django)**
```bash
# Mark all migrations as applied without running them
python manage.py migrate --fake

# Or fake specific migration
python manage.py migrate myapp 0005 --fake
```

**Solution 3: Recreate from scratch**
```bash
# DANGER: Only in development
# Drop migration table
# Recreate and re-run all migrations
python manage.py migrate --run-syncdb
```

---

### Issue: Circular migration dependency

**Problem:**
```bash
$ alembic upgrade head
sqlalchemy.exc.CircularDependencyError:
Circular dependency detected between migrations
```

**Diagnosis:**
- Migration A depends on B
- Migration B depends on A
- Merge conflicts in migrations

**Solutions:**

**Solution 1: Identify the circular dependency**
```bash
# Visualize migration graph (Alembic)
alembic history --verbose

# Or use Django
python manage.py showmigrations --plan
```

**Solution 2: Merge migrations**
```python
# Create a merge migration (Django)
python manage.py makemigrations --merge

# Edit the merge migration to resolve conflicts
# migrations/0006_merge.py
dependencies = [
    ('myapp', '0004_auto_20251201'),
    ('myapp', '0005_auto_20251202'),
]
```

**Solution 3: Reorder migrations**
```python
# Edit migration file dependencies
# In migrations/0005_add_field.py
dependencies = [
    ('myapp', '0004_previous'),  # Changed from 0005
]
```

---

## Schema Drift Detection

### Issue: Database schema doesn't match ORM models

**Problem:**
Production database has columns not in migrations, or migrations have been applied incorrectly.

**Diagnosis:**
- Manual database changes
- Migrations applied out of order
- Migrations missing or skipped

**Solutions:**

**Solution 1: Generate diff (Alembic)**
```bash
# Auto-generate migration based on model changes
alembic revision --autogenerate -m "fix_schema_drift"

# Review the generated migration carefully!
# It will show differences between DB and models
```

**Solution 2: Schema inspection (Django)**
```python
# Compare actual DB schema with expected
from django.core.management import call_command
from django.db import connection

# Get actual schema
cursor = connection.cursor()
cursor.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'myapp_user'
""")
actual_columns = cursor.fetchall()

# Get expected schema from models
from myapp.models import User
expected_fields = User._meta.get_fields()

# Compare and log differences
```

**Solution 3: Use database migration tools**
```bash
# PostgreSQL: Compare schemas
pg_dump -s production_db > prod_schema.sql
pg_dump -s staging_db > staging_schema.sql
diff prod_schema.sql staging_schema.sql

# MySQL: Use pt-table-checksum (Percona Toolkit)
pt-table-checksum --databases mydb
```

**Solution 4: Create reconciliation migration**
```python
# Alembic
def upgrade():
    # Add missing columns
    op.add_column('users', sa.Column('phone', sa.String(20)))

    # Remove extra columns
    op.drop_column('users', 'deprecated_field')

    # Fix column types
    op.alter_column('users', 'age',
                    existing_type=sa.String(),
                    type_=sa.Integer())
```

---

### Issue: Migration history out of sync

**Problem:**
```bash
$ alembic upgrade head
Target database is not up to date.
```

**Diagnosis:**
- Migrations applied manually
- Migration table manually edited
- Different environments have different history

**Solutions:**

**Solution 1: Stamp database to specific version**
```bash
# Alembic: Mark database as being at specific version
alembic stamp head

# Or stamp to specific revision
alembic stamp abc123
```

**Solution 2: Fake migrations (Django)**
```bash
# Mark migration as applied without running
python manage.py migrate myapp 0005 --fake

# Mark all as applied
python manage.py migrate --fake
```

**Solution 3: Reset migration history (DANGEROUS)**
```bash
# Only in development/testing!
# Delete migration tracking
DELETE FROM alembic_version;

# Re-stamp to current
alembic stamp head
```

---

## Migration Conflicts Resolution

### Issue: Multiple developers created same migration number

**Problem:**
```
migrations/
  0004_add_email.py (Developer A)
  0004_add_phone.py (Developer B)  ❌ Conflict!
```

**Diagnosis:**
- Two branches created migrations simultaneously
- Migration numbers collide

**Solutions:**

**Solution 1: Rename migration (Django)**
```bash
# Developer B renames their migration
mv 0004_add_phone.py 0005_add_phone.py

# Update dependencies in file
# migrations/0005_add_phone.py
dependencies = [
    ('myapp', '0004_add_email'),  # Changed from 0003
]
```

**Solution 2: Create merge migration**
```bash
# Django auto-detects and creates merge migration
python manage.py makemigrations --merge
```

**Solution 3: Squash migrations (after resolution)**
```bash
# Combine multiple migrations into one (Django)
python manage.py squashmigrations myapp 0001 0005
```

---

### Issue: Migration depends on deleted migration

**Problem:**
```python
dependencies = [
    ('myapp', '0003_old_migration'),  # This was deleted!
]
```

**Diagnosis:**
- Migration file deleted but referenced
- Branch merged without updating dependencies

**Solutions:**

**Solution 1: Update dependency**
```python
# Edit migration file
dependencies = [
    ('myapp', '0002_previous_migration'),  # Updated
]
```

**Solution 2: Recreate deleted migration**
```bash
# Create empty migration with same number
# migrations/0003_old_migration.py
def upgrade():
    pass

def downgrade():
    pass
```

---

## Rollback Failures

### Issue: Cannot rollback migration (no downgrade)

**Problem:**
```bash
$ alembic downgrade -1
NotImplementedError: downgrade() not implemented
```

**Diagnosis:**
- Migration has no `downgrade()` function
- Irreversible operation (data deletion)

**Solutions:**

**Solution 1: Write downgrade function**
```python
# migrations/abc123_add_column.py
def upgrade():
    op.add_column('users', sa.Column('email', sa.String(255)))

def downgrade():
    # Add the missing downgrade
    op.drop_column('users', 'email')
```

**Solution 2: Create reverse migration**
```bash
# Create new migration that reverses changes
alembic revision -m "reverse_abc123"
```

```python
def upgrade():
    # Reverse the previous migration
    op.drop_column('users', 'email')

def downgrade():
    # Allow rolling back this rollback
    op.add_column('users', sa.Column('email', sa.String(255)))
```

**Solution 3: Manual rollback**
```sql
-- Manually reverse the changes
ALTER TABLE users DROP COLUMN email;

-- Update migration table
UPDATE alembic_version SET version_num = 'previous_version';
```

---

### Issue: Rollback loses data

**Problem:**
Rolling back migration would delete production data.

**Diagnosis:**
- Migration added column with data
- Rollback would drop column
- No data backup

**Solutions:**

**Solution 1: Export data before rollback**
```sql
-- Create backup table
CREATE TABLE users_email_backup AS
SELECT id, email FROM users;

-- Now safe to rollback
-- migrations/downgrade.py
def downgrade():
    op.drop_column('users', 'email')
```

**Solution 2: Modify downgrade to preserve data**
```python
def downgrade():
    # Don't drop column, just mark as deprecated
    op.alter_column('users', 'email',
                    existing_type=sa.String(255),
                    comment='DEPRECATED: Will be removed in next version')
```

**Solution 3: Don't rollback - fix forward**
```python
# Create new migration that fixes the issue
# migrations/abc456_fix_issue.py
def upgrade():
    # Fix the problem without rolling back
    op.alter_column('users', 'email', type_=sa.String(320))
```

---

## Data Integrity Issues

### Issue: Foreign key constraint violation during migration

**Problem:**
```bash
$ alembic upgrade head
IntegrityError: foreign key constraint "fk_orders_user" violated
Key (user_id)=(123) is not present in table "users"
```

**Diagnosis:**
- Data inconsistency exists
- Orphaned records
- Migration adds FK on dirty data

**Solutions:**

**Solution 1: Clean data before adding constraint**
```python
def upgrade():
    # Delete orphaned records first
    op.execute("""
        DELETE FROM orders
        WHERE user_id NOT IN (SELECT id FROM users)
    """)

    # Now safe to add foreign key
    op.create_foreign_key(
        'fk_orders_user',
        'orders', 'users',
        ['user_id'], ['id']
    )
```

**Solution 2: Set orphaned FKs to NULL**
```python
def upgrade():
    # Add column as nullable first
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=True))

    # Update valid references
    op.execute("""
        UPDATE orders o
        SET user_id = old_user_id
        FROM users u
        WHERE o.old_user_id = u.id
    """)

    # Handle orphans (set to NULL or default user)
    op.execute("""
        UPDATE orders
        SET user_id = NULL
        WHERE old_user_id NOT IN (SELECT id FROM users)
    """)

    # Now add foreign key
    op.create_foreign_key('fk_orders_user', 'orders', 'users', ['user_id'], ['id'])
```

**Solution 3: Add constraint as NOT VALID (PostgreSQL)**
```sql
-- Add constraint without validating existing data
ALTER TABLE orders
ADD CONSTRAINT fk_orders_user
FOREIGN KEY (user_id) REFERENCES users(id)
NOT VALID;

-- Validate in separate transaction (can be done later)
ALTER TABLE orders
VALIDATE CONSTRAINT fk_orders_user;
```

---

### Issue: Unique constraint violation during data migration

**Problem:**
```bash
IntegrityError: duplicate key value violates unique constraint "users_email_key"
```

**Diagnosis:**
- Data has duplicates
- Migration adds unique constraint
- Need to deduplicate first

**Solutions:**

**Solution 1: Identify and remove duplicates**
```python
def upgrade():
    # Find duplicates
    op.execute("""
        WITH duplicates AS (
            SELECT email, MIN(id) as keep_id
            FROM users
            GROUP BY email
            HAVING COUNT(*) > 1
        )
        DELETE FROM users
        WHERE id NOT IN (SELECT keep_id FROM duplicates)
    """)

    # Now add unique constraint
    op.create_unique_constraint('uq_users_email', 'users', ['email'])
```

**Solution 2: Merge duplicate records**
```python
def upgrade():
    # Merge duplicates (keep oldest, update references)
    op.execute("""
        WITH duplicates AS (
            SELECT email, array_agg(id ORDER BY created_at) as ids
            FROM users
            GROUP BY email
            HAVING COUNT(*) > 1
        )
        UPDATE orders
        SET user_id = d.ids[1]  -- Keep oldest
        FROM duplicates d, users u
        WHERE orders.user_id = ANY(d.ids[2:])
        AND u.email = d.email
    """)

    # Delete merged records
    op.execute("""
        WITH duplicates AS (
            SELECT email, array_agg(id ORDER BY created_at) as ids
            FROM users
            GROUP BY email
            HAVING COUNT(*) > 1
        )
        DELETE FROM users
        WHERE id IN (
            SELECT unnest(ids[2:]) FROM duplicates
        )
    """)

    # Add constraint
    op.create_unique_constraint('uq_users_email', 'users', ['email'])
```

**Solution 3: Suffix duplicates**
```python
def upgrade():
    # Add suffix to duplicate emails
    op.execute("""
        WITH ranked AS (
            SELECT id, email,
                   ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) as rn
            FROM users
        )
        UPDATE users u
        SET email = u.email || '_' || r.rn
        FROM ranked r
        WHERE u.id = r.id AND r.rn > 1
    """)

    # Now add unique constraint
    op.create_unique_constraint('uq_users_email', 'users', ['email'])
```

---

## Performance Problems

### Issue: Migration locks table for too long

**Problem:**
```bash
$ alembic upgrade head
# ... hangs for 10 minutes ...
# Production writes are blocked!
```

**Diagnosis:**
- Adding NOT NULL to large table
- Creating index without CONCURRENTLY
- Altering column type on large table

**Solutions:**

**Solution 1: Use CONCURRENTLY for indexes (PostgreSQL)**
```python
def upgrade():
    # Create index without locking
    op.execute("""
        CREATE INDEX CONCURRENTLY idx_users_email ON users(email)
    """)

# Note: Cannot use in transaction
# Alembic: Set transaction_per_migration = False
```

**Solution 2: Add column in phases**
```python
# Phase 1: Add as nullable
def upgrade():
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))

# Phase 2 (separate migration): Make NOT NULL
def upgrade():
    # Backfill first
    op.execute("UPDATE users SET email = 'unknown@example.com' WHERE email IS NULL")

    # Then add constraint
    op.alter_column('users', 'email', nullable=False)
```

**Solution 3: Use batched updates**
```python
def upgrade():
    # Process in batches to avoid long locks
    batch_size = 1000
    while True:
        result = op.execute(f"""
            WITH batch AS (
                SELECT id FROM users
                WHERE email IS NULL
                LIMIT {batch_size}
            )
            UPDATE users u
            SET email = 'unknown@example.com'
            FROM batch b
            WHERE u.id = b.id
        """)

        if result.rowcount == 0:
            break
```

---

### Issue: Migration takes too long on large table

**Problem:**
```bash
# Migration running for 2 hours on 100M row table
ALTER TABLE events ADD COLUMN processed BOOLEAN DEFAULT FALSE;
```

**Diagnosis:**
- Large table
- Expensive default value calculation
- Full table rewrite required

**Solutions:**

**Solution 1: Add without default, set later**
```python
def upgrade():
    # Add column without default (instant in PostgreSQL 11+)
    op.add_column('events', sa.Column('processed', sa.Boolean(), nullable=True))

    # Set default for future rows
    op.alter_column('events', 'processed', server_default=sa.false())

    # Backfill in batches (asynchronously)
    # Use background worker to set existing rows
```

**Solution 2: Use background worker for backfill**
```python
# In migration
def upgrade():
    op.add_column('events', sa.Column('processed', sa.Boolean(), nullable=True))

# Separately, run background job
@celery.task
def backfill_processed_flag():
    batch_size = 10000
    while True:
        updated = db.execute("""
            UPDATE events
            SET processed = FALSE
            WHERE processed IS NULL
            LIMIT :batch_size
        """, batch_size=batch_size)

        if updated == 0:
            break
```

**Solution 3: Partition table first (PostgreSQL)**
```sql
-- For very large tables, partition before migration
CREATE TABLE events_new (LIKE events INCLUDING ALL)
PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_01 PARTITION OF events_new
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Migrate data in chunks
INSERT INTO events_new SELECT * FROM events WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01';

-- Swap tables
ALTER TABLE events RENAME TO events_old;
ALTER TABLE events_new RENAME TO events;
```

---

## Migration Checklist for Troubleshooting

When migration fails:

1. **Don't panic** → Most migrations can be fixed forward
2. **Check database state** → What actually exists in the database?
3. **Check migration state** → What does migration tool think state is?
4. **Read error messages** → They usually tell you exactly what's wrong
5. **Test on copy first** → Never experiment on production
6. **Have backup ready** → Always have rollback option
7. **Document the fix** → Help future you and teammates

---

## Related References

- **[Decision Trees](./decision-trees.md)** - Make better migration strategy decisions
- **[Zero-Downtime Patterns](./zero-downtime-patterns.md)** - Prevent issues with proper patterns (coming soon)
- **[Rollback Procedures](./rollback-procedures.md)** - Detailed rollback strategies (coming soon)
