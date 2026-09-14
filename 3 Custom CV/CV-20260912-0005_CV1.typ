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
        #text(size: 9pt, style: "italic")[
          ◆ Rue Montagne de l'Oratoire 28/76
          ◆ B-1000 Brussels
          ◆ mail #profile.mailto
          ◆ #profile.website
          ◆ #profile.tel
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
          ],
          [
            ==== Agile
            - Jira
            - Confluence

            ==== Data & Analytics
            - VBA
            - SQL
            - R

            ==== Data & Analytics
            - VBA
            - SQL
            - R
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
    #v(6pt)
    #text(s, weight: "bold")[#name] #h(1fr) #text(s, style: "italic")[#date_str  |  #location]
    #v(-5pt)

    #if important {
      highlight(fill: rgb(224, 224, 224))[#text(s, weight: "semibold", style: "normal")[#title]]
    } else {
      text(s, weight: "semibold", style: "normal")[#title]
    }
    #v(-5pt)

    #if details != none {
      text(s-small, style: "italic")[#details]
    }
    #v(6pt)
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
    keywords: "Finance Domain Leader, ERP Implementation, ERP Replacement, General Accounting (GL, AP, AR), Financial Close, IFRS, BE-GAAP, Business Blueprint, AS-IS TO-BE Process Design, Workshops, Financial Reporting, Power BI, Cognos, Business Object, Multi-entity, Multi-country, Project Management, Change Management, Stakeholder Management, User Training, French, Dutch",
    quote: "Finance leader with 15+ years leading accounting and transformation mandates for multi-entity, multi-country organisations across BE, FR and NL. I specialise in General Accounting (GL, AP, AR) and financial-close leadership, and in guiding ERP replacements from AS-IS diagnosis to SAP S/4HANA go-live. What sets me apart is perspective: I've sat on both the operator's and the executive-recruiter's side of the table, so I read the numbers and the organisation behind them. I bring calm under pressure, rigorous Power BI / Cognos reporting, and a genuine commitment to turning finance into a lever for growth."
  ),
  position: "Finance Domain Leader",

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

#entry(
  "Strategic Business Analyst & Finance Automation Lead (Freelancer)",
  "Engie SEM",
  "January 2026", "Present",
  "Brussels, BE",
  [
    - Led month-end/year-end GL close for up to 6 BE/FR/NL entities (ERP replacing legacy AS/400), strengthening financial-close control across the multi-entity group.
    - Drove AS-IS to TO-BE process design for finance sub-processes, coordinating cross-functional workshops and stakeholder sign-off.
    - Automated the financial close with PowerQuery ETL, ingesting 1,500+ bookings per close with zero manual intervention.
    - Trained end-users on Infor M3 and validated UAT for finance sub-processes before go-live, documenting steering-committee sign-off.
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
    - Managed the SAP HANA ERP data migration, restructuring data and preserving system integrity.
    - Rolled out Qlik Sense finance reporting, building 8 executive dashboards that shortened reporting cycles by 50% and enabled faster, evidence-based managerial decisions.
    - Built rebate models (matrix & automated SAP) aligned to commercial strategy, driving €150M annual rebate volume with 99.8% accuracy and resolving commercial disputes ~30% faster.
    - Guaranteed data reliability and partnered with auditors on rebate matters.
  ],
  important: true
)

#v(gap)

#entry(
  "Cash Flow & Financial Modeling Specialist (Freelancer)",
  "Engie Tractebel",
  "March 2023", "December 2023",
  "Brussels, BE",
  [
    - Designed cash-flow reporting and per-project financing-need assessment.
    - Assessed local financing needs, performed countercredit analysis, and conducted impairment testing.
    - Engineered finance data models from SAP HANA, delivering 8 Power BI executive dashboards that turned raw transactions into decision-ready insights for finance leadership.
  ],
  important: false
)

#v(gap)

#entry(
  "Freelance M&A / Corporate Development Consultant",
  "Shurgard",
  "February 2022", "February 2023",
  "Brussels, BE",
  [
    - Advised on self-storage M&A transactions worth €10M to €80M, structuring and negotiating acquisitions, restructurings, and divestitures.
    - Maintained project dashboard and initiated corporate development projects to improve department policies and procedures.
    - Designed the data model and visualization for the Investment department's Business Intelligence efforts.
    - Collaborated in the development of a new pricing model using Artificial Intelligence.
  ],
  important: false
)

#v(gap)

#entry(
  "Freelance CFO / Fundraising Consultant",
  "Magnetrap",
  "November 2020", "January 2022",
  "Mons, BE",
  [
    - Acted as interim CFO and led fundraising, organizing €3M in debt/equity fund raises.
    - Produced cash-flow projections, business plans, and long-term financial goals.
    - Monitored company performance and drove corrective actions.
    - Prepared operating results reports and maintained financial models for long-term use.
  ],
  important: false
)

#v(gap)

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
  ],
  important: false
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
  ],
  important: false
)

#v(gap)

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
  ],
  important: false
)

#v(gap)

#entry(
  "Freelance Business Development & Financial Modeling Director",
  "Vinci Airports",
  "February 2016", "December 2017",
  "Brussels, BE & Lisbon, PT",
  [
    - Led the group's subsidiaries, contributing to a €12B valuation.
    - Led deployment of airport operations at 50+ locations in various countries.
    - Developed long-term financial business model including analysis of macroeconomic impact, capital expenditures, and concession valuation.
    - Negotiated extension of concession contract with Portuguese authorities and implemented new financial business model to improve budgeting and forecasting processes.
    - Managed accounting and financial reporting in accordance with BE-GAAP standards.
  ],
  important: false
)

#v(gap)

#entry(
  "Freelance Finance Consolidation & Reporting Consultant",
  "Rexel",
  "September 2014", "January 2016",
  "Paris, FR",
  [
    - Managed consolidated reporting across a €3B-turnover scope spanning LATAM, APAC, and Canada, aligning GL/AP/AR flows for strong financial-close control.
    - Integrated SAP BPC and Cognos reporting, strengthening GL/AP consolidated reporting.
    - Ran annual budgeting and monthly forecasting (actual vs. budget).
  ],
  important: true
)

#v(gap)

#entry(
  "Financial Auditor Supervisor",
  "KPMG Audit",
  "January 2011", "August 2014",
  "Paris, FR",
  [
    - Audited financial statements under multiple accounting standards (BE-GAAP, SOX), strengthening GL and financial-close controls.
    - Audited financial modelling for long-term PPP contracts.
    - Certified FP7 grant agreements; led audit teams and supervised auditors.
  ],
  important: true
)

#v(gap)

#entry(
  "Deputy CFO Trainee",
  "ICM - Brain & Spine Institute", 
  "November 2009", "August 2010",
  "Paris, FR",
  [
    - Implemented the budget system and prepared business plans for the scientific teams.
    - Established the internal control system for purchasing and donation processes and managed bank reconciliation.
    - #set smartquote(enabled: false)
      Prepared the institutional audit necessary for the certification by the "Comité de la Charte".
  ],
  important: false
)
