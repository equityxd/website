#!/usr/bin/env python3
"""Isolate: does run_generation fail when run in a thread vs main thread?"""
import sys, threading
sys.path.insert(0, "cv_dashboard")
sys.path.insert(0, ".")  # so `generation` package is importable
from generation import engine as gen_engine

def run_in_thread(jd):
    try:
        summary = gen_engine.run_generation(jd, on_progress=lambda m: None)
        return ("ok", summary)
    except Exception as exc:
        return ("err", str(exc))

if __name__ == "__main__":
    jd = sys.argv[1] if len(sys.argv) > 1 else "job_descriptions/CV-20260914-0019.txt"

    # Run in a separate thread (simulates the dashboard worker).
    res = {}
    t = threading.Thread(target=lambda: res.__setitem__("r", run_in_thread(jd)), daemon=True)
    t.start()
    t.join()
    kind, data = res["r"]
    print("RUN-IN-THREAD:", kind)
    if kind == "err":
        print("ERROR:", data)
    else:
        print("SUMMARY keys:", list(data.keys()))
