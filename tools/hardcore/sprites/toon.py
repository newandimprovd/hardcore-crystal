"""Toon shading and four-colour quantisation of sdf.render() buffers.

Palette indices of the output: 0 white (background and highlights), 1 body colour, 2 accent colour, 3 black.
"""
import numpy as np

import sdf

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0 + 1 / 32.0

LIGHT = np.array([-0.5, 0.62, 0.6])
LIGHT = LIGHT / np.linalg.norm(LIGHT)

STYLE = dict(term=0.40, band=0.06, core=0.07, hi=0.93, hi_soft=0.05, outline_depth=0.18, part_depth=0.05)


def reduce(buf, model):
    """ss x ss supersamples -> final pixel buffers: cover, depth, normal, pos, mat, tex (taken from the nearest sample of each pixel)."""
    n, ss = buf["n"], buf["ss"]
    k = ss * ss

    def cells(a):
        sh = (n, ss, n, ss) + a.shape[2:]
        a = a.reshape(sh)
        a = a.transpose((0, 2, 1, 3) + tuple(range(4, a.ndim)))
        return a.reshape((n, n, k) + a.shape[4:])

    hit = cells(buf["hit"])
    depth = cells(buf["depth"])
    nrm = cells(buf["normal"])
    pos = cells(buf["pos"])
    pid = cells(buf["pid"])
    cover = hit.mean(-1)
    w = hit[..., None].astype(float)
    nsum = (nrm * w).sum(2)
    ln = np.linalg.norm(nsum, axis=-1, keepdims=True)
    normal = np.where(ln > 1e-9, nsum / np.maximum(ln, 1e-9), 0.0)
    dd = np.where(hit, depth, np.inf)
    near = dd.argmin(-1)
    ii, jj = np.mgrid[0:n, 0:n]
    dmin = dd[ii, jj, near]
    pid_n = pid[ii, jj, near]
    pos_n = pos[ii, jj, near]
    pm = np.array([p.mat for p in model.prims] + [0], np.int8)
    pt = np.array([p.tex for p in model.prims] + [-1], np.int16)
    pg = np.array([p.grp for p in model.prims] + [0], np.int32)
    mat = pm[pid_n]
    tex = pt[pid_n]
    grp = pg[pid_n]
    return dict(cover=cover, depth=dmin, normal=normal, pos=pos_n, mat=mat, tex=tex, grp=grp, n=n)


def vnoise(p):
    """Value noise on points p (..., 3), 0..1."""
    i = np.floor(p).astype(np.int64)
    f = p - i
    f = f * f * (3 - 2 * f)

    def h(ix, iy, iz):
        v = np.sin(ix * 127.1 + iy * 311.7 + iz * 74.7) * 43758.5453
        return v - np.floor(v)

    out = 0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                wgt = (f[..., 0] if dx else 1 - f[..., 0]) * (f[..., 1] if dy else 1 - f[..., 1]) * (f[..., 2] if dz else 1 - f[..., 2])
                out = out + wgt * h(i[..., 0] + dx, i[..., 1] + dy, i[..., 2] + dz)
    return out


def tex_mask(spec, pos):
    kind = spec[0]
    if kind == "spots":  # ("spots", scale, threshold, colour)
        return vnoise(pos * spec[1]) > spec[2], spec[3]
    if kind == "stripes":  # ("stripes", axis, period, width, colour)
        return ((pos[..., spec[1]] / spec[2]) % 1.0) < spec[3], spec[4]
    if kind == "dots":  # ("dots", cell, radius, colour): bumps on a 3D lattice (scales, rivets, pores)
        q = pos / spec[1]
        fr = q - np.floor(q) - 0.5
        return np.sqrt((fr ** 2).sum(-1)) < spec[2], spec[3]
    if kind == "cracks":  # ("cracks", scale, width, colour): thin winding lines (magma, veins)
        v = vnoise(pos * spec[1])
        return np.abs(v - 0.5) < spec[2], spec[3]
    if kind == "rings":  # ("rings", axis, period, width, colour): rings around an axis (segments)
        a = (pos[..., (spec[1] + 1) % 3] ** 2 + pos[..., (spec[1] + 2) % 3] ** 2) ** 0.5
        return ((a / spec[2]) % 1.0) < spec[3], spec[4]
    raise ValueError(kind)


