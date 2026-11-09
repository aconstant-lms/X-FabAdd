"""02_i01 - Price vs voxel size of photopolymer printers (Ashby-style chart).

Reads ../tables/02_printers_price_voxel.csv and writes 02_i01_price_vs_voxel.png/.pdf.
Rows with plotted == 'yes' are drawn as points (price range = vertical bar);
rows with plotted == 'quote' are drawn in a strip "price on request" above the chart.
Family envelopes are drawn as soft bubbles in log space, after Ashby's material charts.
Usage: python 02_i01_price_vs_voxel.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull

from _printers_common import HERE, INK, GREY, GRID, TECH, COL, MRK, rows as load_rows, use_font, usd, is_lease

use_font()
FAMILIES = TECH
rows = load_rows()
pts = [r for r in rows if r["price_usd_low"]]
quotes = [r for r in rows if not r["price_usd_low"]]
NUDGE = {"Microlight3D Altraspin": 1.3}   # co-located with µFAB-3D at 0.2 µm: drawn slightly right

# label offsets (points) to avoid collisions; default right of the marker
OFF = {
    "Nanoscribe Quantum X": (10, 8), "Femtika Laser Nanofactory": (10, -8),
    "Microlight3D µFAB-3D": (6, -16), "Microlight3D Altraspin": (10, 0),
    "BMF microArch S240": (10, 0), "Carbon L1": (10, 0), "Formlabs Form 3L": (-10, 0, "right"), "Elegoo Saturn 4 Ultra 16K": (10, -2),
    "Prusa SL1S Speed": (-10, 0, "right"), "Formlabs Form 4": (10, -6),
    "Formlabs Form 4L": (-10, -9, "right"), "Asiga MAX 2": (10, -10),
    "Asiga MAX X35": (-10, 10, "right"), "Stratasys Origin One": (-10, 0, "right"),
    "Carbon M1": (10, 0), "Carbon M3": (-10, -2, "right"), "Carbon M3 Max": (-10, 8, "right"),
    "UnionTech RSPro 600": (10, -12), "3D Systems SLA 750": (10, 0),
}

fig = plt.figure(figsize=(13, 8.6))
ax = fig.add_axes([0.08, 0.09, 0.62, 0.72])
axq = fig.add_axes([0.08, 0.83, 0.62, 0.07], sharex=ax)

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.05, 600); ax.set_ylim(250, 2e6)
ax.grid(True, which="major", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xlabel("Voxel size: lateral resolution / pixel / beam spot  (µm, log scale)")
ax.set_ylabel("Machine price  (USD, log scale)")
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda v, _: f"{v:g}"))
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda v, _: f"${v/1e6:g}M" if v >= 1e6 else (f"${v/1e3:g}k" if v >= 1e3 else f"${v:g}")))

ax.axvline(1, color=GRID, lw=2, zorder=0)
ax.axvline(100, color=GRID, lw=2, zorder=0)
ax.text(0.22, 1.35e6, "sub-micrometre", color=GREY, ha="center", style="italic")
ax.text(10, 1.35e6, "micrometre", color=GREY, ha="center", style="italic")
ax.text(245, 1.35e6, "≥ 0.1 mm", color=GREY, ha="center", style="italic")


def logxy(r):
    x = float(r["voxel_xy_um"]) * NUDGE.get(r["printer"], 1.0)
    lo, hi = float(r["price_usd_low"]), float(r["price_usd_high"])
    return x, lo, hi, np.sqrt(lo * hi)


# Ashby bubbles: convex hull of each family's points (incl. price-range ends), padded in log space
for fam, c, _ in FAMILIES:
    P = []
    for r in pts:
        if r["technology"] != fam:
            continue
        x, lo, hi, _m = logxy(r)
        P += [(np.log10(x), np.log10(lo)), (np.log10(x), np.log10(hi))]
    P = np.array(P)
    ang = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    ring = np.c_[0.17 * np.cos(ang), 0.19 * np.sin(ang)]
    cloud = (P[:, None, :] + ring[None, :, :]).reshape(-1, 2)
    hull = cloud[ConvexHull(cloud).vertices]
    ax.add_patch(Polygon(10 ** hull, closed=True, fc=c, ec=c, alpha=0.13, lw=0, zorder=1))
    ax.add_patch(Polygon(10 ** hull, closed=True, fc="none", ec=c, alpha=0.7, lw=1.2, zorder=1))

for r in pts:
    fam = r["technology"]; c = COL[fam]
    x, lo, hi, m = logxy(r)
    lease = is_lease(r)
    if hi > lo * 1.01:
        ax.plot([x, x], [lo, hi], color=c, lw=2, solid_capstyle="round", zorder=3)
    ax.scatter([x], [m], s=70, marker=MRK[fam], zorder=4,
               facecolor="white" if lease else c, edgecolor=c if lease else "white",
               linewidth=2 if lease else 1.5)
    o = OFF.get(r["printer"], (10, 0))
    ha = o[2] if len(o) > 2 else "left"
    ax.annotate(r["printer"], (x, m), xytext=o[:2], textcoords="offset points",
                ha=ha, va="center", fontsize=11, color=INK, zorder=5)

# quote-only strip
axq.set_xscale("log"); axq.set_ylim(0, 1); axq.set_yticks([])
for s in ("top", "right", "left"):
    axq.spines[s].set_visible(False)
axq.tick_params(axis="x", labelbottom=False)
axq.text(0.0, 1.25, "Price on request (not plotted below)", transform=axq.transAxes,
         color=GREY, fontsize=12, style="italic")
QOFF = {"UpNano NanoOne 1000": (0.45, "left"), "Nano Dimension Fabrica Tera 250": (0.45, "left")}
for r in quotes:
    x = float(r["voxel_xy_um"]); fam = r["technology"]
    axq.scatter([x], [QOFF[r["printer"]][0]], s=60, marker=MRK[fam], facecolor="white",
                edgecolor=COL[fam], linewidth=1.8, zorder=3)
    dx = 8 if QOFF[r["printer"]][1] == "left" else -8
    axq.annotate(r["printer"], (x, QOFF[r["printer"]][0]), xytext=(dx, 0),
                 textcoords="offset points", ha=QOFF[r["printer"]][1], va="center",
                 fontsize=11, color=INK)

ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
ax.set_xticks([0.1, 1, 10, 100])

# legend + notes on the right
lx = fig.add_axes([0.73, 0.09, 0.26, 0.81]); lx.axis("off")
lx.text(0, 1.0, "Photopolymer printers", fontsize=16, color=INK, weight="bold", va="top")
lx.text(0, 0.955, "machine price vs voxel size", fontsize=14, color=GREY, va="top")
y = 0.88
for fam, c, mk in FAMILIES:
    lx.scatter([0.03], [y], s=80, marker=mk, color=c, edgecolor="white", transform=lx.transAxes)
    lx.text(0.09, y, fam, va="center", fontsize=13, color=INK, transform=lx.transAxes)
    y -= 0.048
y -= 0.015
lx.plot([0.03, 0.03], [y - 0.02, y + 0.02], color=GREY, lw=2, transform=lx.transAxes)
lx.text(0.09, y, "price range", va="center", fontsize=12, color=GREY, transform=lx.transAxes)
y -= 0.05
lx.scatter([0.03], [y], s=70, marker="^", facecolor="white", edgecolor=GREY, linewidth=2,
           transform=lx.transAxes)
lx.text(0.09, y, "open marker: lease / subscription,\n3-year total", va="center",
        fontsize=12, color=GREY, transform=lx.transAxes)
y -= 0.08
lx.text(0, y, "Bubbles: technology envelopes,\nafter Ashby's material-property charts.",
        va="top", fontsize=12, color=GREY, transform=lx.transAxes)
lx.text(0, 0.0,
        "Voxel size = smallest lateral feature:\n"
        "2PP/MPP: focal-spot resolution; PµSL, DLP,\n"
        "MSLA: projected pixel; laser SLA: beam spot\n"
        "(UnionTech: min. layer as proxy).\n\n"
        "Prices: list/launch prices (USD) as published\n"
        "by vendors, dealers, all3dp and aniwaa;\n"
        "EUR at 1.16 USD. Altraspin nudged right\n"
        "(same 0.2 µm as µFAB-3D).\n\n"
        "Data: tables/02_printers_price_voxel.csv\n"
        "Micro rows after all3dp, Micro 3D printing guide.",
        va="bottom", fontsize=10.5, color=GREY, transform=lx.transAxes, linespacing=1.3)

for ext in ("png", "pdf"):
    fig.savefig(HERE / f"02_i01_price_vs_voxel.{ext}", dpi=200, facecolor="white")
print("ok")
