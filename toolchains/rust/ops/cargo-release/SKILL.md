---
name: cargo-release
description: "PM-invocable protocol for Cargo publish and release operations in the trusty-tools Rust monorepo: semver rules, 10-step release sequence, macOS codesign safety, and cross-crate dependency ordering"
user-invocable: false
disable-model-invocation: true
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "10-step Cargo release sequence with semver rules, macOS codesign safety, and cross-crate dependency ordering"
    when_to_use: "When user says 'release', 'publish', 'bump version', 'ship', or 'tag a release' for any crate in the monorepo"
    quick_start: "1. Determine semver bump  2. Update Cargo.toml(s)  3. Quality gates  4. Commit + tag + push  5. cargo publish  6. cargo install --locked (for binaries)"
  token_estimate:
    entry: 140
    full: 1800
context_limit: 800
tags:
  - rust
  - cargo
  - release
  - publish
  - semver
  - versioning
  - monorepo
  - codesign
  - ops
requires_tools: []
---

# Cargo Release Protocol

## When to Invoke

Invoke this protocol when the user says: "release", "publish", "bump version", "ship", "tag a release", or "cut a version" for any crate in the trusty-tools monorepo.

## Semver Bump Rules

Determine the version increment from the commit history since the last tag:

| Commit type | Bump |
|---|---|
| `BREAKING CHANGE` footer or `!` suffix (e.g. `feat!:`) | **Major** (X.0.0) |
| `feat:` — new capability, no breaking change | **Minor** (0.X.0) |
| `fix:`, `chore:`, `refactor:`, `perf:`, `docs:`, `test:` | **Patch** (0.0.X) |

For the `trusty-mpm-*` family, all eight crates share a single workspace version and are bumped together regardless of which crate was touched.

## Crate Name vs Directory Name

Cargo `-p` flags use the **`name` field in `Cargo.toml`**, not the directory name:

| Directory | Cargo flag | Tag prefix |
|---|---|---|
| `crates/trusty-git-analytics/` | `-p tga` | `tga-v` |
| `crates/open-mpm/` | `-p open-mpm` | `open-mpm-v` |

All others: directory name equals crate name (e.g. `crates/trusty-search/` → `-p trusty-search`, tag `trusty-search-v`).

## 10-Step Release Sequence

Execute steps in order. **Stop on any failure.**

### Step 1 — Bump the crate version

```toml
# crates/<name>/Cargo.toml
[package]
version = "0.5.1"   # was 0.5.0
```

For `trusty-mpm-*`, the version is set under `[workspace.package]` in the root `Cargo.toml`. Bump it once; all `trusty-mpm-*` crates inherit it.

### Step 2 — Update all dependent crates in the workspace

If other crates pin the version being bumped (e.g. `trusty-common = "0.4.20"`), update every occurrence to the new version. Use `grep` to find all pins:

```bash
grep -r '"<old-version>"' crates/ --include="Cargo.toml"
```

Never commit Step 1 without completing Step 2 — a partial update breaks `cargo check` workspace-wide.

### Step 3 — Quality gate: tests

```bash
cargo test -p <crate>
```

Must produce: `test result: ok. N passed; 0 failed; ...`

### Step 4 — Quality gate: clippy

```bash
cargo clippy -p <crate> -- -D warnings
```

Must produce no warnings. See `rust-quality-gate` for the `open-mpm` exception.

### Step 5 — Quality gate: format

```bash
cargo fmt --check
```

Must produce no output (exit 0). Fix with `cargo fmt` if needed.

### Step 6 — Commit the version bump

```bash
git add crates/<name>/Cargo.toml   # and any updated dependent Cargo.toml files
git commit -m "chore(<crate>): bump to v<version>"
```

Example: `chore(trusty-memory): bump to v0.5.1`

For `trusty-mpm-*` family: `chore(trusty-mpm): bump to v0.7.0`

### Step 7 — Create the git tag

Tag format: `<crate-name>-v<version>`

```bash
git tag trusty-memory-v0.5.1
```

Examples:
- `trusty-search-v1.2.0`
- `trusty-memory-v0.5.1`
- `tga-v0.3.0`
- `open-mpm-v0.2.1`
- `trusty-mpm-cli-v0.7.0` (one tag per `trusty-mpm-*` crate)

### Step 8 — Push the tag to GitHub

```bash
git push origin trusty-memory-v0.5.1
```

Push the commit first if not already on the remote:
```bash
git push origin main   # or the current branch
git push origin trusty-memory-v0.5.1
```

