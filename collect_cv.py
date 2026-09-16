#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CV Builder — Data Collection Engine
===================================
Beginner-friendly tool that turns a Job Description into a structured session.

  Step 1. Collects the JD via a single GUI window — just one box to
          paste the full JD text (no extra fields required).
  Step 2. Saves the JD to "2 Job description/<serial>.txt".
  Step 3. Appends a new per-session row to the Excel monitoring workbook
          with a unique serial number and structured metadata
          (date, source, status).
  Step 4. Writes an LLM prompt manifest so the running model knows exactly
          what to generate.

Run:   python collect_cv.py
Launch: double-click run_cv_builder.bat

Needs only the standard library + openpyxl (already installed).
"""

import os
import re
import ssl
import urllib.request
import datetime
import openpyxl
import threading
from openpyxl.styles import Font
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # .../MyCV
JOB_DIR = os.path.join(BASE_DIR, "2 Job description")
MON_DIR = os.path.join(BASE_DIR, "4 Application monitoring")
MANIFEST_DIR = os.path.join(MON_DIR, "manifests")
WORKBOOK = os.path.join(MON_DIR, "Application_Tracker.xlsx")

# Excel "Log" sheet columns
HEADERS = [
    "Serial Number", "Company", "Position", "Recruiter Name",
    "Date", "Source Type", "Source", "JD File", "Status",
    "Documents Generated", "Notes",
]


# ── Serial number ──────────────────────────────────────────────────────
def next_serial(existing_rows=0):
    """Return a fresh serial like CV-20250912-0007 based on existing rows."""
    today = datetime.date.today().isoformat().replace("-", "")
    seq = max(1, existing_rows + 1)
    return f"CV-{today}-{seq:04d}"


# ── URL fetch ──────────────────────────────────────────────────────────
def _is_url(value):
    """Return True if the given string looks like an http(s) URL."""
    return bool(re.match(r"^https?://", (value or "").strip(), re.I))


def _safe_remove(el):
    """Best-effort removal of a node from its parent (lxml handles namespaces)."""
    try:
        parent = el.getparent()
        if parent is not None:
            parent.remove(el)
    except Exception:
        pass


def _strip_tags_fallback(text):
    """Naive tag-stripping fallback used when lxml parsing is not available."""
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def _tree_to_text(node):
    """Collect readable text from an lxml node, normalising whitespace."""
    parts = [ln.strip() for ln in node.itertext() if ln.strip()]
    return "\n".join(parts)


def _find_main_content(doc):
    """Try to isolate the main article / job-content block via common markers."""
    selectors = [
        "//article",
        "//main",
        "//[contains(@class, 'job')]",
        "//[contains(@class, 'article')]",
        "//[contains(@class, 'post')]",
        "//[contains(@class, 'entry')]",
        "//[contains(@id, 'content')]",
        "//[contains(@id, 'main')]",
        "//[data-testid]",
    ]
    for sel in selectors:
        try:
            found = doc.xpath(sel)
        except Exception:
            found = []
        if found:
            return found[0]
    return None


def _extract_readable(raw, charset="utf-8"):
    """Turn an HTML byte body into readable plain text.

    Removes scripts/styles/iframes, then tries to isolate the main article /
    job content via common markers before extracting text. Falls back to a
    naive tag-stripper if lxml parsing is unavailable.
    """
    text = raw.decode(charset, errors="ignore")
    try:
        import lxml.html
        try:
            doc = lxml.html.fromstring(text, parser=lxml.html.HTMLParser())
        except Exception:
            return _strip_tags_fallback(text).strip()

        for tag in ("script", "style", "noscript", "iframe", "svg",
                    "template", "head", "nav", "footer", "header", "form"):
            for el in doc.xpath(" //" + tag + "//* | //" + tag):
                _safe_remove(el)

        main = _find_main_content(doc)
        target = main if main is not None else (doc.body if doc.body is not None else doc)
        body = _tree_to_text(target)
        if body and len(body.strip()) >= 40:
            return body.strip()

        return _strip_tags_fallback(text).strip()
    except Exception:
        return _strip_tags_fallback(text).strip()


def fetch_url_text(url):
    """Fetch a URL and return its readable plain-text body.

    Uses the requests library when available (robust redirect / cookie /
    header handling) and falls back to urllib otherwise. Raises RuntimeError
    with an actionable message on any failure (connection, DNS, HTTP status,
    SSL, timeout, or empty / JS-rendered content).
    """
    url = url.strip()
    if not _is_url(url):
        raise RuntimeError(f"Not a URL: {url!r}")

    requests_error = None
    try:
        import requests
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        with requests.get(url, headers=headers, timeout=30,
                          allow_redirects=True) as r:
            r.raise_for_status()
            charset = r.encoding or "utf-8"
            text = _extract_readable(r.content, charset)
            if not text or len(text.strip()) < 20:
                raise RuntimeError(
                    "URL fetch returned too little content (" + str(len(text)) +
" chars). The page may be JavaScript-rendered, "
                    "behind a consent/login wall, or require interaction."
                )
            return text.strip()
    except Exception as e:
        requests_error = e

    # Fallback: urllib (stdlib only)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (CV-Builder Collector)"}
        )
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            raw = r.read()
            charset = "utf-8"
            ct = r.headers.get("Content-Type", "")
            if "charset=" in ct:
                charset = ct.split("charset=")[1].split(";")[0]
            text = _extract_readable(raw, charset)
            if not text or len(text.strip()) < 20:
                raise RuntimeError(
                    "URL fetch returned too little content (" + str(len(text)) +
" chars). The page may be JavaScript-rendered, "
                    "behind a consent/login wall, or require interaction."
                )
            return text.strip()
    except Exception as e:
        raise RuntimeError(
            f"URL fetch failed: {requests_error or e}"
        )


# ── Excel workbook ─────────────────────────────────────────────────────
def load_workbook():
    """Return (workbook, sheet), creating a fresh tracker if none exists."""
    if os.path.exists(WORKBOOK):
        wb = openpyxl.load_workbook(WORKBOOK)
    else:
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        wb.create_sheet("Log")
    ws = wb["Log"] if "Log" in wb.sheetnames else wb.create_sheet("Log")
    return wb, ws


def read_existing_rows(ws):
    """Count data rows already present in the Log sheet."""
    if ws.max_row <= 1:
        return 0
    return sum(1 for row in range(2, ws.max_row + 1)
               if ws.cell(row=row, column=1).value is not None)


def add_session_row(ws, data):
    """Append one metadata row and bold the header on first write."""
    if ws.max_row == 0:
        for c, h in enumerate(HEADERS, start=1):
            cell = ws.cell(row=1, column=c, value=h)
            cell.font = Font(bold=True, color="FFFFFF")
    row = ws.max_row + 1
    for c, h in enumerate(HEADERS, start=1):
        ws.cell(row=row, column=c, value=data.get(h, ""))
    return row


def write_manifest(serial, company, position, recruiter, source_type, source, jtext,
                   target_role="Chief Growth & Transformation Officer"):
    """Write the LLM prompt manifest so the model knows exactly what to do."""
    os.makedirs(MANIFEST_DIR, exist_ok=True)
    safe = re.sub(r"[^\w\-.]", "_", serial)
    path = os.path.join(MANIFEST_DIR, f"{safe}.txt")
    prompt = f"""CV GENERATION TASK — Serial {serial}
