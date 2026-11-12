"""Tomographic volumetric printing (Readily3D, PERFI; Kelly et al. 2019, Loterie et al. 2020):
a glass vial of resin turns; a projector beside it sends, at every angle, the matching image.
The light dose adds up everywhere, but only inside the part does it pass the gel threshold:
the whole part appears at once, without layers or supports. Greyscale isometric line art,
same style as 02_h01-h03. Usage: python 02_h06_tomographic_animation.py"""
import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from iso_anim import Scene, save_gif, TOP, LEFT, RIGHT, PART_TOP, PART_L, PART_R, INK

R, Z0, Z1 = 13.0, 0.0, 30.0         # vial radius, bottom, top
RESIN = (0.62, 0.62, 0.62)
PART = (PART_TOP, PART_L, PART_R)


def ellipse(sc, z, r=R, n=60):
    return [sc.p(r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n), z) for i in range(n)]


def path(c, pts, close=True):
    c.move_to(*pts[0])
    for q in pts[1:]:
        c.line_to(*q)
    if close:
        c.close_path()


def part_boxes(a):
    """A small arch (two pillars and a beam) turning with the vial by angle a."""
    out = []
    for (x0, y0, z0, x1, y1, z1) in [(-6, -2.5, 4, -2, 2.5, 20), (2, -2.5, 4, 6, 2.5, 20), (-6, -2.5, 20, 6, 2.5, 25)]:
        out.append((x0, y0, z0, x1, y1, z1))
    return out, a


def rot(x, y, a):
    return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def rbox(sc, b, a, cols, alpha, stroke=INK):
    """Box rotated about the vial axis: faces as rotated polygons, back faces first."""
    x0, y0, z0, x1, y1, z1 = b
    rc = [rot(x, y, a) for x, y in [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]]
    faces = []
    for i in range(4):
        (xa, ya), (xb, yb) = rc[i], rc[(i + 1) % 4]
        shade = LEFT if abs(xb - xa) > abs(yb - ya) else RIGHT
        faces.append(((xa + xb) / 2 + (ya + yb) / 2, [(xa, ya, z0), (xb, yb, z0), (xb, yb, z1), (xa, ya, z1)], shade))
    for d, f, col in sorted(faces):
        sc.poly(f, col, alpha=alpha, stroke=stroke, lw=0.9)
    sc.poly([(x, y, z1) for x, y in rc], cols[0], alpha=alpha, stroke=stroke, lw=0.9)


def draw(sc, a, dose, beam_on=True):
    c = sc.c
    top, bot = ellipse(sc, Z1), ellipse(sc, Z0)
    xs = [q[0] for q in top]
    il, ir = xs.index(min(xs)), xs.index(max(xs))
    # turntable under the vial
    sc.box(-11, -11, -5, 11, 11, Z0 - 0.01, (TOP, LEFT, RIGHT))
    # projector on the -x side; its lens shows the image for the current angle
    sc.box(-46, -9, 6, -32, 9, 24, (TOP, LEFT, RIGHT))
    xl = -32.0
    sc.poly([(xl, -6, 9), (xl, 6, 9), (xl, 6, 21), (xl, -6, 21)], (0.97, 0.97, 0.97), lw=0.9)
    # back of the vial and resin
    c.set_source_rgba(*RESIN, 0.30); path(c, bot); c.fill()
    # beam: translucent slab from the lens to the vial axis
    if beam_on:
        sc.poly([(xl, 6, 9), (0, 6, 9), (0, 6, 21), (xl, 6, 21)], (1, 1, 1), alpha=0.55, stroke=(0.62, 0.62, 0.62), lw=0.7)
        sc.poly([(xl, -6, 21), (0, -6, 21), (0, 6, 21), (xl, 6, 21)], (1, 1, 1), alpha=0.55, stroke=(0.62, 0.62, 0.62), lw=0.7)
        for k in range(6):                                   # image: bars that change as the vial turns
            yy = -5 + 2 * k + 0.6 * math.sin(2 * a + k)
            w = 0.5 + 0.45 * (1 + math.cos(3 * a + 1.7 * k))
            sc.poly([(xl, yy, 10), (xl, yy + w, 10), (xl, yy + w, 20), (xl, yy, 20)], (0.35, 0.35, 0.35), stroke=None)
    # resin column (front)
    c.set_source_rgba(*RESIN, 0.22)
    c.move_to(*top[il]); c.line_to(*bot[il])
    i = il
    while i != ir:
        i = (i - 1) % 60
        c.line_to(*bot[i])
    c.line_to(*top[ir])
    i = ir
    while i != il:
        i = (i - 1) % 60
        c.line_to(*top[i])
    c.close_path(); c.fill()
    # part: faint ghost while the dose builds up, solid once over the threshold
    boxes, _ = part_boxes(a)
    if dose > 0:
        if dose < 0.85:
            for b in boxes:
                rbox(sc, b, a, PART, 0.10 * dose / 0.85, stroke=(0.62, 0.62, 0.62))
        else:
            for b in sorted(boxes, key=lambda b: (b[2], b[0])):
                rbox(sc, b, a, PART, 1.0)
    # vial outline and a mark on the rim that shows the rotation
    c.set_source_rgb(*INK); c.set_line_width(1.1)
    path(c, top); c.stroke()
    for j in (il, ir):
        c.move_to(*top[j]); c.line_to(*bot[j]); c.stroke()
    c.move_to(*bot[il]); i = il
    while i != ir:
        i = (i - 1) % 60
        c.line_to(*bot[i])
    c.stroke()
    mx, my = R * math.cos(a + 0.8), R * math.sin(a + 0.8)
    c.arc(*sc.p(mx, my, Z1), 3.4, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()


frames = []
def frame(**kw):
    sc = Scene(ox=440, oy=318, s=6.0)
    draw(sc, **kw)
    frames.append(sc.image())

N = 110
for i in range(10):
    frame(a=0.0, dose=0.0, beam_on=False)
for i in range(N):                                   # vial turns, dose builds up
    t = (i + 1) / N
    frame(a=2 * math.pi * 1.5 * t, dose=0.85 * t ** 1.5)
for i in range(6):                                   # threshold passed: the part appears
    frame(a=3 * math.pi + 0.05 * i, dose=1.0)
for i in range(30):
    frame(a=3 * math.pi + 0.3, dose=1.0, beam_on=False)
save_gif(frames, str(Path(__file__).with_suffix(".gif")))
print(len(frames), "frames")
