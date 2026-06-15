# SQL Quality & Efficiency Anti-Patterns (SQLAlchemy)

High-signal SQL anti-patterns to watch for when writing queries — directly or through
the SQLAlchemy ORM. The ORM makes several of these *easier* to introduce by accident
(N+1 query-in-loop, over-fetching, `SELECT *`-equivalents), so they are worth an explicit
review pass.

> **Source note:** These patterns are derived from CAST Highlight's SQL code-quality
> indicators (https://doc.casthighlight.com/), cross-referenced with the SQL standard and
> SonarSource RSPEC. CAST defers to those primary sources for the underlying rules; where
> CAST's own SQL pages had title/content mismatches, the well-established form of the rule
> is used. Examples are original and shown in both raw SQL and SQLAlchemy 2.0 form.

This is a deliberately small, high-value subset — not all of CAST's ~49 SQL rules.

---

## 1. Avoid query-in-loop (the N+1 problem)

**Why:** Issuing one query per row of a previous result multiplies round-trips. With N
parent rows you pay 1 + N queries; latency dominates and the database cache thrashes.
This is the single most common ORM performance defect.

**Non-compliant (N+1):**
```python
authors = session.scalars(select(Author)).all()
for author in authors:
    # one SELECT per author — N+1 round-trips
    books = session.scalars(
        select(Book).where(Book.author_id == author.id)
    ).all()
    print(author.name, len(books))
```

**Compliant — eager-load in one round-trip:**
```python
from sqlalchemy.orm import selectinload

authors = session.scalars(
    select(Author).options(selectinload(Author.books))
).all()
for author in authors:
    print(author.name, len(author.books))   # no extra queries
```

**How to test:** Wrap the call in a query counter (e.g. SQLAlchemy's
`event.listen(engine, "before_cursor_execute", ...)` or `pytest`'s
`sqlalchemy.testing.assert_compile`/a counter fixture) and assert the number of emitted
statements is constant regardless of row count:
```python
def test_authors_with_books_is_constant_queries(query_counter):
    load_authors_with_books(session)
    assert query_counter.count <= 2   # one for authors, one for the selectin load
```

---

## 2. Don't `SELECT *` / over-fetch columns

**Why:** Selecting every column (or hydrating full ORM entities when you need two fields)
pulls unused data over the wire, defeats covering indexes, and breaks silently when the
schema changes. Fetch only the columns you use.

**Non-compliant:**
```sql
SELECT * FROM orders WHERE status = 'open';
```
```python
orders = session.scalars(select(Order).where(Order.status == "open")).all()
total = sum(o.amount for o in orders)   # only needed `amount`, hydrated whole rows
```

**Compliant — project the columns you need:**
```sql
SELECT id, amount FROM orders WHERE status = 'open';
```
```python
rows = session.execute(
    select(Order.id, Order.amount).where(Order.status == "open")
).all()
total = sum(amount for _id, amount in rows)
```

**How to test:** Assert the compiled SQL names explicit columns rather than `*`/all
entity columns:
```python
def test_open_orders_projects_only_needed_columns():
    stmt = open_orders_amount_query()
    sql = str(stmt.compile())
    assert "amount" in sql and "SELECT orders." not in sql.replace("orders.id", "")
```

---

## 3. Add indexes for filter/join/order columns; avoid `SELECT DISTINCT` to mask dupes

**Why:** A `WHERE`, `JOIN`, or `ORDER BY` on an unindexed column forces a full scan.
Reaching for `SELECT DISTINCT` to remove duplicate rows is usually a symptom of a missing
join condition or a missing index, not a fix — it adds a sort/hash on top of the scan.

**Non-compliant:**
```sql
SELECT DISTINCT customer_id FROM orders WHERE region = 'EU';   -- region not indexed
```

**Compliant — index the predicate, drop the DISTINCT if the query is correct:**
```python
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(index=True)
    region: Mapped[str] = mapped_column(index=True)   # predicate column indexed
```
```sql
SELECT customer_id FROM orders WHERE region = 'EU' GROUP BY customer_id;
```

**How to test:** In a test database with representative data, capture the query plan
(`EXPLAIN`) and assert it uses an index scan rather than a sequential/full scan for the
hot query. For correctness, assert the de-duplicated result matches the intended set.

---

## 4. Avoid cursor-in-loop; operate set-at-a-time

**Why:** Row-by-row cursor iteration that issues a write (or another query) per row
("RBAR" — row by agonizing row) serializes work the database could do in one set-based
statement. Prefer a single bulk `UPDATE`/`INSERT ... SELECT`.

**Non-compliant:**
```python
for user in session.scalars(select(User).where(User.inactive)):
    user.archived = True
    session.flush()        # a write per row
```

**Compliant — one set-based statement:**
```python
from sqlalchemy import update

session.execute(
    update(User).where(User.inactive.is_(True)).values(archived=True)
)
```

**How to test:** Count emitted `UPDATE` statements (query-counter fixture) and assert it
is 1 regardless of how many rows match; assert the post-condition (all matching rows
archived) with a follow-up `SELECT COUNT`.

---

## 5. Don't interleave DDL and DML; keep schema changes separate

**Why:** Mixing schema changes (`CREATE`/`ALTER`/`DROP`) with data manipulation
(`INSERT`/`UPDATE`/`DELETE`) inside one procedure or transaction can force statement
recompilation, invalidate cached plans, and on some engines silently auto-commit —
making the unit non-atomic. Put DDL in migrations; keep runtime code DML-only.

**Non-compliant:** a runtime routine that `ALTER TABLE ... ADD COLUMN` then immediately
`UPDATE`s using the new column.

**Compliant:** the column is added by an Alembic migration; application code only reads
and writes it. See the `database-migration` skill for DDL hygiene.

**How to test:** This is a structural/review check. In CI, assert that application
(non-migration) modules emit no DDL — e.g. grep for `CREATE TABLE`/`ALTER TABLE` outside
the `alembic/versions` path, or fail the test suite if the engine logs DDL during a
request-path test.

---

## 6. Parameterize queries — never interpolate untrusted data

**Why:** String-building SQL with user input is the classic SQL-injection vector and also
defeats the database's prepared-statement plan cache. Always bind parameters. SQLAlchemy's
expression language and `text()` with bound params do this for you; raw f-strings do not.

**Non-compliant:**
```python
session.execute(text(f"SELECT * FROM users WHERE email = '{email}'"))  # injectable
```

**Compliant:**
```python
session.execute(
    text("SELECT id FROM users WHERE email = :email"), {"email": email}
)
# or, preferred, the expression language:
session.scalar(select(User.id).where(User.email == email))
```

**How to test:** Add a test that passes an injection payload (e.g. `x'; DROP TABLE …`) and
asserts it is treated as a literal value (no rows / no side effect), plus a lint/grep gate
forbidding f-string/`%`/`+` SQL construction.

---

## 7. Prefer independent subqueries (or joins) over correlated subqueries

**Why:** A correlated subquery re-executes per outer row; an independent subquery (or a
plain join with proper indexes) runs once. Complex nested subqueries also hurt readability
and changeability.

**Non-compliant — correlated, runs per outer row:**
```sql
SELECT o.id
FROM orders o
WHERE o.amount > (SELECT AVG(amount) FROM orders WHERE customer_id = o.customer_id);
```

**Compliant — compute the aggregate once, then join:**
```sql
WITH avg_per_customer AS (
    SELECT customer_id, AVG(amount) AS avg_amount FROM orders GROUP BY customer_id
)
SELECT o.id
FROM orders o
JOIN avg_per_customer a ON a.customer_id = o.customer_id
WHERE o.amount > a.avg_amount;
```

**How to test:** Compare `EXPLAIN` cost/loops between the two forms on representative data,
or assert result-set equality between the correlated and join/CTE rewrite to prove the
refactor is behavior-preserving.

---

## Where this fits

These are query-design checks complementary to the ORM mechanics in the main skill. For
DDL hygiene and migration ordering see the `database-migration` skill; for the
project-wide efficiency checklist see `code-review-standards` (criteria-efficiency.md).
