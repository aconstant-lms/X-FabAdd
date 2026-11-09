"""02_i02 - Where the photopolymer (and micro-metal) printer makers are.

Reads ../tables/02_printers_price_voxel.csv (one marker per manufacturer HQ),
world map + Europe/Israel inset. Coastlines: Natural Earth 1:110m (public domain)
bundled with geopandas < 1.0.  Usage: python 02_i02_manufacturers_map.py
"""
import csv, warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import geopandas as gpd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
CSV = HERE.parent / "tables" / "02_printers_price_voxel.csv"
for f in font_manager.findSystemFonts():
    if "Caladea" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Caladea", "font.size": 12})
INK, GREY = "#1b2433", "#566170"
LAND, EDGE, SEA = "#ece9e2", "#c9c4b8", "#ffffff"

FAMILIES = [
    ("TPP / multiphoton",   "#2a78d6", "o"),
    ("PµSL (micro-DLP)",    "#eb6834", "s"),
    ("DLP / MSLA",          "#1baf7a", "D"),
    ("CLIP / DLS (Carbon)", "#eda100", "^"),
    ("laser SLA",           "#e87ba4", "v"),
    ("metal (micro; for reference)", "#8d949b", "X"),
]
COL = {f: c for f, c, _ in FAMILIES}; MRK = {f: m for f, _, m in FAMILIES}

rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
makers = {}
for r in rows:  # one entry per manufacturer (first family listed)
    makers.setdefault(r["manufacturer"], r)

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world = world[world["continent"] != "Antarctica"]

SHORT = {"Boston Micro Fabrication (BMF)": "BMF", "Nano Dimension (ex Nanofabrica)": "Nano Dimension",
         "Prusa Research": "Prusa"}
# label offsets in points (dx, dy, ha) for the world map; Europe/Israel names go in the inset
W_OFF = {"Carbon": (-8, 0, "right"), "Formlabs": (8, 4, "left"), "Stratasys": (-8, 6, "right"),
         "3D Systems": (8, -6, "left"), "Boston Micro Fabrication (BMF)": (10, -4, "left"),
         "Elegoo": (-8, -8, "right"), "UnionTech": (8, 2, "left"), "Asiga": (-8, 0, "right")}
E_OFF = {"Nanoscribe": (-8, -4, "right"), "UpNano": (10, 2, "left"), "Incus": (8, -8, "left"),
         "Microlight3D": (8, 0, "left"), "Femtika": (8, 0, "left"), "Prusa Research": (6, 13, "left"),
         "3D MicroPrint": (-8, 8, "right"), "Exaddon": (-8, -8, "right"),
         "Nano Dimension (ex Nanofabrica)": (-8, 8, "right"), "Stratasys": (-8, -8, "right")}

fig = plt.figure(figsize=(14, 6.4))
ax = fig.add_axes([0.0, 0.0, 0.66, 0.88])
world.plot(ax=ax, color=LAND, edgecolor=EDGE, linewidth=0.5)
ax.set_xlim(-145, 160); ax.set_ylim(-45, 68); ax.set_aspect("equal"); ax.axis("off")

ins = fig.add_axes([0.665, 0.28, 0.325, 0.60])
world.plot(ax=ins, color=LAND, edgecolor=EDGE, linewidth=0.6)
ins.set_xlim(-2, 38); ins.set_ylim(29, 58); ins.set_aspect("equal")
ins.set_xticks([]); ins.set_yticks([])
for s in ins.spines.values():
    s.set_edgecolor(GREY); s.set_linewidth(0.8)
ins.set_title("Europe and Israel", fontsize=13, color=GREY, loc="left", style="italic")
ax.add_patch(plt.Rectangle((-2, 29), 39, 29, fill=False, ec=GREY, lw=0.8, ls="--"))


def mark(a, r, off):
    fam = r["family"]; lon, lat = float(r["lon"]), float(r["lat"])
    a.scatter([lon], [lat], s=90, marker=MRK[fam], color=COL[fam], edgecolor="white",
              linewidth=1.2, zorder=4)
    if off:
        dx, dy, ha = off
        name = SHORT.get(r["manufacturer"], r["manufacturer"])
        a.annotate(name, (lon, lat), xytext=(dx, dy), textcoords="offset points",
                   ha=ha, va="center", fontsize=12, color=INK, zorder=5)


JIT = {"Boston Micro Fabrication (BMF)": (2.5, 2.0), "Incus": (0.9, -0.5)}
for m, (dlon, dlat) in JIT.items():
    makers[m] = dict(makers[m], lon=str(float(makers[m]["lon"]) + dlon), lat=str(float(makers[m]["lat"]) + dlat))
in_box = lambda r: -2 <= float(r["lon"]) <= 37 and 29 <= float(r["lat"]) <= 58
for m, r in makers.items():
    mark(ax, r, None if in_box(r) else W_OFF.get(m, (8, 0, "left")))
    if in_box(r):
        mark(ins, r, E_OFF.get(m, (8, 0, "left")))
# Stratasys is dual-HQ: also mark Rehovot in the inset
st = dict(makers["Stratasys"]); st.update(lat="31.40", lon="34.811")
mark(ins, st, E_OFF["Stratasys"]); mark(ax, st, None)

fig.text(0.015, 0.94, "Who makes vat-photopolymerisation and multiphoton printers - and where",
         fontsize=17, color=INK, weight="bold")
# legend
lx = fig.add_axes([0.67, 0.01, 0.32, 0.24]); lx.axis("off")
for i, (fam, c, mk) in enumerate(FAMILIES):
    col, row = i // 3, i % 3
    x, y = 0.02 + col * 0.5, 0.93 - row * 0.17
    lx.scatter([x], [y], s=80, marker=mk, color=c, edgecolor="white", transform=lx.transAxes)
    lx.text(x + 0.05, y, fam.replace(" (micro; for reference)", " micro-AM (ref.)"),
            va="center", fontsize=11.5, color=INK, transform=lx.transAxes)
lx.text(0.0, 0.0, "Head offices, one marker per company (Stratasys: Eden Prairie + Rehovot);\n"
        "co-located markers nudged apart. Data: tables/02_printers_price_voxel.csv.\n"
        "Coastlines: Natural Earth 1:110m (public domain).",
        fontsize=9.5, color=GREY, transform=lx.transAxes, va="bottom")

for ext in ("png", "pdf"):
    fig.savefig(HERE / f"02_i02_manufacturers_map.{ext}", dpi=200, facecolor="white")
print("ok")
