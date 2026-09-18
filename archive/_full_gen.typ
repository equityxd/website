// Import the rendercv function and all the refactored components
#import "@preview/rendercv:0.3.0": *

// Apply the rendercv template with custom configuration
#show: rendercv.with(
  name: "Ernest SONG",
  title: "Ernest SONG - CV",
  footer: context { [#emph[Ernest SONG -- #str(here().page())\/#str(counter(page).final().first())]] },
  top-note: [ #emph[Last updated in Sept 2026] ],
  locale-catalog-language: "en",
  text-direction: ltr,
  page-size: "us-letter",
  page-top-margin: 0.7in,
  page-bottom-margin: 0.7in,
  page-left-margin: 0.7in,
  page-right-margin: 0.7in,
  page-show-footer: true,
  page-show-top-note: true,
  colors-body: rgb(0, 0, 0),
  colors-name: rgb(0, 79, 144),
  colors-headline: rgb(0, 79, 144),
  colors-connections: rgb(0, 79, 144),
  colors-section-titles: rgb(0, 79, 144),
  colors-links: rgb(0, 79, 144),
  colors-footer: rgb(128, 128, 128),
  colors-top-note: rgb(128, 128, 128),
  typography-line-spacing: 0.6em,
  typography-alignment: "justified",
  typography-date-and-location-column-alignment: right,
  typography-font-family-body: "Source Sans 3",
  typography-font-family-name: "Source Sans 3",
  typography-font-family-headline: "Source Sans 3",
  typography-font-family-connections: "Source Sans 3",
  typography-font-family-section-titles: "Source Sans 3",
  typography-font-size-body: 10pt,
  typography-font-size-name: 30pt,
  typography-font-size-headline: 10pt,
  typography-font-size-connections: 10pt,
  typography-font-size-section-titles: 1.4em,
  typography-small-caps-name: false,
  typography-small-caps-headline: false,
  typography-small-caps-connections: false,
  typography-small-caps-section-titles: false,
  typography-bold-name: true,
  typography-bold-headline: false,
  typography-bold-connections: false,
  typography-bold-section-titles: true,
  links-underline: false,
  links-show-external-link-icon: false,
  header-alignment: center,
  header-photo-width: 3.5cm,
  header-space-below-name: 0.7cm,
  header-space-below-headline: 0.7cm,
  header-space-below-connections: 0.7cm,
  header-connections-hyperlink: true,
  header-connections-show-icons: true,
  header-connections-display-urls-instead-of-usernames: false,
  header-connections-separator: "",
  header-connections-space-between-connections: 0.5cm,
  section-titles-type: "with_partial_line",
  section-titles-line-thickness: 0.5pt,
  section-titles-space-above: 0.5cm,
  section-titles-space-below: 0.3cm,
  sections-allow-page-break: true,
  sections-space-between-text-based-entries: 0.3em,
  sections-space-between-regular-entries: 1.2em,
  entries-date-and-location-width: 4.15cm,
  entries-side-space: 0.2cm,
  entries-space-between-columns: 0.1cm,
  entries-allow-page-break: false,
  entries-short-second-row: true,
  entries-degree-width: 1cm,
  entries-summary-space-left: 0cm,
  entries-summary-space-above: 0cm,
  entries-highlights-bullet:  "•" ,
  entries-highlights-nested-bullet:  "•" ,
  entries-highlights-space-left: 0.15cm,
  entries-highlights-space-above: 0cm,
  entries-highlights-space-between-items: 0cm,
  entries-highlights-space-between-bullet-and-text: 0.5em,
  date: datetime(
    year: 2026,
    month: 9,
    day: 13,
  ),
)

#import "@preview/octique:0.1.1": *

#grid(
  columns: (1.1fr, 2.9fr),
  gutter: 16pt,
  [
      [#octique-inline("home", width: 0.6em) Rue Montagne de l'Oratoire 28/76]
      #v(4pt)
      [#octique-inline("home", width: 0.6em) B-1000 Brussels]
      #v(4pt)
      [#octique-inline("envelope", width: 0.6em) contact@ernestsong.com]
      #v(4pt)
      [#octique-inline("globe", width: 0.6em) ernestsong.com]
      #v(4pt)
      [#octique-inline("phone", width: 0.6em) +32 476 60 05 90]
      #v(4pt)
  ],
  [
    #text(size: 9pt, style: "italic")[Chief Growth & Transformation Officer]
  ]
)

== Experience

#regular-entry(
  [
    #strong[Engie SEM], Strategic Business Analyst & Finance Automation Lead (Freelancer)

    - Led the financial controlling pilot phase for the SAP S\/4HANA migration across French subsidiaries, successfully acting as the core Business Analyst bridging IT architecture and strategic business operations.

    - Designed, built, and deployed a robust, automated budget modeling tool from scratch within a critical 2-week timeline, ensuring operational continuity during a resource gap and replacing an unreliable legacy framework.

    - Streamlined and automated financial closing processes for commodity trading activities, deploying advanced PowerQuery ETL workflows to safely ingest batches of 1,500+ bookings per close with zero human intervention.

    - Reconciled complex financial data structures between middle-office databases (IVDB) and SAP S\/4HANA while restructuring and simplifying the Work Breakdown Structure (WWS) project codes to optimize portfolio monitoring.

  ],
  [
    Brussels, BE

    Jan 2026 – present

    

    9 months

  ],
)

#regular-entry(
  [
    #strong[Holcim], Senior Operational Excellence & Data Lead (Freelancer)

    - Leveraged data insights derived from market analysis to restructure production workflows post-M&A, significantly enhancing efficiency.

    - Managed SAP HANA migration, restructuring data and ensuring system integrity.

    - Developed rebate models (matrix & automated SAP), aligning with commercial strategy.

    - Implemented Qliksense with new data for financial reporting and insights.

    - Ensured data reliability and liaised with auditors on rebate matters.

  ],
  [
    Nivelles, BE

    Jan 2024 – Dec 2025

    

    2 years

  ],
)

#regular-entry(
  [
    #strong[Engie Tractebel], Cash Flow & Financial Modeling Specialist (Freelancer)

    - Design cashflow reporting and cash exposure per project.

    - Assessment of financing needs in local entity, credit analysis of specific counterpart and impairment testing.

    - Develop Finance data modelling from SAP for HANA and design Power BI reporting.

  ],
  [
    Brussels, BE

    Mar 2023 – Dec 2023

    

    10 months

  ],
)

#regular-entry(
  [
    #strong[Shurgard], Investment & Corporate Development Analyst (Freelancer)

    - Analyzed and managed real estate projects, including construction, redevelopment, and acquisition of self-storage businesses.

    - Maintained project dashboard and initiated corporate development projects to improve department policies and procedures.

    - Designed the data model and visualization for the Investment department's Business Intelligence efforts.

    - Collaborated in the development of a new pricing model using Artificial Intelligence.

  ],
  [
    Brussels, BE

    Feb 2022 – Feb 2023

    

    1 year 1 month

  ],
)

#regular-entry(
  [
    #strong[Magnetrap], Freelance CFO \/ Fundraising Consultant

    - Acted as interim CFO and led fundraising, organizing €3M in debt\/equity fund raises.

    - Created cash flow projections, business plans, and long-term financial goals.

    - Monitored company performance and implemented corrective actions as needed.

    - Prepared operating results reports and managed financial models for long-term use.

  ],
  [
    Mons, BE

    Nov 2020 – Jan 2022

    

    1 year 3 months

  ],
)

#regular-entry(
  [
    #strong[Tobania], Director Business Process Automation

    - Led development and implementation of citizen developer business model using RPA and self-service BI, including pricing strategy and roadmap.

    - Managed business development, including marketing strategy, pre-sales, and sales, and identified new business opportunities.

    - Implemented process optimization, standardization, and harmonization to improve efficiency and profitability for customers.

    - Provided regular, tailored reports to help customers monitor and control costs and make data-driven business decisions, and established change management structures and strategies to facilitate successful adoption of new processes and technologies.

  ],
  [
    Brussels, BE

    Feb 2020 – Oct 2020

    

    9 months

  ],
)

