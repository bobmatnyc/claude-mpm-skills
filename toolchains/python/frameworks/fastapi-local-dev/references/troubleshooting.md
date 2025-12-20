# Troubleshooting Runbook

## Port already in use

```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

## Reload not working

Checklist:
- Confirm `--reload` is set.
- Watch the correct directory (`--reload-dir ./app`).
- On WSL/mounted volumes, set `WATCHFILES_FORCE_POLLING=true`.

```bash
WATCHFILES_FORCE_POLLING=true uvicorn app.main:app --reload
```

## Import errors after reload

Signals:
- `ModuleNotFoundError: No module named 'app'`
- `ImportError: attempted relative import with no known parent package`

Fixes:

```bash
python -m uvicorn app.main:app --reload
PYTHONPATH=. uvicorn app.main:app --reload
```

Confirm the package structure includes `__init__.py`:

```bash
test -f app/__init__.py && echo "ok"
```

## PM2 restart loops

Cause: `watch: true` (breaks Python module resolution).

Fix: disable watch or use systemd.

## Worker timeouts

If requests are slow or blocking:
- increase `timeout` only if needed
- move long work to background tasks
- avoid blocking I/O in async endpoints

