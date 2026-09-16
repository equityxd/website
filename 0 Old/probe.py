#!/usr/bin/env python3
"""Probe the local LLM proxy to measure latency vs context size."""
import sys, time, json, urllib.request

BASE = "http://127.0.0.1:1250/v1/chat/completions"
MODEL = "ornith-1.5-35b-a3b-apex-mtp-i-mini"

def call(content, max_tokens=4000):
    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    })
    req = urllib.request.Request(
        BASE, data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read().decode("utf-8"))
        dt = time.time() - t0
        content_out = ""
        usage = ""
        if "choices" in data:
            content_out = data["choices"][0]["message"].get("content", "")
            usage = data.get("usage", {})
        return dt, content_out, usage, None
    except Exception as e:
        return time.time() - t0, "", "", str(e)

if __name__ == "__main__":
    sizes = [
        ("small", "Say hello in exactly three words.", 20),
        ("medium-2kb", "You are a recruiter. Write a 200-word cover letter for a "
                       "Chief Growth Officer role at a healthcare startup. "
                       "The candidate has 12 years in finance and loves tennis." * 4, 4000),
        ("large-10kb", "You are a principal tech recruiter. Produce a full "
                       "Match & Gap Analysis plus a tailored CV plus a cover "
                       "letter plus interview prep plus an application dossier. "
                       "Be thorough and detailed.\n\n" + "Context padding to simulate large prompt. " * 120, 4000),
    ]
    for item in sizes:
        name, content, mt = item[0], item[1], item[2]
        dt, out, usage, err = call(content, mt)
        print(f"{name:12s} ctx~{len(content)}b  -> {dt:7.2f}s  out={len(out)}b usage={usage} err={err}")
