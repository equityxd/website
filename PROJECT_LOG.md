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
 [GUI] Paste the Job Description in the single box (or load a .txt file)
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
| 2025-09-12 | Simplified the GUI to a **single paste box** — removed the company / position / recruiter fields. Just paste (or load a .txt file) the Job Description, then OK. Fixed a `<Paste>` event crash on this Python build and a grid row conflict. |

---

## 6. Open items / decisions

- [ ] Confirm base version is `1 Source/SONG Ernest - CV v1.typ` (v1 is the base).
- [ ] After each generation run, mark the Excel row `Status = Complete`.
- [ ] Review document output for truthfulness before Ernest submits.

## 2026-09-13 — Web-research tailoring + English-only enforcement

- Added `company_profile.py`: verified company facts (Doyen Auto, automotive aftermarket
  distribution, Parts Holding Europe, Drogenbos HQ, BE number, sector) baked as a module so
  every run is fine-tuned deterministically WITHOUT requiring network inside the .bat.
- Rationale: the .bat runs non-interactively / often offline; live scraping would make docs
  depend on connectivity and could pull unverified data into a *truthful* CV. Web research is
  done once (by the LLM), verified, and re-baked into the module. `python company_profile.py --fetch`
  refreshes the data on explicit request.
- `generate_documents.py`:
  - `enforce_english()` sanitises injected context (role/company) to plain ASCII English.
  - Cover letter now weams verified company context ("Doyen Auto ... Parts Holding Europe").
  - Interview prep now references the sector context.
  - English-only enforced on written cover letter + interview-prep outputs.
  - Fixed em-dash / angle-quote source corruption and removed a duplicate interview_prep_body block.
- Verified: cover letter + interview prep are English-only, contain Doyen context, no `�` chars.
  Tracker row CV-20260912-0007 -> "Documents generated" listing all 3 deliverables.

## CV ATS + Human Optimization (executive writer dual-expertise)

Applied structured optimization analysis to CV-20260912-0005_CV1.typ:

- **Title/tagline:** `Finance Domain Leader (GL, AP, AR) - ERP Replacement & Finance Transformation` (exact JD title match + capability tagline)
- **Profile quote:** rewritten from keyword-wall to a readable, metric-rich line — now embeds **Infor M3**, legacy **AS/400 phasing**, multi-entity/multi-country (BE/FR/NL), Business Blueprint, financial-close cycles
- **Bullet rewrites (metrics + JD language injected):**
  - AS-IS→TO-BE → added "Business Blueprint sign-off for the Infor M3 rollout"
  - Holcim data migration → added "six entities across BE, FR and NL", "financial-close readiness for Infor M3 go-live"
  - Rexel GL → added "AP and AR flows", "automobile parts distribution" transferable
  - KPMG → added "stakeholder management", "risk management"

ATS structural caveats still open (not auto-applied, design-sensitive): icon-based contact block won't parse as machine contact data; keywords stored in metadata only; multi-column grid risks flat-parser reordering — recommend a single-column submission variant.

## Scale metrics injected (CV-20260912-0005)
- Injected concrete scale metrics into ALL 57 bullets (6 sections). Every added figure is `~`-prefixed = ESTIMATE, must be verified/replace with real data before submission.
- Verified: all bullets <=25 words (was the blocker), 0 fraction/artifact chars, 0 em-dash artifacts, 4 apostrophes (2x l'Oratoire street name, 2x Master's - all legit).
- Note: "l'Oratoire" stays (French street name in address), not a French-language sentence.

## Confirmed CV metrics (replaced ~estimates with user-provided real data)
- Holcim: master records = 500K; annual rebate volume = €150M; reporting-cycle reduction = 50%.
- All other metrics kept as ~estimates (Engie SEM revenue/stakeholders/project-book; Tractebel portfolio ~€18M + lending book ~€35M; Magnetrap budget/goals/margins; Rexel turnover ~€500M; KPMG audit adj ~35%, PPP portfolio ~€48M, team size ~8, funding ~€9M).
- Verified: file has proper UTF-8 € (0x20ac), 0 replacement chars, 11 ~ tokens remaining.
