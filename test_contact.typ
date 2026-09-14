set page(page_a4, margin: 12pt)
set text(lang: "en")
set par(leading: 7pt)
#let marker = rect(width: 0.6em, height: 0.6em, fill: blue)

// --- (A) current: icon + separate #text + #v(4pt) ---
#grid(
  columns: (1.1fr, 2.9fr),
  gutter: 20pt,
  [
    #marker #text(9pt)[Rue Montagne de l'Oratoire 28/76]
    #v(4pt)
    #h(0.7em) #text(9pt)[B-1000 Brussels]
    #v(4pt)
    #marker #text(9pt)[Email marker value here]
    #v(4pt)
    #marker #text(9pt)[www dot ernestsong dot com]
    #v(4pt)
    #marker #text(9pt)[+32 476 60 05 90]
  ],
  [
    #set par(justify: true)
    #text(size: 9pt, style: "italic")[This is a long quote line one that wraps to make sure the inter-line spacing of the quote paragraph is stable and reproducible for measuring against the contact block on the left.]
  ]
)

// --- (B) single multi-line text block (no markers) ---
#grid(
  columns: (1.1fr, 2.9fr),
  gutter: 20pt,
  [
    #text(9pt)[
 Rue Montagne de l'Oratoire 28/76
 B-1000 Brussels
 Email marker value here
 www doternestsong dot com
 +32 476 60 05 90]
  ],
  [
    #set par(justify: true)
    #text(size: 9pt, style: "italic")[This is a long quote line one that wraps to make sure the inter-line spacing of the quote paragraph is stable and reproducible for measuring against the contact block on the left.]
  ]
)

// --- (C) single multi-line text block WITH markers per line ---
#grid(
  columns: (1.1fr, 2.9fr),
  gutter: 20pt,
  [
    #text(9pt)[
      #marker Rue Montagne de l'Oratoire 28/76
      #marker Email marker value here
      #marker www doternestsong dot com
      #marker +32 476 60 05 90]
  ],
  [
    #set par(justify: true)
    #text(size: 9pt, style: "italic")[This is a long quote line one that wraps to make sure the inter-line spacing of the quote paragraph is stable and reproducible for measuring against the contact block on the left.]
  ]
)