RAMPS = {
    # material: (highlight, lit, shade, core).  Palette indices: 0 white (glow, highlights, bone), 1 main colour, 2 shade/second colour, 3 black.
    0: (0, 1, 2, 3),   # BODY
    1: (0, 0, 1, 2),   # ACCENT: pale belly and plates, main colour in their shade
    4: (0, 0, 1, 2),   # BONE
    5: (1, 2, 2, 3),   # MEMB: wing membrane and thin skin, the second colour
}


def shade(red, model, style=None):
    """Palette-index image (n x n) from the reduced buffers.  Cel shading in the style of the vanilla sprites: a flat lit colour, a flat shade
    colour behind a narrow dithered terminator, a few white highlight pixels, black only for the outline, creases and the deepest shadow."""
    st = dict(STYLE)
    if style:
        st.update(style)
    ramps = dict(RAMPS)
    ramps.update(getattr(model, "ramps", {}) or {})
    n = red["n"]
    cover = red["cover"]
    solid = cover >= 0.5
    lam = (red["normal"] * LIGHT).sum(-1)
    t = np.clip((lam + 0.15) / 1.15, 0.0, 1.0)
    reps = (n + 3) // 4
    bay = np.tile(BAYER, (reps, reps))[:n, :n]
    yy, xx = np.mgrid[0:n, 0:n]
    checker = ((xx + yy) % 2 == 0)
    band = st["band"]
    # tone level per pixel: 3 highlight, 2 lit, 1 shade, 0 core
    u = np.clip((t - (st["term"] - band)) / (2 * band), 0.0, 1.0)
    lit = u > bay
    level = np.where(lit, 2, 1)
    level = np.where(t < st["core"], np.where(checker & (t > st["core"] * 0.5), 1, 0), level)
    level = np.where((t >= st["hi"]) & (np.clip((t - st["hi"]) / st["hi_soft"], 0, 1) > bay), 3, level)
    mat = red["mat"]
    img = np.zeros((n, n), np.int8)
    for m, (h, l, s_, c) in ramps.items():
        tone = np.choose(level, [c, s_, l, h])
        img = np.where(mat == m, tone, img)
    img = np.where(mat == sdf.DARK, 3, img)
    img = np.where(mat == sdf.EYE, 0, img)
    # textures
    for tid, spec in enumerate(model.texs):
        sel = solid & (red["tex"] == tid) & (t >= st["core"] * 1.5)
        if sel.any():
            m, colour = tex_mask(spec, red["pos"])
            img = np.where(sel & m, np.int8(colour), img)
    img = np.where(solid, img, 0).astype(np.int8)
    # outline: silhouette and depth jumps
    d = red["depth"]
    line = np.zeros((n, n), bool)
    pad = np.pad(solid, 1, constant_values=False)
    dpad = np.pad(d, 1, constant_values=np.inf)
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nb = pad[1 + dy:1 + dy + n, 1 + dx:1 + dx + n]
        nd = dpad[1 + dy:1 + dy + n, 1 + dx:1 + dx + n]
        line |= solid & ~nb
        line |= solid & nb & (nd < d - st["outline_depth"])
        gp = np.pad(red["grp"], 1, constant_values=-1)[1 + dy:1 + dy + n, 1 + dx:1 + dx + n]
        line |= solid & nb & (gp != red["grp"]) & (nd < d - st["part_depth"])
    img = np.where(line, 3, img).astype(np.int8)
    return img


def fit_view(model, cam, fill=0.94, n=48, anchor="center"):
    """Framing (cx, cy, half) that makes the model's silhouette fill `fill` of the canvas."""
    big = 3.5
    buf = sdf.render(model, cam, n=n, ss=1, view=(cam.shift[0], cam.shift[1], big))
    hit = buf["hit"]
    ys, xs = np.where(hit)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    cx = cam.shift[0] + ((x0 + x1) / 2 / n * 2 - 1) * big
    cy = cam.shift[1] - ((y0 + y1) / 2 / n * 2 - 1) * big
    w = (x1 - x0) / n * 2 * big
    h = (y1 - y0) / n * 2 * big
    half = max(w, h) / 2 / fill
    return (cx, cy, half)
