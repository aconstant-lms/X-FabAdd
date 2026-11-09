"""02_j02 - Ashby chart of printable polymers: Young's modulus vs tensile strength.

Reads ../tables/02_polymers_ashby.csv (one ellipse per material class, spanning its
E and strength ranges in log space), colour = printing process. Dashed lines: constant
strain at failure sigma/E (Ashby's yield-strain guide lines).
Usage: python 02_j02_polymer_ashby_E_strength.py
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from matplotlib.ticker import FuncFormatter

from _printers_common import HERE, INK, GREY, GRID, use_font

use_font()
PROC = [("2PP / MPP", "#2a78d6"), ("VPP", "#1baf7a"), ("MEX", "#eb6834"), ("PBF", "#eda100")]
COL = dict(PROC)
rows = [r for r in csv.DictReader(open(HERE.parent / "tables" / "02_polymers_ashby.csv", encoding="utf-8"))
        if r["sigma_MPa_low"]]

fig = plt.figure(figsize=(13, 8.6))
ax = fig.add_axes([0.075, 0.1, 0.47, 0.84])
az = fig.add_axes([0.63, 0.1, 0.355, 0.52])
XL, YL = (5e-6, 30), (0.008, 400)
ZX, ZY = (1.0, 16), (25, 180)
fmt = lambda v, _: (f"{v:g}" if v >= 0.01 else f"$10^{{{int(round(np.log10(v)))}}}$")
for a_, xl, yl in ((ax, XL, YL), (az, ZX, ZY)):
    a_.set_xscale("log"); a_.set_yscale("log"); a_.set_xlim(*xl); a_.set_ylim(*yl)
    a_.grid(True, which="major", color=GRID, lw=0.8); a_.set_axisbelow(True)
    for sp in ("top", "right"):
        a_.spines[sp].set_visible(False)
    a_.xaxis.set_major_formatter(FuncFormatter(fmt)); a_.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
az.xaxis.set_minor_formatter(FuncFormatter(lambda v, _: f"{v:g}" if v in (2, 3, 5) else ""))
az.yaxis.set_minor_formatter(FuncFormatter(lambda v, _: f"{v:g}" if round(v) in (30, 50, 150) else ""))
ax.set_xlabel("Young's modulus E  (GPa, log scale)")
ax.set_ylabel("Tensile strength $\\sigma$  (MPa, log scale)")
az.set_xlabel("E (GPa)", fontsize=12); az.set_ylabel("$\\sigma$ (MPa)", fontsize=12)
az.set_title("Rigid polymers, zoomed", fontsize=13, color=GREY, style="italic", loc="left")
# zoom frame on the main chart
ax.add_patch(plt.Rectangle((ZX[0], ZY[0]), ZX[1] - ZX[0], ZY[1] - ZY[0], fill=False, ec=GREY, lw=0.9, ls=(0, (3, 2)), zorder=6))

# guide lines: sigma = eps * E  (sigma in MPa, E in GPa)
fig.canvas.draw()
def guides(a_, xl, yl, spots):
    xs = np.logspace(np.log10(xl[0]), np.log10(xl[1]), 50)
    for eps, lab_x in spots:
        a_.plot(xs, eps * 1000 * xs, ls=(0, (5, 4)), color="#b9b4a8", lw=1, zorder=0)
        ly = eps * 1000 * lab_x
        if yl[0] < ly < yl[1] and xl[0] < lab_x < xl[1]:
            t = a_.transData.transform([(lab_x, ly), (lab_x * 10, ly * 10)])
            ang = np.degrees(np.arctan2(t[1, 1] - t[0, 1], t[1, 0] - t[0, 0]))
            a_.annotate(f"$\\sigma$/E = {eps*100:g} %", (lab_x, ly), xytext=(-2, 4), textcoords="offset points",
                        rotation=ang, rotation_mode="anchor", color="#8f8a7e", fontsize=10.5, style="italic")
guides(ax, XL, YL, [(0.001, 2.0), (0.01, 0.12), (0.1, 0.004), (1, 0.0003), (10, 0.00002)])
guides(az, ZX, ZY, [(0.01, 4.0), (0.02, 2.0), (0.05, 1.05)])

from scipy.spatial import ConvexHull
def env(sel, label, lxy):
    P = []
    for r in rows:
        if r["family"] in sel:
            for e in (float(r["E_GPa_low"]), float(r["E_GPa_high"])):
                for s_ in (float(r["sigma_MPa_low"]), float(r["sigma_MPa_high"])):
                    P.append((np.log10(e), np.log10(s_)))
    P = np.array(P)
    ang = np.linspace(0, 2 * np.pi, 30, endpoint=False)
    cloud = (P[:, None, :] + np.c_[0.45 * np.cos(ang), 0.35 * np.sin(ang)][None]).reshape(-1, 2)
    h = cloud[ConvexHull(cloud).vertices]
    ax.add_patch(Polygon(10 ** h, closed=True, fc="#7a8794", ec="none", alpha=0.07, zorder=0))
    ax.add_patch(Polygon(10 ** h, closed=True, fc="none", ec="#7a8794", lw=1, ls=(0, (2, 2)), alpha=0.6, zorder=0))
    ax.text(*lxy, label, color=GREY, fontsize=13, style="italic", ha="center")
env({"hydrogel"}, "hydrogels", (2e-5, 0.25))
env({"elastomer"}, "elastomers", (0.0012, 40))
env({"thermoplastic", "thermoset", "composite"}, "rigid polymers", (0.3, 250))

def blobs(a_, labels, pad_w, pad_h, zorder=3):
    area = lambda r: (np.log10(float(r['E_GPa_high'])/float(r['E_GPa_low']))+pad_w)*(np.log10(float(r['sigma_MPa_high'])/float(r['sigma_MPa_low']))+pad_h)
    for r in sorted(rows, key=area, reverse=True):
        e0, e1 = np.log10(float(r["E_GPa_low"])), np.log10(float(r["E_GPa_high"]))
        s0, s1 = np.log10(float(r["sigma_MPa_low"])), np.log10(float(r["sigma_MPa_high"]))
        proc = "2PP / MPP" if r["process"] == "2PP / MPP" else r["process"].split(" / ")[0]
        c = COL[proc]
        cx, cy = (e0 + e1) / 2, (s0 + s1) / 2
        w, h = (e1 - e0) + pad_w, (s1 - s0) + pad_h
        t = np.linspace(0, 2 * np.pi, 80)
        poly = np.c_[10 ** (cx + w / 2 * np.cos(t)), 10 ** (cy + h / 2 * np.sin(t))]
        dark = matplotlib.colors.to_hex(np.array(matplotlib.colors.to_rgb(c)) * 0.7)
        a_.add_patch(Polygon(poly, closed=True, fc=c, ec=dark, alpha=0.5, lw=1.2, zorder=zorder))
        if r["material"] in labels:
            dx, dy, ha = labels[r["material"]]
            a_.annotate(r["material"], (10 ** cx, 10 ** cy), xytext=(dx, dy), textcoords="offset points", ha=ha,
                        va="center", fontsize=11, color=INK, zorder=7,
                        arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6, shrinkA=0, shrinkB=2) if abs(dx) + abs(dy) > 25 else None)
blobs(ax, {"Hydrogel (PEGDA)": (0, -28, "center"), "IP-PDMS": (0, -32, "center"), "TPU / TPE (85A-64D)": (0, 32, "center")}, 0.12, 0.1)
blobs(az, {"PA 12 (SLS)": (-10, -26, "right"), "ABS / ASA (FFF)": (-60, -6, "right"), "PETG (FFF)": (-40, -34, "right"),
           "PLA (FFF)": (10, -34, "left"), "PEEK / PEI (FFF)": (-30, 30, "right"), "CF-PA / CF-PEEK (FFF)": (0, 34, "center"),
           "SLA standard resins": (-55, 26, "right"), "IP-S / IP-Dip": (55, -40, "left"), "SU-8 (2PP)": (40, 26, "left")}, 0.03, 0.03)

# legend and notes (top right)
lx = fig.add_axes([0.63, 0.68, 0.36, 0.28]); lx.axis("off")
lx.text(0, 1.0, "Printable polymers: modulus vs strength", fontsize=15, color=INK, weight="bold", va="top", transform=lx.transAxes)
y = 0.78
for i, (p, c) in enumerate(PROC):
    xx = 0.0 if i < 2 else 0.5; yy = y - (i % 2) * 0.17
    lx.add_patch(Ellipse((xx + 0.03, yy), 0.05, 0.1, transform=lx.transAxes, fc=c, alpha=0.5, ec=c))
    lx.text(xx + 0.08, yy, {"MEX": "MEX (filament)", "PBF": "PBF (powder)", "VPP": "VPP (SLA, DLP)", "2PP / MPP": "2PP / MPP"}[p],
            va="center", fontsize=12.5, color=INK, transform=lx.transAxes)
lx.plot([0.0, 0.06], [0.36, 0.36], ls=(0, (5, 4)), color="#b9b4a8", transform=lx.transAxes)
lx.text(0.08, 0.36, "constant strain $\\sigma$/E", va="center", fontsize=12, color=GREY, transform=lx.transAxes)
lx.text(0, 0.0, "Ellipses span published ranges (2PP resins: compressive yield of micropillars);\n"
        "printed Z values often 10-50 % lower. SZ2080/OrmoComp: strength not published.\n"
        "Data: tables/02_polymers_ashby.csv; makers' data sheets; Ashby (2016).",
        va="bottom", fontsize=9.5, color=GREY, transform=lx.transAxes, linespacing=1.3)
for ext in ("png", "pdf"):
    fig.savefig(HERE / f"02_j02_polymer_ashby_E_strength.{ext}", dpi=200, facecolor="white")
print("ok")
