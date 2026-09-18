# -*- coding: utf-8 -*-
"""
Generate .docx deliverables for serial CV-20260916-0076 (Director of Finance).
- 5 Cover Letters -> cover_letters/CV-20260916-0076_CL{1..5}.docx
- 6 Interview Prep -> 6 Interview Prep/CV-20260916-0076_IP{1..6}.docx
- Application Dossier -> input_job_description/Doyen_DomainLeader_Argumentation.docx

English-only for cover letters and interview prep. Every claim traces to the base CV;
nothing invented.
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor

SERIAL = "CV-20260916-0076"
ROLE = "Director of Finance (United States)"


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


# ----------------------------------------------------------------------------
# MATCH & GAP ANALYSIS (TXT)
# ----------------------------------------------------------------------------
def match_gap_analysis():
    text = """================================================================================
MATCH & GAP ANALYSIS — Serial CV-20260916-0076
================================================================================
TARGET ROLE       : Director of Finance (United States)
SOURCE TYPE       : Job Description (Indeed "Director of Finance" aggregation)
SOURCE FILE       : job_descriptions/CV-20260914-0019.txt
CANDIDATE         : Ernest SONG
DATE              : 2026-09-16
METHODOLOGY       : Factual comparison only. No experience, metric, company or
                    location is invented. Every mapping is traceable to the base CV.

NOTE ON JD NATURE
--------------------------------------------------------------------------------
The supplied JD is an Indeed aggregation / salary page, not a single-employer
requirements document. Its only "role" signals come from the 6 listed openings
and salary metadata. Evident role themes:
  - "Director, Strategic Finance" (Instacart, Remote)            $231k-$254.5k
  - "Director of Finance - Plant" (Chobani, Allentown, PA)       $140k-$190k
  - "Finance Director" (Saab, East Syracuse, NY)                 $165.7k-$223.8k
  - "Director of Client Finance" (FindLev, Remote)               $160k-$170k
  - "Director of Finance" (Marriott International, Tampa, FL)    $110k-$120k
  - "Senior Director of Finance" average $183,135/yr
  - Average base $125,087/yr; range $74,970 – $208,709/yr

This tells us the target role is a generalist corporate / plant / client
Director of Finance at the intersection of financial reporting, budgeting &
forecasting, P&L-adjacent decision support, and multi-entity / multi-site
operations — a director-level operator, not a pure strategy role. The analysis
below maps Ernest's real evidence against those inferred core requirements.

================================================================================
PHASE 1 — RECRUITER AUDIT & ATS STRATEGY
================================================================================

1. TOP-20 JD KEYWORDS (ranked by priority 1→20)
--------------------------------------------------------------------------------
 1. Director of Finance / Finance Director                 (role title match)
 2. Financial reporting (monthly / quarterly)              (JD plant/client)
 3. Budgeting & forecasting                              (strategic finance)
 4. P&L responsibility / profit & loss                     (director ownership)
 5. Financial close / month-end close                      (operational finance)
 6. Cross-functional / operations partnering               (plant & client)
 7. Strategic finance / strategic planning                 (JD "Strategic Finance")
 8. Multi-entity consolidation / GL (AP, AR)               (multi-site ops)
 9. Cash flow management / cash exposure                   (director of finance)
10. Variance analysis (actual vs budget)                   (reporting cadence)
11. Treasury / financing needs / credit analysis           (JD financing needs)
12. BI / dashboards (Power BI)                             (decision-support)
13. ERP (SAP S/4HANA / SAP HANA)                           (implementation projects)
14. Team leadership / stakeholder management               (director-level)
15. Governance & internal control                          (compliance context)
16. Regulatory reporting                                    (sourced regulatory)
17. Financial modeling / business planning                  (strategic finance)
18. M&A / corporate development                             (plant / consolidation)
19. Change management / change transition                   (transformation)
20. Remote / multi-location / multi-country                 (remote + global sites)

