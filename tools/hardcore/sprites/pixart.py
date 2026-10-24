"""Tiny pixel-art toolkit for the Hardcore Crystal creature sprites.

Shapes are drawn as smooth masks at 8x and reduced to 48x48 masks; layers are painted back to front
with a black outline per layer and ordered-dither shading, so the result reads as 4-colour GB art.
Palette indices: 0 white (background and highlights), 1 body, 2 accent (red), 3 black.
"""
import math
from PIL import Image, ImageDraw

K = 8
W = 48  # default size; every Mask and Canvas takes its own size
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


class Mask:
    def __init__(self, n=W):
        self.n = n
        self.im = Image.new("L", (n * K, n * K), 0)
        self.d = ImageDraw.Draw(self.im)

    def poly(self, pts):
        self.d.polygon([(x * K, y * K) for x, y in pts], fill=255)
        return self

    def ell(self, cx, cy, rx, ry=None):
        ry = rx if ry is None else ry
        self.d.ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], fill=255)
        return self

    def curve(self, fn, w0, w1, n=48):
        """Tapered stroke along fn(s), s in 0..1."""
        for i in range(n + 1):
            s = i / n
            x, y = fn(s)
            r = (w0 + (w1 - w0) * s) / 2
            self.ell(x, y, r, r)
        return self

    def bits(self):
        n = self.n
        small = self.im.resize((n, n), Image.BOX)
        return [[small.getpixel((x, y)) >= 128 for x in range(n)] for y in range(n)]


def erode(b):
    n = len(b)
    out = [[False] * n for _ in range(n)]
    for y in range(n):
        for x in range(n):
            if b[y][x]:
                ok = True
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < n and 0 <= ny < n) or not b[ny][nx]:
                        ok = False
                        break
                out[y][x] = ok
    return out


class Canvas:
    def __init__(self, n=W):
        self.n = n
        self.px = [[0] * n for _ in range(n)]

    def paint(self, mask, shade=None, outline=True, fill=1, dark=3):
        """Paint a Mask. shade(x, y) -> darkness 0..1 for ordered dithering with `dark`."""
        b = mask.bits() if isinstance(mask, Mask) else mask
        inner = erode(b)
        for y in range(self.n):
            for x in range(self.n):
                if not b[y][x]:
                    continue
                if outline and not inner[y][x]:
                    self.px[y][x] = 3
                    continue
                p = shade(x, y) if shade else 0.0
                t = (BAYER[y % 4][x % 4] + 0.5) / 16
                self.px[y][x] = dark if p > t else fill
        return b

    def dot(self, x, y, c):
        if 0 <= x < self.n and 0 <= y < self.n:
            self.px[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.dot(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.dot(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

    def flip(self):
        c = Canvas(self.n)
        c.px = [row[::-1] for row in self.px]
        return c


def radial(cx, cy, r, base=0.3, gain=0.7, lx=-0.6, ly=-0.7):
    """Shade function for a rounded part lit from the upper left."""
    def f(x, y):
        nx, ny = (x - cx) / r, (y - cy) / r
        v = base + gain * (nx * -lx + ny * -ly) * 0.5 + 0.0
        return max(0.0, min(1.0, v))
    return f


def render(canvases, pal):
    """Stack canvases vertically into an indexed PNG. pal: four (r,g,b) 8-bit colours."""
    n = canvases[0].n
    im = Image.new("P", (n, n * len(canvases)))
    flat = []
    for c in pal:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    for k, cv in enumerate(canvases):
        for y in range(n):
            for x in range(n):
                im.putpixel((x, k * n + y), cv.px[y][x])
    return im


def preview(canvases, pal, path, scale=8, cols=None, bg=(210, 210, 210)):
    cols = cols or len(canvases)
    rows = (len(canvases) + cols - 1) // cols
    m = max(cv.n for cv in canvases)
    sheet = Image.new("RGB", (cols * (m * scale + 8), rows * (m * scale + 8)), bg)
    for k, cv in enumerate(canvases):
        n = cv.n
        im = Image.new("RGB", (n, n))
        for y in range(n):
            for x in range(n):
                im.putpixel((x, y), pal[cv.px[y][x]])
        im = im.resize((n * scale, n * scale), Image.NEAREST)
        sheet.paste(im, ((k % cols) * (m * scale + 8) + 4, (k // cols) * (m * scale + 8) + 4))
    sheet.save(path)


def c5(r, g, b):
    """5-bit RGB (0..31) to an 8-bit colour that converts back to the same 5-bit value."""
    return tuple(round(v * 255 / 31) for v in (r, g, b))
