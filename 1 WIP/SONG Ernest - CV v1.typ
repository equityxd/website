#import "@preview/octique:0.1.1": *

// ── Type scale (4 steps, no half-points) ──
#let s        = 10pt   // body base: company names, job titles, column headings
#let s-name   = 20pt   // name only
#let s-head   = 12pt   // position + main section headings (h1)
#let s-small  = 9pt    // secondary: dates, subheadings, contact lines, bullets, footer

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

  set text(s, font: "Source Sans 3", lang: "en")
  set par(leading: s * 0.7)
  set align(left)
  set list(body-indent: indent)

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
    #v(gap-m)
    #line(length: 100%, stroke: (thickness: 0.2pt))
    #v(gap-m)
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

    // ─── BLOCK 1 : Centered Title ───
    #align(center)[
      #text(s-name, weight: "bold")[#profile.name • ]
      #text(s-head, weight: "semibold", style: "normal")[#position]
      #v(gap-m)
      #line(length: 3.5cm, stroke: (thickness: 1pt))
    ]
    #v(gap)

    // ─── BLOCK 2 : Contact (left) + Quote (right) ───
    #grid(
      columns: (1.8fr, 2.2fr),
      gutter: gutter,
      [
        #set par(leading: 12pt)
        #octique-inline("location", width: 0.6em) #text(s-small)[#profile.address]

        #octique-inline("mail", width: 0.6em) #text(s-small)[#profile.mailto]

        #octique-inline("globe", width: 0.6em) #text(s-small)[#profile.website]

        #octique-inline("device-mobile", width: 0.6em) #text(s-small)[#profile.tel]
      ],
      block(
        width: 100%,
      )[
        #set par(justify: true)
        #text(s-small, style: "italic")[#profile.quote]
      ]
    )
    #v(gap)

    // ─── BLOCK 3 : Three columns ───
    #grid(
      columns: (2fr, 2.3fr, 2.7fr),
      gutter: gutter,
      [
        // ── Column 1 : Education ──
        === Education
        #education
      ],
      [
        // ── Column 2 : Competencies ──
        === Competencies
        #competencies
      ],
      [
        // ── Column 3 : Languages, Interests, Interpersonal ──
        === Languages
        #languages

        #v(gap)
        === Interests
        #interests

        #v(gap)
        === Interpersonal
        #interpersonal
      ]
    )
    #v(gap)

    // ─── BLOCK 4 : Professional Experience (full width) ───
    #body
  ]
}

// ── Entry content producer (no styling — styling applied at call site) ──
#let entry(title, name, date_start, date_end, location, details) = {
  let date_str = if date_start == none and date_end != none {
    str(date_end)
  } else if date_start != none and date_end == none {
    str(date_start) + " – Present"
  } else if date_start != none and date_end != none {
    str(date_start) + " – " + str(date_end)
  } else {
    ""
  }

  [
    #text(s, weight: "bold")[#name]
    #h(1fr)
    #text(s-small, style: "italic")[#date_str  •  #location]

    #text(s, weight: "semibold", style: "normal")[#title]

    [#set par(leading: 10pt)
      #text(s-small)[#details]
    ]
  ]
}

#show: body => resume(
  profile: (
    name: "Ernest SONG",
    address: "Rue Montagne de l'Oratoire 28/76, B-1000 Brussels",
    mailto: "contact@ernestsong.com",
    website: "ernestsong.com",
    tel: "+32 476 60 05 90",
    keywords: "Entrepreneurship, Strategic, P&L, Profit & Loss Responsibility, Growth, Revenue, Profit, ROI, Metrics, Change Management, Change Transition, Leadership, Operations, Performance Improvement, Stakeholders, Budget & Finance",
    quote: "Managing Director and ESCP graduate with a proven track record of driving exponential value, including a 4x acquisition cost valuation at Vinci Airports across 50+ global locations. Expert in business development and digital transformation, I designed and scaled new RPA/BI business models at Tobania and restructured enterprise workflows post-M&A at Holcim via SAP HANA migrations. Melding financial strategy with data analytics (Power BI), I turn complex global operations into high-growth business engines."
  ),
  position: "Chief Growth & Transformation Officer",

  // ── Education ──
  education: [
    #entry(
      "Specialized Master, Auditing and Consulting",
      "ESCP Business School (Top #1 in Europe @ FT 2026)",
      2010, 2011,
      "Paris, FR",
      none
    )

    #entry(
      "Master's degree, Management Science and Financial Control",
      "Université Paris Nanterre",
      2005, 2010,
      "Paris, FR",
      none
    )
  ],

  // ── Competencies ──
  competencies: [
    ==== Business
    - MS Office (advanced Excel)

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

    ==== Audit
    - IDEA CAATs

    ==== Planning
    - Visual Planning

    ==== Data & Analytics
    - VBA
    - SQL
    - R
  ],

  // ── Languages ──
  languages: [
    ==== Native
    - French
    - Khmer
    - Teochew

    ==== Proficient
    - English

    ==== Basics
    - Dutch (A2)
    - Spanish
    - Mandarin
  ],

  // ── Interests ──
  interests: [
    - Sustainable development
    - Powerlifting
    - Mountain biking
    - Tennis
  ],

  // ── Interpersonal ──
  interpersonal: [
    - Fast-learner
    - Problem solver
    - Diplomacy
    - Driven
    - Autonomous
    - Teamplayer
  ],

  body
)

