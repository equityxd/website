# -*- coding: utf-8 -*-
"""
CV Builder — diagnostic harness.

Mimics exactly what the browser does when you click "Generate Documents",
but logs every step to a file so we can see where it goes wrong.

Run:  python diagnose.py

The log is written to  cv_dashboard/diagnose.log
"""
import sys, io, time, json, urllib.request, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

LOG = open("diagnose.log", "w", encoding="utf-8")


def log(msg):
    line = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line)
    LOG.write(line + "\n")
    LOG.flush()


def step(label):
    log(f"--- {label} ---")


# 1. Server reachability
step("STEP 1: check /health")
try:
    r = urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=6)
    log(f"/health -> {r.status}: {r.read().decode().strip()!r}")
except Exception as e:
    log(f"/health FAILED: {type(e).__name__}: {e}")
    log("SERVER NOT REACHABLE — stop run.bat and re-run it, then retry.")
    LOG.close()
    sys.exit(1)

# 2. Fetch the page and show what assets it references
step("STEP 2: fetch dashboard page (/) and inspect asset URLs")
try:
    html = urllib.request.urlopen("http://127.0.0.1:8000/", timeout=6).read().decode("utf-8")
    log(f"page status: 200, size={len(html)} bytes")
    import re
    refs = re.findall(r'(?:src|href)="([^"]+)"', html)
    for m in refs:
        log(f"  asset ref: {m}")
except Exception as e:
    log(f"page fetch FAILED: {type(e).__name__}: {e}")
    LOG.close()
    sys.exit(1)

# 3. POST to /api/generate exactly like runGeneration does
step("STEP 3: POST /api/generate (input_type=url)")
url = "https://www.linkedin.com/pulse/lead-bi-analytics-consultant-brussels-hybrid-freelance-jeremie-meba-gsqme/"
payload = json.dumps({"input": url, "input_type": "url"}).encode("utf-8")
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/generate",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)
t0 = time.time()
try:
    res = urllib.request.urlopen(req, timeout=90)
except Exception as e:
    log(f"POST FAILED immediately: {type(e).__name__}: {e}")
    LOG.close()
    sys.exit(1)
log(f"POST response status: {res.status} (took {time.time()-t0:.1f}s)")

# 4. Read the SSE stream exactly like readLoop does
step("STEP 4: read SSE stream")
raw = res.read()
text = raw.decode("utf-8", errors="replace")
lines = text.split("\n")
pending_type = None
for raw_line in lines[:-1]:
    line = raw_line.strip()
    if line == "":
        pending_type = None
        continue
    if line.startswith("data: "):
        payload = line[6:]
        if pending_type is None:
            pending_type = payload
        else:
            tag = {"error": "ERROR", "done": "DONE"}.get(pending_type, "INFO")
            log(f"  [{tag}] {payload}")
            pending_type = None
log(f"stream finished. total bytes={len(raw)}, total lines={len(lines)}")

step("STEP 5: summary")
log("If you see DONE and INFO lines, the backend is WORKING — the problem is the browser (stale cache).")
log("Do a HARD REFRESH (Ctrl+Shift+R) and try again.")
log("DIAGNOSIS COMPLETE")
LOG.close()
