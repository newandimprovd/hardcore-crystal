"""Body plans for the creature sprites (see creature.py).  A plan draws a whole creature into a Scene from a parameter dict and optional hooks:
hooks["pre"](sc, a)    behind everything (wings, back plumes)
hooks["body"](sc, a)   after the body and legs, before the head
hooks["post"](sc, a)   after the head (crests, flames, extra eyes)
`a` is the anchor dict of the plan (body centre, head centre, back line...) so a hook can attach things to the creature."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from creature import GROUND, Scene, clamp, spline  # noqa: E402


def _hook(hooks, name, sc, a):
    f = (hooks or {}).get(name)
    if f:
        f(sc, a)


# =============================================================================================
# QUADRUPED, seen from the side facing left (front view) or from behind (back view)
# =============================================================================================
def quad(sc, p, hooks=None):
    if sc.back:
        return quad_back(sc, p, hooks)
    m = sc.m
    rx, ry = p.get("body", (17, 10))
    leg = p.get("leg", 11)
    lw = p.get("legw", 6.5)
    cx = p.get("cx", 31)
    cy = GROUND - leg - ry + 3
    rot = p.get("rot", 0)
    hdx, hdy = p.get("head_off", (-17, -8))
    hrx, hry = p.get("head", (8, 7))
    sn = p.get("snout", (6, 3.5))  # rx, ry of the snout
    sdx = p.get("snout_dx", 0.8)
    dx, dy = sc.head()
    hc = (cx + hdx + dx, cy + hdy + dy)
    a = dict(cx=cx, cy=cy, rx=rx, ry=ry, hc=hc, ground=GROUND, rump=(cx + rx * 0.92, cy - ry * 0.1),
             back=lambda t: (cx + rx * (0.9 - 1.8 * t), cy - ry * (0.78 + 0.1 * math.sin(math.pi * t))), lw=lw)
    _hook(hooks, "pre", sc, a)

    # far legs, drawn first and darker
    for x, d in ((cx - rx * 0.55 + 4.5, -1), (cx + rx * 0.5 + 4, -1)):
        lm = sc.mask()
        sc.tube(lm, [(x, cy + ry * 0.2), (x - 0.3, GROUND - 3)], lw * 0.9, lw * 0.75)
        sc.ell(lm, x - 1.5, GROUND - 1.6, lw * 0.75, 2.0)
        sc.paint(lm, base=0.35, gain=0.55)
    # tail
    tail_style = p.get("tail", "plain")
    tl = p.get("tail_len", 14)
    sw = sc.sway()
    ra = a["rump"]
    tpts = [ra, (ra[0] + tl * 0.4, ra[1] + 1 + sw), (ra[0] + tl * 0.8, ra[1] - 3 + sw * 2), (ra[0] + tl, ra[1] - 6 + sw * 3)]
    tm = sc.mask()
    sc.tube(tm, tpts, p.get("tail_w", 6), 2.2 if tail_style != "club" else 5)
    if tail_style == "club":
        sc.ell(tm, tpts[-1][0] + 1, tpts[-1][1] - 1, 5, 5)
    sc.paint(tm)
    if tail_style in ("spike", "club") and m > 0.3:
        for i in range(3):
            t = 0.45 + 0.17 * i
            tx, ty = spline(tpts, t)
            sm = sc.mask()
            sc.spike(sm, tx, ty - 1, tx + 0.5, ty - 5 - 2 * m, 3.2)
            sc.paint(sm, fill=2, shade=None)
    if tail_style == "flame":
        fx, fy = tpts[-1]
        for i, (ox, oy, h) in enumerate(((0, 0, 9), (-3, 2, 6), (3, 2, 5))):
            fm = sc.mask()
            sc.poly(fm, [(fx + ox - 3, fy + oy + 2), (fx + ox, fy + oy - h), (fx + ox + 3, fy + oy + 2)])
            sc.paint(fm, fill=2 if i == 0 else 0, shade=None)
    # body
    bm = sc.mask()
    sc.ell(bm, cx, cy, rx, ry, rot)
    # hips and shoulders thicken the silhouette
    sc.ell(bm, cx + rx * 0.5, cy + ry * 0.15, rx * 0.55, ry * 0.95)
    sc.ell(bm, cx - rx * 0.5, cy + ry * 0.1, rx * 0.5, ry * 0.95)
    bb = sc.paint(bm, rim=p.get("rim", True))
    belly = p.get("belly")
    if belly:
        bl = sc.mask()
        sc.ell(bl, cx - 1, cy + ry * 0.55, rx * 0.75, ry * 0.5)
        belly_bits = bl.bits()
        inner = [[bb[y][x] and belly_bits[y][x] for x in range(sc.n)] for y in range(sc.n)]
        sc.over(bb, belly, lambda x, y: inner[y][x] and (x + y) % 3 != 0)
    # near legs
    for x in (cx - rx * 0.55, cx + rx * 0.5):
        lm = sc.mask()
        sc.tube(lm, [(x, cy + ry * 0.2), (x - 0.5, GROUND - 3)], lw, lw * 0.85)
        sc.ell(lm, x - 2, GROUND - 1.8, lw * 0.85, 2.3)
        sc.paint(lm, rim=True)
        sc.claws(x - lw * 0.8 - 1, GROUND - 1, -1, 3, 2.2, 2.5 + m)
    _hook(hooks, "body", sc, a)

    # neck and head
    nm = sc.mask()
    sc.tube(nm, [(cx - rx * 0.6, cy - ry * 0.1), ((cx - rx * 0.6 + hc[0]) / 2, (cy + hc[1]) / 2 + 1), hc], p.get("neck_w", 9), p.get("neck_w", 9) * 0.9)
    sc.paint(nm, rim=True)
    hm = sc.mask()
    sc.ell(hm, hc[0], hc[1], hrx, hry)
    sn_c = (hc[0] - hrx * sdx, hc[1] + hry * 0.25)
    sc.ell(hm, sn_c[0], sn_c[1], sn[0], sn[1])
    sc.paint(hm, rim=True)
    # jaw
    jaw = p.get("jaw", 0)
    if jaw:
        jm = sc.mask()
        o = 1.0 + 2.5 * sc.mouth() + 1.5 * m
        sc.ell(jm, sn_c[0] + 1, sn_c[1] + sn[1] * 0.8 + o, sn[0] * 0.85, sn[1] * 0.6)
        sc.paint(jm, shade=None, fill=1)
        # mouth gap
        sc.line(sn_c[0] - sn[0] * 0.8, sn_c[1] + sn[1] * 0.55 + 0.5, sn_c[0] + sn[0] * 0.5, sn_c[1] + sn[1] * 0.5 + 0.5, 3)
        if m > 0.2:
            sc.fangs(sn_c[0] - sn[0] * 0.5, sn_c[1] + sn[1] * 0.55 + 1, sn[0] * 0.9, 3, 2 + m)
    # eye
    sc.eye(hc[0] - hrx * 0.1, hc[1] - hry * 0.2, p.get("eye", "angry"), 3.2, -1)
    # ears and horns
    ears = p.get("ears", "none")
    if ears != "none":
        for ex, h in ((hc[0] + hrx * 0.1, 7), (hc[0] + hrx * 0.7, 6)):
            em = sc.mask()
            if ears == "long":
                sc.tube(em, [(ex, hc[1] - hry * 0.6), (ex + 3, hc[1] - hry - 6), (ex + 7, hc[1] - hry - 8)], 4.5, 2)
            else:
                sc.spike(em, ex, hc[1] - hry * 0.7, ex + 1, hc[1] - hry - h, 5)
            sc.paint(em, shade=None, rim=False)
    nh = p.get("horns", 0)
    for i in range(nh):
        hx0 = hc[0] + hrx * (0.0 + 0.55 * i)
        hm2 = sc.mask()
        L = p.get("horn_len", 8) * (0.6 + 0.7 * m)
        sc.tube(hm2, [(hx0, hc[1] - hry * 0.75), (hx0 + 2, hc[1] - hry - L * 0.6), (hx0 + 5 + i, hc[1] - hry - L)], 4, 1.2)
        sc.paint(hm2, fill=2, shade=None)
    _hook(hooks, "post", sc, a)
    return sc.result()


def quad_back(sc, p, hooks=None):
    """Seen from behind: a broad rump, two legs, the head peeking over the shoulders, the tail hanging down the middle."""
    m = sc.m
    rx, ry = p.get("body", (17, 10))
    leg = p.get("leg", 11)
    lw = p.get("legw", 6.5)
    bw = min(rx * 0.95, 17)
    cx = 28
    cy = GROUND - leg - ry + 3
    a = dict(cx=cx, cy=cy, rx=bw, ry=ry, hc=(cx, cy - ry - 3), ground=GROUND, lw=lw)
    _hook(hooks, "pre", sc, a)
    for x in (cx - bw * 0.5, cx + bw * 0.5):
        lm = sc.mask()
        sc.tube(lm, [(x, cy + ry * 0.2), (x, GROUND - 3)], lw, lw * 0.85)
        sc.ell(lm, x, GROUND - 1.8, lw * 0.9, 2.3)
        sc.paint(lm, rim=True)
        sc.claws(x, GROUND - 1, 0, 3, 2.2, 2.5 + m)
    hrx, hry = p.get("head", (8, 7))
    hm = sc.mask()
    sc.ell(hm, cx, cy - ry * 0.9 - 2, hrx * 0.95, hry * 0.9)
    sc.paint(hm, rim=True)
    ears = p.get("ears", "none")
    if ears != "none":
        for sx in (-1, 1):
            em = sc.mask()
            ex = cx + sx * hrx * 0.7
            if ears == "long":
                sc.tube(em, [(ex, cy - ry - 6), (ex + sx * 2, cy - ry - 12), (ex + sx * 4, cy - ry - 16)], 4.5, 2)
            else:
                sc.spike(em, ex, cy - ry - 5, ex + sx * 1, cy - ry - 11, 5)
            sc.paint(em, shade=None)
    for i in range(p.get("horns", 0)):
        sx = (-1, 1)[i % 2] if p.get("horns", 0) > 1 else 0
        hm2 = sc.mask()
        L = p.get("horn_len", 8) * (0.6 + 0.7 * m)
        sc.tube(hm2, [(cx + sx * hrx * 0.5, cy - ry - 5), (cx + sx * (hrx * 0.7 + 2), cy - ry - 5 - L * 0.6), (cx + sx * (hrx + 3), cy - ry - 5 - L)], 4, 1.2)
        sc.paint(hm2, fill=2, shade=None)
    bm = sc.mask()
    sc.ell(bm, cx, cy, bw, ry)
    sc.ell(bm, cx, cy + ry * 0.4, bw * 0.95, ry * 0.8)
    sc.paint(bm, rim=True)
    # tail
    tail_style = p.get("tail", "plain")
    tm = sc.mask()
    ty0 = cy + ry * 0.5
    sw = sc.sway()
    sc.tube(tm, [(cx, ty0), (cx + 2 + sw, ty0 + 6), (cx + 6 + sw * 2, ty0 + 9)], p.get("tail_w", 6) * 0.9, 2.2)
    sc.paint(tm)
    _hook(hooks, "body", sc, a)
    _hook(hooks, "post", sc, a)
    return sc.result()


# =============================================================================================
# spine and back decorations shared by the plans
# =============================================================================================
def spikes_along(sc, a, count, size, t0=0.05, t1=0.95, fill=2, back_only=False):
    """Triangular spikes standing up from the back line of the quad anchor dict."""
    for i in range(count):
        t = t0 + (t1 - t0) * (i + 0.5) / count
        x, y = a["back"](t)
        sm = sc.mask()
        sc.spike(sm, x, y + 1.5, x + 1.2, y - size * (0.8 + 0.4 * math.sin(math.pi * t)), 3.6 + size * 0.15)
        sc.paint(sm, fill=fill, shade=None)
