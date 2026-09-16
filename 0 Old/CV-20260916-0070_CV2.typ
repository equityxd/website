// ============================================================================
// Serial CV-20260916-0070 — CV2
// Target Role: Director of Finance (US)
// Positioning: "Director of Finance / Strategic Finance" — ERP transformation,
//   strategic finance, long-term business modeling, executive BI reporting.
// Layout preserved from SONG Ernest - CV v1, content rewritten for JD fit.
// ============================================================================

// ── Type scale (4 steps)
#let s        = 10pt
#let s-name   = 18pt
#let s-head   = 12pt
#let s-small  = 9pt
#let s-xsmall = 6.5pt

// ── Rhythm
#let leading     = s * 1.2
#let gap         = 4pt
#let gap-m       = 2pt
#let gutter      = 16pt
#let page-margin = 24pt
#let indent      = 0.35em

#let resume(
  profile: (
    name: str,
    address: str,
    mailto: str,
    website: str,
    tel: str,
    keywords: none,
    quote: str,
  ),
  position: str,
  education: none,
  competencies: none,
  languages: none,
  interests: none,
  interpersonal: none,
  body
) = {
  set document(author: profile.name, keywords: profile.keywords, date: auto)

  set text(s, font: "Source Sans 3", lang: "en")
  set par(leading: s * 0.7)
  set align(left)
  set list(body-indent: indent, tight: true)

  show heading.where(level: 1): body => [
    #line(length: 100%, stroke: (thickness: 0.5pt))
    #v(gap)
    #text(s-head, weight: "bold", style: "normal")[#body]
    #v(gap-m)
  ]

  show heading.where(level: 3): body => [
    #text(s, weight: "semibold", style: "normal")[#body]
    #v(gap-m)
    #line(length: 100%, stroke: (thickness: 0.3pt))
    #v(gap-m)
  ]

  show heading.where(level: 4): body => [
    #text(s-small, weight: "semibold", style: "italic")[#body]
  ]

  set page(
    paper: "a4",
    margin: page-margin,
    footer: context [
      #set align(right)
      #set text(s-small)
      #counter(page).display("1 of 1", both: true)
    ]
  )

  [

    // ─── BLOCK 1 : Title (centered) ───
    #align(center)[
      #text(s-name, weight: "bold")[#profile.name] #h(10pt) #text(s-name, style: "normal", "◆") #h(10pt) #text(s-name, style: "normal")[#position]
    ]
    #v(gap-m)
    #line(length: 100%, stroke: (thickness: 0.75pt))
    #v(gap)

    // ─── BLOCK 2 : Contact (left) + Quote (right) ───
    #grid(
      columns: (1.1fr, 2.9fr),
      gutter: gutter,
      [
        #text(s-small)[Rue Montagne de l'Oratoire 28/76]
        #v(gap)
        #h(0.7em) #text(s-small)[B-1000 Brussels]
        #v(gap)
        #text(s-small)[#profile.mailto]
        #v(gap)
        #text(s-small)[#profile.website]
        #v(gap)
        #text(s-small)[#profile.tel]
      ],
      [
        #set par(justify: true)
        #set text(hyphenate: true)
        #text(size: 9pt, style: "italic")[#profile.quote]
      ]
    )
    #line(length: 100%, stroke: (thickness: 0.75pt))
    #v(gap)

    // ─── BLOCK 3 : Three columns (reduced content) ───
    #context[
      #let s-small = 8pt
      #grid(
        columns: (2.3fr, 3fr, 2.4fr),
        gutter: gutter,
      [
        // ── Column 1 : Education ──
        #text(s, weight: "semibold", style: "normal")[Education]
        #v(gap-m)
        #set text(size: 9pt)
        #education
      ],
      [
        // ── Column 2 : Competencies ──
        #text(s, weight: "semibold", style: "normal")[Competencies]
        #v(gap-m)
        #set text(size: 9pt)
        #grid(
          columns: (1fr, 1fr),
          gutter: 8pt,
          [
            ==== Strategic Finance
            - Financial modeling
            - Business planning
            - Concession valuation

            ==== ERP Transformation
            - SAP S/4HANA migration
            - SAP HANA migration
            - SAP BPC integration

            ==== Business Intelligence
            - MS Power BI
            - Cognos
            - QlikSense
            - Business Objects

            ==== Change Management
            - AS-IS to TO-BE design
            - Change adoption
            - Roadmap & pricing

            ==== Financial Modeling
            - Cash flow modeling
            - P&L partnering
            - Rebate models

            ==== Data & Analytics
            - SQL
            - VBA
            - R
          ],
          [
            ==== Budgeting & Forecasting
            - Annual budgeting
            - Monthly forecasting
            - Variance analysis

            ==== Consolidation
            - Multi-entity GL
            - IFRS reporting
            - Audit coordination

            ==== Treasury & Cash
            - Cash exposure
            - Financing needs
            - Credit analysis

            ==== Agile & Tools
            - Jira
            - Confluence
            - MS Power Automate

            ==== RPA
            - UIPath
            - MS Power Automate

            ==== Governance
            - Internal control
            - SOX context
            - Regulatory reporting
          ]
        )
      ],
      [
        // ── Column 3 : Languages, Interests, Interpersonal ──
        #text(s, weight: "semibold", style: "normal")[Languages]
        #v(gap-m)
        #set text(size: 9pt)
        #languages

        #v(gap-m)
        #text(s, weight: "semibold", style: "normal")[Interests]
        #v(gap-m)
        #set text(size: 9pt)
        #interests

        #v(gap-m)
        #text(s, weight: "semibold", style: "normal")[Interpersonal]
        #v(gap-m)
        #set text(size: 9pt)
        #interpersonal
      ]
    )
    ]
    #v(gap)

    // ─── BLOCK 4 : Professional Experience (full width) ───
    #body
  ]
}

