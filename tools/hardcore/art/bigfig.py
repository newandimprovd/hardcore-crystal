"""Battle portraits drawn in code: a 56x56, four colour, full-figure trainer picture for every character recipe of art/cast.py.

The recipes are the same ones that make the 16x16 overworld sprites (art/npcs.py), so the overworld figure and the battle portrait are the
same person.  Colours are palette indices like in the overworld sheets: 0 white (background, highlights, eyes), 1 skin, 2 cloth, 3 black.
The real colours of a class are its colorway (art/areapal.py).

How it is drawn: every part is a smooth shape (supersampled 8x, then reduced), painted back to front with a one pixel black outline.  Inside a
part, a height field from the distance to the edge gives light from the upper left: a thin dithered white rim lights the upper left edges and
a dithered black band shades the lower right ones, the middle stays flat.  Small details (eyes, brows, buttons) are single pixels.

The figure stands on y=53, centred on x=25 so the held Poke Ball has room on the right.  Tall hats scale the figure down a little (anchored at
the ground) so the whole picture always fits.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

N = 56
K = 8
CX = 25.0
GROUND = 53.0
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0 + 1 / 32.0
CROSS = ndi.generate_binary_structure(2, 1)
LIGHT = np.array([-0.543, -0.641, 0.543])
COL = {"S": 1, "C": 2, "D": 3, "W": 0}


class Sh:
    """A shape: boolean N x N array with set operations."""

    def __init__(self, a=None):
        self.a = np.zeros((N, N), bool) if a is None else a

    def __or__(self, o):
        return Sh(self.a | o.a)

    def __and__(self, o):
        return Sh(self.a & o.a)

    def __sub__(self, o):
        return Sh(self.a & ~o.a)

    def any(self):
        return bool(self.a.any())


def _finish(im):
    small = im.resize((N, N), Image.BOX)
    return Sh(np.asarray(small) >= 128)


def blank():
    im = Image.new("L", (N * K, N * K), 0)
    return im, ImageDraw.Draw(im)


class Painter:
    def __init__(self, scale=1.0):
        self.s = scale
        self.px = np.zeros((N, N), int)
        self.under = np.zeros((N, N), bool)  # pixels already painted by something (for clipping tricks)

    # ---------------------------------------------------------------- mapping from design space
    def X(self, x):
        return CX + (x - CX) * self.s

    def Y(self, y):
        return GROUND - (GROUND - y) * self.s

    # ---------------------------------------------------------------- shapes
    def ell(self, cx, cy, rx, ry=None, rot=0.0):
        ry = rx if ry is None else ry
        im, d = blank()
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts = []
        for i in range(48):
            a = 2 * math.pi * i / 48
            ex, ey = rx * math.cos(a), ry * math.sin(a)
            pts.append((self.X(cx + ex * c - ey * s) * K, self.Y(cy + ex * s + ey * c) * K))
        d.polygon(pts, fill=255)
        return _finish(im)

    def poly(self, pts):
        im, d = blank()
        d.polygon([(self.X(x) * K, self.Y(y) * K) for x, y in pts], fill=255)
        return _finish(im)

    def rect(self, x0, y0, x1, y1):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

    def tube(self, pts, w0, w1=None, steps=40):
        """Tapered stroke through pts (Catmull-Rom), widths in design pixels."""
        w1 = w0 if w1 is None else w1
        im, d = blank()
        sp = [(self.X(x), self.Y(y)) for x, y in pts]
        for i in range(steps + 1):
            t = i / steps
            x, y = spline(sp, t)
            r = (w0 + (w1 - w0) * t) / 2 * self.s
            d.ellipse([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K], fill=255)
        return _finish(im)

    def spike(self, bx, by, tx, ty, w):
        dx, dy = tx - bx, ty - by
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L * w / 2, dx / L * w / 2
        return self.poly([(bx + nx, by + ny), (tx, ty), (bx - nx, by - ny)])

    # ---------------------------------------------------------------- painting
    def paint(self, sh, fill, outline=True, hi=1.0, sd=1.0, R=3.0, flat=False, dark=3, lit=0):
        """Fill a shape with palette index `fill`, black outline, light from the upper left.
        hi: strength of the white rim light, sd: strength of the shadow band (dark colour index `dark`), flat: no shading."""
        b = sh.a
        if not b.any():
            return sh
        inner = ndi.binary_erosion(b, structure=CROSS, border_value=0)
        rim = b & ~inner
        if not flat:
            d = ndi.distance_transform_edt(np.pad(b, 1))[1:-1, 1:-1]
            r = min(R, max(1.3, d.max() * 0.85))
            h = np.minimum(d, r) / r
            hs = ndi.gaussian_filter(h, 0.7)
            gy, gx = np.gradient(hs)
            k = 2.4
            nx, ny, nz = -gx * k, -gy * k, np.ones_like(hs)
            nl = np.sqrt(nx * nx + ny * ny + nz * nz)
            L = (nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2]) / nl
            hd = np.clip((L - 0.72) / 0.3, 0, 1) * hi
            sdn = np.clip((0.36 - L) / 0.3, 0, 1) * sd
        for y in range(N):
            for x in range(N):
                if not b[y, x]:
                    continue
                if outline and rim[y, x]:
                    self.px[y, x] = 3
                    self.under[y, x] = True
                    continue
                c = fill
                if not flat:
                    t = BAYER[y % 4, x % 4]
                    if hd[y, x] > t and fill != 0:
                        c = lit if fill != 3 or lit else 2
                    elif sdn[y, x] > t and fill != dark:
                        c = dark
                self.px[y, x] = c
                self.under[y, x] = True
        return sh

    def dot(self, x, y, c):
        xi, yi = int(round(self.X(x))), int(round(self.Y(y)))
        if 0 <= xi < N and 0 <= yi < N:
            self.px[yi, xi] = c

    def line(self, x0, y0, x1, y1, c):
        a, b = (self.X(x0), self.Y(y0)), (self.X(x1), self.Y(y1))
        n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]), 1))
        for i in range(n + 1):
            xi = int(round(a[0] + (b[0] - a[0]) * i / n))
            yi = int(round(a[1] + (b[1] - a[1]) * i / n))
            if 0 <= xi < N and 0 <= yi < N:
                self.px[yi, xi] = c

    def box(self, x0, y0, x1, y1, c):
        for y in range(int(round(self.Y(y0))), int(round(self.Y(y1))) + 1):
            for x in range(int(round(self.X(x0))), int(round(self.X(x1))) + 1):
                if 0 <= x < N and 0 <= y < N:
                    self.px[y, x] = c

    def at(self, x, y):
        xi, yi = int(round(self.X(x))), int(round(self.Y(y)))
        return int(self.px[yi, xi]) if 0 <= xi < N and 0 <= yi < N else 0


def spline(pts, s):
    n = len(pts) - 1
    if n == 0:
        return pts[0]
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


# =============================================================================================
# the figure
# =============================================================================================
TALL_HAIR = {"mohawk": 0.9, "bun": 0.94, "afro": 0.9}
TALL_HATS = {"mitre": 0.84, "tophat": 0.86, "antlers": 0.86, "witch": 0.82, "crownk": 0.92, "jester": 0.86, "horns": 0.92, "helmet+horns": 0.9,
             "antenna": 0.92}


def col(name, default="D"):
    return COL[name or default]


def draw(rec, hold="ball"):
    """Return the 56x56 array of palette indices for a recipe (art/npcs.py recipe dict)."""
    hat = rec.get("hat")
    scale = min(TALL_HATS.get(hat, 1.0), TALL_HAIR.get(rec.get("hair"), 1.0))
    p = Painter(scale)
    fig = Figure(p, rec)
    fig.render(hold)
    return p.px


class Figure:
    def __init__(self, p, rec):
        self.p = p
        self.r = rec
        self.w = 1.16 if rec.get("width") else 1.0  # broad characters
        self.skin = 1
        self.torso_c = col(rec.get("torsoc"), "C")
        self.arm_c = col(rec.get("armc") or rec.get("torsoc"), "C")
        self.leg_c = col(rec.get("legsc"), "D")
        self.hair_c = col(rec.get("hairc"), "D")
        self.hat_c = col(rec.get("hatc"), "C")
        self.shoe_c = col(rec.get("shoes"), "D")
        self.head_c = (CX, 14.5)

    # ------------------------------------------------------------------------------------ order
    def render(self, hold):
        r = self.r
        extras = tuple(r.get("extra") or ())
        self.extras = extras
        self.behind(extras)
        self.legs()
        self.torso()
        self.arms(hold)
        self.head()
        self.hair()
        self.hat()
        self.front_extras(extras)

    # ------------------------------------------------------------------------------------ behind
    def behind(self, extras):
        p = self.p
        if "wings" in extras:
            for sx in (-1, 1):
                pts = [(CX + sx * 8, 26), (CX + sx * 22, 12), (CX + sx * 25, 26), (CX + sx * 20, 34), (CX + sx * 9, 36)]
                p.paint(p.poly(pts), 2, hi=0.5)
        if "tail" in extras:
            p.paint(p.tube([(CX + 6, 42), (CX + 17, 46), (CX + 20, 38), (CX + 17, 33)], 4, 1.8), 3, hi=0.4)
        if "bag" in extras and self.r.get("bagc") != "front":
            bc = col(self.r.get("bagc"), "D")
            p.paint(p.ell(CX + 12, 33, 6, 8), bc, hi=0.7)
        if "staff" in extras and False:
            pass

    # ------------------------------------------------------------------------------------ legs
    def legs(self):
        p, r = self.p, self.r
        k = r.get("legs", "pants")
        w = self.w
        if k in ("robe",):
            return
        if k == "treads":
            for sx in (-1, 1):
                p.paint(p.rect(CX + sx * 6.5 - 4.5, 44, CX + sx * 6.5 + 4.5, 52), 3, hi=0.8)
                for i in range(3):
                    p.dot(CX + sx * 6.5 - 3 + i * 3, 48, 2)
            return
        if k == "hover":
            p.paint(p.ell(CX, 51.5, 13, 2.6), 3, hi=0.9)
            p.paint(p.ell(CX, 49, 8, 1.6), 2, hi=0.5, flat=True)
            return
        top = 38.5
        for sx in (-1, 1):
            x = CX + sx * 4.4 * w
            if k == "shorts":
                p.paint(p.tube([(x, top), (x + sx * 0.3, 45.5)], 7.0 * w, 7.4 * w), self.leg_c if self.leg_c != 3 else 2, hi=0.8)
                p.paint(p.tube([(x + sx * 0.2, 45), (x + sx * 0.3, 50.5)], 4.6, 4.2), self.skin, sd=0.0, hi=0.6, R=2.0)
            else:
                p.paint(p.tube([(x, top), (x + sx * 0.4, 50)], 7.0 * w, 6.2 * w), self.leg_c, hi=0.8)
        for sx in (-1, 1):
            x = CX + sx * 5.0 * w
            p.paint(p.ell(x + sx * 0.8, 51.6, 4.6, 2.3), self.shoe_c if self.shoe_c != self.leg_c or True else 3, hi=0.9, flat=False)

    # ------------------------------------------------------------------------------------ torso
    def torso(self):
        p, r = self.p, self.r
        k = r.get("torso", "shirt")
        w = self.w
        tc = self.torso_c
        sw = 11.0 * w
        bw = 8.6 * w
        y0, y1 = 25.0, 40.0
        if k in ("robe", "habit"):
            hem = 52.5
            pts = [(CX - sw, 26), (CX + sw, 26), (CX + sw + 3.5, hem), (CX - sw - 3.5, hem)]
            body = p.poly(pts) | p.ell(CX, 27, sw, 3.4)
            p.paint(body, tc, hi=0.8)
            # fold lines
            for dx in (-5, 0, 5):
                p.line(CX + dx * 0.8, 38, CX + dx * 1.2, 51, 3 if tc != 3 else 2)
            if "hem" in self.extras or True:
                pass
            return
        if k == "dress":
            skirt = p.poly([(CX - bw, 38), (CX + bw, 38), (CX + bw + 5.5, 46.5), (CX - bw - 5.5, 46.5)]) | p.ell(CX, 46, bw + 5.5, 1.8)
            p.paint(skirt, tc, hi=0.8)
            p.line(CX - bw - 3, 44, CX + bw + 3, 44, 3 if tc != 3 else 2)
        if k in ("bare", "swim"):
            fillc = self.skin
        elif k == "armor":
            fillc = tc
        else:
            fillc = tc
        body = p.poly([(CX - sw, 26), (CX + sw, 26), (CX + bw, y1), (CX - bw, y1)]) | p.ell(CX, 27, sw, 3.4)
        p.paint(body, fillc, hi=0.8, sd=0.0 if k in ("bare", "swim") else 1.0)
        if k == "coat":
            # open front: white shirt strip and a dark seam
            p.paint(p.poly([(CX - 3, 25), (CX + 3, 25), (CX + 2, 40), (CX - 2, 40)]), 0, hi=0.0, sd=0.6)
            p.line(CX - 3, 26, CX - 2, 40, 3)
            p.line(CX + 3, 26, CX + 2, 40, 3)
            for yy in (31, 35):
                p.dot(CX - 5.5, yy, 3)
                p.dot(CX + 5.5, yy, 3)
        elif k == "shirt":
            pass
        elif k == "bare":
            p.line(CX, 27, CX, 38, 3)  # sternum line
            for yy in (30, 34):
                p.dot(CX - 5, yy, 3)
                p.dot(CX + 5, yy, 3)
        elif k == "swim":
            p.paint(p.ell(CX - 4.2, 29.5, 4.2, 3.0), tc, hi=0.6, R=2.0)
            p.paint(p.ell(CX + 4.2, 29.5, 4.2, 3.0), tc, hi=0.6, R=2.0)
        elif k == "armor":
            for sx in (-1, 1):
                p.paint(p.ell(CX + sx * 11.5, 27.5, 5.0, 3.6), 3, hi=0.9)
            p.line(CX, 27, CX, 39, 3)
            for yy in (29, 33, 37):
                p.dot(CX - 6, yy, 3)
                p.dot(CX + 6, yy, 3)
        elif k == "dress":
            p.line(CX - bw, 36.5, CX + bw, 36.5, 3 if tc != 3 else 2)

    # ------------------------------------------------------------------------------------ arms
    def arms(self, hold):
        p, r = self.p, self.r
        k = r.get("torso", "shirt")
        w = self.w
        skin_arm = k in ("bare", "swim")
        ac = self.skin if skin_arm else self.arm_c
        sw = 11.0 * w
        # viewer's left arm hangs down
        left = p.tube([(CX - sw + 0.5, 28), (CX - sw - 2.4, 34), (CX - sw - 2.4, 39)], 5.2, 4.6)
        p.paint(left, ac, hi=0.7, sd=0.0 if skin_arm else 1.0)
        p.paint(p.ell(CX - sw - 2.4, 41.0, 2.9, 2.8), self.skin, hi=0.7, sd=0.0, R=2.0)
        # viewer's right arm bent up, hand under the ball
        if hold == "ball":
            self.ball()
        right = p.tube([(CX + sw - 0.5, 28), (CX + sw + 3.2, 32), (CX + sw + 6.5, 30)], 5.2, 4.6)
        p.paint(right, ac, hi=0.7, sd=0.0 if skin_arm else 1.0)
        p.paint(p.ell(CX + sw + 7.6, 29.6, 3.0, 2.8), self.skin, hi=0.7, sd=0.0, R=2.0)
        if not skin_arm and k not in ("robe", "habit") and ac != 3:
            # cuffs
            p.line(CX - sw - 4.7, 38.3, CX - sw - 0.1, 38.3, 3)

    def ball(self):
        """A Poke Ball: cloth-coloured top, white bottom, black band, white button.  Drawn before the hand so the fingers wrap it."""
        p = self.p
        sw = 11.0 * self.w
        bx, by, rr = CX + sw + 8.0, 25.0, 4.6
        shape = p.ell(bx, by, rr)
        p.paint(shape, 0, outline=True, flat=True)
        top = shape & p.rect(bx - 7, by - 7, bx + 7, by - 0.2)
        tc = 2
        for y in range(N):
            for x in range(N):
                if top.a[y, x] and p.px[y, x] == 0:
                    p.px[y, x] = tc
        p.line(bx - rr, by + 0.2, bx + rr, by + 0.2, 3)
        p.line(bx - rr, by + 1.0, bx + rr, by + 1.0, 3)
        p.paint(p.ell(bx, by + 0.6, 1.7), 0, flat=True)
        p.dot(bx - 2.4, by - 2.6, 0)
        p.dot(bx - 1.6, by - 3.4, 0)

    # ------------------------------------------------------------------------------------ head
    def head(self):
        p, r = self.p, self.r
        cx, cy = self.head_c
        w = 1.0 + (self.w - 1.0) * 0.5
        p.paint(p.ell(cx, 25.5, 3.4, 2.4), self.skin, flat=True)  # neck
        shape = p.ell(cx, cy, 10.0 * w, 9.6)
        ear = p.ell(cx - 10.0 * w, cy + 1.2, 2.2, 2.8) | p.ell(cx + 10.0 * w, cy + 1.2, 2.2, 2.8)
        p.paint(ear, self.skin, hi=0.0, sd=0.0, flat=True)
        p.paint(shape, self.skin, hi=0.6, sd=0.0, R=3.5)
        self.face()

    def face(self):
        p, r = self.p, self.r
        cx, cy = self.head_c
        f = r.get("face", "eyes")
        ec = r.get("eyec")
        ex = 4.2
        ey = cy + 1.8
        if f == "none":
            return
        if f == "glow":
            for sx in (-1, 1):
                p.box(cx + sx * ex - 1, ey - 1, cx + sx * ex + 1, ey + 1, 0)
                p.dot(cx + sx * ex, ey, 2)
            return
        if f == "hollow":
            for sx in (-1, 1):
                p.box(cx + sx * ex - 1.5, ey - 2, cx + sx * ex + 1.5, ey + 2, 3)
            p.line(cx - 1, ey + 4, cx - 1, ey + 5, 3)
            p.line(cx + 1, ey + 4, cx + 1, ey + 5, 3)
            p.box(cx - 4, ey + 6, cx + 4, ey + 6, 3)
            return
        for sx in (-1, 1):
            x = cx + sx * ex
            if f == "tired":
                p.box(x - 1.5, ey, x + 1.5, ey, 3)
                p.box(x - 1.5, ey - 1, x + 1.5, ey - 1, 3)
                p.dot(x, ey + 2, 3)
            elif f == "blank":
                p.dot(x, ey, 3)
                p.dot(x, ey + 1, 3)
            else:
                p.box(x - 1.5, ey - 1, x + 1.5, ey + 1, 0)  # sclera
                px_ = x + (0.5 if sx < 0 else -0.5)
                p.box(px_ - 0.5, ey - 1, px_ + 0.5, ey + 1, 3)  # pupil
                p.box(x - 1.5, ey - 2, x + 1.5, ey - 2, 3)  # lid line
        # brows
        if f == "angry":
            for sx in (-1, 1):
                x = cx + sx * ex
                p.line(x - sx * 2.5, ey - 4.2, x + sx * 1.0, ey - 2.3, 3)
                p.line(x - sx * 2.5, ey - 3.2, x + sx * 1.0, ey - 1.3, 3)
        elif f != "blank":
            for sx in (-1, 1):
                x = cx + sx * ex
                p.line(x - 2, ey - 3.3, x + 1.5, ey - 3.3, 3)
        # mouth
        my = cy + 6.2
        if f == "grin":
            p.box(cx - 3, my - 1, cx + 3, my + 1, 0)
            p.line(cx - 4, my - 1, cx + 4, my - 1, 3)
            p.line(cx - 3, my + 2, cx + 3, my + 2, 3)
            p.dot(cx - 4, my - 2, 3)
            p.dot(cx + 4, my - 2, 3)
        elif f == "angry":
            p.line(cx - 2.5, my + 1, cx + 2.5, my + 1, 3)
            p.dot(cx - 3, my + 2, 3)
            p.dot(cx + 3, my + 2, 3)
        elif f == "tired":
            p.line(cx - 2, my + 1, cx + 2, my + 1, 3)
        elif f == "blank":
            p.line(cx - 1.5, my + 1, cx + 1.5, my + 1, 3)
        else:
            p.line(cx - 2, my, cx + 2, my, 3)
            p.dot(cx - 3, my - 1, 3)
            p.dot(cx + 3, my - 1, 3)
        p.dot(cx, cy + 4, 3)  # nose

    # ------------------------------------------------------------------------------------ hair
    def hair(self):
        p, r = self.p, self.r
        k = r.get("hair", "short")
        if k in ("bald", None):
            return
        cx, cy = self.head_c
        hc = self.hair_c
        w = 1.0 + (self.w - 1.0) * 0.5
        cap = p.ell(cx, cy - 1.8, 10.8 * w, 9.6)
        face_cut = p.ell(cx, cy + 6.0, 8.2 * w, 8.4)
        if k == "short":
            shape = (cap - face_cut) | p.rect(cx - 10.4 * w, cy - 3, cx - 8.2 * w, cy + 3) | p.rect(cx + 8.2 * w, cy - 3, cx + 10.4 * w, cy + 3)
            p.paint(shape, hc, hi=0.9)
        elif k == "long":
            back = p.poly([(cx - 11.5, cy - 3), (cx + 11.5, cy - 3), (cx + 12, 34), (cx + 8, 38), (cx - 8, 38), (cx - 12, 34)])
            p.paint(back - p.ell(cx, cy + 4, 8.5, 11), hc, hi=0.9)
            p.paint((cap - face_cut), hc, hi=0.9)
        elif k == "mohawk":
            zig = [(cx - 4.5, cy - 7), (cx - 4, cy - 13), (cx - 2.6, cy - 11), (cx - 1.6, cy - 17), (cx - 0.2, cy - 12.5), (cx + 1, cy - 18.5),
                   (cx + 2.2, cy - 12.5), (cx + 3.4, cy - 16), (cx + 4, cy - 11), (cx + 4.8, cy - 7)]
            p.paint(p.poly(zig) | p.ell(cx, cy - 7.5, 4.6, 2.6), hc, hi=0.8)
        elif k == "bun":
            p.paint(p.ell(cx, cy - 13.5, 4.2, 3.6), hc, hi=0.9)
            p.paint(cap - face_cut, hc, hi=0.9)
        elif k == "bushy":
            for (dx, dy, rr) in ((-8, -2, 4.6), (-5, -8, 5.2), (0, -10, 5.8), (5, -8, 5.2), (8, -2, 4.6)):
                p.paint(p.ell(cx + dx, cy + dy, rr), hc, hi=0.9)
            p.paint(cap - face_cut, hc, hi=0.9)
        elif k == "afro":
            p.paint(p.ell(cx, cy - 4.5, 14.5, 13) - face_cut, hc, hi=0.9)
        elif k == "pigtails":
            p.paint(p.ell(cx - 12.5, cy + 6, 3.4, 5.4), hc, hi=0.9)
            p.paint(p.ell(cx + 12.5, cy + 6, 3.4, 5.4), hc, hi=0.9)
            p.paint(cap - face_cut, hc, hi=0.9)
        else:
            p.paint(cap - face_cut, hc, hi=0.9)

    # ------------------------------------------------------------------------------------ hats
    def hat(self):
        p, r = self.p, self.r
        h = r.get("hat")
        if not h:
            return
        for k in str(h).split("+"):
            self.one_hat(k)

    def one_hat(self, k):
        p, r = self.p, self.r
        cx, cy = self.head_c
        hc = self.hat_c
        w = 1.0 + (self.w - 1.0) * 0.5
        if k == "cap":
            dome = p.ell(cx, cy - 4.5, 10.8 * w, 7.0) - p.rect(cx - 14, cy - 1.2, cx + 14, cy + 12)
            p.paint(dome, hc, hi=0.9)
            brim = p.ell(cx, cy - 0.8, 11.8 * w, 2.4) - p.rect(cx - 14, cy - 8, cx + 14, cy - 2)
            p.paint(brim, 3 if hc != 3 else 2, hi=0.8, sd=0.0)
            p.box(cx - 1, cy - 8, cx + 1, cy - 6, 0)  # badge
            p.dot(cx, cy - 7, 3)
        elif k == "bowler":
            p.paint(p.ell(cx, cy - 6.5, 7.8 * w, 6.4) - p.rect(cx - 14, cy - 2.3, cx + 14, cy + 9), hc, hi=0.9)
            p.paint(p.ell(cx, cy - 2.4, 12.6 * w, 2.0), 3 if hc != 3 else 2, hi=0.6)
            p.line(cx - 8, cy - 4.2, cx + 8, cy - 4.2, 3)
        elif k == "tophat":
            p.paint(p.rect(cx - 7 * w, cy - 19, cx + 7 * w, cy - 3), hc, hi=0.9)
            p.paint(p.ell(cx, cy - 3.0, 12.4 * w, 2.2), hc, hi=0.7)
            p.line(cx - 7, cy - 6.5, cx + 7, cy - 6.5, 3)
            p.line(cx - 7, cy - 7.5, cx + 7, cy - 7.5, 3)
        elif k == "mitre":
            p.paint(p.poly([(cx - 8 * w, cy - 4), (cx - 3, cy - 20), (cx + 3, cy - 20), (cx + 8 * w, cy - 4)]), 0, hi=0.0, sd=0.7)
            p.paint(p.poly([(cx - 3, cy - 20), (cx, cy - 15), (cx + 3, cy - 20)]), hc, flat=True)
            p.line(cx, cy - 19, cx, cy - 6, hc)
            p.box(cx - 8, cy - 5, cx + 8, cy - 4, hc)
        elif k == "hood":
            hood = p.ell(cx, cy - 1.0, 12.4 * w, 11.6)
            inner = p.ell(cx, cy + 2.2, 8.2 * w, 8.6)
            p.paint(hood - inner, hc, hi=0.9)
            # shadow inside the hood
            p.paint(p.ell(cx, cy - 4.0, 8.0 * w, 4.6) & p.ell(cx, cy + 2.2, 8.2 * w, 8.6), 3, flat=True, outline=False)
        elif k == "wimple":
            vc = hc if hc != 2 else 3
            veil = p.ell(cx, cy - 0.5, 12.4, 11.6) | p.poly([(cx - 12.4, cy), (cx + 12.4, cy), (cx + 15, 34), (cx - 15, 34)])
            frame = p.ell(cx, cy + 3.4, 8.6, 9.2)
            p.paint(veil - frame, vc, hi=0.8)
            p.paint(p.ell(cx, cy + 3.4, 8.6, 9.2) - p.ell(cx, cy + 3.8, 7.2, 8.0), 0, flat=True)
            p.paint(p.poly([(cx - 6, 25), (cx + 6, 25), (cx + 7, 36), (cx - 7, 36)]), 0, hi=0.0, sd=0.4)
        elif k == "visor":
            p.paint(p.ell(cx, cy - 4.5, 10.2 * w, 5.8) - p.rect(cx - 14, cy - 2.0, cx + 14, cy + 10), 0, hi=0.0, sd=0.5)
            p.paint(p.ell(cx, cy - 1.8, 12.4 * w, 2.2) - p.rect(cx - 14, cy - 8, cx + 14, cy - 2.4), hc, hi=0.8)
        elif k == "sunhat":
            p.paint(p.ell(cx, cy - 6, 8.2 * w, 5.2) - p.rect(cx - 14, cy - 3, cx + 14, cy + 9), 0, hi=0.0, sd=0.5)
            p.paint(p.ell(cx, cy - 3.0, 15.5, 3.4), 0, hi=0.0, sd=0.6)
            p.line(cx - 8, cy - 4.4, cx + 8, cy - 4.4, hc)
            p.line(cx - 8, cy - 3.4, cx + 8, cy - 3.4, hc)
        elif k == "crown":  # flower crown
            for i, dx in enumerate((-8, -4.5, -1.5, 1.5, 4.5, 8)):
                y = cy - 8.2 + abs(dx) * 0.28
                p.paint(p.ell(cx + dx, y, 2.4), 2 if i % 2 == 0 else 0, hi=0.0, sd=0.0, flat=True)
        elif k == "horns":
            for sx in (-1, 1):
                p.paint(p.tube([(cx + sx * 7, cy - 7), (cx + sx * 12, cy - 12), (cx + sx * 11, cy - 18)], 4.6, 1.2), 0, hi=0.0, sd=0.7)
        elif k == "antlers":
            for sx in (-1, 1):
                p.paint(p.tube([(cx + sx * 6, cy - 8), (cx + sx * 9, cy - 14), (cx + sx * 8, cy - 20)], 3.2, 1.6), 0, hi=0.0, sd=0.6)
                p.paint(p.tube([(cx + sx * 8.5, cy - 13), (cx + sx * 13, cy - 16)], 2.4, 1.2), 0, hi=0.0, sd=0.6)
        elif k == "helmet":
            p.paint(p.ell(cx, cy - 3.8, 11.4 * w, 8.6) - p.rect(cx - 14, cy + 0.5, cx + 14, cy + 12), hc if hc != 2 else 3, hi=0.9)
            p.paint(p.rect(cx - 11.5 * w, cy - 0.8, cx + 11.5 * w, cy + 1.2), 3, flat=True)
            p.line(cx, cy - 12, cx, cy - 1, 3)
        elif k == "bandana":
            p.paint(p.ell(cx, cy - 4.2, 10.6 * w, 7.0) - p.rect(cx - 14, cy - 1.6, cx + 14, cy + 9), hc, hi=0.9)
            p.paint(p.tube([(cx + 9, cy - 3), (cx + 14, cy - 2), (cx + 15, cy + 2)], 3.2, 2.0), hc, hi=0.6)
        elif k == "swimcap":
            p.paint(p.ell(cx, cy - 3.0, 10.6 * w, 8.6) - p.rect(cx - 14, cy + 0.6, cx + 14, cy + 12), hc, hi=0.9)
        elif k == "jester":
            for sx in (-1, 1):
                p.paint(p.tube([(cx + sx * 5, cy - 8), (cx + sx * 11, cy - 14), (cx + sx * 16, cy - 10), (cx + sx * 17, cy - 5)], 5.6, 2.2),
                        hc, hi=0.8)
                p.paint(p.ell(cx + sx * 17, cy - 4.2, 2.0), 0, flat=True)
            p.paint(p.ell(cx, cy - 4.2, 10.4, 6.4) - p.rect(cx - 14, cy - 1.6, cx + 14, cy + 9), 3, hi=0.9)
        elif k == "halo":
            p.paint(p.ell(cx, cy - 12.5, 8, 2.2), 0, hi=0.0, sd=0.0, flat=True)
        elif k == "zuc":
            p.paint(p.ell(cx, cy - 6.0, 6.6, 4.8) - p.rect(cx - 14, cy - 3.0, cx + 14, cy + 9), hc, hi=0.9)
        elif k == "beret":
            p.paint(p.ell(cx + 2, cy - 7.0, 10.0, 4.4), hc, hi=0.9)
            p.dot(cx + 3, cy - 12, 3)
        elif k == "antenna":
            p.line(cx, cy - 9, cx, cy - 16, 3)
            p.paint(p.ell(cx, cy - 17, 2.2), 2, flat=True)
        elif k == "witch":
            p.paint(p.ell(cx, cy - 3.0, 15.0, 3.0), 3, hi=0.8)
            p.paint(p.poly([(cx - 8, cy - 3), (cx - 1, cy - 22), (cx + 5, cy - 24), (cx + 8, cy - 3)]), 3, hi=0.9)
            p.line(cx - 7.5, cy - 6, cx + 7.5, cy - 6, hc)
            p.line(cx - 7.2, cy - 7, cx + 7.2, cy - 7, hc)
        elif k == "crownk":
            p.paint(p.poly([(cx - 8, cy - 7), (cx - 8, cy - 14), (cx - 4, cy - 10), (cx, cy - 15), (cx + 4, cy - 10), (cx + 8, cy - 14), (cx + 8, cy - 7)]),
                    0, hi=0.0, sd=0.6)
        # unknown hats are ignored on purpose

    # ------------------------------------------------------------------------------------ extras
    def front_extras(self, extras):
        for e in extras:
            fn = getattr(self, "ex_" + e, None)
            if fn:
                fn()

    def ex_glasses(self):
        p = self.p
        cx, cy = self.head_c
        ey = cy + 1.8
        for sx in (-1, 1):
            x = cx + sx * 4.2
            p.box(x - 3, ey - 2, x + 2, ey - 2, 3)
            p.box(x - 3, ey + 3, x + 2, ey + 3, 3)
            p.box(x - 3, ey - 2, x - 3, ey + 3, 3)
            p.box(x + 2, ey - 2, x + 2, ey + 3, 3)
        p.box(cx - 1, ey, cx + 1, ey, 3)

    def ex_sunglasses(self):
        p = self.p
        cx, cy = self.head_c
        ey = cy + 1.8
        p.box(cx - 8, ey - 2, cx - 1, ey + 2, 3)
        p.box(cx + 1, ey - 2, cx + 8, ey + 2, 3)
        p.box(cx - 1, ey - 1, cx + 1, ey - 1, 3)
        p.dot(cx - 6.5, ey - 1, 0)
        p.dot(cx + 3.5, ey - 1, 0)

    def ex_monocle(self):
        p = self.p
        cx, cy = self.head_c
        x, y = cx + 4.2, cy + 3.6
        p.box(x - 2.5, y - 3, x + 2.5, y - 3, 3)
        p.box(x - 2.5, y + 2, x + 2.5, y + 2, 3)
        p.box(x - 3.5, y - 2, x - 3.5, y + 1, 3)
        p.box(x + 3.5, y - 2, x + 3.5, y + 1, 3)
        p.line(x + 3, y + 2, x + 5, y + 10, 3)

    def ex_goggles(self):
        p = self.p
        cx, cy = self.head_c
        y = cy - 3.0
        p.box(cx - 11, y - 1, cx + 11, y + 1, 3)
        for sx in (-1, 1):
            p.paint(p.ell(cx + sx * 4.8, y, 3.6, 3.0), 0, hi=0.0, sd=0.0, flat=True)
            p.dot(cx + sx * 4.8, y, 3)

    def ex_tie(self):
        p = self.p
        c = 2 if self.torso_c != 2 else 3
        p.paint(p.poly([(CX - 1.6, 26), (CX + 1.6, 26), (CX + 2.4, 33), (CX, 38.5), (CX - 2.4, 33)]), c, hi=0.5, sd=0.5, R=1.6)

    def ex_collar(self):
        p = self.p
        p.box(CX - 1.5, 26, CX + 1.5, 27.5, 0)

    def ex_badge(self):
        p = self.p
        p.paint(p.poly([(CX + 4.5, 29), (CX + 8.5, 29), (CX + 8.5, 33), (CX + 6.5, 35), (CX + 4.5, 33)]), 0, flat=True)
        p.dot(CX + 6.5, 31, 3)

    def ex_belt(self):
        p = self.p
        w = self.w
        p.box(CX - 9 * w, 38, CX + 9 * w, 39, 3)
        p.box(CX - 1, 38, CX + 1, 39, 0)

    def ex_cross(self):
        p = self.p
        p.box(CX - 0.5, 30, CX + 0.5, 36, 0)
        p.box(CX - 2.5, 32, CX + 2.5, 33, 0)
        p.line(CX, 28, CX, 29, 3)

    def ex_chain(self):
        p = self.p
        for i, dx in enumerate((-4, -3, -2, -1, 0, 1, 2, 3, 4)):
            p.dot(CX + dx, 27 + (4 - abs(dx)) * 0.9, 0 if i % 2 == 0 else 3)

    def ex_beard(self):
        p = self.p
        cx, cy = self.head_c
        col_ = col(self.r.get("beardc"), "D")
        p.paint(p.ell(cx, cy + 8.0, 7.6, 4.8) - p.ell(cx, cy + 2.5, 6.2, 5.0), col_, hi=0.8)

    def ex_whisker_hair(self):
        p = self.p
        cx, cy = self.head_c
        col_ = col(self.r.get("beardc"), "C")
        p.paint(p.poly([(cx - 7.5, cy + 4), (cx + 7.5, cy + 4), (cx + 5.5, cy + 22), (cx, cy + 25), (cx - 5.5, cy + 22)]) - p.ell(cx, cy + 3.5, 6.0, 5.0),
                0, hi=0.0, sd=0.6)

    def ex_staff(self):
        p = self.p
        sx = CX + 11.0 * self.w + 9.0
        p.paint(p.rect(sx - 0.8, 10, sx + 0.8, 52), 3, hi=0.0, sd=0.0, flat=True, outline=False)
        p.paint(p.ell(sx, 9.5, 2.4), 0, flat=True)

    def ex_bag(self):
        p = self.p
        bc = col(self.r.get("bagc"), "D")
        p.line(CX - 9, 27, CX + 6, 39, 3)
        p.line(CX - 8, 27, CX + 7, 39, 3)

    def ex_rod(self):
        p = self.p
        sx = CX + 11.0 * self.w + 6.0
        p.line(sx, 29, sx + 8, 3, 3)
        p.line(sx + 1, 29, sx + 9, 3, 3)
        p.line(sx + 8, 3, sx + 8, 12, 3)

    def ex_spikes(self):
        p = self.p
        for sx in (-1, 1):
            for i in range(3):
                p.paint(p.spike(CX + sx * (9 + i * 2), 26 - i * 0.2, CX + sx * (12 + i * 3), 19 - i * 2.5, 3.4), 0, hi=0.0, sd=0.5)

    def ex_sash(self):
        p = self.p
        c = 0 if self.torso_c != 0 else 3
        c = col(self.r.get("sashc"), "S") if self.r.get("sashc") else c
        p.line(CX - 9, 27, CX + 8, 39, c)
        p.line(CX - 9, 28, CX + 8, 40, c)
        p.line(CX - 8, 27, CX + 8, 38, 3)

    def ex_hem(self):
        p = self.p
        p.box(CX - 13, 49, CX + 13, 49, 3)

    def ex_buttons(self):
        p = self.p
        for yy in (30, 34, 38, 42, 46):
            p.dot(CX, yy, 0)

    def ex_number(self):
        p = self.p
        p.box(CX - 3, 31, CX + 3, 35, 0)
        p.dot(CX - 1, 32, 3)
        p.dot(CX - 1, 33, 3)
        p.dot(CX - 1, 34, 3)
        p.dot(CX + 1, 32, 3)
        p.dot(CX + 1, 33, 3)
        p.dot(CX + 1, 34, 3)

    def ex_visor(self):
        p = self.p
        cx, cy = self.head_c
        p.paint(p.rect(cx - 9, cy - 2.5, cx + 9, cy + 4), 3, hi=0.0, sd=0.0, flat=True)
        p.box(cx - 7, cy + 0.5, cx + 7, cy + 1.5, 2)

    def ex_antenna(self):
        p = self.p
        cx, cy = self.head_c
        p.line(cx + 6, cy - 9, cx + 8, cy - 15, 3)
        p.dot(cx + 8, cy - 16, 2)

    def ex_fangs(self):
        p = self.p
        cx, cy = self.head_c
        p.dot(cx - 2, cy + 8, 0)
        p.dot(cx - 2, cy + 9, 0)
        p.dot(cx + 2, cy + 8, 0)
        p.dot(cx + 2, cy + 9, 0)

    def ex_mask(self):
        p = self.p
        cx, cy = self.head_c
        p.paint(p.ell(cx, cy + 6.5, 7.4, 4.2) - p.rect(cx - 12, cy - 10, cx + 12, cy + 3.5), 0, hi=0.0, sd=0.5)

    def ex_tray(self):
        p = self.p
        sx = CX + 11.0 * self.w + 6
        p.paint(p.ell(sx + 3, 21, 8, 2), 0, hi=0.0, sd=0.6)

    def ex_pocket_stripes(self):
        p = self.p
        c = col(self.r.get("stripec"), "S") if self.r.get("stripec") else 0
        for yy in (30, 34, 38):
            p.line(CX - 8, yy, CX + 8, yy, c)

    def ex_aloha(self):
        p = self.p
        for (x, y) in ((-6, 30), (-2, 33), (3, 30), (6, 35), (-5, 37), (1, 38)):
            p.dot(CX + x, y, 0)
            p.dot(CX + x + 1, y, 3)

    def ex_ribs(self):
        p = self.p
        for yy in (29, 32, 35):
            p.line(CX - 6, yy, CX + 6, yy, 3)
        p.line(CX, 27, CX, 38, 3)

    def ex_hump(self):
        pass

    def ex_blush_dots(self):
        p = self.p
        cx, cy = self.head_c
        p.dot(cx - 7, cy + 4, 2)
        p.dot(cx + 7, cy + 4, 2)

    def ex_cheeks(self):
        self.ex_blush_dots()


# =============================================================================================
def to_image(px, colors):
    im = Image.new("P", (N, N), 0)
    flat = []
    for c in colors:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    for y in range(N):
        for x in range(N):
            im.putpixel((x, y), int(px[y, x]))
    return im


def sheet(slugs, out, colors=((255, 255, 255), (240, 190, 150), (60, 100, 200), (0, 0, 0)), scale=5, cols=6):
    import cast
    cell = N * scale + 8
    rows = (len(slugs) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cell, rows * (cell + 14)), (70, 100, 140))
    d = ImageDraw.Draw(sh)
    for k, s in enumerate(slugs):
        px = draw(cast.CAST[s])
        im = to_image(px, colors).convert("RGB").resize((N * scale, N * scale), Image.NEAREST)
        x0, y0 = (k % cols) * cell + 4, (k // cols) * (cell + 14) + 12
        sh.paste(im, (x0, y0))
        d.text((x0, y0 - 11), s, fill=(255, 255, 255))
    sh.save(out)


if __name__ == "__main__":
    import cast
    names = sys.argv[2:] or list(cast.CAST)
    sheet(names, sys.argv[1])
