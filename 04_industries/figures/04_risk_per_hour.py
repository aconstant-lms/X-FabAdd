"""Risk of death (or device event) per person per hour of exposure -> 04_risk_per_hour.png
Data: ../tables/04_risk_per_hour.csv  (orders of magnitude, see sources there)"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE.parent / "tables" / "04_risk_per_hour.csv", encoding="utf-8")))
COL = {"Sports": "#2a78d6", "Medical": "#eb6834", "Car": "#1baf7a",
       "Train": "#eda100", "Aviation": "#e87ba4", "Space": "#008300"}
INK, INK2, GRID, BG = "#1B2433", "#566170", "#DDD6C6", "#FBFAF7"  # deck palette (AM slides)
rows.sort(key=lambda r: float(r["low_per_h"]) * float(r["high_per_h"]))

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=220, facecolor=BG)
ax.set_facecolor(BG)
ax.set_xscale("log"); ax.set_xlim(5e-9, 3e-2)
for k in (1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
    ax.axvline(k, color=GRID, lw=0.8, zorder=0)
# reference lines
ax.axvline(1e-6, color=INK2, lw=1.4, ls=(0, (4, 3)), zorder=1)
ax.text(1.08e-6, len(rows) - 0.35, "all-cause mortality, population average\n≈ 24 micromorts/day ≈ 10⁻⁶ /h",
        fontsize=9, color=INK2, va="top")
for i, r in enumerate(rows):
    lo, hi = float(r["low_per_h"]), float(r["high_per_h"])
    c = COL[r["domain"]]
    hollow = r["kind"] != "death"
    ax.barh(i, hi - lo, left=lo, height=0.56, color="white" if hollow else c,
            edgecolor=c, lw=2.2 if hollow else 0, hatch="////" if hollow else None, zorder=3)
    ax.plot([lo, lo], [i - 0.28, i + 0.28], color=c, lw=2.5, zorder=4)
    ax.plot([hi, hi], [i - 0.28, i + 0.28], color=c, lw=2.5, zorder=4)
    ax.text(hi * 1.35, i, r["activity"], va="center", fontsize=10.5, color=INK, zorder=5,
            bbox=dict(boxstyle="square,pad=0.1", fc=BG, ec="none"))
ax.set_yticks([]); ax.set_ylim(-0.7, len(rows) - 0.2)
for s in ("left", "right", "top"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(INK2)
ax.tick_params(axis="x", colors=INK2)
ax.set_xlabel("Risk per person per hour of exposure (log scale)", color=INK)
# legend
from matplotlib.patches import Patch
h = [Patch(color=c, label={"Car": "Road (car, bus, motorcycle)"}.get(d, d)) for d, c in COL.items()]
h.append(Patch(facecolor="white", edgecolor="#eb6834", hatch="////", label="device failure event (not a death)"))
ax.legend(handles=h, loc="lower right", frameon=False, fontsize=9.5, ncol=2)
fig.tight_layout()
fig.savefig(HERE / "04_risk_per_hour.png", facecolor=BG)
