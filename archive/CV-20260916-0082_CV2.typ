// Icon-based CV using octique contact icons (ATS-label-friendly labels retained).
// CUSTOM CV — CV-20260916-0082_CV2.typ — "Director of Finance" (strategic finance / P&L / treasury)

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
              - P&L responsibility
              - Budgeting & forecasting
              - Strategic planning

              ==== Treasury & Cash Flow
              - Cash exposure modelling
              - Financing needs assessment
              - Debt / equity fundraising

              ==== Financial Modeling
              - Business planning
              - Valuation / M&A
              - Investment dashboards

              ==== ERP & Process
              - SAP S/4HANA
              - SAP HANA
              - Process optimization

              ==== Business Intelligence
              - MS Power BI
              - Cognos
              - QlikSense

              ==== Data & Analytics
              - SQL
              - VBA
              - R
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
    keywords: "Director of Finance, P&L Responsibility, Strategic Finance, Treasury, Cash Flow Modelling, Fundraising, Financial Modeling, Valuation / M&A, SAP S/4HANA, Power BI, Budgeting & Forecasting, Strategic Planning",
    quote: "Director of Finance who has operated as interim CFO and strategic operator across BE, FR and NL. I carry P&L and treasury oversight, have raised €3M in debt/equity, and model long-term business cases — from concession valuation at 4x acquisition cost to per-project cash exposure. I combine a controller's discipline with an operator's outlook: rigorous Power BI / Cognos reporting, disciplined budgeting & forecasting, and a bias toward turning finance into a growth lever."
  ),
  position: "Director of Finance",

  education: [
    #edu(
      "ESCP Business School",
      "(#1 FT 2026)",
      2010, 2011,
      "Paris, FR",
      "Specialized Master's degree",
      "Auditing and Consulting (financial control & valuation)"
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
    - P&L responsibility
    - Budgeting & forecasting
    - Strategic planning

    ==== Treasury & Cash Flow
    - Cash exposure modelling
    - Financing needs assessment
    - Debt / equity fundraising

    ==== Financial Modeling
    - Business planning
    - Valuation / M&A
    - Investment dashboards

    ==== ERP & Process
    - SAP S/4HANA
    - SAP HANA
    - Process optimization

    ==== Business Intelligence
    - MS Power BI
    - Cognos
    - QlikSense

    ==== Data & Analytics
    - SQL
    - VBA
    - R
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
  "Director of Finance — Treasury & Cash Flow (Freelancer)",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Designed per-project cash exposure and cash-flow reporting to give treasury and financing decisions a data-backed basis.
    - Assessed local financing needs and performed counterpart credit analysis and impairment testing.
    - Built finance data models from SAP HANA and designed Power BI reporting to surface cash visibility to leadership.
  ],
  important: true
)

#v(gap)

#entry(
  "Director of Finance — Interim CFO / Fundraising (Freelancer)",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Held P&L and treasury oversight as interim CFO, arranging €3M in debt/equity financing.
    - Built cash-flow projections, business plans and long-term financial models, monitoring performance and applying corrective actions.
    - Prepared operating-results reports and maintained financial models for ongoing executive decision-support.
  ]
)

#v(gap)

#entry(
  "Director of Finance — Strategic Valuation & Business Modeling, Vinci Airports",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Drove value creation with valuation at 4 times acquisition cost across airport operations at 50+ locations in multiple countries.
    - Developed long-term financial business models covering macroeconomic impact, capital expenditures and concession valuation.
    - Negotiated concession contract extensions and implemented new financial models to improve budgeting and forecasting.
  ]
)

#v(gap)

#entry(
  "Director of Finance — Investment & Corporate Development (Freelancer)",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Analyzed and managed real-estate projects including construction, redevelopment and acquisition of self-storage businesses.
    - Designed the data model and visualization for the Investment department's Business Intelligence dashboard.
    - Collaborated on a new pricing model using Artificial Intelligence.
  ]
)

#v(gap)

#entry(
  "Director of Finance — Financial Reporting & Consolidation (Freelancer)",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Delivered IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries on a board-ready monthly/quarterly cadence.
    - Integrated SAP BPC and Cognos reporting to consolidate multi-entity results and drive the budgeting, forecasting and variance cycle.
    - Led the strategic planning process and aligned reporting with executive decision-support.
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
    - Certified FP7 grant agreements for the EU Research program and led supervised audit teams across construction, real estate and water sectors.
    - Built stakeholder partnerships and identified new markets to support business growth.
  ]
)
