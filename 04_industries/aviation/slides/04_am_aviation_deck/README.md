# AM in Aviation — deck source

Source of the 53-slide claude.ai deck (Claude Slides format, 1920×1080), copied on 26 Nov 2026
(online version 1795733593-c1b2).

- `deck.json`: slide order, parts, fonts.
- `slides/<id>.html`: one `<section>` per slide; speaker notes in `<aside>`.
- `assets.json`: maps `/_blob/<id>` picture references to files in `04_industries/aviation/figures/` (empty: the deck still shows picture boxes).
- `export_deck.py`: renders `../04_am_aviation_web.pdf` (picture render, PDF only).
