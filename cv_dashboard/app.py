#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CV Builder — Web Dashboard (FastAPI)
=====================================
A lightweight single-developer frontend to the existing CV Builder pipeline.

It wraps the three stages that turn a Job Description into a full application
package:

    1. Collect        -> collect_cv._run_pipeline   (JD file + manifest + Excel row)
    2. Generate docs  -> generate_documents.py      (cover letter + interview prep)
    3. Render CV      -> build_cv.py                (RenderCV PDF, best-effort)

Live progress is streamed to the browser via Server-Sent Events (SSE).

Run:
    uvicorn app:app --host 0.0.0.0 --port 8000
    # or simply double-click run.bat
"""
import os
import subprocess
import sys
import threading
from pathlib import Path
from queue import Queue

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse

# ---------------------------------------------------------------------------
# Paths / constants
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Import the existing pipeline so we can drive it in-process.
# collect_cv.py lives in the project root (parent of this dashboard folder).
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR.parent))
try:
    import collect_cv
except Exception as exc:  # pragma: no cover - defensive
    raise SystemExit(f"Could not import collect_cv: {exc}")
try:
    import generation.engine as gen_engine
except Exception as exc:  # pragma: no cover - defensive
    raise SystemExit(f"Could not import generation.engine: {exc}")


app = FastAPI(title="CV Builder Dashboard")


# ---------------------------------------------------------------------------
# Input resolution
# ---------------------------------------------------------------------------
def fetch_input_text(input_value, input_type):
    """Resolve the raw input (pasted text or a URL) into plain JD text."""
    input_value = (input_value or "").strip()
    if not input_value:
        raise ValueError("Input is empty — please paste a Job Description or URL.")
    if input_type == "url":
        return collect_cv.fetch_url_text(input_value)
    return input_value


# ---------------------------------------------------------------------------
# Subprocess streaming helper
# ---------------------------------------------------------------------------
def _run_and_step(script, extra_args, label_map):
    """Run a pipeline script and yield clean, per-document completion steps.

    `label_map` is a list of `(needle, label)` pairs. For each non-empty stdout
    line, the first `needle` that appears in the line yields a checked step
    `"✓ {label} → {path}"`; otherwise the line is passed through as plain info.
    A `label` of `None` means "pass the line through as-is". Raises RuntimeError
    on a non-zero exit code so a failed step fails the whole run.
    """
    proc = subprocess.Popen(
        [sys.executable, str(BASE_DIR.parent / script), *extra_args],
        cwd=str(BASE_DIR.parent),  # scripts use relative paths (e.g. "1 Source/…")
        # The pipeline scripts emit emoji/UTF-8 text; decode the captured pipe as
        # UTF-8 rather than the locale's cp1252 so characters like 📍 don't raise
        # 'charmap' codec can't decode byte 0x8d.
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", bufsize=1,
    )
    assert proc.stdout is not None
    for raw in proc.stdout:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped:
            continue
        for needle, label in label_map:
            if needle is not None and needle in stripped:
                parts = stripped.split(None, 1)
                path = parts[1].strip() if len(parts) > 1 else stripped
                if label is None:
                    yield stripped
                else:
                    yield f"✓ {label} → {path}"
                break
        else:
            yield stripped  # informational line (headers, typst commands, etc.)
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"{os.path.basename(script)} failed (exit code {proc.returncode})")



# ---------------------------------------------------------------------------
# API: index
# ---------------------------------------------------------------------------
import hashlib


def _hash(path: str) -> str:
    """Return a short content hash for a static asset, used for cache-busting."""
    try:
        return hashlib.sha256(open(path, encoding="utf-8").read().encode("utf-8")).hexdigest()[:16]
    except OSError:
        return ""


@app.get("/", response_model=None)
async def index():
    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    # Force fresh JS/CSS on every load so stale cached assets can't cause a
    # "still checking" / dead UI after code changes.
    html = html.replace(
        'href="style.css"',
        f'href="style.css?v={_hash("static/style.css")}"',
    )
    html = html.replace(
        '<script src="app.js"></script>',
        f'<script src="app.js?v={_hash("static/app.js")}"></script>',
    )
    return HTMLResponse(html)


# ---------------------------------------------------------------------------
# API: generate
# ---------------------------------------------------------------------------
@app.post("/api/generate")
async def generate(request: Request):
    body = await request.json()
    input_value = body.get("input", "")
    input_type = body.get("input_type", "text")

    q: Queue = Queue()

    def worker():
        try:
            q.put(("progress", "Starting document generation…"))
            jtext = fetch_input_text(input_value, input_type)
            if len(jtext) < 20:
                raise ValueError("Job description too short — please paste the full text.")

            # Stage 1 — collection (in-process).
            q.put(("progress", "Collecting JD, manifest & Excel row…"))
            coll = collect_cv._run_pipeline(
                jtext,
                source_type=("URL" if input_type == "url" else "Job Description (text)"),
                source_value=input_value if input_type == "url" else "(pasted text)",
                on_progress=lambda m: q.put(("progress", f"Collect: {m}")),
            )
            serial = coll.get("serial", "unknown")
            q.put(("progress", f"✓ Collected → serial {serial}"))

            # Stage 2 — LLM-driven full-document generation (Option B).
            # Drives pi to produce the complete application package (Match & Gap
            # Analysis, tailored CV, cover letters, interview prep, dossier) from
            # the collected JD + base CV + manifest, then updates the tracker.
            q.put(("progress", "LLM generating documents (Phase 1-3)…"))
            gen_engine.run_generation(
                str(coll["jd_path"]),
                on_progress=lambda m: q.put(("progress", f"{m}")),
                company=coll.get("company", ""),
                position=coll.get("title", ""),
            )
            q.put(("progress", f"✓ All documents generated for serial {serial}."))
            q.put(("done", None))
        except Exception as exc:
            q.put(("error", str(exc)))
            q.put(("done", None))

    threading.Thread(target=worker, daemon=True).start()

    async def eventstream():
        while True:
            kind, payload = q.get()
            if kind == "done":
                yield "data: done\n\n"
                break
            if kind == "error":
                yield f"data: error\n\ndata: {payload}\n\n"
            else:
                yield f"data: progress\n\ndata: {payload}\n\n"

    return StreamingResponse(eventstream(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# API: static assets (app.js / style.css referenced at root in index.html)
# ---------------------------------------------------------------------------
@app.get("/app.js")
async def serve_app_js():
    return FileResponse(STATIC_DIR / "app.js")


@app.get("/style.css")
async def serve_style_css():
    return FileResponse(STATIC_DIR / "style.css")


# ---------------------------------------------------------------------------
# API: download (path-traversal safe)
# ---------------------------------------------------------------------------
@app.get("/download")
async def download(path: str):
    abs_path = os.path.abspath(path)
    base = os.path.abspath(str(BASE_DIR.parent))
    # Path-traversal guard: only serve files under the project root.
    if abs_path != base and not abs_path.startswith(base + os.sep):
        return HTMLResponse("<p>Access denied.</p>", status_code=403)
    # Return a clean 404 for missing files instead of a raw 500.
    if not os.path.isfile(abs_path):
        return HTMLResponse("<p>File not found.</p>", status_code=404)
    return FileResponse(abs_path)


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
@app.get("/health", response_model=None)
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("DASHBOARD_HOST", "127.0.0.1")
    port = int(os.environ.get("DASHBOARD_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
