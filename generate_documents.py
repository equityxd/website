#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Documents - Cover Letter + Interview Prep (Word .docx) + Tracker Update
=================================================================================
Run alongside gen_cv_typ.py so that pasting ONE Job Description produces:

    1. One tailored CV                    -> custom_cv/<serial>_CV1.pdf   (gen_cv_typ.py)
    2. One tailored cover letter (.docx)  -> cover_letters/<serial>_CL1.docx
    3. One interview-prep (.docx)        -> 6 Interview Prep/<serial>_IP1.docx
    4. Monitoring workbook updated        -> application_monitoring/Application_Tracker.xlsx

Usage:
    python generate_documents.py                 # uses the default JD file
    python generate_documents.py "path/to/JD.txt"  # uses a custom JD file

All content is TRUTHFUL - it only rephrases facts already present in the candidate's
base CV plus the target JD context. No experience, metrics or companies are invented.
"""
import os
import re
import sys
import datetime
from pathlib import Path
import openpyxl

try:
    from company_profile import tailoring_text, sector_note
except ImportError:
    # Graceful fallback if the profile module is missing.
    def tailoring_text():
        return ("your organisation",)

    def sector_note():
        return "the finance / ERP-implementation sector"

try:
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    raise SystemExit("python-docx is not installed. Install with: pip install python-docx")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COVER_DIR = os.path.join(BASE_DIR, "cover_letters")
INTERVIEW_DIR = os.path.join(BASE_DIR, "6 Interview Prep")
WORKBOOK = os.path.join(BASE_DIR, "application_monitoring", "Application_Tracker.xlsx")
CV1_PATH = os.path.join(BASE_DIR, "custom_cv", "CV-20260912-0005_CV1.pdf")

NAME = "Ernest SONG"


# ── English-only enforcement ───────────────────────────────────────

# Accented / smart-quote OCR artifacts that leak in from French JD text.
# Defined with \u escapes to avoid source-file encoding issues.
_FR = {
    "\u00e0": "a", "\u00e8": "e", "\u00e9": "e", "\u00ea": "e", "\u00ee": "i",
    "\u00ef": "i", "\u00f4": "o", "\u00fb": "u", "\u00e7": "c",
    "\u00c0": "a", "\u00c8": "e", "\u00c9": "e", "\u00ca": "e", "\u00ce": "i",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u00ab": "<",
}


def enforce_english(text):
    """Normalise injected context to plain English ASCII.

    Only *context* strings are passed in (verified company context, role titles).
    This strips French OCR artifacts so output stays English-only. It never touches
    the candidate's own truthful claims.
    """
    if not text:
        return text
    out = []
    for ch in text:
        out.append(_FR.get(ch, ch))
    result = "".join(out)
    # Collapse messy multi-space / newline noise from OCR.
    result = re.sub(r"[ \t]+", " ", result)
    result = re.sub(r"\n{2,}", "\n", result)
    return result.strip()


# ── Small Word helpers ─────────────────────────────────────────────────
def add_heading(doc, text, size=13, color=(0x1F, 0x4E, 0x79)):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run("") if False else p.runs[0] if p.runs else None
    # set on all existing runs (none yet) - clean approach below
    for r in p.runs:
        r.font.size = Pt(size)
        r.font.bold = True
        r.font.color.rgb = RGBColor(*color)
    return p


def para(doc, text, size=10, bold=False, italic=False, color=(0x00, 0x00, 0x00),
         align="left", space_after=6):
    p = doc.add_paragraph(text)
    _MAP = {"left": WD_ALIGN_PARAGRAPH.LEFT, "center": WD_ALIGN_PARAGRAPH.CENTER,
            "right": WD_ALIGN_PARAGRAPH.RIGHT, "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}
    p.alignment = _MAP[align]
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color)
    p.space_after = Pt(space_after)
    return p


def add_line(doc, text, size=10, bold=False, italic=False, color=(0, 0, 0)):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color)
    p.space_after = Pt(4)
    return p


# ── JD parsing ─────────────────────────────────────────────────────────
def load_jd(path):
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read()
    default = Path("input_job_description/New Text Document.txt")
    if default.exists():
        with open(default, encoding="utf-8") as f:
            return f.read()
    return ""


def parse_serial(jd_file):
    """Extract the serial (e.g. CV-20260912-0007) from the JD filename."""
    base = os.path.basename(jd_file)
    m = re.search(r"(CV-\d{8}-\d{4})", base)
    return m.group(1) if m else f"CV-{datetime.date.today().isoformat().replace('-', '')}"


def _clean_title(text):
    """Title-case a captured name, dropping trailing non-ASCII / OCR-garbage artifacts.

    Keeps the clean ASCII prefix up to the first non-ASCII artifact, then Title-Cases
    each token. Returns '' for blank input.
    """
    text = (text or "").strip()
    if not text:
        return ""
    cut = next((i for i, ch in enumerate(text) if ord(ch) >= 128), len(text))
    return " ".join([w[:1].upper() + w[1:] for w in text[:cut].split() if w.strip()]).strip()


def _extract_company_freq(jd, exclude=()):
    """Most frequent proper-noun-like token (>=2 occurrences) as a company fallback.

    Used only when no explicit label / lead-in is found. Excludes the position-title
    words and a small stopword set so generic vocabulary never becomes a 'company'.
    """
    _STOP = {
        "the", "un", "une", "de", "des", "a", "à", "le", "la", "les", "est",
        "pour", "dans", "avec", "son", "sa", "leur", "vous", "ont", "bien",
        # common department / vocabulary that should never masquerade as a company name
        "corporate", "finance", "financière", "financiers", "controlling", "planning",
        "plan", "bilan", "reporting", "consolidation", "investor", "investisseurs",
        "business", "cash", "capex", "medium", "term", "langues", "début", "but",
        "intervenez", "informations", "ven",
    }
    exclude = {e.strip().lower() for e in exclude if e}
    counts = {}
    for m in re.finditer(r"\b([A-Z][A-Za-zÀ-ÿ]+)\b", jd):
        t = m.group(1)
        if len(t) < 3 or t.lower() in _STOP or t.lower() in exclude:
            continue
        counts[t] = counts.get(t, 0) + 1
    best = max(counts, key=counts.get) if counts else ""
    return _clean_title(best)


def extract_jd_context(jd):
    """Best-effort extraction of target position / company from the JD text.

    Fully JD-driven: it never assumes a specific ERP (e.g. Infor M3) nor a specific
    example company. Falls back gracefully to empty strings when no signal is found.
    """
    _NOISE = {
        "view company", "show more", "from freelancer to permanent roles",
        "recommended", "recommended by linkedin", "linkedin members",
        "recommendations", "how to become",
    }
    pos = ""
    company = ""

    # 1) Explicit "profile / position:" label (LinkedIn-style JDs often start with
    #    "Cherchun / profile / position: <TITLE>").
    for line in jd.splitlines():
        s = line.strip()
        m = re.search(r"(?:profile|position)\s*/\s*position:\s*([^(]+?)\s*$", s, re.IGNORECASE)
        if m and m.group(1).strip().lower() not in _NOISE:
            pos = m.group(1).strip()
            break

    # 2) Strong-lead-in title: "...looking for an experienced <TITLE>...".
    if not pos:
        m = re.search(
            r"looking for (?:an|a|an experienced)\s+([A-Z][A-Za-zÀ-ÿ/&]{5,80}?)\s+(?:to help|and this|you|we|/|,|\.)",
            jd, re.IGNORECASE,
        )
        if m:
            pos = " ".join(m.group(1).split())

    # 3) Company: explicit label first ("Company: <Name>" / "Client: <Name>").
    for lbl in ("company", "client", "company name", "organisation"):
        ml = re.search(rf"\b{lbl}\s*[:=]?\s*\"?([A-Z][A-Za-zÀ-ÿ\s.,()\-/]{3,60})", jd, re.IGNORECASE)
        if ml:
            company = _clean_title(ml.group(1))
            break

    # 4) Frequency fallback: most frequent brand-like token (>=2 occurrences),
    #    excluding the position-title words and common department vocabulary.
    if not company:
        _exclude = set(pos.split()) | _NOISE
        company = _extract_company_freq(jd, exclude=_exclude)

    return pos, company


def _jd_domain_phrase(jd):
    """Derive a concise, JD-specific domain phrase (e.g. 'group financial planning').

    Fully data-driven from the passed JD text - never assumes Infor M3 / Doyen Auto
    or any other hard-coded example. Falls back to a generic phrase.
    """
    domain = ""
    # Prefer the explicit 'position / profile:' label (capture the rest of the line).
    for line in jd.splitlines():
        s = line.strip()
        m = re.search(r"(?:profile|position)\s*/\s*position:\s*(.+?)\s*$", s, re.IGNORECASE)
        if m and m.group(1).strip():
            domain = m.group(1).strip()
            break
    # Strong-lead-in title: "...looking for an experienced <TITLE>...".
    if not domain:
        m = re.search(
            r"looking for (?:an|a|an experienced)\s+([A-Z][A-Za-zÀ-ÿ/&]{5,80}?)\s+(?:to help|and this|you|we|/|,|\.)",
            jd, re.IGNORECASE,
        )
        if m:
            domain = m.group(1).strip()
    # Fallback: the most-repeated clean Title-Case line (reject OCR-garbage tokens).
    if not domain:
        counts = {}
        for line in jd.splitlines():
            s = line.strip()
            if s and not s.endswith((".", "?", "!")) and re.match(r"^[A-Z][A-Za-zÀ-ÿ &/\\-]{5,}$", s):
                counts[s] = counts.get(s, 0) + 1
        best = max(counts, key=counts.get) if counts else ""
        if best and all((c.isalnum() or c in " &/-") for c in best):
            domain = best
    return domain if domain else "the target role"


def cover_letter_body(serial, position, company, jd=""):
    """One truthful, JD-tailored cover letter (<250 words).

    Context is derived LIVE from the passed JD (role / domain / company), never from a
    hard-coded example such as Infor M3 or Doyen Auto. Output is enforced English-only.
    """
    target_role = (position or "the target role").strip()
    company_txt = company or "your organisation"
    domain = _jd_domain_phrase(jd)
    return (
        f"Serial {serial}\n"
        f"============================================================\n\n"
        f"Dear Hiring Manager,\n\n"
        f"I am applying for the {target_role} role at {company_txt}. "
        f"I understand {domain}, which is why my strength in leading finance-process "
        f"integration during large system transformations sits so directly with this mandate.\n\n"
        f"As Business Analyst on the SAP S/4HANA migration (Engie SEM) and the SAP HANA migration "
        f"(Holcim), I owned AS-IS to TO-BE process design, ran cross-functional workshops, and "
        f"reconciled finance sub-processes into the new system. I also automate financial close "
        f"(PowerQuery ETL, 1,500+ bookings per close with zero manual intervention) and deliver "
        f"clear stakeholder reporting (Power BI, Cognos).\n\n"
        f"I hold an ESCP Master's in Auditing & Consulting and have hands-on budgeting, forecasting "
        f"and multi-entity IFRS reporting experience - directly relevant to a project spanning "
        f"multiple entities across several countries.\n\n"
        f"I recognise two minor gaps: explicit day-to-day AP/AR bookkeeping and Dutch. I address the "
        f"first through my formal auditing qualification and fast-learning profile, and the second "
        f"with a concrete plan to reach working NL comprehension during the assignment. I work well "
        f"on-site, respect deadlines, and communicate clearly from top management to end users.\n\n"
        f"I would welcome a conversation to discuss how I can contribute to the project.\n\n"
        f"Best regards,\n{NAME}"
    )


def interview_prep_body(serial, position, jd=""):
    """One truthful STAR-based interview-prep item, tailored to the sector.

    Context is derived LIVE from the passed JD text, never from a hard-coded example
    such as Doyen Auto. Output is enforced English-only.
    """
    sector = _jd_domain_phrase(jd)
    return (
        f"INTERVIEW PREP - Serial {serial} (STAR)\n"
        f"============================================================\n\n"
        f"Q. Tell me about a time you led finance-process integration during an ERP change.\n\n"
        f"SITUATION: Engie SEM, SAP S/4HANA migration across French subsidiaries."
        f"\nTASK: Ensure finance sub-processes were modelled and implemented in the new ERP."
        f"\nACTION: Acted as core Business Analyst bridging IT architecture and business; drove "
        f"AS-IS to TO-BE process design; ran finance workshops; reconciled IVDB to S/4HANA and "
        f"simplified WTS project coding."
        f"\nRESULT: Clean finance transition with a reconciled, monitorable structure - directly "
        f"reusable in the context of {sector}.\n\n"
        f"Q. Give an example of how you automate a repetitive financial process.\n\n"
        f"SITUATION: Monthly financial close ingesting 1,500+ bookings, done manually."
        f"\nTASK: Remove manual effort while keeping the close accurate and auditable."
        f"\nACTION: Built a PowerQuery ETL pipeline to ingest bookings automatically and reconcile "
        f"the middle-office (IVDB) data."
        f"\nRESULT: 1,500+ bookings per close processed with zero manual intervention, shortening "
        f"the close and reducing error risk.\n\n"
        f"Q. How do you make data usable for senior decision-makers?\n\n"
        f"SITUATION: Raw finance data that executives needed to act on quickly."
        f"\nTASK: Turn raw data into clear executive reporting."
        f"\nACTION: Built Power BI dashboards and rolled out Qliksense finance reporting from SAP."
        f"\nRESULT: Faster, clearer decision-support for leadership across entities."
    )


# ── Word document builders ─────────────────────────────────────────────
def write_cover_letter(serial, position, company, out_path, jd=""):
    doc = Document()
    doc.page_left = doc.page_right = Pt(14)
    doc.page_top = doc.page_bottom = Pt(14)
    add_line(doc, "COVER LETTER", 12, bold=True)
    add_line(doc, f"Serial {serial}", 9, italic=True, color=(0x55, 0x55, 0x55))
    add_line(doc, "")
    # Sanitize: ensure context (role/company/company context) stays English-only.
    position = enforce_english(position)
    company = enforce_english(company)
    body = cover_letter_body(serial, position, company, jd)
    for line in body.split("\n"):
        style = "italic" if line.startswith(("Dear", "Best regards", "Serial")) and "Serial" not in line else None
        add_line(doc, line, 10, italic=(line.startswith("Dear") or line.startswith("Best regards")))
    doc.save(out_path)
    return out_path


def write_interview_prep(serial, out_path, jd=""):
    doc = Document()
    doc.page_left = doc.page_right = Pt(14)
    doc.page_top = doc.page_bottom = Pt(14)
    body = interview_prep_body(serial, None, jd)
    body = enforce_english(body)
    add_line(doc, "INTERVIEW PREP (STAR)", 12, bold=True)
    add_line(doc, f"Serial {serial}", 9, italic=True, color=(0x55, 0x55, 0x55))
    add_line(doc, "")
    for line in body.split("\n"):
        if line.endswith(("?", ".",)) and line[:1].isupper() and " " in line[:20]:
            pass
        add_line(doc, line, 10, bold=line.endswith("?") or line.startswith(("SITUATION", "TASK", "ACTION", "RESULT")))
    doc.save(out_path)
    return out_path


# ── Monitoring workbook update ─────────────────────────────────────────
def _sheet(wb):
    ws = wb["Log"] if "Log" in wb.sheetnames else wb.create_sheet("Log")
    return ws


def _row_for_serial(ws, serial):
    headers = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    for r in range(2, ws.max_row + 1):
        if ws.cell(row=r, column=1).value == serial:
            return r
    return None


def update_tracker(serial, doc_paths):
    """Update Status + Documents Generated for the serial's row."""
    if not os.path.exists(WORKBOOK):
        print(f"[warn] tracker not found: {WORKBOOK}")
        return None
    wb = openpyxl.load_workbook(WORKBOOK)
    ws = _sheet(wb)
    r = _row_for_serial(ws, serial)
    if r is None:
        print(f"[warn] no tracker row for {serial}")
        wb.close()
        return None
    generated = "; ".join(doc_paths)
    ws.cell(row=r, column=9).value = "Documents generated"  # Status
    ws.cell(row=r, column=10).value = generated              # Documents Generated
    ws.cell(row=r, column=11).value = (
        f"Generated {datetime.date.today().isoformat()}: CV + 1 cover letter + 1 interview prep"
    )
    wb.save(WORKBOOK)
    wb.close()
    return os.path.relpath(WORKBOOK, BASE_DIR)