============================================

CONTEXT
You are acting as a principal tech recruiter and executive resume strategist.
The candidate is applying for a specific position. Align his updated CV with the
target Job Description to maximize his match rate while STRICTLY adhering to
100% TRUTHFULNESS and factual accuracy.
Never invent experience, fake metrics, or exaggerate his background.

SESSION METADATA
- Serial Number : {serial}
- Company       : {company if company else 'N/A'}
- Position      : {position if position else 'N/A'}
- Recruiter     : {recruiter if recruiter else 'N/A'}
- Source Type   : {source_type}
- Source        : {source}
- Target Role   : {target_role}

INPUT: The Job Description is appended below this block. Use ONLY the facts
present in the candidate's base CV (1 Source/SONG Ernest - CV v1.typ) plus the JD.

==== JOB DESCRIPTION ====
{jtext}
==== END JOB DESCRIPTION ====

ALL deliverables below must be written as a SINGLE set into the one per-application
folder for this job (named "YYYYMMDD - Company - Position"). Write ONE of each:

1) MATCH & GAP ANALYSIS  ->  filename "{serial}_MATCH_GAP.txt"
   Create a simple comparative breakdown:
     - Direct Matches : skills/tools/experience that directly match the JD.
     - Transferable   : related experience that fulfills implicit JD requirements.
     - Critical Gaps  : required skills/qualifications missing from the CV.