#regular-entry(
  [
    #strong[Soap collect], Founder

    - Established a non-profit organization focused on providing hygiene products to disadvantaged communities.

    - Formed partnerships with luxury hotel chains to source used soap for reconditioning.

  ],
  [
    Phnom Penh, KH

    Jan 2019 – present

    

    7 years 9 months

  ],
)

#regular-entry(
  [
    #strong[Degroof Petercam], Performance Management Project Leader

    - Finance Transformation Operating Model (FTOM)

    - Designed and implemented a client-centric performance management system.

    - Optimized finance close process for improved governance, internal control, and data quality.

    - Led projects related to regulatory reporting sourcing and followed BPM standards.

    - Conducted gap analysis of business requirements and existing procedures to identify areas for improvement.

  ],
  [
    Brussels, BE

    Jan 2018 – Dec 2018

    

    1 year

  ],
)

#regular-entry(
  [
    #strong[Vinci Airports], Managing Director & Head of Project Financial Modeling \/ Cursus Grand Talent

    - Value creation: valuation at 4 times of acquisition cost.

    - Led deployment of airport operations at 50+ locations in various countries.

    - Developed long-term financial business model including analysis of macroeconomic impact, capital expenditures, and concession valuation.

    - Negotiated extension of concession contract with Portuguese authorities and implemented new financial business model to improve budgeting and forecasting processes.

    - Managed accounting and financial reporting in accordance with BE-GAAP standards.

  ],
  [
    Brussels, BE & Lisbon, PT

    Feb 2016 – Dec 2017

    

    1 year 11 months

  ],
)

