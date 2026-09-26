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
import shutil

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


# The master data model is the single source of truth. The Astro site reads
# ``profile.json`` directly; the CV engine reads the .typ generated from it (below).
# When the generated file exists we prefer it over the hardcoded v1.typ, so website
# updates flow into both the portfolio and generated CVs. Otherwise we fall back.
def _base_cv_text():
    """Return the canonical base CV text, generated from the master data model.

    Reads ``MyWebsite/src/data/profile.typ`` (produced by ``typst_builder.py`` from
    ``profile.json``). Falls back to the original ``v1.typ`` when the generated file
    is missing, so CV generation keeps working during early development.
    """
    generated = BASE_DIR / "MyWebsite" / "src" / "data" / "profile.typ"
    if generated.exists():
        try:
            return generated.read_text(encoding="utf-8")
        except OSError as exc:
            _debug(f"could not read generated .typ {generated.name}: {exc}")
    return BASE_CV.read_text(encoding="utf-8") if BASE_CV.exists() else ""

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

_MAX_LLM_RETRIES = int(os.environ.get("PI_MAX_LLM_RETRIES", "3"))

_LLM_RETRY_BASE_DELAY = float(os.environ.get("PI_LLM_RETRY_BASE_DELAY", "10"))



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


def _compact_facts(base_cv):

    """Extract only the ESSENTIAL candidate content for the LLM prompts.

    The full base CV is ~18 KB (mostly Typst layout boilerplate the LLM does not
    need). For the cover-letter / interview-prep / recruiter-message prompts we only
    need: the real profile quote, the target position, and the most recent / most
    relevant professional-experience entries. This shrinks each prompt by ~70%,
    which materially speeds up the LLM (smaller context -> faster output).

    Returns a compact, human-readable string.

    """

    if not base_cv:
        return ""

    out = []

    # 1) Profile quote (the real text, not the boilerplate field).
    qm = re.search(r'quote: "(.*)"', base_cv, re.S)
    if qm:
        out.append("PROFILE QUOTE:\n" + qm.group(1).strip())

    # 2) Position (the role the CV is currently tuned to).
    posm = re.search(r'position: "([^"]*)"', base_cv)
    if posm:
        out.append("CURRENT POSITION:\n" + posm.group(1).strip())

    # 3) The most recent professional-experience entries (first 3 entries only).
    pe_m = re.search(r"= Professional Experience", base_cv)
    if pe_m:
        # Split on the #v(gap) separators between entries; each block is a full
        # #entry(...) record (the role header contains parens, so a paren-matching
        # regex would truncate early).
        body = base_cv[pe_m.end():]
        # Filter out empty blocks (the body begins with the first #v(gap) separator,
        # so the first split element is an empty string).
        entries = [e for e in re.split(r"\n#v\(gap\)\n", body) if e.strip()]
        for i, entry in enumerate(entries[:3], 1):
            cleaned = entry.strip().strip("(").strip()
            out.append("--- EXPERIENCE ENTRY %d ---\n%s" % (i, cleaned))

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

    # Targeted-edit prompt: change as LITTLE as possible. Asking the LLM to
    # rewrite the entire CV from scratch is what makes each step so slow (it must
    # reconstruct ~6-8 KB of candidate content + the full Typst layout). Asking
    # it to keep everything identical except a few tailored edits cuts the LLM's
    # semantic work dramatically while still JD-tailoring the key sections.

    return (

        "You are a senior ATS-friendly CV author. Tailor the candidate CV to the"
        "target Job Description, but change as LITTLE as possible.\n\n"

        "RULES:\n"

        "- Output the FULL Typst source (a complete, valid .typ file).\n"

        "- Keep the base CV layout, styling, Education, Competencies, Languages and"
        "ALL Professional Experience UNCHANGED - do NOT rewrite, reorder or drop anything"
        "except the targeted edits listed below.\n"

        "- ONLY make these edits:"
        "  (1) replace the profile/summary with a concise value proposition (2-3 lines"
        "       that mirror the JD top requirements from the candidate REAL experience;"
        "  (2) adjust 2-3 of the Professional Experience bullets so they surface the"
        "       candidate most relevant, TRUE experience for this JD.\n"

        "- Use exact JD keyword phrasing ONLY where real experience supports it.\n"

        "- Preserve each job TITLE (position name) verbatim. The ONLY permitted change is"
        "   removing a trailing (freelance) tag when the role became permanent.\n"

        "- Never fabricate roles, companies, dates or metrics.\n\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n"

        "==== CANDIDATE CONTENT (base CV - edit minimally) ====\n" + cv_ctx.strip()

    )





