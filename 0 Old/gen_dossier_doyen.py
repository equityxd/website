#!/usr/bin/env python3
"""Generate the Word .docx application dossier for Serial CV-20260914-0019.

Target role: Director of Finance (United States) — inferred from the Indeed
aggregation JD (strategic finance, financial reporting, budgeting/forecasting,
P&L / operations partnering).

Outputs one dossier mapped to the inferred core requirements + honest gaps.
Every claim is evidence-based; nothing invented.
"""
import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from lxml import etree

TARGET_ROLE = "Director of Finance (United States)"
SRC_JD = "Indeed 'Director of Finance' aggregation page (indeed.com/career/finance-director)"

# Part 1: inferred JD requirement -> candidate evidence
ARGUMENTS = [
    ("Financial reporting (monthly / quarterly) & multi-entity reporting",
     "Rexel: IFRS financial reporting across Asia-Pacific, Latin America and Canadian subsidiaries; Engie SEM: direct financial reporting and controlling across French subsidiaries as core Business Analyst."),
    ("Month-end / financial close leadership",
     "Engie SEM: PowerQuery ETL pipeline ingesting close data; 1,500+ bookings processed per close with zero manual intervention, shortening the close and reducing error risk."),
    ("Budgeting & forecasting / variance analysis",
     "Rexel: annual budgeting, monthly forecasting and variance analysis; Engie SEM: built a budgeting/forecasting model from scratch within a critical ~2-week window, replacing an unreliable legacy framework."),
    ("P&L responsibility / operations partnering",
     "Magnetrap: interim CFO with P&L and cash oversight; Vinci Airports: financial modeling across 50+ operations (multi-site partnering)."),
    ("Cash flow management / treasury / financing",
     "Engie Tractebel: per-project cash exposure, credit analysis and impairment testing; Magnetrap: arranged \u20ac3M debt/equity financing as interim CFO."),
    ("Strategic finance / financial modeling / business planning",
     "Vinci Airports: long-term concession business models (CapEx, macroeconomic impact, concession valuation) delivered at \u22484x acquisition cost; Engie SEM budget model."),
    ("Business Intelligence / dashboards (Power BI)",
     "Engie SEM: Power BI dashboards; Holcim: Qliksense rebate-model reporting; general BI tooling (Power BI, Cognos, QlikSense, Business Objects, Hyperion)."),
    ("ERP (SAP S/4HANA / SAP HANA) implementation & change",
     "Engie SEM: core Business Analyst on SAP S/4HANA go-live; Holcim: SAP HANA migration with data restructuring; Tobania: change-management adoption of RPA + self-service BI."),
    ("Multi-entity GL (AP / AR) / consolidation",
     "KPMG Audit (multi-standard statements), Rexel IFRS consolidation, Engie multi-entity controlling — consolidation foundation across BE/FR/NL."),
    ("Governance, internal control & regulatory reporting",
     "KPMG Audit: SOX process testing; Degroof Petercam: FTOM governance and regulatory-reporting sourcing — direct-match governance and regulatory-reporting evidence."),
    ("Team leadership / stakeholder management",
     "Interim CFO and business-leadership roles with cross-department coordination and stakeholder partnering across IT, operations and customers."),
    ("Remote / multi-location / multi-country",
     "Experience spanning BE, FR, NL, PT + subsidiaries across Asia-Pacific, Latin America and Canada; comfortable operating across sites."),
]

GAPS = [
    "US GAAP / SEC / public-company context — not used directly; covered by a structured onboarding ramp (IFRS / BE-GAAP consolidation foundation transfers cleanly to US cadence).",
    "US-based employer / US work context — all experience is European (BE / FR / PT); addressed via a clear ramp plan and a fast-learning profile.",
    "Explicit standing day-to-day AP/AR bookkeeping as a dedicated role — covered by ESCP auditing qualification and rapid domain learning.",
    "Named finance-org-chart / direct reports — influence and team leadership are proven; org-structure ramp plan included.",
    "Salary anchoring below US director bands — positionable across the observed US$110k-255k range depending on angle.",
]

