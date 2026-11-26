"""Digital-warehouse flow: a part is printed on demand from its record, or digitized once.

Output: 04_rl_digital_warehouse_flow.png next to this file. Style: Inter, thin dark outlines,
one blue accent (the warehouse record), no title inside the picture.
Run: python 04_industries/rail/figures/04_rl_digital_warehouse_flow.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

HERE = Path(__file__).resolve().parent
INK, QUIET, EDGE, ACCENT = "#1F2933", "#52606D", "#9AA5B1", "#2A78D6"
plt.rcParams.update({"font.family": "Inter"})

W, H = 2.35, 0.72          # box width and height
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200)
ax.set_xlim(0, 10.2)
ax.set_ylim(0.8, 5.2)
ax.axis("off")


def box(cx, cy, name, line1, line2=None, accent=False, h=H):
    ax.add_patch(FancyBboxPatch((cx - W / 2, cy - h / 2), W, h, boxstyle="round,pad=0,rounding_size=0.08",
                                fc=ACCENT if accent else "white", alpha=1, ec=ACCENT if accent else EDGE,
                                lw=2 if accent else 1.2, zorder=2))
    if accent:  # pale fill under the accent outline
        ax.add_patch(FancyBboxPatch((cx - W / 2, cy - h / 2), W, h, boxstyle="round,pad=0,rounding_size=0.08",
                                    fc="#E5EFFB", ec=ACCENT, lw=2, zorder=3))
    top = 0.12 if line2 is None else 0.2
    ax.text(cx, cy + top, name, ha="center", va="center", fontsize=11, fontweight="bold", color=INK, zorder=4)
    ax.text(cx, cy - 0.13 + (0 if line2 is None else 0.03), line1, ha="center", va="center",
            fontsize=9.5, color=INK if accent else QUIET, zorder=4)
    if line2:
        ax.text(cx, cy - 0.3, line2, ha="center", va="center", fontsize=9.5, color=QUIET, zorder=4)


def arrow(x0, y0, x1, y1):
    ax.annotate("", (x1, y1), (x0, y0), zorder=1,
                arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1.2, shrinkA=0, shrinkB=0, mutation_scale=12))


rowA, rowB, rowC = 4.6, 2.9, 1.3
c1, c2, cd, c3 = 1.25, 3.85, 6.3, 8.95

box(c1, rowA, "A part is needed", "broken, worn, obsolete")
box(c2, rowA, "Look up its record", "digital warehouse", accent=True)
ax.add_patch(Polygon([(cd - 0.9, rowA), (cd, rowA + 0.5), (cd + 0.9, rowA), (cd, rowA - 0.5)],
                     closed=True, fc="white", ec=EDGE, lw=1.2, zorder=2))
ax.text(cd, rowA, "Record exists?", ha="center", va="center", fontsize=9.5, color=INK, zorder=4)
box(c3, rowA, "Print on demand", "own printer or partner")
box(c3, rowB, "Inspect and test", "against the record")
box(c3, rowC, "Install the part", "train back in service")
box(cd, rowB, "Digitize the part", "scan and redesign", "qualify and approve", h=0.9)

arrow(c1 + W / 2, rowA, c2 - W / 2, rowA)
arrow(c2 + W / 2, rowA, cd - 0.9, rowA)
arrow(cd + 0.9, rowA, c3 - W / 2, rowA)
arrow(c3, rowA - H / 2, c3, rowB + H / 2)
arrow(c3, rowB - H / 2, c3, rowC + H / 2)
arrow(cd, rowA - 0.5, cd, rowB + 0.45)
ax.plot([cd - W / 2, c2], [rowB, rowB], color=EDGE, lw=1.2, zorder=1)          # loop back
arrow(c2, rowB, c2, rowA - H / 2)

ax.text((cd + 0.9 + c3 - W / 2) / 2, rowA + 0.12, "yes", ha="center", fontsize=9.5, color=QUIET)
ax.text(cd + 0.1, (rowA - 0.5 + rowB + 0.45) / 2, "no", fontsize=9.5, color=QUIET, va="center")
ax.text(c2 - 0.12, rowB + 0.55, "record added,\nreused next time", ha="right", va="center",
        fontsize=9.5, color=QUIET, linespacing=1.4)

fig.savefig(HERE / "04_rl_digital_warehouse_flow.png", bbox_inches="tight", pad_inches=0.15)
