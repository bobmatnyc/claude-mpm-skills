---
name: clap
description: "Build production Rust CLIs with Clap: subcommands, config layering, validation, exit codes, shell completions, and testable command surfaces"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Create ergonomic, testable Rust CLIs using Clap derive, subcommands, and config layering (CLI + env + config file)"
    when_to_use: "When building Rust CLI tools that need reliable argument parsing, good help UX, strong validation, and automated tests"
    quick_start: "1. Add clap (derive) 2. Define Args + Subcommand 3. Parse once in main 4. Map errors to exit codes 5. Test with assert_cmd"
  token_estimate:
    entry: 120
    full: 4500
context_limit: 700
tags:
  - rust
  - cli
  - clap
  - config
  - testing
requires_tools: []
---

# Clap (Rust) - Production CLI Patterns

## Overview

Clap provides declarative command-line parsing with strong help output, validation, and subcommand support. Use it to build CLIs with predictable UX and testable execution paths.

## Quick Start

### Minimal CLI

✅ **Correct: derive Parser**
```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "mytool", version, about = "Example CLI")]
struct Args {
    /// Enable verbose output
    #[arg(long)]
    verbose: bool,

    /// Input file path
    #[arg(value_name = "FILE")]
    input: String,
}

fn main() {
    let args = Args::parse();
    if args.verbose {
        eprintln!("verbose enabled");
    }
    println!("input={}", args.input);
}
```

❌ **Wrong: parse multiple times**
```rust
fn main() {
    let _a = Args::parse();
    let _b = Args::parse(); // duplicate parsing and inconsistent behavior
}
```

## Subcommands (real tools)

Model multi-mode CLIs with subcommands and shared global flags.

✅ **Correct: global flags + subcommands**
```rust
use clap::{Parser, Subcommand, ValueEnum};

#[derive(Parser, Debug)]
struct Args {
    #[arg(long, global = true)]
    verbose: bool,

    #[arg(long, global = true, env = "MYTOOL_CONFIG")]
    config: Option<String>,

    #[command(subcommand)]
    cmd: Command,
}

#[derive(Subcommand, Debug)]
enum Command {
    Serve { #[arg(long, default_value_t = 3000)] port: u16 },
    Migrate { #[arg(long, value_enum, default_value_t = Mode::Up)] mode: Mode },
}

#[derive(Copy, Clone, Debug, ValueEnum)]
enum Mode { Up, Down }

fn main() {
    let args = Args::parse();
    match args.cmd {
        Command::Serve { port } => println!("serve on {}", port),
        Command::Migrate { mode } => println!("migrate: {:?}", mode),
    }
}
```

## Config layering (CLI + env + config file)

Prefer explicit precedence:

1. CLI flags
2. Environment variables
3. Config file
4. Defaults

✅ **Correct: merge config with CLI overrides**
```rust
use clap::Parser;
use serde::Deserialize;

#[derive(Parser, Debug)]
struct Args {
    #[arg(long, env = "APP_PORT")]
    port: Option<u16>,
}

#[derive(Deserialize)]
struct FileConfig {
    port: Option<u16>,
}

fn effective_port(args: &Args, file: &FileConfig) -> u16 {
    args.port.or(file.port).unwrap_or(3000)
}
```

## Exit codes and error handling

Map failures to stable exit codes. Return `Result` from command handlers and centralize printing.

✅ **Correct: command returns Result**
```rust
use std::process::ExitCode;

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("{e}");
            ExitCode::from(1)
        }
    }
}

fn run() -> Result<(), String> {
    Ok(())
}
```

## Testing (assert_cmd)

Test the binary surface (arguments, output, exit codes) without coupling to internals.

✅ **Correct: integration test**
```rust
use assert_cmd::Command;

#[test]
fn shows_help() {
    Command::cargo_bin("mytool")
        .unwrap()
        .arg("--help")
        .assert()
        .success();
}
```

## Shell completions (optional)

Generate completions for Bash/Zsh/Fish.

✅ **Correct: emit completions**
```rust
use clap::{CommandFactory, Parser};
use clap_complete::{generate, shells::Zsh};
use std::io;

fn print_zsh_completions() {
    let mut cmd = super::Args::command();
    generate(Zsh, &mut cmd, "mytool", &mut io::stdout());
}
```

## Anti-Patterns

- Parse arguments in library code; parse once in `main` and pass a typed config down.
- Hide failures behind `unwrap`; return stable exit codes and structured errors.
- Overload one command with flags; use subcommands for distinct modes.

## Resources

- Clap: https://docs.rs/clap
- assert_cmd: https://docs.rs/assert_cmd
- clap_complete: https://docs.rs/clap_complete