### Step 9 — Publish to crates.io

```bash
cargo publish -p trusty-memory
```

**Publishing order for cross-crate deps**: publish dependencies before consumers. If `trusty-common` is being published alongside `trusty-search`, publish `trusty-common` first and wait for the index to propagate (~30 seconds) before publishing `trusty-search`.

**`publish = false` crates — skip this step**: Some crates are not published to crates.io. Check the crate's `Cargo.toml` for:
```toml
[package]
publish = false
```
Known non-published crates include those that are internal-only or tightly coupled to the monorepo. Skip Step 9 for these and proceed directly to Step 10.

### Step 10 — Install binary locally (binary crates only)

For crates that produce a binary, install it to PATH after publishing:

```bash
cargo install --path crates/<dir> --locked
```

Examples:
```bash
cargo install --path crates/trusty-search --locked
cargo install --path crates/trusty-mpm-cli --locked
cargo install --path crates/trusty-memory --locked
```

## macOS Codesign Safety Rule (Critical)

**NEVER copy a release binary directly to `~/.cargo/bin/`:**

```bash
# WRONG — causes EXC_CRASH / CODESIGNING on macOS
cp target/release/trusty-search ~/.cargo/bin/trusty-search
```

On macOS, `cargo build` produces "ad-hoc linker-signed" binaries. The kernel's code-signing cache is keyed by `cdhash`. A plain `cp` over an existing on-PATH binary leaves the kernel with a stale cached identity. The next execution is killed with `EXC_CRASH / CODESIGNING — Taskgated Invalid Signature` before any code runs, producing only `zsh: killed` with zero output — indistinguishable from an OOM kill but unrelated.

`cargo install` writes to a temp path and renames atomically, keeping the signing cache consistent. Always use it.

If a manual copy was made by mistake, fix with:
```bash
codesign --force --sign - ~/.cargo/bin/<binary>
```

## trusty-mpm-* Family Release

The `trusty-mpm-*` family uses a shared workspace version. Release all eight crates together:

1. Bump `version` under `[workspace.package]` in root `Cargo.toml`.
2. Run quality gates across all `trusty-mpm-*` crates: `cargo test -p trusty-mpm-core`, `cargo test -p trusty-mpm-mcp`, etc.
3. Commit: `chore(trusty-mpm): bump to v<version>`.
4. Tag each crate separately: `trusty-mpm-core-v<version>`, `trusty-mpm-mcp-v<version>`, `trusty-mpm-daemon-v<version>`, `trusty-mpm-client-v<version>`, `trusty-mpm-cli-v<version>`, `trusty-mpm-tui-v<version>`, `trusty-mpm-telegram-v<version>`, `trusty-mpm-gui-v<version>`.
5. Publish publishable crates in dependency order (core → client → mcp/daemon/cli/tui/telegram/gui).
6. Install binaries: `cargo install --path crates/trusty-mpm-cli --locked`.

## Cross-Crate Library Release Checklist

When releasing a shared library (`trusty-common`, `trusty-mcp-core`, `trusty-embedder`, `trusty-symgraph`):

1. Bump library version (Step 1).
2. Update **all** dependent crates' `Cargo.toml` version pins (Step 2) — use `grep` to find every reference.
3. Run `cargo check` (workspace-wide) to confirm the workspace compiles with the new version.
4. Run `cargo test -p <lib>` and `cargo test -p <consumer>` for each dependent.
5. Commit all Cargo.toml changes together — workspace builds are atomic.
6. Publish the library first; wait ~30 seconds for index propagation.
7. Publish consumers in order.

## Evidence Required

After completing the release, report:

```
Released: trusty-memory v0.5.1
Tag: trusty-memory-v0.5.1 (pushed to origin)
Published: https://crates.io/crates/trusty-memory/0.5.1
Installed: cargo install --path crates/trusty-memory --locked ✓
Test result: ok. 87 passed; 0 failed; 5 ignored
Clippy: clean
Fmt: clean
```

## Anti-Patterns

- Copying binaries with `cp` instead of `cargo install` on macOS — causes `zsh: killed` / codesign crash.
- Publishing a consumer crate before its newly-bumped library dependency is available on crates.io.
- Forgetting to update dependent crates' version pins after bumping a library — breaks workspace compilation.
- Tagging before quality gates pass — a bad tag requires a follow-up patch release.
- Using `cargo install` without `--locked` — may resolve different dependency versions than what was tested.
- Skipping Step 2 for `trusty-mpm-*` — the shared workspace version must be consistent across all eight crates.
