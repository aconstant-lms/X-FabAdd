"""Shared data and style for the 02_i0x printer charts and maps."""
import csv
from pathlib import Path

import matplotlib
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
CSV = HERE.parent / "tables" / "02_printers_price_voxel.csv"

INK, GREY, GRID = "#1b2433", "#566170", "#e3e1db"

# One colour per technology, fixed order (finest voxel first).
# Validated with the dataviz validate_palette.js (light surface): all checks pass;
# contrast < 3:1 for three hues -> every point carries a direct label.
TECH = [
    ("2PP / MPP",        "#2a78d6", "o"),   # two-/multiphoton polymerisation
    ("PµSL (micro-DLP)", "#eb6834", "s"),
    ("DLP",              "#1baf7a", "D"),
    ("MSLA (LCD)",       "#008300", "P"),
    ("CLIP / DLS",       "#eda100", "^"),   # Carbon
    ("laser SLA",        "#e87ba4", "v"),
]
COL = {t: c for t, c, _ in TECH}
MRK = {t: m for t, _, m in TECH}


def rows():
    return list(csv.DictReader(open(CSV, encoding="utf-8")))


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
