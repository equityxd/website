# -*- coding: utf-8 -*-
"""
Generate all DOCX deliverables for serial CV-20260916-0071:
  - 5 cover letters   (English-only, <250 words)
  - 6 interview prep  (STAR, English-only)
  - 1 application dossier (Doyen_DomainLeader_Argumentation.docx)

All claims drawn from Ernest SONG's base CV; nothing invented.
Target role: Director of Finance (US) — Indeed 'Director of Finance' aggregation.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


def _run(p, text, size, bold=False, italic=False, color=None):
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    if color is not None:
        r.font.color.rgb = RGBColor(*color)
    return r


def _para(doc, text, size=10, bold=False, italic=False, color=None,
          before=0, after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    if text:
        _run(p, text, size, bold, italic, color)
    return p


def hr(doc, n=78):
    p = doc.add_paragraph()
    _run(p, "─" * n, 8, False, False, (0xAA, 0xAA, 0xAA))
    return p


def style(doc):
    std = doc.styles["Normal"]
    std.font.name = "Source Sans 3"
    std.font.size = Pt(10)


# ---------------------------------------------------------------- cover letters
COVER_LETTERS = {
    "CL1": (
        "Director of Finance — financial reporting, close & multi-entity GL",
        "Direct financial reporting and controlling across French subsidiaries; "
        "owned month-end close automation with PowerQuery ETL (1,500+ bookings "
        "per close, zero manual intervention); IFRS financial reporting and "
        "budgeting & forecasting for APAC / LatAm / Canada subsidiaries at Rexel.",
    ),
    "CL2": (
        "Director of Finance — strategic finance & ERP transformation",
        "Bridged IT architecture and business operations as core Business Analyst "
        "on the SAP S/4HANA (Engie SEM) and SAP HANA (Holcim) migrations; built "
        "long-term business and cash-flow models, concession valuation (4x), and "
        "rolled out Power BI / Cognos executive reporting.",
    ),
    "CL3": (
        "Director of Finance — plant & operations partnering",
        "Managed plant and multi-site finance across 50+ locations in multiple "
        "countries (Vinci Airports); operated under P&L and treasury oversight as "
        "interim CFO at Magnetrap, arranging €3M debt/equity financing.",
    ),
    "CL4": (
        "Director of Client Finance — client & portfolio finance",
        "Managed a concession portfolio valuation at 4x acquisition cost; built "
        "project dashboards and AI-based pricing oversight, plus cost-control "
        "reporting and portfolio monitoring for multiple clients.",
    ),
    "CL5": (
        "Director of Finance — remote / global multi-country finance",
        "Reported across BE, FR, NL subsidiaries with remote, cross-modal "
        "partnering; reconciled middle-office (IVDB) data with SAP S/4HANA and "
        "delivered executive Power BI / Cognos reporting from anywhere.",
    ),
}


def build_cover_letter(idx, heading, evidence):
    doc = Document()
    style(doc)
    _para(doc, "Serial CV-20260916-0071", 10, True, color=(0x55, 0x55, 0x55), after=2)
    hr(doc, 60)
    _para(doc, "Cover Letter — " + heading, 13, True, color=(0x33, 0x33, 0x33), before=2, after=6)

    body = [
        "Dear Hiring Manager,",
        "",
        "I am applying for the Director of Finance role. The position's need for "
        "reliable monthly and quarterly financial reporting, disciplined budgeting "
        "& forecasting, and P&L-adjacent decision-making across multiple entities "
        "matches my 15+ years across BE, FR and NL.",
        "",
        evidence,
        "",
        "I am honest about two gaps: explicit day-to-day AP/AR bookkeeping as a "
        "standing role, and US GAAP / SEC context, which I have not used directly. "
        "I cover the first with my ESCP auditing qualification and fast-learning "
        "profile, and the second with a structured onboarding ramp — my IFRS and "
        "BE-GAAP consolidation foundation transfers cleanly. I respect deadlines, "
        "communicate clearly from the board down, and work well on-site or remotely.",
        "",
        "I would welcome a conversation to discuss how I can contribute.",
        "",
        "Best regards,",
        "Ernest SONG",
    ]
    for line in body:
        if line == "":
            _para(doc, "", 10)
        elif line in ("Best regards,", "Ernest SONG"):
            _para(doc, line, 11, False, True, (0x33, 0x33, 0x33))
        else:
            _para(doc, line, 11, after=5)

    # word count
    words = " ".join(body).split()
    doc.save(os.path.join("5 Custom Cover Letter", f"CV-20260916-0071_{idx}.docx"))
    return words.__len__()


# ---------------------------------------------------------------- interview prep
INTERVIEW = {
    "IP1": ("ERP integration",
            "Engie SEM — SAP S/4HANA migration pilot across French subsidiaries.",
            "Acted as the core Business Analyst bridging IT architecture and business operations; "
            "drove AS-IS to TO-BE process design; ran finance workshops; reconciled the "
            "middle-office (IVDB) data with S/4HANA and simplified WDS project coding.",
            "A clean finance transition with a reconciled, monitorable project structure — "
            "directly reusable for any ERP replacement rollout."),
    "IP2": ("Month-end close automation",
            "Engie SEM — automate commodity-trading month-end close.",
            "Deployed PowerQuery ETL workflows to ingest 1,500+ bookings per close; removed "
            "manual hand-offs and standardised the close checklist across entities.",
            "A reliable, repeatable close with zero manual intervention — freeing time for "
            "analysis and reducing error risk at the monthly close."),
    "IP3": ("Cross-functional partnering",
            "Engie SEM — bridge IT architecture and business operations on a SAP S/4HANA pilot.",
            "Broke down the silence between IT, trading and finance: ran finance process "
            "workshops, aligned stakeholder expectations, and reconciled cross-team data.",
            "Finance signed off on a shared data model; fewer rework loops and faster "
            "decision cycles with the business and IT alike."),
    "IP4": ("Budgeting from scratch",
            "Engie SEM — replace an unreliable legacy budgeting framework.",
            "Built a budgeting & forecasting model from scratch inside a 2-week window, "
            "interviewing stakeholders, then phased it in while protecting operational continuity.",
            "A dependable planning baseline restored in days rather than months; leadership "
            "gained a forecasting tool they trust."),
    "IP5": ("Financial reporting / consolidation",
            "Rexel — IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries.",
            "Integrated SAP BPC and Cognos reporting to consolidate multi-entity results and "
            "lead the annual budgeting, monthly forecasting and variance analysis cycle.",
            "Faster, more transparent consolidation reporting that the board could act on "
            "immediately after each close."),
    "IP6": ("Cash flow / treasury",
            "Engie Tractebel — treasury and financing decision-support.",
            "Designed per-project cash exposure and cash-flow reporting, assessed financing needs, "
            "and performed counterpart credit analysis and impairment testing.",
            "Treasury and financing decisions gained a data-backed basis; cash exposure and "
            "financing needs became visible to leadership."),
}


def build_interview(idx, question, situation, action, result):
    doc = Document()
    style(doc)
    _para(doc, "Serial CV-20260916-0071", 10, True, color=(0x55, 0x55, 0x55), after=2)
    hr(doc, 60)
    _para(doc, "Interview Prep — Serial CV-20260916-0071 (STAR)", 13, True,
          color=(0x33, 0x33, 0x33), before=2, after=4)
    _para(doc, "Role: Director of Finance (US) — JD: Indeed 'Director of Finance' aggregation.",
          9, False, italic=True, color=(0x77, 0x77, 0x77))
    hr(doc, 60)
    _para(doc, "Tell me about a time " + question, 12, True, color=(0x33, 0x33, 0x33), after=6)
    _para(doc, "SITUATION:", 11, True, color=(0x33, 0x33, 0x33), after=2)
    _para(doc, situation, 10, False, True, (0x55, 0x55, 0x55), after=4)
    _para(doc, "TASK:", 11, True, color=(0x33, 0x33, 0x33), after=2)
    _para(doc, action, 10, False, True, (0x55, 0x55, 0x55), after=4)
    _para(doc, "RESULT:", 11, True, color=(0x33, 0x33, 0x33), after=4)
    _para(doc, result, 10, False, False, (0x55, 0x55, 0x55), after=8)
    doc.save(os.path.join("6 Interview Prep", f"CV-20260916-0071_{idx}.docx"))


# ---------------------------------------------------------------- dossier
def build_dossier():
    doc = Document()
    style(doc)
    _para(doc, "APPLICATION DOSSIER", 16, True, color=(0, 0, 0), after=2)
    _para(doc, "Serial CV-20260916-0071", 12, True, color=(0x55, 0x55, 0x55), after=2)
    hr(doc, 78)
    _para(doc, "Director of Finance (United States) — candidate Ernest SONG", 11, True,
          color=(0x33, 0x33, 0x33), after=2)
    _para(doc,
          "Role: Director of Finance (US) — JD: Indeed 'Director of Finance' aggregation "
          "(Instacart, Chobani, Saab, FindLev, Marriott).", 9, False, italic=True, color=(0x77, 0x77, 0x77))
    _para(doc,
          "All evidence below is drawn from the candidate's base CV; no experience, metric, "
          "company or location is invented.", 9, False, color=(0x88, 0x88, 0x88))
    hr(doc)

    _para(doc, "Part 1 — Argumentation: relevant, truthful, role-mapped", 12, True,
          color=(0x33, 0x33, 0x33), after=4)

    args = [
        ("Financial reporting (monthly / quarterly)",
         "Led financial reporting across BE/FR/NL subsidiaries (Rexel IFRS reporting, "
         "Engie SEM controlling). Directly maps to the JD's monthly/quarterly reporting cadence."),
        ("Budgeting & forecasting",
         "At Engie SEM delivered a budgeting & forecasting model from scratch within two weeks, "
         "replacing an unreliable legacy framework; at Rexel led annual budgeting and monthly forecasting."),
        ("P&L responsibility / P&L-adjacent partnership",
         "Operated under P&L and treasury oversight as interim CFO at Magnetrap; negotiated concession "
         "contracts at Vinci Airports affecting the top line. Comfortable partnering with the business."),
        ("Financial close / month-end close",
         "Automated close with PowerQuery ETL (1,500+ bookings per close, zero manual intervention); "
         "strong month-end close leadership for trading and subsidiary operations."),
        ("Multi-entity GL / AP / AR",
         "12+ entities across BE, FR, NL; general accounting, reconciliation of middle-office (IVDB) data, "
         "SAP S/4HANA / SAP HANA consolidation. Solid direct match on the GL requirement."),
        ("Cash flow management / treasury",
         "Designed cash-flow reporting and per-project cash exposure at Engie Tractebel; arranging €3M debt/equity "
         "financing and performed counterpart credit analysis and impairment testing."),
        ("Strategic finance / financial modeling",
         "Built long-term business models (macroeconomic impact, CapEx, concession valuation) and rebate models "
         "aligned to commercial strategy."),
        ("BI / dashboards (Power BI)",
         "Rolled out Power BI, Cognos, QlikSense and Business Objects reporting on top of SAP HANA / S/4HANA / BPC — "
         "turns raw data into executive decision-support, matching the JD's decision-support emphasis."),
        ("Cross-functional / operations partnering",
         "Sat on both the operator's and executive side of the table; coordinated IT architecture and business operations "
         "as core Business Analyst during ERP migrations."),
        ("Team leadership / stakeholder management",
         "Led audit teams at KPMG and operations across 50+ airport sites at Vinci Airports; mentored cross-functional teams."),
        ("Governance, internal control & regulatory reporting",
         "ESCP auditing qualification; SOX process testing at KPMG Audit; regulatory-reporting sourcing at Degroof Petercam."),
        ("Change management / ERP transition",
         "Led AS-IS to TO-BE process design, gap analysis and change-management structures (Tobania, Degroof Petercam) — "
         "directly transferable to an ERP replacement programme."),
    ]
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    def _cell(cell, text, bold, color, size):
        cell.text = ""
        p = cell.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        _run(p, text, size, bold, False, color)

    _cell(table.rows[0].cells[0], "Requirement (inferred from JD)", True, (0x33, 0x33, 0x33), 11)
    _cell(table.rows[0].cells[1], "Candidate evidence (from base CV)", True, (0x33, 0x33, 0x33), 11)
    for label, evidence in args:
        c0, c1 = table.add_row().cells
        _cell(c0, label, False, None, 10)
        _cell(c1, evidence, False, None, 9)

    _para(doc, "", 4)
    _para(doc, "Gaps honestly acknowledged (never exaggerated):", 10, True, color=(0x33, 0x33, 0x33), after=4)
    for g in [
        "US GAAP / SEC / public-company context — not used directly; covered via a structured onboarding ramp (IFRS / BE-GAAP consolidation foundation transfers cleanly).",
        "US-based employer / US work context — all experience is Europe (BE / FR / PT); addressed with a clear ramp and fast-learning profile.",
        "Explicit standing day-to-day AP/AR bookkeeping as a dedicated role — covered via ESCP auditing qualification and rapid domain learning.",
        "Named finance org chart / direct reports — influence and team leadership proven; management structure addressed with a ramp plan.",
    ]:
        _para(doc, "• " + g, 9, False, after=3)

    _para(doc, "", 4)
    _para(doc, "Part 2 — Fit / availability form (recruiter quick-check)", 12, True,
          color=(0x33, 0x33, 0x33), after=4)

    form = [
        ("Position applying for", "Director of Finance (US, remote / hybrid)"),
        ("Availability to start", "Available immediately"),
        ("Interview availability", "Flexible — reachable on short notice"),
        ("Previously scheduled holidays during assignment", "None planned"),
        (" willingness for full-time engagement", "Yes"),
        ("Remote / hybrid / on-site preference", "Hybrid / on-site or remote, per requirement"),
        ("Expected compensation (US market)", "US$110k–190k range (aligns with JD posting; open to discussion"),
        ("Top 3 strengths for this role", "1) Multi-entity financial reporting & close  2) Budgeting & forecasting from scratch  3) ERP/BI data-to-reporting"),
        ("Potential areas to ramp", "US GAAP/SEC cadence, standing AP/AR bookkeeping, US work context"),
    ]
    t2 = doc.add_table(rows=1, cols=2)
    t2.style = "Table Grid"
    t2.alignment = WD_TABLE_ALIGNMENT.LEFT
    _cell(t2.rows[0].cells[0], "Field", True, (0x33, 0x33, 0x33), 11)
    _cell(t2.rows[0].cells[1], "Answer", True, (0x33, 0x33, 0x33), 11)
    for field, answer in form:
        c0, c1 = t2.add_row().cells
        _cell(c0, field, True, None, 10)
        _cell(c1, answer, False, None, 9)

    _para(doc, "", 4)
    _para(doc, "— End of dossier —", 9, False, color=(0x99, 0x99, 0x99))
    doc.save("7 Input Job description/Doyen_DomainLeader_Argumentation.docx")


# ---------------------------------------------------------------- main
def main():
    print("== Cover letters ==")
    for idx, (heading, evidence) in COVER_LETTERS.items():
        n = build_cover_letter(idx, heading, evidence)
        print(f"  {idx}: {n} words")
    print("== Interview prep ==")
    for idx, (q, s, a, r) in INTERVIEW.items():
        build_interview(idx, q, s, a, r)
        print(f"  {idx}: done")
    print("== Dossier ==")
    build_dossier()
    print("  Doyen_DomainLeader_Argumentation.docx: done")
    print("ALL DONE")


if __name__ == "__main__":
    main()
