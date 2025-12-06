---
name: ecto-patterns
description: Ecto patterns for Phoenix/Elixir apps. Covers schemas, changesets, migrations, queries, Ecto.Multi, transactions, constraints, associations, pagination, tenant partitioning, performance, and testing.
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Ecto schemas/changesets, migrations, queries, transactions, constraints, pagination, tenancy, and performance for Phoenix apps."
    when_to_use:
      - "Designing schemas and changesets with validation/constraints"
      - "Running migrations safely (DDL ordering, locks) and managing data migrations"
      - "Executing transactional flows with Ecto.Multi"
      - "Implementing pagination, preloading, and multi-tenant partitioning"
    quick_start:
      - "mix ecto.create && mix ecto.migrate"
      - "Define schemas + changesets; enforce DB constraints (unique/foreign keys)"
      - "Use Repo.transaction / Ecto.Multi for multi-step writes"
      - "Preload associations; paginate with limit/offset or cursor libs (Scrivener/Flop)"
  token_estimate:
    entry: 170
    full: 5400
---

# Ecto Patterns for Phoenix/Elixir

Ecto is the data layer for Phoenix applications: schemas, changesets, queries, migrations, and transactions. Good Ecto practice keeps domain logic in contexts, enforces constraints in the database, and uses transactions for multi-step workflows.

## Schemas and Changesets

```elixir
defmodule MyApp.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :email, :string
    field :hashed_password, :string
    field :confirmed_at, :naive_datetime
    has_many :memberships, MyApp.Orgs.Membership
    timestamps()
  end

  def registration_changeset(user, attrs) do
    user
    |> cast(attrs, [:email, :password])
    |> validate_required([:email, :password])
    |> validate_format(:email, ~r/@/)
    |> validate_length(:password, min: 12)
    |> unique_constraint(:email)
    |> hash_password()
  end

  defp hash_password(%{valid?: true} = cs),
    do: put_change(cs, :hashed_password, Argon2.hash_pwd_salt(get_change(cs, :password)))
  defp hash_password(cs), do: cs
end
```

**Guidelines**
- Keep casting/validation in changesets; keep business logic in contexts.
- Always pair validation with DB constraints (`unique_constraint`, `foreign_key_constraint`).
- Use `changeset/2` for updates; avoid mass assigning without casting.

## Migrations

```elixir
def change do
  create table(:users) do
    add :email, :citext, null: false
    add :hashed_password, :string, null: false
    add :confirmed_at, :naive_datetime
    timestamps()
  end

  create unique_index(:users, [:email])
end
```

**Safe migration tips**
- Prefer additive changes: add columns nullable, backfill, then enforce null: false.
- For large tables: use `concurrently: true` for indexes; disable in `change` and wrap in `up/down` for Postgres.
- Data migrations belong in separate modules called from `mix ecto.migrate` via `execute/1` or in distinct scripts; ensure idempotence.
- Coordinate locks: avoid long transactions; break migrations into small steps.

## Queries and Preloads

```elixir
import Ecto.Query

def list_users(opts \\ %{}) do
  base =
    from u in MyApp.Accounts.User,
      preload: [:memberships],
      order_by: [desc: u.inserted_at]

  Repo.all(apply_pagination(base, opts))
end

defp apply_pagination(query, %{limit: limit, offset: offset}),
  do: query |> limit(^limit) |> offset(^offset)
defp apply_pagination(query, _), do: query
```

**Patterns**
- Use `preload` rather than calling Repo in loops; prefer `Repo.preload/2` after fetching.
- Use `select` to avoid loading large blobs.
- For concurrency, use `Repo.transaction` with `lock: "FOR UPDATE"` in queries that need row-level locks.

## Transactions and Ecto.Multi

```elixir
alias Ecto.Multi

def onboard_user(attrs) do
  Multi.new()
  |> Multi.insert(:user, User.registration_changeset(%User{}, attrs))
  |> Multi.insert(:org, fn %{user: user} ->
    Org.changeset(%Org{}, %{owner_id: user.id, name: attrs["org_name"]})
  end)
  |> Multi.run(:welcome, fn _repo, %{user: user} ->
    MyApp.Mailer.deliver_welcome(user)
    {:ok, :sent}
  end)
  |> Repo.transaction()
end
```

**Guidelines**
- Prefer `Multi.run/3` for side effects that can fail; return `{:ok, value}` or `{:error, reason}`.
- Use `Multi.update_all` for batch updates; include `where` guards to prevent unbounded writes.
- Propagate errors upward; translate them in controllers/LiveViews.

## Associations and Constraints

- Use `on_replace: :delete`/`:nilify` to control nested changes.
- Define `foreign_key_constraint/3` and `unique_constraint/3` in changesets to surface DB errors cleanly.
- For many-to-many, prefer join schema (`has_many :memberships`) instead of automatic `many_to_many` when you need metadata.

## Pagination and Filtering

- Offset/limit for small datasets; cursor-based for large lists (`Scrivener`, `Flop`, `Paginator`).
- Normalize filters in contexts; avoid letting controllers build queries directly.
- Add composite indexes to match filter columns; verify with `EXPLAIN ANALYZE`.

## Multi-Tenancy Patterns

- **Prefix-based**: Postgres schemas per tenant (`put_source/2` with `prefix:`) — good isolation, needs per-tenant migrations.
- **Row-based**: `tenant_id` column + row filters — simpler migrations; add partial indexes per tenant when large.
- Always scope queries by tenant in contexts; consider using policies/guards to enforce.

## Performance and Ops

- Use `Repo.stream` for large exports; wrap in `Repo.transaction`.
- Cache hot reads with ETS/Cachex; invalidate on writes.
- Watch query counts in LiveView/Channels; preload before rendering to avoid N+1.
- Telemetry: `OpentelemetryEcto` exports query timings; add DB connection pool metrics.

## Testing

```elixir
use MyApp.DataCase, async: true

test "registration changeset validates email" do
  changeset = User.registration_changeset(%User{}, %{email: "bad", password: "secretsecret"})
  refute changeset.valid?
  assert %{email: ["has invalid format"]} = errors_on(changeset)
end
```

- `DataCase` sets up sandboxed DB; keep tests async unless transactions conflict.
- Use factories/fixtures in `test/support` to build valid structs quickly.
- For migrations, add regression tests for constraints (unique/index-backed constraints).

## Common Pitfalls

- Running risky DDL in a single migration step (avoid locks; break apart).
- Skipping DB constraints and relying only on changesets.
- Querying associations in loops instead of preloading.
- Missing transactions for multi-step writes (partial state on failure).
- Forgetting tenant scoping on read/write in multi-tenant setups.
