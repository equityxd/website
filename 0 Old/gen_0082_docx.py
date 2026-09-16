# -*- coding: utf-8 -*-
"""Generate docx deliverables for serial CV-20260916-0082 (Director of Finance)."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

SERIAL = "CV-20260916-0082"
ROLE = "Director of Finance (United States)"
NAME = "Ernest SONG"

def style_doc(path, title_lines, body_lines, footer=None):
    d = Document()
    section = d.sections[0]
    section.top_margin = Mm(15)
    section.bottom_margin = Mm(15)
    section.left_margin = Mm(20)
    section.right_margin = Mm(20)

    def add(text, bold=False, italic=False, size=11, color=None, align="left",
            space_after=6, space_before=0, font="Source Sans Text"):
        p = d.add_paragraph()
        p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT,
                       "center": WD_ALIGN_PARAGRAPH.CENTER,
                       "right": WD_ALIGN_PARAGRAPH.RIGHT,
                       "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}[align]
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(size)
        r.font.name = font
        if color is not None:
            r.font.color.rgb = color
        r.paragraph.space_after = Pt(space_after)
        r.paragraph.space_before = Pt(space_before)
        return p

    for line in title_lines:
        if isinstance(line, tuple):
            tag, sub = line
            add(tag, bold=True, size=11, space_after=2)
            add(sub, italic=True, size=10, color=RGBColor(0x55, 0x55, 0x55), space_after=6)
        else:
            add(line, bold=True, size=11, space_after=4)

    for line in body_lines:
        add(line, size=11, space_after=6)

    if footer:
        add(footer, italic=True, size=10, color=RGBColor(0x55,0x55,0x55), space_after=6)

    d.save(path)
    print("WROTE", path)


from docx.shared import Cm, Mm

# ---------- COVER LETTERS ----------
CL = {
1: """Dear Hiring Team,

I am applying for the Director of Finance role. My career is built around the three requirements this position demands: reliable monthly and quarterly financial reporting, disciplined budgeting & forecasting, and P&L-adjacent, multi-entity decision support across BE, FR and NL.

As Business Analyst on the SAP S/4HANA migration (Engie SEM), I own month-end financial reporting while bridging IT architecture and business operations. I automated the commodity-trading close with PowerQuery ETL workflows, ingesting 1,500+ bookings per close with zero manual intervention, and I rebuilt a trustworthy budgeting & forecasting baseline from scratch inside a two-week window. Earlier at Rexel, I delivered IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries and integrated SAP BPC and Cognos reporting to consolidate multi-entity results.

I recognise two minor gaps: explicit day-to-day AP/AR bookkeeping as a dedicated standing role, and US GAAP / US work-context experience. I address the first through my ESCP auditing qualification and fast-learning profile, and the second through my solid IFRS / BE-GAAP consolidation foundation, which transfers cleanly with a short onboarding ramp. I am comfortable delivering remotely or on-site, respect deadlines, and communicate clearly from senior management to end users.

I would welcome a conversation to discuss how I can contribute as your Director of Finance.

Best regards,
Ernest SONG""",

2: """Dear Hiring Manager,

I am writing to apply for the Director of Finance position. Throughout my career I have operated at the intersection of financial reporting, budgeting & forecasting and P&L-adjacent decision support — the exact core of this role.

Most recently, as the core Business Analyst on the SAP S/4HANA migration at Engie SEM, I own month-end financial reporting across French subsidiaries while bridging IT architecture and business operations. I automated the commodity-trading close with PowerQuery ETL workflows (1,500+ bookings per close, zero manual intervention) and rebuilt a trustworthy budgeting & forecasting baseline inside a two-week window. At Rexel, I delivered IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries and integrated SAP BPC and Cognos to consolidate multi-entity results on a board-ready cadence.

I am transparent about two minor gaps: dedicated standing AP/AR bookkeeping and US GAAP / US work context. I close the first with my ESCP auditing qualification and fast-learning approach, and the second with a firm IFRS / BE-GAAP consolidation foundation that transfers quickly under a short onboarding ramp. I communicate clearly across senior management and operational teams, and I work effectively remotely or on-site.

