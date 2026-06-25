---
name: ort
description: "ONNX Runtime in Rust via the `ort` crate (2.x): loading sessions, configuring CPU/CoreML/CUDA execution providers, tensor I/O with ndarray, async-safe spawn_blocking wrapping, global thread-pool init, and debugging provider/opset issues"
user-invocable: false
disable-model-invocation: true
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Load ONNX models in Rust with the ort 2.x crate: commit the global thread pool once, build a Session with providers in priority order (CUDA > CoreML > CPU), run inference inside spawn_blocking, and mark integration tests #[ignore]"
    when_to_use: "When adding or using ONNX models in Rust — embedders, VAD/STT/TTS, classifiers; when targeting CoreML on Apple Silicon or CUDA on Linux/Windows; when debugging silent execution-provider fallback or opset compatibility"
    quick_start: "1. Add ort dep + features  2. Commit global thread pool once at startup  3. Build Session with providers in priority order  4. Wrap run() in spawn_blocking  5. Mark ONNX tests #[ignore]"
  token_estimate:
    entry: 160
    full: 4200
context_limit: 800
tags:
  - rust
  - ort
  - onnx
  - ml
  - inference
  - embeddings
  - coreml
  - cuda
  - ndarray
requires_tools: []
---

# ONNX Runtime in Rust (`ort` 2.x)

## Overview

`ort` is the Rust binding to ONNX Runtime. Use it when you need to run
ONNX-format models locally — text embedders, speech models, classifiers — with
hardware-accelerated execution providers (CoreML on Apple Silicon, CUDA on
Linux/Windows). The `ort` 2.x API changed significantly from 1.x; all patterns
here target `ort = "=2.0.0-rc.12"` (the version pinned by fastembed-rs).

Reference implementation: `crates/trusty-common/src/embedder/fast_embedder.rs`

## Quick Start

### 1. Cargo.toml setup

**Library crate** (default-features = false avoids linking the bundled ORT runtime
unnecessarily; consumers opt into ONNX via a feature):

```toml
# Why: pin to the exact rc version fastembed-rs requires to avoid ABI mismatch.
# What: base features give std + the 24-API-level surface; coreml is macOS-only.
[dependencies.ort]
version = "=2.0.0-rc.12"
default-features = false
features = ["std", "api-24"]
optional = true

# macOS: add CoreML EP (builds to .mlmodelc, runs on ANE/GPU).
[target.'cfg(target_os = "macos")'.dependencies.ort]
version = "=2.0.0-rc.12"
default-features = false
features = ["coreml", "std", "api-24"]
optional = true

# ndarray interop (zero-copy tensor views).
ndarray = { version = "0.16", optional = true }
```

**Binary / daemon crate** (load-dynamic avoids statically linking libonnxruntime
into the binary, reducing binary size when the shared lib is already present):

```toml
[dependencies.ort]
version = "=2.0.0-rc.12"
default-features = false
features = ["load-dynamic", "std", "api-24"]

# For CUDA GPU inference on Linux:
# features = ["load-dynamic", "cuda", "std", "api-24"]
```

**ndarray tensor interop** (add alongside ort):

```toml
# Why: ort's TensorRef::from_array_view needs ndarray's ArrayView.
# What: zero-copy conversion between ndarray arrays and ort Tensors.
ndarray = { version = "0.16", features = ["std"] }
# or in Cargo.toml features = ["std", "ndarray"] on the ort dep directly
```

## Core Concepts

### 2. Global ORT thread pool — commit ONCE before any Session

ORT's per-session thread pool cannot be overridden from outside the session
builder. The only lever that reaches an opaque session (e.g., one built
internally by fastembed-rs) is the **global** environment thread pool. Commit it
exactly once, before any `Session` is created.

