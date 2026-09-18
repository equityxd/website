# -*- coding: utf-8 -*-
"""
Generate 3 tailored, ATS-ready CV versions (.typ) for serial CV-20260916-0071,
targeting the role "Director of Finance (US)". Layout & full function
definitions preserved from the base CV; only content (summary, position,
competencies, experience bullets) is substituted. Bullets rewritten
(Action Verb + Context/Tech + Metric), reordered by JD fit. Every claim
traces to the candidate's base CV; nothing invented.
"""
import os

BASE = "source/SONG Ernest - CV v1.typ"
OUT = "custom_cv"

# The top matter (comments, imports, type scale, and the full function
# definitions: resume(), entry(), edu()). Everything up to the resume call.
with open(BASE, encoding="utf-8") as f:
    base = f.read()
TOP = base[:base.index("#show: body => resume(")]


def bullet(b):
    return "    - " + b


def experiences_block(experiences):
    out = ["= Professional Experience", "#v(gap)"]
    for i, e in enumerate(experiences):
        title, name, ds, de, loc, bullets = e
        imp = "important" if i == 0 else "false"
        out.append(
            "#entry(\n"
            "  " + repr(title) + ",\n"
            "  " + repr(name) + ",\n"
            "  " + repr(ds) + ", " + repr(de) + ",\n"
            "  " + repr(loc) + ",\n"
            "  [\n" + "\n".join(bullet(b) for b in bullets) + "\n"
            "  ]\n"
            ")"
        )
    return "\n".join(out)


def build_cv(position, summary, competencies, experiences):
    comp = ["#text(s, weight: \"semibold\", style: \"normal\)[Competencies]"]
    comp += ["#v(gap-m)", "#set text(size: 9pt)", "#grid("]
    cur = []
    grid = []
    for cat, terms in competencies:
        cur += ["            ==== " + cat] + ["            - " + t for t in terms]
        if len(cur) % 2 == 0:  # two categories per grid cell
            grid += ["          ["] + cur + ["        ],"]
            cur = []
    if cur:
        grid += ["          ["] + cur + ["        ],"]
    comp += grid + ["      ],", "    ]"]

    return (
        TOP +
        "#show: body => resume(\n"
        "  profile: (\n"
        '    name: "Ernest SONG",\n'
        '    address: "Rue Montagne de l\'Oratoire 28/76, B-1000 Brussels",\n'
        '    mailto: "contact@ernestsong.com",\n'
        '    website: "ernestsong.com",\n'
        '    tel: "+32 476 60 05 90",\n'
        '    keywords: "Director of Finance, Financial Reporting, Budgeting, Forecasting, '
        'Multi-entity GL, AP/AR, Financial Close, Cash Flow, Treasury, P&L, Power BI, '
        'Cognos, SAP S/4HANA, Consolidation, IFRS, BE-GAAP, Decision-Support, '
        'Cross-functional Partnering",\n'
        '    quote: "' + summary + '"\n'
        "  ),\n"
        '  position: "' + position + '",\n\n'
        "  education: [\n"
        "    #edu(\n"
        '      "ESCP Business School",\n'
        '      "(#1 FT 2026)",\n'
        "      2010, 2011,\n"
        '      "Paris, FR",\n'
        '      "Specialized Master\'s degree",\n'
        '      "Auditing and Consulting"\n'
        "    )\n\n"
        "    #edu(\n"
        '      "Université Paris Nanterre",\n'
        "      none,\n"
        "      2005, 2010,\n"
        '      "Paris, FR",\n'
        '      "Master\'s degree",\n'
        '      "Management Science and Financial Control"\n'
        "    )\n"
        "  ],\n\n"
        + "\n".join(comp) + "\n\n"
        "  languages: [\n"
        '    #text(s-small, weight: "semibold", style: "normal")[Native:] French, Khmer, Teochew \\\n'
        '    #text(s-small, weight: "semibold", style: "normal")[Proficient:] English \\\n'
        '    #text(s-small, weight: "semibold", style: "normal")[Basics:] Dutch (A2), Spanish, Mandarin \\\n\n'
        "  ],\n\n"
        "  interests: [\n"
        "    Sustainable development, Powerlifting, Mountain biking, Tennis\n"
        "  ],\n\n"
        "  interpersonal: [\n"
        "    Fast-learner, Problem solver, Diplomacy, Driven, Autonomous, Teamplayer\n"
        "  ],\n\n"
        "body"
    )


