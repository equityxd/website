// Icon-based CV using octique contact icons. Layout: standard fonts, section headings,
// standard bullets. Contact uses octique icons (not ATS-label-friendly by design).
// Tailored for: Financial Modelling — Senior FP&A / Group Controller freelance (corporate).

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
        #text(size: 9pt, style: "italic")[
          Rue Montagne de l'Oratoire 28/76\
          B-1000 Brussels\
          #profile.mailto\
          #profile.website\
          #profile.tel
        ]
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
            ==== Planning & Forecasting
            - Medium-Term Plan (Multi-Year Business Planning)
            - P&L Analysis & Forecasting
            ==== Reporting & Consolidation
            - Consolidation & Financial Reporting (IFRS / BE-GAAP)
            - Group Controlling
            ==== Cash & CAPEX
            - Cash Flow Management
            - Working Capital Management
            - CAPEX Planning
            ==== M&A
            - Investor Support & Financial Modelling
            - M&A: Due Diligence & Post-Acquisition Integration
          ],
          [
            #text(s, weight: "bold")[Working Tools]
            ==== Business
            - MS Office (advanced Excel, Power Query)

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
            - VBA
            - SQL
            - R
          ]
        )
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
    ]
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
    keywords: "Multi-Year Business Planning, Medium-Term Plan (MTP 2026–2030), FP&A, Group Controlling, Consolidation (IFRS / BE-GAAP), P&L Analysis, Cash Flow, Working Capital, CAPEX Planning, Movement Schedules, Investor Support, Financial Modelling, M&A, Due Diligence, Post-Acquisition Integration, SAP HANA, SAP BPC, Cognos, Business Object, Hyperion, Power BI, multi-country reporting, English (indispensable), French (desired)",
    quote: "Finance professional with 15+ years across Group Controlling, multi-entity consolidation (IFRS / BE-GAAP), cash-flow and financial modelling, and investor- and bank-facing reporting for multi-country (BE, FR, NL, PT) groups. I can help the CFO and Corporate Controlling build and progressively embed the Medium-Term Plan 2026–2030, and I analyse and challenge regional P&L, bilan, cash-flow, working capital and CAPEX on the fund — turning consolidated data into investor-, bank- and stakeholder-ready analysis."
  ),
  position: "Senior FP&A / Group Controller freelance",

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
    ==== Planning & Forecasting
    - Medium-Term Plan (Multi-Year Business Planning)
    - P&L Analysis & Forecasting
    ==== Reporting & Consolidation
    - Consolidation & Financial Reporting (IFRS / BE-GAAP)
    - Group Controlling
    ==== Cash & CAPEX
    - Cash Flow Management
    - Working Capital Management
    - CAPEX Planning
    ==== M&A
    - Investor Support & Financial Modelling
    - M&A: Due Diligence & Post-Acquisition Integration
    ==== Working Tools
    ==== Business
    - MS Office (advanced Excel, Power Query)

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
    - VBA
    - SQL
    - R
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

#set par(leading: 3pt)

#entry(
  "Strategic Business Analyst & Finance Automation Lead",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Challenged and consolidated financial controlling across French subsidiaries during the SAP S/4HANA migration, preserving the group consolidation pipeline.
    - Reconciled IVDB (middle-office) data against SAP S/4HANA to support balance-sheet movement-schedule analysis, and restructured WBS project codes to strengthen portfolio monitoring.
    - Built a from-scratch automated budget-modelling tool within a 2-week window, ensuring operational continuity during a staffing gap and replacing an unreliable legacy framework.
    - Automated financial closing via PowerQuery ETL workflows, ingesting batches of 1,500+ bookings per close with zero human intervention.
  ],
  important: false
)

#v(0pt)

#entry(
  "Senior Operational Excellence & Data Lead",
  "Holcim",
  "January 2024", "December 2025",
  "Nivelles, BE",
  [
    - Restructured production workflows post-M&A, integrating acquired operations to improve efficiency.
    - Managed the SAP HANA ERP data migration, restructuring data and ensuring system integrity.
    - Built rebate models (matrix & automated SAP) aligned to commercial strategy.
    - Deployed Qlik Sense for financial reporting and new stakeholder insights.
    - Liaised with auditors on rebate matters to guarantee data reliability.
  ],
  important: false
)

#v(0pt)

