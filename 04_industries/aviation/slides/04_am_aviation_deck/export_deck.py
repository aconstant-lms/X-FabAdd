"""Render the claude.ai deck (this folder) to PDF, as it looks online.

  python export_deck.py      ->  ../04_am_aviation_web.pdf   one page per slide

Course rule: picture renders are PDF only. The editable PowerPoint is ../04_am_aviation.pptx.

Fonts: Space Grotesk (titles) and Inter (text), as in claude.ai. Space Grotesk is read from
@fontsource (npm pack @fontsource/space-grotesk; tar xzf into /tmp/sg); Inter must be installed.
Pictures referenced as /_blob/<id> are resolved through assets.json (empty while the deck
only has picture boxes). Needs: playwright (with Chrome), Pillow.
"""
import json, re, io, html
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = HERE.parent / "04_am_aviation_web"
SG = "/tmp/sg/package/files"
FONTS = "".join(f'@font-face{{font-family:"Space Grotesk";font-weight:{w};src:url(file://{SG}/space-grotesk-latin-{w}-normal.woff2)}}'
                for w in (300, 400, 500, 600, 700))
CSS = (FONTS + "body{margin:0}section{position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden}"
       "*{margin:0;box-sizing:border-box}aside{display:none}ul{list-style:disc}")

order = json.loads((HERE / "deck.json").read_text())["order"]
assets = json.loads((HERE / "assets.json").read_text())
pngs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    for sid in order:
        h = (HERE / "slides" / f"{sid}.html").read_text()
        h = re.sub(r"/_blob/[0-9A-Za-z_-]+", lambda m: "file://" + str(REPO / assets.get(m.group(0), "")), h)
        tmp = HERE / "_page.html"
        tmp.write_text(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{h}</body></html>")
        pg.goto("file://" + str(tmp)); pg.wait_for_timeout(250)
        pngs.append(Image.open(io.BytesIO(pg.screenshot(clip={"x": 0, "y": 0, "width": 1920, "height": 1080}))).convert("RGB"))
    b.close()
(HERE / "_page.html").unlink(missing_ok=True)
pngs[0].save(OUT.with_suffix(".pdf"), save_all=True, append_images=pngs[1:], resolution=144)
print(len(pngs), "slides ->", OUT.with_suffix(".pdf").name)
