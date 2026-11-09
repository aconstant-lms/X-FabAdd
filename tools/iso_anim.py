"""Isometric line-art helpers for the AM process animations (style of the multiphoton GIF). Used by 02_technologies/figures/02_h*_animation.py."""
import math
import cairo
from PIL import Image

W, H = 700, 438
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))

INK = (0.23, 0.23, 0.23)
TOP, LEFT, RIGHT = (0.90, 0.90, 0.90), (0.80, 0.80, 0.80), (0.72, 0.72, 0.72)
PART_TOP, PART_L, PART_R = (0.62, 0.62, 0.62), (0.52, 0.52, 0.52), (0.45, 0.45, 0.45)


class Scene:
    def __init__(self, ox=350, oy=290, s=5.0):
        self.ox, self.oy, self.s = ox, oy, s
        self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
        self.c = cairo.Context(self.surf)
        self.c.set_source_rgb(1, 1, 1)
        self.c.paint()
        self.c.set_line_join(cairo.LINE_JOIN_ROUND)

    def p(self, x, y, z):
        return (self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * S30 * self.s - z * self.s)

    def poly(self, pts3, fill=None, alpha=1.0, stroke=INK, lw=1.1):
        c = self.c
        pts = [self.p(*q) for q in pts3]
        c.move_to(*pts[0])
        for q in pts[1:]:
            c.line_to(*q)
        c.close_path()
        if fill is not None:
            c.set_source_rgba(*fill, alpha)
            if stroke is not None:
                c.fill_preserve()
            else:
                c.fill()
        if stroke is not None:
            c.set_source_rgb(*stroke)
            c.set_line_width(lw)
            c.stroke()
        else:
            c.new_path()

    def line(self, a, b, col=INK, lw=1.1, alpha=1.0):
        c = self.c
        c.move_to(*self.p(*a))
        c.line_to(*self.p(*b))
        c.set_source_rgba(*col, alpha)
        c.set_line_width(lw)
        c.stroke()

    def box(self, x0, y0, z0, x1, y1, z1, cols=(TOP, LEFT, RIGHT), alpha=1.0, stroke=INK, lw=1.1):
        """Visible faces for a viewer looking from +x, +y, +z: top, face y=y1 (left), face x=x1 (right)."""
        top, left, right = cols
        self.poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], left, alpha, stroke, lw)
        self.poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], right, alpha, stroke, lw)
        self.poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, alpha, stroke, lw)

    def cylinder(self, cx, cy, z0, z1, r, col=TOP, n=40):
        """Vertical cylinder, drawn as body + top ellipse."""
        c = self.c
        pts_top = [self.p(cx + r * math.cos(t), cy + r * math.sin(t), z1) for t in [2 * math.pi * i / n for i in range(n)]]
        pts_bot = [self.p(cx + r * math.cos(t), cy + r * math.sin(t), z0) for t in [2 * math.pi * i / n for i in range(n)]]
        xs_t = [q[0] for q in pts_top]
        il, ir = xs_t.index(min(xs_t)), xs_t.index(max(xs_t))
        # body: outline from left extreme down, along the front of the bottom ellipse, up the right extreme
        c.move_to(*pts_top[il])
        c.line_to(*pts_bot[il])
        i = il
        while i != ir:
            i = (i - 1) % n
            c.line_to(*pts_bot[i])
        c.line_to(*pts_top[ir])
        c.close_path()
        c.set_source_rgb(*LEFT)
        c.fill_preserve()
        c.set_source_rgb(*INK)
        c.set_line_width(1.1)
        c.stroke()
        c.move_to(*pts_top[0])
        for q in pts_top[1:]:
            c.line_to(*q)
        c.close_path()
        c.set_source_rgb(*col)
        c.fill_preserve()
        c.set_source_rgb(*INK)
        c.stroke()

    def image(self):
        buf = self.surf.get_data()
        im = Image.frombuffer("RGBA", (W, H), bytes(buf), "raw", "BGRA", 0, 1).convert("RGB")
        return im


def save_gif(frames, path, ms=40):
    """Greyscale palette; pure white background becomes transparent, as in the MPP GIF."""
    pal = []
    for g in range(255):
        v = round(g * 254 / 254)
        pal += [v, v, v]
    pal += [255, 255, 255]           # index 255 = transparent white
    out = []
    for im in frames:
        L = im.convert("L")
        px = L.load()
        P = Image.new("P", L.size)
        P.putpalette(pal)
        data = [255 if v == 255 else min(v, 254) for v in L.getdata()]
        P.putdata(data)
        out.append(P)
    out[0].save(path, save_all=True, append_images=out[1:], duration=ms, loop=0,
                transparency=255, disposal=2, optimize=True)
