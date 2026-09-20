import importlib.util, os, re
spec = importlib.util.spec_from_file_location("engine", "generation/engine.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

serial = "CV-20260919-0012"
jd_path = "job_descriptions/CV-20260919-0012.txt"

# Replicate run_generation's lcmm_folder computation (from the manifest).
manifest = open("application_monitoring\\manifests\\CV-20260919-0012.txt", encoding="utf-8").read()
m = re.search(r"^- Company\s*:\s*(.+)", manifest, re.M)
m2 = re.search(r"^- Target Role\s*:\s*(.+)", manifest, re.M)
lcmm_company = m.group(1).strip() if m else ""
lcmm_target_role = m2.group(1).strip() if m2 else ""
lcmm_folder = engine._infer_app_folder(serial, lcmm_company, lcmm_target_role)
app_folder = _app_folder = "Job Applications\\20260919 - Manages_Large - Lead_BI___Analytics_Consultant"

cv_path = engine._generate_cv_deterministic(
    serial, jd_path, str(lcmm_folder), app_folder, on_progress=lambda m: (print("[LOG]", m), None)[1]
)
print("cv_path:", cv_path)
print("exists:", os.path.exists(cv_path) if cv_path else None)
if cv_path:
    exists = os.path.exists(cv_path)
    print("exists:", exists)
    if exists:
        print("size:", os.path.getsize(cv_path), "bytes")
    print("SUCCESS")
else:
    print("FAILED (returned None)")
