// ============================================================================
// Serial CV-20260916-0081 — CV1
// Target Role: Chief Growth & Transformation Officer
// Positioning: TRANSFORMATION-LEADERSHIP emphasis — ERP, process automation,
//   change management. Layout preserved from SONG Ernest - CV v1, content
//   rewritten for JD fit. ATS-friendly (plain contact rows).
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
            ==== Transformation
            - ERP transformation
            - SAP S/4HANA
            - SAP HANA
            - Process automation
            - RPA (UIPath, PowerAutomate)

            ==== Growth & Commercial
            - Pricing strategy
            - Business development
            - Fundraising / capital raising
            - Value creation / valuation
            - Go-to-market partnership

            ==== Business Intelligence
            - MS Power BI
            - Cognos
            - QlikSense
            - Business Objects
            - Hyperion
          ],
          [
            ==== P&L & Finance Leadership
            - P&L oversight
            - Budgeting & forecasting
            - Cash flow management
            - Multi-entity consolidation
            - Governance & internal control

            ==== Change & Delivery
            - Change management
            - Strategic planning
            - Jira
            - Confluence
            - Cross-functional leadership
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
    ]
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
    keywords: "Chief Growth & Transformation Officer, Transformation leadership, ERP transformation, SAP S/4HANA, SAP HANA, Process automation, RPA, Power Automate, UIPath, Change management, P&L oversight, Multi-entity consolidation, Business Intelligence, Power BI, Cognos, Strategic planning, Budgeting & forecasting, Stakeholder management",
    quote: "Chief Growth & Transformation Officer with 15+ years turning complex, multi-entity, multi-country finance operations into scaled growth engines. I lead transformation end to end — from AS-IS diagnosis through SAP S/4HANA / SAP HANA go-live — while automating the month-end close and shipping executive Power BI dashboards that leaders act on. What sets me apart is perspective: I've operated as Business Analyst, interim CFO, process-automation director and founder, so I align IT architecture, commercial strategy and board-level governance into one executable roadmap."
  ),
  position: "Chief Growth & Transformation Officer",

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
  "Growth & Transformation Lead — SAP S/4HANA Migration",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Lead transformation of financial controlling across French subsidiaries, acting as the core Business Analyst that bridges IT architecture and strategic business operations during the SAP S/4HANA migration.
    - Ship an automated month-end close for commodity trading, deploying PowerQuery ETL workflows that safely ingest 1,500+ bookings per close with zero manual intervention.
    - Build a budgeting & forecasting model from scratch within a 2-week window to protect operational continuity and replace an unreliable legacy framework.
    - Reconcile middle-office (IVDB) data with SAP S/4HANA and simplify WWS project codes to strengthen portfolio monitoring and decision support.
  ]
)

#v(gap)

#entry(
  "Operations & Transformation Lead — M&A Integration, SAP HANA",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Drive post-M&A operational restructuring using market and financial data to raise productivity across consolidated entities.
    - Lead the SAP HANA migration, restructuring data and guaranteeing system integrity across multi-entity consolidation reporting.
    - Build rebate models (matrix and automated SAP) aligned to commercial strategy and liaison with auditors on rebate matters.
    - Roll out QlikSense financial reporting to turn SAP data into executive insights that accelerate decisions.
  ]
)

#v(gap)

#entry(
  "Cash Flow & Financial Modeling — Treasury Advisory",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Design cash flow reporting and per-project cash exposure to inform treasury and financing decisions.
    - Assess financing needs, perform counterpart credit analysis and impairment testing for the local entity.
    - Build finance data models from SAP HANA and design Power BI reporting to accelerate decision-making.
  ]
)

#v(gap)

#entry(
  "Investment & Corporate Development — Commercial & Pricing",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Analyse real estate projects including construction, redevelopment and acquisition of self-storage businesses.
    - Maintain a project dashboard and initiate corporate-development initiatives that improve departmental policies and procedures.
    - Design the data model and visualisation for the Investment department's Business Intelligence reporting.
    - Collaborate on an AI-based pricing model to strengthen commercial margin oversight and commercial growth.
  ]
)

#v(gap)

#entry(
  "Interim CFO / Fundraising Consultant — Capital Raising",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Serve as interim CFO and lead fundraising, arranging €3M in debt and equity financing.
    - Prepare cash flow projections, business plans and long-term financial goals under P&L oversight.
    - Monitor performance metrics and implement corrective actions to protect profitability.
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
    - Launch a citizen-developer model using RPA and self-service BI, defining pricing strategy and roadmap.
    - Drive business development across marketing, pre-sales and sales to grow commercial reach.
    - Standardise and harmonise processes to improve efficiency and profitability for clients.
    - Deliver cost-control reporting and establish change management structures to accelerate adoption.
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
    - Partner with luxury hotel chains to source used soap for reconditioning and scale positive impact.
  ]
)

#v(gap)

#entry(
  "Managing Director & Head of Project Financial Modeling",
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
  "Reporting Consolidation Manager — IFRS Financial Reporting",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Lead IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries.
    - Integrate SAP BPC and Cognos reporting systems to strengthen consolidation.
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
