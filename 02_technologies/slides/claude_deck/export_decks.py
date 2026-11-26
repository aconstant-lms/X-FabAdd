"""Export the chapter-02 claude.ai decks to PDF and PowerPoint for the repository.

Run after `python gen_technology_decks.py build`. Each slide (1920 x 1080 HTML) is rendered with
headless Chrome (Playwright) from the local figures listed in build/manifest.json, then

  ../02_technology_<deck>.pdf    one page per slide (GitHub shows it in the browser)
  ../02_technology_<deck>.pptx   one picture per slide, speaker notes from the slide's <aside>

The PowerPoint is a faithful copy for viewing and teaching; text is not editable (edit in claude.ai,
then export again). Pictures not cleared for the public repository are replaced by a grey box.

  python export_decks.py [--full]     # --full keeps the polymer debrief (exercise answers): local use only
"""
import json, re, sys, io, html
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
OUT = HERE.parent
FULL = "--full" in sys.argv
NOT_PUBLIC = {"02_k02_ampower_polymer_landscape.jpg": "AMPOWER polymer landscape: AMPOWER Insights Vol. 11 (2022), p. 9 — not reproduced here"}
# polymer debrief = exercise answers: left out of the public export
ANSWERS = ["part-debrief", "poly-readiness", "poly-status-2026", "vpp-volumetric", "vpp-volumetric-two", "vpp-prices",
           "vpp-makers", "poly-market", "db-patterns", "db-takeuchi", "db-transfer"]
SG = "/tmp/sg/package/files"

FONTS = "".join(f'@font-face{{font-family:"Space Grotesk";font-weight:{w};src:url(file://{SG}/space-grotesk-latin-{w}-normal.woff2)}}'
                for w in (300, 400, 500, 600, 700))
CSS = (FONTS + "body{margin:0}section{position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden}"
       "*{margin:0;box-sizing:border-box}aside{display:none}ul{list-style:disc}")


def placeholder(text):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900"><rect width="1600" height="900" fill="#e4e1da"/>'
           f'<text x="800" y="450" font-family="Inter" font-size="40" text-anchor="middle" fill="#566170">{html.escape(text)}</text></svg>')
    p = BUILD / ("ph_" + str(abs(hash(text))) + ".svg")
    p.write_text(svg)
    return "file://" + str(p)


def export(deck, pg):
    proj = BUILD / deck / "project"
    order = json.loads((proj / "deck.json").read_text())["order"]
    if deck == "technology_polymer" and not FULL:
        order = [s for s in order if s not in ANSWERS]
    blobs = json.loads((BUILD / "manifest.json").read_text())[deck]
    pngs, notes = [], []
    for sid in order:
        h = (proj / "slides" / f"{sid}.html").read_text()
        def sub(m):
            f = Path(blobs.get(m.group(1), ""))
            if f.name in NOT_PUBLIC:
                return placeholder(NOT_PUBLIC[f.name])
            return "file://" + str(f)
        h = re.sub(r"/_blob/([0-9A-Za-z_-]+)", sub, h)
        a = re.search(r"<aside[^>]*>(.*?)</aside>", h, re.S)
        notes.append(html.unescape(re.sub(r"<[^>]+>", " ", a.group(1))).strip() if a else "")
        tmp = BUILD / "_page.html"
        tmp.write_text(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{h}</body></html>")
        pg.goto("file://" + str(tmp)); pg.wait_for_timeout(250)
        pngs.append(Image.open(io.BytesIO(pg.screenshot(clip={"x": 0, "y": 0, "width": 1920, "height": 1080}))).convert("RGB"))
    name = deck.replace("technology_", "02_technology_") + ("_full" if FULL and deck == "technology_polymer" else "")
    pngs[0].save(OUT / f"{name}.pdf", save_all=True, append_images=pngs[1:], resolution=144)
    prs = Presentation(); prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    for im, n in zip(pngs, notes):
        s = prs.slides.add_slide(blank)
        b = io.BytesIO(); im.save(b, "PNG"); b.seek(0)
        s.shapes.add_picture(b, 0, 0, prs.slide_width, prs.slide_height)
        if n:
            s.notes_slide.notes_text_frame.text = n
    prs.save(OUT / f"{name}.pptx")
    print(name, len(pngs), "slides")


with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    for d in ("technology_polymer", "technology_metal", "technology_unused"):
        export(d, pg)
    b.close()
