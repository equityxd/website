// ============================================================================
// Serial CV-20260914-0019 — CV2
// Target Role: Director of Finance (strategic finance & ERP transformation focus)
// Positioning: "Director of Finance" — strategic finance, financial modeling,
//   SAP S/4HANA implementation, change/transformation. ATS-friendly (plain contact).
// Layout preserved from SONG Ernest - CV v1, content rewritten for JD fit.
// ============================================================================

// ── Type scale (4 steps) ──
#let s        = 10pt
#let s-name   = 18pt
#let s-head   = 12pt
#let s-small  = 9pt
#let s-xsmall = 6.5pt

// ── Rhythm ──
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
        #text(s-small)[Phone] #h(6pt) #text(s-small)[#profile.tel]
        #v(gap)
        #text(s-small)[Address] #h(6pt) #text(s-small)[B-1000 Brussels]
        #v(gap)
        #text(s-small)[Email] #h(6pt) #text(s-small)[#profile.mailto]
        #v(gap)
        #text(s-small)[Web] #h(6pt) #text(s-small)[#profile.website]
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
            - Strategic finance
            - Financial modeling
            - Business planning
            - Valuation

            ==== ERP Implementation
            - SAP S/4HANA go-live
            - SAP HANA migration
            - SAP BPC

            ==== Business Intelligence
            - MS Power BI
            - QlikSense
            - Cognos
            - Business Objects

            ==== Change Management
            - Change transition
            - RPA adoption
            - Self-service BI

            ==== Financial Reporting
            - IFRS reporting
            - Consolidation
            - Variance analysis

            ==== Data & Analytics
            - SQL
            - VBA
            - R
          ],
          [
            ==== Budgeting & Forecasting
            - Budgeting & forecasting
            - Cash flow modeling
            - Variance analysis

            ==== Treasury & Financing
            - Cash exposure
            - Credit analysis
            - Debt/equity raises

            ==== Governance & Control
            - Internal control
            - Regulatory reporting
            - SOX context

            ==== Operations Partnering
            - Operations partnering
            - Cross-functional teams
            - Stakeholder management

            ==== M&A / Corporate Dev
            - Corporate development
            - M&A integration
            - Real estate acquisition
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
    keywords: "Director of Finance, Strategic finance, Financial modeling, Business planning, SAP S/4HANA, SAP HANA migration, Business Intelligence Power BI, Cognos, QlikSense, Budgeting & forecasting, Treasury, Change management, Cross-functional partnering, Stakeholder management, M&A, Corporate development",
    quote: "Director of Finance who bridges strategic finance and ERP transformation. I have led SAP S/4HANA go-live as a core Business Analyst, built budgeting & modeling from scratch, and rolled out strategic BI (Power BI, Cognos, Qliksense) that turns SAP data into executive decisions. My value is perspective: I have sat on both the operator's and the executive-recruiter's side of the table, so I pair rigorous financial modeling with change management that makes transformation stick across multi-site, multi-country operations."
  ),
  position: "Director of Finance — Strategic Finance & ERP Transformation",

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
  "Director of Finance — SAP S/4HANA Go-Live & Financial Control",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Guide the financial controlling pilot phase of the SAP S/4HANA migration, bridging IT architecture and strategic business operations as core Business Analyst.
    - Deliver a budgeting & forecasting model built from scratch within a 2-week window, replacing an unreliable legacy framework to protect operational continuity.
    - Automate month-end close for commodity trading, deploying PowerQuery ETL workflows that ingest 1,500+ bookings per close with zero manual intervention.
    - Reconcile middle-office (IVDB) data with SAP S/4HANA and simplify WDS project codes to strengthen portfolio monitoring and strategic variance analysis.
  ]
)

#v(gap)

#entry(
  "Director of Finance — ERP Migration & Strategic BI Reporting",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Drive data-informed operational restructuring post-M&A to improve productivity and post-integration performance.
    - Own the SAP HANA migration, restructuring data and guaranteeing system integrity for strategic consolidation reporting.
    - Lead Qliksense deployment to convert SAP data into executive Business Intelligence reporting and commercial insights.
    - Build rebate models (matrix and automated SAP) aligned to commercial strategy and liaise with auditors on rebate matters.
  ]
)

