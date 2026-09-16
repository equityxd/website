// Icon-based CV using octique contact icons (ATS-label-friendly labels retained).
// CUSTOM CV — CV-20260916-0075_CV3.typ — "Director of Finance" (strategic finance & growth angle)

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
              ==== Strategic Finance
              - Budgeting & forecasting
              - Financial modeling
              - Strategic planning

              ==== Financial Reporting
              - Monthly reporting
              - Quarterly reporting
              - IFRS / BE-GAAP

              ==== ERP Implementation
              - SAP S/4HANA
              - SAP HANA
              - SAP BPC

              ==== Growth & M&A
              - Corporate development
              - Valuation modeling
              - Post-M&A integration

              ==== Treasury
              - Cash exposure
              - Financing structuring
              - Credit analysis

              ==== BI & Dashboards
              - MS Power BI
              - Cognos
              - QlikSense
            ],
            [
              ==== Data & Analytics
              - SQL
              - VBA
              - R

              ==== Close & Controls
              - Month-end close
              - Internal controls
              - SOX testing

              ==== Regulatory & Governance
              - Regulatory reporting
              - Governance
              - Audit management

              ==== Leadership
              - Cross-functional partnering
              - Stakeholder management
              - Team leadership
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
    keywords: "Director of Finance, Strategic Finance, Financial Modeling, Budgeting & Forecasting, Financial Reporting, M&A / Corporate Development, SAP S/4HANA, Power BI, Cash Flow Management, Multi-entity Consolidation, Variance Analysis, Change Management",
    quote: "Strategic finance leader with 15+ years spanning budgeting & forecasting, financial modeling, multi-entity consolidation and growth / M&A. I turn SAP S/4HANA / SAP HANA data into Power BI decision support, protect the P&L as interim CFO (€3M debt/equity raised), and create valuation — delivering four times acquisition cost across 50+ sites. I pair rigor with a translator's instinct, turning finance into a measurable lever for growth."
  ),
  position: "Director of Finance — Strategic Finance & Growth",

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

  competencies: [
    ==== Strategic Finance
    - Budgeting & forecasting
    - Financial modeling
    - Strategic planning

    ==== Financial Reporting
    - Monthly reporting
    - Quarterly reporting
    - IFRS / BE-GAAP

    ==== ERP Implementation
    - SAP S/4HANA
    - SAP HANA
    - SAP BPC

    ==== Growth & M&A
    - Corporate development
    - Valuation modeling
    - Post-M&A integration

    ==== Treasury
    - Cash exposure
    - Financing structuring
    - Credit analysis

    ==== BI & Dashboards
    - MS Power BI
    - Cognos
    - QlikSense

    ==== Data & Analytics
    - SQL
    - VBA
    - R

    ==== Close & Controls
    - Month-end close
    - Internal controls
    - SOX testing

    ==== Regulatory & Governance
    - Regulatory reporting
    - Governance
    - Audit management

    ==== Leadership
    - Cross-functional partnering
    - Stakeholder management
    - Team leadership
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
  "Strategic Finance & Automation Lead — Reporting / Close (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Steer month-end financial close across French subsidiaries as the bridge between SAP S/4HANA architecture and business operations.
    - Automate the commodity-trading close with PowerQuery ETL workflows that ingest 1,500+ bookings per close with zero manual intervention.
    - Reconcile middle-office (IVDB) data with SAP S/4HANA and simplify WDS project codes to improve portfolio monitoring.
    - Restore a credible budgeting & forecasting baseline within a 2-week window, protecting operational continuity through a resource gap.
  ],
  important: true
)

#v(gap)

#entry(
  "Strategic Finance — Reporting, Consolidation & Planning (Freelancer)",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Own board-ready monthly and quarterly IFRS reporting across Asia-Pacific, Latin America and Canadian subsidiaries.
    - Drive multi-entity consolidation via SAP BPC and Cognos reporting across regions and manage the budget-to-variance cycle.
    - Lead the strategic planning process and connect month-end reporting to executive decision-support needs.
  ]
)

#v(gap)

#entry(
  "Strategic Finance — Cash Flow & Financing (Freelancer)",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Model per-project cash exposure and cash-flow reporting to underpin treasury and financing decisions.
    - Assess local financing needs and deliver counterpart credit analysis and impairment testing.
    - Build finance data models from SAP HANA and author Power BI reporting that improves cash visibility.
  ]
)

#v(gap)

#entry(
  "Interim CFO / Fundraising Consultant (Freelancer)",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Provide P&L and treasury oversight as interim CFO while raising €3M in debt/equity financing.
    - Author cash-flow projections, business plans and long-term models, applying corrective actions where performance slips.
    - Prepare operating-results reports and maintain financial models for sustained executive decision-support.
  ]
)

#v(gap)

#entry(
  "Financial Auditor Supervisor — Controls & Governance",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Audit financial statements under multiple accounting standards while testing key processes against SOX requirements.
    - Certify FP7 grant agreements for the EU Research program and lead supervised audit teams across construction, real estate and water.
    - Build stakeholder partnerships and open new markets to drive business growth.
  ]
)

#v(gap)

#entry(
  "Managing Director — Project Financial Modeling & Value Creation",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Create value with valuation at 4 times acquisition cost across airport operations at 50+ locations across multiple countries.
    - Develop long-term financial business models that capture macroeconomic impact, capital expenditures and concession valuation.
    - Extend concession contracts and deploy improved financial models to strengthen budgeting and forecasting.
  ]
)
