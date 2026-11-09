"""SLA animation: a laser spot traces each layer on the resin surface, the platform steps down,
a blade recoats; at the end the part rises out of the vat. Style and size of the MPP GIF."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from iso_anim import Scene, save_gif, TOP, LEFT, RIGHT, PART_TOP, PART_L, PART_R, INK
import math

V = 24.0          # vat half-width
L = 15.0          # resin level
T = 2.0           # layer thickness
N = 6             # layers
RESIN = (0.62, 0.62, 0.62)
GLASS = (0.93, 0.93, 0.93)
BEAM = (0.97, 0.97, 0.97)
PART = (PART_TOP, PART_L, PART_R)


def shape(k):
    """Section of layer k: list of rectangles (x0, y0, x1, y1). A stepped part."""
    return [(-10, -7, 10, 7)] if k < 3 else [(-10, -7, 0, 7)]


def path(k):
    """Laser path of layer k: contour then hatch lines along y, 2 units apart."""
    x0, y0, x1, y1 = shape(k)[0]
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    xs = [x0 + 1 + 2 * i for i in range(int((x1 - x0) / 2))]
    hatch = []
    for i, x in enumerate(xs):
        a, b = (y0 + 0.6, y1 - 0.6) if i % 2 == 0 else (y1 - 0.6, y0 + 0.6)
        hatch.append(((x, a), (x, b)))
    return pts, hatch


def draw(sc, P, k_done, scan=None, blade=None, beam_on=False, spot=None):
    """P: platform top z. k_done: number of finished layers on the platform.
    scan: (k, u) current layer and fraction scanned. blade: x of recoater."""
    # 1 vat floor and back walls
    sc.poly([(-V, -V, 0), (V, -V, 0), (V, V, 0), (-V, V, 0)], GLASS)
    sc.poly([(-V, -V, 0), (-V, V, 0), (-V, V, 20), (-V, -V, 20)], GLASS, alpha=0.9)
    sc.poly([(-V, -V, 0), (V, -V, 0), (V, -V, 20), (-V, -V, 20)], GLASS, alpha=0.9)

    def solids(below):
        items = []
        # platform plate
        items.append(((-14, -10, P - 1.2, 14, 10, P), (TOP, LEFT, RIGHT)))
        for k in range(k_done):
            for (x0, y0, x1, y1) in shape(k):
                items.append(((x0, y0, P + k * T, x1, y1, P + (k + 1) * T), PART))
        for (x0, y0, z0, x1, y1, z1), cols in items:
            is_below = z1 <= L + 0.01
            if is_below == below:
                sc.box(x0, y0, z0, x1, y1, z1, cols)
        # rod: split at the resin level
        z_lo, z_hi = P, P + 32
        if below and z_lo < L:
            sc.box(16, -1, z_lo, 18, 1, min(z_hi, L), (TOP, LEFT, RIGHT))
        if not below and z_hi > L:
            sc.box(16, -1, max(z_lo, L), 18, 1, z_hi, (TOP, LEFT, RIGHT))
            sc.box(14, -3, z_hi, 20, 3, z_hi + 3, (TOP, LEFT, RIGHT))

    solids(True)
    # 3 resin volume
    sc.poly([(-V, V, 0), (V, V, 0), (V, V, L), (-V, V, L)], RESIN, alpha=0.30, stroke=None)
    sc.poly([(V, -V, 0), (V, V, 0), (V, V, L), (V, -V, L)], RESIN, alpha=0.38, stroke=None)
    sc.poly([(-V, -V, L), (V, -V, L), (V, V, L), (-V, V, L)], RESIN, alpha=0.42, stroke=(0.45, 0.45, 0.45), lw=0.8)
    # 4 cured part of the current layer, on the surface
    if scan is not None:
        k, u = scan
        pts, hatch = path(k)
        n_c, n_h = len(pts) - 1, len(hatch)
        total = n_c + n_h
        done = u * total
        for i in range(n_h):
            f = min(max(done - n_c - i, 0), 1)
            if f <= 0:
                break
            (x, a), (_, b) = hatch[i]
            yb = a + (b - a) * f
            ylo, yhi = min(a, yb), max(a, yb)
            sc.poly([(x - 1, ylo, L), (x + 1, ylo, L), (x + 1, yhi, L), (x - 1, yhi, L)], PART_TOP, stroke=None)
        for i in range(n_c):
            f = min(max(done - i, 0), 1)
            if f <= 0:
                break
            (xa, ya), (xb, yb) = pts[i], pts[i + 1]
            sc.line((xa, ya, L), (xa + (xb - xa) * f, ya + (yb - ya) * f, L), col=INK, lw=1.6)
    solids(False)
    # 5 front glass walls
    sc.poly([(-V, V, 0), (V, V, 0), (V, V, 20), (-V, V, 20)], GLASS, alpha=0.10)
    sc.poly([(V, -V, 0), (V, V, 0), (V, V, 20), (V, -V, 20)], GLASS, alpha=0.10)
    sc.poly([(-V, -V, 20), (V, -V, 20), (V, V, 20), (-V, V, 20)], None, stroke=INK, lw=1.1)
    # 6 recoater blade
    if blade is not None:
        sc.box(blade - 0.8, -V + 1, L, blade + 0.8, V - 1, L + 3, (TOP, LEFT, RIGHT))
    # 7 laser, mirror, beam
    mirror = (-4.0, -4.0, 44.0)
    sc.box(-26, -6, 42, -12, -2, 46, (TOP, LEFT, RIGHT))
    sc.poly([(-12, -4.6, 43.4), (-12, -3.4, 43.4), (-12, -3.4, 44.6), (-12, -4.6, 44.6)], (0.3, 0.3, 0.3))
    if beam_on and spot is not None:
        sc.line((-12, -4, 44), mirror, col=(0.45, 0.45, 0.45), lw=5.0)
        sc.line((-12, -4, 44), mirror, col=BEAM, lw=3.0)
        sc.line(mirror, (spot[0], spot[1], L), col=(0.45, 0.45, 0.45), lw=5.0)
        sc.line(mirror, (spot[0], spot[1], L), col=BEAM, lw=3.0)
        c = sc.c
        x, y = sc.p(spot[0], spot[1], L)
        c.arc(x, y, 3.2, 0, 2 * math.pi)
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1); c.stroke()
    # mirror plate
    mx, my = sc.p(*mirror)
    c = sc.c
    c.save(); c.translate(mx, my); c.rotate(math.radians(-25))
    c.rectangle(-9, -2.2, 18, 4.4)
    c.set_source_rgb(0.45, 0.45, 0.45); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1); c.stroke()
    c.restore()


def spot_at(k, u):
    pts, hatch = path(k)
    n_c, n_h = len(pts) - 1, len(hatch)
    d = u * (n_c + n_h)
    if d < n_c:
        i = int(d); f = d - i
        (xa, ya), (xb, yb) = pts[i], pts[min(i + 1, len(pts) - 1)]
        return (xa + (xb - xa) * f, ya + (yb - ya) * f)
    i = min(int(d - n_c), n_h - 1); f = min(d - n_c - i, 1.0)
    (x, a), (_, b) = hatch[i]
    return (x, a + (b - a) * f)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


frames = []
def frame(**kw):
    sc = Scene(ox=350, oy=316, s=4.4)
    draw(sc, **kw)
    frames.append(sc.image())

P0 = L - T
for i in range(12):                                   # intro: vat, platform one layer below the surface
    frame(P=P0, k_done=0)
for k in range(N):
    P = L - (k + 1) * T
    nscan = 26 if k < 3 else 18
    for i in range(nscan):                            # laser traces contour, then hatches
        u = (i + 1) / nscan
        frame(P=P, k_done=k, scan=(k, u), beam_on=True, spot=spot_at(k, u))
    for i in range(6):                                # platform steps down by one layer
        Pn = P - T * ease((i + 1) / 6)
        frame(P=Pn, k_done=k + 1)
    if k < N - 1:
        for i in range(10):                           # blade spreads fresh resin
            frame(P=P - T, k_done=k + 1, blade=-V + 1 + (2 * V - 2) * (i + 1) / 10)
Pend = L - (N + 1) * T
for i in range(40):                                   # part rises out of the resin
    frame(P=Pend + (L + 4 - Pend) * ease((i + 1) / 40), k_done=N)
for i in range(30):
    frame(P=L + 4, k_done=N)
save_gif(frames, str(Path(__file__).with_suffix(".gif")))
print(len(frames), "frames")
