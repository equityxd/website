"""Typst builder — turn the master data model (data/profile.json) into a valid .typ file.

This makes ``profile.json`` the single source of truth:

  * the Astro portfolio site reads ``profile.json`` directly;
  * the CV-for-JD engine (``generation/engine.py``) reads the .typ produced here;

So every website update flows into BOTH the portfolio and generated CVs. The
generated .typ intentionally mirrors the shape of ``source/SONG Ernest - CV v1.typ``
so the existing regex engine (_cv_content, _compact_facts) keeps working.
"""

import json
from pathlib import Path


def _esc(s):
    """Escape backslashes and double-quotes for Typst string literals."""
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def _q(s):
    """Return a Typst/Python string literal ``"escaped"`` for a location value."""
    if not s:
        return "none"
    return '"%s"' % _esc(s)


def build_typ(data):
    """Generate a valid .typ source string from the master data model."""
    profile = data.get("profile", {})
    p = []

    def L(line=""):
        p.append(line)

    # Header
    L("// Auto-generated from data/profile.json — do not edit by hand.")
    L("// Regenerate with:  python generation/typst_builder.py")
    L("")
    L("")
    L('#import "@preview/octique:0.1.1": *;')
    L("")
    L()

    # Type scale
    L("// ── Type scale (4 steps) ──")
    L("#let s        = 10pt   // body base: company names, job titles, column headings, bullets, contact, footer")
    L("#let s-name   = 18pt   // name (title, largest)")
    L("#let s-head   = 12pt   // position/subtitle + main section headings (h1)")
    L("#let s-small  = 9pt    // secondary: dates, subheadings, inline contact lines")
    L("#let s-xsmall = 6.5pt    // tighter: date headers")
    L("")
    L()
    L("// ── Rhythm ──")
    L("#let leading     = s * 1.2")
    L("#let gap         = 4pt   // between major blocks and between entries")
    L("#let gap-m       = 2pt   // heading underline padding")
    L("#let gutter      = 16pt // grid gutters")
    L("#let page-margin = 24pt")
    L("#let indent      = 0.35em")
    L("")
    L()

    # Entry helper
    L("#let entry(title, name, date_start, date_end, location, details, important: false) = {")
    L("  let date_str = if date_start == none and date_end != none {")
    L("    str(date_end)")
    L("  } else if date_start != none and date_end == none {")
    L('    str(date_start) + " – Present"')
    L("  } else if date_start != none and date_end != none {")
    L('    str(date_start) + " – " + str(date_end)')
    L("  } else {")
    L('    ""')
    L("  }")
    L("")
    L("  let content = block(breakable: false)[")
    L("    #v(1pt)")
    L('    #text(s, weight: "bold")[#name] #h(1fr) #text(s, style: "italic")[#date_str  |  #location]')
    L("    #v(-1pt)")
    L("")
    L("    #if important {")
    L('      highlight(fill: rgb(224, 224, 224))[#text(s, weight: "semibold", style: "normal")[#title]]')
    L("    } else {")
    L('      text(s, weight: "semibold", style: "normal")[#title]')
    L("    }")
    L("    #v(-1pt)")
    L("")
    L("    #if details != none {")
    L('      text(s-small, style: "italic")[#details]')
    L("    }")
    L("    #v(1pt)")
    L("  ]")
    L("")
    L("  content")
    L("}")
    L("")
    L()

    # Education helper
    L("// Education uses a dedicated 5-line layout:")
    L("//   Org name — rank (#rank) — date | location — degree — field")
    L("#let edu(name, rank, date_start, date_end, location, degree, field) = {")
    L("  let date_str = if date_start == none and date_end != none {")
    L("    str(date_end)")
    L("  } else if date_start != none and date_end == none {")
    L('    str(date_start) + " – Present"')
    L("  } else if date_start != none and date_end != none {")
    L('    str(date_start) + " – " + str(date_end)')
    L("  } else {")
    L('    ""')
    L("  }")
    L("")
    L("  stack(spacing: 0pt)[")
    L('    #text(s, weight: "bold", style: "normal")[#name]')
    L("    #if rank != none {")
    L("      linebreak()")
    L('      text(s-small, style: "normal")[#rank]')
    L("    }")
    L("    #linebreak()")
    L('    #text(s-small, style: "italic")[#date_str  |  #location]')
    L("    #linebreak()")
    L('    #text(s, style: "normal")[#degree]')
    L("    #linebreak()")
    L('    #text(s-small, style: "italic")[#field]')
    L("  ]")
    L("}")
    L("")
    L()

    # Profile call
    L("#show: body => resume(")
    L("  profile: (")
    L('    name: "%s",' % _esc(profile.get("name", "")))
    L('    address: "%s",' % _esc(profile.get("address", "")))
    L('    mailto: "%s",' % _esc(profile.get("mailto", "")))
    L('    website: "%s",' % _esc(profile.get("website", "")))
    L('    tel: "%s",' % _esc(profile.get("tel", "")))
    kw = ", ".join(_esc(k) for k in profile.get("keywords", []))
    L('    keywords: "%s",' % kw)
    L('    quote: "%s",' % _esc(profile.get("quote", "")))
    L("  ),")
    L('  position: "%s",' % _esc(profile.get("role", "")))
    L("")

    # Education entries
    L("  // ── Education ──")
    L("  education: [")
    edu_list = data.get("education", [])
    for i, edu in enumerate(edu_list):
        org = _esc(edu.get("org", ""))
        rank = ('"%s"' % _esc(edu["rank"])) if edu.get("rank") else "none"
        ds = edu.get("dateStart")
        de = edu.get("dateEnd")
        loc = _esc(edu.get("location", ""))
        degree = _esc(edu.get("degree", ""))
        field = _esc(edu.get("field", ""))
        ds_s = str(ds) if ds is not None else "none"
        de_s = str(de) if de is not None else "none"
        L("    #edu(")
        L('      "%s",' % org)
        L("      %s," % rank)
        L("      %s, %s," % (ds_s, de_s))
        L('      "%s",' % loc)
        L('      "%s",' % degree)
        L('      "%s"' % field)
        L("    )")
        if i < len(edu_list) - 1:
            L("")
    L("  ],")
    L("")

    # Competencies
    L("  // ── Competencies ──")
    L("  competencies: [")
    for comp in data.get("competencies", []):
        group = comp.get("group", "")
        if group:
            L("    ==== %s" % _esc(group))
        for item in comp.get("items", []):
            L("    - %s" % _esc(item))
    L("  ],")
    L("")

    # Languages
    L("  // ── Languages ──")
    L("  languages: [")
    for lang in data.get("languages", []):
        level = lang.get("level", "")
        items = lang.get("items", [])
        parts = []
        if level:
            parts.append('#text(s-small, weight: "semibold", style: "normal")[%s:]' % _esc(level))
        for item in items:
            parts.append('#text(s-small, weight: "semibold", style: "normal")[%s]' % _esc(item))
        L("    " + " \\\n      ".join(parts))
    L("  ],")
    L("")

    # Interests
    L("  // ── Interests ──")
    L("  interests: [")
    L("    %s" % ", ".join(_esc(i) for i in data.get("interests", [])))
    L("  ],")
    L("")

    # Interpersonal
    L("  // ── Interpersonal ──")
    L("  interpersonal: [")
    L("    %s" % ", ".join(_esc(i) for i in data.get("interpersonal", [])))
    L("  ],")
    L("")

    L("  body")
    L(")")
    L("")
    L()

    # Professional Experience
    L("// ── Professional Experience ──")
    L('= Professional Experience')
    L("")
    L("#v(gap)")

    for exp in data.get("experience", []):
        L("")
        L("#entry(")
        L('      "%s",' % _esc(exp.get("title", "")))
        L('      "%s",' % _esc(exp.get("company", "")))
        ds = exp.get("dateStart")
        de = exp.get("dateEnd")
        L("      %s," % (str(ds) if ds is not None else "none"))
        L("      %s," % (str(de) if de is not None else "none"))
        loc_arg = _q(exp.get("location"))
        L("      %s," % loc_arg)
        details = exp.get("details", []) or []
        if details:
            L("      [")
            for d in details:
                L("        %s" % _esc(d))
            L("      ],")
        else:
            L("      none,")
        L("      important: %s," % ("true" if exp.get("highlight") else "false"))
        L("    )")
    L()

    return "\n".join(p) + "\n"


def main():
    here = Path(__file__).resolve().parent.parent
    profile_json = here / "MyWebsite" / "src" / "data" / "profile.json"
    out_typ = here / "MyWebsite" / "src" / "data" / "profile.typ"

    if not profile_json.exists():
        raise SystemExit("profile.json not found: %s" % profile_json)

    data = json.loads(profile_json.read_text(encoding="utf-8"))
    typ = build_typ(data)
    out_typ.write_text(typ, encoding="utf-8")
    print("Wrote %s (%d bytes)" % (out_typ, len(typ)))


if __name__ == "__main__":
    main()
