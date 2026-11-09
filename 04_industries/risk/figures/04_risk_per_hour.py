"""Risk of death (or device event) per person per hour of exposure, grouped by the
categories of the deck (sports, medical, car, train, aviation, space) -> 04_risk_per_hour.png
Data: ../tables/04_risk_per_hour.csv  (orders of magnitude, see sources there)"""
import csv, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE.parent / "tables" / "04_risk_per_hour.csv", encoding="utf-8")))
ORDER = ["Sports", "Medical", "Car", "Train", "Aviation", "Space"]
LABEL = {"Car": "Car and road"}
COL = {"Sports": "#2a78d6", "Medical": "#eb6834", "Car": "#1baf7a", "Train": "#eda100", "Aviation": "#e87ba4", "Space": "#008300"}
INK, INK2, GRID, BG, BAND = "#1B2433", "#566170", "#DDD6C6", "#FBFAF7", "#F1EEE6"  # deck palette

plt.rcParams.update({"font.family": "Inter", "font.size": 12})
fig, ax = plt.subplots(figsize=(15.5, 7.4), dpi=200, facecolor=BG)
ax.set_facecolor(BG)
ax.set_xscale("log"); ax.set_xlim(5e-9, 3e-1)
y, ticks = 0, []
for k, cat in enumerate(ORDER):
    rs = sorted([r for r in rows if r["domain"] == cat], key=lambda r: -float(r["low_per_h"]))
    y0 = y
    for r in rs:
        lo, hi, c = float(r["low_per_h"]), float(r["high_per_h"]), COL[cat]
        hollow = r["kind"] != "death"
        ax.barh(y, hi - lo, left=lo, height=0.62, color=BG if hollow else c, edgecolor=c,
                lw=2.4 if hollow else 0, hatch="////" if hollow else None, zorder=3)
        ax.plot([lo, lo], [y - .31, y + .31], color=c, lw=2.6, zorder=4)
        ax.plot([hi, hi], [y - .31, y + .31], color=c, lw=2.6, zorder=4)
        ax.text(hi * 1.4, y, r["activity"], va="center", fontsize=15.5, color=INK, zorder=5)
        y -= 1
    if k % 2 == 0:
        ax.axhspan(y + 0.5, y0 + 0.5, color=BAND, zorder=0, lw=0)
    ax.text(3.6e-9, (y0 + y + 1) / 2, LABEL.get(cat, cat), ha="right", va="center", fontsize=17,
            fontweight="bold", color=COL[cat], transform=ax.transData, clip_on=False)
    y -= 0.5
for kk in (1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
    ax.axvline(kk, color=GRID, lw=0.8, zorder=1)
ax.axvline(1e-6, color=INK2, lw=1.6, ls=(0, (4, 3)), zorder=2)
ax.text(1.1e-6, 0.75, "everyday life: all-cause mortality ≈ 10⁻⁶ /h", fontsize=14, color=INK2, va="bottom")
ax.set_ylim(y + 0.3, 1.3)
ax.set_yticks([])
for s in ("left", "right", "top"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(INK2)
ax.tick_params(axis="x", colors=INK2, labelsize=15)
ax.set_xlabel("Risk per person per hour of exposure (log scale)", color=INK, fontsize=16)
ax.legend(handles=[Patch(facecolor=BG, edgecolor=COL["Medical"], hatch="////", label="device failure event, not a death")],
          loc="lower right", frameon=False, fontsize=14)
fig.subplots_adjust(left=0.135, right=0.98, top=0.97, bottom=0.11)
fig.savefig(HERE / "04_risk_per_hour.png", facecolor=BG)
