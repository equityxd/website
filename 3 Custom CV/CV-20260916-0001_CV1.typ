// CV v1 — tailored to: Business Analyst – Greenfield ERP Project (Brussels, BE | Hybrid | Contract/Freelance | Logistics/Transport)
// Version: truthful, JD-fit rewrite preserving the base CV layout and styling.

#import "@preview/octique:0.1.1": *;

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

  // ── Show rules ──
  // Level 1 (=) : Main section headings
  show heading.where(level: 1): body => [
    #line(length: 100%, stroke: (thickness: 0.5pt))
    #v(gap)
    #text(s-head, weight: "bold", style: "normal")[#body]
    #v(gap-m)
  ]

  // Level 3 (===) : Section headers inside grid columns
  show heading.where(level: 3): body => [
    #text(s, weight: "semibold", style: "normal")[#body]
    #v(gap-m)
    #line(length: 100%, stroke: (thickness: 0.3pt))
    #v(gap-m)
  ]

  // Level 4 (====) : Sub-category headers
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
            ==== Business Analysis
            - Process Mapping
            - AS-IS / TO-BE Assessment
            - Requirements Gathering
            - Fit-Gap Analysis
            - Stakeholder Management

            ==== ERP
            - SAP S/4HANA
            - SAP HANA
          ],
          [
            ==== Business Intelligence
            - MS Power BI
            - QlikSense
            - Cognos
            - Business Objects

            ==== Agile & Delivery
            - Jira
            - Confluence
            - Process Improvement

            ==== Data & Analytics
            - SQL
            - VBA
            - R
            - PowerQuery ETL
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
    )
    ]
    #v(gap)

    // ─── BLOCK 4 : Professional Experience (full width) ───
    #body
  ]
}

// ── Entry content producer (no styling — styling applied at call site) ──
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

  // Each professional experience is kept as one indivisible block (cannot split across pages)
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

  // JD-fit entries get a light grey highlight on the position name so a recruiter's eye
  // lands immediately on the experience that matters for THIS application.
  content
}


// Education uses a dedicated 5-line layout:
//   Org name — rank (#rank) — date | location — degree — field
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
    keywords: "Business Analyst, ERP Transformation, Greenfield ERP, AS-IS Assessment, Process Mapping, Requirements Gathering, Fit-Gap Analysis, Stakeholder Management, ERP Selection, Business Requirements, Data Requirements, Integration Requirements, Future-State Operating Model, SAP S/4HANA, SAP HANA, Power BI, Process Improvement, Change Management",
    quote: "Business Analyst supporting Greenfield ERP transformation programmes from initial business-needs assessment through to ERP selection and implementation. I assess and document AS-IS processes, systems, data and interfaces, identify gaps, inefficiencies and improvement opportunities, and develop business, functional, non-functional, data and integration requirements. I facilitate workshops with business stakeholders and process owners to capture and prioritise requirements, build the ERP requirements catalogue and evaluation criteria, and analyse ERP solutions against business and operational needs to inform selection and the future-state operating model. Across SAP S/4HANA and SAP HANA migration and greenfield programmes across France, Belgium and the Netherlands, I bring calm decision-making under pressure, disciplined stakeholder management and governed, auditable outcomes."
  ),
  position: "Business Analyst – ERP Transformation",

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
    ==== Business Analysis
    - Process Mapping
    - AS-IS / TO-BE Assessment
    - Requirements Gathering
    - Fit-Gap Analysis
    - Stakeholder Management

    ==== ERP
    - SAP S/4HANA
    - SAP HANA

    ==== Business Intelligence
    - MS Power BI
    - QlikSense
    - Cognos
    - Business Objects

    ==== Agile & Delivery
    - Jira
    - Confluence
    - Process Improvement

    ==== Data & Analytics
    - SQL
    - VBA
    - R
    - PowerQuery ETL
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

#v(gap)

#entry(
  "Strategic Business Analyst & Finance Automation Lead (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Acted as the core Business Analyst across the SAP S/4HANA migration, bridging IT architecture and strategic business operations to align technical delivery with business needs.
    - Assessed and documented AS-IS processes, systems, data and interfaces between the middle-office (IVDB) database and SAP S/4HANA, reworking WBS project codes to strengthen portfolio monitoring and reporting.
    - Identified process gaps, inefficiencies and improvement opportunities, replacing an unreliable legacy budget framework with a new from-scratch automated model delivered within a 2-week timeline to keep operations continuous.
    - Automated financial-close ingestion with PowerQuery ETL workflows, processing 1,500+ bookings per close with zero human intervention.
  ],
  important: true
)

#v(gap)

#entry(
  "Senior Operational Excellence & Data Lead (Freelancer)",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Mapped and restructured production workflows post-M&A to eliminate inefficiencies, strengthening operational efficiency and reporting clarity.
    - Assessed AS-IS data structures and managed the SAP HANA migration, restructuring data to ensure system integrity and reliability.
    - Evaluated ERP/BI solutions against business requirements and operational needs, selecting and implementing Qliksense over new data sources to improve insight reliability.
    - Built rebate models across matrix and automated SAP, aligning commercial strategy with business requirements.
  ]
)

#v(gap)

#entry(
  "Cash Flow & Financial Modeling Specialist (Freelancer)",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Defined cash-flow reporting and per-project cash-exposure requirements for project finance.
    - Modelled finance data from SAP and designed Power BI reporting to connect ERP data to actionable business insights.
    - Assessed subsidiary financing needs through credit analysis and impairment testing.
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
    - Defined the investment department's data model and BI visualizations, measuring KPIs to support decision-making.
    - Translated business requirements into a data-driven framework for a new AI-powered pricing model.
  ]
)

#v(gap)

#entry(
  "Freelance CFO / Fundraising Consultant",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Acted as interim CFO and raised €3M in debt/equity funding, coordinating investor and lender requirements.
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
    - Identified process improvement opportunities and built a citizen-developer model combining RPA and self-service BI, defining a pricing strategy and BI/analytics roadmap.
    - Delivered tailored stakeholder reporting to help clients monitor costs and make data-driven decisions.
    - Established change-management structures to enable adoption of new processes and tools.
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
    - Contributed to establishing the future-state operating model (Finance Transformation Operating Model, FTOM), designing client-centric performance-management reporting.
    - Optimized the finance-close process for governance, internal control and data quality.
    - Conducted fit-gap analysis of business requirements versus existing procedures to identify improvement opportunities.
    - Facilitated workshops with business stakeholders and process owners to capture and prioritise requirements against BPM standards.
  ]
)

#v(gap)

#entry(
  "Managing Director & Head of Project Financial Modeling / Cursus Grand Talent",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Directed airport operations across 50+ locations in multiple countries.
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
    - Integrated SAP BPC and Cognos reporting systems and standardized consolidation.
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
