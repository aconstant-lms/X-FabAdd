"""Stylised standing human pictogram (original drawing) -> 04_human_silhouette.png"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

INK = "#1B2433"
fig = plt.figure(figsize=(2.4, 7.2), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-0.1, 7.1); ax.set_aspect("equal"); ax.axis("off")

def limb(x0, y0, x1, y1, w):
    ax.plot([x0, x1], [y0, y1], color=INK, lw=w, solid_capstyle="round")

ax.add_patch(Circle((0, 6.45), 0.45, color=INK))                      # head
ax.add_patch(FancyBboxPatch((-0.66, 3.05), 1.32, 2.65,                 # torso
             boxstyle="round,pad=0,rounding_size=0.32", color=INK))
limb(-0.86, 5.35, -1.0, 2.9, 23); limb(0.86, 5.35, 1.0, 2.9, 23)  # arms
limb(-0.34, 3.3, -0.40, 0.3, 33);  limb(0.34, 3.3, 0.40, 0.3, 33)   # legs
fig.savefig("04_human_silhouette.png", transparent=True)