def _cover_letter_prompt(jd_text, facts):

    return (

        "You are an executive cover-letter writer. Draft ONE concise, high-converting\n"

        "cover letter (under 250 words) that bridges the candidate's real background to\n"

        "the JD's top 3 requirements. Include an honest statement on how his unique\n"

        " perspective covers any minor skill gap, without apologising.\n\n"

        "==== TARGET ROLE ====\n" + facts.get("target_role", "the target position") + "\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n"

        "==== CANDIDATE FACTS ====\n" + facts.get("compact_content", "")

    )





def _interview_prep_prompt(jd_text, facts):

    return (

        "You are a senior interview coach. Produce 6 targeted behavioral interview\n"

        "questions likely to be asked for this role, each with an STAR-method answer\n"

        "(Situation, Task, Action, Result) based STRICTLY on the candidate's real CV\n"

        "experiences. No fabrication.\n\n"

        "==== TARGET ROLE ====\n" + facts.get("target_role", "the target position") + "\n"

        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n"

        "==== CANDIDATE FACTS ====\n" + facts.get("compact_content", "")

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

        "==== CANDIDATE FACTS (your real CV — your source of truth) ====\n" + facts.get("compact_content", "") + "\n\n"

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

def _derive_position_title(jd_text, on_progress=None):

    """Determine the single concise job TITLE for the CV's top-of-page `position:`.

    This is the fix for the reported issue "title isn't correct". Rather than a
    stale hardcoded fallback, the LLM is asked to DISTINGUISH the exact job
    position from the JD, so the CV header reflects THIS specific role.

    Strategy:
      1. Ask the LLM for the single concise job title (small prompt).
      2. If the LLM path fails, fall back to a keyword search of the JD body.

    Returns the trimmed title string (may be empty if nothing is found).

    """

    def log(msg=""):

        if on_progress:

            on_progress(msg)

        else:

            print(msg, flush=True)

    # 1) Ask the LLM to distinguish the exact job position from the JD.
    try:

        title_prompt = (
            "You are extracting the job title for a CV header. Read the Job Description "
            "below and output ONLY the single concise job TITLE (role/position name). "
            "Do NOT explain, do NOT add prose. Output just the title phrase.\n\n"
            "==== JOB Description ====\n" + jd_text.strip() + "\n"
        )

        stdout_raw, _stderr = _run_pi(title_prompt, log)

        if stdout_raw:

            first = next((ln.strip() for ln in stdout_raw.splitlines() if ln.strip()), "")
            # Drop a leading label like "Title:" or "Job Title:" if the LLM adds one.
            first = re.sub(r"^(?:job\\s+title|title)\\s*:\s*", "", first, flags=re.I)
            if first:

                return first

    except Exception as exc:

        log(f"⚠ LLM title derivation failed: {exc}")

    # 2) Fall back to a keyword search of the JD body (no LLM).
    try:

        from .gen_cv_typ import _extract_position

        return _extract_position(jd_text)

    except Exception as exc:

        log(f"⚠ JD-title fallback failed: {exc}")

        return ""

def _cv_llm_prompt(jd_text, compact_content, target_role=None):

    """Prompt the LLM to generate ONLY the five tailored CV parts.

    The goal is a HYBRID CV: the layout / styling / education / languages /
    interests / interpersonal / Working-Tools / keywords fields stay DETERMINISTIC
    (taken straight from the base template + JD signals), while these FIVE parts are
    generated by the LLM from the candidate's real experience:

      1. QUOTE        – value-proposition summary
      2. CORE COMPETENCIES – the left column of the competencies grid
      3. POSITION NAME – the title of the entry flagged (Freelancer)
      4. BULLETS      – the bullet list of that same (Freelancer) entry
      5. HIGHLIGHT    – which company names get `important: true` (light grey)

    Output is a strict five-header block so it can be parsed deterministically.

    """

    return (
        "You are an expert executive CV writer for a senior FP&A / finance-control "
        "freelancer. Adapt FIVE specific parts of the CV for the target job.\n\n"
        "==== TARGET ROLE ====\n" + str(target_role or "the target position") + "\n\n"
        "==== JOB DESCRIPTION ====\n" + jd_text.strip() + "\n\n"
        "==== YOUR REAL CV CONTEXT ====\n" + (compact_content or "") + "\n\n"
        "Produce EXACTLY these five sections, in this exact order, keeping the header "
        "labels verbatim:\n\n"
        "QUOTE:\n"
        "<One high-impact value-proposition summary (2-4 sentences). English only. "
        "Frame the candidate as an executive finance partner who turns complex data "
        "into insight. Do NOT mention any third-party vendor/tool brand names.>\n\n"
        "CORE COMPETENCIES:\n"
        "<The 'Core competencies' grid content as raw Typst list items grouped under "
        "'====' sub-category headers, e.g.:\n"
        "==== Planning & Forecasting\n"
        "- Medium-Term Plan (Multi-Year Business Planning)\n"
        "- P&L Analysis & Forecasting\n"
        "==== Consolidation & Reporting\n"
        "...> (use only English, ATS-relevant terms; keep it to 3-4 sub-categories)\n\n"
        "POSITION NAME:\n"
        "<The exact job title for the entry flagged (Freelancer) — a single concise title.>\n\n"
        "BULLETS:\n"
        "<The bullet-point list (Typst '- ...' items) for that same (Freelancer) entry. "
        "Base them STRICTLY on the candidate's real experience for that role. No fabrication.>\n\n"
        "HIGHLIGHT:\n"
        "<The comma-separated list of COMPANY NAMES whose experience is relevant to "
        "this JD and should be marked 'important: true' (light grey). If none are "
        "relevant, write NONE.>\n\n"
        "Rules:\n"
        "- English only; truthful to the candidate's real experience (no fabrication).\n"
        "- Do NOT output any other prose before or after these five headers.\n"
        "- For CORE COMPETENCIES and BULLETS, output raw Typst list syntax only."
    )



def _parse_cv_llm_output(raw):

    """Parse the strict five-header block produced by _cv_llm_prompt.\n\n"
    "    Returns a dict with keys: quote, competencies, position, bullets, highlight.

    """

    parts = {"quote": "", "competencies": "", "position": "", "bullets": "", "highlight": "NONE"}

    headers = ["QUOTE:", "CORE COMPETENCIES:", "POSITION NAME:", "BULLETS:", "HIGHLIGHT:"]

    lines = raw.splitlines()

    # Index of each header line (first occurrence wins) so section content can
    # be sliced AFTER the header itself -- the header label is a wrapper, not
    # part of the payload (the LLM echoes it, which must not leak into the CV).

    header_idx = {h: None for h in headers}

    for i, line in enumerate(lines):

        s = line.strip()

        for h in headers:

            if s == h or s.startswith(h + " "):

                if header_idx[h] is None:

                    header_idx[h] = i

    def section(start_header, end_header):

        """Return the content between `start_header`'s line and the next section

        header (or EOF). Missing headers degrade gracefully to an empty section.

        """

        start = header_idx[start_header]

        if start is None:

            return ""

        if end_header is None:

            end = len(lines)

        else:

            end = header_idx[end_header]

            if end is None:

                end = len(lines)

        return "\n".join(lines[start + 1:end]).strip()

    parts["quote"] = section("QUOTE:", "CORE COMPETENCIES:")

    parts["competencies"] = section("CORE COMPETENCIES:", "POSITION NAME:")

    parts["position"] = section("POSITION NAME:", "BULLETS:")

    parts["bullets"] = section("BULLETS:", "HIGHLIGHT:")

    parts["highlight"] = section("HIGHLIGHT:", None)

    return parts



_NOISE = {
    "view company", "show more", "from freelancer to permanent roles",
    "recommended", "recommended by linkedin", "linkedin members",
    "recommendations", "how to become",
}

def _jd_aware_highlight(t, jd_text=""):

    """Deterministically adapt the light-grey highlight to the SPECIFIC JD.

    This is the backstop for "highlighting ... not adapt to the JD". After the LLM's
    `parts["highlight"]` has been applied, this re-evaluates each #entry and forces
    `important: true` when the entry's company name or detail text mentions any JD
    focus term (data-platform / integration / business-analysis signals), and
    `important: false` otherwise. This guarantees the grey highlight reflects THIS
    role regardless of what the LLM happened to emit.

    Returns the modified text.

    """

    if not jd_text:

        return t

    # Derive JD focus terms (role title + multi-word phrases), filtering generic
    # single words so the highlight stays precise (a bare "Business" must not
    # light up every business-analyst entry).
    _COMMON = {
        "business", "data", "platform", "analysis", "management", "experience",
        "role", "team", "services", "working", "group", "level", "company",
        "sector", "position", "career", "field",
    }
    terms = []
    seen = set()

    def _add(term):

        if term and term.lower() not in seen:

            seen.add(term.lower())
            terms.append(term)

    # The role title line is the strongest signal -- keep it whole.
    for line in jd_text.splitlines():

        s = line.strip()

        if not s or s.lower() in _NOISE:

            continue

        if re.search(r"(analyst|officer|manager|director|lead|consultant|specialist|controller)", s, re.I) and not re.search(r"[.!?]$,", s):

            _add(s)

    # Domain-signal vocabulary -- the second word of a bigram or a standalone token
    # marks a phrase/word as JD-relevant (data platform / data migration / integration).
    _DOMAIN = frozenset({
        "data", "platform", "migration", "transform", "transformation",
        "integration", "integrations", "infra", "infrastructures", "sap", "hana", "erp",
    })
    _SIGNAL_WORDS = {"platform", "migration"}
    words = re.split(r"[\s,]+", jd_text)

    # Bigram phrases whose second word is a domain signal ("data platform",
    # "data migration", "data integration"). These precise phrases drive the
    # whole-word highlight matching.
    for a, b in zip(words, words[1:]):

        a, b = a.strip(), b.strip()

        if not a or not b:

            continue

        if b.lower() in _DOMAIN:

            phrase = "%s %s" % (a, b)

            _add(phrase)

    # Standalone domain-signal words that carry meaning ("platform", "migration"),
    # so single-word matches land even without a preceding qualifier. Normalize
    # plurals to their singular signal ("Platforms" -> "platform") so the keyword
    # matches the singular form in CV detail text.
    for tok in re.split(r"[\s,]+", jd_text):

        w = tok.strip()

        w_low = w.lower()

        base = w_low[:-1] if w_low.endswith("s") else w_low

        if base in _DOMAIN and base not in seen:

            _add(base)

            seen.add(base.lower())

    # Filter to MEANINGFUL terms: keep strong single-word signals first (so they
    # survive the `terms[:14]` cap), then multi-word phrases, then single real
    # role/tech signals; drop generic common single words.
    strong, ordered = [], []

    for kw in terms:

        if not kw:

            continue

        words = kw.split()

        if len(words) >= 2:

            ordered.append(kw)

        elif len(words) == 1 and words[0].lower() in _SIGNAL_WORDS:

            strong.append(kw)

    terms = (strong + ordered)[:14]

    def _highlight_block(block):

        company = None

        for m in re.finditer(r'"([^"]*)"', block):

            if company is None:

                company = m.group(1)

            else:

                break

        low = block.lower()

        relevant = any(re.search(r"\b" + re.escape(k.lower()) + r"\b", low) for k in terms) or (
            company is not None and any(
                re.search(r"\b" + re.escape(k.lower()) + r"\b", company.lower()) for k in terms
            )
        )

        if relevant:

            if "important: false" in low:

                return block.replace("important: false", "important: true", 1)

            if "important: true" in low or "important:" in low:

                return block

            # Relevant entry with no important flag yet -> add important: true
            # (base entries use the #let default; insert before the closing ')' )

            return block[:-1].rstrip() + "\n  important: true\n)"

        if not relevant and "important: true" in low:

            return block.replace("important: true", "important: false", 1)

        if not relevant and "important: false" in low:

            return block

        # Not relevant with no important flag -> add important: false

        return block[:-1].rstrip() + "\n  important: false\n)"

    # Preserve the preamble before the first #entry( (set par / list directives).

    m = re.search(r"#entry\(", t)

    preamble = t[: m.start()] if m else ""

    parts_out = [preamble]

    for block in re.split(r"#entry\(", t)[1:]:

        parts_out.append("#entry(" + _highlight_block(block))

    return "".join(parts_out)


def _apply_cv_parts(base_typ, parts, jd_text=""):

    """Apply the five LLM-generated parts onto the base template text.\n\n"
    "    - quote        -> the `quote:` field
    "    - competencies -> the left (Core competencies) column of the grid
    "    - position     -> the title of the (Freelancer) entry
    "    - bullets      -> the bullet list of the (Freelancer) entry
    "    - highlight    -> flip `important:` flags for the JD-relevant companies

    """

    t = base_typ

    # 1) Quote field.

    m = re.search(r'quote: "(.*?)"', t, re.S)

    assert m, "quote field not found in base template"

    # Group 1 is the captured quote text; the replacement preserves it verbatim.
    t = t[:m.start(1)] + parts["quote"].replace("\n", " ") + t[m.end(1):]

    # 2) Core competencies left column — replace up to the 'Working Tools' header.

    left_start = t.index("#text(s, weight: \"bold\")[Core competencies]")

    right_start = t.index("#text(s, weight: \"bold\")[Working Tools]")

    header_block = t[left_start:right_start]

    first_nl = header_block.index("\n")

    prefix = header_block[:first_nl] + "\n"

    # Defensive (fix for "core competencies and the work tool in the same column"):
    # the LLM may fold the Working Tools content into the Core Competencies block.
    # If so, truncate the LLM payload at the first Working Tools header so the tools
    # land in their OWN right-hand column instead of being merged into Core
    # competencies. Only truncate when a Working Tools header actually appears inside
    # the payload (the correct case must stay intact).

    payload = parts["competencies"]

    wt_pos = payload.find("#text(s, weight: \"bold\")[Working Tools]")

    if wt_pos != -1:

        payload = payload[:wt_pos].rstrip()

    t = t[:left_start] + prefix + payload + "\n" + t[right_start:]

    # 3) Position NAME inside the (Freelancer) entry.

    m_title = re.search(r'  "(.*?)\(Freelancer\)",', t)

    assert m_title, "(Freelancer) title not found"

    title_text = parts["position"].rstrip()
    # The LLM may echo stray Typst "#entry(" prefixes or leftover header
    # labels (e.g. "POSITION NAME:") into the title string. Strip those so
    # only a clean single-line title survives (a nested "#entry(#entry("
    # is invalid Typst and would crash the compile).

    title_text = re.sub(r"#entry\(", "", title_text)

    title_text = re.sub(r"^\s*(?:POSITION\s+NAME:)?\s*", "", title_text, flags=re.I)

    title_text = re.sub(r"\s+", " ", title_text).strip()

    if title_text.endswith("(Freelancer)"):
        title_text = title_text[: -len("(Freelancer)")].rstrip()
    title_new = title_text

    if not title_new:

        title_new = m_title.group(1)

    t = t[:m_title.start()] + '  "' + title_new + ' (Freelancer)",' + t[m_title.end():]

    # 4) Bullets of the first (Freelancer) entry — replace the entry's detail
    #    array body. Use string ops (regex of literal parens is error-prone).

    fre_idx = t.find("(Freelancer)")
    assert fre_idx != -1, "(Freelancer) entry not found"

    arr_open = t.find("  [", fre_idx)
    assert arr_open != -1, "(Freelancer) detail array not found"

    arr_close = t.find("  ],", arr_open)
    assert arr_close != -1, "(Freelancer) detail array close not found"

    NL = chr(10)

    # Strip any leftover "BULLETS:" header label the LLM may echo before the
    # bullet list so the Typst array body stays a clean list.

    bullets = re.sub(r"^\s*(?:BULLETS:)?\s*", "", parts["bullets"], flags=re.I)

    bullets = re.sub(r"#entry\(", "", bullets)

    new_body = "  [" + NL + bullets.rstrip(NL) + NL + "  ],"
    t = t[:arr_open] + new_body + t[arr_close + len("  ],"):]

    # 5) Highlight — flip `important:` for the JD-relevant company names.

    highlight_set = {
        h.strip() for h in parts["highlight"].split(",") if h.strip() and h.strip().upper() != "NONE"

    }

    if highlight_set:

        def _fix_importants(block):

            m_name = re.search(r'  "[^"]*",\n  "([^"]*)",', block)

            if not m_name:

                return block

            company = m_name.group(1)

            target = "important: true" if company in highlight_set else "important: false"

            if "important: true" in block and target == "important: false":

                return block.replace("important: true", "important: false", 1)

            if "important: false" in block and target == "important: true":

                return block.replace("important: false", "important: true", 1)

            return block

        entries = re.split(r"(#entry\()", t)

        out = [entries[0]]

        for i in range(1, len(entries), 2):

            remainder = entries[i + 1] if i + 1 < len(entries) else ""

            block = entries[i] + remainder

            # block already begins with the "#entry(" delimiter captured by
            # re.split, so do NOT prepend another one (that would create the
            # invalid nested "#entry(#entry(").

            out.append(_fix_importants(block))

        t = "".join(out)

    # Backstop: make the grey highlight reflect THIS JD deterministically
    # (fixes "highlighting ... not adapt to the JD"), regardless of the LLM's
    # emitted `parts["highlight"]`.

    if jd_text:

        t = _jd_aware_highlight(t, jd_text)

    return t



def _collect(label, folders, ext, serial, on_progress=None):

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



    if isinstance(folders, str):

        folders = [folders]



    for folder in folders:

        folder = Path(folder)

        expected = folder / f"{serial}_{label}.{ext}"

        if expected.exists():

            return expected



        if folder.exists():

            # Search by substring label so LLM label variants are caught: an
            # expected "CL1.txt" also matches a file the agent wrote as "CL.txt".

            found = [f for f in folder.glob(f"*_{label}*.{ext}")]

            for f in found:

                try:

                    f.rename(expected)

                    log(f"\u21aa Renamed {f.name} -> {expected.name}")

                except OSError as exc:

                    log(f"\u26a0 could not rename {f.name}: {exc}")

            if found:

                return expected

    # No match in any candidate folder; return the expected path in the
    # first (primary) folder — which may not exist if the LLM produced nothing.

    primary = Path(folders[0]) if folders else Path(".")

    return primary / f"{serial}_{label}.{ext}"





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



def _infer_app_folder(serial, company, target_role):

    """Compute the per-application folder the LLM agent actually writes into.



    The manifest instructs the LLM to write all deliverables into a single
    per-application folder named "YYYYMMDD - Company - Position". The LLM
    interprets this literally: a BASE_DIR-level folder built from the raw date,
    company and (manifest) Target Role, WITHOUT the "Job Applications/" prefix
    and WITHOUT slug sanitisation. The pipeline's _app_folder() uses the Excel
    title and a "Job Applications/" prefix, so the two rarely match — which is
    why the pipeline's computed folder usually does not exist while the LCM's
    folder does. This helper reconstructs the LCM's exact path so the pipeline
    can find the artefacts wherever they were written.



    Returns a Path even if it does not yet exist.

    """

    ymd = serial[3:11] if len(serial) >= 11 else _today()

    return BASE_DIR / f"{ymd} - {company} - {target_role}"



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



def compile_pdf(serial, on_progress=None, app_folder=None, folders=None):

    """Compile the generated .typ CV(s) to PDF via the python-typst module.


    Searches the given candidate folders (``folders``), falling back to
    ``app_folder`` (or ``CV_DIR``) when ``folders`` is not provided. This matters
    because the CV .typ is relocated into the LCM per-application folder, which
    differs from the pipeline's app_folder.


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



    if folders is None:

        folders = [Path(app_folder) if app_folder is not None else CV_DIR]

    typ_files = sorted({p for f in folders for p in f.glob(f"{serial}_CV*.typ")})

    if not typ_files:

        _log(f"ℹ No .typ files found for {serial}; skipping PDF compilation")

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



def _typst_error_report(serial, folders=None, on_progress=None):

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



    # Search every candidate output folder (the LCM writes to its own
    # per-application folder, not necessarily CV_DIR).

    candidate = []

    for folder in (folders or [CV_DIR]):

        candidate.extend(Path(folder).glob(f"{serial}_CV*.typ"))

    typ_files = sorted(candidate)

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


def _run_cv_llm(jd_text, compact_content, target_role=None, on_progress=None):

    """Run the LLM for the five tailored CV parts and return the parsed dict.

    This is the ONLY place the LLM touches CV content: the five user-designated
    parts (Quote, Core competencies, Position name, Bullets, light-grey Highlight)
    are generated from the candidate's real experience, while the rest of the CV
    stays deterministic. Returns None on LLM/subprocess failure so the caller can
    fall back to the raw deterministic CV.

    """

    def log(msg=""):

        if on_progress:

            on_progress(msg)

        else:

            print(msg, flush=True)

    try:

        prompt = _cv_llm_prompt(jd_text, compact_content, target_role)

        stdout_raw, _stderr = _run_pi(prompt, log)

    except Exception as exc:

        log(f"⚠ CV LLM call failed: {exc}")

        return None

    return _parse_cv_llm_output(stdout_raw)


def _compile_pdf_to(typ_path, pdf_path):

    """Compile a .typ to .pdf with the Typst CLI (mirrors gen_cv_typ.py.compile_pdf)."""

    res = subprocess.run(["typst", "compile", str(typ_path), str(pdf_path)],
                         capture_output=True, text=True)

    if res.returncode != 0:

        raise RuntimeError("typst compile failed: " + res.stdout + "\n" + res.stderr)


def _generate_cv_deterministic(serial, jd_path, lcmm_folder, app_folder, on_progress=None):

    """Hybrid CV generation: deterministic scaffolding + LLM-tailored five parts.

    Per the user's design, exactly FIVE parts of the CV are generated by the LLM
    (Quote, Core competencies, Position name, Bullets, light-grey Highlight), while
    the rest of the CV — layout / styling / education / languages / interests /
    interpersonal / Working-Tools / keywords / contact block — stays DETERMINISTIC.

    Strategy: first render the deterministic CV with gen_cv_typ.py (fast, no LLM),
    then apply the LLM's five parts on top of that scaffolding via _apply_cv_parts.
    This keeps LLM interactions minimal (a single focused call) and avoids the old
    full-CV-rewrite retry storms.

    Returns the relocated .typ path (or None on generation failure).

    """

    def log(msg=""):

        if on_progress:

            on_progress(msg)

        else:

            print(msg, flush=True)

    # 1) Render the deterministic CV scaffolding via gen_cv_typ.py (no LLM).

    try:

        gen_script = Path(BASE_DIR) / "gen_cv_typ.py"

        if not gen_script.exists():

            log("⚠ gen_cv_typ.py not found; skipping CV generation")

            return None

        log("ℹ Generating deterministic CV scaffolding via gen_cv_typ.py")

        # Derive the target position TITLE from the JD so the CV's top-of-page
        # `position:` field reflects THIS specific job (rather than a stale
        # hardcoded fallback). The LLM is asked for a single concise title; if the
        # LLM path is unavailable, fall back to a best-effort keyword search of the
        # JD body. This is what makes the title "a LLM part to distinguish the job
        # position" (one of the three reported issues).
        position_title = _derive_position_title(jd_text)
        log(f"ℹ CV position title -> {position_title!r}")

        proc = subprocess.run(

            [sys.executable, str(gen_script), "--position", position_title, str(jd_path)],

            cwd=str(BASE_DIR),

            capture_output=True,

            text=True,

            timeout=900,

        )

    except FileNotFoundError as exc:

        log(f"⚠ python invocation failed: {exc}")

        return None

    except subprocess.TimeoutExpired:

        log("⚠ gen_cv_typ.py timed out")

        return None

    if proc.returncode != 0:

        log(f"⚠ gen_cv_typ.py exited {proc.returncode}:")

        print(proc.stdout)

        print(proc.stderr)

        return None

    # 2) Read the deterministic .typ as the base for the LLM part overrides.

    typ_candidates = sorted((BASE_DIR / "custom_cv").glob(f"{serial}_CV*.typ"))

    if not typ_candidates:

        log("⚠ gen_cv_typ.py produced no .typ artefact")

        return None

    base_typ = None

    for candidate in typ_candidates:

        try:

            base_typ = candidate.read_text(encoding="utf-8")

        except OSError as exc:

            log(f"⚠ could not read deterministic .typ {candidate.name}: {exc}")

            base_typ = None

            break

    if not base_typ:

        log("⚠ failed to read deterministic .typ")

        return None

    # 3) Compose compact candidate facts for the LLM prompt.

    try:

        base_cv = _base_cv_text()

        compact_content = _compact_facts(base_cv)

    except Exception as exc:

        log(f"⚠ could not compose CV facts: {exc}")

        compact_content = ""

    # Derive the target role from the manifest metadata block (same rule as
    # run_generation) so the CV-parts prompt can be tailored to it.

    target_role = ""

    try:

        manifest_path = Path(BASE_DIR) / "application_monitoring\\manifests" / (serial + ".txt")

        if manifest_path.exists():

            _m = re.search(r"^- Target Role\s*:\s*(.+)", manifest_path.read_text(encoding="utf-8"), re.M)

            target_role = _m.group(1).strip() if _m else ""

    except Exception as exc:

        log(f"⚠ could not derive target role: {exc}")

        target_role = ""

    # 4) Route the five parts through the LLM, then apply them onto the
    #    deterministic scaffolding so only these five fields become LLM-authored.

    jd_text = Path(jd_path).read_text(encoding="utf-8")

    parts = _run_cv_llm(jd_text, compact_content, target_role, on_progress=log)

    if parts is None:

        log("⚠ LLM CV-parts generation failed; using raw deterministic CV")

    else:

        log("ℹ Applying 5 LLM-tailored parts onto deterministic CV")

        try:

            base_typ = _apply_cv_parts(base_typ, parts, jd_text)

        except Exception as exc:

            log(f"⚠ could not apply LLM CV parts: {exc}")

    # 5) Write the final .typ (_CV1) and compile the PDF, then relocate into the
    #    LCM per-application folder so `_collect("CV1", ...)` finds them.

    try:

        dest_parent = Path(lcmm_folder)

        dest_parent.mkdir(parents=True, exist_ok=True)

        dest = dest_parent / f"{serial}_CV1.typ"

        Path(dest).write_text(base_typ, encoding="utf-8")

        pdf_dest = dest_parent / f"{serial}_CV1.pdf"

        _compile_pdf_to(dest, pdf_dest)

        cv_path = dest

    except Exception as exc:

        log(f"⚠ could not write/compile final CV: {exc}")

        return None

    log(f"✓ Applied 5 LLM parts -> {dest.name}")

    return cv_path

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

    # The LCM writes its deliverables into a BASE_DIR-level folder named
    # "<date> - <company> - <target_role>" (raw values, no "Job Applications/"
    # prefix). The pipeline's app_folder uses the Excel title and a prefixed,
    # slugified path, so it often does not exist while the LCM's folder does.
    # Reconstruct the LCM's path so we can find the artefacts wherever they
    # were written.
    _m = re.search(r"^- Company\s*:\s*(.+)", manifest, re.M)
    _m2 = re.search(r"^- Target Role\s*:\s*(.+)", manifest, re.M)
    lcmm_company = _m.group(1).strip() if _m else ""
    lcmm_target_role = _m2.group(1).strip() if _m2 else ""
    lcmm_folder = _infer_app_folder(serial, lcmm_company, lcmm_target_role)

    jd_text = Path(jd_path).read_text(encoding="utf-8")

    base_cv = _base_cv_text()

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

    # Compact facts (profile quote + top 3 experiences) for the LLM prompts --
    # avoids feeding the ~18 KB full CV into every prompt, which speeds up the LLM.
    if "compact_content" not in facts:

        facts["compact_content"] = _compact_facts(base_cv)



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

    gap_path = _collect("MATCH_GAP", [app_folder, lcmm_folder], "txt", serial, on_progress=log)

    produced["match_gap"] = str(gap_path)

    log(f"\u2713 Match & Gap -> {gap_path.name}")
    log(f"\u23f1 Step 1/5 Match & Gap Analysis — {_dur(t_step)}")



    # --- Step 2: Tailored CV (.typ) with self-healing ---

    log("▶ Step 2/5 Tailored CV (.typ) — deterministic (gen_cv_typ.py)")

    # Replaces the previous LLM-driven self-healing CV step. The full-CV LLM rewrite
    # was the bottleneck (huge prompt + exponential-backoff retries). gen_cv_typ.py
    # adapts only the JD-relevant elements (quote, position, keywords, competencies
    # grid, experience body) to THIS JD using the base template + the candidate's
    # REAL content -- no LLM, no retry storms. Produced artefacts are relocated
    # into the LCM per-application folder so `_collect("CV1", ...)` finds them.

    cv_path = _generate_cv_deterministic(

        serial, jd_path, lcmm_folder, app_folder, on_progress=log

    )

    if not cv_path:

        log("⚠ Deterministic CV generation failed; skipping further CV steps")

        # Do not abort the whole run -- surface the failure but continue so the user

        # still gets the other deliverables (cover letter, interview prep, dossier, RM1).

        return dict(status="partial", cv=None, produced=produced)

    produced["cv"] = str(cv_path)

    log(f"✓ CV .typ -> {cv_path.name}")

    log(f"⏱ Step 2/5 Tailored CV .typ -- {_dur(t_step)}")
    log(f"\u2713 CV .typ -> {cv_path.name}")
    log(f"\u23f1 Step 2/5 Tailored CV .typ — {_dur(t_step)}")



    # --- Step 3: Cover Letter ---

    log("▶ Step 3/5 Cover Letter…")

    _run_pi(_cover_letter_prompt(jd_text, facts), log)

    # The LLM writes text; convert it to a real Word docx inside the app folder.
    cl_docx = app_folder / f"{serial}_CL1.docx"
    cl_src = _collect("CL1", [app_folder, lcmm_folder], "docx", serial, on_progress=log)
    if not os.path.isfile(cl_docx):
        # The agent writes the cover letter as CL.txt (or CL2..CL5), not CL1.txt;
        # the substring glob in _collect matches any "_CL*" file.
        cl_txt = _collect("CL", [app_folder, lcmm_folder], "txt", serial, on_progress=log)
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
    ip_src = _collect("IP1", [app_folder, lcmm_folder], "docx", serial, on_progress=log)
    if not os.path.isfile(ip_docx):
        ip_txt = _collect("IP1", [app_folder, lcmm_folder], "txt", serial, on_progress=log)
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

    dossier_path = _collect("Doyen_DomainLeader_Argumentation", [app_folder, lcmm_folder], "docx", serial, on_progress=log)



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
    rm_src = _collect("RM1", [app_folder, lcmm_folder], "docx", serial, on_progress=log)
    if not os.path.isfile(rm_docx):
        rm_txt = _collect("RM1", [app_folder, lcmm_folder], "txt", serial, on_progress=log)
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

    # Search both candidate folders: the CV .typ lives in the LCM folder while
    # the other artefacts live in the pipeline app_folder.

    pdf_paths = compile_pdf(serial, on_progress=log, folders=[app_folder, lcmm_folder])



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
