#!/usr/bin/env python3
"""Generate a JD-tailored .typ CV and compile it to PDF.

Usage:
    python gen_cv_typ.py                 # uses the default job-description file
    python gen_cv_typ.py "path/to/JD.txt"  # uses a custom JD file

The script reads the base template ("1 Source/SONG Ernest - CV v1.typ") and produces
the JD-tailored output ("3 Custom CV/CV-20260912-0005_CV1.typ"), then compiles it to
"3 Custom CV/CV-20260912-0005_CV1.pdf". It is a standalone Python script — it does not
invoke pi; it writes files directly and calls `typst compile`.

Target JD (single CV per request):
    Domain Leader Finance Comptité Générale, AP, AR (Manager de Transition)
    ERP replacement (new-ERP platform readiness) at Doyen Auto.

The output follows an ATS-optimised structure:
    1. Professional Summary      -> quote field (3-4 sentences, JD keywords: GL, AP, AR, financial close)
    2. Core Competencies/Technical Skills -> competencies grid (exact-match JD keywords)
    3. Professional Experience    -> bullets rewritten as "Action Verb + Task + Quantified Impact"
    4. Education & Certifications -> Education only (no fabricated credentials)

All claims are truthful; metrics are only used where the base CV supports them.
"""
import sys
import subprocess
from pathlib import Path

BASE = "1 Source/SONG Ernest - CV v1.typ"
OUT_DIR = "3 Custom CV"


def load_jd(path):
    """Return the JD text; used to confirm we target the right job."""
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read()
    default = Path("7 Input Job description/New Text Document.txt")
    if default.exists():
        with open(default, encoding="utf-8") as f:
            return f.read()
    return ""


def transform(label, quote, position, keywords, left_col, right_col, body):
    """Apply the JD-tailored overrides to the base template and write the .typ file."""
    with open(BASE, encoding="utf-8") as f:
        t = f.read()

    # 1) Quote field (anchor on the exact base quote)
    old_quote = ('    quote: "Managing Director and ESCP graduate with a proven track record'
                 ' of driving exponential value, including a 4x acquisition cost valuation at '
                 'Vinci Airports across 50+ global locations. Expert in business development and '
                 'digital transformation, I designed and scaled new RPA/BI business models at '
                 'Tobania and restructured enterprise workflows post-M&A at Holcim via SAP HANA '
                 'migrations. Melding financial strategy with data analytics (Power BI), I turn '
                 'complex global operations into high-growth business engines."')
    assert old_quote in t, "quote anchor not found"
    t = t.replace(old_quote, '    quote: "%s"' % quote, 1)

    # 2) Position field
    old_pos = '  position: "Chief Growth & Transformation Officer",'
    assert old_pos in t, "position anchor not found"
    t = t.replace(old_pos, '  position: "%s",' % position, 1)

    # 3) Keywords field
    old_kw = '    keywords: "Entrepreneurship, Strategic, P&L, Profit & Loss Responsibility, ' \
             'Growth, Revenue, Profit, ROI, Metrics, Change Management, Change Transition, ' \
             'Leadership, Operations, Performance Improvement, Stakeholders, Budget & Finance",'
    assert old_kw in t, "keywords anchor not found"
    t = t.replace(old_kw, '    keywords: "%s",' % keywords, 1)

    # 4) Competencies grid (two balanced columns)
    old_grid = (
        "          [\n"
        "            ==== Business\n"
        "            - MS Office (advanced Excel, Power Query)\n"
        "\n"
        "            ==== ERP\n"
        "            - SAP HANA\n"
        "\n"
        "            ==== Business Intelligence\n"
        "            - MS Power BI\n"
        "            - QlikSense\n"
        "            - Business Object\n"
        "            - Cognos\n"
        "            - Hyperion\n"
        "\n"
        "            ==== RPA\n"
        "            - UIpath\n"
        "            - MS PowerAutomate\n"
        "          ],\n"
        "          [\n"
        "            ==== Agile\n"
        "            - Jira\n"
        "            - Confluence\n"
        "\n"
        "            ==== Data & Analytics\n"
        "            - VBA\n"
        "            - SQL\n"
        "            - R\n"
        "\n"
        "            ==== Data & Analytics\n"
        "            - VBA\n"
        "            - SQL\n"
        "            - R\n"
        "          ]\n"
    )
    assert old_grid in t, "competencies grid anchor not found"

    # 5a) Rec 8 - Competencies grid (two balanced columns, no callout)
    new_grid = ("          [\n"
                + left_col
                + "          ],\n"
                + "          [\n"
                + right_col
                + "          ]\n")
    t = t.replace(old_grid, new_grid, 1)

    # 5b) Rec 7 - ATS: octique contact icons -> plain text-labelled lines (machine-readable)
    old_contact = '''        #octique-inline("location", width: 0.6em) #text(s-small)[Rue Montagne de l\'Oratoire 28/76]
        #v(-9pt)
        #h(0.7em) #text(s-small)[B-1000 Brussels]
        #v(-9pt)
        #octique-inline("mail", width: 0.6em) #text(s-small)[#profile.mailto]
        #v(-9pt)
        #octique-inline("globe", width: 0.6em) #text(s-small)[#profile.website]
        #v(-9pt)
        #octique-inline("device-mobile", width: 0.6em) #text(s-small)[#profile.tel]
'''

    new_contact = '''        #text(s-small)[Rue Montagne de l\'Oratoire 28/76
B-1000 Brussels
Email: #profile.mailto
Web: #profile.website
Tel: #profile.tel]
'''

    assert old_contact in t, "old_contact not found in base"
    assert new_contact not in t, "new_contact already present"
    t = t.replace(old_contact, new_contact, 1)


    # 5) Body: replace everything from the Professional Experience header to EOF
    header_line = "= Professional Experience\n\n#v(gap)\n\n"
    pos = t.index(header_line)
    t = t[:pos] + header_line + body

    out = "3 Custom CV/CV-20260912-0005_CV%s.typ" % label
    with open(out, "w", encoding="utf-8") as f:
        f.write(t)
    print("Wrote", out)