#regular-entry(
  [
    #strong[Rexel], Freelance Finance Consolidation & Reporting Consultant

    - Led the implementation of IFRS financial reporting for Asia-Pacific, Latin America, and Canadian subsidiaries.

    - Spearheaded the restructuring process and integration of SAP BPC and Cognos reporting systems.

    - Performed annual budgeting, monthly forecasting, and analyses of actual vs. budgeted\/estimated results.

    - Led the strategic planning process for the organization.

  ],
  [
    Paris, FR

    Sept 2014 – Jan 2016

    

    1 year 5 months

  ],
)

#regular-entry(
  [
    #strong[KPMG Audit], Financial Auditor Supervisor

    - Conducted audits of financial statements using various accounting standards, including testing of key processes in accordance with SOX requirements.

    - Experienced in auditing financial modeling for long-term contracts, particularly in the context of Public-Private Partnerships (PPP).

    - Certified FP7 Grant Agreements for the EU Research program and led audit teams and supervised financial auditors.

    - Developed partnerships and identified new markets to support business growth.

    - Main sector: Construction (Vinci, Eiffage, Colas), Real estate (Nexity), Water distribution (Veolia), International parcels distribution (Geopost from La Poste group), Security (Brink's), Healthcare (DomusVie).

  ],
  [
    Paris, FR

    Jan 2011 – Aug 2014

    

    3 years 8 months

  ],
)

#regular-entry(
  [
    #strong[ICM - Brain & Spine Institute], Deputy CFO Trainee

    - Implemented the budget system and prepared business plans for the scientific teams.

    - Established the internal control system for purchasing and donation processes and managed bank reconciliation.

    - Prepared the institutional audit necessary for the certification by the 'Comité de la Charte'.

  ],
  [
    Paris, FR

    Nov 2009 – Aug 2010

    

    10 months

  ],
)

== Education

#education-entry(
  [
    #strong[ESCPS Business School], \#1 FT 2026

    #summary[Auditing and Consulting]

    - Ranked \#1 full-time Master in 2026 (FT Rankings)

  ],
  [
    Paris, FR

    2011

  ],
  degree-column: [
    #strong[Specialized Master's degree]
  ],
)

#education-entry(
  [
    #strong[Université Paris Nanterre], Management Science and Financial Control

    #summary[Management Science and Financial Control]

  ],
  [
    Paris, FR

    2010

  ],
  degree-column: [
    #strong[Master's degree]
  ],
)

== Competencies

#regular-entry(
  [
    #strong[Business]

    - MS Office (advanced Excel, Power Query)

  ],
  [
  ],
)

#regular-entry(
  [
    #strong[ERP]

    - SAP HANA

  ],
  [
  ],
)

#regular-entry(
  [
    #strong[Business Intelligence]

    - MS Power BI

    - QlikSense

    - Business Object

    - Cognos

    - Hyperion

  ],
  [
  ],
)

#regular-entry(
  [
    #strong[RPA]

    - UIpath

    - MS PowerAutomate

  ],
  [
  ],
)

#regular-entry(
  [
    #strong[Agile]

    - Jira

    - Confluence

  ],
  [
  ],
)

#regular-entry(
  [
    #strong[Data & Analytics]

    - VBA

    - SQL

    - R

  ],
  [
  ],
)

== Languages

#regular-entry(
  [
    #strong[Native:]

    - French

    - Khmer

    - Teochew

  ],
  [
  ],
)

#regular-entry(
  [
    #strong[Proficient:]

    - English

  ],
  [
  ],
)

#regular-entry(
  [
    #strong[Basics:]

    - Dutch (A2)

    - Spanish

    - Mandarin

  ],
  [
  ],
)

== Interests

Sustainable development

Powerlifting

Mountain biking

Tennis

== Interpersonal

Fast-learner

Problem solver

Diplomacy

Driven

Autonomous

Teamplayer
