---
name: vector-search-workflows
description: Vector search indexing and querying workflows using MCP Vector Search, including setup, reindexing, auto-index strategies, and MCP integration.
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Index a codebase with mcp-vector-search, keep it fresh with auto-indexing, and query via CLI or MCP integration."
    when_to_use: "Building semantic search for codebases, setting up MCP search tools, or troubleshooting indexing and reindexing workflows."
    quick_start: "1. mcp-vector-search setup 2. mcp-vector-search search \"query\" 3. mcp-vector-search index --force when schema changes"
tags:
  - vector-search
  - embeddings
  - indexing
  - search
  - mcp
---

# Vector Search Workflows (MCP Vector Search)

## Overview

Use `mcp-vector-search` to index codebases into ChromaDB and search via semantic embeddings. The recommended flow is `setup` (init + index + MCP integration), then `search`, and use `index` or `auto-index` to keep data fresh.

## Quick Start

```bash
pip install mcp-vector-search
mcp-vector-search setup
mcp-vector-search search "authentication logic"
```

`setup` detects languages, initializes config, indexes the repo, and configures MCP integrations (Claude Code, Cursor, etc.).

## Core Commands

### Indexing

```bash
mcp-vector-search index
mcp-vector-search index --force
mcp-vector-search index reindex --all --force
mcp-vector-search index reindex path/to/file.py
```

### Auto-Index Strategies

```bash
mcp-vector-search auto-index setup --method all
mcp-vector-search auto-index status
mcp-vector-search auto-index check --auto-reindex --max-files 10
mcp-vector-search auto-index teardown --method all
```

### Search

```bash
mcp-vector-search search "error handling patterns"
mcp-vector-search search "vector store initialization"
```

### Status + Doctor

```bash
mcp-vector-search status
mcp-vector-search doctor
```

## MCP Integration Pattern

`setup` uses native `claude mcp add` when available, otherwise falls back to `.mcp.json`.

Typical `.mcp.json` entry:

```json
{
  "mcpServers": {
    "mcp-vector-search": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "mcp-vector-search", "mcp"],
      "env": {
        "MCP_ENABLE_FILE_WATCHING": "true"
      }
    }
  }
}
```

## Reindex Triggers

- Dependency updates or parser changes
- Large refactors
- Adding new languages or file extensions
- Tool upgrades (version tracking triggers reindex)

## Local Patterns

- Use `uv` for dev installs: `uv sync --dev`
- Use `setup --force` to rebuild config + index after tool upgrades
- Keep file watching on via `MCP_ENABLE_FILE_WATCHING=true`

## Related Skills

- `toolchains/ai/protocols/mcp`
- `universal/main/mcp-builder`
