// CV v1 — tailored to: Lead BI & Analytics Consultant (European Non-Profit)
// Version 2 headline: "Data & Analytics Transformation Consultant"

["@preview/octique:0.1.1": *];

// ── Type scale (4 steps) ──
#let s        = 10pt   // body base: company names, job titles, column headings, bullets, contact, footer
#let s-name   = 18pt   // name (title, largest)
#let s-head   = 12pt   // position/subtitle + main section headings (h1)
#let s-small  = 9pt    // secondary: dates, subheadings, inline contact lines
#let s-xsmall = 6.5pt    // tighter: date headers

// ── Rhythm ──
#let leading     = s * 1.2
#let gap         = 4pt   // between major blocks and between entries
#let gap-m       = 2pt   // heading underline padding
#let gutter      = 16pt // grid gutters
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

  // Font is embedded in the PDF, so ATS parsers read the text correctly.
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
        #octique-inline("location", width: 0.6em) #text(s-small)[Rue Montagne de l'Oratoire 28/76]
        #v(gap)
        #h(0.7em) #text(s-small)[B-1000 Brussels]
        #v(gap)
        #octique-inline("mail", width: 0.6em) #text(s-small)[#profile.mailto]
        #v(gap)
        #octique-inline("globe", width: 0.6em) #text(s-small)[#profile.website]
        #v(gap)
        #octique-inline("device-mobile", width: 0.6em) #text(s-small)[#profile.tel]
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
            ==== Data Engineering
            - SAP HANA / S/4HANA data migration
            - ETL / ingestion pipelines (PowerQuery)
            - Dimensional / relational modelling

            ==== BI / Reporting
            - MS Power BI
            - QlikSense
            - Cognos
            - Business Objects

            ==== Analytics
            - SQL, VBA, R
            - AI / ML-powered modelling
            - Data quality assurance

            ==== Delivery / ERP
            - SAP BPC
            - UIPath / PowerAutomate
            - Data transformation (AS-IS → TO-BE)
          ],
          [
            ==== Agile / Governance
            - Jira
            - Confluence
            - Change management
            - Roadmap planning

            ==== Business
            - KPIs & metrics definition
            - Business definitions & taxonomies
            - Multi-domain stakeholder reporting
          ]
        ]
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
    ]
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
    keywords: "Data Engineering, Data Transformation, Analytics, Data Warehouse, Dimensional Modelling, ETL, BI Reporting, ERP Systems, SAP HANA, SAP S/4HANA, Roadmap, Change Management, Stakeholders, Leadership, Operations, Performance Improvement",
    quote: "Data & analytics transformation specialist with a proven record of turning fragmented legacy data into governed, decision-ready reporting. I have repeatedly led data transformation and analytics programme work — including SAP S/4HANA and SAP HANA data migrations, ETL ingestion pipelines and Power BI / QlikSense rollouts — while keeping data quality high and auditors happy. I operate comfortably from conceptual design through physical engineering to business adoption. What sets me apart is perspective: I've owned both the transformation and the executive mandate, so I keep technical delivery aligned to business outcomes."
  ),
  position: "Data & Analytics Transformation Consultant",

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
    ==== Data Engineering
    - SAP HANA / S/4HANA data migration
    - ETL / ingestion pipelines (PowerQuery)
    - Dimensional / relational modelling

    ==== BI / Reporting
    - MS Power BI
    - QlikSense
    - Cognos
    - Business Objects

    ==== Analytics
    - SQL, VBA, R
    - AI / ML-powered modelling
    - Data quality assurance

    ==== Delivery / ERP
    - SAP BPC
    - UIPath / PowerAutomate
    - Data transformation (AS-IS → TO-BE)

    ==== Agile / Governance
    - Jira
    - Confluence
    - Change management
    - Roadmap planning

    ==== Business
    - KPIs & metrics definition
    - Business definitions & taxonomies
    - Multi-domain stakeholder reporting
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
  "Strategic Business Analyst & Finance Automation Lead (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Engineered the SAP S/4HANA data migration across French subsidiaries as the core Business Analyst linking data engineering and business operations.
    - Built, from scratch within a 2-week timeline, an automated budget-modelling pipeline, replacing an unreliable legacy framework to ensure operational continuity.
    - Automated financial-close ingestion with PowerQuery ETL workflows, safely processing 1,500+ bookings per close with zero human intervention.
    - Mapped and reconciled middle-office (IVDB) data with SAP S/4HANA, restructuring and simplifying WBS project codes to strengthen data quality for portfolio monitoring.
  ]
)

