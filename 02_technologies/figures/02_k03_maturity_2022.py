"""02_k03 - AMPOWER Maturity Index 2022 only (no 2026 estimates), for the polymer exercise.

Reads ../tables/02_ampower_maturity_2022_2026.csv (columns tech_2022, ind_2022 only) and writes
  02_k03_maturity_2022.png/.pdf       slide version: 17 classes (grey) + the 10 companies, numbered as the groups
  02_k03_maturity_2022_wall.pdf       A1 landscape poster for the wall: same grid, large, room for sticky dots
The 2026 columns are never read here, so the picture can be shown before the exercise.
"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _printers_common import HERE, INK, GREY, GRID, use_font

CSV = HERE.parent / "tables" / "02_ampower_maturity_2022_2026.csv"
GROUP = {"XOLO": 1, "READILY3D": 2, "CUBICURE": 3, "BCN3D": 4, "EVOLVE": 5, "IMPOSSIBLE OBJECTS": 6,
         "3DEUS DYNAMICS": 7, "SPECTROPLAST": 8, "MASSIVIT": 9, "INKBIT": 10}
LEVELS = [(1, "proof of concept"), (2, "prototype system"), (3, "first applications"),
          (4, "industrial use"), (5, "widespread industrial use")]
ORANGE, BLUE = "#c4561a", "#2f5f9e"


def company_key(name):
    for k in GROUP:
        if name.upper().startswith(k):
            return k
    return None


rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
classes = [r for r in rows if r["level"] == "class"]
comps = [(GROUP[company_key(r["name"])], company_key(r["name"]), float(r["tech_2022"]), float(r["ind_2022"]))
         for r in rows if r["level"] == "company"]


def draw(fig, ax, big=False):
    fs = 22 if big else 13
    for y, lab in LEVELS:
        ax.axhline(y, color=GRID, lw=1)
        ax.text(5.08, y, lab, va="center", ha="left", color=GREY, fontsize=fs)
    ax.set_xlim(0, 5); ax.set_ylim(0, 5)
    ax.set_xticks(range(6)); ax.set_yticks(range(6))
    ax.grid(True, axis="x", color=GRID, lw=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GREY)
    ax.tick_params(colors=INK, labelsize=fs)
    ax.set_xlabel("technology maturity index", color=INK, fontsize=fs + 2)
    ax.set_ylabel("industrialisation maturity index", color=INK, fontsize=fs + 2)
    for r in classes:
        x, y = float(r["tech_2022"]), float(r["ind_2022"])
        ax.scatter([x], [y], s=(90 if big else 30), color="#b9b4a8", zorder=2)
    est = [r for r in classes if float(r["ind_2022"]) > 3.5]
    dy = {"Powder Bed Fusion": 0.05, "Area-wise Vat Polymerization": -0.05}
    for r in est:  # label only the established classes, the rest are context
        ax.text(float(r["tech_2022"]) - 0.06, float(r["ind_2022"]) + dy.get(r["name"], 0), r["name"], ha="right", va="center",
                color=GREY, fontsize=fs - 3)
    nudge = {2: (-0.075, 0), 8: (0.075, 0), 1: (0, -0.07), 7: (0, 0.07)}  # identical or close 2022 points
    for n, k, x, y in comps:
        x, y = x + nudge.get(n, (0, 0))[0], y + nudge.get(n, (0, 0))[1]
        ax.scatter([x], [y], s=(900 if big else 260), color="white", edgecolor=BLUE, lw=2, zorder=3)
        ax.text(x, y, str(n), ha="center", va="center", color=BLUE, fontsize=fs - 1, weight="bold", zorder=4)
    leg = "  ".join(f"{n} {k.title() if k not in ('BCN3D', 'XOLO') else k}" for n, k, _, _ in sorted(comps))
    return leg


use_font("Inter", 13)
fig, ax = plt.subplots(figsize=(12, 7.2))
leg = draw(fig, ax)
fig.text(0.07, 0.005, "Numbered circles: the ten companies of the exercise, AMPOWER 2022 rating (2 and 8, 1 and 7 nudged apart).  Grey dots: the 17 technology classes.",
         color=GREY, fontsize=11)
for ext in ("png", "pdf"):
    fig.savefig(HERE / f"02_k03_maturity_2022.{ext}", dpi=200, facecolor="white", bbox_inches="tight")
plt.close(fig)

fig, ax = plt.subplots(figsize=(33.1, 23.4))  # A1 landscape
draw(fig, ax, big=True)
fig.text(0.06, 0.95, "Polymer AM 2022 → 2026: where is your technology today?", color=INK, fontsize=40, weight="bold")
fig.text(0.06, 0.92, "Circles: AMPOWER rating, Nov. 2022.  Stick your first-guess dot (colour 1) and your after-research dot (colour 2), "
         "with your group number.", color=GREY, fontsize=24)
fig.text(0.06, 0.03, "Groups: " + leg + ".   Source: AMPOWER Insights Vol. 11, Nov. 2022, pp. 11 and 70.",
         color=GREY, fontsize=20)
fig.savefig(HERE / "02_k03_maturity_2022_wall.pdf", facecolor="white")
plt.close(fig)
print("ok")
