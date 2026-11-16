"""Powder DED animation (laser metal deposition, LMD / DED-LB powder): a coaxial nozzle blows metal powder
into a melt pool made by a laser; the nozzle travels along the wall, rises by one bead height and comes back.
Style and size of the SLA GIF."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from iso_anim import Scene, save_gif, TOP, LEFT, RIGHT, PART_TOP, PART_L, PART_R, INK
import math

X0, X1 = -10.0, 10.0      # wall ends
WB = 1.4                  # half bead width
HB = 1.7                  # bead height
N = 7
PART = (PART_TOP, PART_L, PART_R)
BEAM = (0.97, 0.97, 0.97)
GREY = (0.45, 0.45, 0.45)


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


def solid_of_revolution(sc, cx, cy, z0, z1, r0, r1, col=LEFT, top=None, n=40):
    """Frustum between radius r0 at z0 and r1 at z1, drawn as the hull of the two ellipses; optional top ellipse."""
    ring = lambda z, r: [sc.p(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n), z) for i in range(n)]
    h = hull([(round(u, 2), round(v, 2)) for (u, v) in ring(z0, r0) + ring(z1, r1)])
    c = sc.c
    c.move_to(*h[0])
    for q in h[1:]:
        c.line_to(*q)
    c.close_path()
    c.set_source_rgb(*col); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1.1); c.stroke()
    if top is not None:
        pts = ring(z1, r1)
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.close_path()
        c.set_source_rgb(*top); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()


def bead(sc, k, xa, xb):
    """Bead of layer k between xa and xb (xa < xb), on top of the substrate (z = 0)."""
    if xb - xa < 0.05:
        return
    sc.box(xa, -WB, k * HB, xb, WB, (k + 1) * HB, PART)


def nozzle(sc, x, zt, phase, on):
    """Coaxial nozzle with its tip at height zt above the melt pool at (x, 0)."""
    zp = zt - 5.0                                                    # melt-pool surface
    # powder streams behind the beam
    streams = [(math.cos(a), math.sin(a)) for a in (math.radians(d) for d in (45, 135, 225, 315))]
    def stream(dx, dy):
        if not on:
            return
        c = sc.c
        for j in range(8):
            t = (j / 8 + phase) % 1.0
            px, py, pz = x + 1.8 * dx * (1 - t), 1.8 * dy * (1 - t), zt - (zt - zp) * t
            u, v = sc.p(px, py, pz)
            c.arc(u, v, 1.4, 0, 2 * math.pi); c.set_source_rgb(0.3, 0.3, 0.3); c.fill()
    for dx, dy in streams:
        if dx + dy < 0:
            stream(dx, dy)
    if on:                                                           # laser beam in the gap and melt pool
        sc.line((x, 0, zt), (x, 0, zp), col=GREY, lw=5.0)
        sc.line((x, 0, zt), (x, 0, zp), col=BEAM, lw=3.0)
        c = sc.c
        u, v = sc.p(x, 0, zp)
        c.save(); c.translate(u, v); c.scale(1.0, 0.58); c.arc(0, 0, 9.5, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1); c.stroke()
    for dx, dy in streams:
        if dx + dy >= 0:
            stream(dx, dy)
    # nozzle cone, head, powder hoses
    solid_of_revolution(sc, x, 0, zt, zt + 8, 1.8, 5.0, LEFT)
    solid_of_revolution(sc, x, 0, zt + 8, zt + 14, 5.0, 5.0, LEFT, top=TOP)
    for sx in (-1, 1):                                               # powder hoses
        a = (x + sx * 3.5, -3.5, zt + 11)
        b = (x + sx * 8, -8, zt + 17)
        sc.line(a, b, col=INK, lw=4.0)
        sc.line(a, b, col=(0.8, 0.8, 0.8), lw=2.2)
    # optics column above the head, fed by the laser fibre
    sc.box(x - 2.4, -2.4, zt + 14, x + 2.4, 2.4, zt + 19, (TOP, LEFT, RIGHT))
    sc.line((x, 0, zt + 19), (x, 0, zt + 24), col=INK, lw=3.0)


def draw(sc, k_done, cur=None, x=None, zt=None, phase=0.0, on=False):
    """k_done finished layers; cur=(k, xa, xb) partial layer; nozzle at x with tip at zt."""
    sc.box(-15, -8, -3, 15, 8, 0, (TOP, LEFT, RIGHT))                     # substrate plate
    for k in range(k_done):
        bead(sc, k, X0, X1)
    if cur is not None:
        bead(sc, *cur)
    if x is not None:
        nozzle(sc, x, zt, phase, on)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


frames = []
def frame(**kw):
    sc = Scene(ox=350, oy=300, s=6.0)
    draw(sc, **kw)
    frames.append(sc.image())

if __name__ == "__main__":
    GAP = 5.0
    NF = 20
    for i in range(8):
        frame(k_done=0, x=X0, zt=GAP)
    ph = 0.0
    for k in range(N):
        zt = k * HB + GAP + HB * 0.0
        forward = (k % 2 == 0)
        for i in range(NF):
            f = (i + 1) / NF
            x = X0 + (X1 - X0) * f if forward else X1 - (X1 - X0) * f
            ph = (ph + 0.23) % 1.0
            cur = (k, X0, x) if forward else (k, x, X1)
            frame(k_done=k, cur=cur, x=x, zt=zt + HB, phase=ph, on=True)
        xe = X1 if forward else X0
        for i in range(3):                                            # nozzle rises by one bead height
            frame(k_done=k + 1, x=xe, zt=zt + HB + HB * ease((i + 1) / 3))
    for i in range(16):                                               # nozzle moves away
        frame(k_done=N, x=X0 + (X1 - X0) * 0 if N % 2 == 0 else X0, zt=N * HB + GAP + 4 * ease((i + 1) / 16))
    for i in range(24):
        frame(k_done=N, x=X0, zt=N * HB + GAP + 4)
    save_gif(frames, str(Path(__file__).with_suffix(".gif")))
    for j in (18, 60, 150, len(frames) - 5):
        frames[j].save(f"/tmp/h09_{j}.png")
    print(len(frames), "frames")
