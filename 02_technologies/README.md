# 02 Technologies — chapter plan

A growing path, one idea per slide. Figures follow M. F. Ashby's drawing style: plain
cross-sections, pale flat fills, thin dark outlines, a few labels with leader lines, no title
inside the picture (titles go on the slide, with French and German names where useful).
Slides use the course style (Cambria, EXED footer, picture alt text = repository path).

Figure names carry the step: `02_a…` step (i), `02_b…` step (ii), and so on.

## Colour convention (`02_a00_colour_convention.png`)

| Meaning | Colour |
|---|---|
| initial material (liquid, paste, powder, wire, sheet, gas) | pale yellow |
| final material, the part | blue |
| mould or die (carries the shape) | grey hatching |
| other tools | light grey |
| carrier fluid (water, electrolyte, gas) | pale cyan |
| force, motion | dark arrow |
| heat | orange wavy arrow |
| radiation (laser, UV, electrons) | magenta beam |
| electricity | blue wire |
| chemistry (binder, reaction) | green |

Defined once in `tools/tikz/xfab-tikz.sty`.

## The path

| Step | Content | Figures |
|---|---|---|
| (i) | The structuring idea: shape created, shape changed, material changed — what is what (DIN 8580, six groups; cohesion created / kept / reduced / increased) | `02_a01_process_groups` ✔ |
| (ii) | The six groups in the kitchen, without AM: cake tin, rolling pin, bread knife, gingerbread and icing, glazing, boiled egg — each with its industrial twin | `02_b01` … `02_b06` ✔ |
| (iii) | Classical machines, a series in the same style: casting, injection moulding, forging/rolling, machining, welding, coating, powder pressing + sintering (Ashby's process classes) | to do — `drafts/` has material |
| (iv) | AM: adding material voxel by voxel and layer by layer; geometry stored in a file, not in a mould (Gebhardt 2.4: point, line, area, volume) | to do |
| (v) | The layer philosophy: material paths (liquid→solid, solid→liquid→solid, solid→solid, gas/ions→solid), clocks (setting times) and the interface between layers; Gebhardt's five ideas | to do |
| (vi) | AM technologies one by one, with internal steps where there are several (binder jetting: print, cure, depowder, debind, sinter); ISO/ASTM 52900 as the map; machines and prices at the end | to do — tables ready |

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
