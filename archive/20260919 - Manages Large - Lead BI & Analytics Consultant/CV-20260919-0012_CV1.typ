// Icon-based CV using octique contact icons. Layout: standard fonts, section headings,
// standard bullets. Contact uses octique icons (not ATS-label-friendly by design).

#import "@preview/octique:0.1.1": *;

// ── Type scale (4 steps) ──
#let s        = 10pt   // body base: company names, job titles, column headings, bullets, contact, footer
#let s-name   = 18pt   // name (title, largest)
#let s-head   = 12pt   // position/subtitle + main section headings (h1)
#let s-small  = 9pt    // secondary: dates, subheadings, inline contact lines
#let s-xsmall = 6.5pt    // tighter: date headers

// ── Rhythm ──
#let s   = 10pt
#let leading = s * 1.2
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
  set par(leading: s * 0.55)
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
        #text(s, weight: "bold", style: "normal")[Education]
        #v(gap-m)
        #set text(size: 9pt)
        #education
      ],
      [
        // ── Column 2 : Core competencies (col 1) + Working Tools (col 2) ──
        #set text(size: 9pt)
        #grid(
          columns: (1.5fr, 1.5fr),
          gutter: 8pt,
          [
            #text(s, weight: "bold")[Core competencies]
            ==== BI & Analytics Strategy
            - BI & Analytics Strategy & Roadmap
            - Business Process Translation
            - KPIs, Metrics & Business Definitions
            ==== Data Modelling & Data Architecture
            - Conceptual / Logical / Physical Data Modelling
            - Common Data Model across programmes
            ==== Data Governance & Reporting
            - Data Governance & Data Quality Frameworks
            - Enterprise Reporting & Auditable Analytics
            ==== Programme / Funding Reporting
            - Multi-domain, multi-stakeholder Reporting
            - EU / International Funding Programme Reporting
          ],
          [
            #text(s, weight: "bold")[Working Tools]
            ==== Business
            - MS Office (advanced Excel, Power Query ETL)

            ==== ERP
            - SAP HANA

            ==== Business Intelligence
            - MS Power BI
            - QlikSense
            - Business Object
            - Cognos
            - Hyperion

            ==== RPA
            - UIpath
            - MS PowerAutomate

            ==== Agile
            - Jira
            - Confluence

            ==== Data & Analytics
            - SQL
            - R
            - VBA
          ]
        ]
      ],
      [
        // ── Column 3 : Languages, Interests, Interpersonal ──
        #text(s, weight: "bold", style: "normal")[Languages]
        #v(1pt)
        #set text(size: 9pt)
        #languages

        #v(1pt)
        #text(s, weight: "bold", style: "normal")[Interests]
        #v(1pt)
        #set text(size: 9pt)
        #interests

        #v(1pt)
        #text(s, weight: "bold", style: "normal")[Interpersonal]
        #v(1pt)
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
    keywords: "BI & Analytics Strategy, Data Architecture, Data Governance, Data Modelling (Conceptual/Logical/Physical), Business Process Translation, Enterprise Reporting, KPIs & Metrics, Data Quality, Common Data Model, Stakeholder Reporting, Power BI, SAP HANA, ETL, Programme/Funding Reporting",
    quote: "BI & Analytics leader with 15+ years translating complex business processes into reliable, scalable reporting and data foundations across multi-entity, multi-country organisations (BE, FR, NL). Experienced defining KPIs, metrics and business definitions, establishing common data models and enterprise reporting environments, and bridging business stakeholders with data governance, architecture and delivery teams. Holds direct European Commission / EU-funded (FP7) grant certification and non-profit operating experience, bringing a rare programme-and-funding lens to BI strategy, data governance and analytics transformation — operating comfortably at both strategic and hands-on levels.\n  ),
  position: "Lead BI & Analytics Consultant",

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

#v(2pt)

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
    Core competencies
    ==== BI & Analytics Strategy
    - BI & Analytics Strategy & Roadmap
    - Business Process Translation
    - KPIs, Metrics & Business Definitions
    ==== Data Modelling & Data Architecture
    - Conceptual / Logical / Physical Data Modelling
    - Common Data Model across programmes
    ==== Data Governance & Reporting
    - Data Governance & Data Quality Frameworks
    - Enterprise Reporting & Auditable Analytics
    ==== Programme / Funding Reporting
    - Multi-domain, multi-stakeholder Reporting
    - EU / International Funding Programme Reporting
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
  "Strategic Business Analyst & Finance Automation Lead",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Lead BI & Analytics consultant bridging data architecture and business operations during the SAP S/4HANA migration, establishing the data foundation for French subsidiaries.
    - Defined and documented KPIs, metrics and business definitions for budgeting, translating complex financial requirements into a scalable automated reporting solution built from scratch.
    - Deployed PowerQuery ETL workflows to ingest batches of 1,500+ bookings per close, establishing pipeline standards that ensure consistent, reliable, auditable reporting.
    - Reconciled data relationships between middle-office databases (IVDB) and SAP S/4HANA, restructuring project codes to strengthen portfolio monitoring and reporting accuracy.
  ]
)

