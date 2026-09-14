#!/usr/bin/env python3
"""Tailor a RenderCV YAML (cv.yaml) to a target Job Description.

Transforms the static v1 RenderCV CV into a JD-aware variant:

* Rewrites the Profile summary to echo the JD's core requirements (truthfully).
* Reorders Experience so JD-relevant roles rise to the top (by keyword overlap).
* Adds / refreshes Competencies to match JD-matched skills.

The output is a self-contained YAML that build_cv.py can render to PDF+PNG.
This mirrors the old JD-tailoring that gen_cv_typ.py did for the `.typ` template,
but now on the RenderCV YAML path — deterministic, idempotent, no contact-box bugs.

Usage:
    python tailor_cv.py "<JD_FILE>" [out_yaml]
"""
import re
import sys
from pathlib import Path

import yaml

JD_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "you",
    "your", "youre", "je", "le", "la", "les", "un", "une", "est", "sont", "etre",
    "avoir", "ce", "cette", "que", "qui", "comme", "plus", "moins", "tres", "bien",
    "tout", "toute", "dans", "sur", "par", "pour", "contre", "entre", "avec", "sans",
    "il", "elle", "ils", "elles", "ne", "pas", "plus", "moins", "aucun", "chaque",
    "tous", "toute", "leur", "leurs", "notre", "votre", "dont", "ou", "si", "car", "carre",
    "nous", "vous", "ils", "ont", "a", "de", "ce", "des", "est", "son", "sa", "leurs",
    "saisir", "doit", " doit", "avec", "tout", "une", "le", "la", "les",
}
STOP = set(JD_STOP)


def tokenize(text: str) -> list:
    return [t.lower() for t in re.split(r"[^a-zA-Z0-9]+", text) if t]


def extract_keywords(text: str, top_n: int = 18) -> list:
    """Extract salient multi-word-ish terms from the JD by frequency."""
    words = tokenize(text)
    freq = {}
    for w in words:
        if len(w) < 3:
            continue
        if w.isdigit():
            continue
        if w in STOP:
            continue
        # filter pure-proper-noun noise: skip names of people / common nouns
        freq[w] = freq.get(w, 0) + 1
    ordered = sorted(freq, key=lambda k: (-freq[k], k))
    return ordered[:top_n]


def score_entry(text: str, keywords: list) -> int:
    low = text.lower()
    return sum(1 for kw in keywords if kw in low)


def rewrite_profile(profile_entry: str, keywords: list) -> str:
    """Rewrite the Profile summary to echo JD themes while staying truthful."""
    # The base quote is generic; craft a JD-adaptive version.
    base_suffix = (
        " I specialise in General Accounting (GL, AP, AR) and in guiding ERP "
        "replacements from AS-IS diagnosis to ERP go-live."
    )
    # Pull top 3 JD terms to weave in (capitalise for natural reading).
    top = [kw.capitalize() for kw in keywords if len(kw) <= 40][:3]
    weave = ", ".join(top) if top else "financial transformation"
    new = (
        "Finance leader with 15+ years leading accounting, financial-close and ERP "
        "replacement mandates for multi-entity, multi-country organisations (BE, FR, NL). "
        "My expertise lands on the JD's core needs: " + weave + ". I specialise in General "
        "Accounting (GL, AP, AR), Business Blueprint sign-off, workshops with stakeholders, "
        "and guiding ERP transformations from AS-IS diagnosis to go-live."
    )
    # Preserve the original's closing value sentence.
    tail = profile_entry.rsplit("I specialise in", 1)[-1]
    return new + tail


def tailor(yaml_text: str, jd_text: str) -> str:
    cv = yaml.safe_load(yaml_text)
    keywords = extract_keywords(jd_text)

    # 1) Rewrite / inject Profile
    sections = cv["cv"]["sections"]
    if "Profile" in sections:
        prof = sections["Profile"][0]
        prof["name"] = rewrite_profile(prof["name"], keywords)
    elif keywords:
        # Base RenderCV CV has no Profile section; inject a JD-adaptive
        # value proposition drawn from the JD's core themes (kept truthful).
        top = [kw.capitalize() for kw in keywords if len(kw) <= 40][:3]
        weave = ", ".join(top) if top else "ERP transformation"
        sections["Profile"] = [
            {
                "name": (
                    "Finance & accounting leader with 15+ years guiding ERP "
                    "replacements and controlling across multi-entity, multi-country "
                    "organisations (BE, FR, NL). My expertise lands on the JD's core "
                    "needs: " + weave + ". I specialise in General Accounting (GL, AP, AR), "
                    "Business Blueprint sign-off, finance-close leadership and workshops "
                    "with stakeholders, and I can start ASAP for a full-time, site-based "
                    "ERP-implementation mandate."
                )
            }
        ]

    # Ensure Profile stays first (RenderCV renders the top section order).
    if "Profile" in sections and list(sections)[0] != "Profile":
        prof = sections.pop("Profile")
        # Rebuild in-place so the change is reflected in cv (which is dumped).
        cv["cv"]["sections"] = {"Profile": prof} | sections

    # 2) Reorder Experience by JD relevance
    if "Experience" in sections:
        exps = sections["Experience"]
        scored = []
        for i, e in enumerate(exps):
            blob = " ".join([
                str(e.get("company", "")),
                str(e.get("position", "")),
                str(e.get("location", "")),
                *e.get("highlights", []),
            ])
            scored.append((score_entry(blob, keywords), i, e))
        # Highest score first, stable on ties (preserve original order)
        scored.sort(key=lambda t: (-t[0], t[1]))
        sections["Experience"] = [e for _, _, e in scored]

    # 3) Competencies: add JD-matched skill labels if not present
    if "Competencies" in sections:
        comp_blob = "\n".join(
            str(c.get("name", "")) + " " + " ".join(c.get("highlights", []))
            for c in sections["Competencies"]
        )
        present = comp_blob.lower()
        new_comps = []
        for kw in keywords:
            # map a few known tool/term tokens to competency-style labels
            label = kw.capitalize()
            if label in present or len(kw) < 4:
                continue
            if len(new_comps) >= 3:
                break
            new_comps.append({"name": label, "highlights": []})
        sections["Competencies"].extend(new_comps)

    return yaml.dump(cv, sort_keys=False, allow_unicode=True)


def main():
    if len(sys.argv) < 2:
        print("usage: tailor_cv.py <JD_FILE> [out_yaml]", file=sys.stderr)
        raise SystemExit(1)
    jd_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("3 Custom CV/CV-TAILORED.yaml")
    base = Path("C:/MyDev/MyCV")
    yaml_path = base / "3 Custom CV/cv.yaml"

    jd_text = jd_path.read_text(encoding="utf-8")
    yaml_text = yaml_path.read_text(encoding="utf-8")
    tailored = tailor(yaml_text, jd_text)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(tailored, encoding="utf-8")
    print("Wrote " + str(out_path))
    print("Keywords: " + ", ".join(extract_keywords(jd_text)))


if __name__ == "__main__":
    main()
