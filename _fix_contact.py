# Roll back fa-icon contact block to plain text in the generator.
p = "gen_cv_typ.py"
with open(p, encoding="utf-8") as f:
    s = f.read()

old = (
    '    new_contact = \'\'\'        #text(size: 9pt, style: "italic")[\n'
    '          #fa-icon("location-dot", fill: rgb("#333333")) Rue Montagne de l\'Oratoire 28/76\\\\\n'
    '          #fa-icon("location-dot", fill: rgb("#333333")) B-1000 Brussels\\\\\n'
    '          #fa-icon("envelope", fill: rgb("#333333")) #profile.mailto\\\\\n'
    '          #fa-icon("globe", fill: rgb("#333333")) #profile.website\\\\\n'
    '          #fa-icon("mobile", fill: rgb("#333333")) #profile.tel\n'
    '        ]\n'
    '\'\'\'\n'
)

new = (
    '    new_contact = \'\'\'        #text(size: 9pt, style: "italic")[\n'
    '          Rue Montagne de l\'Oratoire 28/76\\\\\n'
    '          B-1000 Brussels\\\\\n'
    '          #profile.mailto\\\\\n'
    '          #profile.website\\\\\n'
    '          #profile.tel\n'
    '        ]\n'
    '\'\'\'\n'
)

if old not in s:
    raise SystemExit("old new_contact block not found — aborting")

s = s.replace(old, new, 1)
with open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("replaced new_contact -> plain text")
