#import "@preview/octique:0.1.1": *

#let size = 10.5pt
#let block-spacing = size * 0.55
#let block-margin = 22pt
#let list-body-intent = 0.5em

#let envelope = symbol(
  "🖂",

  )

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
  position: none,
  attributes: [],
  body
) = {
  set document(author: profile.name, title: "CV - "+profile.name, keywords: profile.keywords, date: auto)

  set text(size, font: "Source Sans 3", lang: "en")
  set par(leading: size * 0.65, justify: true)

  set list(body-indent: list-body-intent)

  show heading.where(level: 1): body => block(
    width: 100%,
    stroke: (top: 0.5pt),
    inset: (top: block-spacing),
  )[
    #set text(size, weight: "regular")
    #body
  ]

  show heading.where(level: 2): body => block(
    width: 100%,
    stroke: (bottom: 0.25pt),
    inset: (bottom: block-spacing),
    below: block-spacing
  )[
    #set text(size, weight: "regular")
    #body
  ]


  set page(
    paper: "a4",
    margin: 36pt,
    footer: context [
      #set align(right)
      #set text(8pt)
      #counter(page).display(
        "1 of 1",
        both: true,
      )
    ]
  )
  [

    #grid(
      columns: (1fr, 3fr),
      gutter: block-margin,
      [],
      [
        #text(size: 15pt, weight: "black")[#position]
        = #text(size: 12pt, weight: "semibold")[#profile.name]

        #v(size)

        #profile.address \
        #link("mailto:" + profile.mailto)[#octique-inline("mail", width:0.9em, height:0.9em) #profile.mailto] \
        #link("https://" + profile.website)[#octique-inline("globe", width:0.9em, height:0.9em) #profile.website] \ 
        #link("tel:" + profile.tel.replace(" (0) ", " ").replace(" ", "-"))[#octique-inline("device-mobile", width: 0.9em, height:0.9em) #profile.tel]

        #v(size)
        #v(size)

        #emph()[#profile.quote]
      ]
    )
    #v(10%)

    #grid(
      columns: (1fr, 3fr),
      gutter: block-margin,
      [
        #align(start + bottom)[
          #show list: content => [
            #for (index, item) in content.children.enumerate() {
              [#item.body]
               if (index != content.children.len() - 1) [#h(list-body-intent)•#h(list-body-intent)]
            }
          ]
          #text(size: 9pt)[#attributes]
        ]
      ],
      [
        #show heading.where(level: 1): body => block(
          above: block-margin * 3
        )[
          #body
        ]
        #body
      ]
    )
  ]
}

#let entry(
  title: str,
  name: str,
  date_start: none,
  date_end: none,
  location: str,
  intervention: none,
  details: []
) = {
  block(
    above: block-margin,
    below: block-margin,
    breakable: false
  )[
    == #block(width: 100%)[
      #text(weight:"bold")[#name]
      
        
      #place(top + right)[#text(style: "italic")[#location] #h(size *0.5) #if date_start == none and date_end != none [#date_end] else if date_start != none and date_end == none  [#date_start\u{2013}Present] else [#text(style: "italic")[#date_start]\u{2013}#text(style: "italic")[#date_end]]]
        
    ]

  #if intervention != none [
    #columns(2)[
      #title
      #colbreak()
      #align(right)[
       #sym.ast.triple #intervention
      ]
    ]
      ] else [
      #text(weight:"semibold")[#title]
    ]

    #text(size: 10pt, weight: "light")[#details]
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
  attributes: [
    = #text(size: 12pt, weight: "bold")[Competencies]
    == Business
    - MS Office (advanced Excel)

    == ERP
    - SAP HANA

    == Business Intelligence
    - MS Power BI
    - QlikSense
    - Business Object
    - Cognos
    - Hyperion

    == RPA
    - UIpath
    - MS PowerAutomate

    == Agile
    - Jira
    - Confluence

    == Audit
    - IDEA CAATs

    == Planification
    - Visual Planning

    == Data & Analytics
    - VBA
    - SQL
    - R

    #colbreak()

    = #text(size: 12pt, weight: "bold")[Languages]
    == Native
    - French
    - Khmer
    - Teochew

    == Proficient
    - English

    == Basics
    - Dutch(A2)
    - Spanish
    - Mandarin

    = Interest
    - Sustainable development
    - Powerlifting
    - Mountain biking
    - Tennis

    = Interpersonal
    - Fast-learner
    - Problem solver
    - Diplomacy
    - Driven
    - Autonomous
    - Teamplayer
  ],
  body
)

