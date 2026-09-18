#!/usr/bin/env python
"""Clear stale Python bytecode and verify no 'line' free-variable warning remains."""
import os, sys, importlib, warnings, py_compile

ROOT = os.path.abspath(".")


def find_bytecode():
    bad = []
    for dp, _dn, fnames in os.walk(ROOT):
        if "node_modules" in dp or ".git" in dp:
            continue
        for f in fnames:
            if f.endswith(".pyc"):
                bad.append(os.path.join(dp, f))
        if "__pycache__" in fnames:
            bad.append(os.path.join(dp, "__pycache__"))
    return bad


def clear_all():
    removed = []
    for entry in find_bytecode():
        try:
            if entry.endswith(".pyc"):
                os.remove(entry)
                removed.append(entry)
            elif os.path.isdir(entry):
                import shutil
                shutil.rmtree(entry)
                removed.append(entry)
        except OSError as e:
            print(f"  [warn] could not remove {entry}: {e}")
    return removed


def msg_of(e):
    return str(getattr(e, "msg", None) or str(e))


def verify_no_line_warning():
    hits = []
    for dp, _dn, fnames in os.walk(ROOT):
        if "node_modules" in dp or ".git" in dp:
            continue
        for f in fnames:
            if not f.endswith(".py"):
                continue
            path = os.path.join(dp, f)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("error")
                    with open(path, "rb") as fh:
                        data = fh.read()
                    compile(data, path, "exec")
            except SyntaxError as e:
                msg = msg_of(e)
                if "not associated with a value" in msg or "cannot access local variable" in msg:
                    hits.append(f"{path}:{e.lineno}: {msg}")
    return hits


def verify_imports():
    problems = []
    for mod in ["cv_dashboard.app", "generation.engine", "generate_documents", "collect_cv"]:
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                importlib.import_module(mod)
            for w in caught:
                if "not associated with a value" in str(w.message).lower():
                    problems.append(f"{mod}: {w.message}")
        except Exception as e:
            if "not associated with a value" in str(e).lower():
                problems.append(f"{mod}: {e}")
    return problems


def main():
    removed = clear_all()
    print(f"[1] Removed {len(removed)} stale bytecode entries.")
    hits = verify_no_line_warning()
    print(f"\n[2] Compile-scan: {len(hits)} 'line' free-variable warning(s) in source:")
    for h in hits:
        print(f"    {h}")
    problems = verify_imports()
    print(f"\n[3] Import-scan: {len(problems)} line-warning(s) on import:")
    for p in problems:
        print(f"    {p}")
    ok = not hits and not problems
    print(f"\nRESULT: {'CLEAN ✓' if ok else 'STILL HAS line warning ✗'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
