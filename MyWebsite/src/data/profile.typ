// Auto-generated from data/profile.json — do not edit by hand.
// Regenerate with:  python generation/typst_builder.py


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
    keywords: "FP&A, P&L, Financial Modelling, Consolidation, Group Controlling, Cash Flow Management, CAPEX Planning, M&A, Finance Transformation, RPA, Business Intelligence, Change Management, Strategic Planning",
    quote: "15+ years across multi-entity, multi-country organisations (BE, FR, NL). I turn complex finance into clear, growth-driven decisions — from multi-year Medium-Term Plans to M&A due diligence and post-acquisition integration.",
  ),
  position: "Chief Growth & Transformation Officer",

  // ── Education ──
  education: [
    #edu(
      "ESCP Business School",
      "#1 FT 2026",
      2010, 2011,
      "Paris, FR",
      "Specialized Master's degree",
      "Auditing and Consulting"
    )

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

  // ── Languages ──
  languages: [
    #text(s-small, weight: "semibold", style: "normal")[Native:] \
      #text(s-small, weight: "semibold", style: "normal")[French] \
      #text(s-small, weight: "semibold", style: "normal")[Khmer] \
      #text(s-small, weight: "semibold", style: "normal")[Teochew]
    #text(s-small, weight: "semibold", style: "normal")[Proficient:] \
      #text(s-small, weight: "semibold", style: "normal")[English]
    #text(s-small, weight: "semibold", style: "normal")[Basics:] \
      #text(s-small, weight: "semibold", style: "normal")[Dutch (A2)] \
      #text(s-small, weight: "semibold", style: "normal")[Spanish] \
      #text(s-small, weight: "semibold", style: "normal")[Mandarin]
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
      January 2026,
      none,
      "Brussels, BE",
      [
        Led the financial controlling pilot phase for the SAP S/4HANA migration across French subsidiaries, bridging IT architecture and strategic business operations.
        Designed, built and deployed an automated budget-modeling tool from scratch within a 2-week timeline, ensuring operational continuity during a resource gap.
        Streamlined financial closing for commodity trading with PowerQuery ETL workflows, safely ingesting 1,500+ bookings per close with zero human intervention.
        Reconciled financial data between middle-office databases (IVDB) and SAP S/4HANA while restructuring WWS project codes to optimize portfolio monitoring.
      ],
      important: false,
    )

#entry(
      "Senior Operational Excellence & Data Lead",
      "Holcim",
      January 2024,
      December 2025,
      "Nivelles, BE",
      [
        Supported post-M&A integration and group controlling, leveraging data insights to restructure workflows and enhance efficiency.
        Managed SAP HANA migration, restructuring data and ensuring system integrity.
        Developed rebate models (matrix & automated SAP), aligning with commercial strategy.
        Implemented Qliksense with new data for financial reporting and insights.
        Ensured data reliability and liaised with auditors on rebate matters.
      ],
      important: false,
    )

#entry(
      "Cash Flow & Financial Modeling Specialist",
      "Engie Tractebel",
      March 2023,
      December 2023,
      "Brussels, BE",
      [
        Designed cash-flow reporting and cash-exposure modeling per project.
        Assessed financing needs in the local entity, with credit analysis of specific counterparts and impairment testing.
        Developed financial modeling from SAP HANA data and designed Power BI reporting.
      ],
      important: false,
    )

#entry(
      "Investment & Corporate Development Analyst",
      "Shurgard",
      February 2022,
      February 2023,
      "Brussels, BE",
      [
        Analyzed and managed real-estate projects, including construction, redevelopment and acquisition of self-storage businesses.
        Maintained a project dashboard and initiated corporate-development projects to improve department policies.
        Designed the data model and visualization for the Investment department's Business Intelligence efforts.
        Collaborated on a new pricing model using Artificial Intelligence.
      ],
      important: false,
    )