// ── Entry content producer ──
#let entry(title, name, date_start, date_end, location, details, important: false) = {
  let date_str = if date_start == none and date_end != none {
    str(date_end)
  } else if date_start != none and date_end == none {
    str(date_start) + " – Present"
  } else if date_start != none and date_end != none {
    str(date_start) + " – " + str(date_end)
  } else {
    ""
  }

  let content = block(breakable: false)[
    #v(1pt)
    #text(s, weight: "bold")[#name] #h(1fr) #text(s, style: "italic")[#date_str  |  #location]
    #v(-1pt)

    #if important {
      highlight(fill: rgb(224, 224, 224))[#text(s, weight: "semibold", style: "normal")[#title]]
    } else {
      text(s, weight: "semibold", style: "normal")[#title]
    }
    #v(-1pt)

    #if details != none {
      text(s-small, style: "italic")[#details]
    }
    #v(1pt)
  ]

  content
}

// Education uses a dedicated 5-line layout
#let edu(name, rank, date_start, date_end, location, degree, field) = {
  let date_str = if date_start == none and date_end != none {
    str(date_end)
  } else if date_start != none and date_end == none {
    str(date_start) + " – Present"
  } else if date_start != none and date_end != none {
    str(date_start) + " – " + str(date_end)
  } else {
    ""
  }

  stack(spacing: 0pt)[
    #text(s, weight: "bold", style: "normal")[#name]
    #if rank != none {
      linebreak()
      text(s-small, style: "normal")[#rank]
    }
    #linebreak()
    #text(s-small, style: "italic")[#date_str  |  #location]
    #linebreak()
    #text(s, style: "normal")[#degree]
    #linebreak()
    #text(s-small, style: "italic")[#field]
  ]
}

#show: body => resume(
  profile: (
    name: "Ernest SONG",
    address: "Rue Montagne de l'Oratoire 28/76, B-1000 Brussels",
    mailto: "contact@ernestsong.com",
    website: "ernestsong.com",
    tel: "+32 476 60 05 90",
    keywords: "Director of Finance, Strategic Finance, Financial modeling, SAP S/4HANA, SAP HANA, SAP BPC, BI Power BI Cognos QlikSense, Change management, AS-IS TO-BE, Consolidation, IFRS reporting, Budgeting & forecasting, Treasury, Credit analysis, SOX context, Regulatory reporting, Team leadership, Stakeholder management",
    quote: "Director of Finance with a rare operator-to-advisor range: I have led SAP S/4HANA and SAP HANA migrations as the core Business Analyst bridging IT architecture and business operations, and I build the long-term financial models — concession valuation at 4x, cash-flow and business planning — that guide executive decisions. I turn ERP and SAP data into executive Power BI and Cognos reporting, and I structure change management so adoption sticks. What sets me apart is perspective: I read the numbers, the technology, and the organisation behind them, and I stay calm under pressure."
  ),
  position: "Director of Finance (US) — Strategic Finance & ERP Transformation",

  // ── Education ──
  education: [
    #edu(
      "ESCP Business School",
      "(#1 FT 2026)",
      2010, 2011,
      "Paris, FR",
      "Specialized Master's degree",
      "Auditing and Consulting"
    )

#v(gap)

    #edu(
      "Université Paris Nanterre",
      none,
      2005, 2010,
      "Paris, FR",
      "Master's degree",
      "Management Science and Financial Control"
    )
  ],

  // ── Competencies ──
  competencies: [
  ],

  // ── Languages ──
  languages: [
    #text(s-small, weight: "semibold", style: "normal")[Native:] French, Khmer, Teochew \
    #text(s-small, weight: "semibold", style: "normal")[Proficient:] English \
    #text(s-small, weight: "semibold", style: "normal")[Basics:] Dutch (A2), Spanish, Mandarin \

  ],

  // ── Interests ──
  interests: [
    Sustainable development, Powerlifting, Mountain biking, Tennis
  ],

  // ── Interpersonal ──
  interpersonal: [
    Fast-learner, Problem solver, Diplomacy, Driven, Autonomous, Teamplayer
  ],

  body
)