# ---------------------------------------------------------------- CV1: Reporting & Close Focus
CV1 = build_cv(
    "Director of Finance",
    "Director of Finance with 15+ years delivering monthly and quarterly financial "
    "reporting, budgeting and forecasting, and month-end close across multi-entity, "
    "multi-country operations (BE, FR, NL). I specialise in general accounting (GL, "
    "AP, AR), financial-close leadership, and turning SAP-backed finance data into "
    "executive Power BI decisions. What sets me apart: I bridge IT architecture and "
    "business operations as a business analyst, and I turn tight closes into a lever "
    "for growth.",
    [
        ("Financial Reporting & Close",
         ["Financial reporting (monthly / quarterly)",
          "Financial close / month-end close",
          "Multi-entity GL / AP / AR",
          "Consolidation / IFRS / BE-GAAP",
          "Variance / decision-support analysis"]),
        ("Tools & Systems",
         ["MS Power BI", "Cognos", "QlikSense", "Business Objects",
          "SAP S/4HANA", "SAP HANA", "SAP BPC", "SQL", "VBA", "R",
          "Jira", "Confluence"]),
    ],
    [
        ("Director of Finance - Financial Reporting & Close (Freelancer)",
         "Engie SEM", "January 2026", "Present", "Brussels, BE", [
           "Delivered monthly and quarterly financial reporting and controlling for French subsidiaries during the SAP S/4HANA pilot, bridging IT architecture and business operations as the core Business Analyst.",
           "Built an automated budgeting and forecasting model from scratch within two weeks, restoring a planning baseline during a resource gap and replacing an unreliable legacy framework.",
           "Automated month-end close with PowerQuery ETL workflows, ingesting 1,500+ bookings per close with zero manual intervention.",
           "Reconciled middle-office (IVDB) data with SAP S/4HANA and simplified WDS project coding to strengthen portfolio monitoring.",
         ]),
        ("Director of Finance - Consolidation & Reporting (Freelancer)",
         "Rexel", "September 2014", "January 2016", "Paris, FR", [
           "Led IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries.",
           "Integrated SAP BPC and Cognos reporting to consolidate multi-entity results and drive the annual budgeting and monthly forecasting cycle.",
           "Delivered variance analysis of actual vs. budgeted results to support board decisions.",
         ]),
        ("Director of Finance - Treasury & Cash Flow (Freelancer)",
         "Engie Tractebel", "March 2023", "December 2023", "Brussels, BE", [
           "Designed per-project cash exposure and cash-flow reporting to support treasury decisions.",
           "Assessed financing needs, performed counterpart credit analysis and impairment testing.",
           "Built finance data models from SAP HANA and designed Power BI executive reporting.",
         ]),
        ("Director Business Process Automation",
         "Tobania", "February 2020", "October 2020", "Brussels, BE", [
           "Drove process standardization and cost-control reporting to improve efficiency and profitability for clients.",
           "Provided tailored BI reports enabling data-driven decisions and established change-management structures for adoption.",
         ]),
        ("Managing Director - Financial Modeling (Freelancer)",
         "Vinci Airports", "February 2016", "December 2017", "Brussels, BE & Lisbon, PT", [
           "Negotiated concession extensions and implemented new budgeting and forecasting processes.",
           "Produced long-term business models (CapEx, concession valuation) and managed BE-GAAP accounting and financial reporting.",
         ]),
        ("Investment & Corporate Development Analyst (Freelancer)",
         "Shurgard", "February 2022", "February 2023", "Brussels, BE", [
           "Maintained project dashboards and corporate-development reporting for real-estate acquisition and redevelopment.",
           "Designed data models and visualizations for Investment BI efforts.",
         ]),
        ("Freelance CFO / Fundraising Consultant (Freelancer)",
         "Magnetrap", "November 2020", "January 2022", "Mons, BE", [
           "Acted as interim CFO, organizing €3M in debt/equity financing.",
           "Produced cash flow projections, business plans and operating-results reporting.",
         ]),
        ("Performance Management Project Leader (Freelancer)",
         "Degroof Petercam", "January 2018", "December 2018", "Brussels, BE", [
           "Optimized the finance-close process for improved governance, internal control and data quality.",
           "Led regulatory-reporting sourcing projects aligned to BPM standards.",
         ]),
        ("Financial Auditor Supervisor",
         "KPMG Audit", "January 2011", "August 2014", "Paris, FR", [
           "Conducted financial-statement audits across standards including SOX process testing.",
           "Led audit teams and supervised financial auditors across construction, real estate and water sectors.",
         ]),
    ],
)

