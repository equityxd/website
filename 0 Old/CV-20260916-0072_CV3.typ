// Icon-based CV using octique contact icons. Layout preserved from SONG Ernest - CV v1.
// CUSTOM CV — CV-20260916-0072_CV3.typ — "Director of Finance" (plant & operations partnering)

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
  profile: (
    name: str, address: str, mailto: str, website: str, tel: str,
    keywords: none, quote: str,
  ),
  position: str,
  education: none, competencies: none, languages: none,
  interests: none, interpersonal: none, body
) = {
  set document(author: profile.name, keywords: profile.keywords, date: auto)
  set text(s, font: "Source Sans 3", lang: "en")
  set par(leading: s * 0.7)
  set align(left)
  set list(body-indent: indent, tight: true)

  show heading.where(level: 1): body => [
    #line(length: 100%, stroke: (thickness: 0.5pt))
    #v(gap) #text(s-head, weight: "bold", style: "normal")[#body] #v(gap-m)
  ]
  show heading.where(level: 3): body => [
    #text(s, weight: "semibold", style: "normal")[#body]
    #v(gap-m) #line(length: 100%, stroke: (thickness: 0.3pt)) #v(gap-m)
  ]
  show heading.where(level: 4): body => [
    #text(s-small, weight: "semibold", style: "italic")[#body]
  ]

  set page(
    paper: "a4", margin: page-margin,
    footer: context [ #set align(right) #set text(s-small)
      #counter(page).display("1 of 1", both: true) ]
  )

  [
    #align(center)[
      #text(s-name, weight: "bold")[#profile.name] #h(10pt) #text(s-name, style: "normal", "◆") #h(10pt) #text(s-name, style: "normal")[#position]
    ]
    #v(gap-m) #line(length: 100%, stroke: (thickness: 0.75pt)) #v(gap)

    #grid(columns: (1.1fr, 2.9fr), gutter: gutter,
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
        #set par(justify: true) #set text(hyphenate: true)
        #text(size: 9pt, style: "italic")[#profile.quote]
      ]
    )
    #line(length: 100%, stroke: (thickness: 0.75pt)) #v(gap)

    #context[
      #let s-small = 8pt
      #grid(columns: (2.3fr, 3fr, 2.4fr), gutter: gutter,
      [
        #text(s, weight: "semibold", style: "normal")[Education]
        #v(gap-m) #set text(size: 9pt) #education
      ],
      [
        #text(s, weight: "semibold", style: "normal")[Competencies]
        #v(gap-m) #set text(size: 9pt)
        #grid(columns: (1fr, 1fr), gutter: 8pt,
          [
            ==== Operations Partnering
            - Multi-site finance
            - P&L oversight
            - Treasury

            ==== ERP & Data
            - SAP S/4HANA
            - SAP HANA
            - MS Power BI

            ==== Reporting
            - Financial reporting
            - Management reporting
            - dashboards
          ],
          [
            ==== Budgeting & Forecasting
            - Budgeting & forecasting
            - Cash flow management
            - CapX planning

            ==== Controls & Governance
            - Internal controls
            - SOX process testing
            - IFRS / BE-GAAP

            ==== Agile & Analytics
            - Jira
            - Confluence
            - SQL
          ]
        )
      ],
      [
        #text(s, weight: "semibold", style: "normal")[Languages]
        #v(gap-m) #set text(size: 9pt) #languages
        #v(gap-m)
        #text(s, weight: "semibold", style: "normal")[Interests]
        #v(gap-m) #set text(size: 9pt) #interests
        #v(gap-m)
        #text(s, weight: "semibold", style: "normal")[Interpersonal]
        #v(gap-m) #set text(size: 9pt) #interpersonal
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
    #if details != none { text(s-small, style: "italic")[#details] }
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
    #if rank != none { linebreak() text(s-small, style: "normal")[#rank] }
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
    keywords: "Director of Finance, Operations Partnering, Multi-site Finance, P&L Oversight, Treasury, Cash Flow, SAP S/4HANA, Power BI, Financial Reporting, Budgeting & Forecasting, SOX, Internal Controls, IFRS / BE-GAAP",
    quote: "Director of Finance focused on plant and operations partnering across multi-site, multi-country footprint. I operated finance across 50+ airport locations in multiple countries (Vinci Airports) under P&L and treasury oversight, and I ran interim CFO duties at Magnetrap arranging €3M in debt/equity financing. I combine strong month-end close leadership, SAP S/4HANA / SAP HANA consolidation, and Power BI management reporting with disciplined budgeting, forecasting and capital-planning — delivered as a trusted business partner from the shop floor to the board."
  ),
  position: "Director of Finance — Plant & Operations Partnering",

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
    ==== Operations Partnering
    - Multi-site finance
    - P&L oversight
    - Treasury

    ==== ERP & Data
    - SAP S/4HANA
    - SAP HANA
    - MS Power BI

    ==== Reporting
    - Financial reporting
    - Management reporting
    - dashboards

    ==== Budgeting & Forecasting
    - Budgeting & forecasting
    - Cash flow management
    - CapX planning

    ==== Controls & Governance
    - Internal controls
    - SOX process testing
    - IFRS / BE-GAAP

    ==== Agile & Analytics
    - Jira
    - Confluence
    - SQL
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

= Professional Experience

#v(gap)

#entry(
  "Director of Finance — Operations Partnering (Freelancer)",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Operated finance across airport operations at 50+ locations in multiple countries as Managing Director & Head of Project Financial Modeling.
    - Managed accounting and financial reporting in accordance with BE-GAAP standards across a multi-country footprint.
    - Implemented new financial business models to improve budgeting and forecasting across distributed operations.
  ],
  important: true
)

#entry(
  "Director of Finance — Process Automation & Operations (Freelancer)",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Led a citizen-developer business model using RPA and self-service BI, setting pricing strategy and roadmap.
    - Drove business development across marketing, pre-sales and sales, and identified new opportunities.
    - Applied process optimization, standardization and harmonization to improve efficiency and profitability for customers.
  ]
)

#entry(
  "Director of Finance — Cost Control Reporting (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Provided tailored reports helping customers monitor and control costs for data-driven operational decisions.
    - Established change-management structures to accelerate adoption of new operational and finance processes.
    - Supported the SAP S/4HANA pilot as core Business Analyst bridging IT architecture and business operations.
  ]
)

#entry(
  "Director of Finance — Internal Controls & Governance (Freelancer)",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Audited financial statements under multiple standards, testing key processes in accordance with SOX requirements.
    - Certified FP7 grant agreements and led supervised audit teams across construction, real estate and water sectors.
    - Strengthened internal controls and built stakeholder partnerships to support business growth.
  ]
)

#entry(
  "Director of Finance — Treasury (Freelancer)",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Operated under P&L and treasury oversight as interim CFO, arranging €3M in debt/equity financing.
    - Built cash-flow projections and business plans, monitoring performance and applying corrective actions.
    - Maintained operating-results reporting and financial models for ongoing executive decision-support.
  ]
)
