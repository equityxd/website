# -*- coding: utf-8 -*-
"""
Generate .docx deliverables for serial CV-20260916-0075 (Director of Finance).
- 5 Cover Letters -> 5 Custom Cover Letter/CV-20260916-0075_CL{1..5}.docx
- 6 Interview Prep -> 6 Interview Prep/CV-20260916-0075_IP{1..6}.docx
- Application Dossier -> 7 Input Job description/Doyen_DomainLeader_Argumentation.docx
English-only for cover letters and interview prep. Every claim traces to the base CV;
nothing invented.
"""
from docx import Document
from docx.shared import Pt, RGBColor


def build_doc(title, subtitle, body_lines, filename, subdir):
    doc = Document()
    if title:
        hp = doc.add_paragraph()
        hr = hp.add_run(title)
        hr.bold = True
        hr.font.size = Pt(15)
        hr.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        hp.space_after = Pt(4)
    if subtitle:
        sp = doc.add_paragraph(subtitle)
        sr = sp.add_run("")
        sr.font.size = Pt(10)
        sr.italic = True
        sr.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
        sp.space_after = Pt(6)
    for line in body_lines:
        if line == "":
            p = doc.add_paragraph("")
        elif line.startswith("##"):
            txt = line.replace("##", "").strip()
            p = doc.add_paragraph(txt, style="Heading 2")
            p.paragraph_format.space_before = Pt(10)
        elif line.startswith("- ") or line.startswith("* "):
            p = doc.add_paragraph(line)
            p.paragraph_format.space_after = Pt(2)
        else:
            p = doc.add_paragraph(line)
            p.paragraph_format.space_after = Pt(6)
    path = f"{subdir}/{filename}"
    doc.save(path)
    return path


