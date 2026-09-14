# CV Builder Dashboard

A lightweight single-developer web interface that drives the existing
CV Builder pipeline (JD → CV + cover letter + interview prep + Excel tracker)
from a browser.

## Tech stack

| Layer      | Choice                          | Why                                   |
|------------|---------------------------------|---------------------------------------|
| Backend    | FastAPI + Uvicorn               | Async, minimal deps, great on Pi      |
| Frontend   | Vanilla JS + Tailwind (CDN)     | No build step, responsive             |
| Transport  | HTTP REST + SSE (progress)      | Live logs, simple                     |

## Quick start

```bash
# 1. Install deps
pip install -r cv_dashboard/requirements.txt

# 2. Run (default http://127.0.0.1:8000)
python -m uvicorn cv_dashboard.app:app --host 127.0.0.1 --port 8000

# or just double-click run.bat
```

Open the printed URL, paste a Job Description (or check **Input is a URL** and
paste a link), and click **Generate Documents**. The progress log fills live.

## Project layout

```
cv_dashboard/
├── app.py            # FastAPI backend (SSE progress + download)
├── static/
│   ├── index.html    # Layout + controls
│   ├── app.js        # Frontend logic (SSE reader)
│   └── style.css     # Styles
├── run.bat           # One-click launcher
└── requirements.txt
```

## API

| Method | Path             | Purpose                          |
|--------|------------------|----------------------------------|
| GET    | `/`              | Serve the dashboard              |
| GET    | `/health`        | Liveness probe                  |
| POST   | `/api/generate`  | Start generation (SSE stream)   |
| GET    | `/download?path=` | Serve a generated file (safe)  |

`POST /api/generate` accepts `{"input": "...", "input_type": "text"|"url"}`.

## Deploy on Raspberry Pi (boot service)

1. SSH in and clone/copy this folder to your Pi.
2. Create a virtualenv and install deps:
   ```bash
   cd ~/cv_dashboard
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```
3. Install a systemd service (`/etc/systemd/system/cv-dashboard.service`):
   ```ini
   [Unit]
   Description=CV Builder Dashboard
   After=network.target

   [Service]
   Type=simple
   WorkingDirectory=/home/<user>/cv_dashboard
   Environment="PATH=/home/<user>/cv_dashboard/.venv/bin"
   ExecStart=/home/<user>/cv_dashboard/.venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
4. Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now cv-dashboard.service
   sudo systemctl status cv-dashboard.service
   ```
5. Open from another machine: `http://<pi-ip>:8000` (firewall permitting).

## Notes

- CV rendering (`build_cv.py`) uses RenderCV/Typst binaries and is best-effort —
  a failure there is logged, not fatal.
- `download` is path-traversal guarded: only files under the project parent
  directory are served.
