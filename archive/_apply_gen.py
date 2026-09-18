import re

gen_path = "gen_cv_typ.py"
base_path = "source/SONG Ernest - CV v1.typ"

gen = open(gen_path, encoding="utf-8").read()
base = open(base_path, encoding="utf-8").read()

# ---- Locate the contact block in the BASE template ----
start_marker = '        #octique-inline("location", width: 0.6em) #text(s-small)[Rue Montagne de l\'Oratoire 28/76]\n'
end_marker = '        #octique-inline("device-mobile", width: 0.6em) #text(s-small)[#profile.tel]\n'
assert start_marker in base, "base start_marker not found"
assert end_marker in base, "base end_marker not found"
contact_block = base[base.index(start_marker):base.index(end_marker) + len(end_marker)]
# contact_block contains the 5 octique lines + interleaved #v(-9pt) lines, ending with last octique line + \n
assert contact_block.count("#octique-inline") == 4, contact_block.count("#octique-inline")

# ---- Locate the Block 3 comment in the BASE template ----
b3 = "    // \u2500\u2500\u2500 BLOCK 3 : Three columns (reduced content) \u2500\u2500\u2500\n    #context[\n"
assert b3 in base, "base block3 comment not found"

def py_str_literal(text):
    # Produce a valid single-quoted Python string literal representing `text`,
    # escaping backslash and apostrophe.
    out = text.replace("\\", "\\\\").replace("'", "\\'")
    return "'" + out + "'"

# old_contact: reproduce the base template's octique contact block verbatim
# Split contact_block into physical lines (each already includes a trailing \n)
lines = contact_block.splitlines(keepends=True)
old_contact_joined = "".join(lines)  # real newlines
old_contact_py = py_str_literal(old_contact_joined)

# new_contact: replace the 5 octique lines with plain text-labelled lines (ATS machine-readable)
new_lines = [
    "        #text(s-small)[Rue Montagne de l'Oratoire 28/76 \u00a7 B-1000 Brussels]\n",  # euro
    "        #v(-9pt)\n",
    "        #text(s-small)[Email: #profile.mailto]\n",
    "        #v(-9pt)\n",
    "        #text(s-small)[Web: #profile.website]\n",
    "        #v(-9pt)\n",
    "        #text(s-small)[Tel: #profile.tel]\n",
]
new_contact_joined = "".join(new_lines)
new_contact_py = py_str_literal(new_contact_joined)

profile_py = py_str_literal(
    "    // PROFILE HIGHLIGHT (JD-relevance callout) -- inserted above competencies\n"
    "    #text(s-head, weight: "bold")[\n"
    "      ERP Replacement (Infor M3, phasing out legacy AS/400) \u00b7\n"
    "      Business Blueprint (BBP) sign-off authority \u00b7\n"
    "      GL, AP, AR across multi-entity / multi-country (BE, FR, NL)\n"
    "    ]\n"
    "    #v(gap-m)\n\n"
)

addition = (
    "    t = t.replace(old_grid, new_grid, 1)\n\n"
    "    # 5a) Rec 8 - PROFILE HIGHLIGHT (JD-relevance callout) above competencies\n"
    "    highlight = " + profile_py + "\n\n"
    "    # 5b) Rec 7 - ATS: octique contact icons -> plain text-labelled lines (machine-readable)\n"
    "    old_contact = " + old_contact_py + "\n\n"
    "    new_contact = " + new_contact_py + "\n\n"
    "    assert old_contact in t, \"old_contact not found in base\"\n"
    "    assert new_contact not in t, \"new_contact already present\"\n"
    "    t = t.replace(old_contact, new_contact, 1)\n\n"
)

anchor = "    t = t.replace(old_grid, new_grid, 1)\n"
assert gen.count(anchor) == 1, ("anchor count", gen.count(anchor))
gen = gen.replace(anchor, addition, 1)

open(gen_path, "w", encoding="utf-8").write(gen)
print("Wrote", gen_path)
