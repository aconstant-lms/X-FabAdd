"""Woman and man pictograms (original drawing) -> 02_human_silhouette.png"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

INK, INK2 = "#1B2433", "#2F5F9E"
fig = plt.figure(figsize=(4.4, 5.6), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-2.3, 2.3); ax.set_ylim(-0.1, 5.75); ax.set_aspect("equal"); ax.axis("off")

def limb(x0, y0, x1, y1, w, c):
    ax.plot([x0, x1], [y0, y1], color=c, lw=w, solid_capstyle="round")

# woman (left, slightly shorter)
xw, c = -1.05, INK2
ax.add_patch(Circle((xw, 4.72), 0.36, color=c))
ax.add_patch(Polygon([(xw - 0.38, 4.2), (xw + 0.38, 4.2), (xw + 0.78, 2.15), (xw - 0.78, 2.15)], closed=True, color=c, joinstyle="round"))
limb(xw - 0.45, 4.05, xw - 0.85, 2.75, 15, c); limb(xw + 0.45, 4.05, xw + 0.85, 2.75, 15, c)
limb(xw - 0.27, 2.2, xw - 0.27, 0.35, 19, c); limb(xw + 0.27, 2.2, xw + 0.27, 0.35, 19, c)
# man (right)
xm, c = 1.05, INK
ax.add_patch(Circle((xm, 5.12), 0.38, color=c))
ax.add_patch(FancyBboxPatch((xm - 0.55, 2.45), 1.10, 2.2, boxstyle="round,pad=0,rounding_size=0.26", color=c))
limb(xm - 0.73, 4.45, xm - 0.86, 2.35, 18, c); limb(xm + 0.73, 4.45, xm + 0.86, 2.35, 18, c)
limb(xm - 0.29, 2.6, xm - 0.33, 0.3, 26, c); limb(xm + 0.29, 2.6, xm + 0.33, 0.3, 26, c)
fig.savefig("02_human_silhouette.png", transparent=True)
