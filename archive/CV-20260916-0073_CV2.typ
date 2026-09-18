// Icon-based CV using octique contact icons (ATS-label-friendly labels retained).
// CUSTOM CV — CV-20260916-0073_CV2.typ — "Director of Finance" (budgeting / forecasting / P&L / strategic finance)

#import "@preview/octique:0.1.1": *;

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
  profile: (name, address, mailto, website, tel, keywords, quote),
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
    #align(center)[
      #text(s-name, weight: "bold")[#profile.name] #h(10pt) #text(s-name, style: "normal", "◆") #h(10pt) #text(s-name, style: "normal")[#position]
    ]
    #v(gap-m)
    #line(length: 100%, stroke: (thickness: 0.75pt))
    #v(gap)

    #grid(
      columns: (1.1fr, 2.9fr),
      gutter: gutter,
      [
        #octique-inline("location", width: 0.6em) #text(s-small)[Address: Rue Montagne de l'Oratoire 28/76, B-1000 Brussels]
        #v(gap)
        #octique-inline("mail", width: 0.6em) #text(s-small)[Email: #profile.mailto]
        #v(gap)
        #octique-inline("globe", width: 0.6em) #text(s-small)[Web: #profile.website]
        #v(gap)
        #octique-inline("device-mobile", width: 0.6em) #text(s-small)[Phone: #profile.tel]
      ],
      [
        #set par(justify: true)
        #set text(hyphenate: true)
        #text(size: 9pt, style: "italic")[#profile.quote]
      ]
    )
    #line(length: 100%, stroke: (thickness: 0.75pt))
    #v(gap)

    #context[
      #let s-small = 8pt
      #grid(
        columns: (2.3fr, 3fr, 2.4fr),
        gutter: gutter,
        [
          #text(s, weight: "semibold", style: "normal")[Education]
          #v(gap-m)
          #set text(size: 9pt)
          #education
        ],
        [
          #text(s, weight: "semibold", style: "normal")[Competencies]
          #v(gap-m)
          #set text(size: 9pt)
          #grid(
            columns: (1fr, 1fr),
            gutter: 8pt,
            [
              ==== Budgeting & Forecasting
              - Annual budgeting & rolling forecasts
              - Variance analysis (actual vs budget)
              - Strategic planning

              ==== P&L Leadership
              - P&L responsibility / P&L-adjacent oversight
              - Treasury & financing needs
              - Cash flow / cash exposure

              ==== Strategic Finance
              - Financial modeling
              - M&A / corporate development
              - Concession valuation

              ==== ERP / Operations
              - SAP S/4HANA
              - SAP HANA
              - Multi-entity GL / AP / AR
            ],
            [
              ==== Business Intelligence
              - MS Power BI
              - Cognos
              - QlikSense

              ==== Data & Analytics
              - SQL
              - VBA
              - R

              ==== Controls & Governance
              - Internal controls
              - SOX process testing
              - Regulatory reporting

              ==== Leadership
              - Team leadership
              - Stakeholder management
              - Cross-functional partnering
            ]
          )
        ],
        [
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

    #body
  ]
}

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
    keywords: "Director of Finance, Budgeting & Forecasting, Variance Analysis, P&L Responsibility, Strategic Finance, Financial Modeling, Multi-entity GL, Treasury, Cash Flow, M&A, Business Intelligence, SAP S/4HANA, US GAAP Ramp",
    quote: "Director of Finance with 15+ years spanning budgeting & forecasting, P&L-adjacent oversight, and multi-entity financial reporting across BE, FR and NL. I own the full planning cycle — from annual budget and rolling forecasts to variance analysis — and translate consolidated IFRS / BE-GAAP numbers into board-ready decision support. My edge is dual perspective: I've sat on both the operator's and the executive-recruiter's side of the table, so I partner confidently across finance, IT and the business to protect the P&L and grow revenue."
  ),
  position: "Strategic Finance Director",

  education: [
    #edu(
      "ESCP Business School",
      "(#1 FT 2026)",
      2010, 2011,
      "Paris, FR",
      "Specialized Master's degree",
      "Auditing and Consulting (internal controls & governance)"
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

  competencies: [
    ==== Budgeting & Forecasting
    - Annual budgeting & rolling forecasts
    - Variance analysis (actual vs budget)
    - Strategic planning

    ==== P&L Leadership
    - P&L responsibility / P&L-adjacent oversight
    - Treasury & financing needs
    - Cash flow / cash exposure

    ==== Strategic Finance
    - Financial modeling
    - M&A / corporate development
    - Concession valuation

    ==== ERP / Operations
    - SAP S/4HANA
    - SAP HANA
    - Multi-entity GL / AP / AR

    ==== Business Intelligence
    - MS Power BI
    - Cognos
    - QlikSense

    ==== Data & Analytics
    - SQL
    - VBA
    - R

    ==== Controls & Governance
    - Internal controls
    - SOX process testing
    - Regulatory reporting

    ==== Leadership
    - Team leadership
    - Stakeholder management
    - Cross-functional partnering
  ],

  languages: [
    #text(s-small, weight: "semibold", style: "normal")[Native:] French, Khmer, Teochew \
    #text(s-small, weight: "semibold", style: "normal")[Proficient:] English \
    #text(s-small, weight: "semibold", style: "normal")[Basics:] Dutch (A2), Spanish, Mandarin \
  ],

  interests: [
    Sustainable development, Powerlifting, Mountain biking, Tennis
  ],

  interpersonal: [
    Fast-learner, Problem solver, Diplomacy, Driven, Autonomous, Teamplayer
  ],

  body
)

