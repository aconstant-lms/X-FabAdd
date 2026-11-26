# Chapter 04 · aviation slides: which file is what

| File | What it is |
|---|---|
| `04_am_aviation.pptx` | **Master copy**, editable PowerPoint (8 Nov 2026, course fonts, simpler layout): text, tables and picture placeholders whose alt text is the repo path (`xfab.py sync` fills them from `../figures/`). |
| `04_am_aviation_web.pdf` | Picture render of the newer claude.ai deck "AM in Aviation — Applications" (53 slides, 9 parts, 26 Nov 2026): Space Grotesk / Inter, maps, picture boxes, course footer. Read-only; opens directly on GitHub. |
| `04_am_aviation_deck/` | Source of the claude.ai deck: `deck.json`, `slides/<id>.html`, `assets.json`, `export_deck.py`. |

Online deck (owner only): https://claude.ai/artifact/7anGcjnyWJtXAgcpMGCcPK

The claude.ai deck is ahead of the editable PowerPoint (parts 4–9 added after 8 Nov). Bringing
`04_am_aviation.pptx` up to date is an open task; until then use the PDF for the newer slides.

To refresh the PDF after editing online: copy the deck's `project/slides/*.html` and `deck.json`
into `04_am_aviation_deck/`, then

```bash
python 04_am_aviation_deck/export_deck.py
```

Pictures: none in the repo yet. The online deck shows GE Aerospace / Safran pictures taken from the
course introduction PDF and the GE capability slides; their licence is still to check, so they are
listed in `../figures/index.csv` (notes column) and stay as boxes here.
