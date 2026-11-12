"""Light-sheet volumetric printing (xolography by xolo, Regehly et al. 2020; Quadratic 3D):
a UV line laser makes a thin light sheet across the cuvette; a projector sends the matching slice
image onto the sheet from behind. The resin cures only where sheet and image meet; the sheet sweeps
through the resin and the part grows behind it, continuously, without layers or supports.
Greyscale isometric line art, same style as 02_h01-h03. Usage: python 02_h07_lightsheet_animation.py"""
import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from iso_anim import Scene, save_gif, TOP, LEFT, RIGHT, PART_TOP, PART_L, PART_R, INK

B = 14.0                  # cuvette half-width (x, y)
ZT = 26.0                 # cuvette height
YF = 9.0                  # front end of the part
RESIN = (0.62, 0.62, 0.62)
PART = (PART_TOP, PART_L, PART_R)
ARCH = [(-8, 2, -4, 18), (4, 2, 8, 18), (-8, 18, 8, 23)]     # (x0, z0, x1, z1) cross-section


def draw(sc, ys, sheet=True):
    # projector behind the cuvette (-y side), lens facing +y
    sc.box(-9, -46, 5, 9, -32, 23, (TOP, LEFT, RIGHT))
    yl = -32.0
    if sheet:
        # image beam from the lens to the sheet
        sc.poly([(-7, yl, 21), (7, yl, 21), (7, ys, 21), (-7, ys, 21)], (1, 1, 1), alpha=0.55,
                stroke=(0.62, 0.62, 0.62), lw=0.7)
        sc.poly([(7, yl, 1), (7, ys, 1), (7, ys, 21), (7, yl, 21)], (1, 1, 1), alpha=0.45,
                stroke=(0.62, 0.62, 0.62), lw=0.7)
        for x0, z0, x1, z1 in ARCH:                      # slice image on the lens
            sc.poly([(x0 * 0.8, yl, 2 + z0 * 0.8), (x1 * 0.8, yl, 2 + z0 * 0.8),
                     (x1 * 0.8, yl, 2 + z1 * 0.8), (x0 * 0.8, yl, 2 + z1 * 0.8)], (0.35, 0.35, 0.35), stroke=None)
    # UV line laser on the -x side, at the height of the sheet
    sc.box(-44, ys - 3, 10, -32, ys + 3, 16, (TOP, LEFT, RIGHT))
    # cuvette back walls and resin
    sc.poly([(-B, -B, 0), (-B, B, 0), (-B, B, ZT), (-B, -B, ZT)], (0.95, 0.95, 0.95), alpha=0.9)
    sc.poly([(-B, -B, 0), (B, -B, 0), (B, -B, ZT), (-B, -B, ZT)], (0.95, 0.95, 0.95), alpha=0.9)
    sc.poly([(-B, -B, 0), (B, -B, 0), (B, B, 0), (-B, B, 0)], RESIN, alpha=0.35, stroke=None)
    # light sheet: a thin plane y = ys from the laser across the cuvette
    if sheet:
        sc.poly([(-32, ys, 12), (-B, ys, 2), (B, ys, 2), (B, ys, 24), (-B, ys, 24), (-32, ys, 14)],
                (1, 1, 1), alpha=0.75, stroke=(0.25, 0.25, 0.25), lw=1.0)
        for x0, z0, x1, z1 in ARCH:                      # where image and sheet meet: the curing slice
            sc.poly([(x0, ys, z0), (x1, ys, z0), (x1, ys, z1), (x0, ys, z1)], (0.30, 0.30, 0.30), stroke=None)
    # part: already swept between the sheet and the front end
    if ys < YF:
        for x0, z0, x1, z1 in sorted(ARCH, key=lambda a: (a[1], a[0])):
            sc.box(x0, ys, z0, x1, YF, z1, PART)
    # resin in front, cuvette front edges
    sc.poly([(-B, B, 0), (B, B, 0), (B, B, ZT), (-B, B, ZT)], RESIN, alpha=0.18, stroke=None)
    sc.poly([(B, -B, 0), (B, B, 0), (B, B, ZT), (B, -B, ZT)], RESIN, alpha=0.24, stroke=None)
    sc.poly([(-B, -B, ZT), (B, -B, ZT), (B, B, ZT), (-B, B, ZT)], RESIN, alpha=0.22, stroke=INK, lw=1.1)
    sc.line((-B, B, 0), (B, B, 0)); sc.line((B, -B, 0), (B, B, 0)); sc.line((B, B, 0), (B, B, ZT))
    sc.line((-B, B, 0), (-B, B, ZT)); sc.line((B, -B, 0), (B, -B, ZT))


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


frames = []
def frame(**kw):
    sc = Scene(ox=372, oy=318, s=5.5)
    draw(sc, **kw)
    frames.append(sc.image())

for i in range(12):
    frame(ys=YF + 2, sheet=False)
N = 100
for i in range(N):                                   # the sheet sweeps towards the projector
    frame(ys=YF + 2 - (2 * YF + 2) * (i + 1) / N)
for i in range(36):
    frame(ys=-YF, sheet=False)
save_gif(frames, str(Path(__file__).with_suffix(".gif")))
print(len(frames), "frames")
