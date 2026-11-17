"""02_m01-m04 - Physical laws behind metal AM (technology_metal deck, Nov 2026).

Same drawing style as 02_l00_physics_laws.py. Orders of magnitude, alloy-dependent:
the slide notes give the sources and the values still to verify.

  02_m01_melt_cool          process window (laser power vs scan speed, constant energy density)
                            and cooling rate vs cell / dendrite arm spacing
  02_m02_residual_stress    thermal stress E·α·ΔT against the as-built yield strength, four alloys
  02_m03_murakami_fatigue   fatigue limit vs defect size (Murakami √area), with typical defect sizes
  02_m04_rate_resolution    deposition rate vs smallest feature for the five metal processes
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter

from _printers_common import HERE, INK, GREY, GRID, use_font

use_font("Inter", 14)
C = ["#2f5f9e", "#c4561a", "#1f7a5c", "#7b52c7", "#a0522d"]
PALE = ["#dfe8f4", "#f6e0d3", "#d9ece4", "#e7e0f4", "#efe2d8"]
G = FuncFormatter(lambda v, _: f"{v:g}")


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GREY)
    ax.tick_params(colors=INK, labelsize=13)
    ax.grid(True, which="major", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def save(fig, stem):
    for ext in ("png", "pdf"):
        fig.savefig(HERE / f"{stem}.{ext}", dpi=200, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("ok", stem)


# ---------------------------------------------------------------- m01 cooling and crystallisation
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13.5, 5.6), gridspec_kw={"wspace": 0.32})
R = np.logspace(-6, 0.5, 200)
LBL = {1e-1: "0.1 K/s", 1e1: "10 K/s", 1e3: "10³ K/s", 1e5: "10⁵ K/s", 1e7: "10⁷ K/s"}
for cr in (1e-1, 1e1, 1e3, 1e5, 1e7):                          # G*R = cooling rate (K/s)
    a1.plot(R, cr / R, color=GREY, lw=0.9, ls="--")
    if cr / 2.5 >= 1e2:
        a1.text(2.4, cr / 2.4 * 1.25, LBL[cr], color=GREY, fontsize=11, ha="right")
    else:
        a1.text(cr / 1e2 * 1.2, 1.25e2, LBL[cr], color=GREY, fontsize=11, ha="left")
for lo_g, hi_g, lo_r, hi_r, lab, ci in [(1e2, 1e4, 1e-5, 1e-3, "casting", 4), (1e4, 1e6, 1e-3, 1e-2, "DED, WAAM", 1),
                                         (1e6, 1e7, 1e-1, 1, "laser PBF", 2)]:
    a1.add_patch(Rectangle((lo_r, lo_g), hi_r - lo_r, hi_g - lo_g, color=PALE[ci], ec=C[ci], lw=1.6))
    a1.text(np.sqrt(lo_r * hi_r), np.sqrt(lo_g * hi_g), lab, ha="center", va="center", color=INK, fontsize=12.5)
a1.annotate("", xy=(2.5e-6, 6e7), xytext=(2e-4, 6e5), arrowprops=dict(arrowstyle="->", color=C[0], lw=1.6))
a1.text(1.3e-6, 2.5e5, "G/R high:\nplanar, cellular,\ncolumnar", color=C[0], fontsize=12, ha="left")
a1.text(3e-2, 2.2e2, "G/R low:\nequiaxed\ndendrites", color=C[3], fontsize=12, ha="left")
a1.set_xscale("log"); a1.set_yscale("log"); a1.set_xlim(1e-6, 3); a1.set_ylim(1e2, 1e8)
a1.set_xlabel("solidification rate  R  (m/s, log scale)", color=INK, fontsize=14)
a1.set_ylabel("thermal gradient  G  (K/m, log scale)", color=INK, fontsize=14)
style(a1)
rate = np.logspace(-1, 7, 200)
a2.plot(rate, 50 * rate ** (-1 / 3), color=C[0], lw=2.4)
for lo, hi, lab, ci, dy in [(0.1, 10, "sand casting", 4, 1.7), (10, 1e2, "die casting", 3, 1.7), (1e2, 1e4, "DED, WAAM", 1, 1.7),
                            (1e5, 1e7, "laser PBF", 2, 1.7)]:
    rr = np.logspace(np.log10(lo), np.log10(hi), 50)
    a2.plot(rr, 50 * rr ** (-1 / 3) * (dy if dy < 1 else 1), color=C[ci], lw=7, alpha=0.55, solid_capstyle="butt")
    xm = np.sqrt(lo * hi)
    a2.text(xm, 50 * xm ** (-1 / 3) * dy * (0.8 if dy < 1 else 1.0), lab, color=C[ci], fontsize=12, ha="left" if dy >= 1 else "center",
            va="bottom" if dy >= 1 else "top")
a2.set_xscale("log"); a2.set_yscale("log"); a2.set_xlim(0.1, 1e7); a2.set_ylim(0.2, 200)
a2.set_xlabel("cooling rate  dT/dt  (K/s, log scale)", color=INK, fontsize=14)
a2.set_ylabel("cell or dendrite arm spacing  λ  (µm)", color=INK, fontsize=14)
a2.yaxis.set_major_formatter(G)
style(a2)
save(fig, "02_m01_melt_cool")

# ---------------------------------------------------------------- m02 residual stress
alloys = [  # name, E (GPa), alpha (1e-6/K), dT (K), as-built yield (MPa)
    ("Ti-6Al-4V", 114, 8.6, 1450, 1000),
    ("316L", 193, 16.0, 1250, 450),
    ("Inconel 718", 200, 13.0, 1150, 700),
    ("AlSi10Mg", 70, 21.0, 350, 250),
]
fig, (a0, ax) = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw={"width_ratios": [1, 1.6], "wspace": 0.25})
a0.set_xlim(0, 10); a0.set_ylim(0, 10); a0.axis("off")
a0.add_patch(Rectangle((1, 6.2), 8, 1.2, color=PALE[1], ec=C[1], lw=1.8))
a0.add_patch(Rectangle((1, 2.0), 8, 3.4, color=PALE[0], ec=C[0], lw=1.8))
a0.text(5, 6.8, "new layer: hot", ha="center", va="center", color=INK, fontsize=12)
a0.text(5, 3.7, "part below: cold", ha="center", va="center", color=INK, fontsize=12)
for xx in (1.6, 8.4):
    a0.annotate("", xy=(5 + (xx - 5) * 0.75, 7.9), xytext=(xx, 7.9), arrowprops=dict(arrowstyle="->", color=C[1], lw=1.6))
a0.text(5, 8.5, "wants to shrink by α Δθ, held: tension", ha="center", color=C[1], fontsize=12)
a0.text(5, 1.2, "pulled in: compression", ha="center", color=C[0], fontsize=12)
a0.text(5, 9.6, "σᵢ = Eᵢ (εᵢ − αᵢ Δθᵢ),  ε₁ = ε₂,  σ₁A₁ + σ₂A₂ = 0", ha="center", color=INK, fontsize=12.5)

x = np.arange(len(alloys))
sig = [E_ * 1e3 * a * 1e-6 * dT for _, E_, a, dT, _ in alloys]      # MPa
ys = [y for *_, y in alloys]
ax.bar(x - 0.18, sig, 0.34, color=PALE[1], edgecolor=C[1], lw=1.6, label="thermal stress if fully constrained  E·α·ΔT")
ax.bar(x + 0.18, ys, 0.34, color=PALE[0], edgecolor=C[0], lw=1.6, label="yield strength as built")
for i, (s, y) in enumerate(zip(sig, ys)):
    ax.text(i - 0.18, s * 1.06, f"{s / 1000:.1f} GPa", ha="center", color=C[1], fontsize=12)
    ax.text(i + 0.18, y * 1.06, f"{y / 1000:.2f}", ha="center", color=C[0], fontsize=12)
    ax.text(i, -420, f"× {s / y:.0f}" if s / y >= 2 else f"× {s / y:.1f}", ha="center", color=INK, fontsize=14, weight="bold")
ax.set_xticks(x); ax.set_xticklabels([a[0] for a in alloys], fontsize=14)
ax.set_ylim(-600, 5600)
ax.set_ylabel("stress  (MPa)", color=INK, fontsize=14)
ax.axhline(0, color=GREY, lw=1)
ax.legend(frameon=False, fontsize=12, loc="upper right")
style(ax); ax.grid(axis="x", visible=False)
save(fig, "02_m02_residual_stress")

# ---------------------------------------------------------------- m03 cycles, defects and fatigue
fig, (a0, ax) = plt.subplots(1, 2, figsize=(14.5, 5.6), gridspec_kw={"wspace": 0.28})
N = np.logspace(3, 8, 300)
for sf, se, lab, c, ls in [(1.0, 0.50, "wrought, machined", C[2], "-"), (0.95, 0.45, "AM, HIP + machined", C[0], "-"),
                           (0.85, 0.20, "AM as built (pores, rough surface)", C[1], "-")]:
    amp = np.maximum(sf * (N / 1e3) ** -0.09, se)
    a0.plot(N, amp, color=c, lw=2.4, ls=ls, label=lab)
a0.set_xscale("log"); a0.set_xlim(1e3, 1e8); a0.set_ylim(0, 1.1)
a0.set_xlabel("cycles to failure  N  (log scale)", color=INK, fontsize=14)
a0.set_ylabel("stress amplitude / σ_u  (schematic)", color=INK, fontsize=14)
a0.text(2e7, 0.53, "endurance limit", color=C[2], fontsize=11, ha="center")
a0.legend(frameon=False, fontsize=11.5, loc="upper right")
style(a0)
a = np.logspace(0.5, 3, 300)                         # sqrt(area) in µm
for HV, lab, c in [(350, "Ti-6Al-4V, HV ≈ 350", C[0]), (220, "316L, HV ≈ 220", C[1])]:
    ax.plot(a, 1.43 * (HV + 120) / a ** (1 / 6), color=c, lw=2.4, label=f"{lab}, surface defect")
    ax.plot(a, 1.56 * (HV + 120) / a ** (1 / 6), color=c, lw=1.4, ls="--", label=f"{lab}, internal defect")
for lo, hi, lab, ci, y in [(5, 50, "gas pores", 2, 140), (50, 500, "lack-of-fusion pores", 1, 140), (20, 150, "as-built surface valleys", 3, 105)]:
    ax.add_patch(Rectangle((lo, y - 12), hi - lo, 24, color=PALE[ci], ec=C[ci], lw=1.2))
    ax.text(np.sqrt(lo * hi), y, lab, ha="center", va="center", color=INK, fontsize=12)
ax.set_xscale("log"); ax.set_xlim(3, 1000); ax.set_ylim(80, 620)
ax.set_xlabel("defect size  √area  (µm, log scale)", color=INK, fontsize=14)
ax.set_ylabel("fatigue limit  σ_w  (MPa)", color=INK, fontsize=14)
ax.xaxis.set_major_formatter(G)
ax.legend(frameon=False, fontsize=11.5, loc="upper right")
style(ax)
save(fig, "02_m03_murakami_fatigue")

# ---------------------------------------------------------------- m04 rate vs resolution
procs = [  # name, feature lo, hi (mm), rate lo, hi (cm³/h), colour, label position
    ("laser PBF", 0.1, 0.3, 5, 1000, 0),
    ("binder jetting (printing step)", 0.1, 0.4, 1000, 12000, 3),
    ("DED powder (LMD)", 0.5, 4, 13, 250, 2),
    ("cold spray", 2, 8, 50, 700, 4),
    ("DED wire (WAAM)", 3, 10, 125, 1250, 1),
]
LAB = {"DED powder (LMD)": (1.3, 22), "cold spray": (3.4, 75), "DED wire (WAAM)": (5.5, 900), "laser PBF": (0.17, 60)}
fig, ax = plt.subplots(figsize=(11.5, 6))
for name, f0, f1, r0, r1, ci in procs:
    ax.add_patch(Rectangle((f0, r0), f1 - f0, r1 - r0, color=PALE[ci], ec=C[ci], lw=1.6, alpha=0.9))
    lx, ly = LAB.get(name, (np.sqrt(f0 * f1), np.sqrt(r0 * r1)))
    ax.text(lx, ly, name, ha="center", va="center", color=INK, fontsize=12.5)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(0.05, 20); ax.set_ylim(2, 30000)
ax.set_xlabel("smallest feature  (mm, log scale)", color=INK, fontsize=14)
ax.set_ylabel("build rate  (cm³/h, log scale)", color=INK, fontsize=14)
ax.xaxis.set_major_formatter(G); ax.yaxis.set_major_formatter(G)
ax.text(0.06, 3, "fine and slow", color=GREY, fontsize=12); ax.text(17, 15000, "coarse and fast", color=GREY, fontsize=12, ha="right")
style(ax)
save(fig, "02_m04_rate_resolution")
