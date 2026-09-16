#!/usr/bin/env python3
"""Sanity test: context reduction + a couple of real LLM steps (fast)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import engine

base_cv = engine.BASE_CV.read_text(encoding="utf-8")
cv_ctx = engine._cv_content(base_cv)
print(f"full base_cv = {len(base_cv)} bytes; reduced cv_ctx = {len(cv_ctx)} chars")

# Manifest + JD
serial = "CV-20260914-0019"
manifest = engine._read_manifest(serial)
jd_path = str(engine.JOB_DIR / "CV-20260914-0019.txt")
jd_text = open(jd_path, encoding="utf-8").read()
facts = engine._candidate_facts(manifest)
if "content" not in facts:
    facts["content"] = cv_ctx

t0 = time.time()
print("\n--- Step: Match & Gap ---")
out = engine._run_pi(engine._match_gap_prompt(jd_text, cv_ctx), lambda m: print("  " + m, flush=True), timeout=300)
print(f"[{time.time()-t0:.1f}s] match_gap output chars = {len(out)}")

print("\n--- Step: CV .typ ---")
out = engine._run_pi(engine._cv_prompt(jd_text, cv_ctx), lambda m: print("  " + m, flush=True), timeout=300)
engine.CV_DIR.mkdir(exist_ok=True)
(engine.CV_DIR / f"{serial}_CV1.typ").write_text(out.strip(), encoding="utf-8")
print(f"[{time.time()-t0:.1f}s] CV .typ chars = {len(out)}")

print("\nALL STEPS OK")