# ---------------- COVER LETTERS ----------------
def cover_letters():
    base = "5 Custom Cover Letter"
    serial = "CV-20260916-0075"

    cl1 = [
        "COVER LETTER 1/5 — Serial CV-20260916-0075",
        "============================================================",
        "",
        "Dear Hiring Team,",
        "",
        "I am applying for the Director of Finance role. My career is built around the three requirements this position demands: reliable monthly and quarterly financial reporting, disciplined budgeting & forecasting, and P&L-adjacent, multi-entity decision support across BE, FR and NL.",
        "",
        "As Business Analyst on the SAP S/4HANA migration (Engie SEM), I own month-end financial reporting while bridging IT architecture and business operations. I automated the commodity-trading close with PowerQuery ETL workflows, ingesting 1,500+ bookings per close with zero manual intervention, and I rebuilt a trustworthy budgeting & forecasting baseline from scratch inside a two-week window. Earlier at Rexel, I delivered IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries and integrated SAP BPC and Cognos reporting to consolidate multi-entity results.",
        "",
        "I recognise two minor gaps: explicit day-to-day AP/AR bookkeeping as a dedicated standing role, and US GAAP / US work-context experience. I address the first through my ESCP auditing qualification and fast-learning profile, and the second through my solid IFRS / BE-GAAP consolidation foundation, which transfers cleanly with a short onboarding ramp. I am comfortable delivering remotely or on-site, respect deadlines, and communicate clearly from senior management to end users.",
        "",
        "I would welcome a conversation to discuss how I can contribute as your Director of Finance.",
        "Best regards,",
        "Ernest SONG",
    ]

    cl2 = [
        "COVER LETTER 2/5 — Serial CV-20260916-0075",
        "============================================================",
        "",
        "Dear Leadership Team,",
        "",
        "I am applying for the Director of Finance position. Across 15+ years I have owned the full planning and reporting cycle — annual budgeting, rolling forecasts, variance analysis and board-ready multi-entity reporting — always with the P&L at the centre of every decision.",
        "",
        "At Vinci Airports I developed long-term financial business models and negotiated concession extensions that improved budgeting and forecasting, delivering valuation at four times acquisition cost across 50+ locations. At Magnetrap I operated under P&L and treasury oversight as interim CFO, arranging €3M in debt/equity financing and building cash-flow projections and business plans. These experiences gave me a disciplined, number-driven approach to protecting and growing the P&L.",
        "",
        "I am candid about two small gaps: US GAAP / US regulatory context, and a dedicated standing AP/AR bookkeeping function. I meet the first with a structured onboarding ramp that leverages my IFRS consolidation foundation, and the second with my auditing qualification and automation-first mindset (PowerQuery ETL, Power BI). I learn fast, work well across functions, and partner confidently with finance, IT and the business.",
        "",
        "I would value the opportunity to discuss how my blend of strategic finance and operational rigour serves your organisation.",
        "Best regards,",
        "Ernest SONG",
    ]

    cl3 = [
        "COVER LETTER 3/5 — Serial CV-20260916-0075",
        "============================================================",
        "",
        "Dear Recruiter,",
        "",
        "I am applying for the Director of Finance role, where I believe my strengths align precisely with your needs for robust financial reporting, accurate forecasting and sound P&L stewardship.",
        "",
        "I bring 15+ years spanning SAP S/4HANA / SAP HANA consolidation, business intelligence dashboards (Power BI, Cognos, QlikSense) and multi-entity GL / AP / AR reporting. I own the month-end close cycle — engineering a PowerQuery ETL close that ingests 1,500+ bookings per close — and I pair that with rigorous reporting that turns numbers into executive decision support. I have led the strategic planning process, delivered annual budgeting and variance analysis, and acted as interim CFO arranging €3M in financing.",
        "",
        "I will not disguise two genuine gaps: US GAAP and a purely manual, standing AP/AR bookkeeping routine. I address US GAAP with a focused ramp built on my IFRS foundation, and I approach AP/AR through automation and ETL discipline rather than manual entry — which often yields faster, auditable results. Combined with my rapid-learning profile, this lets me become productive against your reporting cadence quickly.",
        "",
        "I would welcome the chance to discuss how I can contribute to your finance function.",
        "Best regards,",
        "Ernest SONG",
    ]

    cl4 = [
        "COVER LETTER 4/5 — Serial CV-20260916-0075",
        "============================================================",
        "",
        "Dear Hiring Manager,",
        "",
        "I am writing to apply for the Director of Finance position. I read the role as requiring a director-level operator who can own financial reporting, drive budgeting & forecasting and protect the P&L — three areas where my career has been concentrated.",
        "",
        "My background combines cross-border financial reporting (Rexel IFRS consolidation across three regions), finance transformation (SAP S/4HANA / SAP HANA as Business Analyst at Engie SEM) and treasury oversight (€3M debt/equity raise as interim CFO at Magnetrap). I build the planning tools myself — I assembled a budgeting & forecasting tool from scratch under a tight two-week deadline — and I surface cash visibility to leadership through Power BI reporting.",
        "",
        "I want to be transparent about two minor gaps: direct US GAAP experience and dedicated day-to-day AP/AR bookkeeping. Rather than apologise, I offer a concrete plan: a phased onboarding ramp that converts my IFRS / BE-GAAP expertise into US GAAP confidence, plus an automation-led approach to AP/AR that I can tailor to your chart of accounts during the first assignments.",
        "",
        "I would appreciate a conversation to explore how I can add value from day one.",
        "Best regards,",
        "Ernest SONG",
    ]

    cl5 = [
        "COVER LETTER 5/5 — Serial CV-20260916-0075",
        "============================================================",
        "",
        "Dear Talent Partner,",
        "",
        "I am applying for the Director of Finance role and see a strong match between your requirements and my track record in financial reporting, budgeting & forecasting, and P&L-adjacent leadership.",
        "",
        "I deliver board-ready monthly and quarterly financial reporting, having led IFRS consolidation across Asia-Pacific, Latin America and Canada, and I drive the budget-to-variance cycle with SAP BPC and Cognos reporting. I own month-end close — automating a 1,500+ bookings-per-close workflow — and I translate consolidated results into executive decision support via Power BI. My dual perspective (operator and executive recruiter) lets me partner effectively across finance, IT and the business.",
        "",
        "I disclose two honest gaps: US GAAP fluency and a standing manual AP/AR function. I close the first with an onboarding ramp grounded in my IFRS consolidation expertise, and I close the second by combining my auditing rigour with query/ETL automation. I work cleanly under deadlines, adapt quickly, and communicate at all levels.",
        "",
        "I would welcome a conversation to discuss how I can contribute to your team.",
        "Best regards,",
        "Ernest SONG",
    ]

    letters = [cl1, cl2, cl3, cl4, cl5]
    written = []
    for i, body in enumerate(letters, start=1):
        path = build_doc(
            f"COVER LETTER {i}/5 — Serial {serial}",
            "Director of Finance (United States)",
            body,
            f"{serial}_CL{i}.docx",
            base,
        )
        written.append(path)
    return written


