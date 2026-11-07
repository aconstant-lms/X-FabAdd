"""Schematic half cross-sections: monobloc wheel vs rubber-sprung (resilient) wheel of the ICE 1
(original simplified drawing, not to scale) -> 04_eschede_wheel_schematic.png"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

STEEL, RUBBER, TYRE, INK, RED = "#9AA5B1", "#3E4A57", "#C5CDD5", "#1F2933", "#C0392B"
fig, axs = plt.subplots(1, 2, figsize=(10, 5.2), dpi=220)

def rail(ax):
    ax.add_patch(Rectangle((0.3, -0.55), 1.4, 0.35, color="#7B8794"))
    ax.text(1.0, -0.75, "rail", ha="center", va="top", fontsize=10, color=INK)

def frame(ax, title):
    ax.set_xlim(-0.6, 3.2); ax.set_ylim(-1.2, 4.6); ax.set_aspect("equal"); ax.axis("off")
    ax.text(1.3, 4.45, title, ha="center", va="top", fontsize=13, weight="bold", color=INK)
    ax.plot([1.0, 1.0], [-0.2, 3.9], color=INK, lw=0.8, ls="-.")
    ax.text(1.05, 3.85, "axle (centre line above)", fontsize=8.5, color=INK, va="top")

# --- monobloc
ax = axs[0]; frame(ax, "Monobloc wheel"); rail(ax)
ax.add_patch(Polygon([(0.15, -0.2), (1.85, -0.2), (1.85, 0.75), (1.25, 0.95), (1.25, 3.4),
                      (0.75, 3.4), (0.75, 0.95), (0.0, 0.75), (0.0, 0.25), (0.15, 0.25)],
                     closed=True, fc=STEEL, ec=INK, lw=1.2))
ax.text(2.0, 0.3, "rim, web and hub\nin one forged steel piece", fontsize=10, color=INK, va="center")
ax.text(2.0, 1.9, "highest tensile stress\non the outer rim,\nwhere it can be inspected", fontsize=10, color=INK)

# --- resilient
ax = axs[1]; frame(ax, "Rubber-sprung wheel (ICE 1, 1992-98)"); rail(ax)
ax.add_patch(Polygon([(0.15, -0.2), (1.85, -0.2), (1.85, 0.35), (0.0, 0.35), (0.0, 0.1), (0.15, 0.1)],
                     closed=True, fc=TYRE, ec=INK, lw=1.2))                    # thin tyre
ax.add_patch(Rectangle((0.2, 0.35), 1.45, 0.22, fc=RUBBER, ec=INK, lw=1.0))   # rubber ring
ax.add_patch(Polygon([(0.2, 0.57), (1.65, 0.57), (1.65, 0.85), (1.25, 1.0), (1.25, 3.4),
                      (0.75, 3.4), (0.75, 1.0), (0.2, 0.85)], closed=True, fc=STEEL, ec=INK, lw=1.2))
ax.plot([0.55, 0.62], [0.36, 0.12], color=RED, lw=2.4)                         # crack
ax.annotate("fatigue crack from the INNER\nface of the worn tyre:\nhidden from visual inspection",
            xy=(0.6, 0.25), xytext=(1.95, 2.0), fontsize=10, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
ax.annotate("rubber damping ring", xy=(1.62, 0.46), xytext=(1.95, 0.95), fontsize=10, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
ax.annotate("thin steel tyre, flexed at\nevery revolution", xy=(1.8, 0.05), xytext=(1.95, -0.55),
            fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
fig.text(0.5, 0.01, "Simplified half cross-sections, not to scale", ha="center", fontsize=9, color="#52514e")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("04_eschede_wheel_schematic.png")
