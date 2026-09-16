# coding: utf-8
"""
Generate cover letters (CL1-CL5) and interview prep (IP1-IP6) docx files
for serial CV-20260915-0068, target role Director of Finance (US).
English only. All claims drawn from base CV; nothing invented.
"""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

SERIAL = "CV-20260915-0068"
ROLE = "Director of Finance (United States)"
CONTACT_LINE = "Ernest SONG  �  contact@ernestsong.com  �  +32 476 60 05 90  �  Rue Montagne de l'Oratoire 28/76, B-1000 Brussels, Belgium"

CL_FILES = "5 Custom Cover Letter"
IP_FILES = "6 Interview Prep"


def add_heading(doc, text, size=14, bold=True, color=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    return p


def add_body(doc, text, size=10, italic=False, bold=False):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(4)
    r = p.runs[0]
    r.font.size = Pt(size)
    r.italic = italic
    r.bold = bold
    return p


def add_body_multiline(doc, lines):
    for line in lines:
        add_body(doc, line)


# ---------------------------------------------------------------
# COVER LETTERS (5 distinct JD angles)
# ---------------------------------------------------------------
COVER_LETTERS = {
    "CL1": (
        "Reporters & close leadership",
        "Your Director of Finance role leans on financial reporting & month-end close leadership. "
        "I have led month-end close and IFRS consolidation across multiple BE/FR jurisdictions, and I optimise "
        "close processes for governance, internal control and data quality — including automating a commodity-trading "
        "close with PowerQuery ETL that ingests 1,500+ bookings per close with zero manual intervention.",
    ),
    "CL2": (
        "budgeting & forecasting",
        "Your budgeting & forecasting requirement matches my interim-CFO and corporate-development work: "
        "I build cash-flow models, business plans and variance analysis that inform executive decisions, and I "
        "delivered a budgeting model from scratch inside a 2-week window.",
    ),
    "CL3": (
        "ERP and Business Intelligence",
        "Your ERP & BI requirement is something I deliver as a working Business Analyst: I drive SAP S/4HANA go-lives "
        "and build Power BI / Cognos reporting used by senior leaders, and I reconcile middle-office data with SAP for "
        "accurate consolidation.",
    ),
    "CL4": (
        "strategic finance & multi-entity operations",
        "Your strategic-finance, multi-entity operations requirement is my daily ground: I have led IFRS consolidation, "
        "annual budgeting, monthly forecasting and variance analysis, and managed multi-location operations (50+ sites).",
    ),
    "CL5": (
        "remote / multi-country finance",
        "Your remote, multi-country finance requirement maps to my BE/FR/PT multi-country practice, where I partner "
        "across jurisdictions, standardise reporting and lead change management so transformation is adopted.",
    ),
}


def write_cover_letter(path, angle, body_text):
    doc = Document()
    add_body(doc, CONTACT_LINE, size=9)
    add_heading(doc, "Director of Finance � Candidate Cover Letter", size=14)
    add_body(doc, "Dear Hiring Manager,", bold=True)
    add_body(doc,
        f"Applying for your {ROLE.split(' ')[0]} position, I offer a blend of operational P&L partnering, "
        "financial reporting, and ERP transformation that matches your top requirements.")
    add_body(doc, f"Your first requirement � {angle} � is central to my background:", bold=True)
    add_body(doc, body_text)
    add_body(doc,
        "Your second and third requirements – budgeting & forecasting, and ERP / Business Intelligence – I bring as "
        "a working Business Analyst: I drive SAP S/4HANA go-lives and build Power BI / Cognos reporting used by "
        "senior leaders, and I own cash-flow modelling, business plans and variance analysis that inform executive "
        "decisions.")
    add_body(doc,
        "On the gaps: I have not worked under US GAAP or held a US \"Director of Finance\" title. I address these "
        "honestly as an onboarding ramp rather than hiding them, and I lean on my proven multi-entity, multi-country "
        "foundation and my ability to learn financial regulation quickly.")
    add_body(doc, "I am excited about contributing to your organisation and would appreciate a conversation.")
    add_body(doc, "Best regards,", bold=True)
    add_body(doc, "Ernest SONG", bold=True)
    doc.save(path)
    print("wrote", path)


# ---------------------------------------------------------------
# INTERVIEW PREP (6 STAR questions)
# ---------------------------------------------------------------
INTERVIEW = [
    (
        "Tell me about a time you led a financial-close or month-end automation under pressure.",
        "Engie SEM � SAP S/4HANA pilot (Business Analyst), 2026�Present",
        "The close for commodity trading was still manual and error-prone.",
        "Remove manual effort while keeping the close accurate and auditable.",
        "As core Business Analyst bridging IT and business, I engineered a PowerQuery ETL pipeline to ingest close "
        "data automatically and reconciled middle-office (IVDB) data with SAP S/4HANA.",
        "1,500+ bookings per close processed with zero manual intervention, shortening the close and materially "
        "reducing error risk.",
    ),
    (
        "Tell me about a time you built a budgeting or forecasting model from scratch under a tight deadline.",
        "Engie SEM � financial modelling, 2026�Present",
        "The organisation faced a resource gap and relied on an unreliable legacy budgeting framework.",
        "Deliver a trustworthy budgeting & forecasting model quickly to protect operational continuity.",
        "I designed and built a budgeting model from scratch within a 2-week window, replacing the legacy framework "
        "and aligning it with actual business operations.",
        "Operational continuity protected during the resource gap; a reliable, audit-friendly budgeting baseline "
        "established in an unrealistic 2-week timeline.",
    ),
    (
        "Tell me about a time you managed an ERP / SAP migration or replacement from diagnosis to go-live.",
        "Holcim / Engie SEM � SAP HANA / S/4HANA, 2024�Present",
        "Legacy systems carried data-integrity and reporting gaps across multi-entity operations.",
        "Lead the ERP migration while guaranteeing data integrity and clean consolidation reporting.",
        "I managed the SAP HANA migration, restructured source data, and served as the core Business Analyst "
        "bridging IT architecture and business operations for the S/4HANA pilot.",
        "System integrity preserved across consolidation reporting; IT-to-business alignment enabled a smoother "
        "go-live.",
    ),
    (
        "Tell me about a time you turned financial data into executive Business Intelligence reporting.",
        "Engie Tractebel / Holcim / Shurgard � Power BI & Qliksense, 2022�2023",
        "Senior leaders lacked decision-ready visibility into cash, rebates and investment performance.",
        "Design BI reporting that turns raw SAP/data into executive insight.",
        "I built Power BI and Qliksense dashboards from SAP HANA data, and designed the data model and "
        "visualisation for the Investment department's BI efforts.",
        "Executive decision-making accelerated; investment and rebate visibility moved from manual spreadsheets to "
        "live dashboards.",
    ),
    (
        "Tell me about a time you managed P&L / treasury responsibility under uncertainty.",
        "Magnetrap � interim CFO / fundraising, 2020�2022",
        "The company needed growth capital and disciplined cash oversight simultaneously.",
        "Raise financing and protect profitability as an interim finance leader.",
        "I served as interim CFO and led fundraising, arranging €3M in debt and equity financing, while preparing "
        "cash-flow projections and monitoring performance with corrective actions.",
        "€3M in debt/equity capital secured; profitability protected through monitored metrics and corrective "
        "actions.",
    ),
    (
        "Tell me about a time you improved governance, internal control or data quality in financial reporting.",
        "Rexel / KPMG Audit / ICM � IFRS consolidation & compliance, 2009�2016",
        "Cross-border reporting introduced control and data-quality risk.",
        "Strengthen governance, internal control and data quality across consolidation.",
        "I led IFRS financial reporting for APAC/LatAm/Canada subsidiaries, integrated SAP BPC and Cognos, audited "
        "statements under SOX, and established internal control for purchasing/donation at ICM.",
        "Consolidation reporting strengthened; SOX process testing and audit-certification experience raised "
        "governance and data quality.",
    ),
]


def write_interview_prep(path, q, ctx, situation, task, action, result):
    doc = Document()
    add_heading(doc, "INTERVIEW PREP (STAR)", size=14, bold=True)
    add_body(doc, f"Serial {SERIAL} � {ROLE}", size=10, italic=True)
    add_body(doc, "Structure every answer: Situation � Task � Action � Result. Keep results quantified only where "
                  "the real CV supports them.", size=10, italic=True)
    add_body(doc, "BEHAVIORAL QUESTION", size=11, bold=True)
    add_body(doc, q, size=10, bold=True)
    add_body(doc, f"Context / source experience: {ctx}", size=9, italic=True)
    add_body(doc, "SITUATION:", size=10, bold=True)
    add_body(doc, situation, size=10)
    add_body(doc, "TASK:", size=10, bold=True)
    add_body(doc, task, size=10)
    add_body(doc, "ACTION:", size=10, bold=True)
    add_body(doc, action, size=10)
    add_body(doc, "RESULT:", size=10, bold=True)
    add_body(doc, result, size=10)
    doc.save(path)
    print("wrote", path)


def main():
    for angle, body in COVER_LETTERS.items():
        write_cover_letter(f"{CL_FILES}/{SERIAL}_{angle}.docx", angle, body)
    for i, (q, ctx, s, t, a, r) in enumerate(INTERVIEW, 1):
        write_interview_prep(f"{IP_FILES}/{SERIAL}_IP{i}.docx", q, ctx, s, t, a, r)


if __name__ == "__main__":
    main()