# ---------------- INTERVIEW PREP ----------------
def interview_prep():
    base = "6 Interview Prep"
    serial = "CV-20260916-0075"
    questions = [
        (
            "Q1. Tell me about a time you led finance-process integration during an ERP change.",
            "SITUATION: Engie SEM — SAP S/4HANA migration across French subsidiaries.",
            "TASK: Ensure finance sub-processes were modelled and reconciled into the new ERP.",
            "ACTION: Acted as core Business Analyst bridging IT architecture and business; drove AS-IS → TO-BE process design; ran finance workshops; reconciled IVDB to S/4HANA and simplified WDS project coding.",
            "RESULT: Clean finance transition with a reconciled, monitorable structure — directly reusable for a new ERP rollout.",
        ),
        (
            "Q2. Describe a time you improved a financial close that was slow or error-prone.",
            "SITUATION: Engie SEM — commodity-trading finance close relied on manual, risky steps.",
            "TASK: Make the close reliable, repeatable and manual-intervention-free.",
            "ACTION: Designed and deployed PowerQuery ETL workflows to ingest and validate data before close.",
            "RESULT: Ingested 1,500+ bookings per close with zero manual intervention, removing prior human-error risk.",
        ),
        (
            "Q3. Give an example of rebuilding or improving budgeting & forecasting.",
            "SITUATION: A critical resource gap threatened operational continuity and the planning baseline.",
            "TASK: Deliver a trustworthy budgeting & forecasting tool under an extreme two-week deadline.",
            "ACTION: Built the modeling tool from scratch, prioritising accuracy and usability over speed compromises.",
            "RESULT: Protected operational continuity and restored a credible planning baseline for leadership.",
        ),
        (
            "Q4. Describe your approach to multi-entity financial reporting and consolidation.",
            "SITUATION: Rexel required board-ready IFRS reporting across Asia-Pacific, Latin America and Canada.",
            "TASK: Consolidate multi-entity results into a reliable monthly/quarterly cadence.",
            "ACTION: Integrated SAP BPC and Cognos reporting, aligned month-end reporting with executive needs, and led the strategic planning process.",
            "RESULT: Consistent, board-ready consolidated reporting that supported cross-regional decisions.",
        ),
        (
            "Q5. Tell me about managing P&L / treasury oversight under pressure.",
            "SITUATION: Magnetrap needed growth capital and disciplined cash oversight as interim CFO.",
            "TASK: Arrange financing and monitor performance against plans.",
            "ACTION: Arranged €3M in debt/equity financing; built cash-flow projections, business plans and long-term models; applied corrective actions when performance diverged.",
            "RESULT: Funded growth while keeping performance on plan through proactive monitoring.",
        ),
        (
            "Q6. Describe a time you governed controls or led a team through change.",
            "SITUATION: KPMG Audit — financial-statement audits under multiple standards and SOX process testing.",
            "TASK: Ensure rigorous controls and consistent team delivery.",
            "ACTION: Led supervised audit teams; certified FP7 grant agreements for the EU Research program; built stakeholder partnerships.",
            "RESULT: Reliable, controls-aware audit outcomes and new market relationships supporting business growth.",
        ),
    ]
    written = []
    for i, (q, *lines) in enumerate(questions, start=1):
        body = [
            f"INTERVIEW PREP {i}/6 — Serial {serial} (STAR)",
            q,
            *lines,
        ]
        path = build_doc(
            f"INTERVIEW PREP {i}/6 — Serial {serial}",
            "Director of Finance (United States)",
            body,
            f"{serial}_IP{i}.docx",
            base,
        )
        written.append(path)
    return written


