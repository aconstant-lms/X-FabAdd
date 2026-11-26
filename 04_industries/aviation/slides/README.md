# Chapter 04 · aviation slides: which file is what

| File | What it is |
|---|---|
| `04_am_aviation.pdf` | **Current** deck "AM in Aviation — Applications" (53 slides, 9 parts), rendered exactly as the claude.ai deck: Space Grotesk / Inter, maps, picture boxes, course footer. Opens directly on GitHub. |
| `04_am_aviation.pptx` | Same deck for presenting: one picture per slide, speaker notes kept. Text is not editable here. |
| `04_am_aviation_editable.pptx` | Editable PowerPoint version (8 Nov 2026, Cambria, simpler layout): text, tables and picture placeholders whose alt text is the repo path (`xfab.py sync` fills them from `../figures/`). |
| `04_am_aviation_deck/` | Source of the claude.ai deck: `deck.json`, `slides/<id>.html`, `assets.json`, `export_deck.py`. |

Editable online deck: https://claude.ai/artifact/7anGcjnyWJtXAgcpMGCcPK

To refresh the PDF and PowerPoint after editing online: copy the deck's `project/slides/*.html` and
`deck.json` into `04_am_aviation_deck/`, then

```bash
python 04_am_aviation_deck/export_deck.py
```

Pictures: none yet; the 58 pictures to add are listed in `../figures/index.csv` with a suggested source.