#v(gap)

#entry(
  "Senior Operational Excellence & Data Lead (Freelancer)",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Migrated and restructured production data post-M&A, enabling efficiency gains captured in new reporting.
    - Managed the SAP HANA migration, restructuring data and ensuring system integrity across the consolidated environment.
    - Built rebate-data models (matrix & automated SAP) aligned to commercial strategy and defined measurable definitions.
    - Implemented Qliksense financial reporting over new data and assured data reliability while liaising with auditors.
  ]
)

#v(gap)

#entry(
  "Cash Flow & Financial Modeling Specialist (Freelancer)",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Built financial data pipelines from SAP for HANA and designed the downstream Power BI reporting layer.
    - Modelled per-project cash exposure, financing needs, credit analysis and impairment testing.
    - Designed Power BI reporting to convert raw operational data into decision-ready business insights.
  ]
)

#v(gap)

#entry(
  "Investment & Corporate Development Analyst (Freelancer)",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Built and maintained project dashboards for a portfolio of self-storage real-estate projects.
    - Engineered the investment department's data model and BI visualizations, defining measurable KPIs.
    - Contributed to an AI-powered pricing model, translating business requirements into an analytical framework.
  ]
)

#v(gap)

#entry(
  "Freelance CFO / Fundraising Consultant",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Acted as interim CFO and led fundraising, organizing €3M in debt/equity fund raises.
    - Built cash-flow projections, business plans and long-term financial models, tracking KPIs with corrective actions.
    - Produced operating-results reporting to support board and investor decision-making.
  ]
)

#v(gap)

#entry(
  "Director Business Process Automation",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Delivered a citizen-developer model combining RPA and self-service BI, with a defined pricing and analytics roadmap.
    - Built tailored stakeholder reporting to help clients monitor costs and make data-driven decisions.
    - Established change-management structures to enable adoption of new BI and automation processes.
  ]
)

#v(gap)

#entry(
  "Founder",
  "Soap collect",
  "January 2019", "Present",
  "Phnom Penh, KH",
  [
    - Founded a non-profit organisation providing hygiene products to disadvantaged communities.
    - Partnered with luxury hotel chains to source used soap for reconditioning.
  ]
)

#v(gap)

#entry(
  "Performance Management Project Leader",
  "Degroof Petercam",
  "January 2018", "December 2018",
  "Brussels, BE",
  [
    - Drove the Finance Transformation Operating Model (FTOM) reporting data design.
    - Optimized the finance-close process to improve governance, internal control and data quality.
    - Led regulatory-reporting sourcing against BPM standards and ran gap analysis of business versus existing procedures.
  ]
)

#v(gap)

#entry(
  "Managing Director & Head of Project Financial Modeling / Cursus Grand Talent",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Directed data and operations across airport sites in 50+ locations across multiple countries.
    - Built concession-valuation financial models analysing macroeconomic impact, capex and forecasting.
    - Negotiated concession extensions and improved budgeting/forecasting processes; managed BE-GAAP accounting and reporting.
  ]
)

#v(gap)

#entry(
  "Reporting Consolidation Manager",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Led IFRS cross-subsidiary reporting across Asia-Pacific, Latin America and Canada.
    - Integrated SAP BPC and Cognos reporting systems and standardized consolidation data.
    - Drove annual budgeting, monthly forecasting and strategic planning reporting.
  ]
)

#v(gap)

#entry(
  "Financial Auditor Supervisor",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Performed statement audits and key-process testing against SOX requirements.
    - Certified FP7 Grant Agreements for the EU Research program, applying auditable data standards.
    - Led and supervised financial-audit teams while managing multiple stakeholder requirements.
  ]
)

#v(gap)

#entry(
  "Deputy CFO Trainee",
  "ICM - Brain & Spine Institute", 
  "November 2009", "August 2010",
  "Paris, FR",
  [
    - Implemented the budget system and prepared business plans for scientific teams.
    - Established internal-control systems for purchasing and donation processes and managed bank reconciliation.
    - Prepared the institutional audit necessary for certification by the "Comité de la Charte".
  ]
)