// ── Professional Experience ──
= Professional Experience

#entry(
  "Strategic Finance & ERP Transformation — SAP S/4HANA / SAP HANA",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Steer the SAP HANA migration, restructuring data and guaranteeing system integrity across multi-entity consolidation reporting.
    - Use market and financial data insights to drive post-M&A operational restructuring that raises productivity and consolidation speed.
    - Roll out Qliksense financial reporting to turn SAP data into actionable executive insights for faster decision-making.
    - Build rebate models (matrix and automated SAP) aligned to commercial strategy and coordinate with auditors on rebate matters.
  ]
)

#v(gap)

#entry(
  "Finance Business Analyst — SAP S/4HANA Migration Pilot",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Serve as the core Business Analyst bridging IT architecture and business operations during the SAP S/4HANA migration pilot across French subsidiaries.
    - Own month-end close automation for commodity trading, deploying PowerQuery ETL workflows that ingest 1,500+ bookings per close with zero manual intervention.
    - Reconcile middle-office (IVDB) data with SAP S/4HANA and simplify WDS project codes to strengthen portfolio monitoring and variance analysis.
    - Deliver a budgeting & forecasting model built from scratch inside a 2-week window, replacing an unreliable legacy framework to protect operational continuity.
  ]
)

#v(gap)

#entry(
  "Treasury & Financial Modeling — Cash Exposure / Financing",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Design per-project cash exposure and cash-flow reporting to inform treasury and financing decisions.
    - Assess financing needs, perform counterpart credit analysis and impairment testing for the local entity.
    - Build finance data models from SAP HANA and design Power BI reporting to accelerate executive decision-making.
  ]
)

#v(gap)

#entry(
  "Investment & Corporate Development — Valuation / AI Pricing",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Manage real estate projects including construction, redevelopment and acquisition of self-storage businesses.
    - Maintain a project dashboard and initiate corporate-development initiatives that improve departmental policies.
    - Design the data model and visualisation for the Investment department's Business Intelligence reporting.
    - Collaborate on an AI-based pricing model to strengthen commercial margin oversight.
  ]
)

#v(gap)

#entry(
  "Interim CFO — P&L & Treasury Oversight / Fundraising",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Act as interim CFO and raise €3M in debt and equity financing while overseeing P&L and treasury.
    - Prepare cash flow projections, business plans and long-term financial goals under P&L oversight.
    - Monitor performance metrics and implement corrective actions to protect profitability.
    - Maintain financial models for ongoing strategic planning and operating-results reporting.
  ]
)

#v(gap)

#entry(
  "Business Process Automation — RPA & Self-Service BI",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Launch a citizen-developer model using RPA and self-service BI, defining pricing strategy and roadmap.
    - Drive business development across marketing, pre-sales and sales to expand finance-operations offerings.
    - Standardise and harmonise processes to improve efficiency and profitability for clients.
    - Deliver cost-control reporting and establish change management structures to accelerate adoption.
  ]
)

#v(gap)

#entry(
  "Consolidation & Financial Reporting — IFRS / Cognos",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Lead IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries.
    - Integrate SAP BPC and Cognos reporting systems to strengthen consolidation and executive reporting.
    - Perform annual budgeting, monthly forecasting and variance analysis versus budgeted results.
    - Lead the strategic planning process for the organisation.
  ]
)

#v(gap)

#entry(
  "Managing Director — Concession Valuation & Financial Modeling",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Drive value creation with a valuation at 4 times acquisition cost across a concession portfolio.
    - Deploy airport operations across 50+ locations in multiple countries while managing accounting.
    - Build long-term financial business models incorporating macroeconomic impact, CapEx and concession valuation.
    - Negotiate concession contract extensions and improve budgeting and forecasting processes.
    - Manage financial reporting in line with BE-GAAP standards across operations.
  ]
)

#v(gap)

#entry(
  "Financial Auditor Supervisor — SOX & Governance",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Conduct audits of financial statements under various accounting standards, including SOX key-process testing.
    - Audit financial modeling for long-term PPP contracts and certify FP7 grant agreements for the EU research program.
    - Lead audit teams and supervise financial auditors across construction, real estate, water and logistics sectors.
    - Develop partnerships and identify new markets to support business growth.
  ]
)

#v(gap)

#entry(
  "Deputy CFO Trainee — Budget & Internal Control",
  "ICM - Brain & Spine Institute",
  "November 2009", "August 2010",
  "Paris, FR",
  [
    - Implement the budget system and prepare business plans for the scientific teams.
    - Establish the internal control system for purchasing and donation processes and manage bank reconciliation.
    - Prepare the institutional audit necessary for certification by the "Comité de la Charte".
  ]
)