// ── Professional Experience ──
= Professional Experience

#entry(
  "Strategic Business Analyst & Finance Automation Lead (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Led the financial controlling pilot phase for the SAP S/4HANA migration across French subsidiaries, successfully acting as the core Business Analyst bridging IT architecture and strategic business operations.
    - Designed, built, and deployed a robust, automated budget modeling tool from scratch within a critical 2-week timeline, ensuring operational continuity during a resource gap and replacing an unreliable legacy framework.
    - Streamlined and automated financial closing processes for commodity trading activities, deploying advanced PowerQuery ETL workflows to safely ingest batches of 1,500+ bookings per close with zero human intervention.
    - Reconciled complex financial data structures between middle-office databases (IVDB) and SAP S/4HANA while restructuring and simplifying the Work Breakdown Structure (WBS) project codes to optimize portfolio monitoring.
  ]
)

#entry(
  "Senior Operational Excellence & Data Lead (Freelancer)",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Leveraged data insights derived from market analysis to restructure production workflows post-M&A, significantly enhancing efficiency.
    - Managed SAP HANA migration, restructuring data and ensuring system integrity.
    - Developed rebate models (matrix & automated SAP), aligning with commercial strategy.
    - Implemented Qliksense with new data for financial reporting and insights.
    - Ensured data reliability and liaised with auditors on rebate matters.
  ]
)

#entry(
  "Cash Flow & Financial Modeling Specialist (Freelancer)",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Design cashflow reporting and cash exposure per project.
    - Assessment of financing needs in local entity, credit analysis of specific counterpart and impairment testing.
    - Develop Finance data modelling from SAP for HANA and design Power BI reporting.
  ]
)

#entry(
  "Investment & Corporate Development Analyst (Freelancer)",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Analyzed and managed real estate projects, including construction, redevelopment, and acquisition of self-storage businesses.
    - Maintained project dashboard and initiated corporate development projects to improve department policies and procedures.
    - Designed the data model and visualization for the Investment department's Business Intelligence efforts.
    - Collaborated in the development of a new pricing model using Artificial Intelligence.
  ]
)

#entry(
  "Head of Controlling",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Implemented budgeting, forecasting, and financial control systems.
    - Created cash flow projections, business plans, and long-term financial goals.
    - Monitored company performance and implemented corrective actions as needed.
    - Prepared operating results reports and managed financial models for long-term use.
  ]
)

#entry(
  "Director Business Process Automation",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Led development and implementation of citizen developer business model using RPA and self-service BI, including pricing strategy and roadmap.
    - Managed business development, including marketing strategy, pre-sales, and sales, and identified new business opportunities.
    - Implemented process optimization, standardization, and harmonization to improve efficiency and profitability for customers.
    - Provided regular, tailored reports to help customers monitor and control costs and make data-driven business decisions, and established change management structures and strategies to facilitate successful adoption of new processes and technologies.
  ]
)

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

#entry(
  "Performance Management Project Leader",
  "Degroof Petercam",
  "January 2018", "December 2018",
  "Brussels, BE",
  [
    - Finance Transformation Operating Model (FTOM)
    - Designed and implemented a client-centric performance management system.
    - Optimized finance close process for improved governance, internal control, and data quality.
    - Led projects related to regulatory reporting sourcing and followed BPM standards.
    - Conducted gap analysis of business requirements and existing procedures to identify areas for improvement.
  ]
)

#entry(
  "Managing Director & Head of Project Financial Modeling • Cursus Grand Talent",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Value creation: valuation at 4 times of acquisition cost.
    - Led deployment of airport operations at 50+ locations in various countries.
    - Developed long-term financial business model including analysis of macroeconomic impact, capital expenditures, and concession valuation.
    - Negotiated extension of concession contract with Portuguese authorities and implemented new financial business model to improve budgeting and forecasting processes.
    - Managed accounting and financial reporting in accordance with BE-GAAP standards.
  ]
)

#entry(
  "Reporting Consolidation Manager",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Led the implementation of IFRS financial reporting for Asia-Pacific, Latin America, and Canadian subsidiaries.
    - Spearheaded the restructuring process and integration of SAP BPC and Cognos reporting systems.
    - Performed annual budgeting, monthly forecasting, and analyses of actual vs. budgeted/estimated results.
    - Led the strategic planning process for the organization.
  ]
)

#entry(
  "Financial Auditor Supervisor",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Conducted audits of financial statements using various accounting standards, including testing of key processes in accordance with SOX requirements.
    - Experienced in auditing financial modeling for long-term contracts, particularly in the context of Public-Private Partnerships (PPP).
    - Certified FP7 Grant Agreements for the EU Research program and led audit teams and supervised financial auditors.
    - Developed partnerships and identified new markets to support business growth.
    Main sector: Construction (Vinci, Eiffage, Colas), Real estate (Nexity), Water distribution (Veolia), International parcels distribution (Geopost from La Poste group), Security (Brink's), Healthcare (DomusVie).
  ]
)

#entry(
  "Deputy CFO Trainee",
  "ICM - Brain & Spine Institute", 
  "November 2009", "August 2010",
  "Paris, FR",
  [
    - Implemented the budget system and prepared business plans for the scientific teams.
    - Established the internal control system for purchasing and donation processes and managed bank reconciliation.
    - Prepared the institutional audit necessary for the certification by the "Comité de la Charte".
  ]
)
