# Golang Web Stack

**Version:** 1.0.0
**Category:** Golang
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Production-ready Go service stack for HTTP APIs and gRPC services, including database patterns, concurrency primitives, testing strategies, observability defaults, CI security scanning, and Docker packaging.

## Included Skills

- **golang-http-frameworks** (toolchains/golang/web) - net/http + routers (Chi/Gin/Echo/Fiber), middleware, REST patterns
- **golang-grpc** (toolchains/golang/grpc) - protobuf-first APIs, interceptors, deadlines, streaming, TLS, bufconn tests
- **golang-concurrency-patterns** (toolchains/golang/concurrency) - context cancellation, errgroup, bounded concurrency, leak/race pitfalls
- **golang-database-patterns** (toolchains/golang/data) - sqlx/pgx patterns, repository design, pooling, transactions, migrations
- **golang-observability-opentelemetry** (toolchains/golang/observability) - tracing/metrics/logging defaults (OTel, Prometheus, slog)
- **golang-testing-strategies** (toolchains/golang/testing) - table-driven tests, gomock/testify, benchmarks, `-race`, CI patterns
- **api-design-patterns** (universal/web/api-design-patterns) - resource design, error shapes, pagination, idempotency
- **security-scanning** (universal/security/security-scanning) - CI scanning workflow (secrets, deps, SAST) + triage/exceptions
- **docker** (toolchains/universal/infrastructure/docker) - container packaging, compose workflows, prod patterns

## Use Cases

**When to Deploy This Bundle:**
- Building Go REST APIs or service-to-service RPC
- Running web services with a SQL database
- Hardening Go services with testing + observability defaults
- Adding baseline CI security scanning and Docker packaging

**What You Get:**
- A clear path from API design → implementation → tests → deployable container
- Production defaults for cancellation, timeouts, graceful shutdown, and instrumentation
- Playbooks for gRPC contracts, interceptors, and streaming patterns

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
| golang-http-frameworks | ✅ Yes | 🚀 Enhanced | api-design-patterns (recommended) |
| golang-grpc | ✅ Yes | 🚀 Enhanced | golang-concurrency-patterns (recommended) |
| golang-concurrency-patterns | ✅ Yes | 🚀 Enhanced | None |
| golang-database-patterns | ✅ Yes | 🚀 Enhanced | None |
| golang-observability-opentelemetry | ✅ Yes | 🚀 Enhanced | None |
| golang-testing-strategies | ✅ Yes | 🚀 Enhanced | None |
| api-design-patterns | ✅ Yes | 🚀 Enhanced | None |
| security-scanning | ✅ Yes | 🚀 Enhanced | None |
| docker | ✅ Yes | 🚀 Enhanced | None |

**Bundle Synergies:**
- golang-http-frameworks + golang-observability-opentelemetry: instrument middleware with trace IDs and structured logs
- golang-concurrency-patterns + golang-testing-strategies: prevent goroutine leaks with `-race`, timeouts, and errgroup patterns
- golang-database-patterns + docker: run ephemeral Postgres + migrations in local compose for integration tests
- security-scanning + docker: scan images/SBOMs and gate high-signal findings in CI

## Integration Example

```go
package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	_ "github.com/jackc/pgx/v5/stdlib"
	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
	"golang.org/x/sync/errgroup"
)

type User struct {
	ID    string `json:"id"`
	Email string `json:"email"`
}

type Repo struct{ db *sql.DB }

func (r *Repo) GetUser(ctx context.Context, id string) (User, error) {
	var u User
	err := r.db.QueryRowContext(ctx, `select id, email from users where id = $1`, id).Scan(&u.ID, &u.Email)
	if err != nil {
		return User{}, err
	}
	return u, nil
}

func main() {
	slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, nil)))

	db, err := sql.Open("pgx", os.Getenv("DATABASE_URL"))
	if err != nil {
		slog.Error("db open failed", "err", err)
		os.Exit(1)
	}
	defer db.Close()

	repo := &Repo{db: db}

	mux := http.NewServeMux()
	mux.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
		u, err := repo.GetUser(r.Context(), r.PathValue("id"))
		if err != nil {
			if errors.Is(err, sql.ErrNoRows) {
				http.Error(w, "not found", http.StatusNotFound)
				return
			}
			http.Error(w, "internal error", http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(u)
	})

	srv := &http.Server{
		Addr:              ":8080",
		Handler:           otelhttp.NewHandler(mux, "http"),
		ReadHeaderTimeout: 5 * time.Second,
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	g, ctx := errgroup.WithContext(ctx)
	g.Go(func() error {
		<-ctx.Done()
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		return srv.Shutdown(shutdownCtx)
	})
	g.Go(func() error {
		err := srv.ListenAndServe()
		if errors.Is(err, http.ErrServerClosed) {
			return nil
		}
		return err
	})

	if err := g.Wait(); err != nil {
		slog.Error("service failed", "err", err)
		os.Exit(1)
	}
}
```

## Version History

- **1.0.0** (2025-12-17): Initial release with 9 skills for Go web services

