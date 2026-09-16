// Icon-based CV using octique contact icons (ATS-label-friendly labels retained).
// CUSTOM CV — CV-20260916-0073_CV3.typ — "Director of Finance" (Business Intelligence / ERP transformation / treasury)

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
              ==== Business Intelligence
              - MS Power BI dashboards
              - Cognos reporting
              - QlikSense

              ==== ERP Transformation
              - SAP S/4HANA migration
              - SAP HANA consolidation
              - Business Objects

              ==== Treasury & Cash Management
              - Cash flow / cash exposure
              - Financing needs / credit analysis
              - Treasury oversight

              ==== Data & Analytics
              - SQL
              - VBA
              - R
            ],
            [
              ==== Reporting & Close
              - Month-end / financial close
              - IFRS / BE-GAAP reporting
              - Monthly & quarterly cadence

              ==== P&L & Strategic Finance
              - Budgeting & forecasting
              - Financial modeling
              - M&A / corporate development

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
    keywords: "Director of Finance, Business Intelligence, Power BI, Cognos, QlikSense, SAP S/4HANA, ERP Transformation, Treasury, Cash Flow Management, Financial Reporting, Month-end Close, Financial Modeling, US GAAP Ramp",
    quote: "Director of Finance with 15+ years turning raw finance data into board-ready decision support. I design and deploy Business Intelligence dashboards (Power BI, Cognos, QlikSense), lead SAP S/4HANA / SAP HANA transformations from AS-IS diagnosis to go-live, and own treasury and cash-flow visibility for multi-entity operations across BE, FR and NL. What sets me apart is a translator's mindset: I bridge IT architecture and the business, automating month-end close while keeping P&L and governance at the centre of every decision."
  ),
  position: "Director of Finance — BI & ERP Transformation",

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
    ==== Business Intelligence
    - MS Power BI dashboards
    - Cognos reporting
    - QlikSense

    ==== ERP Transformation
    - SAP S/4HANA migration
    - SAP HANA consolidation
    - Business Objects

    ==== Treasury & Cash Management
    - Cash flow / cash exposure
    - Financing needs / credit analysis
    - Treasury oversight

    ==== Reporting & Close
    - Month-end / financial close
    - IFRS / BE-GAAP reporting
    - Monthly & quarterly cadence

    ==== P&L & Strategic Finance
    - Budgeting & forecasting
    - Financial modeling
    - M&A / corporate development

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
  "Director of Finance — BI Dashboard & Treasury (Freelancer)",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Designed per-project cash exposure and cash-flow reporting to give treasury and financing decisions a data-backed basis.
    - Assessed local financing needs and performed counterpart credit analysis and impairment testing.
    - Built finance data models from SAP HANA and designed Power BI dashboards to surface cash visibility to leadership.
  ],
  important: true
)

#v(gap)

#entry(
  "Director of Finance — Business Intelligence (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Own month-end financial reporting while bridging SAP S/4HANA migration architecture with business operations as core Business Analyst.
    - Automated the commodity-trading close with PowerQuery ETL workflows, ingesting 1,500+ bookings per close with zero manual intervention.
    - Designed and deployed an automated budget modeling tool from scratch within a 2-week timeline, preserving operational continuity.
    - Reconciled middle-office (IVDB) data with SAP S/4HANA and simplified WDS project codes to strengthen portfolio monitoring.
  ]
)

#v(gap)

#entry(
  "Director of Finance — ERP Reporting Integration (Freelancer)",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Spearheaded the integration of SAP BPC and Cognos reporting to consolidate multi-entity results for a board-ready cadence.
    - Delivered IFRS financial reporting across Asia-Pacific, Latin America and Canadian subsidiaries.
    - Conducted annual budgeting, monthly forecasting and variance analysis against budgeted results.
  ]
)

#v(gap)

#entry(
  "Founder — Business Intelligence & Pricing (AI) (Non-profit)",
  "Soap Collect",
  "January 2019", "Present",
  "Phnom Penh, KH",
  [
    - Established a non-profit organisation sourcing used soap from luxury hotel chains to recondition and redistribute to disadvantaged communities.
    - Co-developed a new AI-driven pricing model to optimise cost and distribution reach.
    - Maintained a project dashboard to track programme impact and corporate-development milestones.
  ]
)

#v(gap)

#entry(
  "Director Business Process Automation — RPA & Self-Service BI",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Led a citizen-developer business model using RPA and self-service BI, defining pricing strategy and roadmap.
    - Managed business development, pre-sales and sales, identifying new opportunities to expand margin.
    - Established change management structures to drive adoption of new processes and reporting technologies.
  ]
)

#v(gap)

#entry(
  "Investment & Corporate Development — BI & Pricing (Freelancer)",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Designed the data model and visualisation for the Investment department's Business Intelligence efforts across self-storage redevelopment and acquisition projects.
    - Collaborated on a new AI-driven pricing model to commercialise underused assets.
    - Maintained a project dashboard and launched corporate-development initiatives to improve departmental policies.
  ]
)
