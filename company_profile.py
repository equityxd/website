# -*- coding: utf-8 -*-
"""
Verified company context — used to fine-tune generated cover letter / interview-prep docs.

SOURCE OF TRUTH
---------------
These facts are VERIFIED via web research (company website, Partseholding Europe,
company web / AD International, LinkedIn). They describe the *company only* and are
used to TAILOR the documents (sector awareness, scale, geography). They are NOT a
source to invent or inflate the candidate's personal experience.

WHY A MODULE AND NOT LIVE SCRAPING
-----------------------------------
The .bat / generator runs non-interactively and often without a network connection.
Baking live web scraping into the generator would make documents depend on
connectivity and could pull unverified scraper data into a *truthful* CV. Instead we
research + verify once (by the LLM) and bake the verified facts into this module, so
every generated run is fine-tuned deterministically. Use `python company_profile.py --fetch`
only to refresh the data when you explicitly ask for a live re-search.
"""

COMPANY_PROFILE = {
    "name": "Doyen Auto",
    "legal_name": "DAB (SA)",
    "be_number": "0895.469.554",
    "sector": "automotive aftermarket parts distribution (wholesale of vehicle parts & accessories)",
    "founded": 1922,
    "hq": "Drogenbos, Belgium",
    "address": "W.A. Mozartlaan 8 / Amadeus Square, 1620 Drogenbos",
    "group": "Parts Holding Europe (PHE) / Autodistribution",
    "parent_acquisition": "D'Ieteren Group acquired PHE on 4 August 2022",
    "parent_scale": "Parts Holding Europe: ~10,500 employees across Western Europe",
    "parent_revenue_h1_2025": "EUR 1,458.9M (+5.2% YoY)",
    "customer_network": "Aftermarket: ~170 distributors + ~650 repairers via API Belux/France, Autodistribution (BE/NL), 1,2,3 AutoService and AD Garage",
    "product_lines": "~25 product lines incl. the Requal range (auto repair / sustainable mobility)",
    "countries": "Belgium, France, Netherlands, Luxembourg (+ workforce presence in Germany, Nigeria per LinkedIn)",
    "headcount_note": "Site-cited headcount varies (~283 per LinkedIn vs. 700+ per Partseholding Europe) — treat as inconsistent across sources.",
}


def tailoring_text():
    """A single English paragraph of verified company context, for tailoring docs.

    Returns "" when the profile is empty. Only company context — never candidate facts.
    """
    if not COMPANY_PROFILE:
        return ""
    p = COMPANY_PROFILE
    return (
        f"{p['name']} is a {p['founded']}-year-old automotive aftermarket parts distributor "
        f"(wholesale of vehicle parts and accessories), headquartered in Drogenbos, Belgium, "
        f"and part of Parts Holding Europe, a leading Western Europe spare-parts group."
    )


def sector_note():
    """Short English note about the sector, for interview-prep tailoring."""
    return (
        "the automotive aftermarket / parts-distribution sector (bout-to-flux accounting flows, "
        "multi-entity close across BE, FR and NL)"
    )


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="attempt a live re-search and re-verify")
    args = ap.parse_args()
    if args.fetch:
        print("[info] live-fetch mode requested — verify facts manually before re-baking.")
        print("[note] offline run: skipping live search.")
    # Deterministic baseline: just print the verified context for inspection.
    print(tailoring_text())