#entry(
      "Freelance CFO / Fundraising Consultant",
      "Magnetrap",
      November 2020,
      January 2022,
      "Mons, BE",
      [
        Acted as interim CFO and led fundraising, organizing €3M in debt/equity fund raises.
        Created cash-flow projections, business plans and long-term financial goals.
        Monitored company performance and implemented corrective actions as needed.
        Prepared operating-results reports and managed financial models for long-term use.
      ],
      important: false,
    )

#entry(
      "Director Business Process Automation",
      "Tobania",
      February 2020,
      October 2020,
      "Brussels, BE",
      [
        Led development and implementation of a citizen-developer business model using RPA and self-service BI, including pricing strategy and roadmap.
        Managed business development including marketing strategy, pre-sales and sales, and identified new opportunities.
        Implemented process optimization, standardization and harmonization to improve efficiency and profitability.
        Provided tailored reports to help customers monitor costs and established change-management structures for adoption.
      ],
      important: false,
    )

#entry(
      "Founder",
      "Soap collect",
      January 2019,
      none,
      "Phnom Penh, KH",
      [
        Established a non-profit providing hygiene products to disadvantaged communities.
        Formed partnerships with luxury hotel chains to source used soap for reconditioning.
      ],
      important: false,
    )

#entry(
      "Performance Management Project Leader",
      "Degroof Petercam",
      January 2018,
      December 2018,
      "Brussels, BE",
      [
        Finance Transformation Operating Model (FTOM).
        Designed and implemented a client-centric performance-management system.
        Optimized the finance-close process for improved governance, internal control and data quality.
        Led projects related to regulatory-reporting sourcing and followed BPM standards.
        Conducted gap analysis of business requirements against existing procedures.
      ],
      important: false,
    )

#entry(
      "Managing Director & Head of Project Financial Modeling",
      "Vinci Airports",
      February 2016,
      December 2017,
      "Brussels, BE & Lisbon, PT",
      [
        Value creation: valuation at 4 times acquisition cost.
        Led deployment of airport operations at 50+ locations in various countries.
        Developed a long-term financial business model including macroeconomic impact, capital expenditures and concession valuation.
        Negotiated extension of the concession contract with Portuguese authorities and implemented a new financial model to improve budgeting and forecasting.
        Managed accounting and financial reporting in accordance with BE-GAAP standards.
      ],
      important: true,
    )

#entry(
      "Reporting Consolidation Manager",
      "Rexel",
      September 2014,
      January 2016,
      "Paris, FR",
      [
        Led the implementation of IFRS financial reporting for Asia-Pacific, Latin America and Canadian subsidiaries.
        Spearheaded the restructuring and integration of SAP BPC and Cognos reporting systems.
        Performed annual budgeting, monthly forecasting and analyses of actual vs. budgeted results.
        Led the strategic-planning process for the organization.
      ],
      important: false,
    )

#entry(
      "Financial Auditor Supervisor",
      "KPMG Audit",
      January 2011,
      August 2014,
      "Paris, FR",
      [
        Conducted audits using various accounting standards, including testing key processes in accordance with SOX requirements.
        Experienced in auditing financial modeling for long-term contracts, especially Public-Private Partnerships (PPP).
        Certified FP7 Grant Agreements for the EU Research program and led audit teams.
        Developed partnerships and identified new markets to support business growth.
        Key clients span Construction (Vinci, Eiffage, Colas), Real estate (Nexity), Water distribution (Veolia), Parcels distribution (Geopost), Security (Brink's) and Healthcare (DomusVie).
      ],
      important: false,
    )

#entry(
      "Deputy CFO Trainee",
      "ICM – Brain & Spine Institute",
      November 2009,
      August 2010,
      "Paris, FR",
      [
        Implemented the budget system and prepared business plans for the scientific teams.
        Established the internal-control system for purchasing and donation processes and managed bank reconciliation.
        Prepared the institutional audit necessary for certification by the Comité de la Charte.
      ],
      important: false,
    )

