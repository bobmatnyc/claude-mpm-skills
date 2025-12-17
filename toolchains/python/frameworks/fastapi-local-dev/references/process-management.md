# Process Management (systemd vs PM2)

## systemd (recommended on Linux)

```ini
[Unit]
Description=FastAPI Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/fastapi-app
Environment="PATH=/opt/fastapi-app/venv/bin"
ExecStart=/opt/fastapi-app/venv/bin/gunicorn -c /opt/fastapi-app/gunicorn_conf.py app.main:app
Restart=always
RestartSec=10
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Useful commands:

```bash
sudo systemctl enable --now fastapi
sudo systemctl status fastapi
sudo journalctl -u fastapi -f
```

## PM2 (only if required)

Do not use PM2 watch mode for Python.

```js
module.exports = {
  apps: [
    {
      name: "fastapi-app",
      script: "/opt/fastapi-app/venv/bin/gunicorn",
      args: "-c gunicorn_conf.py app.main:app",
      cwd: "/opt/fastapi-app",
      exec_mode: "fork",
      instances: 1,
      autorestart: true,
      watch: false
    }
  ],
};
```

