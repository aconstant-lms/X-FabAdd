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

A chapter made of several independent decks gets **one subfolder per deck**, each with the same
`slides/`, `figures/` (+ `index.csv`), `tables/`:

```
04_industries/
  aviation/   slides/04_am_aviation.pptx                 figures/04_av_*   tables/04_av_*
  repair/     slides/04_am_repair_figures_test.pptx      figures/          tables/
  risk/       slides/04_risk_human_activities.pptx (+ _deck/ source, PDF)  figures/   tables/
  space/      slides/04_am_space.pptx                    figures/04_sp_*   tables/
```

A new topic in such a chapter = a new subfolder (`04_industries/medical/…`). File names still
start with the chapter number. The toolkit handles both layouts; the footer always shows the
chapter (“04 Industries”).

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
| Start a new deck in the course style | `python tools/xfab.py new 05_economics/slides/05_economics.pptx --title "…"` |
| Apply the course style (fonts, colours, footer) to every deck | `python tools/xfab.py restyle --all` |
| Rebuild the template after changing the style | `python tools/xfab.py template` |
| List missing and unused figures across all decks | `python tools/xfab.py status` |
| Build a catalogue of every figure (picture, full path, caption, decks and slides using it, source, credit, licence) | `python tools/catalogue.py` → `figures_catalogue.pptx` (not committed) |

## Course style: one place

The style lives in **`templates/style.json`**: footer text and position, fonts, theme colours.
`templates/exed_am_template.pptx` is the PowerPoint template built from it (layouts `DEFAULT`,
`TITLE_ONLY`, `OVERVIEW`, `SECTION`).

- Fonts: **Space Grotesk** for titles and large numbers, **Inter** for body text (theme fonts).
  Both are free (SIL OFL): install the `static` TTFs from fonts.google.com on every machine you
  present or export from, and tick *PowerPoint › Preferences › Save › Embed fonts in the file*.
  Characters Space Grotesk lacks (Greek, ≈, superscripts, arrows) stay in Inter.
- Fit: after a font change, boxes whose text wraps onto too many lines are shrunk (never below 80 %
  of the original size, kept in the shape name `… [fit 3200]`); `restyle` lists them, and those
  still too long must be shortened by hand. `templates/font-metrics/` holds latin-only copies used
  for measuring only — do not install them.
- Footer: *EXED Polytechnique - Additive Manufacturing - 04 Industries by Andrei Constantinescu 2027*,
  8 pt grey, bottom left, **in the slide master** (one text box, not one per slide); the chapter label
  comes from the folder. Hidden on a cover slide (slide 1 with layout `SECTION`).
- Dark section slides: dark text is turned into the light text colour.

To change the style: edit `style.json`, then `python tools/xfab.py restyle --all` and
`python tools/xfab.py template`. Never style slides one by one.

claude.ai Slides decks use the **EXED Additive Manufacturing** design system (Space Grotesk / Inter,
same colours and footer). The PowerPoint deck in this repository is the reference; a claude.ai deck is a draft or
a presentation copy.

Every command except `--check` also refreshes the `slides` column of the `index.csv` files.

Presentations kept outside the repository (for example a claude.ai Slides deck) can be listed per chapter or topic in
`…/figures/external_usage.csv` (columns `file,presentation,slides`); the catalogue shows them next to
the repository decks.

## Typical cycle

1. Put or update pictures in `NN_chapter/figures/` (or `NN_chapter/<topic>/figures/`).
2. Add or edit slides (in PowerPoint, or with `add-slide`). When adding a picture by hand
   in PowerPoint, type its repo path in the alt text.
3. Before teaching: `python tools/xfab.py sync DECK`, then `status`.
4. Export the PDF for students; present from the PPTX (it keeps the speaker notes).
5. Commit the deck, the figures and the updated `index.csv` together.
