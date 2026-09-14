# -*- coding: utf-8 -*-
"""
CV Builder — connectivity checker.

Reports whether a server is listening on port 8000 and whether it can be
reached over HTTP. Run:  python check_server.py
"""
import sys, io, subprocess, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def netstat_listeners():
    out = subprocess.run(
        ["netstat", "-ano", "-p", "TCP"],
        capture_output=True, text=True, timeout=10
    ).stdout
    return out


def main():
    print("=== 1. Is anything LISTENING on port 8000? ===")
    listeners = [l for l in netstat_listeners().splitlines() if ":8000" in l and "LISTENING" in l]
    if listeners:
        print("  YES:")
        for l in listeners:
            print("   ", l.strip())
    else:
        print("  NO — no server is listening. Run run.bat to start it.")

    print("\n=== 2. Can we reach http://127.0.0.1:8000/health? ===")
    try:
        r = urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=6)
        print(f"  OK -> {r.status}: {r.read().decode().strip()!r}")
    except Exception as e:
        print(f"  FAILED -> {type(e).__name__}: {e}")
        print("  => Browser cannot reach the server (firewall/antivirus/port issue).")

    print("\n=== 3. Can we reach http://localhost:8000/health? ===")
    try:
        r = urllib.request.urlopen("http://localhost:8000/health", timeout=6)
        print(f"  OK -> {r.status}: {r.read().decode().strip()!r}")
    except Exception as e:
        print(f"  FAILED -> {type(e).__name__}: {e}")

    print("\n=== 4. uvicorn python processes ===")
    procs = subprocess.run(
        ["cmd", "/c", "tasklist"], capture_output=True, text=True, timeout=10
    ).stdout
    uv = [l for l in procs.splitlines() if "uvicorn" in l or "app:app" in l]
    if uv:
        for l in uv:
            print("   ", l.strip())
    else:
        print("  NO uvicorn process found — server is not running.")


if __name__ == "__main__":
    main()
