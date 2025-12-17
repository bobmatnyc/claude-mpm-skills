# Dev Server (Uvicorn)

## Recommended command

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Add logging while debugging:

```bash
uvicorn app.main:app --reload --log-level debug --access-log
```

## Import hygiene (most common local-dev failure)

Rules:
- Run from the repo root so imports resolve consistently.
- Treat `app/` as a real package (`app/__init__.py`).

Fix patterns:

```bash
# Run as a module (keeps import semantics consistent)
python -m uvicorn app.main:app --reload

# Or explicitly set PYTHONPATH
PYTHONPATH=. uvicorn app.main:app --reload
```

Minimal expected layout:

```
project/
├── app/
│   ├── __init__.py
│   └── main.py
└── pyproject.toml / requirements.txt
```

## Reload tuning

Reload mode requires a single worker:

```bash
uvicorn app.main:app --reload --workers 1
```

Control watch scope:

```bash
uvicorn app.main:app --reload \
  --reload-dir ./app \
  --reload-exclude ./app/tests \
  --reload-include '*.py'
```

## WSL / network filesystems

If file events are unreliable, force polling:

```bash
WATCHFILES_FORCE_POLLING=true uvicorn app.main:app --reload
```

## Virtual environments

Avoid “works locally but not in scripts” by invoking the venv binary explicitly:

```bash
./venv/bin/uvicorn app.main:app --reload
./venv/bin/python -m uvicorn app.main:app --reload
```

