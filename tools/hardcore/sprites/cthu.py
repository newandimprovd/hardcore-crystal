"""Sprites for CTHUSPAWN and CTHULUDON (the Tentacool line, stages 3 and 4).

CTHUSPAWN is an octopus whose head carries two big glossy red gems (the gems of TENTACRUEL, grown up)
and eight curling tentacles. CTHULUDON is the full cosmic horror: winged, fanged, clawed, with a tentacle
beard and the same two gems. Both are 4-colour Game Boy Color art: white, body, accent, black.
Palettes come from roster_data (single source of truth); run through gen_roster.py.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from pixart import Canvas, Mask, c5, erode, preview, radial, render  # noqa: E402
from roster.roster_data import NEW  # noqa: E402

F = 56  # front size (7x7 tiles)
B = 48  # back size (6x6 tiles)


def pal(name, shiny=False):
    d = NEW[name.upper()]
    body, accent = (d["shiny"] if shiny else d["pal"])
    return [(255, 255, 255), c5(*body), c5(*accent), (0, 0, 0)]


# --------------------------------------------------------------------------- helpers
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


def mirror(pts, n):
    return [(n - 1 - x, y) for x, y in pts]


def swayed(pts, ph, amp, grow=1.0):
    """Move the later control points sideways so the tentacle waves."""
    out = []
    for i, (x, y) in enumerate(pts):
        w = (i / max(len(pts) - 1, 1)) ** 1.3
        out.append((x + math.sin(ph + i * 0.8) * amp * w * grow, y + math.cos(ph * 0.9 + i) * amp * 0.35 * w))
    return out


def tentacle(cv, pts, w0, w1, suckers=True):
    n = cv.n
    m = Mask(n)
    m.curve(lambda s: spline(pts, s), w0, w1, n=70)
    cv.paint(m, shade=lambda x, y: 0.22 if (x + y) % 2 else 0.0, fill=1, dark=3)
    if suckers:
        b = erode(erode(m.bits()))
        for k in range(1, 12):
            x, y = spline(pts, 0.12 + k * 0.07)
            xi, yi = round(x), round(y)
            if 0 <= xi < n and 0 <= yi < n and b[yi][xi]:
                cv.px[yi][xi] = 0


def gem(cv, cx, cy, r, glow=0):
    """Big glossy red sphere: outline, red body, dithered shadow bottom-right, white glints top-left."""
    m = Mask(cv.n).ell(cx, cy, r, r)
    cv.paint(m, shade=radial(cx, cy, r, base=0.12, gain=1.05, lx=-0.7, ly=-0.7), fill=2, dark=3)
    gx, gy = round(cx - r * 0.5), round(cy - r * 0.55)
    cv.dot(gx, gy, 0)
    cv.dot(gx + 1, gy, 0)
    cv.dot(gx, gy + 1, 0)
    if glow:
        cv.dot(gx + 2, gy, 0)
        cv.dot(gx + 1, gy + 1, 0)
        cv.dot(gx, gy + 2, 0)
        cv.dot(round(cx + r * 0.45), round(cy + r * 0.45), 0)


def claws(cv, x, y, d, count=3, gap=2, length=2):
    """Pale claws pointing down from (x, y), fanned slightly toward d."""
    for k in range(count):
        cx = x + (k - (count - 1) / 2) * gap
        for j in range(length):
            cv.dot(round(cx + d * j * 0.5 * (k - (count - 1) / 2)), y + j, 0)
        cv.dot(round(cx + d * length * 0.5 * (k - (count - 1) / 2)), y + length, 3)


# --------------------------------------------------------------------------- CTHUSPAWN
SPAWN_TENT = [
    # outer, curling upward beside the head
    [(15, 27), (9, 29), (4, 25), (4, 18), (9, 14)],
    [(18, 31), (10, 36), (4, 42), (5, 49), (11, 50)],
    [(21, 33), (15, 41), (13, 48), (17, 54), (23, 53)],
    [(25, 35), (22, 43), (23, 50), (28, 54)],
]


def front_cthuspawn(ph=0.0, glow=0, open_=0):
    n = F
    cv = Canvas(n)
    # only the two inner pairs wave, so the animation stays inside the tile budget of a 7x7 pic
    for i, pts in enumerate(SPAWN_TENT):
        amp = 2.4 if i >= 2 else 0.0
        tentacle(cv, swayed(pts, ph, amp), 6.5, 1.8)
        tentacle(cv, swayed(mirror(pts, n), ph + 3.1, amp), 6.5, 1.8)
    # fin flaps either side of the head
    for sx in (0, 1):
        pts = [(13, 21), (6, 25), (7, 31), (14, 30)]
        pts = mirror(pts, n) if sx else pts
        cv.paint(Mask(n).poly(pts), shade=lambda x, y: 0.35)
    head = Mask(n).ell(27.5, 21, 14.5, 12.5)
    cv.paint(head, shade=radial(27.5, 21, 13, base=0.2, gain=0.95))
    # eyes: white with a black slit, angry brows
    for sx in (-1, 1):
        ex = 27 + sx * 7 + (0 if sx > 0 else 1)
        for k in range(-2, 3):
            cv.dot(round(ex + k), 22 - (1 if abs(k) < 2 else 0) + (1 if (k * sx) > 0 else 0), 3)
        cv.rect(round(ex) - 2, 24, round(ex) + 1, 25, 0)
        cv.rect(round(ex) - 2, 26, round(ex) + 1, 26, 3)
        cv.dot(round(ex) - (1 if sx < 0 else 0), 24, 3)
        cv.dot(round(ex) - (1 if sx < 0 else 0), 25, 3)
    # beak
    cv.rect(26, 30, 29, 30, 3)
    cv.rect(27, 31, 28, 31, 3)
    gem(cv, 20.5, 12.5, 6.2, glow)
    gem(cv, 34.5, 12.5, 6.2, glow)
    return cv


def back_cthuspawn():
    n = B
    cv = Canvas(n)
    tents = [
        [(13, 26), (7, 31), (4, 38), (7, 45)],
        [(17, 30), (11, 37), (10, 44), (14, 47)],
        [(21, 32), (17, 40), (19, 46), (23, 47)],
    ]
    for pts in tents:
        tentacle(cv, pts, 6, 1.8)
        tentacle(cv, mirror(pts, n), 6, 1.8)
    head = Mask(n).ell(23.5, 20, 13.5, 12)
    cv.paint(head, shade=radial(23.5, 19, 13, base=0.35, gain=0.95))
    for yy in range(14, 30, 4):  # a faint ridge down the back of the head
        cv.dot(23, yy, 3)
        cv.dot(24, yy + 1, 3)
    gem(cv, 17, 11, 5.4)
    gem(cv, 30, 11, 5.4)
    return cv


# --------------------------------------------------------------------------- CTHULUDON
LUDON_BEARD = [
    [(19, 26), (14, 30), (12, 36), (15, 41), (19, 43), (21, 40)],
    [(22, 29), (19, 35), (19, 42), (22, 47)],
]


def front_cthuludon(ph=0.0, glow=0, open_=0):
    n = F
    cv = Canvas(n)
    # wings: magenta membranes, black ribs
    for sx in (0, 1):
        def X(pts):
            return mirror(pts, n) if sx else pts
        wing = X([(22, 26), (19, 16), (13, 9), (4, 2), (8, 12), (1, 18), (7, 22), (2, 29), (10, 28), (9, 36), (17, 32),
                  (21, 33)])
        cv.paint(Mask(n).poly(wing), shade=lambda x, y: 0.5 if (x + y) % 3 else 0.18, fill=2, dark=3)
        for tip in X([(4, 2), (1, 18), (2, 29), (9, 36)]):
            cv.line(round(X([(22, 26)])[0][0]), 26, round(tip[0]), round(tip[1]), 3)
    # feet first, the body overlaps them
    for sx in (0, 1):
        fx = 40 if sx else 15
        cv.paint(Mask(n).ell(fx, 49, 8, 3.6), shade=lambda x, y: 0.5)
        claws(cv, fx + (3 if sx else -3), 51, -1 if sx else 1, 4, 3, 3)
    # body
    cv.paint(Mask(n).ell(27.5, 38, 11.5, 14), shade=radial(27.5, 36, 14, base=0.55, gain=0.7))
    cv.paint(Mask(n).ell(27.5, 41, 6.5, 10.5), shade=lambda x, y: 0.28 if (x + y) % 2 else 0.05, fill=2, dark=3)
    for yy in (34, 38, 42, 46):
        for xx in range(22, 34):
            cv.dot(xx, yy + round(((xx - 27.5) / 6) ** 2 * 1.6), 3)
    # arms, hanging out to the sides with clawed hands
    for sx in (0, 1):
        pts = [(15, 28), (8, 33), (5, 40), (7, 45)]
        pts = mirror(pts, n) if sx else pts
        arm = Mask(n).curve(lambda s: spline(pts, s), 7, 4.6)
        cv.paint(arm, shade=radial(8 if not sx else 47, 36, 9, base=0.3, gain=0.8))
        hx, hy = round(pts[-1][0]), round(pts[-1][1])
        claws(cv, hx, hy + 1, 1 if sx else -1, 3, 3, 4)
    # head, crest spikes
    for sx in (0, 1):
        sp = [(15, 13), (10, 4), (20, 8)]
        sp = mirror(sp, n) if sx else sp
        cv.paint(Mask(n).poly(sp), shade=lambda x, y: 0.4)
    cv.paint(Mask(n).ell(27.5, 17.5, 13.5, 12), shade=radial(27.5, 17, 13, base=0.2, gain=0.95))
    gem(cv, 21, 9, 4.8, glow)
    gem(cv, 34, 9, 4.8, glow)
    # eyes: glowing, with a heavy brow
    for sx in (-1, 1):
        ex = round(27.5 + sx * 7)
        for k in (-3, -2, -1, 0, 1, 2, 3):
            cv.dot(ex + k, 14 + (1 if k * sx > 0 else 0) + (1 if k * sx > 2 else 0), 3)
        cv.rect(ex - 1, 16, ex + 1, 17, 2)
        cv.dot(ex - (1 if sx < 0 else -1), 16, 0)
    # mouth with fangs: black throat, red tongue
    mo = 1 if open_ else 0
    cv.paint(Mask(n).ell(27.5, 25.5, 6.8, 4.4 + mo), shade=lambda x, y: 1.0, fill=3, dark=3)
    cv.paint(Mask(n).ell(27.5, 27.2 + mo, 3.6, 1.8), shade=lambda x, y: 0.0, fill=2, dark=3, outline=False)
    for fx in (23, 25, 30, 32):
        cv.rect(fx, 22, fx, 24, 0)
    for fx in (26, 29):
        cv.rect(fx, 28 + mo, fx, 29 + mo, 0)
    # tentacle beard over the chest
    for pts in LUDON_BEARD:
        tentacle(cv, swayed(pts, ph, 2.2), 6.5, 2.0)
        tentacle(cv, swayed(mirror(pts, n), ph + 3.1, 2.2), 6.5, 2.0)
    return cv


def back_cthuludon():
    n = B
    cv = Canvas(n)
    for sx in (0, 1):
        def X(pts):
            return mirror(pts, n) if sx else pts
        wing = X([(19, 24), (16, 15), (11, 8), (3, 2), (7, 11), (1, 17), (6, 21), (2, 28), (9, 27), (8, 35), (15, 32),
                  (19, 34)])
        cv.paint(Mask(n).poly(wing), shade=lambda x, y: 0.5 if (x + y) % 3 else 0.18, fill=2, dark=3)
        for tip in X([(3, 2), (1, 17), (2, 28), (8, 35)]):
            cv.line(round(X([(19, 24)])[0][0]), 24, round(tip[0]), round(tip[1]), 3)
    for sx in (0, 1):
        fx = 33 if sx else 14
        cv.paint(Mask(n).ell(fx, 44, 7, 3.4), shade=lambda x, y: 0.5)
        claws(cv, fx + (3 if sx else -3), 45, -1 if sx else 1, 4, 3, 2)
    cv.paint(Mask(n).ell(23.5, 34, 13, 15), shade=radial(23.5, 32, 15, base=0.5, gain=0.8))
    for k in range(5):  # spine ridge
        y = 20 + k * 5
        sp = [(23.5, y - 3), (20.5, y + 1), (26.5, y + 1)]
        cv.paint(Mask(n).poly(sp), shade=lambda x, y_: 0.2)
    cv.paint(Mask(n).ell(23.5, 16, 10.5, 9.5), shade=radial(23.5, 15, 10, base=0.35, gain=0.95))
    for sx in (-1, 1):
        pts = [(23.5 + sx * 9, 20), (23.5 + sx * 11, 26), (23.5 + sx * 10, 32)]
        tentacle(cv, pts, 4.5, 1.6)
    gem(cv, 17.5, 8, 4.4)
    gem(cv, 29.5, 8, 4.4)
    return cv


def build(name, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    f = {"cthuspawn": front_cthuspawn, "cthuludon": front_cthuludon}[name]
    b = {"cthuspawn": back_cthuspawn, "cthuludon": back_cthuludon}[name]
    frames = [f(0.0, 0, 0), f(1.0, 0, 0), f(2.2, 0, 1), f(3.4, 1, 0)]
    render(frames, pal(name)).save(os.path.join(out_dir, "front.png"))
    back = b()
    render([back], pal(name)).save(os.path.join(out_dir, "back.png"))
    return frames, back


def tile_diff(frames):
    base = frames[0]
    n = base.n // 8
    out = []
    for fr in frames[1:]:
        d = 0
        for ty in range(n):
            for tx in range(n):
                a = [r[tx * 8:tx * 8 + 8] for r in base.px[ty * 8:ty * 8 + 8]]
                c = [r[tx * 8:tx * 8 + 8] for r in fr.px[ty * 8:ty * 8 + 8]]
                d += a != c
        out.append(d)
    return out


if __name__ == "__main__":
    prev = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/scratch/cthu_prev.png"
    sheets = []
    for nme in ("cthuspawn", "cthuludon"):
        frames, back = build(nme, f"/home/claude/scratch/sprites/{nme}")
        print(nme, "changed tiles per frame", tile_diff(frames))
        sheets.append((nme, frames, back))
    # preview: for each species the base frame, the back sprite and two animation frames
    for nme, frames, back in sheets:
        preview([frames[0], back, frames[2], frames[3]], pal(nme), prev.replace(".png", f"_{nme}.png"), scale=6, cols=4,
                bg=(60, 90, 140))
    print("wrote previews")
