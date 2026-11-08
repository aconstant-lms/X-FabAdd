#!/usr/bin/env python3
"""Build figures_catalogue.pptx: one slide per figure of every chapter.

Each slide shows the picture (or a grey box when the file is still missing),
its full repository path, caption, every deck and slide that uses it,
source, credit, licence and notes.

Usage comes from two places:
  * the decks of the repository (alt-text links, as in xfab.py);
  * NN_chapter/figures/external_usage.csv for presentations kept outside
    the repository (columns: file, presentation, slides).

    python tools/catalogue.py            # writes figures_catalogue.pptx at the repo root
    python tools/catalogue.py --out other.pptx
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Emu, Inches, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import xfab  # noqa: E402  (shared helpers: REPO, scan_usage, read_index, placeholder_png, image_size)

FONT = "Cambria"
GREY = RGBColor(0x59, 0x59, 0x59)
DARK = RGBColor(0x1B, 0x24, 0x33)
ACCENT = RGBColor(0xA8, 0x48, 0x0F)
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff"}


def text_box(slide, x, y, w, h, paragraphs, size=12):
    """paragraphs: list of (text, bold, colour) or lists of such runs."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for para in paragraphs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        runs = para if isinstance(para, list) else [para]
        for text, bold, colour in runs:
            r = p.add_run()
            r.text = text
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = colour
        p.space_after = Pt(4)
    return tb


def external_usage() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for g in xfab.figure_groups():
        f = xfab.REPO / g / "figures" / "external_usage.csv"
        if not f.exists():
            continue
        chapter = g
        for row in csv.DictReader(f.open(encoding="utf-8")):
            path = f"{chapter}/figures/{row['file']}"
            out.setdefault(path, []).append(f"{row['presentation']}: slide {row['slides']}")
    return out


def repo_usage() -> dict[str, list[str]]:
    by_deck: dict[str, dict[str, list[str]]] = {}
    for fig, places in xfab.scan_usage().items():
        for place in places:  # "deck.pptx:12"
            deck, _, num = place.rpartition(":")
            by_deck.setdefault(fig, {}).setdefault(deck, []).append(num)
    return {fig: [f"{deck}: slide{'s' if len(n) > 1 else ''} {', '.join(sorted(set(n), key=int))}"
                  for deck, n in decks.items()] for fig, decks in by_deck.items()}


def collect():
    """All figures: files present in figures/ plus rows of index.csv (missing files too)."""
    usage_repo, usage_ext = repo_usage(), external_usage()
    figs = []
    for chapter in xfab.figure_groups():
        chap_dir = xfab.REPO / chapter
        index = xfab.read_index(chapter)
        names = set(index) | {f.name for f in (chap_dir / "figures").iterdir() if f.is_file()}
        for name in sorted(names):
            if Path(name).suffix.lower() not in IMAGE_EXT:
                continue  # sources (.py, .svg …) are listed in index.csv, not shown here
            path = f"{chapter}/figures/{name}"
            figs.append({
                "chapter": chapter, "name": name, "path": path,
                "file": chap_dir / "figures" / name,
                "row": index.get(name, {}),
                "used": usage_repo.get(path, []) + usage_ext.get(path, []),
            })
    return figs


def footer(slide, prs, text):
    text_box(slide, Emu(int(prs.slide_width * 0.02)), prs.slide_height - Inches(0.36),
             Emu(int(prs.slide_width * 0.7)), Inches(0.3), [(text, False, RGBColor(0x7F, 0x7F, 0x7F))], size=8)


def build(out: Path, year: str):
    figs = collect()
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    foot = f"EXED Polytechnique - Additive Manufacturing - Figures catalogue by Andrei Constantinescu {year}"

    # overview slide
    s = prs.slides.add_slide(blank)
    present = sum(1 for f in figs if f["file"].is_file())
    lines = [[("Figures catalogue", True, DARK)],
             [(f"{len(figs)} figures, {present} present, {len(figs) - present} still missing", False, GREY)], [("", False, GREY)]]
    for chap in sorted({f["chapter"] for f in figs}):
        cf = [f for f in figs if f["chapter"] == chap]
        miss = sum(1 for f in cf if not f["file"].is_file())
        lines.append([(xfab.chapter_label(chap), True, DARK), (f"   {len(cf)} figures, {miss} missing", False, GREY)])
    lines += [[("", False, GREY)],
              [("One slide per figure: picture, repository path, caption, presentations and slides using it, "
                "source, credit, licence. Regenerate with: python tools/catalogue.py", False, GREY)]]
    text_box(s, Inches(0.8), Inches(1.2), Inches(11.7), Inches(5.5), lines, size=18)
    footer(s, prs, foot)

    box_x, box_y, box_w, box_h = Inches(0.5), Inches(1.05), Inches(7.3), Inches(5.6)
    for f in figs:
        s = prs.slides.add_slide(blank)
        text_box(s, Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.6),
                 [[(f["path"], True, DARK)]], size=20)
        if f["file"].is_file():
            data = f["file"].read_bytes()
            wh = xfab.image_size(data)
            x, y, w, h = xfab.fit_box((box_x, box_y, box_w, box_h), wh) if wh else (box_x, box_y, box_w, box_h)
            pic = s.shapes.add_picture(str(f["file"]), x, y, w, h)
            xfab.set_alt(pic, f["path"])
        else:
            frame = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, box_x, box_y, box_w, box_h)
            frame.fill.solid(); frame.fill.fore_color.rgb = RGBColor(0xE1, 0xE1, 0xE1)
            frame.line.color.rgb = RGBColor(0xB0, 0xB0, 0xB0)
            text_box(s, box_x, box_y + box_h / 2 - Inches(0.4), box_w, Inches(0.8),
                     [[("MISSING - file not in figures/ yet", True, ACCENT)]], size=16).text_frame.paragraphs[0].alignment = 2
        r = f["row"]
        used = f["used"] or ["not used in any presentation"]
        right = [[("Caption", True, ACCENT)], [(r.get("caption") or "-", False, DARK)],
                 [("Used in", True, ACCENT)]] + [[("• " + u, False, DARK)] for u in used] + [
                 [("Source", True, ACCENT)], [(r.get("source") or "-", False, DARK)],
                 [("Credit", True, ACCENT)], [(r.get("credit") or "-", False, DARK)],
                 [("Licence", True, ACCENT)], [(r.get("license") or "-", False, DARK)]]
        if r.get("notes"):
            right += [[("Notes", True, ACCENT)], [(r["notes"], False, GREY)]]
        text_box(s, Inches(8.1), Inches(1.05), Inches(4.8), Inches(5.9), right, size=11)
        footer(s, prs, foot)
    prs.save(out)
    print(f"{out.name}: {len(figs)} figure slides + overview ({present} present, {len(figs) - present} missing)")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(xfab.REPO / "figures_catalogue.pptx"))
    ap.add_argument("--year", default="2027")
    a = ap.parse_args(argv)
    build(Path(a.out), a.year)


if __name__ == "__main__":
    main()