#v(gap)

#entry(
  "Senior Operational Excellence & Data Lead",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Established common data models and enterprise reporting standards to support post-M&A integration and group controlling across the consolidated group.
    - Led SAP HANA migration ensuring data integrity, contributing to the transition of logical data models into physical structures supporting analytics.
    - Defined rebate models and implemented QlikSense financial reporting, aligning metrics and business definitions with commercial strategy.
    - Resolved data quality and governance issues, liaising with auditors to ensure reporting is consistent, reliable and auditable.
  ]
)

#v(gap)

#entry(
  "Cash Flow & Financial Modeling Specialist",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Defined cash-flow reporting requirements and designed Power BI reporting, translating business processes into scalable analytics solutions.
    - Built cash-exposure and financing-needed models from SAP HANA data, documenting metrics and data relationships for stakeholder decisions.
  ]
)

#v(gap)

#entry(
  "Investment & Corporate Development Analyst",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Designed the data model and visualization for the Investment department's Business Intelligence efforts, transitioning conceptual/logical models into physical reporting structures.
    - Maintained stakeholder dashboards and drove corporate development initiatives to improve department policies and reporting consistency.
    - Contributed to an AI-based pricing model, collaborating across business and technical teams.
  ]
)

#v(gap)

#entry(
  "Freelace CFO / Fundraising Consultant",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Acted as interim CFO and led fundraising, organizing €3M in debt/equity fund raises.
    - Established cash-flow projections, business plans and long-term financial goals, defining KPIs and business definitions for performance monitoring.
    - Prepared operating results reports and maintained financial models for long-term stakeholder reporting.
  ]
)

#v(gap)

#entry(
  "Director Business Process Automation",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Established self-service BI and RPA business model with pricing strategy and roadmap, guiding BI and analytics delivery teams.
    - Delivered regular, tailored reports enabling data-driven business decisions, presenting analytical concepts to technical and non-technical audiences.
    - Established standards for process optimization, standardization and reporting consistency, and created change management structures for adoption.
  ]
)

#v(gap)

#entry(
  "Founder",
  "Soap collect",
  "January 2019", "Present",
  "Phnom Penh, KH",
  [
    - Established a non-profit organization focused on providing hygiene products to disadvantaged communities.
    - Formed partnerships with luxury hotel chains to source used soap for reconditioning.
  ]
)

#v(gap)

#entry(
  "Performance Management Project Leader",
  "Degroof Petercam",
  "January 2018", "December 2018",
  "Brussels, BE",
  [
    - Finance Transformation Operating Model (FTOM).
    - Established data governance and data quality standards optimizing the finance close process for auditable reporting.
    - Led regulatory-reporting sourcing projects following BPM standards.
    - Conducted gap analysis of business requirements against existing procedures to improve reporting and data consistency.
  ]
)

#v(gap)

#entry(
  "Managing Director & Head of Project Financial Modeling / Cursus Grand Talent",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Value creation: valuation at 4 times of acquisition cost.
    - Led deployment of airport operations across 50+ locations in various countries, managing multi-domain stakeholder reporting.
    - Developed long-term financial business models analyzing macroeconomic impact, capital expenditures and concession valuation.
    - Managed accounting and financial reporting in accordance with BE-GAAP standards.
  ]
)

#v(gap)

#entry(
  "Reporting Consolidation Manager",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Led implementation of IFRS financial reporting across Asia-Pacific, Latin America and Canadian subsidiaries.
    - Integrated enterprise reporting environments (SAP BPC and Cognos), standardizing reporting across multiple domains.
    - Drove budgeting, forecasting and actual-vs-budget analysis with consistent, reliable reporting.
  ]
)

#v(gap)

#entry(
  "Financial Auditor Supervisor",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Certified FP7 Grant Agreements for the EU Research program — direct European Commission / EU-funded programme exposure.
    - Ensured auditable financial reporting under SOX requirements for long-term contracts (Public-Private Partnerships).
    - Led audit teams and supervised financial auditors across multiple business domains.
    Main sector: Construction (Vinci, Eiffage, Colas), Real estate (Nexity), Water distribution (Veolia), International parcels distribution (Geopost from La Poste group), Security (Brink's), Healthcare (DomusVie).
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
    - Established the internal control system for purchasing and donation processes and managed bank reconciliation.
    - #set smartquote(enabled: false)
      Prepared the institutional audit necessary for the certification by the "Comité de la Charte".
  ]
)
