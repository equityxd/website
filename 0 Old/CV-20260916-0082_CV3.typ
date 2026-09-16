// Icon-based CV using octique contact icons (ATS-label-friendly labels retained).
// CUSTOM CV — CV-20260916-0082_CV3.typ — "Director of Finance" (operations / ERP transformation)

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
              ==== ERP & Transformation
              - SAP S/4HANA migration
              - SAP HANA consolidation
              - Process optimization

              ==== Operations Finance
              - Cross-functional partnering
              - Multi-entity GL / AP / AR
              - Performance improvement

              ==== Change Management
              - Change transition
              - Business adoption
              - Stakeholder management

              ==== Business Intelligence
              - MS Power BI
              - Cognos
              - QlikSense

              ==== ERP Reporting Tools
              - Business Objects
              - BI dashboards
              - Process standardization

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
    keywords: "Director of Finance, SAP S/4HANA Migration, ERP Transformation, Process Optimization, Cross-functional Partnering, Multi-entity GL/AP/AR, Change Management, Business Intelligence, Power BI, Cognos, Performance Improvement, Stakeholder Management",
    quote: "Director of Finance who bridges IT architecture and business operations. I have guided ERP replacements from AS-IS diagnosis to SAP S/4HANA go-live, automated month-end closes with PowerQuery ETL, and deployed self-service BI so leaders make data-driven decisions. I pair a controller's discipline with a change manager's instinct — aligning process optimization, multi-entity GL / AP / AR, and performance improvement with stakeholder adoption."
  ),
  position: "Director of Finance",

  education: [
    #edu(
      "ESCP Business School",
      "(#1 FT 2026)",
      2010, 2011,
      "Paris, FR",
      "Specialized Master's degree",
      "Auditing and Consulting (ERP change & transition)"
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
    ==== ERP & Transformation
    - SAP S/4HANA migration
    - SAP HANA consolidation
    - Process optimization

    ==== Operations Finance
    - Cross-functional partnering
    - Multi-entity GL / AP / AR
    - Performance improvement

    ==== Change Management
    - Change transition
    - Business adoption
    - Stakeholder management

    ==== Business Intelligence
    - MS Power BI
    - Cognos
    - QlikSense

    ==== ERP Reporting Tools
    - Business Objects
    - BI dashboards
    - Process standardization

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
  "Director of Finance — SAP S/4HANA Migration & Change Transition (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Drove the financial controlling pivot during the SAP S/4HANA migration, bridging IT architecture and strategic business operations as the core Business Analyst.
    - Restructured and simplified WDS project codes to re-serve portfolio monitoring through the consolidated ERP platform.
    - Reconciled middle-office (IVDB) data with SAP S/4HANA to protect data integrity during the transition.
    - Automated the commodity-trading close with PowerQuery ETL workflows, ingesting 1,500+ bookings per close with zero manual intervention.
  ],
  important: true
)

#v(gap)

#entry(
  "Director of Finance — ERP Process Automation & Optimization (Freelancer)",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Led a citizen-developer business model using RPA and self-service BI, defining pricing strategy and roadmap.
    - Implemented process optimization, standardization and harmonization to improve efficiency and profitability for customers.
    - Established change management structures and strategies to facilitate adoption of new processes and technologies.
  ]
)

#v(gap)

#entry(
  "Director of Finance — Operational & Data Excellence (Freelancer)",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Leveraged market-analysis data insights to restructure production workflows post-M&A, enhancing efficiency.
    - Managed the SAP HANA migration, restructuring data and ensuring system integrity.
    - Implemented QlikSense with new data for financial reporting and decision-support insights.
  ]
)

#v(gap)

#entry(
  "Director of Finance — Finance Transformation Operating Model (Freelancer)",
  "Degroof Petercam",
  "January 2018", "December 2018",
  "Brussels, BE",
  [
    - Delivered a Finance Transformation Operating Model (FTOM) and a client-centric performance management system.
    - Optimized the finance close process for improved governance, internal control and data quality.
    - Conducted gap analysis of business requirements versus existing procedures to drive continuous improvement.
  ]
)

#v(gap)

#entry(
  "Director of Finance — IFRS Reporting & Consolidation (Freelancer)",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Delivered IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries on a board-ready monthly/quarterly cadence.
    - Integrated SAP BPC and Cognos reporting to consolidate multi-entity results and drive the budgeting, forecasting and variance cycle.
    - Led the strategic planning process for the organization.
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
