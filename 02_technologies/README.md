# 02 Technologies — chapter plan

A growing path, one idea per slide. Figures follow M. F. Ashby's drawing style: plain
cross-sections, pale flat fills, thin dark outlines, a few labels with leader lines, no title
inside the picture (titles go on the slide, with French and German names where useful).
Slides use the course style (Space Grotesk titles, Inter body, EXED footer, picture alt text = repository path).

Figure names carry the part: `02_a` structure, `02_b` kitchen, `02_c` classical machines, `02_d` voxels and addressing, `02_e` paths, clocks, interfaces, `02_f` AM processes, `02_g` industrial twins, `02_h` process animations (SLA, DLP, multi-photon, Carbon CLIP, volumetric, LPBF, powder DED, wire DED, cold spray), `02_i` polymer printer prices and maps, `02_j` polymer materials (pyramid, Ashby, prices, makers), `02_k` maturity index, `02_l` polymer physical laws, `02_m` metal physics, `02_n` metal supply (machines, powders, makers, market).

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

Since 17 Nov 2026 the chapter is taught from two claude.ai Slides decks, built by
`slides/claude_deck/gen_technology_decks.py` (which runs `gen_am_technologies.py`, then
`slides_polymer_new.py`, `slides_metal_new.py` and `slides_metal_supply.py`; Andrei's page edits are kept
verbatim in `slides/claude_deck/raw/`). Slide use of every figure: `figures/external_usage.csv`.

| Deck | Link | Slides | Content |
|---|---|---|---|
| AM technologies: polymers | https://claude.ai/artifact/QUfFAekdYybxee5PVWWPAF | 66 | polymer processes (photopolymerisation, Carbon CLIP, MJT, MEX, SHL, PBF, injection moulding), prices and makers, box, clocks, interface, six physical laws, maturity index, exercise "Polymer AM 2022 → 2026" and its debrief (volumetric printing, PERFI, Quadratic 3D, 2026 status, market), references |
| AM technologies: metals | https://claude.ai/artifact/Jre7zVeP4jn9DWpsZQVyVf | 39 | metal processes (LPBF, powder DED, WAAM, cold spray, binder jetting, powder metallurgy), box, clocks, interface, five physical laws for metals, machines, powders and makers (prices, maps, China, market), references |
| AM technologies: slides set aside | https://claude.ai/artifact/92KDPMDHVf63xrDNPEGhwJ | 28 | Part 1 traditional technologies (kitchen cases and industrial twins), other AM processes (paste, micro, LCVD, ECAM), parked slides |
| AM technologies (superseded) | https://claude.ai/artifact/4bKyVcrndt1NUbHWZMYcqk | 68 | the single deck before the split; every slide is in one of the three decks above |

The polymer deck holds the exercise answers (part 9 and some notes): do not share it with students before the session.

- **PDF and PowerPoint copies** of the three decks: `slides/02_technology_polymer|metal|unused.pdf/.pptx` (see `slides/README.md`); the first PowerPoint version (52 slides, 9 Nov) is `slides/02_technologies_old_2026-11-09.pptx`.

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
- `02_printers_price_voxel.csv` — polymer printers: price, voxel, build volume, head office (charts `02_i…`, maps)
- `02_polymer_prices_makers.csv`, `02_polymers_ashby.csv` — polymer feedstock prices, makers, Ashby data (`02_j…`)
- `02_ampower_maturity_2022_2026.csv` — AMPOWER Insights Vol. 11 (2022) maturity points and the 2026 status of the ten companies (exercise answer key: public)
- `02_machines_metal_makers.csv` (column `plotted`: yes / tier / quote), `02_metal_powder_prices.csv`, `02_powder_makers.csv`, `02_powder_co2.csv`, `02_metal_market_ampower.csv` — metal supply (`02_n…`)

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
python 02_technologies/figures/02_h08_lpbf_animation.py   # each animation / chart has its own script
```
TikZ needs XeLaTeX (TeX Live / MacTeX), poppler (`pdftoppm`) and the Inter font. Animations use
pycairo and `tools/iso_anim.py`; charts use matplotlib (`_printers_common.py` holds the validated
technology palette); the maps need `geopandas<1.0`.

Pictures kept out of this public repository until permission is checked: the AMPOWER polymer
landscape (`02_k02`, deck only) and Ashby's materials evolution. The Carbon and Femtika
animations are in the repository with their credit; licence still to confirm.
`figures/drafts/` holds the first, denser schematics, kept as material for steps (iii) and (vi);
they are not built or indexed.
