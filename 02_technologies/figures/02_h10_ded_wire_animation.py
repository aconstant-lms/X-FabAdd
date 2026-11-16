"""Wire DED animation (wire arc additive manufacturing, WAAM / DED-Arc): a welding torch melts a wire,
fed from a spool, in an electric arc; the torch lays a bead along the wall, rises by one bead height and
comes back. Style and size of the SLA GIF."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from iso_anim import Scene, save_gif, TOP, LEFT, RIGHT, PART_TOP, PART_L, PART_R, INK
import math

# reuse the frustum helper of the powder DED animation without running it
_src = Path(__file__).with_name("02_h09_ded_powder_animation.py").read_text().split('if __name__ == "__main__":')[0]
_ns = {"__file__": str(Path(__file__).with_name("02_h09_ded_powder_animation.py"))}
exec(compile(_src, "h09", "exec"), _ns)
solid_of_revolution = _ns["solid_of_revolution"]

X0, X1 = -11.0, 11.0
WB = 2.2                  # half bead width (wire beads are wider than powder beads)
HB = 2.4                  # bead height
N = 5
PART = (PART_TOP, PART_L, PART_R)
WIRE = (0.35, 0.35, 0.35)


def bead(sc, k, xa, xb):
    if xb - xa < 0.05:
        return
    sc.box(xa, -WB, k * HB, xb, WB, (k + 1) * HB, PART)


def feeder(sc):
    """Wire feeder with its spool, behind the plate."""
    sc.box(-4, -30, -3, 6, -22, 5, (TOP, LEFT, RIGHT))
    sc.cylinder(1, -26, 5, 7.5, 4.2, col=(0.80, 0.80, 0.80))
    c = sc.c
    u, v = sc.p(1, -26, 7.5)
    c.save(); c.translate(u, v); c.scale(1.0, 0.58)
    for r in (6, 10, 14, 18):
        c.arc(0, 0, r * 1.0, 0, 2 * math.pi)
        c.set_source_rgb(*WIRE); c.set_line_width(0.6); c.stroke()
    c.restore()


def torch(sc, x, zp, on, phase):
    """Torch above the melt pool at (x, 0, zp): wire stick-out, arc, gas cup, body and hose to the feeder."""
    zc = zp + 4.5                                   # bottom of the gas cup
    c = sc.c
    if on:
        # arc: a bright cone from the wire tip to the pool, with a flicker
        u, v = sc.p(x, 0, zp)
        c.save(); c.translate(u, v); c.scale(1.0, 0.58); c.arc(0, 0, 13, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(1); c.stroke()
        tip = sc.p(x, 0, zp + 1.8)
        c.move_to(*tip); c.line_to(u - 8, v); c.line_to(u + 8, v); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(0.40, 0.40, 0.40); c.set_line_width(1.2); c.stroke()
        for i in range(8):                          # light rays
            a = 2 * math.pi * (i / 8 + phase / 8)
            r0, r1 = 16 + 3 * math.sin(7 * phase + i), 27 + 5 * math.sin(5 * phase + 2 * i)
            c.move_to(u + r0 * math.cos(a), v - 6 + r0 * 0.7 * math.sin(a))
            c.line_to(u + r1 * math.cos(a), v - 6 + r1 * 0.7 * math.sin(a))
            c.set_source_rgb(0.45, 0.45, 0.45); c.set_line_width(1.4); c.stroke()
    sc.line((x, 0, zp + (1.8 if on else 2.6)), (x, 0, zc), col=WIRE, lw=2.4)      # wire stick-out
    solid_of_revolution(sc, x, 0, zc, zc + 5, 1.6, 3.2, LEFT)                     # gas cup
    solid_of_revolution(sc, x, 0, zc + 5, zc + 13, 3.2, 3.2, LEFT, top=TOP)       # torch body
    # hose (cable + wire liner) from the torch top to the feeder
    a = sc.p(x, 0, zc + 13)
    b = sc.p(-2, -22, 5)
    m1 = sc.p(x, 0, zc + 22)
    m2 = sc.p(-2, -22, 18)
    for col, lw in ((INK, 5.0), ((0.80, 0.80, 0.80), 3.0)):
        c.move_to(*a); c.curve_to(*m1, *m2, *b)
        c.set_source_rgb(*col); c.set_line_width(lw); c.stroke()


def draw(sc, k_done, cur=None, x=None, zp=None, on=False, phase=0.0):
    feeder(sc)
    sc.box(-15, -8, -3, 15, 8, 0, (TOP, LEFT, RIGHT))        # substrate plate
    for k in range(k_done):
        bead(sc, k, X0, X1)
    if cur is not None:
        bead(sc, *cur)
    if x is not None:
        torch(sc, x, zp, on, phase)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


frames = []
def frame(**kw):
    sc = Scene(ox=340, oy=300, s=6.0)
    draw(sc, **kw)
    frames.append(sc.image())

if __name__ == "__main__":
    NF = 22
    for i in range(8):
        frame(k_done=0, x=X0, zp=1.0)
    ph = 0.0
    for k in range(N):
        forward = (k % 2 == 0)
        for i in range(NF):
            f = (i + 1) / NF
            x = X0 + (X1 - X0) * f if forward else X1 - (X1 - X0) * f
            ph += 0.9
            frame(k_done=k, cur=(k, X0, x) if forward else (k, x, X1), x=x, zp=(k + 1) * HB, on=True, phase=ph)
        xe = X1 if forward else X0
        for i in range(4):                                   # arc off, torch rises by one bead
            frame(k_done=k + 1, x=xe, zp=(k + 1) * HB + HB * ease((i + 1) / 4))
    xe = X1 if N % 2 == 1 else X0
    for i in range(12):
        frame(k_done=N, x=xe, zp=(N + 1) * HB + 3 * ease((i + 1) / 12))
    for i in range(24):
        frame(k_done=N, x=xe, zp=(N + 1) * HB + 3)
    save_gif(frames, str(Path(__file__).with_suffix(".gif")))
    for j in (18, 70, 125, len(frames) - 5):
        frames[j].save(f"/tmp/h10_{j}.png")
    print(len(frames), "frames")
