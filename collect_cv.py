#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CV Builder — Data Collection Engine
===================================
Beginner-friendly tool that turns a Job Description into a structured session.

  Step 1. Collects the JD (pasted text OR a URL) via a small GUI window.
  Step 2. Saves the JD to "2 Job description/<serial>.txt".
  Step 3. Appends a new per-session row to the Excel monitoring workbook
          with a unique serial number and structured metadata
          (recruiter, company, date, source, status).
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
def fetch_url_text(url):
    """Fetch a URL and return its plain-text body (best-effort)."""
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (CV-Builder Collector)"}
    )
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            raw = r.read()
            charset = "utf-8"
            ct = r.headers.get("Content-Type", "")
            if "charset=" in ct:
                charset = ct.split("charset=")[1].split(";")[0]
    except Exception as e:
        raise RuntimeError(f"URL fetch failed: {e}")
    text = raw.decode(charset, errors="ignore")
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


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

EXECUTE THE FOLLOWING AND WRITE EACH DELIVERABLE TO ITS FOLDER:

1) MATCH & GAP ANALYSIS  ->  folder "2 Job description"
   Create a simple comparative breakdown:
     - Direct Matches : skills/tools/experience that directly match the JD.
     - Transferable   : related experience that fulfills implicit JD requirements.
     - Critical Gaps  : required skills/qualifications missing from the CV.

2) 3 CUSTOM CVs       ->  folder "3 Custom CV"
   Rewrite bullet points using exact JD keyword phrasing, ONLY where real
   experience supports it. Restructure the summary into a high-impact
   "Value Proposition" answering the JD's primary business pain point.
   Every bullet = Action Verb + Context/Tech + Metric or Outcome, without
   inflating the real role. Produce 3 distinct tailored versions.
   Keep the visual formatting of SONG Ernest - CV v1 (only change the content).

3) 5 CUSTOM COVER LETTERS ->  folder "5 Custom Cover Letter"
   Draft 5 concise, high-converting cover letters (under 250 words each)
   that bridge the candidate's background to the JD's top 3 requirements.
   Include an honest, proactive statement on how his unique perspective
   covers any minor skill gaps, without apologizing for them.

