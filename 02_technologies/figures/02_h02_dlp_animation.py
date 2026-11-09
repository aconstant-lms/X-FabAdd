"""DLP animation (bottom-up): a projector under a glass-bottomed vat flashes the whole layer at once;
the platform peels the cured layer off the glass, rises by one layer, and the part grows hanging down."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from iso_anim import Scene, save_gif, TOP, LEFT, RIGHT, PART_TOP, PART_L, PART_R, INK
import math

V = 20.0          # vat half-width
ZV = 22.0         # top of the glass floor
LR = 26.0         # resin level
T = 2.0
N = 7
RESIN = (0.62, 0.62, 0.62)
GLASS = (0.93, 0.93, 0.93)
PART = (PART_TOP, PART_L, PART_R)
LIT = ((0.99, 0.99, 0.99), (0.93, 0.93, 0.93), (0.88, 0.88, 0.88))


def shape(k):
    """Layer k counted from the platform: the part is built upside down."""
    return [(-10, -7, 10, 7)] if k < 4 else [(-10, -7, 0, 7)]


def hull(pts):
    pts = sorted(set(pts))
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def draw(sc, Pb, k_done, flash=None, lit=0.0):
    """Pb: bottom of the platform plate. k_done: finished layers. flash: layer index being exposed."""
    # 1 projector
    sc.box(-9, -7, 0, 9, 7, 8, (TOP, LEFT, RIGHT))
    sc.cylinder(0, 0, 8, 10, 2.6, col=(0.55, 0.55, 0.55))
    # 2 light cone to the footprint of the exposed layer
    if flash is not None and lit > 0:
        x0, y0, x1, y1 = shape(flash)[0]
        pts = [sc.p(0, 0, 10)] + [sc.p(x, y, ZV) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        h = hull(pts)
        c = sc.c
        c.move_to(*h[0])
        for q in h[1:]:
            c.line_to(*q)
        c.close_path()
        c.set_source_rgba(1, 1, 1, 0.95 * lit); c.fill_preserve()
        c.set_source_rgba(0.45, 0.45, 0.45, lit); c.set_line_width(0.9); c.stroke()
    # 3 glass floor and back walls
    sc.box(-V, -V, ZV - 1.2, V, V, ZV, (GLASS, LEFT, RIGHT), alpha=0.18)
    sc.poly([(-V, -V, ZV), (-V, V, ZV), (-V, V, ZV + 7), (-V, -V, ZV + 7)], GLASS, alpha=0.9)
    sc.poly([(-V, -V, ZV), (V, -V, ZV), (V, -V, ZV + 7), (-V, -V, ZV + 7)], GLASS, alpha=0.9)

    # part slabs, lowest first; layer k sits at z [Pb-(k+1)T, Pb-kT]
    slabs = []
    for k in range(k_done):
        for (x0, y0, x1, y1) in shape(k):
            slabs.append((Pb - (k + 1) * T, (x0, y0, x1, y1), PART))
    if flash is not None and lit <= 0.3:
        for (x0, y0, x1, y1) in shape(flash):
            slabs.append((ZV, (x0, y0, x1, y1), PART))
    slabs.sort(key=lambda s: s[0])

    def draw_slabs(below):
        for z0, (x0, y0, x1, y1), cols in slabs:
            if (z0 + T <= LR + 0.01) == below:
                sc.box(x0, y0, z0, x1, y1, z0 + T, cols)

    draw_slabs(True)
    if Pb + 1.2 <= LR:
        sc.box(-11, -8, Pb, 11, 8, Pb + 1.2, (TOP, LEFT, RIGHT))
    # 4 resin
    sc.poly([(-V, V, ZV), (V, V, ZV), (V, V, LR), (-V, V, LR)], RESIN, alpha=0.30, stroke=None)
    sc.poly([(V, -V, ZV), (V, V, ZV), (V, V, LR), (V, -V, LR)], RESIN, alpha=0.38, stroke=None)
    sc.poly([(-V, -V, LR), (V, -V, LR), (V, V, LR), (-V, V, LR)], RESIN, alpha=0.42, stroke=(0.45, 0.45, 0.45), lw=0.8)
    # 5 the exposed layer glows through the resin; then everything above the resin
    if flash is not None and lit > 0.3:
        for (x0, y0, x1, y1) in shape(flash):
            z0, z1 = ZV, ZV + T
            sc.poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], LIT[0])
            sc.poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], LIT[1])
    draw_slabs(False)
    if Pb + 1.2 > LR:
        sc.box(-11, -8, Pb, 11, 8, Pb + 1.2, (TOP, LEFT, RIGHT))
    sc.box(-1.2, -1.2, Pb + 1.2, 1.2, 1.2, Pb + 18, (TOP, LEFT, RIGHT))
    sc.box(-4, -4, Pb + 18, 4, 4, Pb + 21, (TOP, LEFT, RIGHT))
    # 6 front glass walls and rim
    sc.poly([(-V, V, ZV), (V, V, ZV), (V, V, ZV + 7), (-V, V, ZV + 7)], GLASS, alpha=0.10)
    sc.poly([(V, -V, ZV), (V, V, ZV), (V, V, ZV + 7), (V, -V, ZV + 7)], GLASS, alpha=0.10)
    sc.poly([(-V, -V, ZV + 7), (V, -V, ZV + 7), (V, V, ZV + 7), (-V, V, ZV + 7)], None, stroke=INK, lw=1.1)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


frames = []
def frame(**kw):
    sc = Scene(ox=350, oy=384, s=5.5)
    draw(sc, **kw)
    frames.append(sc.image())

for i in range(12):                                   # intro: platform lowered to one layer above the glass
    frame(Pb=ZV + T, k_done=0)
for k in range(N):
    Pb = ZV + (k + 1) * T
    for i in range(8):                                # flash: the whole layer at once
        frame(Pb=Pb, k_done=k, flash=k, lit=1.0)
    for i in range(3):
        frame(Pb=Pb, k_done=k, flash=k, lit=0.0)
    for i in range(8):                                # peel: platform lifts
        frame(Pb=Pb + 6 * ease((i + 1) / 8), k_done=k + 1)
    if k < N - 1:
        for i in range(7):                            # back down, one layer higher than before
            frame(Pb=Pb + 6 - (6 - T) * ease((i + 1) / 7), k_done=k + 1)
Pend = ZV + N * T
top = LR + N * T + 1
for i in range(40):                                   # part rises out of the resin
    frame(Pb=Pend + 6 + (top - Pend - 6) * ease((i + 1) / 40), k_done=N)
for i in range(28):
    frame(Pb=top, k_done=N)
save_gif(frames, str(Path(__file__).with_suffix(".gif")))
print(len(frames), "frames")
