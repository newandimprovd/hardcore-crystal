"""Import a finished multi-colour sprite (pixel art, any size, transparent or white background) as a four-colour Game Boy Color picture.

The Game Boy Color picture format allows white, two colours and black.  The importer
  1. undoes an integer upscaling of the source (a 288x288 image that is a 96x96 sprite drawn at 3x becomes 96x96 again),
  2. classifies every source pixel as white, colour 1, colour 2 or black (nearest colour in Lab, lightness weighted up),
  3. shrinks the class map to the picture size with area weights that favour black, so the thin outline of the source survives,
  4. closes the outline around the silhouette and removes stray pixels.
`suggest_palette()` finds the two colours from the source (the recipe keeps them as explicit 5-bit RGB).
"""
import numpy as np
from PIL import Image


def load_native(path):
    a = np.array(Image.open(path).convert("RGBA"))
    h, w = a.shape[:2]
    best = 1
    for k in range(2, 9):
        if h % k or w % k:
            continue
        small = a[::k, ::k]
        if np.array_equal(np.kron(small, np.ones((k, k, 1), a.dtype)), a):
            best = k
    return a[::best, ::best], best


def rgb2lab(rgb):
    c = np.asarray(rgb, float) / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def foreground(nat):
    return nat[..., 3] >= 128


def suggest_palette(path):
    """Two 8-bit colours (lit body, shade/second colour) from the mid-tone pixels of the source, by a weighted two-means in Lab."""
    nat, _ = load_native(path)
    fg = foreground(nat)
    rgb = nat[..., :3][fg].reshape(-1, 3)
    lab = rgb2lab(rgb)
    keep = (lab[:, 0] > 22) & (lab[:, 0] < 86)
    pts, lb = rgb[keep].astype(float), lab[keep]
    order = np.argsort(lb[:, 0])
    c = np.array([lb[order[int(len(order) * 0.75)]], lb[order[int(len(order) * 0.25)]]])
    for _ in range(20):
        d = ((lb[:, None, :] - c[None]) ** 2 * np.array([1.6, 1, 1])).sum(-1)
        lab_ = d.argmin(1)
        for k in range(2):
            if (lab_ == k).any():
                c[k] = lb[lab_ == k].mean(0)
    cols = []
    for k in range(2):
        sel = lab_ == k
        cols.append(tuple(int(round(v)) for v in pts[sel].mean(0)))
    if rgb2lab(np.array(cols[0]))[0] < rgb2lab(np.array(cols[1]))[0]:
        cols.reverse()
    return cols


def classify(nat, pal8, lw=1.5):
    """Class map 0 white, 1 colour 1, 2 colour 2, 3 black for every pixel of nat (the background is classified too; use foreground())."""
    pal = np.array([(255, 255, 255), pal8[0], pal8[1], (0, 0, 0)], float)
    plab = rgb2lab(pal)
    lab = rgb2lab(nat[..., :3])
    d = ((lab[..., None, :] - plab[None, None]) ** 2 * np.array([lw, 1.0, 1.0])).sum(-1)
    return d.argmin(-1)


def fit(cls, fg, size, margin=1, black_w=1.7, bottom=True):
    """Shrink class map and mask to a size x size picture.  Returns (indices, mask)."""
    ys, xs = np.where(fg)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    cls, fg = cls[y0:y1, x0:x1], fg[y0:y1, x0:x1]
    h, w = cls.shape
    s = min((size - 2 * margin) / w, (size - 2 * margin) / h)
    tw, th = max(1, int(round(w * s))), max(1, int(round(h * s)))
    chans = []
    for k in range(4):
        ch = ((cls == k) & fg).astype(np.float32)
        chans.append(np.array(Image.fromarray(ch, "F").resize((tw, th), Image.BOX)))
    cover = np.array(Image.fromarray(fg.astype(np.float32), "F").resize((tw, th), Image.BOX))
    chans = np.stack(chans, -1)
    wgt = np.array([1.0, 1.0, 1.0, black_w])
    idx = (chans * wgt).argmax(-1)
    mask = cover >= 0.5
    out = np.zeros((size, size), np.int8)
    om = np.zeros((size, size), bool)
    ox = (size - tw) // 2
    oy = size - margin - th if bottom else (size - th) // 2
    out[oy:oy + th, ox:ox + tw] = idx
    om[oy:oy + th, ox:ox + tw] = mask
    return out, om


def clean(idx, mask, outline=True):
    n = idx.shape[0]
    idx = np.where(mask, idx, 0).astype(np.int8)
    # remove isolated pixels: a non-black pixel whose four neighbours are all one other class takes that class
    for _ in range(2):
        p = np.pad(idx, 1, mode="edge")
        nb = np.stack([p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]], -1)
        same = (nb == nb[..., :1]).all(-1)
        iso = same & (nb[..., 0] != idx) & mask & (idx != 3)
        idx = np.where(iso, nb[..., 0], idx)
    if outline:
        pm = np.pad(mask, 1, constant_values=False)
        edge = mask & ~(pm[:-2, 1:-1] & pm[2:, 1:-1] & pm[1:-1, :-2] & pm[1:-1, 2:])
        idx = np.where(edge, 3, idx)
    return idx.astype(np.int8)


def convert(path, pal8, size=56, **kw):
    nat, _ = load_native(path)
    fg = foreground(nat)
    cls = classify(nat, pal8)
    idx, mask = fit(cls, fg, size, **kw)
    return clean(idx, mask), mask


def bob_frames(base, mask, bands=((0.0, 0.33),), dx=(1, 0, -1), dy=(0, -1, 0)):
    """Three animation frames: the top part of the picture (rows between the given fractions of its height) shifted a pixel, the rest left alone
    (so only a few tiles change)."""
    ys = np.where(mask.any(1))[0]
    top, bot = ys.min(), ys.max() + 1
    out = []
    for k in range(3):
        fr = base.copy()
        for f0, f1 in bands:
            r0, r1 = int(top + (bot - top) * f0), int(top + (bot - top) * f1)
            band = base[r0:r1].copy()
            band = np.roll(band, dx[k], axis=1)
            if dy[k]:
                band = np.roll(band, dy[k], axis=0)
            fr[r0:r1] = band
        out.append(fr)
    return out


def convert_mirror(path, pal8, size=48, drop_c2=False):
    """A stand-in back picture made from the front sprite: mirrored, smaller, and with colour 2 folded into colour 1 when it only marks
    front-only details such as a belly patch (drop_c2).  Used until the author supplies a real back sprite."""
    nat, _ = load_native(path)
    nat = nat[:, ::-1]
    fg = foreground(nat)
    cls = classify(nat, pal8)
    idx, mask = fit(cls, fg, size)
    if drop_c2:
        idx = np.where(idx == 2, 1, idx)
    return clean(idx, mask)
