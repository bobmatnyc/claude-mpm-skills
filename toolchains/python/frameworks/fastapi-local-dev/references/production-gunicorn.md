# Production (Gunicorn + UvicornWorker)

## Baseline command

```bash
gunicorn app.main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --graceful-timeout 30
```

## Worker sizing

Start point: `(2 × CPU cores) + 1`, then load-test and adjust.

Common adjustments:
- Lower workers if the app is memory-heavy.
- Increase timeout for long-running endpoints or move work to background jobs.

## gunicorn_conf.py (minimal)

```py
import multiprocessing

bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
graceful_timeout = 30
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"
```

Run it:

```bash
gunicorn -c gunicorn_conf.py app.main:app
```

## Worker timeouts (common under load)

If you see `WORKER TIMEOUT`, treat it as a symptom:
- Increase `timeout` only if slow requests are expected.
- Remove blocking I/O from `async def` endpoints (use `httpx.AsyncClient`).
- Push long work to background tasks/queues.

