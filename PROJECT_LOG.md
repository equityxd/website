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

## RenderCV + JD-tailoring pipeline (YAML-based, replaces `.typ` generator)

Pivoted from the Typst `.typ` template to a **RenderCV YAML** data model, plus a
JD-driven tailoring script. Benefits: single source of truth (YAML), deterministic
render, no contact-box spacing bugs, no `.typ` authoring.

- `tailor_cv.py`: reads base `cv.yaml` + a JD, then:
  - rewrites the **Profile summary** to echo the JD's core keywords (truthfully),
  - **reorders Experience** so JD-relevant roles rise to the top (by keyword-overlap score),
  - refreshes **Competencies** with matched skill labels.
  Deterministic + idempotent. Emits `3 Custom CV/CV-<serial>_CV1.yaml`.
- `build_cv.py`: RenderCV → PDF + PNG. Accepts `--yaml <path>`; the standard output
  PDF name (`CV-<serial>_CV1.pdf`) is derived from the input YAML basename.
- `run_cv_builder.bat`: launcher now runs **tailor_cv.py → build_cv.py** (full JD-tailored
  RenderCV pipeline) instead of the old `gen_cv_typ.py` `.typ` generator.

Verified end-to-end: tailored PDF for JD `CV-20260912-0006` renders (4 pages) and the
Profile summary changes vs base (`..., financial-close and ERP replacement`).

## Confirmed CV metrics (replaced ~estimates with user-provided real data)
- Holcim: master records = 500K; annual rebate volume = €150M; reporting-cycle reduction = 50%.
- All other metrics kept as ~estimates (Engie SEM revenue/stakeholders/project-book; Tractebel portfolio ~€18M + lending book ~€35M; Magnetrap budget/goals/margins; Rexel turnover ~€500M; KPMG audit adj ~35%, PPP portfolio ~€48M, team size ~8, funding ~€9M).
- Verified: file has proper UTF-8 € (0x20ac), 0 replacement chars, 11 ~ tokens remaining.

## 2026-09-16 — Engine refactor: step-by-step generation with small focused prompts

**Problem diagnosed & resolved.** The previous engine used one giant ~30 KB prompt
(single `_build_prompt` + `_invoke_pi`). Testing showed the local LLM hangs forever
on prompts ≥ ~15 KB of context (exit 124 / empty output). The full base CV (~18 KB) +
JD (~3.5 KB) + manifest (~6 KB) ≈ 30 KB exceeded the model's usable context.

**Fix — `generation/engine.py`, committed (`b436e5a`):**
- Split the single mega-prompt into per-deliverable small-prompt pi calls, each kept
  minimal (base CV reduced to ~17 KB meaningful content via `_cv_content`).
- `_run_pi`: one focused pi invocation with SIGTERM/timeout retry + exponential backoff
  (`PI_MAX_LLM_RETRIES`, `PI_LLM_RETRY_BASE_DELAY`).
- `_collect`: canonicalises LLM-written deliverables to the expected `{serial}_{label}.{ext}`.
- `run_generation` orchestrates Match & Gap → CV (self-healing Typst recompile) →
  Cover Letter → Interview Prep → Dossier → compile PDFs → tracker update.
- Removed the clobbering `_write_deliverable`; replaced with `_collect`.

**Verified end-to-end (both paths):**
- Direct `run_generation` on `CV-20260914-0019`: all 5 steps succeed, `_collect`
  renamed the dossier file correctly, PDFs compiled, tracker row updated, elapsed ~467 s.
- Web dashboard `/api/generate` via `TestClient` (new session `CV-20260916-0083`):
  status 200, 134 stream events, all artifacts + manifest + tracker row 84 produced,
  elapsed ~554 s.
- Both confirm the context-threshold hang is gone and deliverables land at canonical
  paths.

## 2026-09-17 — Progress-log line breaks + per-step/total timing + test-phase cleanup

**A. Process-log readability (`cv_dashboard/static/app.js`).**
- `logLine()` previously rendered each progress line as a `<span>` (inline), so
  consecutive log lines collided on one visual line. Switched to a block-level
  `<div>` per entry so every progress message starts on its own line (the
  surrounding `#log` `<pre>` keeps `whitespace-pre` wrapping).

**B. Timing (`generation/engine.py`).**
- Added `t_start = time.monotonic()` before `log`; the `log` wrapper now prefixes
  every progress line with a running clock (`[  12.3s]`), so the pace of
  generation is visible.
- Added `_dur(t0)` returning a per-step duration; each step (1/5 → 5/5) logs
  `⏱ Step N/5 <name> — <dur>`, and the run logs a final `⏱ TOTAL — <dur>`.
- Handled the `▶`/`…` mojibake in the Step-1 header (restored the correct U+25B6
  glyph; timing glyphs use the escaped `\u23f1` form, consistent with the
  existing `\u2713` style).

**C. Test-phase cleanup ("move, don't delete").**
- Moved every generated document out of `2 Job description`, `3 Custom CV`,
  `5 Custom Cover Letter`, `6 Interview prep`, `7 Input Job description`,
  `Temp` and `4 Application monitoring/manifests` into `0 Old`.
  `1 Source` was left untouched.
- Reset `4 Application monitoring/Application_Tracker.xlsx`: kept only the header
  row (was 85 rows → 1). The tracker is testing-phase bookkeeping; fresh
  sessions repopulate it on the next `/api/generate` run.

**Verification:**
- `engine.py` passes `py_compile` + `ast.parse`; `import engine` succeeds.
- `app.js` `logLine` now uses `<div>` (block-level).
- Tracker opens cleanly, 1 row (header), ~5 KB.
- Working folders empty; 467 files archived to `0 Old`.
