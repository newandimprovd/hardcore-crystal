"""Procedural creature toolkit for the Hardcore Crystal Pokemon sprites (front 56x56, back 48x48, four colours).

A Scene is one drawing: every coordinate is given in a 56x56 "design space" and mapped to the canvas by the stage scale (a stage 3 form is
drawn smaller than a stage 4 form, anchored at the feet) and by the back-view factor (48/56).  Shapes are smooth masks at 8x (pixart.Mask)
that are painted back to front with a black outline and ordered-dither shading.  Palette indices: 0 white, 1 body, 2 accent, 3 black.

Menace: scene.m runs from 0 to 1.  A stage 4 form is drawn at 1.0 and uses it for horns, spikes, fangs and eye angle; stage 3 forms are drawn
at 0.35.  Poses (front view animation): scene.pose carries {"head": (dx, dy), "mouth": 0/1, "glow": 0/1, "sway": float}.
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pixart import BAYER, Canvas, Mask, erode  # noqa: E402

DESIGN = 56.0
GROUND = 52.0
CX = 28.0


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def spline(pts, s):
    """Catmull-Rom through pts, s in 0..1."""
    n = len(pts) - 1
    t = min(max(s, 0), 0.9999) * n
    i = int(t)
    u = t - i
    p0 = pts[max(i - 1, 0)]
    p1 = pts[i]
    p2 = pts[min(i + 1, n)]
    p3 = pts[min(i + 2, n)]
    out = []
    for k in (0, 1):
        out.append(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u * u
                          + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u ** 3))
    return out[0], out[1]


class Scene:
    def __init__(self, view="front", stage=4, menace=None, seed=0, pose=None):
        self.view = view
        self.back = view == "back"
        self.stage = stage
        self.n = 48 if self.back else 56
        self.k = self.n / DESIGN
        self.s = 1.0 if stage >= 4 else 0.8
        self.m = (1.0 if stage >= 4 else 0.35) if menace is None else menace
        self.cv = Canvas(self.n)
        self.pose = pose or {}
        self.rng = random.Random(seed * 7919 + (1 if self.back else 0))

    # ---- coordinate mapping
    def X(self, x):
        return (CX + (x - CX) * self.s) * self.k

    def Y(self, y):
        return (GROUND + 1 - (GROUND + 1 - y) * self.s) * self.k

    def P(self, pts):
        return [(self.X(x), self.Y(y)) for x, y in pts]

    def R(self, r):
        return r * self.s * self.k

    # ---- pose helpers
    def head(self):
        dx, dy = self.pose.get("head", (0, 0))
        return dx, dy

    def mouth(self):
        return self.pose.get("mouth", 0)

    def glow(self):
        return self.pose.get("glow", 0)

    def sway(self):
        return self.pose.get("sway", 0.0)

    # ---- masks
    def mask(self):
        return Mask(self.n)

    def ell(self, m, cx, cy, rx, ry=None, rot=0.0, steps=40):
        ry = rx if ry is None else ry
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts = []
        for i in range(steps):
            a = 2 * math.pi * i / steps
            ex, ey = rx * math.cos(a), ry * math.sin(a)
            pts.append((cx + ex * c - ey * s, cy + ex * s + ey * c))
        m.poly(self.P(pts))
        return m

    def poly(self, m, pts):
        m.poly(self.P(pts))
        return m

    def tube(self, m, pts, w0, w1, steps=60):
        """Tapered stroke along the spline through pts (design coordinates, widths in design pixels)."""
        cp = self.P(pts)
        for i in range(steps + 1):
            t = i / steps
            x, y = spline(cp, t)
            r = self.R((w0 + (w1 - w0) * t) / 2)
            m.ell(x, y, r, r)
        return m

    def spike(self, m, bx, by, tx, ty, w):
        """Triangle with base centre (bx, by) and tip (tx, ty)."""
        dx, dy = tx - bx, ty - by
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * w / 2, dx / L * w / 2
        m.poly(self.P([(bx + nx, by + ny), (tx, ty), (bx - nx, by - ny)]))
        return m

    # ---- painting
    def grad(self, bits, base=-0.05, gain=0.9, lx=0.5, ly=0.65):
        ys = [y for y in range(self.n) if any(bits[y])]
        xs = [x for x in range(self.n) if any(bits[y][x] for y in range(self.n))]
        if not ys:
            return lambda x, y: 0.0
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        w, h = max(1, x1 - x0), max(1, y1 - y0)

        def f(x, y):
            u, v = (x - x0) / w, (y - y0) / h
            return clamp(base + gain * (lx * u + ly * v) / (lx + ly))
        return f

    def paint(self, m, fill=1, dark=3, shade="auto", outline=True, rim=False, base=-0.05, gain=0.9):
        """Paint a Mask. shade: 'auto' (gradient from upper left), None (flat), or a function (x, y) -> 0..1."""
        bits = m.bits()
        if shade == "auto":
            shade = self.grad(bits, base, gain)
        self.cv.paint(bits, shade=shade, outline=outline, fill=fill, dark=dark)
        if rim:
            inner = erode(bits)
            n = self.n
            px = self.cv.px
            for y in range(1, n - 1):
                for x in range(1, n - 1):
                    if inner[y][x] and px[y][x] == fill and (not inner[y - 1][x] or not inner[y][x - 1]) and (x + y) % 2 == 0:
                        px[y][x] = 0
        return bits

    def over(self, bits, c, pred):
        """Recolor the pixels of `bits` (a painted mask) for which pred(x, y) holds and that are not outline."""
        inner = erode(bits)
        for y in range(self.n):
            for x in range(self.n):
                if inner[y][x] and pred(x, y):
                    self.cv.px[y][x] = c

    # ---- direct pixel marks in design space
    def dot(self, x, y, c):
        self.cv.dot(int(round(self.X(x))), int(round(self.Y(y))), c)

    def line(self, x0, y0, x1, y1, c):
        self.cv.line(int(round(self.X(x0))), int(round(self.Y(y0))), int(round(self.X(x1))), int(round(self.Y(y1))), c)

    def rect(self, x0, y0, x1, y1, c):
        self.cv.rect(int(round(self.X(x0))), int(round(self.Y(y0))), int(round(self.X(x1))), int(round(self.Y(y1))), c)

    def px(self, x, y):
        """Pixel of the canvas under design point (x, y), or None."""
        xi, yi = int(round(self.X(x))), int(round(self.Y(y)))
        if 0 <= xi < self.n and 0 <= yi < self.n:
            return self.cv.px[yi][xi]
        return None

    # ---- common parts
    def eye(self, x, y, kind="angry", size=3.0, side=-1, color=0, pupil=3):
        """An eye centred at (x, y).  side = -1 for an eye on the left half of a face looking right/forward (brow slants down toward the
        centre), +1 for the right half.  kinds: angry, glow, slit, hollow, round, dot."""
        s = max(1, int(round(size * self.s * self.k)))
        cx, cy = int(round(self.X(x))), int(round(self.Y(y)))
        g = self.glow()
        if kind == "dot":
            self.cv.dot(cx, cy, 3)
            return
        if kind == "hollow":
            self.cv.rect(cx - s // 2, cy - s // 2, cx + (s + 1) // 2 - 1, cy + (s + 1) // 2 - 1, 3)
            self.cv.dot(cx, cy, 2 if g else 0)
            return
        if kind == "round":
            self.cv.rect(cx - s // 2, cy - s // 2, cx + (s + 1) // 2 - 1, cy + (s + 1) // 2 - 1, 0)
            self.cv.dot(cx, cy, 3)
            if s >= 3:
                self.cv.dot(cx + 1 * (-side), cy, 3)
            return
        if kind == "slit":
            self.cv.rect(cx - s // 2, cy - s // 2, cx + s // 2, cy, 2 if g else 0)
            self.cv.rect(cx, cy - s // 2, cx, cy + 1, 3)
            return
        # angry / glow: a band of colour with a heavy brow cutting down toward the nose
        fillc = 2 if kind == "glow" else color
        self.cv.rect(cx - s // 2, cy, cx + s // 2, cy + max(1, s // 2), 0 if kind == "angry" else fillc)
        for i in range(-s // 2 - 1, s // 2 + 2):
            drop = max(0, (i * -side) if side else 0)
            self.cv.dot(cx + i, cy - 1 + (1 if i * -side > 0 else 0) - (1 if i * -side < -1 else 0), 3)
        self.cv.dot(cx + (1 if side > 0 else -1) * 0, cy + 1, pupil)
        if g:
            self.cv.dot(cx - 1, cy, 0)

    def fangs(self, x, y, w, count=3, length=2.5, up=False):
        """A row of white fangs hanging from the line y (or standing up from it when up=True), spread over width w."""
        for i in range(count):
            fx = x + (i - (count - 1) / 2) * (w / max(count - 1, 1))
            L = max(1, int(round(length * self.s * self.k)))
            for j in range(L):
                self.cv.dot(int(round(self.X(fx))), int(round(self.Y(y))) + (-j if up else j), 0)

    def claws(self, x, y, d=-1, count=3, gap=2.2, length=2.5):
        """White claws pointing down from (x, y)."""
        L = max(1, int(round(length * self.s * self.k)))
        for i in range(count):
            cx = x + (i - (count - 1) / 2) * gap
            xi = int(round(self.X(cx)))
            yi = int(round(self.Y(y)))
            for j in range(L):
                self.cv.dot(xi, yi + j, 0)
            self.cv.dot(xi, yi + L, 3)

    def result(self):
        return self.cv


def render_frames(draw, poses):
    """draw(scene) per pose -> list of Canvases."""
    return [draw(p) for p in poses]