#v(gap)

#entry(
  "Strategic Finance Advisor — Cash Flow & Financial Modeling",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Design cash flow reporting and per-project cash exposure to support treasury and financing decisions.
    - Model financing needs, perform counterpart credit analysis and impairment testing for the local entity.
    - Build finance data models from SAP HANA and design Power BI strategic reporting to accelerate executive decisions.
  ]
)

#v(gap)

#entry(
  "Corporate Development — Investment & M&A Real Estate",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Manage real estate M&A including construction, redevelopment and acquisition of self-storage businesses.
    - Maintain a project dashboard and initiate corporate-development initiatives that improve departmental policies.
    - Design the data model and visualisation for the Investment department's Business Intelligence reporting.
    - Collaborate on an AI-based pricing model to strengthen commercial margin oversight and strategic positioning.
  ]
)

#v(gap)

#entry(
  "Interim CFO / Fundraising Consultant — Strategic Capital",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Act as interim CFO and raise strategic capital, arranging €3M in debt and equity financing.
    - Build long-term business plans, cash flow projections and financial goals under P&L oversight.
    - Monitor performance against plan and implement corrective actions to protect profitability.
    - Prepare operating-results reports and maintain financial models for ongoing strategic planning.
  ]
)

#v(gap)

#entry(
  "Director Business Process Automation — RPA & Self-Service BI",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Roll out a citizen-developer model using RPA and self-service BI, defining pricing strategy and roadmap.
    - Drive business development across marketing, pre-sales and sales to expand finance-operations offerings.
    - Implement process optimisation, standardisation and harmonisation to improve efficiency and profitability.
    - Establish change management structures to accelerate adoption of new processes and technology.
  ]
)

#v(gap)

#entry(
  "Founder — Non-Profit & Sustainability",
  "Soap collect",
  "January 2019", "Present",
  "Phnom Penh, KH",
  [
    - Establish a non-profit providing hygiene products to disadvantaged communities.
    - Partner with luxury hotel chains to source used soap for reconditioning and scale impact.
  ]
)

#v(gap)

#entry(
  "Managing Director & Head of Project Financial Modeling",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Deliver value creation with a valuation at 4 times acquisition cost across a concession portfolio.
    - Deploy airport operations across 50+ locations in multiple countries while managing accounting.
    - Build long-term financial business models incorporating macroeconomic impact, CapEx and concession valuation.
    - Negotiate concession contract extensions and improve budgeting and forecasting processes.
    - Manage financial reporting in line with BE-GAAP standards across operations.
  ]
)

#v(gap)

#entry(
  "Reporting Consolidation Manager — IFRS Strategic Reporting",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Lead IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries.
    - Spearhead SAP BPC and Cognos integration to strengthen strategic consolidation reporting.
    - Perform annual budgeting, monthly forecasting and variance analysis versus budgeted results.
    - Lead the strategic planning process for the organisation.
  ]
)

#v(gap)

#entry(
  "Financial Auditor Supervisor — Governance & Compliance",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Audit financial statements under various accounting standards, including SOX process testing.
    - Review financial modeling for long-term Public-Private Partnership contracts.
    - Certify FP7 grant agreements and lead supervised audit teams.
    - Develop partnerships and identify new markets to support business growth.
    - Cover main sectors: construction, real estate, water distribution, parcels distribution, security and healthcare.
  ]
)

#v(gap)

#entry(
  "Deputy CFO Trainee — Budgeting & Internal Control",
  "ICM - Brain & Spine Institute",
  "November 2009", "August 2010",
  "Paris, FR",
  [
    - Implement the budget system and prepare business plans for scientific teams.
    - Establish internal control for purchasing and donation processes and manage bank reconciliation.
    - Prepare the institutional audit supporting certification by the "Comité de la Charte".
  ]
)
