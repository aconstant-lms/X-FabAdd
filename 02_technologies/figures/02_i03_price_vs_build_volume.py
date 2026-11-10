"""02_i03 - Price vs build volume of photopolymer printers (Ashby-style chart).

Reads ../tables/02_printers_price_voxel.csv, writes 02_i03_price_vs_build_volume.png/.pdf.
Points: plotted == 'yes' (price range = vertical bar, open marker = lease/subscription).
Strip on top: plotted == 'quote' (price on request) at their build volume.
Dashed guide lines: constant price per litre of build volume (Ashby 'design index' lines).
Usage: python 02_i03_price_vs_build_volume.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.ticker import FuncFormatter
from scipy.spatial import ConvexHull

from _printers_common import HERE, INK, GREY, GRID, TECH, COL, MRK, rows, use_font, usd, is_lease

use_font()
R = rows()
pts = [r for r in R if r["plotted"] == "yes"]
quotes = [r for r in R if r["plotted"] == "quote"]

# label offsets in points: (dx, dy[, ha])
OFF = {
    "Nanoscribe Quantum X": (10, 0), "Microlight3D µFAB-3D": (10, 0),
    "Microlight3D Altraspin": (6, -22), "BMF microArch S240": (-12, 0, "right"),
    "Asiga MAX X35": (-10, 0, "right"), "Asiga MAX 2": (10, 0),
    "Stratasys Origin One": (-10, 0, "right"), "Elegoo Saturn 4 Ultra 16K": (10, 0),
    "Prusa SL1S Speed": (-10, 0, "right"), "Formlabs Form 4": (-10, 0, "right"),
    "Formlabs Form 4L": (10, -2), "Formlabs Form 3L": (-10, 0, "right"),
    "Carbon M1": (-10, 0, "right"), "Carbon M3": (10, -7),
    "Carbon M3 Max": (-10, 10, "right"), "Carbon L1": (10, 4),
    "UnionTech RSPro 600": (4, -40, "right"), "3D Systems SLA 750": (-10, 6, "right"),
}

fig = plt.figure(figsize=(13, 8.6))
ax = fig.add_axes([0.085, 0.09, 0.615, 0.72])
axq = fig.add_axes([0.085, 0.83, 0.615, 0.07], sharex=ax)
ax.set_xscale("log"); ax.set_yscale("log")
XL, YL = (0.05, 2e6), (250, 3e6)
ax.set_xlim(*XL); ax.set_ylim(*YL)
ax.grid(True, which="major", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xlabel("Build volume  (cm³ up to 100, then litres; log scale)")
ax.set_ylabel("Machine price  (USD, log scale)")
ax.yaxis.set_major_formatter(FuncFormatter(usd))

# Ashby guide lines: price = k x volume  (k in USD per litre)
xs = np.logspace(np.log10(XL[0]), np.log10(XL[1]), 50)
GUIDES = [(1e2, 4e5), (1e4, 40), (1e6, 0.5), (1e8, 0.075)]
for k, _x in GUIDES:
    ax.plot(xs, k * xs / 1000.0, ls=(0, (5, 4)), color="#b9b4a8", lw=1, zorder=0)


def label_guides():
    fig.canvas.draw()
    for k, lx_ in GUIDES:
        ly = k * lx_ / 1000.0
        a = ax.transData.transform([(lx_, ly), (lx_ * 10, ly * 10)])
        ang = np.degrees(np.arctan2(a[1, 1] - a[0, 1], a[1, 0] - a[0, 0]))
        ax.annotate(f"{usd(k)} per litre", (lx_, ly), xytext=(-4, 5), textcoords="offset points",
                    rotation=ang, rotation_mode="anchor", color="#8f8a7e", fontsize=10.5,
                    ha="left", va="bottom", style="italic")


def xy(r):
    v = float(r["build_volume_cm3"]); lo, hi = float(r["price_usd_low"]), float(r["price_usd_high"])
    return v, lo, hi, np.sqrt(lo * hi)


# technology envelopes (Ashby bubbles)
for tech, c, _ in TECH:
    P = []
    for r in pts:
        if r["technology"] == tech:
            v, lo, hi, _m = xy(r)
            P += [(np.log10(v), np.log10(lo)), (np.log10(v), np.log10(hi))]
    if not P:
        continue
    P = np.array(P)
    ang = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    ring = np.c_[0.2 * np.cos(ang), 0.17 * np.sin(ang)]
    cloud = (P[:, None, :] + ring[None, :, :]).reshape(-1, 2)
    hull = cloud[ConvexHull(cloud).vertices]
    ax.add_patch(Polygon(10 ** hull, closed=True, fc=c, ec="none", alpha=0.13, zorder=1))
    ax.add_patch(Polygon(10 ** hull, closed=True, fc="none", ec=c, alpha=0.75, lw=1.2, zorder=1))

for r in pts:
    t = r["technology"]; c = COL[t]
    v, lo, hi, m = xy(r)
    if hi > lo * 1.01:
        ax.plot([v, v], [lo, hi], color=c, lw=2, solid_capstyle="round", zorder=3)
    lease = is_lease(r)
    ax.scatter([v], [m], s=72, marker=MRK[t], zorder=4,
               facecolor="white" if lease else c, edgecolor=c if lease else "white",
               linewidth=2 if lease else 1.5)
    o = OFF.get(r["printer"], (10, 0))
    ax.annotate(r["printer"], (v, m), xytext=o[:2], textcoords="offset points",
                ha=o[2] if len(o) > 2 else "left", va="center", fontsize=11, color=INK, zorder=5)

# quote-only strip
axq.set_ylim(0, 1); axq.set_yticks([])
for s in ("top", "right", "left"):
    axq.spines[s].set_visible(False)
axq.tick_params(axis="x", labelbottom=False)
axq.text(0, 1.25, "Price on request (build volume known)", transform=axq.transAxes,
         color=GREY, fontsize=12, style="italic")
QPOS = {"Nano Dimension Fabrica Tera 250": (0.7, -8, "right"), "UpNano NanoOne 1000": (0.25, 8, "left")}
for r in quotes:
    v = float(r["build_volume_cm3"]); t = r["technology"]
    yq, dxq, haq = QPOS.get(r["printer"], (0.45, 8, "left"))
    axq.scatter([v], [yq], s=62, marker=MRK[t], facecolor="white", edgecolor=COL[t],
                linewidth=1.8, zorder=3)
    axq.annotate(r["printer"], (v, yq), xytext=(dxq, 0), textcoords="offset points",
                 ha=haq, va="center", fontsize=11, color=INK)
VLAB = {0.1: "0.1", 1: "1", 10: "10", 100: "100", 1e3: "1 L", 1e4: "10 L", 1e5: "100 L", 1e6: "1 m³"}
ax.set_xticks(list(VLAB)); ax.set_xticklabels(list(VLAB.values()))

# legend + notes
lx = fig.add_axes([0.725, 0.09, 0.27, 0.81]); lx.axis("off")
lx.text(0, 1.0, "Photopolymer printers", fontsize=16, color=INK, weight="bold", va="top")
lx.text(0, 0.955, "machine price vs build volume", fontsize=14, color=GREY, va="top")
y = 0.88
for t, c, mk in TECH:
    lx.scatter([0.03], [y], s=80, marker=mk, color=c, edgecolor="white", transform=lx.transAxes)
    lx.text(0.09, y, t, va="center", fontsize=13, color=INK, transform=lx.transAxes)
    y -= 0.048
y -= 0.015
lx.plot([0.03, 0.03], [y - 0.02, y + 0.02], color=GREY, lw=2, transform=lx.transAxes)
lx.text(0.09, y, "price range", va="center", fontsize=12, color=GREY, transform=lx.transAxes)
y -= 0.05
lx.scatter([0.03], [y], s=70, marker="^", facecolor="white", edgecolor=GREY, linewidth=2,
           transform=lx.transAxes)
lx.text(0.09, y, "open marker: lease / subscription,\n3-year total", va="center",
        fontsize=12, color=GREY, transform=lx.transAxes)
y -= 0.075
lx.plot([0.0, 0.07], [y, y], ls=(0, (5, 4)), color="#b9b4a8", transform=lx.transAxes)
lx.text(0.09, y, "constant price per litre", va="center", fontsize=12, color=GREY,
        transform=lx.transAxes)
lx.text(0, 0.0,
        "Bubbles: technology envelopes (after Ashby).\n"
        "Build volume = maximum build envelope (W x D x H;\n"
        "Microlight3D µFAB-3D: cylinder dia. 3 x 20 mm).\n"
        "Prices: list/launch prices in USD published by\n"
        "vendors, dealers, all3dp and aniwaa, 2019-2025;\n"
        "EUR at 1.16 USD. BMF bar = microArch line range.\n"
        "Carbon: 3-year subscription totals, two of them\n"
        "from competitors' comparison pages.\n"
        "Femtika Laser Nanofactory (USD 415k, aniwaa)\n"
        "not plotted: modular stage, no build volume.\n\n"
        "Data: tables/02_printers_price_voxel.csv",
        va="bottom", fontsize=10, color=GREY, transform=lx.transAxes, linespacing=1.25)

label_guides()
for ext in ("png", "pdf"):
    fig.savefig(HERE / f"02_i03_price_vs_build_volume.{ext}", dpi=200, facecolor="white")
print("ok")
