#!/usr/bin/env python3
"""Build the TikZ schematics of the course.

Every  NN_chapter/figures/*.tex  is a standalone TikZ picture using
tools/tikz/xfab-tikz.sty. This script compiles it with XeLaTeX and writes,
next to the source:
    name.pdf   vector, for LaTeX documents and printing
    name.png   300 dpi (or --dpi), the file used in the decks

    python tools/build_figures.py                 # all figures of all chapters
    python tools/build_figures.py 02_technologies/figures/02_din8580_main_groups.tex
    python tools/build_figures.py --dpi 450

Then run  python tools/xfab.py sync DECK  to refresh the slides.
Needs: xelatex (TeX Live with pgf, standalone, fontspec), pdftoppm (poppler),
       the Inter font (full version, fonts.google.com or fonts-inter).
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STYLE_DIR = REPO / "tools" / "tikz"


def build(tex: Path, dpi: int) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, TEXINPUTS=f"{STYLE_DIR}{os.pathsep}{tex.parent}{os.pathsep}")
        r = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
             f"-output-directory={tmp}", tex.name],
            cwd=tex.parent, env=env, capture_output=True, text=True)
        pdf = Path(tmp) / (tex.stem + ".pdf")
        if r.returncode != 0 or not pdf.exists():
            log = (Path(tmp) / (tex.stem + ".log"))
            tail = log.read_text(errors="replace").splitlines()[-25:] if log.exists() else r.stdout.splitlines()[-25:]
            print(f"FAILED  {tex.relative_to(REPO)}\n  " + "\n  ".join(tail))
            return False
        shutil.copy(pdf, tex.with_suffix(".pdf"))
        subprocess.run(["pdftoppm", "-png", "-singlefile", "-r", str(dpi),
                        str(pdf), str(tex.with_suffix(""))], check=True)
    print(f"ok      {tex.relative_to(REPO)}  -> .pdf, .png ({dpi} dpi)")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="figure .tex files (default: all chapters)")
    ap.add_argument("--dpi", type=int, default=300)
    a = ap.parse_args(argv)
    files = [Path(f).resolve() for f in a.files] or sorted(REPO.glob("[0-9][0-9]_*/figures/*.tex"))
    ok = all([build(f, a.dpi) for f in files])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