= #text(size: 15pt, weight: "black")[Professional Experience]

#entry(
  title: "Strategic Business Analyst & Finance Automation Lead (Freelancer)",
  name: "Engie SEM",
  date_start: "January 2026",
  date_end: "Present",
  location: "Brussels, BE",
  details: [
    - Led the financial controlling pilot phase for the SAP S/4HANA migration across French subsidiaries, successfully acting as the core Business Analyst bridging IT architecture and strategic business operations.
    - Designed, built, and deployed a robust, automated budget modeling tool from scratch within a critical 2-week timeline, ensuring operational continuity during a resource gap and replacing an unreliable legacy framework.
    - Streamlined and automated financial closing processes for commodity trading activities, deploying advanced PowerQuery ETL workflows to safely ingest batches of 1,500+ bookings per close with zero human intervention.
    - Reconciled complex financial data structures between middle-office databases (IVDB) and SAP S/4HANA while restructuring and simplifying the Work Breakdown Structure (WBS) project codes to optimize portfolio monitoring.
  ]
)

#entry(
  title: "Senior Operational Excellence & Data Lead (Freelancer)",
  name: "Holcim",
  date_start: "January 2024",
  date_end: "December 2025",
  location: "Nivelles, BE",
  details: [
    - Leveraged data insights derived from market analysis to restructure production workflows post-M&A, significantly enhancing efficiency.
    - Managed SAP HANA migration, restructuring data and ensuring system integrity.
    - Developed rebate models (matrix & automated SAP), aligning with commercial strategy.
    - Implemented Qliksense with new data for financial reporting and insights.
    - Ensured data reliability and liaised with auditors on rebate matters.
  ]
)

#entry(
  title: "Cash Flow & Financial Modeling Specialist (Freelancer)",
  name: "Engie Tractebel",
  date_start: "March 2023",
  date_end: "December 2023",
  location: "Brussels, BE",
  details: [
    - Design cashflow reporting and cash exposure per project.
    - Assessment of financing needss in local entity, credit analysis of specific counterpart and impairment testing.
    - Develop Finance data modelling from SAP for HANA and design Power BI reporting.
  ]
)

#entry(
  title: "Investment & Corporate Development Analyst (Freelancer)",
  name: "Shurgard",
  date_start: "February 2022",
  date_end: "February 2023",
  location: "Brussels, BE",
  details: [
    - Analyzed and managed real estate projects, including construction, redevelopment, and acquisition of self-storage businesses.
    - Maintained project dashboard and initiated corporate development projects to improve department policies and procedures.
    - Designed the data model and visualization for the Investment department's Business Intelligence efforts.
    - Collaborated in the development of a new pricing model using Artificial Intelligence.
  ]
)

#entry(
  title: "Head of Controlling",
  name: "Magnetrap",
  date_start: "November 2020",
  date_end: "January 2022",
  location: "Mons, BE",
  details: [
    - Implemented budgeting, forecasting, and financial control systems.
    - Created cash flow projections, business plans, and long-term financial goals.
    - Monitored company performance and implemented corrective actions as needed.
    - Prepared operating results reports and managed financial models for long-term use.
  ]
)

#entry(
  title: "Director Business Process Automation",
  name: "Tobania",
  date_start: "February 2020",
  date_end: "October 2020",
  location: "Brussels, BE",
  details: [
    - Led development and implementation of citizen developer business model using RPA and self-service BI, including pricing strategy and roadmap.
    - Managed business development, including marketing strategy, pre-sales, and sales, and identified new business opportunities.
    - Implemented process optimization, standardization, and harmonization to improve efficiency and profitability for customers.
    - Provided regular, tailored reports to help customers monitor and control costs and make data-driven business decisions, and established change management structures and strategies to facilitate successful adoption of new processes and technologies.
  ]
)

