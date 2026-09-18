# -*- coding: utf-8 -*-
"""
Generate a Word .docx "application dossier" for serial CV-20260914-0019,
target role 'Director of Finance' (United States - Indeed aggregation JD).

Two parts in one document:
  Part 1 -- Argumentation: relevant, concrete, truthful experience mapped to
            the inferred core requirements of the Director of Finance role.
  Part 2 -- A fit / availability table (recruiter-facing quick-check form).

Every claim is drawn from facts present in Ernest SONG's base CV; nothing
invented. This is the correct dossier for the Director of Finance role.
(The pre-existing Doyen_DomainLeader_Argumentation.docx in this folder belongs
to a different candidate/mission and is left untouched.)
"""
import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


def _cell(cell, text, bold, _r, _g, _b, size):
    cell.text = ""
    p = cell.add_paragraph(text)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    run = p.runs[0] if p.runs else p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    if _r is not None:
        run.font.color.rgb = RGBColor(_r, _g, _b)
    return cell


def style(doc):
    std = doc.styles["Normal"]
    std.font.name = "Source Sans 3"
    std.font.size = Pt(10)


def title(doc, lines):
    for i, (text, size, bold, color) in enumerate(lines):
        p = doc.add_paragraph()
        p.alignment = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT,
                         WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT][i]
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.font.bold = bold
        if color is not None:
            r.font.color.rgb = RGBColor(*color)


def para(doc, text, size=10, bold=False, italic=False, color=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        if color is not None:
            r.font.color.rgb = RGBColor(*color)
    return p


def hr(doc):
    p = doc.add_paragraph()
    r = p.add_run("─" * 78)
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
    return p


def build():
    doc = Document()
    style(doc)

    title(doc, [
        ("APPLICATION DOSSIER", 16, True, (0, 0, 0)),
        ("Serial CV-20260914-0019", 12, False, (0x55, 0x55, 0x55)),
        ("─" * 78, 8, False, (0xAA, 0xAA, 0xAA)),
        ("Director of Finance (United States) — candidate Ernest SONG", 11, True, (0x33, 0x33, 0x33)),
    ])
    para(doc, "Serial CV-20260914-0019", 10, True, color=(0x55, 0x55, 0x55))
    para(doc,
        "Role: Director of Finance (US) — JD: Indeed 'Director of Finance' aggregation "
        "(Instacart, Chobani, Saab, FindLev, Marriott).", 9, False, italic=True, color=(0x77, 0x77, 0x77))
    para(doc,
        "All evidence below is drawn from the candidate's base CV; no experience, metric, "
        "company or location is invented.", 9, False, color=(0x88, 0x88, 0x88))
    hr(doc)

    # ---- Part 1: Argumentation ----
    p = doc.add_paragraph()
    r = p.add_run("Part 1 — Argumentation: relevant, truthful, role-mapped")
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    para(doc, "", 6)

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
         "SAP S/4HANA / SAP HANA consolidation. Solid direct-match on the GL requirement."),
        ("Cash flow management / treasury",
         "Designed cash-flow reporting and per-project cash exposure at Engie Tractebel; arranged €3M debt/equity "
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
    _cell(table.rows[0].cells[0], "Requirement (inferred from JD)", True, 0x33, 0x33, 0x33, 11)
    _cell(table.rows[0].cells[1], "Candidate evidence (from base CV)", True, 0x33, 0x33, 0x33, 11)
    for label, evidence in args:
        c0, c1 = table.add_row().cells
        _cell(c0, label, False, None, None, None, 10)
        _cell(c1, evidence, False, None, None, None, 9)

    para(doc, "", 6)
    para(doc, "Gaps honestly acknowledged (never exaggerated):", 10, True, color=(0x33, 0x33, 0x33))
    for g in [
        "US GAAP / SEC / public-company context — not used directly; covered via a structured onboarding ramp (IFRS / BE-GAAP consolidation foundation transfers cleanly).",
        "US-based employer / US work context — all experience is Europe (BE / FR / PT); addressed with a clear ramp and fast-learning profile.",
        "Explicit standing day-to-day AP/AR bookkeeping as a dedicated role — covered via ESCP auditing qualification and rapid domain learning.",
        "Named finance org chart / direct reports — influence and team leadership proven; management structure addressed with a ramp plan.",
    ]:
        para(doc, "• " + g, 9, False, space_after=3)

    # ---- Part 2: Fit / availability table ----
    p = doc.add_paragraph()
    r = p.add_run("Part 2 — Fit / availability form (recruiter quick-check)")
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    para(doc, "", 6)

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
    _cell(t2.rows[0].cells[0], "Field", True, 0x33, 0x33, 0x33, 11)
    _cell(t2.rows[0].cells[1], "Answer", True, 0x33, 0x33, 0x33, 11)
    for field, answer in form:
        c0, c1 = t2.add_row().cells
        _cell(c0, field, True, None, None, None, 10)
        _cell(c1, answer, False, None, None, None, 9)

    para(doc, "", 6)
    para(doc, "— End of dossier —", 9, False, color=(0x99, 0x99, 0x99))
    return doc


def _cell(cell, text, bold, _r, _g, _b, size):
    cell.text = ""
    p = cell.add_paragraph(text)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    run = p.runs[0] if p.runs else p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    if _r is not None:
        run.font.color.rgb = RGBColor(_r, _g, _b)
    return cell


def main():
    path = "input_job_description/CV-20260914-0019_Dossier.docx"
    doc = build()
    doc.save(path)
    print("WROTE", path)


if __name__ == "__main__":
    main()