> **Why this matters:** The deferred-embed deadlock (trusty-tools issue #1668 /
> originally #1542) was traced to fastembed's internal session hardcoding
> `with_intra_threads(available_parallelism())`. On a multi-core host, 8+ ORT
> threads spawn; two busy-wait at ~70% CPU while the rest block forever inside
> `condition_variable::wait`, yielding zero embeddings and an empty HNSW index.
> Committing a global pool with `intra_threads = 1` and `spin_control = false`
> causes ORT to call `DisablePerSessionThreads`, overriding fastembed's value.

```rust
use std::sync::OnceLock;

/// Why: record the committed threading opts so we log them once and can
/// surface them via /health or diagnostics.
/// What: stores the resolved OrtThreadingOptions committed to the global pool.
/// Test: resolver unit tests in mod.rs; actual commit is #[ignore]-tested.
static ORT_RUNTIME: OnceLock<OrtThreadingOptions> = OnceLock::new();

/// Why: commit the ORT global thread pool BEFORE any Session is created.
///
/// What: reads TRUSTY_ORT_INTRA_THREADS / TRUSTY_ORT_INTER_THREADS /
/// TRUSTY_ORT_ALLOW_SPINNING (defaults: 1 / 1 / false), builds
/// GlobalThreadPoolOptions, calls ort::init().with_global_thread_pool().commit().
/// The commit call returns `true` on success, `false` if an environment already
/// exists (meaning another Session was created first — the deadlock fix did NOT
/// take effect).
///
/// Test: #[ignore] ONNX integration tests verify round-trip inference after init.
fn init_ort_runtime() {
    ORT_RUNTIME.get_or_init(|| {
        let intra = std::env::var("TRUSTY_ORT_INTRA_THREADS")
            .ok()
            .and_then(|v| v.parse::<i16>().ok())
            .unwrap_or(1);
        let inter = std::env::var("TRUSTY_ORT_INTER_THREADS")
            .ok()
            .and_then(|v| v.parse::<i16>().ok())
            .unwrap_or(1);
        let spinning = std::env::var("TRUSTY_ORT_ALLOW_SPINNING")
            .map(|v| v == "1" || v.eq_ignore_ascii_case("true"))
            .unwrap_or(false);

        let pool = ort::environment::GlobalThreadPoolOptions::default()
            .with_intra_threads(intra)
            .and_then(|p| p.with_inter_threads(inter))
            .and_then(|p| p.with_spin_control(spinning));

        match pool {
            Ok(pool) => {
                let committed = ort::init().with_global_thread_pool(pool).commit();
                if committed {
                    tracing::info!(
                        intra_threads = intra,
                        inter_threads = inter,
                        allow_spinning = spinning,
                        "ORT global thread pool committed (DisablePerSessionThreads active)"
                    );
                } else {
                    tracing::warn!(
                        "ORT environment already committed before init_ort_runtime() — \
                         deadlock fix did NOT take effect; ensure no Session is created \
                         before calling init_ort_runtime()"
                    );
                }
            }
            Err(e) => {
                tracing::error!(
                    error = %e,
                    "Failed to build ORT global thread pool options; falling back to defaults"
                );
            }
        }

        OrtThreadingOptions { intra_threads: intra, inter_threads: inter, allow_spinning: spinning }
    });
}
```

### 3. Build a Session with providers in priority order

Providers are tried in registration order; the first available one wins. Always
register more-capable (faster) providers first with CPU as the unconditional
fallback.

```rust
use ort::{GraphOptimizationLevel, Session};

/// Why: build an ORT session with accelerated EP if available, CPU fallback.
/// What: CUDA (if feature enabled) > CoreML (macOS) > CPU (always).
///   Disables the BFC arena on CPU to prevent 19–53 GB virtual address pre-alloc.
/// Test: mock path; actual model load is #[ignore]-tested.
fn build_session(model_bytes: &[u8]) -> anyhow::Result<Session> {
    // CPU provider — always last, arena disabled to avoid massive VA reservation.
    // Why: ort's default CPU BFCArena pre-allocates 19–53 GB of virtual address
    // space on first inference; disable it to keep RSS predictable.
    let cpu = ort::execution_providers::CPU::default()
        .with_arena_allocator(false)
        .build();

    let mut providers: Vec<ort::execution_providers::ExecutionProviderDispatch> = Vec::new();

    // CUDA (Linux/Windows GPU inference).
    #[cfg(feature = "embedder-cuda")]
    {
        use ort::ep::ArenaExtendStrategy;
        providers.push(
            ort::ep::CUDA::default()
                .with_arena_extend_strategy(ArenaExtendStrategy::SameAsRequested)
                .with_memory_limit(12 * 1024 * 1024 * 1024) // 12 GiB cap
                .build(),
        );
    }

    // CoreML (Apple Silicon — ANE/GPU).
    #[cfg(all(target_os = "macos", feature = "coreml"))]
    {
        use ort::ep::CoreML;
        providers.push(
            CoreML::default()
                .with_static_input_shapes(true)
                .with_specialization_strategy(
                    ort::ep::coreml::CoreMLSpecializationStrategy::FastPrediction,
                )
                .build(),
        );
    }

    providers.push(cpu);

    // commit_from_memory_directly: zero-copy if bytes outlive the session.
    // Use commit_from_file for a path, commit_from_memory for a Vec<u8>.
    let session = Session::builder()?
        .with_optimization_level(GraphOptimizationLevel::All)?
        .with_execution_providers(providers)?
        .commit_from_memory_directly(model_bytes)?;

    Ok(session)
}
```

> **Tip:** `commit_from_file`, `commit_from_memory`, and `commit_from_memory_directly`
> are the terminal builder calls. There is no standalone `.build()`.

### 4. Tensor I/O with ndarray

```rust
use ndarray::{Array2, ArrayView2};
use ort::{inputs, tensor::{Tensor, TensorRef}};

/// Why: wrap ndarray arrays into ORT tensors without copying data where possible.
/// What: TensorRef::from_array_view is zero-copy; Tensor::from_array owns data.
/// Test: #[ignore] integration test with real model.
fn run_inference(
    session: &mut ort::Session,
    input: ArrayView2<'_, f32>,
) -> anyhow::Result<Array2<f32>> {
    // Zero-copy view — input array must outlive the TensorRef.
    let tensor = TensorRef::from_array_view(input)?;

    // Named input; name must match the ONNX graph's input node name.
    let outputs = session.run(inputs!["input_ids" => &tensor])?;

    // Extract as owned ndarray.
    let embedding: Array2<f32> = outputs[0]
        .try_extract_array::<f32>()?
        .into_dimensionality::<ndarray::Ix2>()?
        .to_owned();

    Ok(embedding)
}

// Dynamic batch size: disable memory pattern to allow variable batch shapes.
fn build_dynamic_session(model_bytes: &[u8]) -> anyhow::Result<ort::Session> {
    Ok(Session::builder()?
        .with_memory_pattern(false)?     // allow dynamic batch dimension
        .with_optimization_level(GraphOptimizationLevel::All)?
        .commit_from_memory_directly(model_bytes)?)
}
```

### 5. Async wrapping — never run inference on a tokio thread

`Session` is `Send + Sync` but `run()` takes `&mut self`. Wrap behind a
`parking_lot::Mutex` and call from `spawn_blocking`.

```rust
use parking_lot::Mutex;
use std::sync::Arc;
use tokio::task;

/// Why: ORT inference is CPU-bound and blocks; running it on a tokio async
///   thread starves the executor and can deadlock the blocking thread pool.
/// What: Arc<Mutex<Session>> allows sharing across tasks; spawn_blocking
///   moves the lock-and-run onto a dedicated blocking thread.
/// Test: unit tests use a MockEmbedder; #[ignore] tests hit a real model.
pub struct OrtInferencer {
    session: Arc<Mutex<ort::Session>>,
}

impl OrtInferencer {
    /// Initialise EAGERLY at startup — do NOT defer behind Mutex<Option<Session>>.
    ///
    /// Why: the #1668 deferred-init deadlock: if multiple tokio tasks race to
    ///   initialise the session concurrently (all blocked on the same
    ///   Mutex<Option<Session>>), each calls spawn_blocking, exhausting the
    ///   blocking thread pool. Eager init at startup means the Session exists
    ///   before any request arrives.
    pub async fn new(model_bytes: Vec<u8>) -> anyhow::Result<Self> {
        let session = task::spawn_blocking(move || -> anyhow::Result<ort::Session> {
            // Commit global thread pool FIRST (idempotent via OnceLock).
            init_ort_runtime();
            build_session(&model_bytes)
        })
        .await
        .context("spawn_blocking error during Session init")??;

        Ok(Self {
            session: Arc::new(Mutex::new(session)),
        })
    }

    pub async fn embed(&self, input: Vec<f32>, shape: [usize; 2]) -> anyhow::Result<Vec<f32>> {
        let session = Arc::clone(&self.session);
        task::spawn_blocking(move || -> anyhow::Result<Vec<f32>> {
            use ndarray::Array2;
            let arr = Array2::from_shape_vec(shape, input)?;
            let mut guard = session.lock();
            let result = run_inference(&mut guard, arr.view())?;
            Ok(result.into_raw_vec())
        })
        .await
        .context("spawn_blocking error during inference")?
    }
}
```

> **Anti-pattern:** `Mutex<Option<Session>>` with lazy init — concurrent callers
> all call `spawn_blocking` to race at init, exhaust the pool, and deadlock.
> Initialise `Arc<Session>` eagerly at startup instead.

## Testing

Mark ONNX integration tests `#[ignore]` so CI stays fast while still allowing
local validation with a real model:

```rust
/// Why: downloading a real ONNX model (~22 MB) in CI adds 30-60s and
///   requires network access; mark #[ignore] to exclude from default runs.
/// What: verifies the full init → inference → dimension check pipeline.
/// Test: run with `cargo test -p my-crate --features embedder -- --include-ignored`
#[tokio::test]
#[ignore = "requires ONNX model download (~22 MB); run with --include-ignored"]
async fn embedder_returns_correct_dim() {
    let model_bytes = std::fs::read("tests/fixtures/model.onnx").unwrap();
    let inferencer = OrtInferencer::new(model_bytes).await.unwrap();
    let output = inferencer.embed(vec![0.0_f32; 128], [1, 128]).await.unwrap();
    assert_eq!(output.len(), 384, "embedding dim should be 384");
}

/// Why: non-ONNX unit tests must always run (no model download needed).
/// What: exercises the mock path without ORT.
/// Test: always runs in CI.
#[tokio::test]
async fn mock_embedder_returns_correct_dim() {
    // Use a MockEmbedder that returns fixed-size zero vectors.
    let mock = MockEmbedder::new(384);
    let result = mock.embed_batch(&["hello world".to_string()]).await.unwrap();
    assert_eq!(result[0].len(), 384);
}
```

**Run commands:**

```bash
# Fast: no model download; runs in CI.
cargo test -p my-crate --features embedder

# Full: downloads ONNX model and runs integration tests.
cargo test -p my-crate --features embedder -- --include-ignored

# Single named test.
cargo test -p my-crate --features embedder -- embedder_returns_correct_dim --include-ignored --nocapture
```

## Gotchas

### Silent execution-provider fallback

ORT silently falls back to CPU when a registered EP is unavailable. Always log
the resolved EP or call `ep.is_available()` before building the Session.

```rust
// Detect fallback: log SILENT FALLBACK with the expected vs actual provider.
if expected_provider != ExecutionProvider::Cpu {
    tracing::error!(
        "SILENT FALLBACK: {} EP failed — running on CPU. \
         Inference will be slower than expected.",
        expected_provider
    );
}
```

### CoreML silent FP16 cast

CoreML may silently cast FP32 weights to FP16, reducing precision. Export your
model in MLProgram format (`mlpackage`) rather than NeuralNetwork (`mlmodel`) to
avoid the cast.

### CPU arena pre-allocation

ORT's default CPU BFCArena reserves 19–53 GB of virtual address space on first
inference (issue #89). Always pass `.with_arena_allocator(false)` on the CPU
provider.

### `ort::init()` must precede all Sessions

Call `init_ort_runtime()` (which calls `ort::init().commit()`) before any
`Session::builder()...commit_from_*()` call. Once any session exists, the
global environment is locked and the thread-pool commit returns `false`.

### `run()` needs `&mut self` — must use Mutex or pool

ORT's `Session::run()` takes `&mut self`. Wrap in `Mutex<Session>` for
concurrent access, or use a pool of sessions. Never expose `&Session` directly
from an `Arc`.

### CoreML cold-start compile to `.mlmodelc`

On first run, CoreML compiles the model to a `.mlmodelc` bundle. Set a
persistent `model_cache_dir` on the CoreML EP so recompilation is skipped on
restarts. Without a cache dir, every process restart pays the compile cost.

### Export opset

ONNX opset ≤ 16 is the safest target for broad ORT compatibility. ORT may
refuse or silently degrade models exported at opset 17+ with older runtime
versions.

### Windows DLL conflicts with `load-dynamic`

When using the `load-dynamic` feature on Windows, ensure only one copy of
`onnxruntime.dll` is on `PATH`. Conflicting copies from different packages
cause runtime crashes at session creation.

### Forgetting the `"std"` feature

Without `features = ["std"]`, `commit_from_file` and related APIs are not
available. `default-features = false` is correct for library crates but always
add `"std"` back explicitly.

## Decision Trees

### Which session commit call?

| Situation | API |
|---|---|
| Model bytes already in memory, bytes outlive session | `commit_from_memory_directly(&bytes)` |
| Model bytes in a `Vec<u8>`, want ORT to own a copy | `commit_from_memory(bytes.as_slice())` |
| Model is a file on disk | `commit_from_file("/path/to/model.onnx")` |

### Which execution provider?

| Hardware | Recommended EP | Notes |
|---|---|---|
| Apple Silicon (M1–M4) | CoreML | Add `features = ["coreml"]`; cold-compile on first run |
| NVIDIA GPU (Linux) | CUDA | Add `features = ["cuda"]`; cap memory with `with_memory_limit` |
| CPU-only / CI | CPU | Always last; disable arena with `with_arena_allocator(false)` |

## Anti-Patterns

- Calling `ort::init()` after creating any Session — the commit returns `false` and the thread pool is not set.
- Using `unwrap()` inside `spawn_blocking` closures — panics in a blocking thread are not caught by the async runtime; use `?` and propagate via `anyhow::Result`.
- Deferring Session init behind `Mutex<Option<Session>>` — concurrent callers exhaust the blocking thread pool (the #1668 deadlock).
- Registering CUDA or CoreML but not logging the fallback when they are unavailable — silent performance regressions.
- Dynamic batch inference without `.with_memory_pattern(false)` — ORT pre-allocates for the first batch shape and panics on a different shape.

## Resources

- Reference implementation: `crates/trusty-common/src/embedder/fast_embedder.rs`
- `#[ignore]` ONNX test pattern: `crates/trusty-embedderd/tests/bit_identical.rs`
- ort crate docs: https://docs.rs/ort
- ort guide: https://ort.pyke.io
- ONNX Runtime graph optimizations: https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html
- ONNX opset compatibility matrix: https://onnxruntime.ai/docs/reference/compatibility.html