#entry(
  title: "Founder",
  name: "Soap collect",
  date_start: "January 2019",
  date_end: "Present",
  location: "Phnom Penh, KH",
  details: [
    - Established a non-profit organization focused on providing hygiene products to disadvantaged communities.
    - Formed partnerships with luxury hotel chains to source used soap for reconditioning.
  ]
)

#entry(
  title: "Performance Management Project Leader",
  name: "Degroof Petercam",
  date_start: "January 2018",
  date_end: "December 2018",
  location: "Brussels, BE",
  details: [
    - Finance Transformation Operating Model (FTOM)
    - Designed and implemented a client-centric performance management system.
    - Optimized finance close process for improved governance, internal control, and data quality.
    - Led projects related to regulatory reporting sourcing and followed BPM standards.
    - Conducted gap analysis of business requirements and existing procedures to identify areas for improvement.
  ]
)

#entry(
  title: "Managing Director & Head of Project Financial Modeling • Cursus Grand Talent",
  name: "Vinci Airports",
  date_start: "February 2016",
  date_end: "December 2017",
  location: "Brussels, BE & Lisbon, PT",
  details: [
    - Value creation: valuation at 4 times of acquisition cost.
    - Led deployment of airport operations at 50+ locations in various countries.
    - Developed long-term financial business model including analysis of macroeconomic impact, capital expenditures, and concession valuation.
    - Negotiated extension of concession contract with Portuguese authorities and implemented new financial business model to improve budgeting and forecasting processes.
    - Managed accounting and financial reporting in accordance with BE-GAAP standards.
  ]
)

#entry(
  title: "Reporting Consolidation Manager",
  name: "Rexel",
  date_start: "September 2014",
  date_end: "January 2016",
  location: "Paris, FR",
  details: [
    - Led the implementation of IFRS financial reporting for Asia-Pacific, Latin America, and Canadian subsidiaries.
    - Spearheaded the restructuring process and integration of SAP BPC and Cognos reporting systems.
    - Performed annual budgeting, monthly forecasting, and analyses of actual vs. budgeted/estimated results.
    - Led the strategic planning process for the organization.
  ]
)

#entry(
  title: "Financial Auditor Supervisor",
  name: "KPMG Audit",
  date_start: "January 2011",
  date_end: "August 2014",
  location: "Paris, FR",
  details: [
    - Conducted audits of financial statements using various accounting standards, including testing of key processes in accordance with SOX requirements.
    - Experienced in auditing financial modeling for long-term contracts, particularly in the context of Public-Private Partnerships (PPP).
    - Certified FP7 Grant Agreements for the EU Research program and led audit teams and supervised financial auditors.
    - Developed partnerships and identified new markets to support business growth.
    Main sector: Construction (Vinci, Eiffage, Colas), Real estate (Nexity), Water distribution (Veolia), International parcels distribution (Geopost from La Poste group), Security (Brink’s), Healthcare (DomusVie).
  ]
)

#entry(
  title: "Deputy CFO Trainee",
  name: "ICM - Brain & Spine Institute", 
  date_start: "November 2009",
  date_end: "August 2010",
  location: "Paris, FR",
  details: [
    - Implemented the budget system and prepared business plans for the scientific teams.
    - Established the internal control system for purchasing and donation processes and managed bank reconciliation.
    - Prepared the institutional audit necessary for the certification by the "Comité de la Charte".
  ]
)

= #text(size: 15pt, weight: "black")[Education]

#entry(
  title: "Specialized Master, Auditing and Consulting",
  name: "ESCP Business School (Top #1 in Europe @ FT 2026)",
  location: "Paris, FR",
  date_start: 2010,
  date_end: 2011,
)

#entry(
  title: "Master’s degree, Management Science and Financial Control",
  name: "Université Paris Nanterre",
  location: "Paris, FR",
  date_start: 2005,
  date_end: 2010,
)
