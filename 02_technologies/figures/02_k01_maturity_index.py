"""02_k01 - Technology readiness of polymer AM: AMPOWER Maturity Index 2022 and a 2026 update.

Grey dots: technology classes that had reached the index in 2022 (AMPOWER Insights Vol. 11, p. 11).
Coloured arrows: the new technologies AMPOWER reviewed, from their 2022 rating (open marker,
AMPOWER, p. 70) to an indicative 2026 position (filled marker) estimated for this course from
the 2026 company status (machines on sale, series users, services, closures). The 2026 points are
NOT an AMPOWER rating. Data and sources: tables/02_ampower_maturity_2022_2026.csv.
Writes 02_k01_maturity_index.png / .pdf.  Usage: python 02_k01_maturity_index.py
"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from _printers_common import HERE, INK, GREY, use_font

use_font()
CSV = HERE.parent / "tables" / "02_ampower_maturity_2022_2026.csv"
R = list(csv.DictReader(open(CSV, encoding="utf-8")))
MAT = {"thermoset": ("#2a78d6", "photopolymer (thermoset)"),
       "elastomer": ("#1baf7a", "elastomer (silicone)"),
       "thermoplastic": ("#b5651d", "thermoplastic")}
BAND = ["#eef3f8", "#e6eef6", "#dde8f2", "#e3efe3", "#d5e8d4"]       # proof of concept ... widespread
BAND_TXT = ["proof of\nconcept", "prototype\nsystem", "first\napplications", "industrial\nuse",
            "widespread\nindustrial use"]
SHOW_CLASS = {"Filament Material Extrusion", "Powder Bed Fusion", "Vat Polymerization",
              "Area-wise Vat Polymerization", "Material Jetting", "Thermal Powder Bed Fusion"}
# label position (data coordinates) for the 2026 end point, joined by a thin leader line
LAB = {
    "CUBICURE (area-wise film)": (3.55, 3.45, "left"),
    "MASSIVIT (thermoset deposition)": (1.55, 3.35, "left"),
    "INKBIT (material jetting)": (3.55, 2.95, "left"),
    "SPECTROPLAST (vat vulcanization)": (3.55, 2.55, "left"),
    "IMPOSSIBLE OBJECTS (CF sheet lamination)": (1.55, 3.0, "left"),
    "READILY3D (volumetric)": (3.55, 2.15, "left"),
    "BCN3D -> SUPERNOVA (area-wise film)": (3.55, 1.8, "left"),
    "XOLO (volumetric)": (2.75, 1.45, "left"),
    "3DEUS DYNAMICS (elastomer deposition)": (1.55, 1.95, "left"),
}
EVOLVE_LAB = (1.55, 2.3)
CLS = {  # class label offsets
    "Filament Material Extrusion": (-8, 0, "right"), "Powder Bed Fusion": (-8, 2, "right"),
    "Vat Polymerization": (-8, -4, "right"), "Area-wise Vat Polymerization": (-8, -12, "right"),
    "Material Jetting": (-8, 0, "right"), "Thermal Powder Bed Fusion": (-8, 0, "right"),
    "Pellet Material Extrusion": (8, 4, "left"), "Continuous Fiber Material Extrusion": (8, -6, "left"),
}
NICE = {"BCN3D -> SUPERNOVA (area-wise film)": "BCN3D → Supernova (VLM)",
        "XOLO (volumetric)": "xolo (volumetric)", "READILY3D (volumetric)": "Readily3D (volumetric)",
        "CUBICURE (area-wise film)": "Cubicure (Hot Lithography)",
        "INKBIT (material jetting)": "Inkbit (vision-controlled jetting)",
        "MASSIVIT (thermoset deposition)": "Massivit (gel dispensing)",
        "SPECTROPLAST (vat vulcanization)": "Spectroplast (silicone DLP)",
        "3DEUS DYNAMICS (elastomer deposition)": "3Deus Dynamics (silicone)",
        "IMPOSSIBLE OBJECTS (CF sheet lamination)": "Impossible Objects (CBAM)",
        "EVOLVE (electrophotography lamination)": "Evolve (STEP)"}
halo = [pe.withStroke(linewidth=3, foreground="white")]

fig = plt.figure(figsize=(16, 9))
ax = fig.add_axes([0.06, 0.09, 0.64, 0.86])
X0, Y0 = 1.4, 1.2                                   # zoom on the populated part of the 0-5 chart
for i in range(5):
    ax.axhspan(i, i + 1, color=BAND[i], zorder=0, lw=0)
    if i + 1 > Y0:
        ax.text(5.06, (max(i, Y0) + i + 1) / 2, BAND_TXT[i], va="center", ha="left",
                fontsize=12.5, color=GREY, clip_on=False)
for v in range(1, 5):
    ax.axvline(v, color="white", lw=1.4, zorder=0)
    ax.axhline(v, color="white", lw=1.4, zorder=0)
ax.set_xlim(X0, 5); ax.set_ylim(Y0, 5)
ax.set_xticks(range(2, 6)); ax.set_yticks(range(2, 6))
ax.set_xlabel("Technology maturity index  (series production, process capability, machine, process control)",
              fontsize=13, color=INK)
ax.set_ylabel("Industrialisation index  (installed base, materials, knowledge, standards)",
              fontsize=13, color=INK)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

for r in R:
    if r["level"] == "class" and r["name"] in SHOW_CLASS:
        x, y = float(r["tech_2022"]), float(r["ind_2022"])
        ax.scatter([x], [y], s=70, color="#8a96a3", edgecolor="white", lw=1.2, zorder=3)
        dx, dy, ha = CLS[r["name"]]
        ax.annotate(r["name"], (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha,
                    va="center", fontsize=11.5, color=GREY, zorder=4, path_effects=halo)

for r in R:
    if r["level"] != "company":
        continue
    c = MAT[r["material"]][0]
    x0, y0 = float(r["tech_2022"]), float(r["ind_2022"])
    ax.scatter([x0], [y0], s=80, facecolor="white", edgecolor=c, lw=2, zorder=5)
    if not r["tech_2026_est"]:                       # wound down
        ax.scatter([x0], [y0], s=150, marker="x", color=INK, lw=2.4, zorder=6)
        ax.annotate(NICE[r["name"]] + ": wound down 2026", (x0, y0), xytext=EVOLVE_LAB,
                    textcoords="data", ha="left", va="center", fontsize=12, color=INK, zorder=7,
                    path_effects=halo, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8,
                                                       shrinkA=2, shrinkB=7))
        continue
    x1, y1 = float(r["tech_2026_est"]), float(r["ind_2026_est"])
    ax.annotate("", (x1, y1), (x0, y0), zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8, shrinkA=6, shrinkB=6,
                                mutation_scale=16))
    ax.scatter([x1], [y1], s=110, color=c, edgecolor="white", lw=1.5, zorder=6)
    lxp, lyp, ha = LAB[r["name"]]
    ax.annotate(NICE[r["name"]], (x1, y1), xytext=(lxp, lyp), textcoords="data", ha=ha,
                va="center", fontsize=12, color=INK, zorder=7, path_effects=halo,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.8, shrinkA=2, shrinkB=7))

# legend + note
lx = fig.add_axes([0.80, 0.09, 0.19, 0.86]); lx.axis("off")
y = 0.98
for k in ("thermoset", "elastomer", "thermoplastic"):
    c, t = MAT[k]
    lx.scatter([0.04], [y], s=110, color=c, transform=lx.transAxes)
    lx.text(0.12, y, t, va="center", fontsize=13, color=INK, transform=lx.transAxes)
    y -= 0.05
y -= 0.02
lx.scatter([0.04], [y], s=80, facecolor="white", edgecolor=GREY, lw=2, transform=lx.transAxes)
lx.text(0.12, y, "2022: AMPOWER rating", va="center", fontsize=12.5, color=GREY, transform=lx.transAxes)
y -= 0.05
lx.scatter([0.04], [y], s=110, color=GREY, transform=lx.transAxes)
lx.text(0.12, y, "2026: course estimate", va="center", fontsize=12.5, color=GREY, transform=lx.transAxes)
y -= 0.05
lx.scatter([0.04], [y], s=70, color="#8a96a3", edgecolor="white", transform=lx.transAxes)
lx.text(0.12, y, "established classes (2022)", va="center", fontsize=12.5, color=GREY,
        transform=lx.transAxes)
lx.text(0, 0.0,
        "Zoom on the 1.4-5 / 1.2-5 part of the\n"
        "AMPOWER 0-5 chart.\n"
        "2022 positions read from AMPOWER\n"
        "Insights Vol. 11 (Nov. 2022), pp. 11, 70.\n"
        "2026 positions: indicative, set for this\n"
        "course from the companies' 2026 status\n"
        "(machines on sale, series users, parts\n"
        "services, funding, closures); they are\n"
        "not an AMPOWER rating.\n\n"
        "Data and sources:\n"
        "tables/\n02_ampower_maturity_2022_2026.csv",
        va="bottom", fontsize=11, color=GREY, transform=lx.transAxes, linespacing=1.35)

for ext in ("png", "pdf"):
    fig.savefig(HERE / f"02_k01_maturity_index.{ext}", dpi=200, facecolor="white")
print("ok")