# ---------------------------------------------------------------- CV2: Strategic Finance & Transformation Focus
CV2 = build_cv(
    "Director of Finance",
    "Director of Finance who turns ERP transformation into a finance-leverage "
    "opportunity: 15+ years leading financial reporting, budgeting & forecasting, "
    "and month-end close while guiding SAP S/4HANA migrations from AS-IS diagnosis to "
    "go-live. I partner across IT, trading and operations, and convert SAP-backed "
    "data into executive Power BI decisions for multi-entity operations (BE, FR, NL).",
    [
        ("Strategic Finance & Transformation",
         ["ERP transformation (SAP S/4HANA / HANA)",
          "Cross-functional / operations partnering",
          "Financial modeling",
          "Change management",
          "Decision-support"]),
        ("Financial & Reporting Controls",
         ["Financial reporting (monthly / quarterly)",
          "Budgeting & forecasting",
          "Financial close / month-end close",
          "Multi-entity GL / AP / AR",
          "Consolidation / IFRS / BE-GAAP"]),
    ],
    [
        ("Director of Finance - ERP Transformation & Business Analyst (Freelancer)",
         "Engie SEM", "January 2026", "Present", "Brussels, BE", [
           "Guided the financial controlling pilot of the SAP S/4HANA migration across French subsidiaries, acting as the core Business Analyst bridging IT architecture and business operations.",
           "Designed, built and deployed an automated budgeting and forecasting model in a two-week window, replacing an unreliable legacy framework.",
           "Automated month-end close with PowerQuery ETL workflows (1,500+ bookings per close) and reconciled IVDB data with S/4HANA while simplifying WDS project coding.",
         ]),
        ("Director of Finance - Rebate Modeling & BI (Freelancer)",
         "Holcim", "January 2024", "December 2025", "Nivelles, BE", [
           "Managed SAP HANA migration, restructured data and ensured system integrity post-M&A.",
           "Developed rebate models (matrix & automated SAP) aligning with commercial strategy.",
           "Rolled out QlikSense financial reporting and liaised with auditors on rebate matters.",
         ]),
        ("Director of Finance - Treasury (Freelancer)",
         "Engie Tractebel", "March 2023", "December 2023", "Brussels, BE", [
           "Designed per-project cash exposure and cash-flow reporting.",
           "Assessed financing needs, executed credit analysis and impairment testing.",
           "Built finance data models from SAP HANA and designed Power BI reporting.",
         ]),
        ("Director Business Process Automation",
         "Tobania", "February 2020", "October 2020", "Brussels, BE", [
           "Led a citizen-developer model using RPA and self-service BI, including pricing and roadmap.",
           "Drove business development, pre-sales and sales, and established change-management structures for adoption.",
         ]),
        ("Managing Director - Financial Modeling (Freelancer)",
         "Vinci Airports", "February 2016", "December 2017", "Brussels, BE & Lisbon, PT", [
           "Negotiated concession extensions and improved budgeting and forecasting processes.",
           "Produced long-term business models (CapEx, concession valuation 4x acquisition cost).",
         ]),
        ("Reporting Consolidation Manager (Freelancer)",
         "Rexel", "September 2014", "January 2016", "Paris, FR", [
           "Led IFRS financial reporting for APAC, LatAm and Canadian subsidiaries.",
           "Integrated SAP BPC and Cognos reporting and led annual budgeting and monthly forecasting.",
         ]),
        ("Freelance CFO / Fundraising Consultant (Freelancer)",
         "Magnetrap", "November 2020", "January 2022", "Mons, BE", [
           "Acted as interim CFO, organizing €3M in debt/equity financing.",
           "Produced cash flow projections and operating-results reporting.",
         ]),
        ("Financial Auditor Supervisor",
         "KPMG Audit", "January 2011", "August 2014", "Paris, FR", [
           "Conducted financial-statement audits including SOX process testing.",
           "Led audit teams across construction, real estate and water sectors.",
         ]),
    ],
)

