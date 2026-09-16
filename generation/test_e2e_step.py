#!/usr/bin/env python3
"""End-to-end test of run_generation (step-by-step, small prompts)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from generation import engine

jd_path = "2 Job description/CV-20260914-0019.txt"

def on_progress(m):
    print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)

t0 = time.time()
try:
    summary = engine.run_generation(jd_path, on_progress=on_progress)
    print("\n=== SUMMARY ===")
    import json
    print(json.dumps(summary, indent=2))
    print(f"\nELAPSED {time.time()-t0:.1f}s")
except Exception as exc:
    print(f"\n[ERROR] {type(exc).__name__}: {exc}")
    import traceback; traceback.print_exc()
