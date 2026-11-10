#!/usr/bin/env python3
"""Build 02_technologies/slides/02_technologies.pptx from the course template.

    python 02_technologies/slides/build_02_technologies.py
    python tools/xfab.py footer 02_technologies/slides/02_technologies.pptx --skip-first

The template is the chapter 04 deck (layouts, theme; fonts come from templates/style.json via xfab.py restyle); its slides
are removed and the chapter 02 slides are written. Every picture carries its
repository path in the alt text, so `xfab.py sync` refreshes it later.
Speaker notes carry the French and German keywords.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
import xfab  # noqa: E402  (set_alt, fit_box, image_size, placeholder_png)

TEMPLATE = REPO / "04_industries/slides/04_risk_human_activities.pptx"
OUT = REPO / "02_technologies/slides/02_technologies.pptx"
FIG = "02_technologies/figures/"

INK = RGBColor(0x1F, 0x29, 0x33)
SOFT = RGBColor(0x5F, 0x6B, 0x76)
CARD = RGBColor(0xEE, 0xF1, 0xF4)
HEAD = RGBColor(0x2B, 0x34, 0x40)
RULE = "D5DBE1"
ACCENT = RGBColor(0x36, 0x47, 0x5A)

prs = Presentation(TEMPLATE)
W, H = prs.slide_width, prs.slide_height
# drop the template's slides, keep layouts and theme
sldIdLst = prs.slides._sldIdLst
for sldId in list(sldIdLst):
    prs.part.drop_rel(sldId.rId)
    sldIdLst.remove(sldId)
LAY = {l.name: l for l in prs.slide_layouts}


# ------------------------------------------------------------------ helpers
def ph(s, idx):
    return next(p for p in s.placeholders if p.placeholder_format.idx == idx)


def notes(s, text):
    if text:
        s.notes_slide.notes_text_frame.text = text


def title_slide(title, note=""):
    s = prs.slides.add_slide(LAY["TITLE_ONLY"])
    ph(s, 100).text = title
    notes(s, note)
    return s


def section(title, sub, note=""):
    s = prs.slides.add_slide(LAY["SECTION"])
    ph(s, 100).text = title
    ph(s, 101).text = sub
    notes(s, note)
    return s


def text(s, x, y, w, h, lines, size=14, bold_first=False, color=INK, font=None, align=None, italic=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    if isinstance(lines, str):
        lines = [lines]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ln
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.italic = italic
        if font:
            p.font.name = font
        if align:
            p.alignment = align
        if bold_first and i == 0:
            p.font.bold = True
        p.space_after = Pt(4)
    return tb


def card(s, x, y, w, h, heading, lines, size=13.5):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.adjustments[0] = 0.04
    sh.fill.solid(); sh.fill.fore_color.rgb = CARD
    sh.line.fill.background()
    sh.shadow.inherit = False
    sh.name = "card"
    text(s, x + 0.2, y + 0.12, w - 0.4, 0.45, heading, size=17, font="Inter", color=INK)
    text(s, x + 0.2, y + 0.62, w - 0.4, h - 0.7, lines, size=size)
    return sh


def figure(s, name, x, y, w, h):
    rel = FIG + name
    f = REPO / rel
    data = f.read_bytes() if f.exists() else xfab.placeholder_png(rel)
    src = str(f) if f.exists() else __import__("io").BytesIO(data)
    l, t, ww, hh = xfab.fit_box((Inches(x), Inches(y), Inches(w), Inches(h)), xfab.image_size(data))
    pic = s.shapes.add_picture(src, Emu(l), Emu(t), Emu(ww), Emu(hh))
    xfab.set_alt(pic, rel)
    pic.name = Path(rel).stem
    return pic


def source(s, txt, y=6.72):
    text(s, 0.5, y, 12.3, 0.3, txt, size=10, color=SOFT)


def _border(tc, color=RULE):
    tcPr = tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = etree.SubElement(tcPr, qn(tag), w="9525")
        sf = etree.SubElement(ln, qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr"), val=color)


def table(s, x, y, w, rows, widths, size=12, head_size=13, row_h=0.36):
    nr, nc = len(rows), len(rows[0])
    gf = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    t = gf.table
    tblPr = gf._element.graphic.graphicData.tbl.tblPr
    for a in ("firstRow", "bandRow"):
        tblPr.set(a, "0")
    tot = sum(widths)
    for j, wd in enumerate(widths):
        t.columns[j].width = Inches(w * wd / tot)
    for i, row in enumerate(rows):
        t.rows[i].height = Inches(row_h)
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.margin_left = c.margin_right = Inches(0.06)
            c.margin_top = c.margin_bottom = Inches(0.04)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            tf.paragraphs[0].text = str(val)
            for p in tf.paragraphs:
                p.font.size = Pt(head_size if i == 0 else size)
                p.font.bold = (i == 0) or (j == 0)
                p.font.color.rgb = RGBColor(255, 255, 255) if i == 0 else INK
            c.fill.solid()
            c.fill.fore_color.rgb = HEAD if i == 0 else RGBColor(255, 255, 255)
            _border(c._tc)
    return gf


def fig_slide(title, name, note="", src=None, cardspec=None, fig_w=None):
    """Figure slide: full width, or figure left + one card right."""
    s = title_slide(title, note)
    if cardspec:
        fw = fig_w or 8.3
        figure(s, name, 0.5, 1.35, fw, 5.2)
        card(s, 0.5 + fw + 0.3, 1.35, 12.3 - fw - 0.3, 5.2, cardspec[0], cardspec[1])
    else:
        figure(s, name, 0.5, 1.3, 12.3, 5.3)
    if src:
        source(s, src)
    return s


# ------------------------------------------------------------------ slides
s = section("Technologies", "From a shapeless material to a part: shaping, then adding, layer by layer",
            "FR : technologies de fabrication additive. DE: Fertigungstechnologien.")

s = title_slide("The path of this chapter")
steps = [("0", "Materials and traditional technologies", "what is made, how it is shaped, the kitchen and the machines"),
         ("1", "AM as layer-wise primary shaping", "every AM process is an old primary-shaping process, made selective"),
         ("2", "A morphological box", "material state × feedstock × agent × addressing"),
         ("3", "Clocks", "how fast the material sets, how fast the next layer comes"),
         ("4", "The layer interface", "what joins layer n to layer n − 1"),
         ("5", "From physics to potentials", "detail, accuracy, surface, residual stress")]
for i, (n, h, b) in enumerate(steps):
    x = 0.5 + (i % 3) * 4.15
    y = 1.4 + (i // 3) * 2.75
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.95), Inches(2.5))
    sh.adjustments[0] = 0.04; sh.fill.solid(); sh.fill.fore_color.rgb = CARD; sh.line.fill.background()
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.25), Inches(y + 0.25), Inches(0.55), Inches(0.55))
    o.fill.solid(); o.fill.fore_color.rgb = ACCENT; o.line.fill.background()
    o.text_frame.text = n; o.text_frame.paragraphs[0].font.size = Pt(18); o.text_frame.paragraphs[0].font.bold = True
    o.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    text(s, x + 0.95, y + 0.22, 2.85, 0.9, h, size=17, font="Inter")
    text(s, x + 0.25, y + 1.2, 3.5, 1.2, b, size=13.5, color=SOFT)
source(s, "Structure after Gebhardt & Hötter, Additive Manufacturing (Hanser 2016), ch. 2; figures in the style of M. F. Ashby.")

fig_slide("One colour convention for every schematic", "02_a00_colour_convention.png",
          "Kitchen figures: pale yellow → blue. Industrial figures: orange → slate. Moulds hatched, tools grey; "
          "heat orange waves, radiation magenta, electricity blue, chemistry green.")

# ======================= 0 materials and traditional technologies
section("0 · Materials and traditional technologies", "What we make things from, and the six ways of making them",
        "FR : matériaux et procédés traditionnels. DE: Werkstoffe und konventionelle Fertigungsverfahren.")

s = title_slide("Materials through the ages")
figure(s, "02_ashby_materials_evolution.png", 0.5, 1.35, 8.3, 5.1)
card(s, 9.1, 1.35, 3.7, 5.1, "Four families", [
    "Metals", "Polymers and elastomers", "Ceramics and glasses", "Composites",
    "Relative importance changes with time: the age of steel, of polymers, of composites.",
    "Every family has its own ways of being shaped."])
source(s, "M. F. Ashby, Materials Selection in Mechanical Design, Butterworth-Heinemann: evolution of engineering materials with time "
          "(picture to add: 02_ashby_materials_evolution.png, licence to check).")
notes(s, "FR : métaux, polymères et élastomères, céramiques et verres, composites. "
         "DE: Metalle, Polymere und Elastomere, Keramiken und Gläser, Verbundwerkstoffe.")

fig_slide("Shape created, shape changed, material changed", "02_a01_process_groups.png",
          "DIN 8580 main groups. FR : mise en forme primaire, formage, séparation, assemblage, revêtement, "
          "modification des propriétés. DE: Urformen, Umformen, Trennen, Fügen, Beschichten, Stoffeigenschaft ändern.")

s = title_slide("What is what: the six groups and their cohesion")
table(s, 0.5, 1.4, 12.3, [
    ["DIN 8580", "English", "Français", "Deutsch", "Cohesion", "Examples"],
    ["1", "Primary shaping", "Mise en forme primaire", "Urformen", "created", "casting, injection moulding, sintering"],
    ["2", "Forming", "Formage", "Umformen", "kept", "forging, rolling, deep drawing"],
    ["3", "Separating", "Séparation", "Trennen", "reduced", "turning, milling, cutting"],
    ["4", "Joining", "Assemblage", "Fügen", "increased", "welding, brazing, bonding"],
    ["5", "Coating", "Revêtement", "Beschichten", "increased", "painting, plating, spraying"],
    ["6", "Changing properties", "Modification des propriétés", "Stoffeigenschaft ändern", "atoms rearranged", "heat treatment, hardening, HIP"],
], [0.8, 1.9, 2.4, 2.3, 1.5, 3.4], row_h=0.5, size=13)
card(s, 0.5, 5.25, 12.3, 1.3, "Additive manufacturing belongs to group 1",
     ["It creates the shape and the cohesion of the part from a shapeless material, like casting, but without a mould: "
      "the shape comes from a file, layer by layer."])
source(s, "DIN 8580, Fertigungsverfahren — Begriffe, Einteilung.")

kitchen = [
    ("02_b01_kitchen_primary_shaping.png", "Kitchen · primary shaping: a cake takes its tin's shape",
     "FR : mise en forme primaire (moulage). DE: Urformen (Gießen)."),
    ("02_b02_kitchen_forming.png", "Kitchen · forming: same dough, new shape",
     "FR : formage, laminage. DE: Umformen, Walzen."),
    ("02_b03_kitchen_separating.png", "Kitchen · separating: slicing removes material",
     "FR : séparation, usinage, copeaux. DE: Trennen, Spanen, Späne."),
    ("02_b04_kitchen_joining.png", "Kitchen · joining: icing glues two walls",
     "FR : assemblage, collage, soudage. DE: Fügen, Kleben, Schweißen."),
    ("02_b05_kitchen_coating.png", "Kitchen · coating: a glaze, a new surface",
     "FR : revêtement. DE: Beschichten."),
    ("02_b06_kitchen_properties.png", "Kitchen · changing properties: the boiled egg",
     "FR : modification des propriétés, traitement thermique. DE: Stoffeigenschaft ändern, Wärmebehandlung. "
     "Later: the kitchen parallel extends to a material twin — heterogeneous, fibrous and crystalline materials."),
]
for f, t, n in kitchen:
    fig_slide(t, f, n)

s = title_slide("Processes, as Ashby classifies them")
figure(s, "02_c00_ashby_process_tree.png", 0.5, 1.35, 7.6, 5.2)
card(s, 8.4, 1.35, 4.4, 5.2, "Kingdom, family, class", [
    "Ashby sorts processes like living things: kingdom → family → class → member → attributes.",
    "Three families: shaping, joining, surface treatment.",
    "Additive manufacturing is one class of shaping.",
    "Each member is described by attributes: materials, size, tolerance, roughness, economic batch size."])
source(s, "M. F. Ashby, Materials Selection in Mechanical Design, 5th ed., 2016, ch. 6–7.")
notes(s, "FR : mise en forme, assemblage, traitement de surface. DE: Formgebung, Fügen, Oberflächenbehandlung.")

machines = [
    ("02_c01_sand_casting.png", "Casting: the mould holds the shape",
     ("Primary shaping from the liquid", ["Molten metal fills a cavity and solidifies.",
      "Sand moulds: one part each; die casting: steel moulds, many parts.", "Risers feed the shrinkage on solidification.",
      "Twin in AM: powder bed fusion, DED (melt and solidify)."]),
     "FR : fonderie, moulage en sable, masselotte. DE: Gießen, Sandguss, Speiser."),
    ("02_c02_injection_moulding.png", "Injection moulding: plastic flow into a steel mould",
     ("Shaping from the plastic state", ["Pellets melt in a heated barrel, a screw pushes the melt.",
      "The mould is clamped, cooled, opened: seconds per part.", "Moulds cost 10⁴–10⁵ €: large batches only.",
      "Twin in AM: material extrusion."]),
     "FR : moulage par injection. DE: Spritzgießen."),
    ("02_c03_closed_die_forging.png", "Forging: the dies hold the shape",
     ("Forming: cohesion kept", ["A hot billet is pressed or hammered between two dies.",
      "The grain flows with the shape: strong parts.", "The flash takes the excess metal.",
      "No AM twin: AM parts are not deformed, hence different microstructures."]),
     "FR : forgeage en matrice, bavure. DE: Gesenkschmieden, Grat."),
    ("02_c04_milling.png", "Machining: the tool path holds the shape",
     ("Separating: cohesion reduced", ["A rotating tool removes chips from a stock.",
      "The geometry is stored in a program, as in AM.", "Buy-to-fly of aerospace parts can reach 10–20.",
      "In AM: finishing of functional faces, hybrid machines."]),
     "FR : usinage, fraisage, copeaux. DE: Spanen, Fräsen, Späne."),
    ("02_c05_arc_welding.png", "Welding: a moving melt pool joins two parts",
     ("Joining: cohesion increased", ["An arc melts the wire and the edges; the pool solidifies behind the torch.",
      "Pool, heat-affected zone, residual stress: the same physics as in metal AM.",
      "Twin in AM: wire-arc DED and laser DED, welding bead on bead."]),
     "FR : soudage à l'arc, bain fondu. DE: Lichtbogenschweißen, Schmelzbad."),
    ("02_c06_thermal_spray.png", "Thermal spraying: droplets build a coating",
     ("Coating", ["Powder melts in a plasma or flame and hits the part.",
      "Each droplet flattens into a splat; splats build a layer.",
      "Twin in AM: cold spray, where the particles stay solid and bond by impact."]),
     "FR : projection thermique. DE: thermisches Spritzen."),
]
for f, t, c, n in machines:
    fig_slide(t, f, n, cardspec=c)

fig_slide("Changing properties: phenomena and temperatures", "02_c07_heat_treatment_scales.png",
          "Egg 60–100 °C, curing 120–180 °C, tempering, quench hardening, stress relief, HIP 900–1250 °C at 100–200 MPa. "
          "FR : trempe, revenu, détensionnement, compaction isostatique à chaud. DE: Härten, Anlassen, Spannungsarmglühen, "
          "heißisostatisches Pressen.")

fig_slide("Powder metallurgy: press, then sinter", "02_c08_press_and_sinter.png",
          "FR : métallurgie des poudres, compactage, frittage. DE: Pulvermetallurgie, Pressen, Sintern.",
          cardspec=("Primary shaping from powder", ["A die gives the shape to a green compact.",
                    "Sintering bonds the grains by diffusion below the melting point.",
                    "The part shrinks: tolerances must allow for it.",
                    "Twin in AM: binder jetting followed by sintering."]))

s = title_slide("Where is the geometry stored?")
figure(s, "02_c09_four_routes.png", 0.5, 1.3, 12.3, 3.7)
card(s, 0.5, 5.15, 12.3, 1.45, "From the tool to the file",
     ["Casting and forging store the shape in a mould or a die: expensive, so many identical parts. "
      "Machining and AM store it in a program: one part can differ from the next."])
notes(s, "FR : outillage, programme, fichier. DE: Werkzeug, Programm, Datei.")

# ======================= 1 AM as layer-wise primary shaping
section("1 · AM as layer-wise primary shaping", "Every AM process is an old primary-shaping process, made selective and layer by layer",
        "FR : la fabrication additive comme mise en forme primaire couche par couche. DE: additive Fertigung als schichtweises Urformen.")

fig_slide("Adding material: file, layer, voxel", "02_d01_file_layer_voxel.png",
          "FR : tranche, couche, voxel. DE: Schicht, Voxel.")

s = title_slide("Seven starting states, seven conventional twins")
table(s, 0.5, 1.35, 12.3, [
    ["DIN 8580", "Starting state", "Conventional twin", "AM process", "ISO/ASTM 52900"],
    ["1.1", "liquid", "casting, resin casting", "vat photopolymerisation, material jetting", "VPP, MJT"],
    ["1.2", "plastic", "injection moulding, extrusion", "material extrusion (filament, pellets)", "MEX"],
    ["1.3", "pasty", "slip casting, concrete casting", "paste extrusion: ceramics, clay, concrete", "MEX"],
    ["1.4", "granular or powder", "pressing and sintering; welding, casting", "binder jetting; powder bed fusion, DED; cold spray", "BJT, PBF, DED"],
    ["1.5", "chips or fibres", "board pressing, lamination", "sheet lamination; continuous-fibre extrusion", "SHL, MEX"],
    ["1.6", "gas or vapour", "CVD, PVD", "laser CVD", "—"],
    ["1.7", "ionised", "electroforming", "electrochemical AM", "—"],
], [1.0, 1.9, 3.1, 4.4, 1.7], row_h=0.52, size=13)
source(s, "DIN 8580 primary-shaping subgroups; ISO/ASTM 52900:2021 process categories.", y=5.75)
notes(s, "FR : liquide, plastique, pâteux, granulaire ou pulvérulent, copeaux ou fibres, gazeux, ionisé. "
         "DE: flüssig, plastisch, breiig, körnig oder pulverförmig, span- oder faserförmig, gas- oder dampfförmig, ionisiert.")

fig_slide("Four material paths to a solid", "02_e01_material_paths.png",
          "Kruth's classification by the state of the material, completed by the binding mechanisms of Kruth et al. (2005) "
          "and the solid-state processes of Tuncer & Bose (2020).")

am = [
    ("02_f02_vat_photopolymerisation.png", "Vat photopolymerisation: resin casting, one spot at a time",
     ("Twin: resin casting", ["Liquid monomers polymerise under UV light.", "Laser spot (SLA) or projected mask (DLP).",
      "Layers 25–100 µm; fine detail and smooth surfaces.", "Post-cure and support removal."]),
     "FR : photopolymérisation en cuve. DE: Badbasierte Photopolymerisation."),
    ("02_f04_material_jetting.png", "Material jetting: droplets that cure where they land",
     ("Twin: inkjet casting", ["A print head jets resin droplets, a lamp cures them.",
      "Several materials and colours in one part.", "A gel support fills the overhangs."]),
     "FR : projection de matière. DE: Freistrahl-Materialauftrag."),
    ("02_f03_material_extrusion.png", "Material extrusion: injection moulding without a mould",
     ("Twin: injection moulding", ["A filament or pellets melt in a hot end.", "The nozzle lays roads; each cools on the one below.",
      "Cheap and simple; the weak point is the bond between layers."]),
     "FR : extrusion de matière. DE: Materialextrusion."),
    ("02_f12_paste_extrusion.png", "Paste extrusion: slip and concrete, bead by bead",
     ("Twin: slip and concrete casting", ["A paste is pushed through a nozzle.", "It must flow in the nozzle and stand still on the stack.",
      "Ceramics are dried and fired; concrete sets by hydration."]),
     "FR : extrusion de pâte, impression béton. DE: Pastenextrusion, Betondruck."),
    ("02_f06_laser_powder_bed_fusion.png", "Powder bed fusion: welding and casting, layer by layer",
     ("Twin: welding, casting", ["A recoater spreads 20–100 µm of powder.", "A laser or electron beam melts the cross-section.",
      "Melt pool, fast solidification, residual stress: welding physics.", "Platform down, next layer."]),
     "FR : fusion sur lit de poudre. DE: Pulverbettbasiertes Schmelzen."),
    ("02_f07_directed_energy_deposition.png", "Directed energy deposition: a welding torch that builds",
     ("Twin: cladding, welding", ["Powder or wire is fed into a melt pool made by a laser, an arc or a beam.",
      "Large parts, repair of worn parts.", "Near-net shape: finish by machining."]),
     "FR : dépôt de matière sous énergie concentrée. DE: Gerichtete Energieeinbringung."),
    ("02_f08_sheet_lamination.png", "Sheet lamination: cut and glue",
     ("Twin: lamination, gluing", ["Sheets of paper, polymer or metal are glued or welded.",
      "Each contour is cut by a laser or a knife.", "Ultrasonic AM joins metal foils in the solid state."]),
     "FR : stratification de couches. DE: Schichtlaminierung."),
    ("02_f09_cold_spray.png", "Cold spray: thermal spraying without melting",
     ("Twin: thermal spraying", ["Particles are accelerated in a supersonic gas jet.",
      "They deform plastically at impact and bond in the solid state.", "No melt pool: little oxidation, used for repair."]),
     "FR : projection à froid. DE: Kaltgasspritzen."),
    ("02_f10_laser_cvd.png", "Laser CVD: CVD at one hot spot",
     ("Twin: CVD", ["A precursor gas decomposes on a hot surface.",
      "A focused laser makes only one spot hot.", "Fibres and rods of carbon, SiC, tungsten."]),
     "FR : dépôt chimique en phase vapeur assisté par laser. DE: laserunterstützte Gasphasenabscheidung."),
    ("02_f11_electrochemical_am.png", "Electrochemical AM: electroforming under a nozzle",
     ("Twin: electroforming", ["Metal ions are reduced on a cathode.", "A micro-nozzle confines the reaction to a meniscus.",
      "Copper and nickel at room temperature, micrometre features."]),
     "FR : fabrication additive électrochimique, électroformage. DE: elektrochemische additive Fertigung, Galvanoformung."),
]
# binder jetting gets a full-width slide (internal steps)
for f, t, c, n in am[:4]:
    fig_slide(t, f, n, cardspec=c)
s = title_slide("Binder jetting: one AM step, four powder-metallurgy steps")
figure(s, "02_f05_binder_jetting_chain.png", 0.5, 1.3, 12.3, 3.6)
card(s, 0.5, 5.0, 6.0, 1.6, "Twin: pressing and sintering", ["The printer replaces the die; curing, depowdering, debinding and "
     "sintering are those of powder metallurgy."], size=13)
card(s, 6.8, 5.0, 6.0, 1.6, "Consequences", ["No melt pool: no residual stress from printing. Shrinkage of 15–20 % "
     "must be built into the file."], size=13)
notes(s, "FR : projection de liant, déliantage, frittage. DE: Binder Jetting, Entbindern, Sintern.")
for f, t, c, n in am[4:]:
    fig_slide(t, f, n, cardspec=c)

# ======================= 2 morphological box
section("2 · A morphological box", "Material state × feedstock form × agent × addressing",
        "FR : boîte morphologique (Zwicky). DE: morphologischer Kasten.")
fig_slide("Point, line, area, volume", "02_d02_point_line_area_volume.png",
          "Gebhardt: vector (contour traced continuously, most accurate, slowest), raster (line by line), mask "
          "(whole layer at once, time independent of layer complexity). Volume: tomographic and volumetric printing.")
s = title_slide("Every process is one path through the box")
table(s, 0.5, 1.35, 12.3, [
    ["Process", "Material state", "Feedstock form", "Agent", "Addressing"],
    ["SLA", "liquid", "vat", "light", "point"],
    ["DLP", "liquid", "vat", "light", "area"],
    ["Multi-jet fusion", "powder", "bed", "agent + heat", "line"],
    ["Binder jetting", "powder", "bed", "binder", "line"],
    ["Laser PBF", "powder", "bed", "laser", "point"],
    ["Laser DED", "powder or wire", "jet", "laser", "point"],
    ["FFF", "plastic", "filament", "heat", "point"],
    ["Cold spray", "powder", "jet", "kinetic energy", "point"],
    ["Volumetric printing", "liquid", "vat", "light", "volume"],
], [2.6, 2.3, 2.3, 2.6, 2.0], row_h=0.42, size=13)
card(s, 0.5, 5.75, 12.3, 0.85, "Exercise", ["Find the empty cells: area-wise metal PBF and volumetric printing appeared there."], size=13)

# ======================= 3 clocks
section("3 · Clocks", "A race between how fast the material sets and how fast the next layer comes",
        "FR : temps caractéristiques. DE: charakteristische Zeiten.")
fig_slide("How fast does the material set?", "02_e02_clocks.png",
          "Explains build speed, why supports are needed, and the open-time problem of concrete.")

# ======================= 4 layer interface
section("4 · The layer interface", "What joins layer n to layer n − 1?",
        "FR : interface entre couches, anisotropie. DE: Schichtgrenzfläche, Anisotropie.")
fig_slide("Six ways to join a layer to the one below", "02_e03_layer_interfaces.png",
          "Is it the same mechanism that formed the layer? This explains anisotropy, the weaker z direction, and why "
          "each path needs its own design rules.")

# ======================= 5 potentials
section("5 · From physics to potentials", "Gebhardt's theoretical potentials, derived from the material path",
        "FR : potentiels théoriques. DE: theoretische Potenziale.")
s = title_slide("From physics to design rules")
table(s, 0.5, 1.4, 12.3, [
    ["Criterion", "Set by", "Orders of magnitude", "Design rule"],
    ["Smallest detail", "spot, droplet or particle size", "0.1 µm (2PP) – 0.1 mm (PBF) – 1 mm (DED)", "no feature below ≈ 2–3 voxels"],
    ["Accuracy", "shrinkage of the transformation", "polymerisation, solidification; 15–20 % linear on sintering", "scale the file, test parts"],
    ["Surface", "layer thickness + partly bonded particles", "Ra ≈ 5–20 µm for metal PBF", "machine functional faces"],
    ["Residual stress", "a liquid-to-solid step over a large temperature range", "PBF, DED: high; binder jetting, cold spray: low", "supports, stress relief, HIP"],
    ["Anisotropy", "the layer interface", "z direction weakest in FFF", "orient the load along the layers"],
], [2.2, 3.3, 3.9, 2.9], row_h=0.68, size=13)
source(s, "After Gebhardt & Hötter (2016) §2.6; orders of magnitude are indicative.", y=5.9)

# ======================= machines and prices
section("Machines and prices", "Build volumes, resolutions and investment", "FR : machines et prix. DE: Maschinen und Preise.")
s = title_slide("Metal laser powder bed fusion: investment")
table(s, 0.5, 1.4, 12.3, [["Manufacturer", "Model", "Price (USD)", "Build volume (mm)"],
    ["SLM Solutions", "SLM 125", "400 000 – 500 000", "125 × 125 × 125"],
    ["SLM Solutions", "SLM 280", "500 000 – 800 000", "280 × 280 × 300"],
    ["SLM Solutions", "SLM 500", "800 000 +", "500 × 500 × 500"],
    ["EOS", "M 290", "600 000 – 1 000 000", "290 × 290 × 400"],
    ["EOS", "M 400", "1 000 000 +", "400 × 400 × 400"],
    ["Renishaw", "AM 400", "600 000 – 1 000 000", "to check"],
    ["TRUMPF", "TruPrint 1000", "170 000", "100 × 100 × 100"]], [2.5, 2.5, 3.0, 3.0], row_h=0.48, size=13)
source(s, "Source: 03_Technologies deck (2025), after AMPOWER Insights. Table: tables/02_machines_lpbf_metal.csv.", y=5.6)

s = title_slide("Metal binder jetting: five systems")
table(s, 0.5, 1.4, 12.3, [["System", "Maker", "Build volume", "Build speed", "Resolution", "Cost"],
    ["X160PRO", "ExOne (Desktop Metal)", "800 × 500 × 400 mm", "≤ 3 120 cm³/h", "layers 30–200 µm", "$$$$"],
    ["Production System P-50", "Desktop Metal", "490 × 380 × 260 mm", "≤ 12 000 cm³/h", "1 200 dpi", "$$$$$"],
    ["Metal Jet S100", "HP", "430 × 309 × 200 mm", "1 990 cm³/h", "1 200 dpi", "$$$"],
    ["Series 3", "GE Additive", "500 × 500 × 500 mm", "≤ 100 × metal PBF", "walls ≥ 400 µm", "$$$$"],
    ["PX100", "Markforged", "250 × 217 × ? mm", "1 000 cm³/h", "1 600 dpi", "$$$"]],
    [2.6, 2.4, 2.3, 2.0, 1.9, 1.0], row_h=0.55, size=12.5)
source(s, "Source: voxelmatters.com, complete guide to binder-based metal 3D printing. Table: tables/02_machines_binder_jetting_metal.csv.", y=5.2)

s = title_slide("Microprinting: liquid, paste, powder and ions")
table(s, 0.5, 1.35, 12.3, [["Printer", "Technology", "State", "Min. layer", "Resolution", "Price (USD)"],
    ["BMF microArch", "projection micro-SLA", "liquid", "5 µm", "2 µm", "145 000 – 230 000"],
    ["Nanoscribe Quantum X", "two-photon polymerisation", "liquid", "0.1 µm", "0.2 µm", "500 000"],
    ["UpNano NanoOne", "two-photon polymerisation", "liquid", "0.17 µm", "0.01 µm", "on request"],
    ["Incus Hammer Lab35", "lithography-based metal", "pasty", "10 µm", "35 µm", "250 000"],
    ["Exaddon Ceres", "electrochemical deposition", "ionised", "—", "< 1 µm", "272 000"],
    ["3D MicroPrint DMP", "micro laser sintering", "powder", "15 µm", "1 µm", "on request"],
    ["Microlight3D µFAB-3D", "two-photon polymerisation", "liquid", "0.6 µm", "0.2 µm", "120 000 – 180 000"],
    ["Femtika Nanofactory", "two-photon polymerisation", "liquid", "0.2 µm", "0.3 µm", "on request"]],
    [2.6, 2.8, 1.2, 1.3, 1.4, 2.2], row_h=0.5, size=12.5)
source(s, "Source: all3dp.com, micro 3D printing guide. Table: tables/02_machines_microprinting.csv.", y=6.0)

s = title_slide("References")
text(s, 0.5, 1.35, 5.95, 5.4, [
    "Classification and processes",
    "DIN 8580, Fertigungsverfahren — Begriffe, Einteilung. Beuth.",
    "ISO/ASTM 52900:2021, Additive manufacturing — General principles — Fundamentals and vocabulary.",
    "M. F. Ashby, Materials Selection in Mechanical Design, 5th ed., Butterworth-Heinemann, 2016.",
    "M. F. Ashby, H. Shercliff, D. Cebon, Materials: Engineering, Science, Processing and Design, 3rd ed., 2013.",
    "M. F. Ashby, K. Johnson, Materials and Design, 3rd ed., 2014.",
], size=13, bold_first=True)
text(s, 6.85, 1.35, 5.95, 5.4, [
    "Additive manufacturing",
    "A. Gebhardt, J.-S. Hötter, Additive Manufacturing: 3D Printing for Prototyping and Manufacturing, Hanser, 2016.",
    "I. Gibson, D. Rosen, B. Stucker, M. Khorasani, Additive Manufacturing Technologies, 3rd ed., Springer, 2021.",
    "J.-P. Kruth, Material incress manufacturing by rapid prototyping techniques, CIRP Annals 40 (1991).",
    "J.-P. Kruth, M. C. Leu, T. Nakagawa, Progress in additive manufacturing and rapid prototyping, CIRP Annals 47 (1998).",
    "J.-P. Kruth et al., Binding mechanisms in SLS and SLM, Rapid Prototyping Journal 11 (2005).",
    "N. Tuncer, A. Bose, Solid-state metal additive manufacturing: a review, JOM 72 (2020).",
], size=13, bold_first=True)

prs.save(OUT)
print(f"{OUT.relative_to(REPO)}: {len(prs.slides)} slides")