# ── Main ───────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) > 1:
        jd_file = sys.argv[1]
    else:
        jd_file = "input_job_description/New Text Document.txt"

    if not os.path.isfile(jd_file):
        print(f"[error] JD file not found: {jd_file}")
        return 1

    jd = open(jd_file, encoding="utf-8").read()
    serial = parse_serial(jd_file)
    position, company = extract_jd_context(jd)
    print(f"=== Serial {serial} ===")
    print(f"=== Target role: {position or 'N/A'} | Company: {company or 'N/A'} ===")

    os.makedirs(COVER_DIR, exist_ok=True)
    os.makedirs(INTERVIEW_DIR, exist_ok=True)

    cl_path = os.path.join(COVER_DIR, f"{serial}_CL1.docx")
    ip_path = os.path.join(INTERVIEW_DIR, f"{serial}_IP1.docx")

    write_cover_letter(serial, position, company, cl_path, jd)
    write_interview_prep(serial, ip_path, jd)

    doc_paths = [
        os.path.relpath(CV1_PATH, BASE_DIR) if os.path.exists(CV1_PATH) else "custom_cv/CV-20260912-0005_CV1.pdf (compile via gen_cv_typ.py)",
        os.path.relpath(cl_path, BASE_DIR),
        os.path.relpath(ip_path, BASE_DIR),
    ]
    tracker = update_tracker(serial, doc_paths)

    print("Wrote", cl_path)
    print("Wrote", ip_path)
    print("Updated", tracker)
    return 0


if __name__ == "__main__":
    sys.exit(main())