FORM = [
    ("Availability to start", "ASAP — available immediately"),
    ("Availability for interview", "Flexible — reachable in a short notice"),
    ("Already planned leave during engagement", "None planned"),
    ("Interest in full-time role", "Yes"),
    ("Desired monthly / annual compensation (US$)", "Open to observed US$110k-255k band depending on angle"),
    ("Remote / multi-location willingness", "Comfortable across sites; open to remote + multi-country"),
    ("Key strengths for this role", "1. Financial reporting & multi-entity close\n2. Budgeting / forecasting / variance analysis\n3. Cash flow / treasury / financing\n4. BI dashboards (Power BI)\n5. ERP SAP S/4HANA implementation & change\n6. Governance, internal control & regulatory reporting"),
    ("Potential gaps (honest)", "1. US GAAP / SEC context (onboarding ramp)\n2. US-based employer context (ramp + fast learning)\n3. Dedicated AP/AR bookkeeping role (ESCP audit + fast domain learning)"),
    ("Other remarks", "Director-level operator at the intersection of reporting, budgeting/forecasting, P&L partnering and strategic finance; fast-learning profile with a structured ramp for US context."),
]


def shade(cell, hex_color):
    tc = cell._tc
    tcPr = tc._add_tcPr()
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    shd = etree.SubElement(tcPr, "{%s}shd" % ns)
    shd.set("val", "clear")
    shd.set("color", "auto")
    shd.set("fill", hex_color)


def set_cell(cell, text, bold=False, color=None, size=10, align='left'):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = {'left': WD_ALIGN_PARAGRAPH.LEFT, 'center': WD_ALIGN_PARAGRAPH.CENTER, 'right': WD_ALIGN_PARAGRAPH.RIGHT}[align]
    run = p.add_run(text or "")
    run.font.bold = bold
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color if isinstance(color, RGBColor) else RGBColor.from_string(color)
    return cell


def build_doc():
    doc = Document()
    h = doc.add_heading("Application dossier -- Director of Finance (United States)", level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub = doc.add_paragraph(f"Poste: {TARGET_ROLE}")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.runs[0]; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    doc.add_paragraph(SRC_JD)
    doc.add_paragraph("Tout la preuve ci-dessous est tirée du CV de base; aucun chiffre, qualification n'a été inventé.")

    doc.add_heading("Part 1 -- Argumentaire: pertinente et vraie, base de la fonction", level=2)
    doc.add_paragraph("Sur base de la description de fonction (Director of Finance):")
    for title, body in ARGUMENTS:
        p = doc.add_paragraph()
        p.add_run(f"\u2022 {title}: ").font.bold = True; p.runs[0].font.size = Pt(10)
        p.add_run(body).font.size = Pt(10)

    doc.add_heading("Part 2 -- Formulaire rempli", level=2)
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    set_cell(hdr[0], "Question", bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), size=11)
    set_cell(hdr[1], "Reponse / disponibilite", bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), size=11, align='center')
    shade(hdr[0], "1F4E79"); shade(hdr[1], "1F4E79")
    for q, a in FORM:
        row = table.add_row()
        set_cell(row.cells[0], q, bold=True, size=10, align='left')
        set_cell(row.cells[1], a.replace("\\n", "\n"), bold=False, size=10, align='left')

    doc.add_paragraph("")
    note = doc.add_paragraph()
    note.add_run("Remarque: champs = a confirmer par le recruteur. A remplir/manipuler avant envoi.").font.size = Pt(8)
    note.runs[0].font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    # Gaps register
    doc.add_heading("Honest gap register", level=2)
    for g in GAPS:
        pp = doc.add_paragraph(); pp.add_run("\u2022 " + g).font.size = Pt(10)

    return doc


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("7 Input Job description/Doyen_DomainLeader_Argumentation.docx")
    doc = build_doc()
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    main()
