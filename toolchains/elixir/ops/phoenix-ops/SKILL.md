---
name: phoenix-ops
description: "Phoenix operations and deployment: releases, runtime configuration, clustering, libcluster, telemetry/logging, secrets, assets, background jobs, and production hardening on the BEAM."
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Phoenix production ops: releases, runtime config, libcluster, telemetry/logging, secrets, assets, jobs, and hardening on the BEAM."
    when_to_use:
      - "Preparing Phoenix apps for production deployment or CI/CD"
      - "Configuring clustering/libcluster for multi-node PubSub/Presence"
      - "Setting up telemetry/logging and runtime configuration for releases"
      - "Hardening endpoints (HTTPS, rate limiting, CORS, secrets)"
    quick_start:
      - "Set env: MIX_ENV=prod PHX_SERVER=true SECRET_KEY_BASE=... DATABASE_URL=..."
      - "mix assets.deploy && MIX_ENV=prod mix release"
      - "Configure runtime in config/runtime.exs (DB, cache, endpoints, Oban)"
      - "Add libcluster + DNS/epmd strategy; enable OpentelemetryPhoenix/Ecto"
  token_estimate:
    entry: 180
    full: 5600
---

# Phoenix Operations and Deployment (Elixir/BEAM)

Production-ready Phoenix apps rely on releases, runtime configuration, telemetry, clustering, and secure endpoints. The BEAM enables rolling restarts and supervision resilience when configured correctly.

## Releases and Runtime Config

```bash
MIX_ENV=prod PHX_SERVER=true mix assets.deploy
MIX_ENV=prod mix release
_build/prod/rel/my_app/bin/my_app eval "IO.puts(:os.type())"
_build/prod/rel/my_app/bin/my_app start
```

`config/runtime.exs` for env-driven settings:
```elixir
config :my_app, MyApp.Repo,
  url: System.fetch_env!("DATABASE_URL"),
  pool_size: String.to_integer(System.get_env("POOL_SIZE", "10")),
  ssl: true

config :my_app, MyAppWeb.Endpoint,
  url: [host: System.fetch_env!("PHX_HOST"), port: 443, scheme: "https"],
  http: [ip: {0,0,0,0}, port: String.to_integer(System.get_env("PORT", "4000"))],
  secret_key_base: System.fetch_env!("SECRET_KEY_BASE"),
  server: true
```

**Secrets**
- Prefer env vars or secret stores (AWS/GCP KMS, Vault); avoid embedding in configs.
- Generate `SECRET_KEY_BASE` with `mix phx.gen.secret`.

## Clustering and PubSub/Presence

Add `libcluster` for automatic node discovery:
```elixir
# mix.exs deps
{:libcluster, "~> 3.3"},
{:phoenix_pubsub, "~> 2.1"},

# application.ex
topologies = [
  dns_poll: [
    strategy: Cluster.Strategy.DNSPoll,
    config: [poll_interval: 5_000, query: "my-app.internal"],
    connect: {:net_adm, :ping}
  ]
]

children = [
  {Cluster.Supervisor, [topologies, [name: MyApp.ClusterSupervisor]]},
  {Phoenix.PubSub, name: MyApp.PubSub},
  MyAppWeb.Endpoint
]
```

**Guidelines**
- Share `secret_key_base` across nodes for consistent session signing.
- Use distributed PubSub for Presence; ensure node connectivity before enabling Presence-heavy features.
- For blue/green, keep cookies compatible between versions.

## Telemetry, Logging, and Metrics

- Install `opentelemetry_phoenix` and `opentelemetry_ecto` for traces/metrics.
- Add `Plug.Telemetry` and `LoggerJSON` or structured logging.
- Export metrics (Prometheus/OpenTelemetry) via `:telemetry_poller` for VM stats (reductions, memory, schedulers).
- Set `LOGGER_LEVEL=info` in prod; use `:debug` only for troubleshooting.

## HTTP and Network Hardening

- Enforce HTTPS (`force_ssl`), HSTS, secure cookies (`same_site`, `secure`), and proper `content_security_policy`.
- CORS: configure `cors_plug` for API origins.
- Rate limiting: apply plugs (ETS/Cachex token bucket) or edge (NGINX/Cloudflare).
- Uploads: prefer presigned URLs; limit request body size (`:max_request_line_length`, `:max_header_value_length`).

## Assets and Static Delivery

- `mix assets.deploy` runs npm/tailwind/esbuild and digests assets.
- Serve static files via CDN/reverse proxy; ensure `cache-control` headers set in Endpoint.
- Disable unused watchers in production to trim image size.

## Background Jobs

- Oban recommended for retries/backoff, scheduled jobs, and isolation; supervise in `application.ex`.
- Configure queues via runtime env; monitor with Oban Web/Pro or telemetry.
- For CPU-heavy tasks, consider pooling or external workers to avoid blocking schedulers.

## Deployment Patterns

- **Containers**: multi-stage builds; run `mix deps.get --only prod`, `mix compile`, `mix assets.deploy`, then `mix release`.
- **Systemd**: run release binary as service with `Environment=` secrets; add `Restart=on-failure`.
- **Fly/Gigalixir/Render**: supply env vars, attach Postgres/Redis, open long-lived WebSocket ports.
- **Blue/green or canary**: keep DB migrations compatible; deploy code first, then run migrations; keep feature flags for schema changes.

## Observability and Health

- Add `/health` and `/ready` endpoints (Repo check + PubSub/Presence check).
- Export VM metrics: run `:telemetry_poller` for scheduler utilization and memory.
- Alert on error rates, DB timeouts, queue depths, and VM memory.

## Common Pitfalls

- Building releases without `PHX_SERVER=true` (endpoint won’t start).
- Missing runtime config in `config/runtime.exs`; relying on compile-time config for secrets.
- No cluster discovery configured → Presence inconsistencies across nodes.
- Leaving default `secret_key_base` or per-node keys → invalid sessions after deploy.
- Large assets without digests/CDN → slow cold loads.