I would welcome the opportunity to discuss how my operator's outlook can serve your finance function.

Best regards,
Ernest SONG""",

3: """Dear Selection Committee,

I apply for the Director of Finance role with 15+ years delivering trustworthy financial reporting, disciplined budgeting & forecasting and P&L-adjacent, multi-entity decision support across BE, FR and NL.

My recent mandate as Business Analyst on the SAP S/4HANA migration demonstrates the blend this role needs: I own month-end financial reporting while linking IT architecture to business operations, automated the commodity-trading close with PowerQuery ETL (1,500+ bookings per close, zero manual intervention), and restored a trustworthy budgeting & forecasting baseline from scratch in a two-week window. Earlier at Rexel I delivered IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries and integrated SAP BPC and Cognos to consolidate multi-entity results.

I address two minor gaps proactively. Dedicated day-to-day AP/AR bookkeeping I cover through my ESCP auditing qualification and rapid learning, and US GAAP / US work context I cover through a robust IFRS / BE-GAAP consolidation foundation that transfers cleanly with a short onboarding ramp. I am comfortable working remotely or on-site, meet deadlines, and translate finance for audiences from senior management to end users.

I would value a conversation about contributing as your Director of Finance.

Best regards,
Ernest SONG""",

4: """Dear Hiring Team,

I am pleased to apply for the Director of Finance position. My profile centers on the three capabilities the role requires: accurate monthly/quarterly financial reporting, rigorous budgeting & forecasting, and P&L-adjacent multi-entity decision support.

At Engie SEM, serving as the core Business Analyst on the SAP S/4HANA migration, I own month-end financial reporting across French subsidiaries while bridging IT architecture and business operations. I automated the commodity-trading close with PowerQuery ETL workflows (ingesting 1,500+ bookings per close with zero manual intervention) and rebuilt a trustworthy budgeting & forecasting baseline within a two-week window. Prior to that at Rexel, I delivered IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries and integrated SAP BPC and Cognos reporting to consolidate multi-entity results.

On two minor gaps I am honest and proactive: I have not held a dedicated standing AP/AR bookkeeping role, nor US GAAP / US work-context experience. I bridge the first with my ESCP auditing qualification and fast-learning habit, and the second with a strong IFRS / BE-GAAP consolidation foundation that transfers quickly under a concise onboarding ramp. I collaborate cleanly across senior management and end users, and I work remotely or on-site.

I would welcome a conversation to explore how I can contribute.

Best regards,
Ernest SONG""",

5: """Dear HR Team,

I am applying for the Director of Finance role. What I bring is a controller's discipline paired with an operator's outlook — reliable financial reporting, disciplined budgeting & forecasting, and P&L-adjacent, multi-entity decision support earned across BE, FR and NL.

Recently, as the core Business Analyst on the SAP S/4HANA migration at Engie SEM, I owned month-end financial reporting while bridging IT architecture and business operations. I automated the commodity-trading close with PowerQuery ETL workflows (1,500+ bookings per close, zero manual intervention) and rebuilt a trustworthy budgeting & forecasting baseline inside a two-week window. Earlier at Rexel, I delivered IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries and integrated SAP BPC and Cognos reporting to consolidate multi-entity results.

I do not hide two minor gaps — dedicated standing AP/AR bookkeeping and US GAAP / US work context — and I address them head-on: my ESCP auditing qualification and fast-learning profile cover the first, and my solid IFRS / BE-GAAP consolidation foundation transfers cleanly with a short onboarding ramp for the second. I communicate clearly from senior management to end users, respect deadlines, and deliver remotely or on-site.

I would welcome a conversation about contributing as your Director of Finance.