// ── Professional Experience ──
= Professional Experience

#v(gap)

#entry(
  "Strategic Finance Director — Budgeting & Forecasting (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Rebuilt the budgeting & forecasting baseline from scratch inside a 2-week window, restoring a trustworthy planning tool during a resource gap.
    - Own month-end financial reporting while bridging SAP S/4HANA migration architecture with strategic business operations as core Business Analyst.
    - Automated the commodity-trading close with PowerQuery ETL workflows, ingesting 1,500+ bookings per close with zero manual intervention.
    - Reconciled middle-office (IVDB) data with SAP S/4HANA and simplified WDS project codes to strengthen portfolio monitoring.
  ],
  important: true
)

#v(gap)

#entry(
  "Strategic Finance Director — Strategic Planning & Consolidation (Freelancer)",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Led the strategic planning process and executed annual budgeting against a monthly/quarterly reporting cadence across Asia-Pacific, Latin America and Canadian subsidiaries.
    - Consolidated multi-entity results via SAP BPC and Cognos reporting, driving the budget-to-variance cycle.
    - Delivered IFRS financial reporting for board-ready decision support across multiple geographies.
  ]
)

#v(gap)

#entry(
  "Strategic Finance Director — P&L & Treasury (Freelancer)",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Exercised P&L-adjacent oversight as interim CFO, arranging €3M in debt/equity financing to fund growth.
    - Built cash-flow projections, business plans and long-term financial models, applying corrective actions when performance deviated.
    - Prepared operating-results reports and sustained financial models for ongoing executive decision-support.
  ]
)

#v(gap)

#entry(
  "Managing Director — Project Financial Modeling & Value Creation",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Delivered value creation with valuation at 4 times acquisition cost across airport operations at 50+ locations in multiple countries.
    - Developed long-term financial business models covering macroeconomic impact, capital expenditures and concession valuation.
    - Negotiated concession contract extensions and embedded new financial models to improve budgeting and forecasting.
  ]
)

#v(gap)

#entry(
  "Financial Auditor Supervisor — Controls & Governance",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Audited financial statements under multiple accounting standards, testing key processes in accordance with SOX requirements.
    - Certified FP7 grant agreements for the EU Research program and led supervised audit teams.
    - Built stakeholder partnerships and identified new markets to support business growth.
  ]
)

#v(gap)

#entry(
  "Director Business Process Automation — BI & RPA",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Led a citizen-developer business model using RPA and self-service BI, including pricing strategy and roadmap.
    - Managed business development, pre-sales and sales, identifying new opportunities to expand margin.
    - Established change management structures to drive adoption of new processes and reporting technologies.
  ]
)
