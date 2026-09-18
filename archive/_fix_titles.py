#!/usr/bin/env python3
"""Fix professional-experience titles in the generator (org-anchored)."""
import re

path = "gen_cv_typ.py"
with open(path, encoding="utf-8") as f:
    lines = f.read().split("\n")

# org-name -> new title
mapping = {
    "Shurgard": "M&A / Corporate Development Consultant (Freelancer)",
    "Vinci Airports": "Head of Controlling",
    "Rexel": "Head of Controlling",
}

def parse_title(line):
    # line is e.g.         '  "TITLE",\\n'  (the \\n is a literal backslash + n)
    s = line.strip()
    assert s.startswith("'"), "unexpected line: %r" % line
    s = s[1:]            # drop leading '
    s = s[2:]            # drop the two spaces after '
    assert s.startswith('"'), "unexpected after peel: %r" % line
    s = s[1:]            # drop leading "
    s = s[:-5]           # drop trailing ",\\n'  (5 chars: " , \\ n ')
    return s

def apply(org, new_title):
    for i, line in enumerate(lines):
        if ('"%s",' % org) in line and line.strip().startswith("'"):
            tidx = i - 1
            old_title = parse_title(lines[tidx])
            print("  %s: %r -> %r" % (org, old_title, new_title))
            indent = line[:len(line) - len(line.lstrip(" "))]
            # rebuild: <indent>'  <title>,<backslash>n'<newline>  (single literal backslash)
            lines[tidx] = "%s'  %s,\\n'\n" % (indent, new_title)
            return
    raise SystemExit("org %s not found" % org)

for org, new_title in mapping.items():
    apply(org, new_title)

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("applied title fixes")