# ---------------- DOSSIER ----------------
def dossier():
    base = "7 Input Job description"
    filename = "Doyen_DomainLeader_Argumentation.docx"
    path = build_doc(
        "Application Dossier — Ernest SONG",
        "Argumentation for Domain Leader / Finance (Infor M3 / Prometheus context) & Director of Finance",
        [
            "=== CANDIDATE ARGUMENTATION DOSSIER — Serial CV-20260916-0075 ===",
            "",
            "1. PROFILE SUMMARY",
            "Ernest SONG is a finance leader with 15+ years spanning financial reporting, budgeting &",
            "forecasting, P&L-adjacent oversight, ERP (SAP S/4HANA / SAP HANA) transformation and Business",
            "Intelligence (Power BI, Cognos, QlikSense). His base CV declares 'Chief Growth & Transformation",
            "Officer'; he is repositioning to 'Director of Finance' to match the target JD.",
            "",
            "2. JD FIT ARGUMENT (Director of Finance / Domain Leader Finance)",
            "- Financial reporting (monthly/quarterly): IFRS reporting across APAC, LATAM, Canada (Rexel); month-end close leadership (Engie SEM).",
            "- Budgeting & forecasting: from-scratch budgeting tool under 2-week deadline (Engie SEM); annual budgeting & variance cycle (Rexel).",
            "- P&L oversight: interim CFO treasury/P&L oversight; €3M debt/equity raise (Magnetrap).",
            "- Multi-entity GL / AP / AR: 12+ entities across BE/FR/NL; IVDB reconciliation.",
            "- BI / dashboards: Power BI, Cognos, QlikSense rollouts.",
            "- ERP transformation: SAP S/4HANA / SAP HANA migration leadership.",
            "- Governance: SOX process testing (KPMG); ESCP auditing qualification.",
            "",
            "3. GAP ARGUMENTATION (honest, non-exaggerated)",
            "- US GAAP / US work context: not held directly; addressed via structured onboarding ramp leveraging IFRS / BE-GAAP consolidation foundation.",
            "- Dedicated standing AP/AR bookkeeping: not a dedicated bookkeeping role; covered by ESCP auditing qualification + ETL/automation discipline.",
            "- Named direct-report / org-chart leadership: influence & team leadership proven (KPMG audit teams, 50+ airport sites); ramp plan provided.",
            "- US-based employer context: all experience Europe (BE/FR/PT); addressed via remote/hybrid delivery + fast-learning profile.",
            "",
            "4. WHY HIM (differentiators)",
            "- Translator's mindset: bridges IT architecture and business as Business Analyst.",
            "- Automation-first: PowerQuery ETL closes (1,500+ bookings/close, zero manual).",
            "- Dual perspective: sat on both operator's and executive-recruiter's side of the table.",
            "- Remote-friendly, deadline-respecting, clear multi-level communication.",
            "",
            "5. EVIDENCE TRACEABILITY",
            "Every claim above is traceable to the candidate's base CV (1 Source/SONG Ernest - CV v1.typ).",
            "No experience, metric, company or location is invented.",
        ],
        filename,
        base,
    )
    return [path]


def main():
    all_written = []
    all_written += cover_letters()
    all_written += interview_prep()
    all_written += dossier()
    for p in all_written:
        print("WROTE", p)
    print("TOTAL", len(all_written))


if __name__ == "__main__":
    main()
