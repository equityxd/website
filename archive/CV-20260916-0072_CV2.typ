// Icon-based CV using octique contact icons. Layout preserved from SONG Ernest - CV v1.
// CUSTOM CV — CV-20260916-0072_CV2.typ — "Director of Finance" (strategic finance & ERP transformation)

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
            ==== ERP Transformation
            - SAP S/4HANA
            - SAP HANA
            - SAP BPC

            ==== Strategic Finance
            - Budgeting & forecasting
            - Financial modeling
            - Valuation

            ==== Business Intelligence
            - MS Power BI
            - Cognos
            - QlikSense
          ],
          [
            ==== Strategic Planning
            - Strategic planning
            - P&L-adjacent decisions
            - Capital expenditures

            ==== Change Management
            - GAP analysis
            - AS-IS → TO-BE design
            - Stakeholder management

            ==== Data & Analytics
            - SQL
            - VBA
            - R
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
    keywords: "Director of Finance, Strategic Finance, ERP Transformation, SAP S/4HANA, SAP HANA, Budgeting & Forecasting, Valuation, Strategic Planning, Change Management, Business Intelligence, Stakeholder Management, Financial Modeling, Capital Expenditures",
    quote: "Director of Finance positioned at the intersection of strategic finance and ERP transformation. I bridge IT architecture and business operations as a core Business Analyst on SAP S/4HANA (Engie SEM) and SAP HANA (Holcim) migrations, and I build long-term business, cash-flow and concession models that inform budgeting, forecasting and capital-allocation decisions. I roll out Power BI / Cognos executive reporting, lead change management with structured AS-IS → TO-BE design, and partner cross-functionally from the board down."
  ),
  position: "Director of Finance — Strategic Finance & ERP Transformation",

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
    ==== ERP Transformation
    - SAP S/4HANA
    - SAP HANA
    - SAP BPC

    ==== Strategic Finance
    - Budgeting & forecasting
    - Financial modeling
    - Valuation

    ==== Business Intelligence
    - MS Power BI
    - Cognos
    - QlikSense

    ==== Strategic Planning
    - Strategic planning
    - P&L-adjacent decisions
    - Capital expenditures

    ==== Change Management
    - GAP analysis
    - AS-IS → TO-BE design
    - Stakeholder management

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

= Professional Experience

#v(gap)

#entry(
  "Director of Finance — ERP Transformation (Freelancer)",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Directed the SAP HANA migration, restructuring data and guaranteeing system integrity across the finance function.
    - Built rebate models (matrix & automated SAP) tightly aligned with commercial strategy and top-line performance.
    - Rolled out Qliksense with refreshed data to drive financial reporting and executive decision-support.
    - Safeguarded data reliability and acted as the interface with auditors on rebate matters.
  ],
  important: true
)

#entry(
  "Director of Finance — Strategic Business Analysis (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Bridged IT architecture and strategic business operations as the core Business Analyst on the SAP S/4HANA migration across French subsidiaries.
    - Established change-management structures and adoption strategies to ensure successful rollout of new finance processes.
    - Simplified WDS project codes to strengthen portfolio monitoring and reporting fidelity.
  ]
)

#entry(
  "Director of Finance — Investment & Corporate Development (Freelancer)",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Analyzed and managed real-estate projects covering construction, redevelopment and acquisition of self-storage businesses.
    - Maintained a project dashboard and launched corporate-development initiatives to improve policies and procedures.
    - Designed the data model and visualization for the Investment department's Business Intelligence effort, plus an AI-based pricing model.
  ]
)

#entry(
  "Director of Finance — Strategic Planning (Freelancer)",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Led the strategic planning process and reconciled actuals against budgeted/estimated results through monthly forecasting.
    - Integrated SAP BPC and Cognos reporting to consolidate multi-entity results for executive decision-support.
    - Delivered IFRS financial reporting across Asia-Pacific, Latin America and Canadian subsidiaries.
  ]
)

#entry(
  "Director of Finance — Valuation & Capital Allocation (Freelancer)",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Created value at 4 times acquisition cost through disciplined capital allocation and concession valuation.
    - Developed long-term financial business models incorporating macroeconomic impact and capital expenditures.
    - Negotiated concession contract extensions and implemented new financial models to improve budgeting and forecasting.
  ]
)
