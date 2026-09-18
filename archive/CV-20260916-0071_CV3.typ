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
    keywords: "Director of Finance, Financial Reporting, Budgeting, Forecasting, Multi-entity GL, AP/AR, Financial Close, Cash Flow, Treasury, P&L, Power BI, Cognos, SAP S/4HANA, Consolidation, IFRS, BE-GAAP, Decision-Support, Cross-functional Partnering",
    quote: "Director of Finance with hands-on multi-entity finance operations across 12+ entities in BE, FR and NL: month-end close, budgeting & forecasting, cash flow and treasury, and IFRS / BE-GAAP consolidation. I combine operator discipline with executive partnering — from interim CFO / treasury at a startup to financial controlling on SAP S/4HANA migrations — to deliver decision-support across remote, multi-country teams."
  ),
  position: "Director of Finance",

  education: [
    #edu(
      "ESCP Business School",
      "(#1 FT 2026)",
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

#text(s, weight: "semibold", style: "normal\)[Competencies]
#v(gap-m)
#set text(size: 9pt)
#grid(
          [
            ==== Multi-Entity Finance Operations
            - Multi-entity GL / AP / AR
            - Consolidation / IFRS / BE-GAAP
            - Cash flow management / treasury
            - Financial close / month-end close
            - Budgeting & forecasting
        ],
          [
            ==== Strategic & Executive Finance
            - P&L / P&L-adjacent partnership
            - BI / executive reporting (Power BI)
            - Financial modeling
            - Cross-functional / operations partnering
            - Remote / hybrid / multi-country
        ],
      ],
    ]

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