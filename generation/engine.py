#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

CV Builder — LLM-Driven Generation Engine (Option B)

=====================================================

Given a collected session (base CV + JD + manifest), drive an LLM (pi) to

produce the full application package described by the manifest:



    1. Match & Gap Analysis   -> 2 Job description/

    2. Tailored CV (.typ)     -> 3 Custom CV/<serial>_CV1.typ   (+ compiled .pdf)

    3. Tailored Cover Letter  -> 5 Custom Cover Letter/<serial>_CL1.docx

    4. Interview Prep (STAR)  -> 6 Interview Prep/<serial>_IP1.docx

    5. Application Dossier    -> 7 Input Job description/

    6. Tracker + status update -> 4 Application monitoring/Application_Tracker.xlsx



DESIGN PRINCIPLE — small, focused prompts

-------------------------------------------

The remote LLM (via the local proxy) hangs on large prompts (>~15 KB of context).

To stay reliable and fast, every deliverable is generated in its **own** small

pi invocation with a *minimal, context-extracted* prompt rather than one giant

30 KB mega-prompt. This "step by step" approach:



  * keeps each LLM call well under the context threshold (no hangs / timeouts),

  * isolates failures so one bad step doesn't waste the whole run,

  * lets progress stream to the dashboard in real time.



The content method is the same 3-phase intelligence defined in the project:



    PHASE 1  Recruiter audit & ATS strategy     (top-20 JD keywords, frequency maps,

                                                 terminology swaps, ATS format flags,

                                                 human-scan score)

    PHASE 2  Per-bullet deep rewrite             (Action-Verb + Context + Metric,

                                                 18-25 words, verb variety, correct tense)

    PHASE 3  Final CV generation                (summary + competencies + experience,

                                                 ATS-ready, strictly truthful)



This module is the *plumbing + method*. The LLM makes the creative/content calls.



Usage:

    python generation/engine.py "<path/to/JD.txt>"        # LLM-generate for one JD

    python generation/engine.py                              # newest JD in 2 Job description



Progress is printed to stdout so the web dashboard can stream it.

