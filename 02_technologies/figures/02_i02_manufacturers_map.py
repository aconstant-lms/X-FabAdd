"""02_i02 - Where the photopolymer printer makers are (world + Europe/Israel maps).

Same visual language as the aviation maps (04_av_map_*): sea #dfe6ee, land #cbc4b4,
coast #b3ab98, white ring markers, dark Inter labels with a light halo.
Ring colour = technology (same palette as the 02_i01 / 02_i03 charts); a maker with two
technologies (Formlabs) gets two markers side by side.
Reads ../tables/02_printers_price_voxel.csv. Coastlines: Natural Earth 1:110m (public
domain) bundled with geopandas < 1.0.
Writes 02_i02_map_world.{png,svg} and 02_i02_map_europe.{png,svg}.
Usage: python 02_i02_manufacturers_map.py
"""
import warnings
from collections import OrderedDict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
import geopandas as gpd

from _printers_common import HERE, TECH, COL, rows, use_font

warnings.filterwarnings("ignore")
use_font("Inter", 14)
matplotlib.rcParams["svg.fonttype"] = "none"
SEA, LAND, COAST, INK, HALO, FILL = "#dfe6ee", "#cbc4b4", "#b3ab98", "#1b2433", "#eef2f6", "#fbfaf7"
HALO_FX = [pe.withStroke(linewidth=4, foreground=HALO)]

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world = world[world["continent"] != "Antarctica"]

SHORT = {"Boston Micro Fabrication (BMF)": "BMF", "Nano Dimension (ex Nanofabrica)": "Nano Dimension",
         "Prusa Research": "Prusa"}
# one entry per (maker, technology); HQ position from the table
makers = OrderedDict()
for r in rows():
    makers.setdefault(r["manufacturer"], {"lat": float(r["lat"]), "lon": float(r["lon"]), "tech": []})
    if r["technology"] not in makers[r["manufacturer"]]["tech"]:
        makers[r["manufacturer"]]["tech"].append(r["technology"])
# Stratasys is dual-HQ (Eden Prairie MN + Rehovot)
makers["Stratasys (Rehovot)"] = {"lat": 31.894, "lon": 34.811, "tech": ["DLP"]}

# display nudges for co-located HQs (degrees) - documented in the caption
NUDGE = {"Elegoo": (-1.6, -1.0), "Boston Micro Fabrication (BMF)": (1.6, 1.0),
         "Nano Dimension (ex Nanofabrica)": (-0.35, 0.45), "Stratasys (Rehovot)": (0.35, -0.45)}


def draw_base(ax, xlim, ylim, aspect):
    ax.set_facecolor(SEA)
    world.plot(ax=ax, color=LAND, edgecolor=COAST, linewidth=0.6)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect(aspect)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def draw_maker(ax, name, m, label, off, step):
    lon, lat = m["lon"], m["lat"]
    dlon, dlat = NUDGE.get(name, (0, 0))
    lon, lat = lon + dlon, lat + dlat
    n = len(m["tech"])
    for i, t in enumerate(m["tech"]):
        x = lon + (i - (n - 1) / 2) * step
        ax.scatter([x], [lat], s=150, facecolor=FILL, edgecolor=COL[t], linewidth=2.6, zorder=5)
    if label:
        dx, dy, ha = off
        dx = dx + np.sign(dx) * (n - 1) * 7
        ax.annotate(label, (lon, lat), xytext=(dx, dy), textcoords="offset points", ha=ha,
                    va="center", fontsize=14, fontweight="semibold", color=INK, zorder=6,
                    path_effects=HALO_FX)


def legend(fig, rect, ncol):
    lx = fig.add_axes(rect); lx.axis("off")
    h = [Line2D([], [], ls="", marker="o", ms=10, mfc=FILL, mec=c, mew=2.4, label=t) for t, c, _ in TECH]
    lx.legend(handles=h, loc="center", ncol=ncol, frameon=False, fontsize=13,
              handletextpad=0.4, columnspacing=1.4)


EUROPE = (-2.0, 37.0, 29.5, 57.5)
in_eu = lambda m: EUROPE[0] <= m["lon"] <= EUROPE[1] and EUROPE[2] <= m["lat"] <= EUROPE[3]

# ---------------- world ----------------
W_OFF = {"Carbon": (12, 0, "left"), "Formlabs": (12, 4, "left"), "Stratasys": (-12, 4, "right"),
         "3D Systems": (12, -4, "left"), "Boston Micro Fabrication (BMF)": (12, 4, "left"),
         "Elegoo": (-12, -4, "right"), "UnionTech": (12, 0, "left"), "Asiga": (-12, 0, "right")}
fig = plt.figure(figsize=(10.4, 4.0))
ax = fig.add_axes([0, 0.16, 1, 0.84])
draw_base(ax, (-134, 158), (-42, 70), "auto")
for name, m in makers.items():
    eu = in_eu(m)
    draw_maker(ax, name, m, None if eu else SHORT.get(name, name), W_OFF.get(name, (12, 0, "left")), 2.6)
x0, x1, y0, y1 = EUROPE
ax.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], ls=(0, (4, 3)), color="#6b7480", lw=1, zorder=4)
ax.annotate("Europe and Israel: see detail", (x1, y0), xytext=(6, -2), textcoords="offset points",
            fontsize=12, color=INK, path_effects=HALO_FX, va="top")
legend(fig, [0, 0, 1, 0.15], 6)
for ext in ("png", "svg"):
    fig.savefig(HERE / f"02_i02_map_world.{ext}", dpi=200, facecolor="white")
plt.close(fig)

# ---------------- Europe + Israel ----------------
E_OFF = {"Nanoscribe": (-12, 0, "right"), "UpNano": (12, 6, "left"), "Microlight3D": (12, 0, "left"),
         "Femtika": (12, 0, "left"), "Prusa Research": (12, 4, "left"),
         "Nano Dimension (ex Nanofabrica)": (-12, 4, "right"), "Stratasys (Rehovot)": (-12, -6, "right")}
fig = plt.figure(figsize=(6.48, 7.2))
ax = fig.add_axes([0, 0.1, 1, 0.9])
draw_base(ax, EUROPE[:2], EUROPE[2:], 1 / np.cos(np.radians(44)))
for name, m in makers.items():
    if in_eu(m):
        lab = "Stratasys" if name.startswith("Stratasys") else SHORT.get(name, name)
        draw_maker(ax, name, m, lab, E_OFF.get(name, (12, 0, "left")), 0.6)
legend(fig, [0, 0, 1, 0.09], 3)
for ext in ("png", "svg"):
    fig.savefig(HERE / f"02_i02_map_europe.{ext}", dpi=200, facecolor="white")
print("ok")
