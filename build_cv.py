#!/usr/bin/env python3
"""Build a RenderCV YAML CV to PDF + PNG previews.

This replaces the old JD-tailored `.typ` pipeline (gen_cv_typ.py). RenderCV renders a
fixed, reproducible CV from YAML — it removes the `.typ`/octique contact-box spacing bugs
that plagued the custom template, and makes regeneration deterministic.

Usage:
    python build_cv.py            # render the canonical cv.yaml
    python build_cv.py --pages    # also emit page-count metadata

The generated PDF and previews are written to `3 Custom CV/rendercv_output/`
(the RenderCV default folder), then the PDF is copied to the standard
`3 Custom CV/CV-20260912-0005_CV1.pdf` name for downstream tooling.

Requires `rendercv[full]`, the Typst CLI, and its fonts (all installable / present).
"""
import argparse
import os
import shutil
import subprocess
from pathlib import Path

RENDERCV = r"C:\Users\ernes\AppData\Roaming\Python\Python314\Scripts\rendercv.exe"
TYPST = r"C:\Users\ernes\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst"

BASE = Path("C:/MyDev/MyCV")
DEFAULT_YAML = BASE / "3 Custom CV/cv.yaml"
OUT_DIR = BASE / "3 Custom CV/rendercv_output"


def _default_pdf_name(yaml_path: Path) -> str:
    """Derive the standard PDF name from the input YAML's basename.

    e.g. "cv.yaml" -> "CV-20260912-0005_CV1.pdf", "CV-TAILORED.yaml" ->
    "CV-TAILORED_CV1.pdf". Falls back to the canonical name.
    """
    stem = yaml_path.stem
    if stem == "cv":
        return "CV-20260912-0005_CV1.pdf"
    return f"{stem}_CV1.pdf"


def find_typst():
    """Return the Typst binary path (search a few likely locations)."""
    if Path(TYPST).exists():
        return TYPST
    for cand in (
        r"C:\Users\ernes\AppData\Local\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst",
        r"C:\Users\ernes\bin\typst",
    ):
        if Path(cand).exists():
            return cand
    return TYPST


def render():
    typst = find_typst()
    cmd = [
        str(RENDERCV),
        "render",
        str(YAML_IN),
        "--typst-path",
        typst,
        "-q",
    ]
    print("[build] Running: " + " ".join(cmd))
    env = dict(os.environ)
    env["PATH"] = Path(typst).parent.__str__() + os.pathsep + env["PATH"]
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        print("RenderCV FAILED:\n" + res.stdout + res.stderr)
        raise SystemExit(1)
    print(res.stdout)


def copy_standard_pdf():
    """Copy the RenderCV-generated PDF to the standard output name."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    candidates = list(OUT_DIR.glob("*.pdf"))
    if not candidates:
        raise SystemExit("No PDF found in " + str(OUT_DIR))
    pdf = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    shutil.copy2(pdf, STANDARD_PDF)
    print("Copied " + pdf.name + " -> " + STANDARD_PDF.name)


def main():
    parser = argparse.ArgumentParser(description="Build RenderCV YAML to PDF+PNG.")
    parser.add_argument("--pages", action="store_true", help="print page count metadata")
    parser.add_argument("--yaml", help="path to a YAML file (default: base cv.yaml)")
    args = parser.parse_args()

    global YAML_IN, STANDARD_PDF
    YAML_IN = BASE / args.yaml if args.yaml else DEFAULT_YAML
    STANDARD_PDF = BASE / "3 Custom CV" / _default_pdf_name(YAML_IN)

    render()
    copy_standard_pdf()

    if args.pages:
        try:
            import pymupdf
            doc = pymupdf.open(str(STANDARD_PDF))
            print("pages:", len(doc))
        except Exception as e:  # noqa: BLE001
            print("page-count skip:", e)


if __name__ == "__main__":
    main()