"""

import os

import re

import sys

import json

import time

import subprocess

from pathlib import Path



try:

    import openpyxl

except Exception:  # pragma: no cover - optional dependency

    openpyxl = None



# Ensure checkmarks / unicode log lines can be written on Windows consoles.

try:

    sys.stdout.reconfigure(encoding="utf-8")

    sys.stderr.reconfigure(encoding="utf-8")

except (AttributeError, ValueError):

    pass



# ---------------------------------------------------------------------------

# Paths

# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent          # .../MyCV

CV_DIR = BASE_DIR / "3 Custom CV"

COVER_DIR = BASE_DIR / "5 Custom Cover Letter"

INTERVIEW_DIR = BASE_DIR / "6 Interview Prep"

DOSSIER_DIR = BASE_DIR / "7 Input Job description"

MANIFEST_DIR = BASE_DIR / "4 Application monitoring" / "manifests"

WORKBOOK = BASE_DIR / "4 Application monitoring" / "Application_Tracker.xlsx"

BASE_CV = BASE_DIR / "1 Source" / "SONG Ernest - CV v1.typ"

JOB_DIR = BASE_DIR / "2 Job description"



# ---------------------------------------------------------------------------

# LLM invocation configuration

# ---------------------------------------------------------------------------



# Model used for generation unless overridden by env. Matches the session model.

DEFAULT_MODEL = os.environ.get("PI_GENERATION_MODEL", "ornith-1.5-35b-a3b-apex-mtp-i-mini")



# Each per-step LLM call gets a bounded wall-clock budget. Override with env.

PI_STEP_TIMEOUT = int(os.environ.get("PI_STEP_TIMEOUT", "900"))



# Transient SIGTERM (exit code 143) / timeout: retry a few times with backoff.

_MAX_LLM_RETRIES = int(os.environ.get("PI_MAX_LLM_RETRIES", "5"))

_LLM_RETRY_BASE_DELAY = float(os.environ.get("PI_LLM_RETRY_BASE_DELAY", "20"))



# ---------------------------------------------------------------------------
# Hidden debug log
# ---------------------------------------------------------------------------

# A dot-prefixed (hidden) log at the project root that captures diagnostics
# (pi return code, stderr snippets, typst compile errors, per-step timing,
# renames) so reproducibility issues such as "unclosed delimiter" can be
# investigated later and the process improved.
DEBUG_LOG = BASE_DIR / ".generation_debug.log"


def _debug(msg=""):
    """Append a timestamped entry to the hidden debug log (best-effort)."""
    try:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        with open(DEBUG_LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        # Never let debug logging break the generation flow.
        pass

    return line





def _pi_executable():

    """Return the path to the pi CLI, or None if it cannot be found."""

    candidates = []

    npm_root = os.environ.get("APPDATA", os.path.expanduser("~/.npm"))

    candidates.append(os.path.join(os.environ.get("APPDATA", ""), "npm", "pi"))

    candidates.append(os.path.join(os.environ.get("LOCALAPPDATA", ""), "npm", "pi"))

    for dir_ in os.environ.get("PATH", "").split(os.pathsep):

        candidates.append(os.path.join(dir_, "pi"))

        candidates.append(os.path.join(dir_, "pi.exe"))

    for c in candidates:

        if os.path.isfile(c):

            return c

    return None





# ---------------------------------------------------------------------------

# Context summarisation — keep prompts small to avoid LLM hangs

# ---------------------------------------------------------------------------





def _read_manifest(serial):

    """Return the manifest text for a serial, or '' if none exists."""

    safe = re.sub(r"[^\w\-.]", "_", serial)

    path = MANIFEST_DIR / f"{safe}.txt"

    if path.exists():

        return path.read_text(encoding="utf-8")

    return ""





def _cv_content(base_cv):

    """Extract only the *meaningful* content from the base CV, stripping the

    Typst styling/layout boilerplate. The raw .typ is ~18 KB but most of it is

    font/layout definitions the LLM does not need. Returning ~6-8 KB of actual

    candidate content keeps each generation prompt well under the context limit.



    Returns the profile block + Education + Competencies + Professional Experience.

    """

    if not base_cv:

        return ""



    out = []



    # 1) Profile block: from `profile: (` through the closing `),` after position.

    pm = re.search(r"profile: \(", base_cv)

    posm = re.search(r"position:\s*\"[^\"]*\"", base_cv)

    if pm and posm:

        # Find the closing `),` that ends the profile dict (first occurrence after position)

        tail = base_cv[posm.end():]

        close = tail.find("),")

        end = posm.end() + close + len("),")

        out.append("BASE CV PROFILE:\n" + base_cv[pm.start():end].strip())



    # 2) Education block (from `// ── Education ──` to the competencies marker)

    edu_m = re.search(r"// ── Education ──", base_cv)

    comp_m = re.search(r"// ── Competencies ──", base_cv)

    if edu_m and comp_m:

        out.append("EDUCATION:\n" + base_cv[edu_m.start():comp_m.start()].strip())



    # 3) Competencies block

    comp2_m = re.search(r"// ── Competencies ──", base_cv)

    lang_m = re.search(r"// ── Languages ──", base_cv)

    if comp2_m and lang_m:

        out.append("COMPETENCIES + LANGUAGES:\n" + base_cv[comp2_m.start():lang_m.start()].strip())



    # 4) Professional Experience (the bulk of what needs rewriting) — to EOF

    pe_m = re.search(r"= Professional Experience", base_cv)

    if pe_m:

        out.append("PROFESSIONAL EXPERIENCE (real, verifiable):\n" + base_cv[pe_m.start():].strip())



    return "\n\n".join(out)





def _candidate_facts(manifest):

    """Extract structured candidate facts from the manifest metadata block."""

    facts = {}

    m = re.search(r"Serial Number\s*:\s*(\S+)", manifest)

    if m:

        facts["serial"] = m.group(1)

    m = re.search(r"Target Role\s*:\s*(.+)", manifest)

    if m:

        facts["target_role"] = m.group(1).strip()

    return facts





# ---------------------------------------------------------------------------

# Focused per-deliverable prompt builders (each kept small)

# ---------------------------------------------------------------------------



def _match_gap_prompt(jd_text, cv_ctx):

    return (

        "You are a principal tech recruiter and executive resume strategist.\n"

        "Given the candidate's real content and the target Job Description, produce a\n"

        "MATCH & GAP ANALYSIS written to a plain-text file.\n\n"

        "STRUCTURE:\n"

        "- DIRECT MATCHES: skills / tools / experience that directly match the JD.\n"

        "- TRANSFERABLE: related experience that fulfills implicit JD requirements.\n"

        "- CRITICAL GAPS: required skills / qualifications missing from the CV.\n\n"

        "Rules: factual only; cite the JD text as evidence; never invent numbers,\n"

        "companies or metrics.\n\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n"

        "==== CANDIDATE CONTENT ====\n" + cv_ctx.strip()

    )





def _cv_prompt(jd_text, cv_ctx):

    return (

        "You are a senior ATS-friendly CV author. Rewrite the candidate's CV content to\n"

        "maximise the match with the target Job Description while STRICTLY adhering to\n"

        "truthfulness. Produce the final Typst source (.typ) for the tailored CV.\n\n"

        "RULES:\n"

        "- Preserve the base CV's visual layout and styling; change only the CONTENT.\n"

        "- Rewrite every Professional Experience bullet as: Action Verb + Context/Tech + Metric/Outcome.\n"

        "- Use exact JD keyword phrasing ONLY where real experience supports it.\n"

        "- Restructure the summary into a high-impact 'Value Proposition' answering the JD's pain point.\n"

        "- Output VALID Typst. Balance every `#text[...]`, `#grid(...)`, `#if {...}` etc.\n"

        "- Never fabricate roles, companies, dates or metrics.\n\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n"

        "==== CANDIDATE CONTENT (rewrite these) ====\n" + cv_ctx.strip()

    )





def _cover_letter_prompt(jd_text, facts):

    return (

        "You are an executive cover-letter writer. Draft ONE concise, high-converting\n"

        "cover letter (under 250 words) that bridges the candidate's real background to\n"

        "the JD's top 3 requirements. Include an honest statement on how his unique\n"

        " perspective covers any minor skill gap, without apologising.\n\n"

        "==== TARGET ROLE ====\n" + facts.get("target_role", "the target position") + "\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n"

        "==== CANDIDATE FACTS ====\n" + facts.get("content", "")

    )





def _interview_prep_prompt(jd_text, facts):

    return (

        "You are a senior interview coach. Produce 6 targeted behavioral interview\n"

        "questions likely to be asked for this role, each with an STAR-method answer\n"

        "(Situation, Task, Action, Result) based STRICTLY on the candidate's real CV\n"

        "experiences. No fabrication.\n\n"

        "==== TARGET ROLE ====\n" + facts.get("target_role", "the target position") + "\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n"

        "==== CANDIDATE FACTS ====\n" + facts.get("content", "")

    )





def _dossier_prompt(jd_text, manifest):

    return (

        "You are an executive recruitment strategist. Compile an Application Dossier\n"

        "for this candidate's application: a concise strategic briefing that summarises\n"

        "the role, the candidate's strongest matching angles, and recommended talking\n"

        "points. Be factual.\n\n"

        "==== MANIFEST (session metadata) ====\n" + manifest.strip() + "\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip()

    )





# ---------------------------------------------------------------------------

# Core LLM step runner

# ---------------------------------------------------------------------------



def _run_pi(prompt_text, on_progress, timeout=None):

    """Run the pi CLI ONCE with a focused (small) prompt, retrying transient

    SIGTERM (exit 143) and timeout failures. Returns (stdout_raw, stderr_raw).



    Raises RuntimeError on repeated failure or explicit non-143 errors.

    """

    timeout = timeout or PI_STEP_TIMEOUT



    def log(msg=""):

        if on_progress:

            on_progress(msg)

        else:

            print(msg, flush=True)



    last_err = None

    for attempt in range(_MAX_LLM_RETRIES):

        if attempt:

            delay = _LLM_RETRY_BASE_DELAY * (2 ** attempt)

            log(f"\u2139 LLM step failed (retry {attempt + 1}/{_MAX_LLM_RETRIES} in {int(delay)}s…)")

            time.sleep(delay)

        try:

            proc = subprocess.Popen(

                # --thinking off disables expensive extended-thinking to speed output.

                f"{_pi_executable()} --no-session --thinking off --model {DEFAULT_MODEL} -p",

                cwd=str(BASE_DIR),

                stdin=subprocess.PIPE,

                stdout=subprocess.PIPE,

                stderr=subprocess.PIPE,

                encoding="utf-8",

                bufsize=1,

                shell=True,

            )

        except Exception as exc:  # spawn failed

            last_err = f"failed to start pi: {exc}"

            continue

        try:

            stdout_raw, stderr_raw = proc.communicate(

                input=prompt_text, timeout=timeout

            )

        except subprocess.TimeoutExpired:

            try:

                proc.kill()

            except OSError:

                pass

            last_err = "LLM step timed out."

            _debug(f"pi-timeout: prompt={len(prompt_text)} chars | killed process")

            continue



        if proc.returncode == 0:

            return stdout_raw, stderr_raw



        if proc.returncode == 143:

            last_err = "pi killed by SIGTERM (exit 143)"

            continue



        detail = (stderr_raw or "").strip()

        last = stdout_raw.strip().splitlines()[-5:] if stdout_raw else []

        # Best-effort: append structured diagnostics to the hidden debug log so
        # reproducibility issues (e.g. "unclosed delimiter") can be traced.
        _debug(
            f"pi-exit {proc.returncode} | prompt={len(prompt_text)} chars "
            f"| stderr={detail!r} | last-output={last!r}"
        )

        try:

            Path("pi_debug.log").write_text(

                f"returncode={proc.returncode}\n[stderr] {detail}\n[last-output] {last}\n",

                encoding="utf-8",

            )

        except Exception:

            pass

        last_err = f"pi failed (exit code {proc.returncode}):\n[stderr] {detail}\n[last-output] {last}"

    raise RuntimeError(f"LLM step failed after {_MAX_LLM_RETRIES} attempts: {last_err}")





def _collect(label, folder, ext, serial, on_progress=None):

    """Canonicalise a deliverable produced by the LLM agent.



    The LLM writes files autonomously and may name them differently from the

    expected ``{serial}_{label}.{ext}``. This ensures the expected path exists:

    if the expected file is already present it is returned as-is; otherwise the

    most recently created file of the same extension (that is not already

    ``{serial}_``-prefixed) is renamed to the expected path.



    Returns the expected path (which may not exist if the LLM produced nothing).

    Progress strings are passed to ``on_progress``.

    """

    def log(msg=""):

        if on_progress:

            on_progress(msg)

        else:

            print(msg, flush=True)



    folder = Path(folder)

    expected = folder / f"{serial}_{label}.{ext}"

    if expected.exists():

        return expected



    if folder.exists():

        fresh = [f for f in folder.glob(f"*.{ext}")

                 if not f.name.startswith(f"{serial}_")]

        if fresh:

            newest = max(fresh, key=lambda f: f.stat().st_mtime)

            if newest != expected:

                try:

                    newest.rename(expected)

                    log(f"\u21aa Renamed {newest.name} -> {expected.name}")

                except OSError as exc:

                    log(f"\u26a0 could not rename {newest.name}: {exc}")

    return expected





# ---------------------------------------------------------------------------

# Helpers: PDF compilation, typst error reporting, tracker update

# ---------------------------------------------------------------------------



def compile_pdf(serial, on_progress=None):

    """Compile the LLM-generated .typ CV(s) to PDF via the python-typst module.



    Returns the list of generated PDF paths (empty if none found).

    """

    def _log(m):

        if on_progress:

            on_progress(m)

        else:

            print(m, flush=True)



    try:

        import typst

    except Exception:

        _log("ℹ python-typst module not available; skipping PDF compilation")

        return []



    typ_files = sorted(CV_DIR.glob(f"{serial}_CV*.typ"))

    if not typ_files:

        _log("ℹ No .typ files found for {serial}; skipping PDF compilation")

        return []



    pdfs = []

    for typ_path in typ_files:

        pdf_path = typ_path.with_suffix(".pdf")

        try:

            typst.compile(str(typ_path), str(pdf_path))

            pdfs.append(str(pdf_path))

            _log(f"\u2713 Compiled {pdf_path.name}")

        except Exception as exc:

            _log(f"\u2717 Failed to compile {typ_path.name}: {exc}")

    return pdfs





def _compile_typ_to_pdf(typ_path, on_progress=None):

    """Compile a single generated .typ file to its sibling .pdf via python-typst.

    Returns the PDF path on success, or None on failure (logged). This lets the
    .pdf artefact be produced immediately whenever a valid .typ lands, rather
    than only at the very end of the run.

    """

    def _log(m):

        if on_progress:

            on_progress(m)

        else:

            print(m, flush=True)


    try:

        import typst

    except Exception as exc:

        _debug(f"python-typst unavailable: {exc}")

        _log("\u26a9 python-typst module not available; skipping PDF compilation")

        return None


    typ_path = str(typ_path)

    pdf_path = str(Path(typ_path).with_suffix(".pdf"))

    try:

        typst.compile(typ_path, pdf_path)

        _debug(f"compiled {Path(typ_path).name} -> {Path(pdf_path).name}")

        _log(f"\u2713 Compiled {Path(typ_path).name} -> {Path(pdf_path).name}")

        return pdf_path

    except Exception as exc:

        _debug(f"typst-compile-fail {Path(typ_path).name}: {exc}")

        _log(f"\u2717 Failed to compile {Path(typ_path).name}: {exc}")

        return None



def _typst_error_report(serial, on_progress=None):

    """Attempt to compile every generated .typ CV and report the ones that fail.



    Returns an ordered dict {filename: error_message} for the malformed files

    (empty if all compile cleanly). Errors are fed back to the LLM so it can

    repair the Typst syntax. Progress strings are passed to `on_progress`.

    """

    def log(msg=""):

        if on_progress:

            on_progress(msg)

        else:

            print(msg, flush=True)



    try:

        import typst

    except Exception:

        log("ℹ python-typst module not available; skipping typst error check")

        return {}



    typ_files = sorted(CV_DIR.glob(f"{serial}_CV*.typ"))

    if not typ_files:

        return {}



    errors = {}

    for typ_path in typ_files:

        try:

            typst.compile(str(typ_path), str(typ_path.with_suffix(".tmp_pdf")))

        except Exception as exc:

            errors[typ_path.name] = str(exc).strip()

            log(f"\u26a0 Typst error in {typ_path.name}: {exc}")

        finally:

            tmp = str(typ_path.with_suffix(".tmp_pdf"))

            try:

                if os.path.exists(tmp):

                    os.remove(tmp)

            except OSError:

                pass

    return errors





def run_generation(jd_path, on_progress=None):

    """Run the LLM-driven generation for one JD file, step by step.



    Returns a summary dict. Progress strings are passed to `on_progress`.

    Raises on LLM invocation failure.

    """

    # Wall-clock start so every progress line carries its elapsed processing time.
    t_start = time.monotonic()

    def log(msg=""):
        # Prefix each progress line with the running elapsed time so the user can
        # see the pace of generation.
        elapsed = time.monotonic() - t_start
        prefix = f"[{elapsed:6.1f}s] " if msg else ""
        if on_progress:
            on_progress(f"{prefix}{msg}")
        else:
            print(f"{prefix}{msg}", flush=True)

    def _dur(t0):
        """Return a human-readable duration since marker t0 (used for per-step timing)."""
        return f"{time.monotonic() - t0:06.1f}s"



    jd_path = str(jd_path)

    if not os.path.isfile(jd_path):

        raise RuntimeError(f"JD file not found: {jd_path}")



    pi_exe = _pi_executable()

    if not pi_exe:

        raise RuntimeError("pi executable not found on PATH / npm global bin.")



    # Serial + minimal context.

    serial_m = re.search(r"(CV-\d{8}-\d{4})", os.path.basename(jd_path))

    serial = serial_m.group(1) if serial_m else f"CV-{_today()}"

    manifest = _read_manifest(serial)

    jd_text = Path(jd_path).read_text(encoding="utf-8")

    base_cv = BASE_CV.read_text(encoding="utf-8") if BASE_CV.exists() else ""

    cv_ctx = _cv_content(base_cv)



    log("CV Builder — LLM Generation Engine")

    log("=" * 44)

    log(f"Serial      {serial}")

    log(f"Manifest    {MANIFEST_DIR / re.sub(r'[^\w\-.]', '_', serial)}.txt")

    log(f"CV context  {len(cv_ctx)} chars (reduced from full {len(base_cv)} bytes)")



    facts = _candidate_facts(manifest)

    if "content" not in facts:

        facts["content"] = cv_ctx



    produced = {}  # label -> path



    # --- Step 1: Match & Gap Analysis ---

    t_step = time.monotonic()
    log("▶ Step 1/5 Match & Gap Analysis…")

    _run_pi(_match_gap_prompt(jd_text, cv_ctx), log)

    gap_path = _collect("MATCH_GAP", JOB_DIR, "txt", serial, on_progress=log)

    produced["match_gap"] = str(gap_path)

    log(f"\u2713 Match & Gap -> {gap_path.name}")
    log(f"\u23f1 Step 1/5 Match & Gap Analysis — {_dur(t_step)}")



    # --- Step 2: Tailored CV (.typ) with self-healing ---

    log("▶ Step 2/5 Tailored CV (.typ) with self-healing…")

    max_regenerate = int(os.environ.get("PI_MAX_REGENERATE", "2"))

    typst_errors = ""

    cv_path = CV_DIR / f"{serial}_CV1.typ"

    for attempt in range(max_regenerate + 1):

        if attempt:

            log(f"\u2139 Regenerating CV with typst error context (attempt {attempt}/{max_regenerate})…")

            prompt = _cv_prompt(jd_text, cv_ctx) + "\n\n==== TYPST COMPILE ERRORS TO FIX ====\n" + typst_errors

        else:

            prompt = _cv_prompt(jd_text, cv_ctx)

        _run_pi(prompt, log)

        cv_path = _collect("CV1", CV_DIR, "typ", serial, on_progress=log)

        errors = _typst_error_report(serial, on_progress=log)

        if not errors:

            typst_errors = ""

            break

        typst_errors = "\n".join(f"{fn}: {msg}" for fn, msg in errors.items())

    if typst_errors:

        log(f"\u26a0 Max regeneration attempts ({max_regenerate}) reached; returning best-effort artefacts.")

    # Per-typ: compile whatever .typ was produced to its sibling .pdf now,
    # so the PDF artefact exists immediately (not only at the end of the run).

    _debug(f"compiling produced CV .typ for {serial}")

    _compile_typ_to_pdf(cv_path, on_progress=log)

    produced["cv"] = str(cv_path)

    log(f"\u2713 CV .typ -> {cv_path.name}")
    log(f"\u23f1 Step 2/5 Tailored CV .typ — {_dur(t_step)}")



    # --- Step 3: Cover Letter ---

    log("▶ Step 3/5 Cover Letter…")

    _run_pi(_cover_letter_prompt(jd_text, facts), log)

    cl_path = _collect("CL1", COVER_DIR, "docx", serial, on_progress=log)

    produced["cover_letter"] = str(cl_path)

    log(f"\u2713 Cover Letter -> {cl_path.name}")
    log(f"\u23f1 Step 3/5 Cover Letter — {_dur(t_step)}")



    # --- Step 4: Interview Prep ---

    log("▶ Step 4/5 Interview Prep…")

    _run_pi(_interview_prep_prompt(jd_text, facts), log)

    ip_path = _collect("IP1", INTERVIEW_DIR, "docx", serial, on_progress=log)

    produced["interview_prep"] = str(ip_path)

    log(f"\u2713 Interview Prep -> {ip_path.name}")
    log(f"\u23f1 Step 4/5 Interview Prep — {_dur(t_step)}")



    # --- Step 5: Application Dossier ---

    log("▶ Step 5/5 Application Dossier…")

    _run_pi(_dossier_prompt(jd_text, manifest), log)

    dossier_path = _collect("Doyen_DomainLeader_Argumentation", DOSSIER_DIR, "docx", serial, on_progress=log)



    # Sanity: warn if any expected deliverable is missing.

    for label, path_p in produced.items():

        if not os.path.isfile(path_p):

            log(f"⚠ Expected deliverable missing: {path_p}")

    produced["dossier"] = str(dossier_path)

    log(f"\u2713 Dossier -> {dossier_path.name}")
    log(f"\u23f1 Step 5/5 Application Dossier — {_dur(t_step)}")



    # Post-step: compile the CV .typ(s) to PDF so artefacts are submission-ready.

    pdf_paths = compile_pdf(serial, on_progress=log)



    # Post-step: record every produced artefact in the monitoring workbook.

    tracker_path = update_tracker(serial, pdf_paths, produced, on_progress=log)

    # Wall-clock total for the whole generation run.
    log(f"\u23f1 TOTAL — {_dur(t_start)}")

    summary = {

        "serial": serial,

        "jd_path": os.path.relpath(jd_path, BASE_DIR),

        "produced": {k: os.path.relpath(v, BASE_DIR) for k, v in produced.items()},

        "pdfs": [os.path.relpath(p, BASE_DIR) for p in pdf_paths],

        "tracker": tracker_path,

    }

    return summary





# ---------------------------------------------------------------------------

# Tracker update

# ---------------------------------------------------------------------------



def update_tracker(serial, pdf_paths, produced=None, on_progress=None):

    """Update the monitoring workbook's row for the serial (Status + Documents Generated)."""

    def _log(m):

        if on_progress:

            on_progress(m)

        else:

            print(m, flush=True)



    if openpyxl is None:

        _log("\u26a0 openpyxl unavailable; skipping tracker update")

        return None



    if not WORKBOOK.exists():

        _log(f"\u26a0 tracker workbook not found: {WORKBOOK}")

        return None



    try:

        wb = openpyxl.load_workbook(WORKBOOK)

    except Exception as exc:

        _log(f"\u2717 failed to open tracker workbook: {exc}")

        return None



    ws = wb["Log"] if "Log" in wb.sheetnames else wb.create_sheet("Log")

    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]

    row = None

    for r in range(2, ws.max_row + 1):

        if ws.cell(row=r, column=1).value == serial:

            row = r

            break



    if row is None:

        _log(f"\u26a0 no tracker row for {serial}")

        wb.close()

        return None



    # Collect every produced artefact relative to the project root.

    doc_paths = list(pdf_paths)

    patterns = ("*.pdf", "*.docx")

    for sub in ("3 Custom CV", "5 Custom Cover Letter", "6 Interview Prep"):

        for pattern in patterns:

            for f in sorted((BASE_DIR / sub).glob(pattern)):

                if f.name.startswith(f"{serial}_"):

                    doc_paths.append(str(f))

    gap = BASE_DIR / "2 Job description" / f"{serial}_MATCH_GAP.txt"

    if gap.exists():

        doc_paths.append(str(gap))

    doc_paths = list(dict.fromkeys(doc_paths))



    generated = "; ".join(doc_paths)

    ws.cell(row=row, column=9).value = "Documents generated"  # Status

    ws.cell(row=row, column=10).value = generated              # Documents Generated

    ws.cell(row=row, column=11).value = (

        f"Generated {_today()}: {len([p for p in doc_paths if '.pdf' in p])} CV PDF(s) + "

        f"{len([p for p in doc_paths if 'CL' in p])} cover letter(s) + "

        f"{len([p for p in doc_paths if 'IP' in p])} interview prep(s)"

    )

    wb.save(WORKBOOK)

    wb.close()

    _log(f"\u2713 Tracker updated: {os.path.relpath(WORKBOOK, BASE_DIR)}")

    return os.path.relpath(WORKBOOK, BASE_DIR)





def _today():

    import datetime

    return datetime.date.today().isoformat().replace("-", "")





if __name__ == "__main__":

    argv = sys.argv[1:]

    if argv:

        jd_path = argv[-1]

    else:

        jd_files = sorted(JOB_DIR.glob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)

        jd_path = str(jd_files[0]) if jd_files else ""

        if not jd_path:

            print("[error] no JD .txt file found in 2 Job description")

            sys.exit(1)

    try:

        summary = run_generation(jd_path)

        print("Summary:", json.dumps(summary, indent=2))

    except Exception as e:

        print(f"[error] generation failed: {e}")

        sys.exit(1)
