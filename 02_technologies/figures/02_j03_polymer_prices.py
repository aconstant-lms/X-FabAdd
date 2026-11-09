"""02_j03 - Typical price per kg of printable polymer feedstocks (range bars, log scale).

Reads ../tables/02_polymer_prices_makers.csv. Resins sold per litre are converted with a
density of 1.1 kg/L. EUR and GBP taken at par with USD at this resolution (log scale).
Usage: python 02_j03_polymer_prices.py
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from _printers_common import HERE, INK, GREY, GRID, use_font

use_font()
COL = {"MEX": "#eb6834", "PBF": "#eda100", "VPP": "#1baf7a", "2PP / MPP": "#2a78d6"}
rows = [r for r in csv.DictReader(open(HERE.parent / "tables" / "02_polymer_prices_makers.csv", encoding="utf-8"))]
data = []
for r in rows:
    if not r["price_low"]:
        continue
    lo, hi = float(r["price_low"]), float(r["price_high"])
    if r["unit"] == "L":
        lo, hi = lo / 1.1, hi / 1.1
    data.append((r["material"], r["process"], lo, hi, r["price_basis"]))
data.sort(key=lambda d: np.sqrt(d[2] * d[3]))

fig = plt.figure(figsize=(13, 7.2))
ax = fig.add_axes([0.25, 0.12, 0.5, 0.8])
ax.set_xscale("log"); ax.set_xlim(5, 1500)
ax.grid(True, axis="x", which="major", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g} $"))
ax.set_xlabel("Price per kg of feedstock  (USD or EUR, log scale)")
ax.set_yticks([]); ax.set_ylim(-0.7, len(data) - 0.3)
for i, (m, p, lo, hi, basis) in enumerate(data):
    c = COL[p]
    ax.plot([lo, hi], [i, i], color=c, lw=12, solid_capstyle="round", alpha=0.85)
    ax.text(4.3, i, m, ha="right", va="center", fontsize=13, color=INK, transform=ax.transData)
    ax.text(hi * 1.15, i, f"{lo:.0f}–{hi:.0f}", ha="left", va="center", fontsize=11.5, color=GREY)
# reference: base polymer pellets
ax.axvspan(5, 20, color="#e9e6df", zorder=0)
ax.text(10, len(data) - 0.55, "bulk pellets\nPA12 ≈ 18–22 $/kg", ha="center", va="top", fontsize=10.5, color=GREY, style="italic")
lx = fig.add_axes([0.79, 0.12, 0.2, 0.8]); lx.axis("off")
lx.text(0, 1.0, "Printable polymers:\nprice per kg", fontsize=15, weight="bold", color=INK, va="top", transform=lx.transAxes)
y = 0.82
for p, c in [(k, v) for k, v in COL.items() if k != "2PP / MPP"]:
    lx.plot([0.0, 0.1], [y, y], color=c, lw=10, solid_capstyle="round", transform=lx.transAxes)
    lx.text(0.15, y, {"MEX": "filament (MEX)", "PBF": "powder (PBF)", "VPP": "resin (VPP)", "2PP / MPP": "2PP resin"}[p],
            va="center", fontsize=12.5, color=INK, transform=lx.transAxes)
    y -= 0.07
lx.text(0, 0.0, "Retail and bulk prices 2025-2026 from\nmakers and resellers; resins at\n1.1 kg/L; EUR and GBP at par with USD\n"
        "on this log scale. 2PP photoresins\n(IP-S, OrmoComp, SU-8): small bottles,\nprice on request.\n\n"
        "Data: tables/02_polymer_prices_makers.csv", va="bottom", fontsize=10.5, color=GREY,
        transform=lx.transAxes, linespacing=1.3)
for ext in ("png", "pdf"):
    fig.savefig(HERE / f"02_j03_polymer_prices.{ext}", dpi=200, facecolor="white")
print("ok")
