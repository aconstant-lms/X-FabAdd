"""Shared data and style for the 02_i0x printer charts and maps."""
import csv
import os
from pathlib import Path

import matplotlib
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
CSV = HERE.parent / "tables" / "02_printers_price_voxel.csv"

INK, GREY, GRID = "#1b2433", "#566170", "#e3e1db"

# One colour per technology, fixed order (finest voxel first).
# Validated with the dataviz validate_palette.js (light surface, 8 hues, Nov 2026): all checks pass;
# contrast < 3:1 for three hues -> every point carries a direct label.
TECH = [
    ("2PP / MPP",        "#2a78d6", "o"),   # two-/multiphoton polymerisation
    ("PµSL (micro-DLP)", "#eb6834", "s"),
    ("DLP",              "#1baf7a", "D"),
    ("MSLA (LCD)",       "#008300", "P"),
    ("CLIP / DLS",       "#eda100", "^"),   # Carbon
    ("laser SLA",        "#e87ba4", "v"),
    ("volumetric",       "#7b52c7", "h"),   # xolography, tomographic (AMPOWER Insights 11)
    ("high-viscosity film", "#a0522d", "p"),  # Cubicure Hot Lithography, Supernova VLM
]
# XFAB_INTRO=1: version shown before the polymer exercise, without the 2026 additions
# (volumetric and high-viscosity film printers would give the exercise answers away).
INTRO = bool(os.environ.get("XFAB_INTRO"))
HIDDEN = {"volumetric", "high-viscosity film"}
SUFFIX = "_intro" if INTRO else ""
if INTRO:
    TECH = [t for t in TECH if t[0] not in HIDDEN]
COL = {t: c for t, c, _ in TECH}
MRK = {t: m for t, _, m in TECH}


def rows():
    r = list(csv.DictReader(open(CSV, encoding="utf-8")))
    return [x for x in r if x["technology"] not in HIDDEN] if INTRO else r


def use_font(name="Inter", size=13):
    for f in font_manager.findSystemFonts():
        if name.split()[0] in Path(f).name:
            try:
                font_manager.fontManager.addfont(f)
            except Exception:
                pass
    matplotlib.rcParams.update({"font.family": name, "font.size": size,
                                "axes.edgecolor": GREY, "axes.labelcolor": INK,
                                "xtick.color": GREY, "ytick.color": GREY})


def usd(v, _=None):
    if v >= 1e6:
        return f"${v/1e6:g}M"
    if v >= 1e3:
        return f"${v/1e3:g}k"
    return f"${v:g}"


def is_lease(r):
    return "lease" in r["price_basis"] or "subscription" in r["price_basis"]