4) 6 INTERVIEW PREP    ->  folder "6 Interview Prep"
   Provide 6 targeted behavioral interview questions likely based on this JD,
   with outline answers based strictly on the candidate's real CV experiences,
   using the STAR method (Situation, Task, Action, Result).

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
        self.root.geometry("640x560")
        self.root.configure(bg="#f4f4f4")
        self.meta = {"Company": "", "Position": "", "Recruiter Name": ""}
        self.source_type = "Job Description (text)"
        self.source_value = ""
        self._build_page1()

    def _build_page1(self):
        p = tk.Frame(self.root, bg="#f4f4f4", padx=20, pady=16)
        tk.Label(p, text="Company:", bg="#f4f4f4", anchor="e", width=16,
                 font=("Segoe UI", 9)).grid(row=0, column=0, pady=5, sticky="ew")
        e1 = tk.Entry(p, width=45, bd=1)
        e1.grid(row=0, column=1, padx=8, sticky="ew")
        tk.Label(p, text="Position / Role:", bg="#f4f4f4", anchor="e", width=16,
                 font=("Segoe UI", 9)).grid(row=1, column=0, pady=5, sticky="ew")
        e2 = tk.Entry(p, width=45, bd=1)
        e2.grid(row=1, column=1, padx=8, sticky="ew")
        tk.Label(p, text="Recruiter Name:", bg="#f4f4f4", anchor="e", width=16,
                 font=("Segoe UI", 9)).grid(row=2, column=0, pady=5, sticky="ew")
        e3 = tk.Entry(p, width=45, bd=1)
        e3.grid(row=2, column=1, padx=8, sticky="ew")

        def go():
            self.meta["Company"] = e1.get().strip()
            self.meta["Position"] = e2.get().strip()
            self.meta["Recruiter Name"] = e3.get().strip()
            p.pack(forget=True)
            self._build_page2()

        tk.Button(p, text="Next →", command=go, width=12,
                  font=("Segoe UI", 9)).grid(row=3, column=1, pady=16)

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
                self.content.set(f.read())
            self.status_label.configure(text=f"Loaded: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("CV Builder", f"Could not read file:\n{e}")

    def _build_page2(self):
        p = tk.Frame(self.root, bg="#f4f4f4", padx=20, pady=16)
        p.pack(fill="both", expand=True)
        tk.Label(p, text="Choose input type:", bg="#f4f4f4",
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
        var = tk.StringVar(value="File")
        self.content = tk.StringVar()
        self.status_label = tk.Label(p, bg="#f4f4f4", fg="#c0392b",
                                     font=("Segoe UI", 8), anchor="w")
        self.status_label.grid(row=5, column=0, sticky="w")
        tk.Radiobutton(p, text="Load .txt file (recommended)", value="File",
                       bg="#f4f4f4", fg="#111", selectcolor="#dfeaff", var=var).grid(row=1, column=0, sticky="w")
        tk.Radiobutton(p, text="Job Description (paste text)", value="Job Description (text)",
                       bg="#f4f4f4", fg="#111", selectcolor="#dfeaff", var=var).grid(row=2, column=0, sticky="w")
        tk.Radiobutton(p, text="Job URL", value="URL",
                       bg="#f4f4f4", fg="#111", selectcolor="#dfeaff", var=var).grid(row=3, column=0, sticky="w")
        tk.Label(p, text="Recommended: click 'Choose file…' below and pick your JD text file:",
                 bg="#f4f4f4", font=("Segoe UI", 8)).grid(row=4, column=0, sticky="w", pady=(8, 2))
        tk.Button(p, text="Choose file…", command=self._load_file, width=14,
                  font=("Segoe UI", 9)).grid(row=6, column=0, sticky="w")
        # Tall, scrollable text box — no practical paste limit
        txt_frame = tk.Frame(p, bg="#f4f4f4")
        txt_frame.grid(row=7, column=0, pady=8, sticky="ew")
        txt = tk.Text(txt_frame, height=22, width=84, bg="#fff", fg="#111",
                      wrap="word")
        sb = tk.Scrollbar(txt_frame, command=txt.yscrollcommand)
        sb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)

        def done():
            try:
                self.source_type = var.get()
                if var.get() == "File":
                    self.source_value = self.content.get()
                else:
                    self.source_value = txt.get("1.0", "end").strip()
                if not self.source_value:
                    messagebox.showinfo("CV Builder", "No input received — please load a file or paste content first.")
                    return
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("CV Builder", f"Something went wrong:\n{e}")

        tk.Button(p, text="OK — Run process", command=done, width=16,
                  font=("Segoe UI", 9)).grid(row=8, column=0, pady=10, sticky="w")
        tk.Button(p, text="Cancel", command=self.root.destroy, width=10,
                  font=("Segoe UI", 9)).grid(row=8, column=1, pady=10, sticky="w")

    def run(self):
        self.root.mainloop()


# ── Main ───────────────────────────────────────────────────────────────
def main():
    print("CV Builder — Data Collection Engine")
    print("=" * 44)

    # 1. Collect metadata + JD source via GUI
    root = tk.Tk()
    win = SessionWindow(root)
    win.run()

    if not win.source_value:
        messagebox.showinfo("CV Builder", "No input received — cancelled.")
        root.destroy()
        return

    # 2. Fetch URL content if needed
    if win.source_type == "URL":
        try:
            jtext = fetch_url_text(win.source_value)
        except Exception as e:
            messagebox.showerror("CV Builder", f"Could not fetch URL: {e}")
            root.destroy()
            return
    else:
        jtext = win.source_value

    if len(jtext) < 20:
        messagebox.showinfo("CV Builder", "Job description too short — please paste the full text.")
        root.destroy()
        return

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
        company=win.meta.get("Company", ""),
        position=win.meta.get("Position", ""),
        recruiter=win.meta.get("Recruiter Name", ""),
        source_type=win.source_type,
        source=win.source_value if win.source_type == "URL" else "(pasted text)",
        jtext=jtext,
    )

    # 4. Update Excel row
    data = {
        "Serial Number": serial,
        "Company": win.meta.get("Company", ""),
        "Position": win.meta.get("Position", ""),
        "Recruiter Name": win.meta.get("Recruiter Name", ""),
        "Date": today,
        "Source Type": win.source_type,
        "Source": win.source_value if win.source_type == "URL" else "(pasted text)",
        "JD File": os.path.relpath(jd_path, BASE_DIR),
        "Status": "JD collected — awaiting document generation",
        "Documents Generated": "",
        "Notes": f"Manifest: {os.path.relpath(manifest, BASE_DIR)}",
    }
    row = add_session_row(ws, data)
    wb.save(WORKBOOK)
    root.destroy()

    print(f"[serial]     {serial}")
    print(f"[jd_file]    2 Job description/{safe}.txt")
    print(f"[manifest]   {os.path.relpath(manifest, BASE_DIR)}")
    print(f"[excel_log]  Application_Tracker.xlsx -> row {row}")
    messagebox.showinfo(
        "CV Builder",
        f"Session logged!\n\nSerial: {serial}\nJD saved to 2 Job description/{safe}.txt\nExcel tracker updated.\n\nNow run the LLM generation (pi) to produce the documents."
    )


if __name__ == "__main__":
    main()