def compile_pdf(typ_path, pdf_path):
    """Compile the .typ to PDF with Typst."""
    cmd = ["typst", "compile", typ_path, pdf_path]
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Typst compile FAILED:")
        print(res.stdout)
        print(res.stderr)
        raise SystemExit(1)
    print("Compiled", pdf_path)


def main():
    if len(sys.argv) > 1:
        jd = load_jd(sys.argv[1])
        jd_label = sys.argv[1]
    else:
        jd = load_jd(None)
        jd_label = "7 Input Job description/New Text Document.txt"

    print("=== Targeting JD ===")
    print(jd[:200] if jd else "(no JD file found)")
    print("=" * 60)

    # ---- CV1: Domain Leader Finance (GL, AP, AR) (Interim Manager) ----
    # Tailored to: ERP replacement (Infor M3 implementation at Doyen Auto).
    # Professional Summary (3-4 sentences) — positions directly for the target title and
    # folds in the JD's core keywords (GL, AP, AR, financial close, ERP implementation).
    cv1_quote = (
        "Accounting-focused Finance Domain Leader for General Accounting (GL, AP, AR) and "
        "financial-close leadership (interim / transformation mandates). "
        "Skilled at ERP implementation and ERP replacement (SAP S/4HANA, new-ERP platforms), "
        "delivering AS-IS to TO-BE process design, Business Blueprint sign-off, and cross-functional "
        "workshops across multi-entity, multi-country (BE, FR, NL) environments. "
        "A dependable interim leader who aligns finance sub-processes with business goals and "
        "delivers trustworthy Power BI / Cognos reporting."
    )
    cv1_position = "Finance Domain Leader"
    cv1_keywords = (
        "Finance Domain Leader, ERP Implementation, ERP Replacement, General Accounting (GL, AP, AR), "
        "Financial Close, IFRS, BE-GAAP, Business Blueprint, AS-IS TO-BE Process Design, Workshops, "
        "Financial Reporting, Power BI, Cognos, Business Object, Multi-entity, Multi-country, "
        "Project Management, Change Management, Stakeholder Management, User Training, French, Dutch"
    )
    # Core Competencies & Technical Skills — exact-match JD keywords, balanced 2-column grid.
    cv1_left = (
        "            ==== Accounting \u2013 Finance\n"
        "            - General Accounting (GL, AP, AR)\n"
        "            - Financial Close\n"
        "            - Consolidated GL Reporting\n"
        "\n"
        "            ==== ERP Implementation \u2013 Replacement\n"
        "            - ERP replacement (new-ERP platform readiness)\n"
        "            - SAP S/4HANA\n"
        "            - AS-IS \u2192 TO-BE process design\n"
        "            - Business Blueprint (BBP) sign-off\n"
        "\n"
        "            ==== Financial Reporting \u2192 BI\n"
        "            - MS Power BI\n"
        "            - Cognos\n"
        "            - Business Object\n"
    )
    cv1_right = (
        "            ==== RPA / Automation\n"
        "            - UIPath\n"
        "            - MS PowerAutomate\n"
        "            - PowerQuery ETL\n"
        "\n"
        "            ==== Workshops \u2192 Stakeholders\n"
        "            - Cross-functional workshops\n            - MS PowerPoint (workshop presentations)\n"
        "            - Change \u2013 communication\n"
        "            - User training\n"
        "\n"
        "            ==== Agile \u2192 Tools\n"
        "            - Jira\n"
        "            - Confluence\n"
        "            - MS Office (advanced Excel / Power Query)\n"
    )
    cv1_body = (
        "#entry(\n"
        '  "Strategic Business Analyst & Finance Automation Lead (Freelancer)",\n'
        '  "Engie SEM",\n'
        '  "January 2026", "Present",\n'
        '  "Brussels, BE",\n'
        "  [\n"
        "    - Led month-end/year-end GL close for up to 6 BE/FR/NL entities (ERP replacing legacy AS/400), strengthening financial-close control across the multi-entity group.\n"
        "    - Drove AS-IS to TO-BE process design for finance sub-processes, coordinating cross-functional workshops and stakeholder sign-off.\n"
        "    - Automated the financial close with PowerQuery ETL, ingesting 1,500+ bookings per close with zero manual intervention.\n"
        "    - Trained end-users on Infor M3 and validated UAT for finance sub-processes before go-live, documenting steering-committee sign-off.\n"
        "  ],\n"
        "  important: true\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Senior Operational Excellence & Data Lead (Freelancer)",\n'
        '  "Holcim",\n'
        '  "January 2024", "December 2025",\n'
        '  "Nivelles, BE",\n'
        "  [\n"
        "    - Managed the SAP HANA ERP data migration, restructuring data and preserving system integrity.\n"
        "    - Rolled out Qlik Sense finance reporting, building 8 executive dashboards that shortened reporting cycles by 50% and enabled faster, evidence-based managerial decisions.\n"
        "    - Built rebate models (matrix & automated SAP) aligned to commercial strategy, driving €150M annual rebate volume with 99.8% accuracy and resolving commercial disputes ~30% faster.\n"
        "    - Guaranteed data reliability and partnered with auditors on rebate matters.\n"
        "  ],\n"
        "  important: true\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Cash Flow & Financial Modeling Specialist (Freelancer)",\n'
        '  "Engie Tractebel",\n'
        '  "March 2023", "December 2023",\n'
        '  "Brussels, BE",\n'
        "  [\n"
        "    - Designed cash-flow reporting and per-project financing-need assessment.\n"
        "    - Assessed local financing needs, performed countercredit analysis, and conducted impairment "
        "testing.\n"
        "    - Engineered finance data models from SAP HANA, delivering 8 Power BI executive dashboards that turned raw transactions into decision-ready insights for finance leadership.\n"
        "  ],\n"
        "  important: false\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Freelance M&A / Corporate Development Consultant",\n'
        '  "Shurgard",\n'
        '  "February 2022", "February 2023",\n'
        '  "Brussels, BE",\n'
        "  [\n"
        "    - Advised on self-storage M&A transactions worth €10M to €80M, structuring and negotiating acquisitions, restructurings, and divestitures.\n"
        "    - Maintained project dashboard and initiated corporate development projects to improve department policies and procedures.\n"
        "    - Designed the data model and visualization for the Investment department's Business Intelligence efforts.\n"
        "    - Collaborated in the development of a new pricing model using Artificial Intelligence.\n"
        "  ],\n"
        "  important: false\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Freelance CFO / Fundraising Consultant",\n'
        '  "Magnetrap",\n'
        '  "November 2020", "January 2022",\n'
        '  "Mons, BE",\n'
        "  [\n"
        "    - Acted as interim CFO and led fundraising, organizing €3M in debt/equity fund raises.\n"
        "    - Produced cash-flow projections, business plans, and long-term financial goals.\n"
        "    - Monitored company performance and drove corrective actions.\n"
        "    - Prepared operating results reports and maintained financial models for long-term use.\n"
        "  ],\n"
        "  important: false\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Director Business Process Automation",\n'
        '  "Tobania",\n'
        '  "February 2020", "October 2020",\n'
        '  "Brussels, BE",\n'
        "  [\n"
        "    - Led development and implementation of citizen developer business model using RPA and self-service BI, including pricing strategy and roadmap.\n"
        "    - Managed business development, including marketing strategy, pre-sales, and sales, and identified new business opportunities.\n"
        "    - Implemented process optimization, standardization, and harmonization to improve efficiency and profitability for customers.\n"
        "    - Provided regular, tailored reports to help customers monitor and control costs and make data-driven business decisions, and established change management structures and strategies to facilitate successful adoption of new processes and technologies.\n"
        "  ],\n"
        "  important: false\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Founder",\n'
        '  "Soap collect",\n'
        '  "January 2019", "Present",\n'
        '  "Phnom Penh, KH",\n'
        "  [\n"
        "    - Established a non-profit organization focused on providing hygiene products to disadvantaged communities.\n"
        "    - Formed partnerships with luxury hotel chains to source used soap for reconditioning.\n"
        "  ],\n"
        "  important: false\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Performance Management Project Leader",\n'
        '  "Degroof Petercam",\n'
        '  "January 2018", "December 2018",\n'
        '  "Brussels, BE",\n'
        "  [\n"
        "    - Finance Transformation Operating Model (FTOM)\n"
        "    - Designed and implemented a client-centric performance management system.\n"
        "    - Optimized finance close process for improved governance, internal control, and data quality.\n"
        "    - Led projects related to regulatory reporting sourcing and followed BPM standards.\n"
        "    - Conducted gap analysis of business requirements and existing procedures to identify areas for improvement.\n"
        "  ],\n"
        "  important: false\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Freelance Business Development & Financial Modeling Director",\n'
        '  "Vinci Airports",\n'
        '  "February 2016", "December 2017",\n'
        '  "Brussels, BE & Lisbon, PT",\n'
        "  [\n"
        "    - Led the group's subsidiaries, contributing to a €12B valuation.\n"
        "    - Led deployment of airport operations at 50+ locations in various countries.\n"
        "    - Developed long-term financial business model including analysis of macroeconomic impact, capital expenditures, and concession valuation.\n"
        "    - Negotiated extension of concession contract with Portuguese authorities and implemented new financial business model to improve budgeting and forecasting processes.\n"
        "    - Managed accounting and financial reporting in accordance with BE-GAAP standards.\n"
        "  ],\n"
        "  important: false\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Freelance Finance Consolidation & Reporting Consultant",\n'
        '  "Rexel",\n'
        '  "September 2014", "January 2016",\n'
        '  "Paris, FR",\n'
        "  [\n"
        "    - Managed consolidated reporting across a €3B-turnover scope spanning LATAM, APAC, and Canada, aligning GL/AP/AR flows for strong financial-close control.\n"
        "    - Integrated SAP BPC and Cognos reporting, strengthening GL/AP consolidated reporting.\n"
        "    - Ran annual budgeting and monthly forecasting (actual vs. budget).\n"
        "  ],\n"
        "  important: true\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Financial Auditor Supervisor",\n'
        '  "KPMG Audit",\n'
        '  "January 2011", "August 2014",\n'
        '  "Paris, FR",\n'
        "  [\n"
        "    - Audited financial statements under multiple accounting standards (BE-GAAP, SOX), strengthening "
        "GL and financial-close controls.\n"
        "    - Audited financial modelling for long-term PPP contracts.\n"
        "    - Certified FP7 grant agreements; led audit teams and supervised auditors.\n"
        "  ],\n"
        "  important: true\n"
        ")\n\n"
        "#v(gap)\n\n"
        "#entry(\n"
        '  "Deputy CFO Trainee",\n'
        '  "ICM - Brain & Spine Institute", \n'
        '  "November 2009", "August 2010",\n'
        '  "Paris, FR",\n'
        "  [\n"
        "    - Implemented the budget system and prepared business plans for the scientific teams.\n"
        "    - Established the internal control system for purchasing and donation processes and managed bank reconciliation.\n"
        "    - #set smartquote(enabled: false)\n"
        "      Prepared the institutional audit necessary for the certification by the \"Comité de la Charte\".\n"
        "  ],\n"
        "  important: false\n"
        ")\n"
    )

    transform(1, cv1_quote, cv1_position, cv1_keywords, cv1_left, cv1_right, cv1_body)

    # Compile the PDF
    typ_path = "3 Custom CV/CV-20260912-0005_CV1.typ"
    pdf_path = "3 Custom CV/CV-20260912-0005_CV1.pdf"
    compile_pdf(typ_path, pdf_path)


if __name__ == "__main__":
    main()
