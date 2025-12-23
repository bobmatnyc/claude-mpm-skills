---
name: axum
description: "Axum (Rust) web framework patterns for production APIs: routers/extractors, state, middleware, error handling, tracing, graceful shutdown, and testing"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Build production Rust APIs with Axum using typed extractors, Tower middleware, structured errors, tracing, and testable routers"
    when_to_use: "When building Rust HTTP APIs/services that need predictable middleware composition, strong typing, and production-ready shutdown/observability patterns"
    quick_start: "1. Add axum + tokio + tower-http 2. Build Router with typed handlers 3. Define AppState + error type 4. Add tracing + timeouts 5. Test router with ServiceExt"
  token_estimate:
    entry: 140
    full: 5500
context_limit: 800
tags:
  - rust
  - axum
  - tokio
  - http
  - api
  - tower
  - middleware
  - tracing
requires_tools: []
---

# Axum (Rust) - Production Web APIs

## Overview

Axum is a Rust web framework built on Hyper and Tower. Use it for type-safe request handling with composable middleware, structured errors, and excellent testability.

## Quick Start

### Minimal server

✅ **Correct: typed handler + JSON response**
```rust
use axum::{routing::get, Json, Router};
use serde::Serialize;
use std::net::SocketAddr;

#[derive(Serialize)]
struct Health {
    status: &'static str,
}

async fn health() -> Json<Health> {
    Json(Health { status: "ok" })
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/health", get(health));

    let addr: SocketAddr = "0.0.0.0:3000".parse().unwrap();
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

❌ **Wrong: block the async runtime**
```rust
async fn handler() {
    std::thread::sleep(std::time::Duration::from_secs(1)); // blocks executor
}
```

## Core Concepts

### Router + handlers

Handlers are async functions that return something implementing `IntoResponse`.

✅ **Correct: route nesting**
```rust
use axum::{routing::get, Router};

fn router() -> Router {
    let api = Router::new()
        .route("/users", get(list_users))
        .route("/users/:id", get(get_user));

    Router::new().nest("/api/v1", api)
}

async fn list_users() -> &'static str { "[]" }
async fn get_user() -> &'static str { "{}" }
```

### Extractors

Prefer extractors for parsing and validation at the boundary:

- `Path<T>`: typed path params
- `Query<T>`: query strings
- `Json<T>`: JSON bodies
- `State<T>`: shared application state

✅ **Correct: typed path + JSON**
```rust
use axum::{extract::Path, Json};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateUser {
    email: String,
}

#[derive(Serialize)]
struct User {
    id: String,
    email: String,
}

async fn create_user(Json(body): Json<CreateUser>) -> Json<User> {
    Json(User { id: "1".into(), email: body.email })
}

async fn get_user(Path(id): Path<String>) -> Json<User> {
    Json(User { id, email: "a@example.com".into() })
}
```

## Production Patterns

### 1) Shared state (DB pool, config, clients)

Use `State<Arc<AppState>>` and keep state immutable where possible.

✅ **Correct: AppState via Arc**
```rust
use axum::{extract::State, routing::get, Router};
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    build_sha: &'static str,
}

async fn version(State(state): State<Arc<AppState>>) -> String {
    state.build_sha.to_string()
}

fn app(state: Arc<AppState>) -> Router {
    Router::new().route("/version", get(version)).with_state(state)
}
```

### 2) Structured error handling (`IntoResponse`)

Centralize error mapping to HTTP status codes and JSON.

✅ **Correct: AppError converts into response**
```rust
use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::Serialize;

#[derive(Debug)]
enum AppError {
    NotFound,
    BadRequest(&'static str),
    Internal,
}

#[derive(Serialize)]
struct ErrorBody {
    error: &'static str,
}

impl IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        let (status, msg) = match self {
            AppError::NotFound => (StatusCode::NOT_FOUND, "not_found"),
            AppError::BadRequest(_) => (StatusCode::BAD_REQUEST, "bad_request"),
            AppError::Internal => (StatusCode::INTERNAL_SERVER_ERROR, "internal"),
        };

        (status, Json(ErrorBody { error: msg })).into_response()
    }
}
```

### 3) Middleware (Tower layers)

Use `tower-http` for production-grade layers: tracing, timeouts, request IDs, CORS.

✅ **Correct: trace + timeout + CORS**
```rust
use axum::{routing::get, Router};
use std::time::Duration;
use tower::ServiceBuilder;
use tower_http::{
    cors::{Any, CorsLayer},
    timeout::TimeoutLayer,
    trace::TraceLayer,
};

fn app() -> Router {
    let layers = ServiceBuilder::new()
        .layer(TraceLayer::new_for_http())
        .layer(TimeoutLayer::new(Duration::from_secs(10)))
        .layer(CorsLayer::new().allow_origin(Any));

    Router::new()
        .route("/health", get(|| async { "ok" }))
        .layer(layers)
}
```

### 4) Graceful shutdown

Terminate on SIGINT/SIGTERM and let in-flight requests drain.

✅ **Correct: with_graceful_shutdown**
```rust
async fn shutdown_signal() {
    let ctrl_c = async {
        tokio::signal::ctrl_c().await.ok();
    };

    #[cfg(unix)]
    let terminate = async {
        tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())
            .ok()
            .and_then(|mut s| s.recv().await);
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {}
        _ = terminate => {}
    }
}

#[tokio::main]
async fn main() {
    let app = app();
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();

    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}
```

## Testing

Test routers without sockets using `tower::ServiceExt`.

✅ **Correct: request/response test**
```rust
use axum::{body::Body, http::Request, Router};
use tower::ServiceExt;

#[tokio::test]
async fn health_returns_ok() {
    let app: Router = super::app();

    let res = app
        .oneshot(Request::builder().uri("/health").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(res.status(), 200);
}
```

## Decision Trees

### Axum vs other Rust frameworks

- Prefer **Axum** for Tower middleware composition and typed extractors.
- Prefer **Actix Web** for a mature ecosystem and actor-style runtime model.
- Prefer **Warp** for functional filters and minimalism.

## Anti-Patterns

- Block the async runtime (`std::thread::sleep`, blocking I/O inside handlers).
- Use `unwrap()` in request paths; return structured errors instead.
- Run without timeouts; add request timeouts and upstream deadlines.

## Resources

- Axum docs: https://docs.rs/axum
- Tower HTTP layers: https://docs.rs/tower-http
- Tracing: https://docs.rs/tracing

