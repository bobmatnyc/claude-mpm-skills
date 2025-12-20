---
name: fastapi-local-dev
description: FastAPI dev/prod runbook (Uvicorn reload, Gunicorn)
version: 1.1.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "FastAPI dev: Uvicorn reload; prod: Gunicorn+UvicornWorker"
tags: [python, fastapi]
---

# FastAPI Local Dev

- Dev: `uvicorn app.main:app --reload`
- Imports: run from repo root; use `python -m uvicorn ...` or `PYTHONPATH=.`
- WSL: `WATCHFILES_FORCE_POLLING=true` if reload misses changes
- Prod: `gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w <n> --bind :8000`

Anti-patterns:
- `--reload --workers > 1`
- PM2 `watch: true` for Python

References: `references/`.
