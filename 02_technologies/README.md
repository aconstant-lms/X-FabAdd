# 02 Technologies — chapter plan

A growing path, one idea per slide. Figures follow M. F. Ashby's drawing style: plain
cross-sections, pale flat fills, thin dark outlines, a few labels with leader lines, no title
inside the picture (titles go on the slide, with French and German names where useful).
Slides use the course style (Cambria, EXED footer, picture alt text = repository path).

Figure names carry the part: `02_a` structure, `02_b` kitchen, `02_c` classical machines, `02_d` voxels and addressing, `02_e` paths, clocks, interfaces, `02_f` AM processes.

## Colour convention (`02_a00_colour_convention.png`)

| Meaning | Colour |
|---|---|
| initial material (liquid, paste, powder, wire, sheet, gas) | kitchen: pale yellow · industry: orange |
| final material, the part | kitchen: blue · industry: slate |
| mould or die (carries the shape) | grey hatching |
| other tools | light grey |
| carrier fluid (water, electrolyte, gas) | pale cyan |
| force, motion | dark arrow |
| heat | orange wavy arrow |
| radiation (laser, UV, electrons) | magenta beam |
| electricity | blue wire |
| chemistry (binder, reaction) | green |

Defined once in `tools/tikz/xfab-tikz.sty`.

## The decks

- **claude.ai Slides: "AM technologies"**, https://claude.ai/artifact/4bKyVcrndt1NUbHWZMYcqk (45 slides, course style: Caladea, navy part slides, EXED footer, picture boxes labelled with the repo path; slide numbers in `figures/external_usage.csv`). Part 1 *Traditional technologies* shows six cases, one per DIN 8580 group, each titled by its operation with the kitchen steps above and the industrial twin's steps below (`02_b…` + `02_g…`).
- **`slides/02_technologies.pptx`** (first version, 52 slides) — to be regenerated from the claude.ai structure once the story is reworked.

### First PowerPoint version

Built by `slides/build_02_technologies.py` from the chapter 04 template (same layouts, theme,
Cambria titles, cards and tables), then `python tools/xfab.py footer … --skip-first`.
Labels in English; French and German keywords in the speaker notes.

| Part | Content | Figures |
|---|---|---|
| 0 | Materials and traditional technologies: materials through the ages (Ashby), the six DIN 8580 groups — shape created / changed / material changed — the kitchen series with industrial twins, Ashby's process taxonomy, the classical machines (casting, injection moulding, forging, milling, welding, thermal spraying, heat-treatment temperature scales, press + sinter), where the geometry is stored | `02_a…`, `02_b…`, `02_c…` |
| 1 | AM as layer-wise primary shaping: file → layer → voxel; seven DIN 8580 starting states and their conventional twins; four material paths; each AM process next to its twin (VPP–resin casting, MJT, MEX–injection moulding, paste–slip/concrete casting, BJT–powder metallurgy with its internal steps, PBF and DED–welding/casting, SHL–lamination, cold spray–thermal spraying, laser CVD–CVD, electrochemical AM–electroforming) | `02_d01`, `02_e01`, `02_f…` |
| 2 | Morphological box: material state × feedstock form × agent × addressing (point, line, area, volume) | `02_d02` + table |
| 3 | Clocks: setting time vs time between layers | `02_e02` |
| 4 | The layer interface: what joins layer n to n − 1 | `02_e03` |
| 5 | From physics to potentials (Gebhardt §2.6) → design rules; machines and prices; references | tables |

Missing picture: `figures/02_ashby_materials_evolution.png` (slide 5 shows a placeholder;
permission to check before adding it to this public repository; then `xfab.py sync`).

Kitchen examples carry through the chapter (chocolate, jelly, glue gun, icing, sandcastle and
sugar cube, papier-mâché, frost on a window, electroformed leaf; CandyFab sugar sintering).

## Tables (`tables/`)

- `02_din8580_main_groups.csv` — six groups, DE/EN/FR, cohesion, link with AM
- `02_primary_shaping_states.csv` — seven starting states, DE/EN/FR, conventional and AM processes
- `02_machines_lpbf_metal.csv`, `02_machines_binder_jetting_metal.csv`, `02_machines_microprinting.csv`

## References

- DIN 8580, *Fertigungsverfahren — Begriffe, Einteilung*. Beuth.
- M. F. Ashby, *Materials Selection in Mechanical Design*, 5th ed., Butterworth-Heinemann, 2016,
  ch. 6–7 (classifying processes, process selection).
- M. F. Ashby, H. Shercliff, D. Cebon, *Materials: Engineering, Science, Processing and Design*,
  3rd ed., Butterworth-Heinemann, 2013, ch. 18–19.
- M. F. Ashby, K. Johnson, *Materials and Design*, 3rd ed., Butterworth-Heinemann, 2014, ch. 5.
- A. Gebhardt, J.-S. Hötter, *Additive Manufacturing: 3D Printing for Prototyping and
  Manufacturing*, Hanser, 2016, ch. 2.
- I. Gibson, D. Rosen, B. Stucker, M. Khorasani, *Additive Manufacturing Technologies*, 3rd ed.,
  Springer, 2021.
- J.-P. Kruth, *Material incress manufacturing by rapid prototyping techniques*, CIRP Annals 40
  (1991); J.-P. Kruth, M. C. Leu, T. Nakagawa, *Progress in additive manufacturing and rapid
  prototyping*, CIRP Annals 47 (1998).
- J.-P. Kruth et al., *Binding mechanisms in selective laser sintering and selective laser
  melting*, Rapid Prototyping Journal 11 (2005).
- N. Tuncer, A. Bose, *Solid-state metal additive manufacturing: a review*, JOM 72 (2020).
- ISO/ASTM 52900:2021, *Additive manufacturing — General principles — Fundamentals and vocabulary*.

## Building the figures

```bash
python tools/build_figures.py          # every NN_*/figures/*.tex -> .pdf + .png (300 dpi)
```
Needs XeLaTeX (TeX Live / MacTeX), poppler (`pdftoppm`) and the Caladea font.
`figures/drafts/` holds the first, denser schematics, kept as material for steps (iii) and (vi);
they are not built or indexed.
