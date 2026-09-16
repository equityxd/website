// Icon-based CV using octique contact icons (ATS-label-friendly labels retained).
// CUSTOM CV — CV-20260916-0075_CV2.typ — "Director of Finance" (finance-transformation + reporting angle)

#import "@preview/octique:0.1.1": *;

// ── Type scale (4 steps) ──
#let s        = 10pt   // body base
#let s-name   = 18pt   // name (title, largest)
#let s-head   = 12pt   // position/subtitle + main section headings (h1)
#let s-small  = 9pt    // secondary: dates, subheadings, inline contact lines
#let s-xsmall = 6.5pt  // tighter: date headers

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
    // ─── BLOCK 1 : Title ───
    #align(center)[
      #text(s-name, weight: "bold")[#profile.name] #h(10pt) #text(s-name, style: "normal", "◆") #h(10pt) #text(s-name, style: "normal")[#position]
    ]
    #v(gap-m)
    #line(length: 100%, stroke: (thickness: 0.75pt))
    #v(gap)

    // ─── BLOCK 2 : Contact + Quote ───
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

    // ─── BLOCK 3 : Three columns ───
    #context[
      #let s-small = 8pt
      #grid(
        columns: (2.3fr, 3fr, 2.4fr),
        gutter: gutter,
        [
          // Education
          #text(s, weight: "semibold", style: "normal")[Education]
          #v(gap-m)
          #set text(size: 9pt)
          #education
        ],
        [
          // Competencies
          #text(s, weight: "semibold", style: "normal")[Competencies]
          #v(gap-m)
          #set text(size: 9pt)
          #grid(
            columns: (1fr, 1fr),
            gutter: 8pt,
            [
              ==== Financial Reporting
              - Monthly / quarterly reporting
              - IFRS / BE-GAAP consolidation
              - Board-ready packages

              ==== Budgeting & Forecasting
              - Annual budgeting
              - Rolling forecasts
              - Variance analysis

              ==== ERP & Automation
              - SAP S/4HANA
              - SAP HANA
              - PowerQuery ETL

              ==== Treasury & P&L
              - Cash flow / cash exposure
              - Financing & credit analysis
              - P&L oversight
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

              ==== Governance
              - Internal controls
              - SOX process testing
              - Regulatory reporting

              ==== Leadership
              - Cross-functional partnering
              - Stakeholder management
              - Change management
            ]
          )
        ],
        [
          // Languages, Interests, Interpersonal
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

    // ─── BLOCK 4 : Professional Experience ───
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
    keywords: "Finance Director, Financial Reporting, Budgeting & Forecasting, Variance Analysis, Month-end Close, Multi-entity Consolidation, SAP S/4HANA, Power BI, Treasury, Internal Controls, SOX, Change Management",
    quote: "Finance Director who owns the full planning and reporting cycle — annual budgeting, rolling forecasts, variance analysis and board-ready monthly/quarterly results. Over 15 years I have consolidated multi-entity outcomes on SAP S/4HANA / SAP HANA, automated the close with PowerQuery ETL, and turned BI dashboards (Power BI, Cognos) into executive decision support. I combine operator rigour with a translator's ability to bridge finance, IT and the business."
  ),
  position: "Finance Director",

  education: [
    #edu(
      "ESCP Business School",
      "(#1 FT 2026)",
      2010, 2011,
      "Paris, FR",
      "Specialized Master's degree",
      "Auditing and Consulting (internal controls, financial close)"
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
    ==== Financial Reporting
    - Monthly / quarterly reporting
    - IFRS / BE-GAAP consolidation
    - Board-ready packages

    ==== Budgeting & Forecasting
    - Annual budgeting
    - Rolling forecasts
    - Variance analysis

    ==== ERP & Automation
    - SAP S/4HANA
    - SAP HANA
    - PowerQuery ETL

    ==== Treasury & P&L
    - Cash flow / cash exposure
    - Financing & credit analysis
    - P&L oversight

    ==== Business Intelligence
    - MS Power BI
    - Cognos
    - QlikSense

    ==== Data & Analytics
    - SQL
    - VBA
    - R

    ==== Governance
    - Internal controls
    - SOX process testing
    - Regulatory reporting

    ==== Leadership
    - Cross-functional partnering
    - Stakeholder management
    - Change management
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
  "Finance Director — Financial Reporting & Month-end Close (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Direct month-end financial reporting across French subsidiaries while acting as the bridge between SAP S/4HANA architecture and business operations.
    - Engineered a PowerQuery ETL close that ingests 1,500+ bookings per close with zero manual intervention, eliminating prior human-error risk.
    - Reconciled middle-office (IVDB) data with SAP S/4HANA and restructured WDS project codes to strengthen portfolio monitoring.
    - Reconstructed a credible budgeting & forecasting baseline under a two-week deadline, safeguarding operational continuity during a resource gap.
  ],
  important: true
)

#v(gap)

#entry(
  "Finance Director — Multi-entity Consolidation & Reporting (Freelancer)",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Produced IFRS monthly/quarterly reporting for Asia-Pacific, Latin America and Canadian subsidiaries with a consistent, board-ready cadence.
    - Integrated SAP BPC and Cognos to consolidate multi-entity results across regions and steer the budget-to-variance cycle.
    - Championed the strategic planning process and aligned month-end reporting with executive decision needs.
  ]
)

#v(gap)

#entry(
  "Finance Director — Treasury, Cash Flow & Financing (Freelancer)",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Structured per-project cash exposure and cash-flow reporting to ground treasury and financing decisions in data.
    - Evaluated local financing needs and delivered counterpart credit analysis and impairment testing.
    - Constructed finance data models from SAP HANA and authored Power BI reporting that lifted cash visibility across leadership.
  ]
)

#v(gap)

#entry(
  "Interim CFO / Fundraising Consultant (Freelancer)",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Held P&L and treasury oversight as interim CFO while arranging €3M in debt/equity financing.
    - Authored cash-flow projections, business plans and long-term models, applying corrective actions where performance diverged.
    - Produced operating-results reports and sustained financial models for ongoing executive decision-support.
  ]
)

#v(gap)

#entry(
  "Financial Auditor Supervisor — Controls & Governance",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Audited financial statements under multiple accounting standards while testing key processes against SOX requirements.
    - Certified FP7 grant agreements for the EU Research program and supervised audit teams across construction, real estate and water.
    - Established stakeholder partnerships and opened new markets to underpin business growth.
  ]
)

#v(gap)

#entry(
  "Managing Director — Project Financial Modeling",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Generated value creation with valuation at 4 times acquisition cost across airport operations spanning 50+ locations.
    - Built long-term business models accounting for macroeconomic impact, capital expenditures and concession valuation.
    - Extended concession contracts and embedded improved budgeting and forecasting models to strengthen financial planning.
  ]
)
