p = "gen_cv_typ.py"
s = open(p, encoding="utf-8").read()

old = "            - MS Power Bi\\n\n            - Cognos\\n"
new = "            - MS Power Bi\\n\n            - Qlik Sense\\n\n            - Cognos\\n"

c = s.count(old)
print("old count:", c)
assert c == 1, c
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(s)
print("DONE: Qlik Sense inserted after MS Power BI")
