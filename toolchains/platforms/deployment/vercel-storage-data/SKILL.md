---
name: vercel-storage-data
description: Vercel data and storage services including Postgres, Redis, Vercel Blob, Edge Config, and data cache. Use when selecting data storage or caching on Vercel.
progressive_disclosure:
  entry_point:
    summary: "Vercel data and storage services including Postgres, Redis, Vercel Blob, Edge Config, and data cache. Use when selecting data storage or caching on Vercel."
    when_to_use: "When working with data, databases, or data transformations."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Vercel Storage and Data Skill

---
progressive_disclosure:
  entry_point:
    summary: "Vercel data and storage: Postgres, Redis, Vercel Blob, Edge Config, and data cache." 
    when_to_use:
      - "When selecting a data store or cache"
      - "When using managed Postgres or Redis"
      - "When storing files with Vercel Blob"
    quick_start:
      - "Choose Postgres, Redis, or Blob"
      - "Configure Edge Config or data cache"
      - "Connect from Functions or apps"
      - "Monitor usage"
  token_estimate:
    entry: 90-110
    full: 3800-4800
---

## Overview

Vercel provides managed data services and storage for application state, cache, and files.

## Postgres

- Provision Postgres for relational data.
- Manage credentials and connection strings.

## Redis

- Use Redis for caching and ephemeral state.
- Configure access for Functions and Edge workloads.

## Vercel Blob

- Store and serve files with Vercel Blob.
- Use Blob for uploads, assets, and media storage.

## Edge Config

- Use Edge Config for low-latency configuration and feature data.
- Read from Edge Runtime workloads.

## Data Cache and Storage

- Use data cache features for response caching.
- Review storage options for app data.

## Complementary Skills

When using this skill, consider these related skills (if deployed):

- **vercel-functions-runtime**: Functions and Edge access to data.
- **vercel-networking-domains**: Edge caching and routing.
- **vercel-observability**: Usage and performance monitoring.

*Note: Complementary skills are optional. This skill is fully functional without them.*

## Resources

**Vercel Docs**:
- Postgres: https://vercel.com/docs/postgres
- Redis: https://vercel.com/docs/redis
- Vercel Blob: https://vercel.com/docs/vercel-blob
- Edge Config: https://vercel.com/docs/edge-config
- Data Cache: https://vercel.com/docs/data-cache
- Storage: https://vercel.com/docs/storage
