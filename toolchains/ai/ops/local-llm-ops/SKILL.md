---
name: local-llm-ops
description: Local LLM operations with Ollama on Apple Silicon, including setup, model pulls, chat launchers, benchmarks, and diagnostics.
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Run local LLMs with Ollama: setup venv, start service, pull models, launch chat, benchmark, and diagnose."
    when_to_use: "Operating local LLMs on macOS, running Ollama-based chat sessions, or benchmarking models for speed/latency."
    quick_start: "1. ./setup_chatbot.sh 2. ./chatllm 3. ollama pull mistral (if no models)"
tags:
  - llm
  - ollama
  - local
  - benchmark
  - chat
  - ops
---

# Local LLM Ops (Ollama)

## Overview

Your `localLLM` repo provides a full local LLM toolchain on Apple Silicon: setup scripts, a rich CLI chat launcher, benchmarks, and diagnostics. The operational path is: install Ollama, ensure the service is running, initialize the venv, pull models, then launch chat or benchmarks.

## Quick Start

```bash
./setup_chatbot.sh
./chatllm
```

If no models are present:

```bash
ollama pull mistral
```

## Setup Checklist

1. Install Ollama: `brew install ollama`
2. Start the service: `brew services start ollama`
3. Run setup: `./setup_chatbot.sh`
4. Verify service: `curl http://localhost:11434/api/version`

## Chat Launchers

- `./chatllm` (primary launcher)
- `./chat` or `./chat.py` (alternate launchers)
- Aliases: `./install_aliases.sh` then `llm`, `llm-code`, `llm-fast`

Task modes:

```bash
./chat -t coding -m codellama:70b
./chat -t creative -m llama3.1:70b
./chat -t analytical
```

## Benchmark Workflow

Benchmarks are scripted in `scripts/run_benchmarks.sh`:

```bash
./scripts/run_benchmarks.sh
```

This runs `bench_ollama.py` with:

- `benchmarks/prompts.yaml`
- `benchmarks/models.yaml`
- Multiple runs and max token limits

## Diagnostics

Run the built-in diagnostic script when setup fails:

```bash
./diagnose.sh
```

Common fixes:

- Re-run `./setup_chatbot.sh`
- Ensure `ollama` is in PATH
- Pull at least one model: `ollama pull mistral`

## Operational Notes

- Virtualenv lives in `.venv`
- Chat configs and sessions live under `~/.localllm/`
- Ollama API runs at `http://localhost:11434`

## Related Skills

- `toolchains/universal/infrastructure/docker`
