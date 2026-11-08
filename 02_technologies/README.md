# 02 Technologies — chapter plan

Guiding line: **classify AM by what happens to the material**, following the
physical-principles approach of Gebhardt (*Additive Manufacturing*, Hanser,
ch. 2: physical principles → machine elements → classification → potentials),
and place every AM process next to its conventional "twin" in DIN 8580.
Slides follow the course style (Cambria, EXED footer, picture alt text = repo path).

## 0. The starting material (introduction)

- Materials through history: Ashby's chart of the relative importance of material
  families (*Materials Selection in Mechanical Design*) — a figure to request permission for
  if the repository stays public.
- Seven starting states (DIN 8580 primary shaping 1.1–1.7): liquid, plastic, pasty,
  granular/powder, chips/fibres, gas/vapour, ionised.
- Kitchen examples, one per state: ice cube and jelly, hot-glue gun, icing and cake batter
  (baking = irreversible chemistry, like a thermoset), sandcastle and sugar cube, papier-mâché,
  frost on a window, electroformed leaf. Live demos: chocolate, UV nail gel, sugar sintered with
  hot air (CandyFab).

## 1. AM among the manufacturing processes (DIN 8580)

- Six main groups; AM = primary shaping done selectively, layer by layer, without a mould.
  Figure `02_din8580_main_groups.png`, table `tables/02_din8580_main_groups.csv`.
- One part, four routes — where is the geometry stored (mould, die, tool path, layer path)?
  Figure `02_create_form_cut_add.png`.
- Conventional twins by state of the starting material: figure `02_primary_shaping_states.png`,
  table `tables/02_primary_shaping_states.csv`, and the seven pair schematics
  `02_<state>_<conventional>_vs_<additive>.png`.

## 2. Material paths (the physics of consolidation)

| Path | Mechanism | Processes |
|---|---|---|
| liquid → solid | cooling; polymerisation; hydration; drying | VPP, MJT, concrete, paste extrusion |
| solid → liquid → solid | transient melt pool | PBF, DED, wire-arc, FFF (softening) |
| solid → solid | binder; sintering (diffusion); plastic deformation | binder jetting, LOM, cold spray, friction stir, ultrasonic AM |
| gas or ions → solid | deposition from vapour; electrochemical reduction | laser CVD, aerosol jet, electrochemical AM |

References: Kruth (CIRP 1991, 1998) state of the material; Kruth et al. RPJ 2005 binding
mechanisms; Tuncer & Bose JOM 2020 solid-state AM; Gebhardt ch. 2.3.

## 3. Machine elements and addressing (Gebhardt 2.4)

Moving element (plotter, scanner, robot) × generating element (laser, nozzle, extruder, knife)
→ point / line / area / volume. Morphological box: each process is one path through it;
empty cells = new processes (area-wise PBF, volumetric printing).

## 4. Clocks and interfaces

- Setting time on a log scale: photopolymer ms, melt pool µs–ms, FFF s, concrete min–h,
  sintering h, cake ≈ 30 min.
- What joins layer *n* to *n−1*: over-cure, remelting, polymer interdiffusion, plastic
  deformation, binder bridges + sintering necks, glue → anisotropy and Z-weakness.

## 5. Theoretical potentials (Gebhardt 2.6)

Physics → consequence → design rule: smallest detail (spot, droplet, particle), accuracy
(shrinkage of the transformation), surface (layer + attached particles), residual stress.
Bridge to chapter 03 *Materials in design*. Inspiration: Ashby's process-selection charts
(material compatibility, size, tolerance, roughness, economic batch size), with AM added.

## 6. The standard and the market

- ISO/ASTM 52900 seven categories as a map over sections 2–3.
- Machines, sizes and prices (end of chapter): `tables/02_machines_lpbf_metal.csv`,
  `tables/02_machines_binder_jetting_metal.csv`, `tables/02_machines_microprinting.csv`.
- Source deck: *03_Technologies* (Keynote, 2025) — scales and materials, microprinting,
  maturity, pricing, acting companies.

## Building the figures

```bash
python tools/build_figures.py          # every NN_*/figures/*.tex -> .pdf + .png (300 dpi)
```
Needs XeLaTeX (TeX Live / MacTeX), poppler (`pdftoppm`) and the Caladea font.
Shared style: `tools/tikz/xfab-tikz.sty` (one colour per DIN 8580 state).
