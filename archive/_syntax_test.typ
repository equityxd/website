set page(paper: "a4", margin: 24pt)
set text(10pt)

// variant A: trailing block after kwargs
#text(color: rgb(0, 79, 144)) {
  hello A
}

// variant B: content first, then set rule
#text("hello B", color: rgb(0, 79, 144))

// variant C: bracket content after kw
#text(color: rgb(0, 79, 144))["hello C"]
