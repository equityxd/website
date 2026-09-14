#import @preview/fontawesome:0.6.0: fa-icon
#show: rendercv.with(name: "Test", title: "Test", footer: context {}, locale-catalog-language: "en")
// ============================================================================
// Custom header (replaces RenderCV's native Header.j2.typ).
//
// Reproduces the original hand-crafted design exactly:
//   - Title:   "Ernest SONG   ◆   Chief Growth & Transformation Officer" (centered)
//   - Left col: contact lines rendered from cv.custom_connections (fa-icon + text)
//   - Right col: profile quote (Ernest's fixed Profile text)
//   - Two 0.75pt dividers framing the block
//
// NOTE: the profile quote is baked in because RenderCV's CV model has no
// top-level "quote" field. All contact lines are carried by
// `cv.custom_connections` so the built-in email/website/phone fields are
// ignored (the custom header never calls the native #connections()).
// ============================================================================
#import "@preview/fontawesome:0.6.0": fa-icon

// ---- Title (name ◆ headline) ----
#align(center)[
  #text(size: 18pt, weight: "bold")[Ernest SONG]
  #h(10pt)
  #text(size: 18pt)[\()]
  #h(10pt)
  #text(size: 14pt, style: "normal")[{{ cv.headline }}]
]
#v(2pt)
#line(length: 100%, stroke: (thickness: 0.75pt))
#v(16pt)

// ---- Contact (left) + Quote (right) ----
#grid(
  columns: (1.1fr, 2.9fr),
  gutter: 16pt,
  [
    {% for c in cv.custom_connections %}
    #text(color: rgb(0, 79, 144)) {
      #fa-icon(name: "{{ c.fontawesome_icon }}", size: 0.6em) {
        #text(size: 9pt)[{{ c.placeholder }}]
      }
    }
    #v(4pt)
    {% endfor %}
  ],
  [
    #set text(color: rgb(0, 79, 144))
    #set par(justify: true)
    #set text(hyphenate: true)
    #text(size: 9pt, style: "italic")[Finance leader with 15+ years leading accounting and transformation mandates for multi-entity, multi-country organisations across BE, FR and NL. I specialise in General Accounting (GL, AP, AR) and financial-close leadership, and in guiding ERP replacements from AS-IS diagnosis to SAP S/4HANA go-live. What sets me apart is perspective: I've sat on both the operator's and the executive-recruiter's side of the table, so I read the numbers and the organisation behind them. I bring calm under pressure, rigorous Power BI / Cognos reporting, and a genuine commitment to turning finance into a lever for growth.]
  ]
)
#line(length: 100%, stroke: (thickness: 0.75pt))
#v(16pt)
