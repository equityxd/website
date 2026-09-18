#!/usr/bin/env python3
"""End-to-end test for the web dashboard /api/generate (Option B)."""
import sys, time
sys.path.insert(0, "cv_dashboard")
from fastapi.testclient import TestClient
import app

with TestClient(app.app) as c:
    # health
    r = c.get("/health")
    print("health:", r.status_code, r.json())

    # trigger generation for the Doyen JD
    t0 = time.time()
    resp = c.post("/api/generate", json={"input": "job_descriptions/CV-20260914-0019.txt", "input_type": "text"})
    print("status:", resp.status_code)
    print("elapsed: %.1fs" % (time.time() - t0))
    lines = resp.text.splitlines()
    print("events:", len(lines))
    for ln in lines[-8:]:
        print("  ", ln[:160])