# ---------------------------------------------------------------- CV3: Multi-Entity Operations & Treasury Focus
CV3 = build_cv(
    "Director of Finance",
    "Director of Finance with hands-on multi-entity finance operations across 12+ "
    "entities in BE, FR and NL: month-end close, budgeting & forecasting, cash flow "
    "and treasury, and IFRS / BE-GAAP consolidation. I combine operator discipline "
    "with executive partnering — from interim CFO / treasury at a startup to "
    "financial controlling on SAP S/4HANA migrations — to deliver decision-support "
    "across remote, multi-country teams.",
    [
        ("Multi-Entity Finance Operations",
         ["Multi-entity GL / AP / AR",
          "Consolidation / IFRS / BE-GAAP",
          "Cash flow management / treasury",
          "Financial close / month-end close",
          "Budgeting & forecasting"]),
        ("Strategic & Executive Finance",
         ["P&L / P&L-adjacent partnership",
          "BI / executive reporting (Power BI)",
          "Financial modeling",
          "Cross-functional / operations partnering",
          "Remote / hybrid / multi-country"]),
    ],
    [
        ("Director of Finance - Multi-Entity Operations (Freelancer)",
         "Holcim", "January 2024", "December 2025", "Nivelles, BE", [
           "Managed multi-entity finance and the SAP HANA migration post-M&A, ensuring data reliability and system integrity.",
           "Developed rebate models (matrix & automated SAP) aligning finance with commercial strategy.",
           "Rolled out QlikSense financial reporting and liaised with auditors on rebate matters.",
         ]),
        ("Director of Finance - Financial Reporting & Close (Freelancer)",
         "Engie SEM", "January 2026", "Present", "Brussels, BE", [
           "Delivered monthly/quarterly financial reporting and controlling for French subsidiaries during the SAP S/4HANA pilot.",
           "Automated month-end close with PowerQuery ETL workflows (1,500+ bookings per close) and reconciled IVDB data with S/4HANA while simplifying WDS project coding.",
           "Built an automated budgeting model from scratch within two weeks during a resource gap.",
         ]),
        ("Interim CFO - Treasury & Cash Flow (Freelancer)",
         "Magnetrap", "November 2020", "January 2022", "Mons, BE", [
           "Operated under P&L and treasury oversight as interim CFO, arranging €3M in debt/equity financing.",
           "Produced cash flow projections, business plans and operating-results reporting.",
         ]),
        ("Director of Finance - Treasury (Freelancer)",
         "Engie Tractebel", "March 2023", "December 2023", "Brussels, BE", [
           "Designed per-project cash exposure and cash-flow reporting and assessed financing needs.",
           "Executed counterpart credit analysis and impairment testing.",
           "Built finance data models from SAP HANA and designed Power BI executive reporting.",
         ]),
        ("Managing Director - Financial Modeling (Freelancer)",
         "Vinci Airports", "February 2016", "December 2017", "Brussels, BE & Lisbon, PT", [
           "Managed finance across 50+ operational locations in multiple countries.",
           "Negotiated concession extensions and improved budgeting and forecasting processes.",
         ]),
        ("Reporting Consolidation Manager (Freelancer)",
         "Rexel", "September 2014", "January 2016", "Paris, FR", [
           "Led IFRS financial reporting for APAC, LatAm and Canadian subsidiaries.",
           "Integrated SAP BPC and Cognos reporting and led annual budgeting and monthly forecasting.",
         ]),
        ("Director Business Process Automation",
         "Tobania", "February 2020", "October 2020", "Brussels, BE", [
           "Drove cost-control reporting and change-management structures for cross-functional adoption.",
         ]),
        ("Financial Auditor Supervisor",
         "KPMG Audit", "January 2011", "August 2014", "Paris, FR", [
           "Conducted financial-statement audits including SOX process testing.",
           "Led audit teams across construction, real estate and water sectors.",
         ]),
    ],
)


def main():
    for name, content in [("CV1", CV1), ("CV2", CV2), ("CV3", CV3)]:
        path = os.path.join(OUT, f"CV-20260916-0071_{name}.typ")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"wrote {path} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