Best regards,
Ernest SONG""",
}

def write_cover_letter(i, text):
    path = f"5 Custom Cover Letter/{SERIAL}_CL{i}.docx"
    title_lines = [
        ("COVER LETTER", f"{i}/5  ·  {ROLE}"),
        (f"COVER LETTER {i}/5", f"Serial {SERIAL}"),
    ]
    body_lines = text.split("\n")
    style_doc(path, title_lines, body_lines)

for i in range(1, 6):
    write_cover_letter(i, CL[i])

print("=== COVER LETTERS DONE ===")

# ---------- INTERVIEW PREP (6 STAR questions) ----------
IP = [
  (
    "Tell me about a time you took ownership of a month-end or financial-close cycle under pressure.",
    "S: At Engie SEM during the SAP S/4HANA migration, the month-end close for commodity trading had to be protected across French subsidiaries. "
    "T: I was responsible for delivering trustworthy month-end financial reporting while bridging IT architecture and business operations. "
    "A: I engineered PowerQuery ETL workflows to ingest 1,500+ bookings per close with zero manual intervention, and rebuilt a trustworthy budgeting & forecasting baseline from scratch within a two-week window. "
    "R: The close ran with zero human intervention and operational continuity was preserved during a resource gap — turning a fragile legacy process into an automated, error-resistant close."
  ),
  (
    "Describe a time you had to align IT/finance architecture with business operations on a large-scale program.",
    "S: SAP S/4HANA migration at Engie SEM required a single interface between complex IT data structures and strategic business needs. "
    "T: Act as the core Business Analyst translating between IT architecture and business operations. "
    "A: I reconciled middle-office (IVDB) data with SAP S/4HANA, simplified WDS project codes to re-serve portfolio monitoring, and chaired the ongoing dialogue between IT and business stakeholders. "
    "R: This reduced reconciliation errors and improved portfolio visibility, demonstrating cross-functional partnering at director level."
  ),
  (
    "Give an example of using financial reporting / BI to drive an executive business decision.",
    "S: Leadership at multiple organizations needed reliable, timely reporting to make decisions. "
    "T: Turn fragmented data into decision-support. "
    "A: I designed Power BI reporting (with Cognos/QlikSense rollouts) to surface cash visibility and consolidated multi-entity IFRS reporting for board-ready monthly/quarterly cadence. "
    "R: Leaders gained a data-backed basis for cash/treasury and budgeting decisions, elevating reporting from descriptive to decision-support."
  ),
  (
    "Tell me about a time you improved a finance process for governance, internal control or data quality.",
    "S: At Degroof Petercam the finance close and governance gaps needed structural improvement. "
    "T: Deliver a Finance Transformation Operating Model (FTOM) and raise data quality. "
    "A: I designed and implemented a client-centric performance management system and optimized the finance close process for improved governance, internal control and data quality, following BPM standards. "
    "R: Stronger internal controls and cleaner data laid a reusable foundation for ongoing reporting."
  ),
  (
    "Describe a time you led a team or influenced stakeholders without direct authority.",
    "S: At KPMG Audit I supervised financial auditors across multi-client, multi-sector engagements. "
    "T: Lead audit teams while satisfying SOX and FP7 grant-certification requirements. "
    "A: I led supervised audit teams, certified FP7 grant agreements for the EU Research program, and tested key processes against SOX requirements across construction, real estate and water sectors. "
    "R: Delivered compliant audit outcomes and built stakeholder partnerships that supported business growth."
  ),
  (
    "Walk me through how you would onboard into a US Director of Finance role given my background.",
    "S: My experience is Europe (BE/FR/PT) and the role is US-based with US GAAP context. "
    "T: Close the minor gaps quickly without compromising delivery. "
    "A: I lean on my ESCP auditing qualification and fast-learning profile for standing AP/AR bookkeeping, and map my solid IFRS / BE-GAAP consolidation foundation onto US GAAP with a short onboarding ramp; I also work cleanly remotely or on-site. "
    "R: I can contribute from day one on reporting, close and budgeting while the GAAP/onboarding ramp completes."
  ),
]

def write_interview_prep():
    path = f"6 Interview Prep/{SERIAL}_IP1.docx"
    d = Document()
    section = d.sections[0]
    section.top_margin = Mm(15); section.bottom_margin = Mm(15)
    section.left_margin = Mm(20); section.right_margin = Mm(20)

    def add(text, bold=False, italic=False, size=11, space_after=6, space_before=0, align="left"):
        p = d.add_paragraph()
        p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT, "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}[align]
        r = p.add_run(text)
        r.bold = bold; r.italic = italic; r.font.size = Pt(size)
        r.font.name = "Source Sans Text"
        r.paragraph.space_after = Pt(space_after)
        r.paragraph.space_before = Pt(space_before)
        return p

    add("INTERVIEW PREP", bold=True, size=13, space_after=2)
    add(f"Serial {SERIAL}  ·  {ROLE}", italic=True, size=10, color=RGBColor(0x55,0x55,0x55), space_after=4)
    add("Six targeted behavioral questions, answered via the STAR method using only the candidate's real CV experience.",
        italic=True, size=10, color=RGBColor(0x55,0x55,0x55), space_after=8)

    for i, (q, a) in enumerate(IP, 1):
        add(f"Q{i}. {q}", bold=True, size=11, space_after=2)
        add(a, size=10, space_after=8, align="justify")

    add("Note: all examples are drawn strictly from the candidate's base CV (Engie SEM, Rexel, KPMG, Degroof Petercam, Vinci Airports, Magnetrap). No facts are invented.",
        italic=True, size=9, color=RGBColor(0x55,0x55,0x55), space_after=6)
    d.save(path)
    print("WROTE", path)

write_interview_prep()
print("=== INTERVIEW PREP DONE ===")

# ---------- APPLICATION DOSSIER ----------
def write_dossier():
    path = "7 Input Job description/Doyen_DomainLeader_Argumentation.docx"
    d = Document()
    section = d.sections[0]
    section.top_margin = Mm(15); section.bottom_margin = Mm(15)
    section.left_margin = Mm(20); section.right_margin = Mm(20)

    def add(text, bold=False, italic=False, size=11, space_after=6, space_before=0, align="left"):
        p = d.add_paragraph()
        p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT, "center": WD_ALIGN_PARAGRAPH.CENTER, "justify": WD_ALIGN_PARAGRAPH.JUSTIFY}[align]
        r = p.add_run(text)
        r.bold = bold; r.italic = italic; r.font.size = Pt(size)
        r.font.name = "Source Sans Text"
        r.paragraph.space_after = Pt(space_after)
        r.paragraph.space_before = Pt(space_before)
        return p

    add("APPLICATION DOSSIER — ARGUMENTATION", bold=True, size=13, space_after=2)
    add(f"Doyen / Domain Leader argumentation  ·  Serial {SERIAL}  ·  {ROLE}",
        italic=True, size=10, color=RGBColor(0x55,0x55,0x55), space_after=6)

    add("1. Positioning", bold=True, size=11, space_after=2)
    add("The candidate repositions from 'Chief Growth & Transformation Officer' to 'Director of Finance'",
        size=10, space_after=4, align="justify")

    add("2. Core argument (evidence-based)", bold=True, size=11, space_after=2)
    for line in [
        "• 15+ years delivering trustworthy monthly/quarterly financial reporting across BE, FR and NL.",
        "• Owns the month-end close cycle: automated PowerQuery ETL closes ingesting 1,500+ bookings per close with zero manual intervention.",
        "• Budgeting & forecasting: rebuilt a trustworthy baseline from scratch within a two-week window at Engie SEM.",
        "• Multi-entity GL / AP / AR: 12+ entities consolidated; IVDB reconciliation and WDS project-code simplification.",
        "• ERP (SAP S/4HANA / SAP HANA) and BI (Power BI / Cognos / QlikSense) leadership — the JD's decision-support stack.",
        "• P&L / treasury oversight as interim CFO; arranged \u20ac3M in debt/equity financing (Magnetrap).",
        "• Governance & internal control: KPMG SOX context, ESCP auditing qualification; regulatory reporting sourcing.",
    ]:
        add(line, size=10, space_after=3)

    add("3. Honest gap statement (proactive, non-apologetic)", bold=True, size=11, space_after=2)
    add("The two minor gaps — dedicated standing AP/AR bookkeeping and US GAAP / US
