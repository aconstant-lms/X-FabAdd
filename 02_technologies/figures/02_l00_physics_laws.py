"""02_l01-l06 - Six physical laws behind polymer AM (technology_polymer deck, Nov 2026).

Writes one PNG + PDF per law, in the course drawing style: thin dark lines, pale fills,
few labels, no title inside the picture. Orders of magnitude are indicative: see the
speaker notes of the slides for sources and the values still to verify.

  02_l01_beer_lambert       light decay in a resin and the Jacobs working curve
  02_l02_two_photon         absorbed energy per plane: one photon vs two photons
  02_l03_viscosity_ruler    viscosity windows of the polymer processes
  02_l04_jetting_window     Derby's printable window (Re, We, Z = 1/Oh)
  02_l05_frenkel_sintering  neck growth of two polymer particles vs melt viscosity
  02_l06_yield_stress       height a material holds up by its yield stress
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from _printers_common import HERE, INK, GREY, GRID, use_font

use_font("Inter", 14)
C = ["#2f5f9e", "#c4561a", "#1f7a5c", "#7b52c7", "#a0522d"]
PALE = ["#dfe8f4", "#f6e0d3", "#d9ece4", "#e7e0f4", "#efe2d8"]


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


def pow10(v, _=None):
    e = int(round(np.log10(v)))
    return {-3: "0.001", -2: "0.01", -1: "0.1", 0: "1", 1: "10", 2: "100", 3: "1000"}.get(e, f"$10^{{{e}}}$")


# ---------------------------------------------------------------- l01 Beer-Lambert
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={"wspace": 0.32})
z = np.linspace(0, 30, 600)
for Dp, c, lab in [(0.15, C[1], "SLA / DLP resin, $D_p$ = 0.15 mm"),
                   (2.0, C[0], "clear resin, $D_p$ = 2 mm"),
                   (15.0, C[3], "volumetric resin, $D_p$ = 15 mm")]:
    a1.plot(z, np.exp(-z / Dp), color=c, lw=2.2, label=lab)
a1.set_yscale("log"); a1.set_ylim(1e-4, 1.3); a1.set_xlim(0, 30)
a1.set_xlabel("depth in the resin  z  (mm)", color=INK, fontsize=14)
a1.set_ylabel("light left  I / I$_0$", color=INK, fontsize=14)
a1.axhline(0.1, color=GREY, lw=1, ls="--")
a1.text(9, 0.13, "10 % left", ha="left", color=GREY, fontsize=12)
a1.legend(frameon=False, fontsize=12, loc="lower left")
style(a1)
E = np.logspace(0.7, 3, 300); Ec, Dp = 8.0, 0.15
a2.plot(E, np.maximum(Dp * np.log(E / Ec), 0), color=C[1], lw=2.4)
a2.set_xscale("log"); a2.set_xlim(5, 1000); a2.set_ylim(0, 0.8)
a2.set_xlabel("exposure  E  (mJ/cm², log scale)", color=INK, fontsize=14)
a2.set_ylabel("cured depth  C$_d$  (mm)", color=INK, fontsize=14)
a2.axvline(Ec, color=GREY, lw=1, ls="--"); a2.text(Ec * 1.08, 0.72, "E$_c$: gel threshold", color=GREY, fontsize=12)
a2.annotate("slope = D$_p$ per factor e", xy=(120, Dp * np.log(120 / Ec)), xytext=(11, 0.5),
            color=INK, fontsize=12, arrowprops=dict(arrowstyle="-", color=GREY, lw=1))
a2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
style(a2)
save(fig, "02_l01_beer_lambert")

# ---------------------------------------------------------------- l02 one vs two photons
fig, ax = plt.subplots(figsize=(11, 5))
u = np.linspace(-6, 6, 800)
one = np.ones_like(u)
two = 1 / (1 + u ** 2)
ax.fill_between(u, 0, two, where=two > 0.5, color=PALE[3])
ax.plot(u, one, color=C[1], lw=2.4, label="one photon: rate ~ I, every plane gets the same energy")
ax.plot(u, two, color=C[3], lw=2.4, label="two photons: rate ~ I², energy concentrates at the focus")
ax.axhline(0.5, color=GREY, lw=1, ls="--"); ax.text(5.9, 0.53, "cure threshold", ha="right", color=GREY, fontsize=12)
ax.set_xlim(-6, 6); ax.set_ylim(0, 1.25)
ax.set_xlabel("distance from the focus along the beam  z / z$_R$  (Rayleigh lengths)", color=INK, fontsize=14)
ax.set_ylabel("energy absorbed per plane\n(normalised)", color=INK, fontsize=14)
ax.text(0, 0.18, "voxel", ha="center", color=C[3], fontsize=13, weight="bold")
ax.legend(frameon=False, fontsize=12, loc="upper left")
style(ax)
save(fig, "02_l02_two_photon")

# ---------------------------------------------------------------- l03 viscosity ruler
rows = [  # label, low, high (Pa.s), colour index
    ("polymer melts: filament, powder fusion, moulding (zero shear)", 1e2, 1e4, 4),
    ("liquid silicone rubbers", 5, 5e2, 2),
    ("high-viscosity photopolymers (heated or film-carried)", 5, 1e3, 1),
    ("standard SLA / DLP resins", 0.1, 3, 0),
    ("jetting inks (at jetting temperature)", 0.005, 0.02, 3),
]
fig, ax = plt.subplots(figsize=(13, 4.8))
for i, (lab, lo, hi, ci) in enumerate(rows):
    ax.barh(i, hi - lo, left=lo, height=0.55, color=PALE[ci], edgecolor=C[ci], lw=1.6)
    ax.text(hi * 1.5 if hi < 1e3 else lo / 1.5, i, lab, va="center", ha="left" if hi < 1e3 else "right",
            fontsize=13, color=INK)
for v, lab in [(1e-3, "water"), (0.08, "olive oil"), (10, "honey")]:
    ax.axvline(v, color=GREY, lw=0.9, ls=":")
    ax.text(v, len(rows) - 0.35, lab, ha="center", color=GREY, fontsize=12)
ax.set_xscale("log"); ax.set_xlim(5e-4, 1e5); ax.set_ylim(-0.6, len(rows) - 0.1)
ax.set_yticks([])
ax.set_xlabel("dynamic viscosity  η  (Pa·s, log scale; 1 Pa·s = 1000 cP)", color=INK, fontsize=14)
ax.xaxis.set_major_formatter(FuncFormatter(pow10))
style(ax); ax.spines["left"].set_visible(False); ax.grid(axis="y", visible=False)
save(fig, "02_l03_viscosity_ruler")

# ---------------------------------------------------------------- l04 jetting window (Derby 2010)
fig, ax = plt.subplots(figsize=(10, 6.5))
Re = np.logspace(0, 3, 400)
we_z1, we_z10 = Re ** 2, (Re / 10) ** 2           # Oh = sqrt(We)/Re = 1/Z
we_splash = (50 / Re ** 0.25) ** 2                  # We^0.5 Re^0.25 = 50
lo = np.maximum.reduce([we_z10, np.full_like(Re, 4.0)])
hi = np.minimum(we_z1, we_splash)
ax.fill_between(Re, lo, hi, where=hi > lo, color=PALE[2], edgecolor=C[2], lw=0)
ax.plot(Re, we_z1, color=GREY, lw=1.4); ax.plot(Re, we_z10, color=GREY, lw=1.4)
ax.plot(Re, we_splash, color=C[1], lw=1.6); ax.axhline(4, color=C[0], lw=1.6)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1, 1000); ax.set_ylim(1, 1000)
ax.set_xlabel("Reynolds number  Re = ρvd / η", color=INK, fontsize=14)
ax.set_ylabel("Weber number  We = ρv²d / γ", color=INK, fontsize=14)
ax.text(2.0, 200, "too viscous\nZ < 1", color=INK, fontsize=13)
ax.text(330, 9, "satellite\ndrops\nZ > 10", color=INK, fontsize=13)
ax.text(20, 1.6, "not enough energy to eject a drop", color=C[0], fontsize=12)
ax.text(150, 300, "splashing\non impact", color=C[1], fontsize=13)
ax.text(30, 20, "printable\nfluid", color=C[2], fontsize=15, weight="bold", ha="center")
ax.text(1.4, 1.6 ** 2 * 0.95, "Z = 1", color=GREY, fontsize=12, rotation=0)
ax.text(60, 36 * 0.6, "Z = 10", color=GREY, fontsize=12)
style(ax)
save(fig, "02_l04_jetting_window")

# ---------------------------------------------------------------- l05 Frenkel sintering
fig, ax = plt.subplots(figsize=(11, 5.6))
t = np.logspace(-3, 4, 500); a, gam = 12e-6, 0.03          # particle radius 12 µm, surface tension 0.03 N/m
for eta, c in [(1e2, C[2]), (1e3, C[0]), (1e4, C[1]), (1e5, C[3])]:
    xa = np.sqrt(3 * gam * t / (2 * eta * a))
    m = xa <= 0.6
    ax.plot(t[m], xa[m], color=c, lw=2.3)
    j = np.argmin(abs(xa - 0.45))
    ax.text(t[j] * 1.25, 0.43, f"η = 10$^{{{int(np.log10(eta))}}}$ Pa·s", color=c, fontsize=12, ha="left")
ax.axhspan(0.3, 0.6, color="#f3f1ec", zorder=0)
ax.text(1.2e-3, 0.56, "neck large enough to carry load", color=GREY, fontsize=12)
for tl, lab in [(1, "1 s"), (5, "5 s per layer"), (60, "1 min")]:
    ax.axvline(tl, color=GREY, lw=0.9, ls=":"); ax.text(tl * 1.08, 0.03, lab, color=GREY, fontsize=12)
ax.set_xscale("log"); ax.set_xlim(1e-3, 1e4); ax.set_ylim(0, 0.62)
ax.set_xlabel("time at temperature  t  (s, log scale)", color=INK, fontsize=14)
ax.set_ylabel("neck radius / particle radius  x / a", color=INK, fontsize=14)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
style(ax)
save(fig, "02_l05_frenkel_sintering")

# ---------------------------------------------------------------- l06 yield stress
fig, ax = plt.subplots(figsize=(11, 5.6))
tau = np.logspace(-1, 5, 300); rho, g = 1100, 9.81
h = tau / (rho * g)
ax.plot(tau, h * 1000, color=C[0], lw=2.4)
ax.axvspan(10, 200, color=PALE[2]); ax.text(45, 4e3, "granular or\ngel support baths", color=C[2], fontsize=12, ha="center")
ax.axvspan(1e3, 1e5, color=PALE[1]); ax.text(1e4, 4e3, "pastes, gels that cure\nwhile they are laid", color=C[1], fontsize=12, ha="center")
for hh, lab in [(1, "1 mm"), (10, "1 cm"), (100, "10 cm"), (1000, "1 m")]:
    ax.axhline(hh, color=GREY, lw=0.8, ls=":"); ax.text(0.12, hh * 1.15, lab, color=GREY, fontsize=12)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(0.1, 1e5); ax.set_ylim(1e-2, 1e4)
ax.set_xlabel("yield stress of the material or of the bath  τ$_y$  (Pa)", color=INK, fontsize=14)
ax.set_ylabel("height held up  h = τ$_y$ / ρg  (mm)", color=INK, fontsize=14)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.text(0.15, 0.03, "a liquid resin or silicone (τ$_y$ ≈ 0) holds nothing: it needs supports, a bath or curing on the fly",
        color=INK, fontsize=12)
style(ax)
save(fig, "02_l06_yield_stress")
