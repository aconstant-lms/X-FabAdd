"""Render the claude.ai deck (this folder) to PDF and PowerPoint, as it looks online.

  python export_deck.py      ->  ../04_am_aviation.pdf   one page per slide
                                 ../04_am_aviation.pptx  one picture per slide + speaker notes

Fonts: Space Grotesk (titles) and Inter (text), as in claude.ai. Space Grotesk is read from
@fontsource (npm pack @fontsource/space-grotesk; tar xzf into /tmp/sg); Inter must be installed.
Pictures referenced as /_blob/<id> are resolved through assets.json (empty while the deck
only has picture boxes). Needs: playwright (with Chrome), Pillow, python-pptx.
"""
import json, re, io, html
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from pptx import Presentation
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = HERE.parent / "04_am_aviation"
SG = "/tmp/sg/package/files"
FONTS = "".join(f'@font-face{{font-family:"Space Grotesk";font-weight:{w};src:url(file://{SG}/space-grotesk-latin-{w}-normal.woff2)}}'
                for w in (300, 400, 500, 600, 700))
CSS = (FONTS + "body{margin:0}section{position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden}"
       "*{margin:0;box-sizing:border-box}aside{display:none}ul{list-style:disc}")

order = json.loads((HERE / "deck.json").read_text())["order"]
assets = json.loads((HERE / "assets.json").read_text())
pngs, notes = [], []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    for sid in order:
        h = (HERE / "slides" / f"{sid}.html").read_text()
        h = re.sub(r"/_blob/[0-9A-Za-z_-]+", lambda m: "file://" + str(REPO / assets.get(m.group(0), "")), h)
        a = re.search(r"<aside[^>]*>(.*?)</aside>", h, re.S)
        notes.append(html.unescape(re.sub(r"<[^>]+>", " ", a.group(1))).strip() if a else "")
        tmp = HERE / "_page.html"
        tmp.write_text(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{h}</body></html>")
        pg.goto("file://" + str(tmp)); pg.wait_for_timeout(250)
        pngs.append(Image.open(io.BytesIO(pg.screenshot(clip={"x": 0, "y": 0, "width": 1920, "height": 1080}))).convert("RGB"))
    b.close()
(HERE / "_page.html").unlink(missing_ok=True)
pngs[0].save(OUT.with_suffix(".pdf"), save_all=True, append_images=pngs[1:], resolution=144)
prs = Presentation(); prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
for im, n in zip(pngs, notes):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    buf = io.BytesIO(); im.save(buf, "PNG"); buf.seek(0)
    s.shapes.add_picture(buf, 0, 0, prs.slide_width, prs.slide_height)
    if n:
        s.notes_slide.notes_text_frame.text = n
prs.save(OUT.with_suffix(".pptx"))
print(len(pngs), "slides ->", OUT.with_suffix(".pdf").name, OUT.with_suffix(".pptx").name)
