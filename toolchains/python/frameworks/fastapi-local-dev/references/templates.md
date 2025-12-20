# Templates

## requirements.txt (example)

```txt
fastapi
uvicorn[standard]
gunicorn
httpx
```

## Minimal app

```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

## gunicorn_conf.py (example)

```py
import multiprocessing

bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
graceful_timeout = 30
keepalive = 5
```

