"""02_j04 - Who makes the printable polymers: world strip (numbered) and Europe panel (labelled),
in the layout of the aviation map slide. Ring colour = role: base-polymer producer, filament,
powder, resin, 2PP photoresin. Writes 02_j04_map_world_numbered.png/.svg and
02_j04_map_europe_labels.png/.svg. The numbered list is set in the slide.
Usage: python 02_j04_polymer_makers_map.py
"""
import warnings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import geopandas as gpd
from _printers_common import HERE, use_font

warnings.filterwarnings("ignore")
use_font("Inter", 14)
matplotlib.rcParams["svg.fonttype"] = "none"
SEA, LAND, COAST, INK, HALO, FILL = "#dfe6ee", "#cbc4b4", "#b3ab98", "#1b2433", "#eef2f6", "#fbfaf7"
ROLE = {"polymer": "#566170", "filament": "#eb6834", "powder": "#eda100", "resin": "#1baf7a", "2PP resin": "#2a78d6"}
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres")); world = world[world["continent"] != "Antarctica"]

# (n, name, role, lon, lat, ring offset deg)
WORLD = [(1, "NatureWorks", "polymer", -93.45, 44.98, (0, 0)), (2, "Lubrizol", "polymer", -81.47, 41.60, (0, 0)),
         (3, "Formlabs", "resin", -71.10, 42.39, (6, 4)), (4, "Kayaku AM", "2PP resin", -71.62, 42.27, (4, -6)),
         (5, "SABIC", "polymer", 46.68, 24.71, (0, 0)), (6, "Polymaker", "filament", 120.75, 31.65, (6, 4)),
         (7, "eSUN", "filament", 114.06, 22.54, (0, 0))]
EUROPE = [("Arkema", "polymer", 2.25, 48.92, (-14, 0), "right"), ("Evonik", "powder", 7.01, 51.46, (0, 20), "center"),
          ("Henkel Loctite", "resin", 6.78, 51.23, (14, 2), "left"), ("Forward AM (BASF)", "filament", 8.67, 49.40, (-14, 6), "right"),
          ("Nanoscribe", "2PP resin", 8.40, 49.09, (-14, -14), "right"), ("Victrex", "polymer", -3.02, 53.87, (14, 0), "left"),
          ("Syensqo", "polymer", 4.35, 50.85, (-14, 0), "right"), ("TotalEnergies Corbion", "polymer", 4.97, 51.83, (-14, 8), "right"),
          ("EOS", "powder", 11.40, 48.10, (14, -4), "left"), ("Prusa Polymers", "filament", 14.44, 50.08, (14, 0), "left"),
          ("micro resist\ntechnology", "2PP resin", 13.40, 52.52, (14, 0), "left")]
NUDGE = {"Henkel Loctite": (-0.3, -0.25), "Nanoscribe": (-0.25, -0.2), "Forward AM (BASF)": (0.2, 0.15)}

fig = plt.figure(figsize=(10.4, 3.26)); ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(SEA); world.plot(ax=ax, color=LAND, edgecolor=COAST, linewidth=0.5)
ax.set_xlim(-130, 150); ax.set_ylim(-8, 70); ax.set_aspect("auto"); ax.axis("off")
x0, x1, y0, y1 = -11, 20, 42, 58
ax.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], ls=(0, (4, 3)), color="#6b7480", lw=1, zorder=4)
for n, name, role, lon, lat, (dx, dy) in WORLD:
    x, y = lon + dx, lat + dy
    if (dx, dy) != (0, 0):
        ax.plot([lon, x], [lat, y], color=INK, lw=1.4, zorder=4); ax.scatter([lon], [lat], s=20, color=INK, zorder=4)
    ax.scatter([x], [y], s=470, facecolor=FILL, edgecolor=ROLE[role], linewidth=2.2, zorder=5)
    ax.text(x, y - 0.3, str(n), ha="center", va="center", fontsize=12.5, fontweight="bold", color=ROLE[role], zorder=6)
for ext in ("png", "svg"):
    fig.savefig(HERE / f"02_j04_map_world_numbered.{ext}", dpi=200, facecolor=SEA)
plt.close(fig)

fig = plt.figure(figsize=(6.0, 7.05)); ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(SEA); world.plot(ax=ax, color=LAND, edgecolor=COAST, linewidth=0.6)
asp = 1 / np.cos(np.radians(51)); lon0, lon1 = -9.0, 24.0
h = (lon1 - lon0) / asp * 7.05 / 6.0
ax.set_xlim(lon0, lon1); ax.set_ylim(50.2 - h / 2, 50.2 + h / 2); ax.set_aspect(asp); ax.axis("off")
for name, role, lon, lat, (ox, oy), ha in EUROPE:
    dx, dy = NUDGE.get(name, (0, 0))
    ax.scatter([lon + dx], [lat + dy], s=135, facecolor=FILL, edgecolor=ROLE[role], linewidth=2.2, zorder=5)
    ax.annotate(name, (lon + dx, lat + dy), xytext=(ox, oy), textcoords="offset points", ha=ha, va="center", fontsize=13,
                fontweight="semibold", color=INK, zorder=6, path_effects=[pe.withStroke(linewidth=3.6, foreground=HALO)])
for ext in ("png", "svg"):
    fig.savefig(HERE / f"02_j04_map_europe_labels.{ext}", dpi=200, facecolor=SEA)
print("ok")
