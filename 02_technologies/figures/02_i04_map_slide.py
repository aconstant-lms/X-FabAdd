"""02_i04 - Maps for the 'origin of the makers' slide, in the layout of the aviation map
slide (04 Industries, 'Machine makers worldwide'): a numbered world strip (1040 x 326) and a
labelled Europe panel (600 x 705). Ring colour = technology (palette of 02_i01-02_i03).
Writes 02_i04_map_world_numbered.png and 02_i04_map_europe_labels.png (+ .svg).
The numbered list itself is set in the slide (HTML), from WORLD below.
Usage: python 02_i04_map_slide.py
"""
import warnings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import geopandas as gpd

from _printers_common import HERE, COL, use_font

warnings.filterwarnings("ignore")
use_font("Inter", 14)
matplotlib.rcParams["svg.fonttype"] = "none"
SEA, LAND, COAST, INK, HALO, FILL = "#dfe6ee", "#cbc4b4", "#b3ab98", "#1b2433", "#eef2f6", "#fbfaf7"
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world = world[world["continent"] != "Antarctica"]

# (number, name, city, technologies, lon, lat, ring offset in degrees for co-located HQs)
WORLD = [
    (1, "Carbon", "Redwood City, US", ["CLIP / DLS"], -122.24, 37.49, (0, 0)),
    (2, "Formlabs", "Somerville, US", ["MSLA (LCD)", "laser SLA"], -71.10, 42.39, (0, 0)),
    (3, "3D Systems", "Rock Hill, US", ["laser SLA"], -81.03, 34.93, (0, 0)),
    (4, "Stratasys", "Eden Prairie, US / Rehovot, Israel", ["DLP"], -93.47, 44.86, (0, 0)),
    (5, "BMF", "Shenzhen, China", ["PµSL (micro-DLP)"], 114.06, 22.54, (9, -6)),
    (6, "Elegoo", "Shenzhen, China", ["MSLA (LCD)"], 113.95, 22.55, (-9, -7)),
    (7, "UnionTech", "Shanghai, China", ["laser SLA"], 121.47, 31.23, (6, 5)),
    (8, "Asiga", "Sydney, Australia", ["DLP"], 151.20, -33.91, (0, 0)),
]
EUROPE = [  # name, technologies, lon, lat, label offset (points), ha
    ("Nanoscribe", ["2PP / MPP"], 8.40, 49.09, (-14, 0), "right"),
    ("UpNano", ["2PP / MPP"], 16.37, 48.21, (14, -6), "left"),
    ("Microlight3D", ["2PP / MPP"], 5.72, 45.19, (14, 0), "left"),
    ("Femtika", ["2PP / MPP"], 25.28, 54.69, (14, 0), "left"),
    ("Prusa", ["MSLA (LCD)"], 14.44, 50.08, (14, 6), "left"),
    ("Nano Dimension", ["PµSL (micro-DLP)"], 34.80, 31.93, (-14, 8), "right"),
    ("Stratasys", ["DLP"], 34.81, 31.89, (-14, -10), "right"),
]

# ---------------- world strip, numbered rings
fig = plt.figure(figsize=(10.4, 3.26))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(SEA); world.plot(ax=ax, color=LAND, edgecolor=COAST, linewidth=0.5)
ax.set_xlim(-150, 172); ax.set_ylim(-44, 66); ax.set_aspect("auto"); ax.axis("off")
for n, name, city, techs, lon, lat, (dx, dy) in WORLD:
    x, y = lon + dx, lat + dy
    if (dx, dy) != (0, 0):
        ax.plot([lon, x], [lat, y], color=INK, lw=1.4, zorder=4)
        ax.scatter([lon], [lat], s=20, color=INK, zorder=4)
    k = len(techs)
    for i, t in enumerate(techs):          # two technologies: two rings side by side
        xi = x + (i - (k - 1) / 2) * 7.5
        ax.scatter([xi], [y], s=470, facecolor=FILL, edgecolor=COL[t], linewidth=2.2, zorder=5)
        ax.text(xi, y - 0.3, str(n), ha="center", va="center", fontsize=12.5, fontweight="bold",
                color=COL[t], zorder=6)
for ext in ("png", "svg"):
    fig.savefig(HERE / f"02_i04_map_world_numbered.{ext}", dpi=200, facecolor=SEA)
plt.close(fig)

# ---------------- Europe panel, labelled rings
fig = plt.figure(figsize=(6.0, 7.05))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(SEA); world.plot(ax=ax, color=LAND, edgecolor=COAST, linewidth=0.6)
asp = 1 / np.cos(np.radians(44))
lon0, lon1 = -3.0, 39.0
h = (lon1 - lon0) / asp * 7.05 / 6.0
ax.set_xlim(lon0, lon1); ax.set_ylim(43.5 - h / 2 - 1.5, 43.5 + h / 2 - 1.5); ax.set_aspect(asp); ax.axis("off")
for name, techs, lon, lat, (ox, oy), ha in EUROPE:
    ax.scatter([lon], [lat + (0.25 if name == "Nano Dimension" else -0.25 if name == "Stratasys" else 0)],
               s=135, facecolor=FILL, edgecolor=COL[techs[0]], linewidth=2.2, zorder=5)
    ax.annotate(name, (lon, lat), xytext=(ox, oy), textcoords="offset points", ha=ha, va="center",
                fontsize=14, fontweight="semibold", color=INK, zorder=6,
                path_effects=[pe.withStroke(linewidth=3.6, foreground=HALO)])
for ext in ("png", "svg"):
    fig.savefig(HERE / f"02_i04_map_europe_labels.{ext}", dpi=200, facecolor=SEA)
print("ok")
