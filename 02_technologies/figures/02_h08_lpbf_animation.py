"""LPBF animation (laser powder bed fusion): a laser, steered by a galvanometer mirror, melts each layer
of a metal powder bed; the build piston steps down, the supply piston rises, a blade spreads fresh powder.
At the end the loose powder is removed and the part stands on the build plate. Style and size of the SLA GIF."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from iso_anim import Scene, save_gif, TOP, LEFT, RIGHT, PART_TOP, PART_L, PART_R, INK
import math
import random

B = 12.0            # build well half-width (x and y), centred at x = 0
SX0, SX1 = -40.0, -18.0   # supply well
D = 26.0            # well depth
T = 2.0             # layer thickness (drawn)
N = 7
POWDER = (0.70, 0.70, 0.70)
GLASS = (0.93, 0.93, 0.93)
BEAM = (0.97, 0.97, 0.97)
PART = (PART_TOP, PART_L, PART_R)
MELT = (0.40, 0.40, 0.40)
FLOOR = ((0.86, 0.86, 0.86), (0.76, 0.76, 0.76), (0.68, 0.68, 0.68))


def shape(k):
    """Section of layer k: a base, then two posts (a U-shaped bracket)."""
    return [(-9, -6, 9, 6)] if k < 3 else [(-9, -6, -3, 6), (3, -6, 9, 6)]


def path(k):
    """Laser path: contours of each island, then hatch lines along y, 2 units apart."""
    contours, hatch = [], []
    for (x0, y0, x1, y1) in shape(k):
        contours.append([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)])
        for i in range(int((x1 - x0) / 2)):
            x = x0 + 1 + 2 * i
            a, b = (y0 + 0.6, y1 - 0.6) if i % 2 == 0 else (y1 - 0.6, y0 + 0.6)
            hatch.append(((x, a), (x, b)))
    segs = []
    for c in contours:
        segs += [(c[i], c[i + 1]) for i in range(4)]
    return segs, hatch


rng = random.Random(7)
DOTS_B = [(rng.uniform(-B + 0.6, B - 0.6), rng.uniform(-B + 0.6, B - 0.6)) for _ in range(150)]
DOTS_S = [(rng.uniform(SX0 + 0.6, SX1 - 0.6), rng.uniform(-B + 0.6, B - 0.6)) for _ in range(150)]


def dots(sc, pts, z, skip=None, alpha=1.0):
    c = sc.c
    for (x, y) in pts:
        if skip and any(x0 - 0.3 < x < x1 + 0.3 and y0 - 0.3 < y < y1 + 0.3 for (x0, y0, x1, y1) in skip):
            continue
        u, v = sc.p(x, y, z)
        c.arc(u, v, 0.9, 0, 2 * math.pi)
        c.set_source_rgba(0.38, 0.38, 0.38, alpha)
        c.fill()


def powder(sc, x0, x1, zb, alpha=1.0):
    """Powder volume in a well from piston top zb to the floor level 0."""
    if zb >= -0.01 or alpha <= 0:
        return
    sc.poly([(x0, B, zb), (x1, B, zb), (x1, B, 0), (x0, B, 0)], POWDER, alpha=0.40 * alpha, stroke=None)
    sc.poly([(x1, -B, zb), (x1, B, zb), (x1, B, 0), (x1, -B, 0)], POWDER, alpha=0.50 * alpha, stroke=None)
    sc.poly([(x0, -B, 0), (x1, -B, 0), (x1, B, 0), (x0, B, 0)], POWDER, alpha=0.55 * alpha, stroke=(0.5, 0.5, 0.5), lw=0.8)


FX0, FX1, FY, FZ = -46.0, 18.0, 16.0, -D - 4.0   # machine body (cut-away glass, as the SLA vat)
WALL = (0.55, 0.55, 0.55)


def body_back(sc):
    sc.poly([(FX0, -FY, FZ), (FX1, -FY, FZ), (FX1, FY, FZ), (FX0, FY, FZ)], GLASS)
    sc.poly([(FX0, -FY, FZ), (FX0, FY, FZ), (FX0, FY, 0), (FX0, -FY, 0)], GLASS, alpha=0.9)
    sc.poly([(FX0, -FY, FZ), (FX1, -FY, FZ), (FX1, -FY, 0), (FX0, -FY, 0)], GLASS, alpha=0.9)


def well_back(sc, x0, x1):
    for a, b in [((x0, -B, -D), (x1, -B, -D)), ((x0, -B, -D), (x0, B, -D)), ((x0, -B, -D), (x0, -B, 0)),
                 ((x1, -B, -D), (x1, -B, 0)), ((x0, B, -D), (x0, B, 0))]:
        sc.line(a, b, col=WALL, lw=0.8)


def well_front(sc, x0, x1):
    for a, b in [((x0, B, -D), (x1, B, -D)), ((x1, -B, -D), (x1, B, -D)), ((x1, B, -D), (x1, B, 0))]:
        sc.line(a, b, col=WALL, lw=0.8)


def piston(sc, x0, x1, z):
    sc.box(x0 + 0.4, -B + 0.4, z - 1.6, x1 - 0.4, B - 0.4, z, (TOP, LEFT, RIGHT))
    sc.box((x0 + x1) / 2 - 1, -1, -D - 2, (x0 + x1) / 2 + 1, 1, z - 1.6, (TOP, LEFT, RIGHT))


def floor(sc):
    """Machine deck at z = 0 around the two wells (drawn as strips), with a thickness of 2."""
    fx0, fx1, fy = FX0, FX1, FY
    top = FLOOR[0]
    for (x0, y0, x1, y1) in [(fx0, -fy, fx1, -B), (fx0, B, fx1, fy), (fx0, -B, SX0, B), (SX1, -B, -B, B), (B, -B, fx1, B)]:
        sc.poly([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], top, stroke=None)
    sc.poly([(fx0, -fy, 0), (fx1, -fy, 0), (fx1, fy, 0), (fx0, fy, 0)], None, stroke=INK)
    for (x0, x1) in [(SX0, SX1), (-B, B)]:
        sc.poly([(x0, -B, 0), (x1, -B, 0), (x1, B, 0), (x0, B, 0)], None, stroke=INK)


def draw(sc, zb, zs, k_done, scan=None, blade=None, spot=None, pa=1.0):
    """zb, zs: build and supply piston tops; k_done: finished layers; scan=(k, u); blade: x of recoater;
    pa: powder opacity (1 during the build, fades to 0 when the part is unpacked)."""
    body_back(sc)
    well_back(sc, SX0, SX1)
    well_back(sc, -B, B)
    piston(sc, SX0, SX1, zs)

    def build(below):
        """Build plate and part, split at the deck level z = 0 (as the SLA rod at the resin level)."""
        items = [((-B + 0.4, -B + 0.4, zb - 1.6, B - 0.4, B - 0.4, zb), (TOP, LEFT, RIGHT))]
        for k in range(k_done):
            for (x0, y0, x1, y1) in shape(k):
                items.append(((x0, y0, zb + k * T, x1, y1, zb + (k + 1) * T), PART))
        if below:
            sc.box(-1, -1, -D - 2, 1, 1, zb - 1.6, (TOP, LEFT, RIGHT))
        for (x0, y0, z0, x1, y1, z1), cols in items:
            if below and z0 < 0:
                sc.box(x0, y0, z0, x1, y1, min(z1, 0), cols)
            if not below and z1 > 0:
                sc.box(x0, y0, max(z0, 0), x1, y1, z1, cols)
    build(True)
    powder(sc, SX0, SX1, zs)
    powder(sc, -B, B, zb, pa)
    dots(sc, DOTS_S, 0)
    if pa > 0:
        dots(sc, DOTS_B, 0, skip=None, alpha=pa)
    # current layer: melted tracks on the powder surface
    if scan is not None:
        k, u = scan
        segs, hatch = path(k)
        n_c, n_h = len(segs), len(hatch)
        done = u * (n_c + n_h)
        for i in range(n_h):
            f = min(max(done - n_c - i, 0), 1)
            if f <= 0:
                break
            (x, a), (_, b) = hatch[i]
            yb = a + (b - a) * f
            ylo, yhi = min(a, yb), max(a, yb)
            sc.poly([(x - 1, ylo, 0), (x + 1, ylo, 0), (x + 1, yhi, 0), (x - 1, yhi, 0)], MELT, stroke=None)
        for i in range(n_c):
            f = min(max(done - i, 0), 1)
            if f <= 0:
                break
            (xa, ya), (xb, yb) = segs[i]
            sc.line((xa, ya, 0), (xa + (xb - xa) * f, ya + (yb - ya) * f, 0), col=INK, lw=1.6)
    well_front(sc, SX0, SX1)
    well_front(sc, -B, B)
    floor(sc)
    sc.poly([(FX0, FY, FZ), (FX1, FY, FZ), (FX1, FY, 0), (FX0, FY, 0)], GLASS, alpha=0.10)
    sc.poly([(FX1, -FY, FZ), (FX1, FY, FZ), (FX1, FY, 0), (FX1, -FY, 0)], GLASS, alpha=0.10)
    build(False)
    # recoater blade with a small heap of powder in front of it
    if blade is not None:
        sc.poly([(blade + 0.8, -B + 1, 0), (blade + 3.2, -B + 1, 0), (blade + 0.8, -B + 1, 1.8)], POWDER, stroke=INK, lw=0.8)
        sc.poly([(blade + 0.8, B - 1, 0), (blade + 3.2, B - 1, 0), (blade + 0.8, B - 1, 1.8)], POWDER, stroke=INK, lw=0.8)
        sc.poly([(blade + 3.2, -B + 1, 0), (blade + 3.2, B - 1, 0), (blade + 0.8, B - 1, 1.8), (blade + 0.8, -B + 1, 1.8)], POWDER, stroke=INK, lw=0.8)
        sc.box(blade - 0.8, -B - 1, 0.2, blade + 0.8, B + 1, 4, (TOP, LEFT, RIGHT))
    # laser source, galvo mirror, beam
    mirror = (-4.0, -4.0, 28.0)
    sc.box(-30, -6, 26, -16, -2, 30, (TOP, LEFT, RIGHT))
    sc.poly([(-16, -4.6, 27.4), (-16, -3.4, 27.4), (-16, -3.4, 28.6), (-16, -4.6, 28.6)], (0.3, 0.3, 0.3))
    c = sc.c
    if spot is not None:
        for a, b in [((-16, -4, 28), mirror), (mirror, (spot[0], spot[1], 0))]:
            sc.line(a, b, col=(0.45, 0.45, 0.45), lw=5.0)
            sc.line(a, b, col=BEAM, lw=3.0)
        x, y = sc.p(spot[0], spot[1], 0)
        c.arc(x, y, 4.2, 0, 2 * math.pi)
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1); c.stroke()
        r = random.Random(int(spot[0] * 97 + spot[1] * 13))
        for _ in range(5):                                     # spatter
            a = r.uniform(0, 2 * math.pi); d = r.uniform(7, 16)
            c.arc(x + d * math.cos(a), y - abs(d * math.sin(a)) * 0.9, 1.1, 0, 2 * math.pi)
            c.set_source_rgb(0.3, 0.3, 0.3); c.fill()
    mx, my = sc.p(*mirror)
    c.save(); c.translate(mx, my); c.rotate(math.radians(-25))
    c.rectangle(-9, -2.2, 18, 4.4)
    c.set_source_rgb(0.45, 0.45, 0.45); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1); c.stroke()
    c.restore()


def spot_at(k, u):
    segs, hatch = path(k)
    n_c, n_h = len(segs), len(hatch)
    d = u * (n_c + n_h)
    if d < n_c:
        i = int(d); f = d - i
        (xa, ya), (xb, yb) = segs[i]
        return (xa + (xb - xa) * f, ya + (yb - ya) * f)
    i = min(int(d - n_c), n_h - 1); f = min(d - n_c - i, 1.0)
    (x, a), (_, b) = hatch[i]
    return (x, a + (b - a) * f)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


frames = []
def frame(**kw):
    sc = Scene(ox=404, oy=226, s=4.4)
    draw(sc, **kw)
    frames.append(sc.image())

if __name__ == "__main__":
    ZS0 = -D + 3.0                            # supply piston start: full of powder
    for i in range(10):
        frame(zb=-T, zs=ZS0 - 0 * T, k_done=0)
    for k in range(N):
        zb, zs = -(k + 1) * T, ZS0 + k * T
        nscan = 16
        for i in range(nscan):
            u = (i + 1) / nscan
            frame(zb=zb, zs=zs, k_done=k, scan=(k, u), spot=spot_at(k, u))
        if k == N - 1:
            break
        for i in range(5):                                    # build piston down, supply piston up
            e = ease((i + 1) / 5)
            frame(zb=zb - T * e, zs=zs + T * e, k_done=k + 1)
        for i in range(8):                                    # blade spreads powder from the supply to the build well
            frame(zb=zb - T, zs=zs + T, k_done=k + 1, blade=SX0 - 2 + (B + 2 - SX0 + 2) * (i + 1) / 8)
        for i in range(2):
            frame(zb=zb - T, zs=zs + T, k_done=k + 1)
        # (blade goes back between frames; the next layer starts with the blade parked)
    zb_end, zs_end = -N * T, ZS0 + (N - 1) * T
    for i in range(10):
        frame(zb=zb_end, zs=zs_end, k_done=N)
    for i in range(16):                                       # unpacking: the loose powder is removed
        frame(zb=zb_end, zs=zs_end, k_done=N, pa=1 - (i + 1) / 16)
    for i in range(20):                                       # the plate rises with the part
        frame(zb=zb_end + (2.0 - zb_end) * ease((i + 1) / 20), zs=zs_end, k_done=N, pa=0)
    for i in range(25):
        frame(zb=2.0, zs=zs_end, k_done=N, pa=0)
    save_gif(frames, str(Path(__file__).with_suffix(".gif")))
    for j in (30, 90, len(frames) - 5):
        frames[j].save(f"/tmp/h08_{j}.png")
    print(len(frames), "frames")
