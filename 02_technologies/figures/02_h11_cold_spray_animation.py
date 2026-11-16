"""Cold spray animation (CSAM): a heated, high-pressure gas is accelerated in a converging-diverging
(de Laval) nozzle; metal particles injected upstream leave the nozzle at supersonic speed and bond on impact
without melting. The nozzle sweeps the plate, the deposit grows pass after pass with tapered sides.
Style and size of the SLA GIF."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from iso_anim import Scene, save_gif, TOP, LEFT, RIGHT, PART_TOP, PART_L, PART_R, INK
import math

_h09 = Path(__file__).with_name("02_h09_ded_powder_animation.py")
_ns = {"__file__": str(_h09)}
exec(compile(_h09.read_text().split('if __name__ == "__main__":')[0], "h09", "exec"), _ns)
solid_of_revolution = _ns["solid_of_revolution"]

HL = 1.6                  # layer (pass) height
N = 7
STAND = 9.0               # stand-off distance, nozzle exit to the deposit
PART = (PART_TOP, PART_L, PART_R)


def layer_box(k):
    """Pass k: the deposit narrows as it grows (tapered walls, typical of cold spray)."""
    return (-12 + 0.7 * k, -5.5 + 0.45 * k, 12 - 0.7 * k, 5.5 - 0.45 * k)


def layer(sc, k, xa=None, xb=None):
    x0, y0, x1, y1 = layer_box(k)
    xa = x0 if xa is None else max(xa, x0)
    xb = x1 if xb is None else min(xb, x1)
    if xb - xa > 0.05:
        sc.box(xa, y0, k * HL, xb, y1, (k + 1) * HL, PART)


def nozzle(sc, x, ze, on, phase):
    """De Laval nozzle with its exit at height ze, above (x, 0)."""
    zs = ze - STAND
    c = sc.c
    if on:                                                       # particle jet: short streaks (no melting)
        for j in range(30):
            t = (j / 30 + phase + 0.31 * (j % 4)) % 1.0
            a = 2 * math.pi * ((j * 0.618) % 1.0)
            rr = (1.0 + 1.6 * t) * (0.3 + 0.7 * ((j * 0.37) % 1.0))
            px, py = x + rr * math.cos(a), rr * math.sin(a)
            z0 = ze - (ze - zs) * t
            z1 = min(ze, z0 + 2.2)
            sc.line((px, py, z0), (px, py, z1), col=(0.25, 0.25, 0.25), lw=1.8)
        u, v = sc.p(x, 0, zs)                                    # impact zone: flattened splats
        c.save(); c.translate(u, v); c.scale(1.0, 0.58); c.arc(0, 0, 14, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0.30, 0.30, 0.30, 0.45); c.fill()
    solid_of_revolution(sc, x, 0, ze, ze + 13, 2.5, 1.0, LEFT)             # diverging section
    solid_of_revolution(sc, x, 0, ze + 13, ze + 16, 1.0, 3.6, LEFT)        # converging section
    solid_of_revolution(sc, x, 0, ze + 16, ze + 21, 3.6, 3.6, LEFT, top=TOP)  # pre-chamber
    # powder feed (side) and hot gas line from the heater (top)
    sc.line((x + 3.0, 0, ze + 18), (x + 12, 0, ze + 24), col=INK, lw=4.0)
    sc.line((x + 3.0, 0, ze + 18), (x + 12, 0, ze + 24), col=(0.80, 0.80, 0.80), lw=2.2)
    sc.box(x - 2.2, -2.2, ze + 21, x + 2.2, 2.2, ze + 27, (TOP, LEFT, RIGHT))  # gas heater
    sc.line((x, 0, ze + 27), (x - 4, 0, ze + 33), col=INK, lw=4.0)
    sc.line((x, 0, ze + 27), (x - 4, 0, ze + 33), col=(0.80, 0.80, 0.80), lw=2.2)


def draw(sc, k_done, cur=None, x=None, ze=None, on=False, phase=0.0):
    sc.box(-16, -9, -3, 16, 9, 0, (TOP, LEFT, RIGHT))        # substrate plate
    for k in range(k_done):
        layer(sc, k)
    if cur is not None:
        layer(sc, *cur)
    if x is not None:
        nozzle(sc, x, ze, on, phase)


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


frames = []
def frame(**kw):
    sc = Scene(ox=350, oy=318, s=5.4)
    draw(sc, **kw)
    frames.append(sc.image())

if __name__ == "__main__":
    NF = 16
    XA, XB = -14.0, 14.0
    for i in range(8):
        frame(k_done=0, x=XA, ze=STAND)
    ph = 0.0
    for k in range(N):
        forward = (k % 2 == 0)
        ze = k * HL + STAND
        for i in range(NF):
            f = (i + 1) / NF
            x = XA + (XB - XA) * f if forward else XB - (XB - XA) * f
            ph = (ph + 0.29) % 1.0
            frame(k_done=k, cur=(k, -99, x) if forward else (k, x, 99), x=x, ze=ze, on=True, phase=ph)
        xe = XB if forward else XA
        for i in range(3):
            frame(k_done=k + 1, x=xe, ze=ze + HL * ease((i + 1) / 3))
    xe = XB if N % 2 == 1 else XA
    for i in range(12):
        frame(k_done=N, x=xe, ze=N * HL + STAND + 3 * ease((i + 1) / 12))
    for i in range(24):
        frame(k_done=N, x=xe, ze=N * HL + STAND + 3)
    save_gif(frames, str(Path(__file__).with_suffix(".gif")))
    for j in (14, 60, 120, len(frames) - 5):
        frames[j].save(f"/tmp/h11_{j}.png")
    print(len(frames), "frames")