2. ATS MAPPING (keyword -> target section & target frequency)
--------------------------------------------------------------------------------
  Financial reporting        -> Summary + Competencies + Experience (3-4x)
  Budgeting/forecasting      -> Summary + Experience (3x)
  P&L responsibility         -> Summary + Experience (2-3x)
  Month-end close            -> Experience (2-3x)
  Multi-entity GL/AP/AR      -> Competencies + Experience (3x)
  Strategic planning         -> Summary + Experience (2-3x)
  Cash flow management       -> Experience (2x)
  Variance analysis          -> Experience (2x)
  BI dashboards (Power BI)   -> Competencies + Experience (2x)
  ERP (SAP S/4HANA/HANA)     -> Competencies + Experience (2-3x)
  Treasury / financing       -> Experience (2x)
  Team leadership            -> Experience (2x)
  Governance/internal control -> Competencies + Experience (2x)
  Regulatory reporting       -> Experience (2x)
  M&A / corporate dev        -> Experience (1-2x)
  Change management          -> Experience (2x)
  Remote / multi-country     -> Contact/Summary + Experience (2x)

3. TERMINLOGY SWAPS (5 exact swaps aligning CV language with the JD)
--------------------------------------------------------------------------------
  A. "Auditing / Financial Auditor"  ->  "Director of Finance / Finance Director"
       (position title now declares the target role, not "Chief Growth &
        Transformation Officer")
  B. "Business Object"              ->  "Business Objects"  (correct product name)
  C. "Financial close process"     ->  "Month-end close leadership"
       (JD uses close/finance-close terminology)
  D. "Financial controlling"       ->  "Financial reporting & P&L controlling"
       (aligns with "P&L responsibility" + "financial reporting")
  E. "Strategic planning process"  ->  "Strategic finance / budgeting & forecasting"
       (aligns with JD "Strategic Finance" heading)

4. ATS FORMAT FLAGS (structure issues that affect ATS parsing)
--------------------------------------------------------------------------------
  - Original CV uses octique icon contact blocks (location/mail/globe/device).
    Icons are NOT ATS-label-friendly and can drop contact text from parsing.
    FIX: replace icon contact lines with plain, machine-readable contact rows.
  - Position hardcoded as "Chief Growth & Transformation Officer" does NOT match
    the JD title "Director of Finance". FIX: update position to "Director of Finance".
  - Competencies list is generic (MS Office, RPA, Agile) but the JD wants finance-
    reporting / close / consolidation / ERP language. FIX: restructure into finance-
    reporting, close, BI, ERP, governance buckets with exact-match keywords.
  - Single keyword string in profile (SEO/ATS) should mirror top JD keywords.
    FIX: update keywords metadata to the ranked ATS keyword set.
  - Bullet phrasing is activity-based; JD is outcome/quantified. FIX: rewrite each
    bullet as Power Verb + Context/Tech + Quantified Outcome.

5. HUMAN SCAN SCORE (1-10)
--------------------------------------------------------------------------------
  Current (base) content scan effectiveness : 5 / 10
  Target (tailored Director of Finance)     : 9 / 10
  Reason: after tailoring, the title, summary, competencies and top experience
  entries all read immediately as "Director of Finance" evidence within 6 seconds.

6. GAPS (explicit gaps between the base CV and the JD)
--------------------------------------------------------------------------------
  G1. Title mismatch: base CV declares "Chief Growth & Transformation Officer";
      JD role is "Director of Finance". (Covered by repositioning + summary.)
  G2. No US GAAP / SEC / public-company context in the base CV; role is US-based.
      Covered via structured onboarding ramp (IFRS / BE-GAAP consolidation
      foundation transfers cleanly).
  G3. All experience is Europe (BE / FR / PT); no US work context.
      Addressed with a clear ramp + fast-learning profile + remote/hybrid flexibility.
  G4. No dedicated standing day-to-day AP/AR bookkeeping role in the base CV
      (close is automated/leadership-focused). Covered via ESCP auditing
      qualification and rapid domain learning.
  G5. No named direct-reports / org-chart leadership is thin; influence & team
      leadership is proven (KPMG audit teams, 50+ airport sites). Management
      structure addressed with a ramp plan.
  All evidence cited is drawn from the candidate's base CV; nothing invented.

================================================================================
DIRECT / TRANSFERABLE GAP TABLE
================================================================================
DIRECT MATCHES (real evidence satisfies inferred JD requirements)
  - Financial reporting (monthly/quarterly): Rexel IFRS reporting; Engie SEM controlling.
  - Month-end close leadership: Engie SEM PowerQuery ETL close, 1,500+ bookings/close.
  - Budgeting & forecasting: Engie SEM 2-week budget model; Rexel annual budgeting.
  - Multi-entity GL/AP/AR: 12+ entities across BE/FR/NL; IVDB reconciliation.
  - BI dashboards (Power BI): Power BI/Cognos/QlikSense/Business Objects rollouts.
  - ERP (SAP S/4HANA/SAP HANA): migration & consolidation leadership.
  - Strategic finance: concession valuation 4x, long-term business models.
TRANSFERABLE (fulfills implicit JD requirements)
  - P&L/treasury oversight as interim CFO (Magnetrap, €3M debt/equity raised).
  - Cross-functional/operations partnering (IT <-> business as Business Analyst).
  - Governance, internal control, SOX context (KPMG Audit, ESCP auditing).
  - Regulatory reporting sourcing (Degroof Petercam).
  - Change management / ERP transition (Tobania, Degroof Petercam).
CRITICAL GAPS (honest, non-exaggerated)
  - US GAAP/SEC context, US work context, dedicated standing AP/AR role,
    named direct reports — all addressed via ramp + transferable foundation.

================================================================================
"""
    path = f"job_descriptions/{SERIAL}_MATCH_GAP.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


# ----------------------------------------------------------------------------
# COVER LETTERS
# ----------------------------------------------------------------------------
def cover_letters():
    base = "cover_letters"
    cl1 = [
        "COVER LETTER 1/5 — Serial CV-20260916-0076",
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
        "COVER LETTER 2/5 — Serial CV-20260916-0076",
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
        "COVER LETTER 3/5 — Serial CV-20260916-0076",
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
        "COVER LETTER 4/5 — Serial CV-20260916-0076",
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
        "COVER LETTER 5/5 — Serial CV-20260916-0076",
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
            f"COVER LETTER {i}/5 — Serial {SERIAL}",
            ROLE,
            body,
            f"{SERIAL}_CL{i}.docx",
            base,
        )
        written.append(path)
    return written


# ----------------------------------------------------------------------------
# INTERVIEW PREP
# ----------------------------------------------------------------------------
def interview_prep():
    base = "6 Interview Prep"
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
            f"INTERVIEW PREP {i}/6 — Serial {SERIAL} (STAR)",
            q,
            *lines,
        ]
        path = build_doc(
            f"INTERVIEW PREP {i}/6 — Serial {SERIAL}",
            ROLE,
            body,
            f"{SERIAL}_IP{i}.docx",
            base,
        )
        written.append(path)
    return written


# ----------------------------------------------------------------------------
# DOSSIER
# ----------------------------------------------------------------------------
def dossier():
    base = "input_job_description"
    filename = "Doyen_DomainLeader_Argumentation.docx"
    path = build_doc(
        "Application Dossier — Ernest SONG",
        "Argumentation for Domain Leader / Finance (Infor M3 / Prometheus context) & Director of Finance",
        [
            "=== CANDIDATE ARGUMENTATION DOSSIER — Serial CV-20260916-0076 ===",
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
            "Every claim above is traceable to the candidate's base CV (source/SONG Ernest - CV v1.typ).",
            "No experience, metric, company or location is invented.",
        ],
        filename,
        base,
    )
    return [path]


def main():
    all_written = []
    all_written.append(match_gap_analysis())
    all_written += cover_letters()
    all_written += interview_prep()
    all_written += dossier()
    for p in all_written:
        print("WROTE", p)
    print("TOTAL", len(all_written))


if __name__ == "__main__":
    main()
