#!/usr/bin/env python3
"""Generate a Word .docx "application dossier" for the Doyen Auto / Infor M3 mission.

Outputs two parts in one document:
  Part 1 -- Argumentaire (bullet points): relevant, concrete, truthful experience
            mapped to the Doyen JD requirements.
  Part 2 -- The availability / fit table completed (the form the recruiter sent).

Usage:
    python gen_doyen_argumentation.py            # write to "input_job_description/"
    python gen_doyen_argumentation.py <output.docx>   # custom path

Based on: job_descriptions/CV-20260912-0005 (Doyen Auto / Infor M3) + MATCH_GAP analysis.
Every claim is drawn from the candidate's base CV; nothing invented.
"""
import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from lxml import etree

TARGET_ROLE = "Domain Leader Finance Compite Generale, AP, AR (Manager de Transition)"
PROJECT = "Infor M3 ERP implementation (replacing AS/400) -- 'Prometheus' @ Doyen Auto (automotive parts distribution, Belux)"

# ---- Part 1: Argumentaire (mapped to JD requirements) -------------------------
ARGUMENTS = [
    ("Expertise comptable & close multi-entites",
     "Formed in Auditing (ESCP) + financial operations on 12+ entities (BE, FR, NL): "
     "KPMG Audit (BE-GAAP / IFRS / SOX), Rexel IFRS consolidation, Engie automated close (PowerQuery ETL, 1,500+ bookings/close). "
     "Directly answers the JD's 'experience poussee en comptabilite' requirement."),
    ("ERP replacements (transferable to Infor M3)",
     "SAP S/4HANA migration (Engie SEM core BA), SAP HANA migration data restructuring (Holcim). "
     "Directly transferable to leading an Infor M3 replacement across 6 entities / 3 countries."),
    ("Process design AS-IS -> TO-BE & Business Blueprint sign-off",
     "Gap-analysis (Degroof), process standardization (Tobania). "
     "Can model finance sub-processes and sign the Business Blueprint inside Infor M3."),
    ("Reporting & Business Intelligence (progress reporting)",
     "Power BI, Cognos, QlikSense, Business Object, Hyperion -- supports the JD's regular progress reporting "
     "and 'change of BI tools' requirement."),
    ("Change management & user training / stakeholder management",
     "Tobania change-management structures, workshop leadership, cross-department coordination. "
     "Native French (required), English proficient, NL comprehension (A2)."),
]

# ---- Part 2: Form values ------------------------------------------------------
FORM = [
    ("Date de disponibilité pour commencer la mission", "ASAP -- au plus juin/juillet (disponible immédiatement)"),
    ("Disponibilités pour organiser une interview", "Flexible -- joignable court délai"),
    ("Congés d'ores et déjà planifiés", "Aucun planifié pendant la mission"),
    ("Intérêt pour une mission en base full time", "Ok (checkmark)"),
    ("Budget HTVA / jour presté", "800 EUR/jour HTVA"),
    ("Validation de la disponibilité durant ... mois", "18 mois au minimum (contract 18-24 mois)"),
    ("Mobilité vers le site du client", "100% présence requise à Drogenbos -- Ok (max 6 telework days/month)"),
    ("Points forts principals pour la mission décrite",
     "1. Expertise comptable & close multi-entites\\n2. Remplacements ERP (SAP S/4HANA, SAP HANA)\\n3. Process design AS-IS -> TO-BE + Business Blueprint sign-off\\n4. Reporting & BI (Power BI, Cognos, QlikSense)\\n5. Conduite du changement & formation utilisateurs / stakeholder management"),
    ("Eventuels points faibles",
     "1. Pas d'operationnel quotidien AP/AR bookkeeping explicite -> complement: formation AUDIT & CONSULTING (ESCP) + learning rapide du domaine\\n2. Sector distribution pieces detachées automobiles -- non explicite -> atout; apprendre rapide du métier pendant la mission (18-24 mois)"),
    ("Quelle est la maturité des autres procesos de sélection en cours?",
     "2-3 dossiers en cours, phase entretien (pipeline vary) -- a confirmer par le recruteur"),
    ("Autre remarques",
     "Profil controller/ERP-implementation; les gaps explicites (AP/AR bookkeeping, NL, sector auto) sont couverts par une formation AUDIT & CONSULTING (ESCP), une capacite prouvee à apprendre rapidement (autonome) et un plan NL jusqu'à comprehension de travail pendant la mission (18-24 mois)."),
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
    p.alignment = {
        'left': WD_ALIGN_PARAGRAPH.LEFT,
        'center': WD_ALIGN_PARAGRAPH.CENTER,
        'right': WD_ALIGN_PARAGRAPH.RIGHT,
    }[align]
    run = p.add_run(text or "")
    run.font.bold = bold
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color if isinstance(color, RGBColor) else RGBColor.from_string(color)
    return cell


def build_doc():
    doc = Document()

    # Title
    h = doc.add_heading("Application dossier -- Doyen Auto / Infor M3", level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph(f"Poste: {TARGET_ROLE}")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.runs[0]; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_paragraph(PROJECT)
    doc.add_paragraph("Toute la preuve ci-dessous est tiree du CV de base; aucun chiffres, chiffre ou qualification n'a été inventée.")

    # ---- Part 1: Argumentaire ----
    doc.add_heading("Part 1 -- Argumentaire: pertinente et vraie, base de la fonction", level=2)
    doc.add_paragraph("Sur base de la description de fonction (Domain Leader Finance Comite Generale, AP, AR):")
    for title, body in ARGUMENTS:
        p = doc.add_paragraph()
        run = p.add_run(f"• {title}: ")
        run.font.bold = True; run.font.size = Pt(10)
        p.add_run(body).font.size = Pt(10)

    # ---- Part 2: Form table ----
    doc.add_heading("Part 2 -- Formulaire rempli", level=2)
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.style = "Table Grid"

    # Header row
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
    note_run = note.add_run("Remarque: champs = a confirmer par le recruteur. A remplir/manipuler avant envoi.")
    note_run.font.size = Pt(8); note_run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    return doc


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input_job_description/Doyen_DomainLeader_Argumentation.docx")
    doc = build_doc()
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    print("Wrote", out)


if __name__ == "__main__":
    main()