#entry(
  "Cash Flow & Financial Modeling Specialist",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Designed project-level cash-flow reporting and per-project cash exposure to support financing decisions.
    - Assessed local financing needs and performed counterpart credit analysis and impairment testing.
    - Developed finance data models from SAP HANA and designed Power BI reporting.
    - Underwrote capex and cash-flow assumptions for investor support engagements.
  ],
  important: true
)

#v(0pt)

#entry(
  "Investment & Corporate Development Analyst",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Analysed and managed real estate transactions, including the acquisition of self-storage businesses (restructuring, divestitures).
    - Maintained project dashboards for corporate development and initiated initiatives to improve department policies and procedures.
    - Designed the data model and visualization for the Investment department's Business Intelligence efforts.
    - Collaborated in the development of a new pricing model using Artificial Intelligence.
  ],
  important: true
)

#v(0pt)

#entry(
  "Freelance CFO / Fundraising Consultant",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Acted as interim CFO and led fundraising, structuring €3M in debt/equity fund raises for investor and banking stakeholders.
    - Created cash-flow projections, business plans, and long-term financial goals (business planning / MTP).
    - Monitored company performance and implemented corrective actions to protect profitability.
    - Prepared operating-results reports for investors and maintained financial models for long-term planning.
  ],
  important: true
)

#v(0pt)

#entry(
  "Director Business Process Automation",
  "Tobania",
  "February 2020", "October 2020",
  "Brussels, BE",
  [
    - Led RPA and self-service BI rollout, including pricing strategy and roadmap.
    - Managed business development, marketing and pre-sales, identifying new opportunities.
    - Implemented process optimization, standardization, and harmonization to improve efficiency and profitability.
    - Provided tailored reports to help customers monitor and control costs, and established change-management structures for adoption.
  ],
  important: false
)

#v(0pt)

#entry(
  "Founder",
  "Soap collect",
  "January 2019", "Present",
  "Phnom Penh, KH",
  [
    - Established a non-profit organization focused on providing hygiene products to disadvantaged communities.
    - Formed partnerships with luxury hotel chains to source used soap for reconditioning.
  ],
  important: false
)

#v(0pt)

#entry(
  "Performance Management Project Leader",
  "Degroof Petercam",
  "January 2018", "December 2018",
  "Brussels, BE",
  [
    - Contributed to a Finance Transformation Operating Model (FTOM).
    - Designed and implemented a client-centric performance management system.
    - Optimized the finance close process for improved governance, internal control and data quality.
    - Conducted gap analysis of business requirements versus existing procedures.
  ],
  important: true
)

#v(0pt)

#entry(
  "Managing Director & Head of Project Financial Modeling / Cursus Grand Talent",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Delivered value creation through valuation at 4 times acquisition cost.
    - Led deployment of airport operations across 50+ locations in various countries.
    - Developed the long-term financial business model, analysing macroeconomic impact, capital expenditures and concession valuation.
    - Negotiated extension of the concession contract with Portuguese authorities and implemented new budgeting and forecasting processes.
    - Managed accounting and financial reporting in accordance with BE-GAAP standards.
  ],
  important: true
)

#v(0pt)

#entry(
  "Reporting Consolidation Manager",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Led the implementation of IFRS consolidated reporting for Asia-Pacific, Latin America, and Canadian subsidiaries.
    - Integrated SAP BPC and Cognos reporting systems, strengthening GL/AP consolidated reporting.
    - Ran annual budgeting and monthly forecasting (actual vs. budget).
    - Led the strategic planning process for the organization.
  ],
  important: true
)

#v(0pt)

#entry(
  "Financial Auditor Supervisor",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Audited financial statements under multiple accounting standards (BE-GAAP, IFRS, SOX), strengthening GL and financial-close controls.
    - Audited financial modelling for long-term contracts, particularly in the context of Public-Private Partnerships (PPP).
    - Certified FP7 Grant Agreements for the EU Research program; led audit teams and supervised financial auditors.
  ],
  important: true
)

#v(0pt)

#entry(
  "Deputy CFO Trainee",
  "ICM - Brain & Spine Institute", 
  "November 2009", "August 2010",
  "Paris, FR",
  [
    - Implemented the budget system and prepared business plans for the scientific teams.
    - Established the internal control system for purchasing and donation processes and managed bank reconciliation.
    - Prepared the institutional audit necessary for the certification by the "Comité de la Charte".
  ],
  important: true
)
#v(gap)