2) 1 CUSTOM CV         ->  filename "{serial}_CV1.typ"
   Rewrite bullet points using exact JD keyword phrasing, ONLY where real
   experience supports it. Restructure the summary into a high-impact
   "Value Proposition" answering the JD's primary business pain point.
   Every bullet = Action Verb + Context/Tech + Metric or Outcome, without
   inflating the real role. Produce EXACTLY ONE tailored CV (not several versions).
   Keep the visual formatting of SONG Ernest - CV v1 (only change the content).
   Position-name preservation: keep each professional-experience job title VERBATIM;
   the ONLY change allowed is stripping a trailing "(freelance)" tag. Otherwise
   the title must remain identical.

3) 1 COVER LETTER       ->  filename "{serial}_CL1.txt"
   Draft ONE concise, high-converting cover letter (under 250 words) that bridges
   the candidate's background to the JD's top 3 requirements. Include an honest,
   proactive statement on how his unique perspective covers any minor skill gaps,
   without apologizing for them.

4) 1 INTERVIEW PREP     ->  filename "{serial}_IP1.txt"
   Provide ONE interview-prep document that groups STAR-based (Situation, Task,
   Action, Result) Q&A outlines based strictly on the candidate's real CV experiences.

OUTPUT: Confirm each file was written and list the file paths.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(prompt)
    return path


