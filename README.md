# X-FabAdd — Additive Manufacturing course material

EXED Polytechnique — Additive Manufacturing, by Andrei Constantinescu.
Slides, figures and tables, organised by chapter.

| Chapter | Folder |
|---|---|
| 1. Introduction | `01_introduction/` |
| 2. Technologies | `02_technologies/` |
| 3. Materials in design | `03_materials_in_design/` |
| 4. Industries | `04_industries/` |
| 5. Economics | `05_economics/` |

Each chapter folder contains:

- `slides/` — the PowerPoint deck(s) of the chapter (`.pptx`, the master copy; PDFs are exports)
- `figures/` — **every picture used in the slides; this folder is the source of truth**
- `figures/index.csv` — one line per figure: file, slides using it, caption, source, credit, licence, notes
- `tables/` — tabular data (CSV, XLSX, …)

## How figures work

Every picture in a deck carries its repository path in its **alt text**
(PowerPoint: right-click the picture › *View Alt Text*), for instance

```
02_technologies/figures/02_lpbf_schematic.png
```

That path is the link between the slide and the file. Improve the file in
`figures/`, run `sync`, and every slide using it — in any chapter — is updated,
with its position kept and its proportions respected.

### Naming

- `NN_short_name.png`, where `NN` is the chapter number: `02_lpbf_schematic.png`,
  `04_ge_fuel_nozzle.jpg`. Lower case, underscores, no spaces or accents.
- Pictures extracted from an old deck start as `NN_sSS_KK.ext`
  (chapter, slide, rank). Rename them with `rename` (never by hand, or the slides lose the link).
- Keep editable sources next to the image with the same name
  (`02_lpbf_schematic.svg`, `.py`, `.ai`); the deck uses the PNG/JPG.
- Fill in `source`, `credit` and `license` in `index.csv` for anything not drawn by us.

## The toolkit: `tools/xfab.py`

```bash
pip install -r tools/requirements.txt
```

| Task | Command |
|---|---|
| Bring an existing deck under the system (extract pictures into `figures/`, set alt texts) | `python tools/xfab.py extract 02_technologies/slides/02_technologies.pptx` |
| Add a slide with a figure (a grey placeholder is inserted if the figure does not exist yet) | `python tools/xfab.py add-slide DECK --title "LPBF" --figure 02_technologies/figures/02_lpbf_schematic.png --notes "…" --caption "…" [--after 7]` |
| Refresh the slides from `figures/` (new versions, placeholders filled) | `python tools/xfab.py sync DECK` |
| Just check, change nothing (exit code 1 if a figure is missing) | `python tools/xfab.py sync DECK --check` |
| Rename a figure and relink every deck | `python tools/xfab.py rename 02_technologies/figures/02_s05_01.png 02_lpbf_schematic.png` |
| Put the course footer on every slide | `python tools/xfab.py footer DECK [--skip-first]` |
| List missing and unused figures across all decks | `python tools/xfab.py status` |
| Build a catalogue of every figure (picture, full path, caption, decks and slides using it, source, credit, licence) | `python tools/catalogue.py` → `figures_catalogue.pptx` (not committed) |

The footer reads, in 8 pt grey, bottom left:
*EXED Polytechnique - Additive Manufacturing - 02 Technologies by Andrei Constantinescu 2027*
(the chapter label comes from the folder name; `--chapter`, `--year`, `--size`, `--template` override it).
New slides made with `add-slide` get the footer automatically.

Every command except `--check` also refreshes the `slides` column of the `index.csv` files.

Presentations kept outside the repository (for example a claude.ai Slides deck) can be listed per chapter in
`NN_chapter/figures/external_usage.csv` (columns `file,presentation,slides`); the catalogue shows them next to
the repository decks.

## Typical cycle

1. Put or update pictures in `NN_chapter/figures/`.
2. Add or edit slides (in PowerPoint, or with `add-slide`). When adding a picture by hand
   in PowerPoint, type its repo path in the alt text.
3. Before teaching: `python tools/xfab.py sync DECK`, then `status`.
4. Export the PDF for students; present from the PPTX (it keeps the speaker notes).
5. Commit the deck, the figures and the updated `index.csv` together.
