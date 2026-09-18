#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

CV Builder — LLM-Driven Generation Engine (Option B)

=====================================================

Given a collected session (base CV + JD + manifest), drive an LLM (pi) to

produce the full application package described by the manifest:



    1. Match & Gap Analysis   -> job_descriptions/

    2. Tailored CV (.typ)     -> custom_cv/<serial>_CV1.typ   (+ compiled .pdf)

    3. Tailored Cover Letter  -> cover_letters/<serial>_CL1.docx

    4. Interview Prep (STAR)  -> 6 Interview Prep/<serial>_IP1.docx

    5. Application Dossier    -> input_job_description/

    6. Recruiter Fit Message   -> application_monitoring/<serial>_RM1.docx

    7. Tracker + status update -> application_monitoring/Application_Tracker.xlsx



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

    python generation/engine.py                              # newest JD in job_descriptions



Progress is printed to stdout so the web dashboard can stream it.

"""

import os

import re

import sys

import json

import time

import datetime

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

CV_DIR = BASE_DIR / "custom_cv"

COVER_DIR = BASE_DIR / "cover_letters"

INTERVIEW_DIR = BASE_DIR / "6 Interview Prep"

DOSSIER_DIR = BASE_DIR / "input_job_description"

MANIFEST_DIR = BASE_DIR / "application_monitoring" / "manifests"

WORKBOOK = BASE_DIR / "application_monitoring" / "Application_Tracker.xlsx"

BASE_CV = BASE_DIR / "source" / "SONG Ernest - CV v1.typ"

JOB_DIR = BASE_DIR / "job_descriptions"

# One folder per job application, named "YYYYMMDD - Company - Position".
APPLICATIONS_DIR = BASE_DIR / "Job Applications"



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
    # Assign `line` BEFORE the try so a logging failure (e.g. unwritable DEBUG_LOG)
    # can never leave it unbound and raise UnboundLocalError at `return line`.
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        with open(DEBUG_LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        # Never let debug logging break the generation flow.
        pass

    return line





def _pi_executable():

    """Return the path to the pi CLI, or None if it cannot be found."""

    candidates = []

    # npm global bins on Windows are installed as .cmd/.ps1/.js (not bare `pi`),
    # so look across common extensions rather than assuming a bare name or .exe.
    exts = ("", ".cmd", ".ps1", ".js")

    npm_dirs = [
        os.environ.get("APPDATA", ""),
        os.environ.get("LOCALAPPDATA", ""),
    ]

    for d in npm_dirs:

        for ext in exts:

            if d:

                candidates.append(os.path.join(d, "npm", "pi" + ext))

    for dir_ in os.environ.get("PATH", "").split(os.pathsep):

        for ext in exts:

            candidates.append(os.path.join(dir_, "pi" + ext))

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

    m = re.search(r"Recruiter\s*:\s*(.+)", manifest)

    if m:

        recruiter = m.group(1).strip()

        # Treat placeholders / missing values as "unknown" rather than the literal "N/A".

        facts["recruiter"] = None if recruiter.upper() in ("N/A", "NA", "–", "") else recruiter

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

        "- Position-name preservation: the job TITLE (position name) of each professional-experience entry must stay VERBATIM. The ONLY permitted change is removing a trailing \"(freelance)\" tag when the role became permanent; every other word of the title must remain identical.\n"

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



def _recruiter_message_prompt(jd_text, facts, recruiter_name):

    """Reverse-engineered prompt for the recruiter-fit 'cheat-sheet' message.

    Reproduces the kind of message Ernest SONG sends to his recruiter (Milète / Michèle)
    when a new opportunity arrives: a warm, confident, recruiter-ready email that maps the
    candidate's REAL experience to the JD's specific requirements, framed as a quick
    cheat-sheet ahead of a recruiter/client call. Output is a single .docx message.

    The structure mirrors a validated human-written example (greeting -> conviction ->
    JD-context acknowledgement -> time-pressure frame -> themed cheat-sheet -> profile
    summary -> warm closing), but every section and heading is derived fresh from the
    incoming JD + candidate facts, so it generalises to any future JD.
    """

    role = facts.get("target_role", "the target role")

    return (
        "You are Ernest SONG, a senior executive finance professional, writing a warm but "
        "confident email to your recruiter, " + str(recruiter_name) + ", who has just "
        "passed you a new opportunity. Your goal is to make it trivial for them to sell you "
        "to their client, so hand them a ready-to-use 'fit cheat-sheet'.\n\n"

        "==== TARGET ROLE ====\n" + role + "\n\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n\n"

        "==== CANDIDATE FACTS (your real CV — your source of truth) ====\n" + facts.get("content", "") + "\n\n"

        "==== EMAIL STRUCTURE (follow exactly) ====\n"

        "1) Greet the recruiter by name at the very top ('Dear " + str(recruiter_name) + ",').\n"

        "2) Open with genuine conviction: you are the ideal candidate for this client and "
        "this opportunity is your top priority.\n"

        "3) State that you reviewed the role/scope, then explicitly name 1-2 of the JD's "
        "defining themes (e.g. high growth + acquisitions + Medium-Term Plan) and how they "
        "align perfectly with your core expertise.\n"

        "4) Add a short 'time is short' frame: acknowledge that they are meeting the client "
        "soon, so here is a compact cheat-sheet proving your fit.\n"

        "5) Provide the CHEAT-SHEET of 3-4 THEMED SECTIONS. Derive each section heading "
        "directly from the JD's actual requirements (e.g. 'Medium-Term Plan / Multi-year "
        "Planning', 'Group Controlling, Consolidation & Technical Mastery', 'Investor "
        "Support, M&A & Due Diligence', 'Business Partner Mindset & Systems'). Under each "
        "heading cite 2-3 concrete evidence bullets drawn STRICTLY from your real CV — "
        "include company names, years, and hard numbers (turnover, deal sizes, budget, "
        "headcount). Ensure every major JD requirement is backed by at least one bullet.\n"

        "6) Close with a short PROFILE SUMMARY of exactly these four labelled lines: "
        "Profile (e.g. 'Executive Finance Professional (15+ years)'), Education, "
        "Positioning (your target niche), and Availability (immediate, location, schedule).\n"

        "7) Final line: confirm the updated CV is attached, wish them a good evening, and "
        "reference the upcoming conversation.\n\n"

        "==== RULES ====\n"

        "- Tone: warm, professional, self-assured — never arrogant, never apologetic.\n"

        "- Base EVERY claim on the candidate's real CV facts. No fabrication and no "
        "invented numbers; if a precise figure is unknown, describe the impact qualitatively.\n"

        "- Keep it scannable: short paragraphs and punchy bullet lists (roughly under 400 words).\n"

        "- Output ONLY the email body, ready to paste into an email client (no meta-commentary).\n"

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

# ---------------------------------------------------------------------------
# Application-folder helpers (one folder per job application) + docx conversion
# ---------------------------------------------------------------------------


def _slug(text):

    """Sanitize a string for safe use as a folder / file name component.

    Keeps the " - " separators readable while replacing Windows-invalid
    characters (_) with underscores.

    """

    if not text:

        return ""

    return re.sub(r"[^\w\-.]", "_", str(text)).strip(" .")



def _app_folder(serial, company="", position=""):

    """Return the per-application output folder named "YYYYMMDD - Company - Position".

    The date is derived from the serial (CV-YYYYMMDD-NNNN); company/position
    are free-form but fall back to safe placeholders so a folder always exists.

    """

    ymd = serial[3:11] if len(serial) >= 11 else _today()

    comps = [ymd, company or "Unknown Company", position or "Unknown Position"]

    return APPLICATIONS_DIR / " - ".join(_slug(c) for c in comps)



def _txt_to_docx(src_txt, dst_docx):

    """Convert an LLM-produced .txt file into a proper .docx (deterministic).

    Returns the docx path on success, or None on failure (logged).

    """

    try:

        from docx import Document

    except ImportError:

        _debug("python-docx unavailable; skipping txt -> docx conversion")

        return None


    try:

        with open(src_txt, "r", encoding="utf-8") as fh:

            content = fh.read()

        doc = Document()

        for line in content.split("\n"):

            doc.add_paragraph(line)

        doc.save(dst_docx)

        _debug(f"converted {Path(src_txt).name} -> {Path(dst_docx).name}")

        return dst_docx

    except Exception as exc:

        _debug(f"txt_to_docx failed {Path(src_txt).name}: {exc}")

        return None



def _clean_stale(folder, serial, ext, keep_labels=()):

    """Remove files of extension `ext` in `folder` that do NOT match

    ``{serial}_{label}.{ext}`` for any label in `keep_labels`, so only a single
    canonical document of each kind survives.

    """

    folder = Path(folder)

    if not folder.exists():

        return

    for f in folder.glob(f"*.{ext}"):

        kept = any(f.name.startswith(f"{serial}_{lbl}") for lbl in keep_labels)

        if not kept:

            try:

                f.unlink()

                _debug(f"removed stale {f.name}")

            except OSError as exc:

                _debug(f"could not remove stale {f.name}: {exc}")


# Helpers: PDF compilation, typst error reporting, tracker update

# ---------------------------------------------------------------------------



def compile_pdf(serial, on_progress=None, app_folder=None):

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



    folder = Path(app_folder) if app_folder is not None else CV_DIR
    typ_files = sorted(folder.glob(f"{serial}_CV*.typ"))

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





def run_generation(jd_path, on_progress=None, company="", position=""):

    """Run the LLM-driven generation for one JD file, step by step.



    Returns a summary dict. Progress strings are passed to `on_progress`.

    Raises on LLM invocation failure.

    """

    # Wall-clock start so every progress line carries its elapsed processing time.
    t_start = time.monotonic()

    def _fmt(secs):
        # Timing shown consistently in M:SS (minutes) throughout the log.
        return f"{int(secs // 60):02d}:{secs % 60:05.1f}"

    def log(msg=""):
        # Prefix each progress line with the running elapsed time (in minutes) so
        # the user can see the pace of generation.
        prefix = f"[{_fmt(time.monotonic() - t_start)}] " if msg else ""
        if on_progress:
            on_progress(f"{prefix}{msg}")
        else:
            print(f"{prefix}{msg}", flush=True)

    def _dur(t0):
        """Return a human-readable duration since marker t0 in M:SS form (e.g. 07:52.3)."""
        secs = time.monotonic() - t0
        mins = int(secs // 60)
        rest = secs % 60
        return f"{mins:02d}:{rest:05.1f}"



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

    # Per-application output folder: "YYYYMMDD - Company - Position".
    app_folder = _app_folder(serial, company=company, position=position)
    os.makedirs(app_folder, exist_ok=True)

    jd_text = Path(jd_path).read_text(encoding="utf-8")

    base_cv = BASE_CV.read_text(encoding="utf-8") if BASE_CV.exists() else ""

    cv_ctx = _cv_content(base_cv)



    log("CV Builder — LLM Generation Engine")

    log("=" * 44)

    log(f"Serial      {serial}")

    log(f"Manifest    {MANIFEST_DIR / re.sub(r'[^\w\-.]', '_', serial)}.txt")

    log(f"CV context  {len(cv_ctx)} chars (reduced from full {len(base_cv)} bytes)")
    log(f"App folder  {os.path.relpath(app_folder, BASE_DIR)}")



    facts = _candidate_facts(manifest)

    if "content" not in facts:

        facts["content"] = cv_ctx



    produced = {}  # label -> path

    # Remove stale artefacts from prior runs so only ONE canonical doc of each
    # kind survives inside the per-application folder.
    _debug("cleaning stale artefacts in app folder")
    _clean_stale(app_folder, serial, "typ", keep_labels=("CV1",))
    _clean_stale(app_folder, serial, "docx", keep_labels=("CL1", "IP1", "Doyen_DomainLeader_Argumentation", "RM1"))
    _clean_stale(app_folder, serial, "txt", keep_labels=("MATCH_GAP",))



    # --- Step 1: Match & Gap Analysis ---

    t_step = time.monotonic()
    log("▶ Step 1/5 Match & Gap Analysis…")

    _run_pi(_match_gap_prompt(jd_text, cv_ctx), log)

    # Keep the JD input inside the per-application folder for easy retrieval.
    jd_dest = app_folder / f"{serial}.txt"
    try:
        if str(jd_path) != str(jd_dest) and not jd_dest.exists():
            _debug(f"stored JD -> {jd_dest.name}")
            Path(jd_dest).write_text(jd_text, encoding="utf-8")
    except OSError as exc:
        _debug(f"could not store JD file: {exc}")

    gap_path = _collect("MATCH_GAP", app_folder, "txt", serial, on_progress=log)

    produced["match_gap"] = str(gap_path)

    log(f"\u2713 Match & Gap -> {gap_path.name}")
    log(f"\u23f1 Step 1/5 Match & Gap Analysis — {_dur(t_step)}")



    # --- Step 2: Tailored CV (.typ) with self-healing ---

    log("▶ Step 2/5 Tailored CV (.typ) with self-healing…")

    max_regenerate = int(os.environ.get("PI_MAX_REGENERATE", "2"))

    typst_errors = ""

    cv_path = app_folder / f"{serial}_CV1.typ"

    for attempt in range(max_regenerate + 1):

        if attempt:

            log(f"\u2139 Regenerating CV with typst error context (attempt {attempt}/{max_regenerate})…")

            prompt = _cv_prompt(jd_text, cv_ctx) + "\n\n==== TYPST COMPILE ERRORS TO FIX ====\n" + typst_errors

        else:

            prompt = _cv_prompt(jd_text, cv_ctx)

        _run_pi(prompt, log)

        cv_path = _collect("CV1", app_folder, "typ", serial, on_progress=log)

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

    # The LLM writes text; convert it to a real Word docx inside the app folder.
    cl_docx = app_folder / f"{serial}_CL1.docx"
    cl_src = _collect("CL1", app_folder, "docx", serial, on_progress=log)
    if not os.path.isfile(cl_docx):
        cl_txt = _collect("CL1", app_folder, "txt", serial, on_progress=log)
        if os.path.isfile(cl_txt):
            _debug(f"converting cover letter {Path(cl_txt).name} -> docx")
            _txt_to_docx(cl_txt, str(cl_docx))
            try:
                if cl_txt != cl_docx:
                    cl_txt.unlink()
            except OSError:
                pass

    # Ensure only ONE cover letter survives (the LLM sometimes writes CL1..CL5).
    for _extra in app_folder.glob(f"{serial}_CL*.txt"):
        if _extra.name not in (f"{serial}_CL1.txt",):
            try:
                _debug(f"removed extra cover-letter {_extra.name}")
                _extra.unlink()
            except OSError as exc:
                _debug(f"could not remove {_extra.name}: {exc}")

    produced["cover_letter"] = str(cl_docx)

    log(f"\u2713 Cover Letter -> {cl_docx.name}")
    log(f"\u23f1 Step 3/5 Cover Letter — {_dur(t_step)}")



    # --- Step 4: Interview Prep ---

    log("▶ Step 4/5 Interview Prep…")

    _run_pi(_interview_prep_prompt(jd_text, facts), log)

    # The LLM writes text; convert it to a real Word docx inside the app folder.
    ip_docx = app_folder / f"{serial}_IP1.docx"
    ip_src = _collect("IP1", app_folder, "docx", serial, on_progress=log)
    if not os.path.isfile(ip_docx):
        ip_txt = _collect("IP1", app_folder, "txt", serial, on_progress=log)
        if os.path.isfile(ip_txt):
            _debug(f"converting interview prep {Path(ip_txt).name} -> docx")
            _txt_to_docx(ip_txt, str(ip_docx))
            try:
                if ip_txt != ip_docx:
                    ip_txt.unlink()
            except OSError:
                pass

    # Ensure only ONE interview-prep item survives (the LLM sometimes writes IP1..IP6).
    for _extra in app_folder.glob(f"{serial}_IP*.txt"):
        if _extra.name not in (f"{serial}_IP1.txt",):
            try:
                _debug(f"removed extra interview prep {_extra.name}")
                _extra.unlink()
            except OSError as exc:
                _debug(f"could not remove {_extra.name}: {exc}")

    produced["interview_prep"] = str(ip_docx)

    log(f"\u2713 Interview Prep -> {ip_docx.name}")
    log(f"\u23f1 Step 4/5 Interview Prep — {_dur(t_step)}")



    # --- Step 5: Application Dossier ---

    log("▶ Step 5/5 Application Dossier…")

    _run_pi(_dossier_prompt(jd_text, manifest), log)

    dossier_path = _collect("Doyen_DomainLeader_Argumentation", app_folder, "docx", serial, on_progress=log)



    # Sanity: warn if any expected deliverable is missing.

    for label, path_p in produced.items():

        if not os.path.isfile(path_p):

            log(f"⚠ Expected deliverable missing: {path_p}")

    produced["dossier"] = str(dossier_path)

    log(f"\u2713 Dossier -> {dossier_path.name}")
    log(f"\u23f1 Step 5/5 Application Dossier — {_dur(t_step)}")



    # --- Step 6/6: Recruiter 'Fit Cheat-Sheet' Email (docx) ---

    log("▶ Step 6/6 Recruiter Fit Message...")

    recruiter_name = facts.get("recruiter") or "the recruiter"

    rm_stdout, _ = _run_pi(_recruiter_message_prompt(jd_text, facts, recruiter_name), log)

    # The LLM writes text; convert it to a real Word docx inside the app folder.
    rm_docx = app_folder / f"{serial}_RM1.docx"
    rm_src = _collect("RM1", app_folder, "docx", serial, on_progress=log)
    if not os.path.isfile(rm_docx):
        rm_txt = _collect("RM1", app_folder, "txt", serial, on_progress=log)
        if os.path.isfile(rm_txt):
            _debug(f"converting recruiter message {Path(rm_txt).name} -> docx")
            _txt_to_docx(rm_txt, str(rm_docx))
            try:
                if rm_txt != rm_docx:
                    rm_txt.unlink()
            except OSError:
                pass
    # Fallback: if the LLM printed the message to stdout instead of writing a file,
    # persist it as RM1.txt and convert to docx (mirrors the cover-letter step).
    if not os.path.isfile(rm_docx) and rm_stdout and not os.path.isfile(app_folder / f"{serial}_RM1.txt"):
        _debug(f"recruiter message not written by LLM; persisting stdout -> RM1.txt")
        (app_folder / f"{serial}_RM1.txt").write_text(rm_stdout, encoding="utf-8")
        _txt_to_docx(app_folder / f"{serial}_RM1.txt", str(rm_docx))

    # Ensure only ONE recruiter-message artefact survives (the LLM sometimes writes RM1..RM3).
    for _extra in app_folder.glob(f"{serial}_RM*.txt"):
        if _extra.name not in (f"{serial}_RM1.txt",):
            try:
                _debug(f"removed extra recruiter message {_extra.name}")
                _extra.unlink()
            except OSError as exc:
                _debug(f"could not remove {_extra.name}: {exc}")

    produced["recruiter_message"] = str(rm_docx)

    if not os.path.isfile(rm_docx):
        log(f"⚠ Recruiter Fit Message not produced: {rm_docx}")

    log(f"✓ Recruiter Fit Message -> {rm_docx.name}")
    log(f"⏱ Step 6/6 Recruiter Fit Message — {_dur(t_step)}")


    # Post-step: compile the CV .typ(s) to PDF so artefacts are submission-ready.

    pdf_paths = compile_pdf(serial, on_progress=log, app_folder=app_folder)



    # Post-step: record every produced artefact in the monitoring workbook.

    tracker_path = update_tracker(serial, pdf_paths, produced, on_progress=log)

    # Wall-clock total for the whole generation run.
    log(f"\u23f1 TOTAL — {_dur(t_start)}")

    summary = {

        "serial": serial,

        "app_folder": os.path.relpath(app_folder, BASE_DIR),

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

    for sub in ("custom_cv", "cover_letters", "6 Interview Prep"):

        for pattern in patterns:

            for f in sorted((BASE_DIR / sub).glob(pattern)):

                if f.name.startswith(f"{serial}_"):

                    doc_paths.append(str(f))

    # Recruiter Fit Message + dossier live in the per-application sub-folders
    # (named by date, not by serial), so walk one level of sub-folder.

    for app_sub in APPLICATIONS_DIR.glob("*"):

        if not app_sub.is_dir():

            continue

        for pattern in patterns:

            for f in sorted(app_sub.glob(pattern)):

                if f.name.startswith(f"{serial}_"):

                    doc_paths.append(str(f))

    gap = BASE_DIR / "job_descriptions" / f"{serial}_MATCH_GAP.txt"

    if gap.exists():

        doc_paths.append(str(gap))

    doc_paths = list(dict.fromkeys(doc_paths))



    generated = "; ".join(doc_paths)

    ws.cell(row=row, column=9).value = "Documents generated"  # Status

    ws.cell(row=row, column=10).value = generated              # Documents Generated

    ws.cell(row=row, column=11).value = (

        f"Generated {_today()}: {len([p for p in doc_paths if '.pdf' in p])} CV PDF(s) + "

        f"{len([p for p in doc_paths if 'CL' in p])} cover letter(s) + "

        f"{len([p for p in doc_paths if 'IP' in p])} interview prep(s) + "

        f"{len([p for p in doc_paths if 'RM' in p])} recruiter message(s)"

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

            print("[error] no JD .txt file found in job_descriptions")

            sys.exit(1)

    try:

        summary = run_generation(jd_path)

        print("Summary:", json.dumps(summary, indent=2))

    except Exception as e:

        print(f"[error] generation failed: {e}")

        sys.exit(1)