# ── GUI ────────────────────────────────────────────────────────────────
class SessionWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("CV Builder — Session")
        self.root.geometry("960x680")
        self.root.configure(bg="#f4f4f4")
        self.meta = {"Company": "", "Position": "", "Recruiter Name": ""}
        self.source_type = "Job Description (text)"
        self.source_value = ""
        self._build_page()

    def _build_page(self):
        # Single clean page: just one box to paste (or load) the Job Description.
        p = tk.Frame(self.root, bg="#f4f4f4", padx=20, pady=16)
        p.pack(fill="both", expand=True)
        tk.Label(p, text="Paste the Job Description below:", bg="#f4f4f4",
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(p, text="No other fields needed — just paste the full JD text, or load a .txt file.",
                 bg="#f4f4f4", font=("Segoe UI", 8), fg="#555").grid(row=1, column=0, sticky="w", pady=(4, 10))
        # Compact status footer (quick one-line status)
        self.status_label = tk.Label(p, bg="#f4f4f4", fg="#c0392b",
                                     font=("Segoe UI", 8), anchor="w")
        self.status_label.grid(row=6, column=0, sticky="w")

        # Live progress console — a small scrollable log so the user can see
        # every step of the collection pipeline as it happens.
        log_frame = tk.Frame(p, bg="#f4f4f4")
        log_frame.grid(row=7, column=0, sticky="nw", pady=4)
        self._log_area = tk.Text(log_frame, height=8, width=92, bg="#1e1e1e",
                                 fg="#e6e6e6", font=("Consolas", 8),
                                 wrap="word", insertbackground="#000")
        log_sb = tk.Scrollbar(log_frame, command=self._log_area.yview)
        log_sb.pack(side="right", fill="y")
        self._log_area.pack(side="left", fill="both", expand=True)
        self._log_area.configure(state="disabled")

        # Tall, scrollable text box — no practical paste limit
        txt_frame = tk.Frame(p, bg="#f4f4f4")
        txt_frame.grid(row=2, column=0, pady=4, sticky="ew")
        self._text = tk.Text(txt_frame, height=24, width=90, bg="#fff", fg="#111",
                             wrap="word")
        sb = tk.Scrollbar(txt_frame, command=self._text.yview)
        sb.pack(side="right", fill="y")
        self._text.pack(side="left", fill="both", expand=True)
        # Bind paste so Ctrl+C/V + middle-click always land in the box
        for binding in ("<Control-v>", "<Control-V>", "<Alt-v>", "<Alt-V>"):
            self._text.bind(binding, self._on_paste)
        tk.Button(p, text="Choose file…", command=self._load_file, width=14,
                  font=("Segoe UI", 9)).grid(row=3, column=0, sticky="w")

        def done():
            # Collect the JD, then RUN the collection pipeline BEFORE closing the
            # window. The window must stay alive while _run_pipeline runs, because
            # the pipeline reports progress/errors through Tk message boxes. If the
            # window were destroyed first (previous behaviour), _run_pipeline would
            # crash with "TclError: application has been destroyed" and the user
            # would see nothing created.
            try:
                raw = self._text.get("1.0", "end").strip()
                if not raw:
                    messagebox.showinfo("CV Builder", "No input received — please paste the Job Description.")
                    return
                # Auto-detect URLs: fetch + parse the page, otherwise use pasted text.
                self.source_value, self.source_type = self._resolve_jtext(raw)
                # Run the pipeline; only close the window once it has succeeded.
                ok = self._run_pipeline_from_ui()
                if ok:
                    _safe_destroy(self.root)
            except Exception as e:
                # Any unexpected error keeps the window open so the user can see it.
                self._progress(f"\u2717 Unexpected error: {e}")
                messagebox.showerror("CV Builder", f"Something went wrong:\n{e}")

    def _resolve_jtext(self, value):
        """Return (jtext, source_type).

        If `value` is a URL, fetch + parse the page and mark the source as
        'URL'; otherwise return the pasted text as-is with its source type.
        """
        if _is_url(value):
            text = fetch_url_text(value)
            return text, "URL"
        return value, "Job Description (text)"

        def _run_pipeline_from_ui(self):
            """Wrapper used by the OK button.

            Runs the collection pipeline in a background thread so the GUI stays
            responsive, and pumps a live progress log so the user can see each
            step. Returns True on success, False on failure. The window is kept
            open on failure so the user can see what went wrong.
            """
            self._set_status("Collecting… please wait")
            self._log("CV Builder — Data Collection Engine")
            self._log("=" * 44)

            state = {"kind": None, "payload": None}
            lock = threading.Lock()

            def report(msg):
                with lock:
                    state["kind"] = "progress"
                    state["payload"] = msg

            def worker():
                try:
                    self._run_pipeline(self.source_value, self.source_type, on_progress=report)
                    with lock:
                        state["kind"] = "success"
                        state["payload"] = None
                except Exception as e:  # noqa: BLE001
                    with lock:
                        state["kind"] = "failure"
                        state["payload"] = e

            t = threading.Thread(target=worker, daemon=True)
            t.start()

            def poll():
                with lock:
                    kind = state["kind"]
                    payload = state["payload"]
                if kind == "progress":
                    self._log(payload)
                    self.root.after(50, poll)
                elif kind == "success":
                    self._log("\u2713 Collection complete")
                    self._set_status("\u2713 Collection complete")
                    messagebox.showinfo(
                        "CV Builder — Success",
                        "Session collected successfully!\n\n"
                        "The Job Description has been saved and the Excel tracker updated.\n"
                        "Next: run the LLM generation to produce the tailored documents.",
                    )
                    _safe_destroy(self.root)
                elif kind == "failure":
                    e = payload
                    self._log(f"\u2717 Collection failed: {e}")
                    self._set_status(f"\u2717 Collection failed")
                    messagebox.showerror(
                        "CV Builder — Error",
                        f"Collection failed:\n{e}\n\n(See the progress area above for details.)",
                    )
                elif kind is None:
                    self.root.after(50, poll)

            self.root.after(50, poll)
            return True

        def _progress(self, msg):
            """Append a line to the live progress console (GUI-only helper)."""
            self._log(msg)

        tk.Button(p, text="OK — Run process", command=done, width=16,
                  font=("Segoe UI", 9)).grid(row=5, column=0, sticky="w")
        tk.Button(p, text="Cancel", command=lambda: _safe_destroy(self.root), width=10,
                  font=("Segoe UI", 9)).grid(row=5, column=1, sticky="e", padx=20)

        # Make sure the window + text box are active so paste lands here
        self.root.deiconify()
        self.root.focus_force()
        self._text.focus_set()
        self.root.after(50, lambda: self.root.focus_force())

    def _log(self, msg=""):
        """Append a line to the live progress console (GUI-only helper)."""
        try:
            self._log_area.configure(state="normal")
            self._log_area.insert("end", f"{msg}\n" if msg else "\n")
            self._log_area.see("end")
            self._log_area.configure(state="disabled")
        except Exception:
            pass

    def _set_status(self, msg):
        """Update the compact status footer (GUI-only helper)."""
        self.status_label.configure(text=msg)

    def _on_paste(self, event=None):
        """Read the Windows clipboard directly and insert it. Works even when
        the default Paste binding misbehaves."""
        try:
            data = self.root.clipboard_get()
            if data and data.strip():
                self._text.insert("end", data)
                self.status_label.configure(text="Pasted from clipboard ✓")
            else:
                self.status_label.configure(text="Clipboard is empty.")
        except tk.TclError:
            self.status_label.configure(text="Could not read clipboard — use 'Choose file…'.")
        return "break"  # stop the default (broken) paste handling

    def _load_file(self):
        """Open a file dialog and load the chosen .txt into the text box."""
        path = filedialog.askopenfilename(
            title="Choose a file containing the Job Description",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self._text.delete("1.0", "end")
            self._text.insert("end", content)
            self.status_label.configure(text=f"Loaded: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("CV Builder", f"Could not read file:\n{e}")

    def run(self):
        self.root.mainloop()


def _safe_destroy(root):
    """Destroy the window only if it still exists (avoids double-destroy errors).

    The Cancel / OK buttons already call root.destroy() themselves; if we then
    call root.destroy() again here we get
    "can't invoke 'destroy' command: application has been destroyed".
    We also guard winfo_exists() itself, since it raises on an already-destroyed app.
    """
    try:
        if root.winfo_exists():
            root.destroy()
    except tk.TclError:
        pass


# ── Main ───────────────────────────────────────────────────────────────
def extract_position(jd):
    """Best-effort extraction of the target job title from the JD text.

    Two signals, in order:
      1. A title following a strong lead-in ("...looking for an experienced <TITLE>...").
      2. The most-repeated Title-Case standalone line (the highlighted title is repeated
 throughout the JD body).
    Falls back to an empty string when no title-like candidate is found (e.g. old French
    JDs with no clean English title). LinkedIn UI boilerplate is filtered out.
    """
    _NOISE = {
        "view company", "show more", "from freelancer to permanent roles",
        "recommended", "recommended by linkedin", "linkedin members",
        "recommendations", "how to become",
    }
    m = re.search(
        r"looking for (?:an|a|an experienced)\s+([A-Z][A-Za-zÀ-ÿ/&]{5,80}?)\s+(?:to help|and this|you|we|/|,|\.)",
        jd, re.IGNORECASE,
    )
    if m:
        return " ".join(m.group(1).split())
    counts = {}
    for line in jd.splitlines():
        s = line.strip()
        if s and not s.endswith((".", "?", "!")) and re.match(r"^[A-Z][A-Za-zÀ-ÿ &/\-]{3,}$", s):
            if s.lower() not in _NOISE:
                counts[s] = counts.get(s, 0) + 1
    if counts and max(counts.values()) >= 2:
        return max(counts, key=counts.get)
    return ""


def _extract_company(jd):
    """Best-effort extraction of the target company from the JD text.

    Looks for a proper-noun phrase after lead-ins like "chez / at / de / at the".
    Returns an empty string when no clean candidate is found.
    """
    cm = re.search(
        r"(?:chez|at|de)\s+([A-Z][A-ZÀ-ÿ\s]{3,40})",
        jd, re.IGNORECASE,
    )
    if cm:
        company = " ".join(w for w in cm.group(1).split() if w.strip())
        # normalise to Title Case
        company = " ".join(w[:1].upper() + w[1:] for w in company.split())
        return company.strip()
    return ""


def _run_pipeline(jtext, source_type, source_value=None, on_progress=None):
    """Shared processing pipeline used by both GUI and CLI entry points.

    If `on_progress` is supplied it is called with progress strings (GUI mode);
    otherwise progress is printed to stdout (CLI mode). Errors are raised so the
    caller can report them via message boxes.
    """
    def log(msg=""):
        if on_progress:
            on_progress(msg)
        else:
            print(msg)

    log("CV Builder — Data Collection Engine")
    log("=" * 44)

    # 1. Validate
    if len(jtext) < 20:
        raise RuntimeError("Job description too short — please paste the full text.")

    # 3. Serial + workbook + save JD + manifest
    wb, ws = load_workbook()
    n = read_existing_rows(ws)
    serial = next_serial(n)
    today = datetime.date.today().isoformat()

    os.makedirs(JOB_DIR, exist_ok=True)
    safe = re.sub(r"[^\w\-.]", "_", serial)
    jd_path = os.path.join(JOB_DIR, f"{safe}.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(jtext)

    manifest = write_manifest(
        serial=serial,
        company=company,
        position=position,
        recruiter="",
        source_type=source_type,
        source=(source_value if source_type == "URL" else "(pasted text)"),
        jtext=jtext,
    )

    # 4. Update Excel row
    position = extract_position(jtext)
    company = _extract_company(jtext)

    data = {
        "Serial Number": serial,
        "Company": company,
        "Position": position,
        "Recruiter Name": "",
        "Date": today,
        "Source Type": source_type,
        "Source": (source_value if source_type == "URL" else "(pasted text)"),
        "JD File": os.path.relpath(jd_path, BASE_DIR),
        "Status": "JD collected — awaiting document generation",
        "Notes": f"Manifest: {os.path.relpath(manifest, BASE_DIR)}",
    }
    row = add_session_row(ws, data)
    wb.save(WORKBOOK)

    log(f"Serial      {serial}")
    log(f"JD file     2 Job description/{safe}.txt")
    log(f"Manifest    {os.path.relpath(manifest, BASE_DIR)}")
    log(f"Excel log   Application_Tracker.xlsx -> row {row}")
    return {
        "serial": serial,
        "jd_path": jd_path,
        "manifest": manifest,
        "row": row,
        "title": position,
        "company": company,
    }


if __name__ == "__main__":
    import sys
    # Non-interactive mode: pass --file "path/to/jd.txt" to skip the GUI and
    # feed the file content directly into the pipeline (handy for tests).
    argv = sys.argv[1:]
    file_arg = None
    for i, a in enumerate(argv):
        if a.startswith("--file"):
            # Support both '--file value' and '--file=value'
            if "=" in a:
                file_arg = a.split("=", 1)[1]
            elif i + 1 < len(argv):
                file_arg = argv[i + 1]
            break
    if file_arg:
        path = file_arg.strip().strip('"')
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                jtext = f.read()
            source_type = "Job Description (file)"
            source_value = jtext
        else:
            print(f"[error] file not found: {path}")
            sys.exit(1)
    else:
        # Interactive GUI mode (existing behaviour)
        root = tk.Tk()
        win = SessionWindow(root)
        win.run()

        if not win.source_value:
            messagebox.showinfo("CV Builder", "No input received — cancelled.")
            _safe_destroy(root)
            sys.exit(0)
        # Input was already resolved (auto-fetched if it was a URL) by done().
        jtext = win.source_value
        source_type = win.source_type
        source_value = jtext

    _run_pipeline(jtext=jtext, source_type=source_type, source_value=source_value)



