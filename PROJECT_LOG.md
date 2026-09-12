# Project Log — Ernest SONG · CV Builder

> Central log for the CV tracking project. Acts as the project manager's record.

---

## 1. Project overview

**Goal:** Give Ernest a repeatable, beginner-friendly workflow to turn any job
description into a set of tailored, 100 %-truthful application documents — a
match & gap analysis, 3 custom CVs, 5 cover letters and 6 interview-prep STAR
answers — while keeping the visual format of the base CV (`SONG Ernest - CV v1`).

**Who does what:**
- **Ernest** provides the job description (paste text or URL) and approves documents.
- **The LLM (me / pi)** acts as principal tech recruiter + executive resume
 strategist + project manager, generating the documents and updating logs.
- **The script** (`collect_cv.py`) handles data collection, file organization
  and the Excel session log — no coding required from Ernest.

---

## 2. Folder structure

| Folder | Purpose |
|--------|---------|
| `0 Old` | Archive of superseded work (never deleted, only moved here) |
| `1 Source` | Base source files — `es` (initial) and `v1` (current base version) |
| `2 Job description` | Saved JD text files, one `<serial>.txt` per session |
| `3 Custom CV` | Generated tailored CVs (3 per session) |
| `4 Application monitoring` | Excel tracking workbook + LLM prompt manifests |
| `5 Custom Cover Letter` | Generated cover letters (5 per session) |
| `6 Interview prep` | Generated interview-prep STAR answers (6 per session) |

---

## 3. The process (one session)

```
Double-click run_cv_builder.bat
        │
        ▼
 [GUI] Enter company / position / recruiter + paste JD or URL
        │
        ▼
 collect_cv.py  →  save "2 Job description/<serial>.txt"
                  →  append row to Excel tracker
                  →  write LLM manifest
        │
        ▼
 pi (LLM) reads the manifest + base CV + JD
        │
        ▼
 Generate: Match & Gap Analysis · 3× CV · 5× Cover Letter · 6× Interview Prep
        │
        ▼
 Update Excel "Documents Generated" + "Status" for that serial
```

**Serial number format:** `CV-YYYYMMDD-NNNN` (date-based + running counter).

---

## 4. Tooling

| File | Role |
|------|------|
| `collect_cv.py` | Data collection engine (GUI + URL fetch + Excel + manifest) |
| `run_cv_builder.bat` | Double-click launcher — runs the collector then opens pi |
| `4 Application monitoring/Application_Tracker.xlsx` | Per-session serial log |

---

## 5. Changelog

| Date | Change |
|------|--------|
| 2025-09-12 | Project kickoff. Reorganized `MyCV` into numbered tracking folders. |
| 2025-09-12 | Added `collect_cv.py` — data collection engine (GUI, URL fetch, Excel, manifest). |
| 2025-09-12 | Added `run_cv_builder.bat` launcher. |
| 2025-09-12 | Added `Application_Tracker.xlsx` per-session log.
| 2025-09-12 | Overlined the JD paste limit: added "Load .txt file" option (bypasses clipboard), tall scrollable text box. |

---

## 6. Open items / decisions

- [ ] Confirm base version is `1 Source/SONG Ernest - CV v1.typ` (v1 is the base).
- [ ] After each generation run, mark the Excel row `Status = Complete`.
- [ ] Review document output for truthfulness before Ernest submits.
