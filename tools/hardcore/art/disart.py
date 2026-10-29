"""DIS / COCYTUS / JUDECCA outdoor tileset: black basalt, ember seams, lava pools, bone, dead ash trees, ice shards.

Palette slots (areapal AREA5 out): GRAY basalt and ash, RED lava and embers, GREEN dead moss, WATER ice, YELLOW flame, BROWN bone,
ROOF obsidian (own base).  Index 0 of every slot except ROOF is the shared basalt."""
import math

from tilebuild import Canvas, GRAY, RED, GREEN, WATER, YELLOW, BROWN, ROOF
from common import AUTO, FACADE_WEIGHTS, build_set, fill, speckle  # noqa: F401
import paint


def slab(x, y):
    """Basalt paving: bevelled 8x8 stones, lit top-left, dark seams."""
    X, Y = x % 8, y % 8
    if X == 7 or Y == 7:
        return 2
    if X == 0 or Y == 0:
        return 1
    if (X, Y) in ((3, 3), (4, 5)) and (x // 8 + y // 8) % 2:
        return 2
    return 0


def block_wall(x, y):
    """Dark ashlar: courses of 8x4 blocks, mortar seams, a pale chipped corner."""
    X, Y = x % 8, y % 8
    jx = 0 if Y < 4 else 4
    if Y % 4 == 3:
        return 2
    if X == jx:
        return 2
    if Y % 4 == 0 and X in ((jx + 1) % 8, (jx + 2) % 8):
        return 1
    return 0


def rock(x, y, var=0):
    """Obsidian facets: diagonal planes."""
    X, Y = (x + var * 3) % 8, y % 8
    d = (X + Y) % 8
    if d == 0:
        return 2
    if d in (1, 2):
        return 1 if Y < 4 else 0
    return 0


def cliff(x, y):
    Y = y % 8
    X = x % 8
    return (3, 1, 0, 0, 2, 0, 2, 2)[Y] if X not in (3, 4) or Y > 3 else (3, 1, 1, 0, 2, 0, 2, 2)[Y]


def ember(x, y):
    X, Y = x % 8, y % 8
    return 1 if (X + Y) % 8 == 0 else (2 if (X + Y) % 8 in (1, 7) else 0)


# ---------------------------------------------------------------- floors
def floor_plain():
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, GRAY, slab)
    return cv


def floor_ash():
    cv = floor_plain()
    for (x, y) in ((4, 4), (5, 4), (6, 5), (20, 12), (21, 12), (22, 13), (10, 24), (11, 24), (12, 25)):
        cv.set(x, y, 1)
    return cv


def floor_crack():
    cv = floor_plain()
    cv.cell(1, 1, RED, 1, 2)
    for y in range(8, 24):
        for x in range(8, 16):
            cv.set(x, y, slab(x, y))
    for (x, y) in ((11, 8), (12, 9), (12, 10), (11, 11), (10, 12), (10, 13), (11, 14), (12, 15), (13, 16), (12, 17), (11, 18)):
        cv.set(x, y, 1)
        cv.set(x + 1, y, 2)
    return cv


def rare_embers():
    cv = floor_plain()
    cv.cell(1, 1, RED, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, slab(x, y))
    for (x, y, c) in ((10, 11, 1), (11, 11, 2), (14, 14, 1), (15, 14, 1), (19, 10, 1), (20, 18, 1), (12, 20, 2), (13, 20, 1), (18, 15, 2), (17, 21, 1)):
        cv.set(x, y, c)
    return cv


def rare_icepatch():
    cv = floor_plain()
    cv.cell(1, 1, WATER, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    for (y, a, b) in ((9, 12, 20), (10, 10, 22), (11, 9, 23), (12, 8, 24), (13, 8, 24), (14, 8, 24), (15, 8, 24), (16, 9, 23), (17, 10, 22), (18, 12, 20)):
        cv.hline(a, y, b - a, 1)
    cv.hline(10, 11, 5, 0)
    cv.line(9, 16, 14, 11, 2)
    cv.line(14, 17, 21, 10, 2)
    cv.line(17, 13, 22, 17, 2)
    return cv


def rare_bones():
    cv = floor_plain()
    cv.cell(1, 1, BROWN, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, slab(x, y))
    cv.disc(14, 14, 4, 3)
    cv.disc(14, 14, 3, 1)
    cv.rect(12, 16, 5, 3, 1)
    cv.rect(12, 18, 5, 1, 3)
    cv.set(12, 14, 3)
    cv.set(16, 14, 3)
    cv.set(13, 16, 3)
    cv.set(15, 16, 3)
    cv.line(18, 21, 22, 17, 1)
    cv.line(18, 22, 22, 18, 3)
    return cv


def plaza_sigil():
    """A cold sigil on the paving: ring, inverted triangle, one lit eye."""
    cv = floor_plain()
    cv.cell(1, 1, RED, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, slab(x, y))
    cv.disc(15, 15, 7, 2)
    cv.disc(15, 15, 6, 0)
    cv.line(9, 11, 21, 11, 1)
    cv.line(9, 11, 15, 22, 1)
    cv.line(21, 11, 15, 22, 1)
    cv.disc(15, 14, 1, 1)
    return cv


def plaza_slab():
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, GRAY, lambda x, y: 2 if (x % 16 == 15 or y % 16 == 15) else (1 if (x % 16 == 0 or y % 16 == 0) else (2 if (x % 16, y % 16) in ((5, 6), (10, 10)) else 0)))
    return cv


# ---------------------------------------------------------------- fronts: spiked cornice, ashlar, ember-lit base
def front(inner=None):
    cv = Canvas()
    fill(cv, 0, 0, 4, 1, GRAY, cliff)
    fill(cv, 0, 1, 4, 2, GRAY, block_wall)
    fill(cv, 0, 3, 4, 1, GRAY, lambda x, y: (1, 0, 2, 0, 2, 0, 2, 3)[y % 8])
    cv.hline(0, 24, 32, 3)
    if inner:
        inner(cv)
    return cv


def _arch(cv, x, slot, glass):
    cv.cell(x // 8, 1, slot, 2, 2)
    cv.rect(x, 8, 16, 16, 0)
    cv.disc(x + 7, 14, 5, 3)
    cv.rect(x + 2, 14, 11, 9, 3)
    cv.disc(x + 7, 14, 4, glass)
    cv.rect(x + 3, 14, 9, 8, glass)
    cv.vline(x + 7, 11, 11, 3)
    cv.hline(x + 3, 18, 9, 3)
    cv.hline(x + 1, 23, 13, 3)


def f_glow(cv):
    _arch(cv, 8, YELLOW, 1)


def f_ice(cv):
    _arch(cv, 8, WATER, 1)


def f_lavafall(cv):
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.box(8, 8, 16, 16, 3)
    for x in range(9, 23):
        for y in range(9, 23):
            cv.set(x, y, 1 if (x + (y // 3)) % 5 else 2)
    for x in (11, 15, 19):
        cv.vline(x, 9, 14, 1)
    cv.hline(9, 22, 14, 2)


def f_ribs(cv):
    cv.cell(1, 1, BROWN, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.vline(15, 9, 14, 3)
    cv.vline(16, 9, 14, 1)
    for k in range(4):
        y = 11 + k * 3
        cv.line(15, y, 9 + k, y + 2, 3)
        cv.line(16, y, 22 - k, y + 2, 3)
        cv.line(15, y - 1, 10 + k, y + 1, 1)
        cv.line(16, y - 1, 21 - k, y + 1, 1)


def f_skull(cv):
    cv.cell(1, 1, BROWN, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.disc(15, 14, 6, 3)
    cv.disc(15, 14, 5, 1)
    cv.rect(11, 18, 9, 4, 3)
    cv.rect(12, 18, 7, 3, 1)
    cv.rect(11, 13, 3, 3, 3)
    cv.rect(17, 13, 3, 3, 3)
    cv.set(15, 16, 3)
    for x in (13, 15, 17):
        cv.vline(x, 19, 2, 3)


def f_bars(cv):
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.box(9, 9, 14, 14, 3)
    cv.rect(10, 10, 12, 12, 2)
    for x in (12, 15, 18, 21):
        cv.vline(x, 9, 14, 3)
    cv.hline(10, 14, 12, 3)
    cv.rect(13, 16, 2, 2, 1)
    cv.rect(19, 18, 2, 2, 1)


def f_sign(kind, *lines):
    def inner(cv):
        cv.cell(0, 1, kind, 4, 2)
        cv.rect(0, 8, 32, 16, 3)
        cv.rect(1, 9, 30, 14, 2)
        cv.rect(2, 10, 28, 12, 0)
        n = len(lines)
        y = 10 + (12 - (5 * n + (n - 1) * 2)) // 2
        for t in lines:
            w = cv.text_width(t)
            cv.text(2 + (28 - w) // 2, y, t, 1)
            y += 7
    return inner


def facades():
    return [front(f_glow), front(f_ice), front(f_ribs), front(f_skull), front(f_bars),
            front(f_sign(RED, "NO", "EXIT")), front(f_sign(YELLOW, "HOPE", "LOST")), front(f_lavafall)]


# ---------------------------------------------------------------- obsidian mass, crags on the path side
def mass():
    cv = Canvas()
    for cy in range(4):
        for cx in range(4):
            fill(cv, cx, cy, 1, 1, ROOF, lambda x, y, v=(cx + cy) % 3: rock(x, y, v))
    return cv


def roof_n():
    cv = mass()
    cv.cell(0, 0, GRAY, 4, 1)
    for x in range(32):
        h = 3 + (4 if x % 8 == 3 else (3 if x % 8 in (2, 4) else (1 if x % 8 in (1, 5) else 0)))
        for y in range(8):
            cv.set(x, y, 0 if y < 8 - h else (3 if y == 8 - h else (1 if y == 9 - h else 0 if (x + y) % 3 else 2)))
    return cv


def crag(which):
    cv = mass()
    cx = 3 if which == "e" else 0
    cv.cell(cx, 0, GRAY, 1, 4)
    x0 = cx * 8
    for y in range(32):
        d = (3 + (3 if y % 8 in (3, 4) else (2 if y % 8 in (2, 5) else (1 if y % 8 in (1, 6) else 0)))) if True else 0
        for x in range(8):
            ex = (7 - x) if which == "w" else x  # distance from the wall side, so the spikes point at the path
            if which == "e":
                v = 0 if x < 8 - d - 0 else (3 if x == 8 - d else 0)
                v = 0 if x < 8 - d else (3 if x == 8 - d else 0)
                v = 0
            cv.set(x0 + x, y, 0)
        for x in range(8):
            if which == "e":
                depth = x  # 0 at the wall, 7 at the path
                edge = 7 - d
                v = (0 if x > edge else (3 if x == edge else (1 if x == edge - 1 else (2 if (x + y) % 4 == 0 else 0))))
                v = 0 if x > edge else v
            else:
                depth = 7 - x
                edge = d
                v = (0 if x < edge else (3 if x == edge else (1 if x == edge + 1 else (2 if (x + y) % 4 == 0 else 0))))
            cv.set(x0 + x, y, v)
    return cv


def side_win(which, rows):
    cv = crag(which)
    cx = 3 if which == "e" else 0
    for cy in rows:
        cv.cell(cx, cy, RED)
        x0 = cx * 8
        for y in range(8):
            for x in range(8):
                cv.set(x0 + x, cy * 8 + y, 0)
        for k in range(8):
            xx = x0 + (2 + (k % 3) if which == "e" else 3 + (k % 3))
            cv.set(xx, cy * 8 + k, 1)
            cv.set(xx + 1, cy * 8 + k, 2)
    return cv


def mass_rares():
    out = []
    a = mass()  # a lava pool
    a.cell(1, 1, RED, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            a.set(x, y, 2 if (x + y) % 7 == 0 else 1)
    a.box(8, 8, 16, 16, 3)
    for k in range(4):
        a.hline(10 + k, 11 + k * 3, 8, 2)
    a.rect(13, 14, 3, 2, 3)
    out.append(a)
    b = mass()  # a heap of bones
    b.cell(1, 1, BROWN, 2, 2)
    b.rect(8, 8, 16, 16, 0)
    for (x, y) in ((10, 12), (16, 10), (13, 17), (19, 16)):
        b.disc(x, y, 2, 3)
        b.disc(x, y, 1, 1)
    b.line(9, 21, 21, 21, 3)
    b.line(9, 20, 21, 20, 1)
    b.line(10, 9, 14, 14, 1)
    out.append(b)
    c = mass()  # a dead ash tree
    c.cell(1, 1, GREEN, 2, 2)
    c.rect(8, 8, 16, 16, 0)
    c.vline(15, 14, 10, 3)
    c.vline(16, 14, 10, 1)
    c.line(15, 14, 10, 9, 3)
    c.line(16, 14, 21, 9, 3)
    c.line(15, 17, 11, 15, 3)
    c.line(16, 16, 20, 14, 3)
    for (x, y) in ((10, 9), (21, 9), (11, 15), (20, 14), (13, 11), (18, 11)):
        c.set(x, y, 1)
        c.set(x + 1, y + 1, 2)
    out.append(c)
    d = mass()  # an ice shard thrust up through the rock
    d.cell(1, 1, WATER, 2, 2)
    d.rect(8, 8, 16, 16, 0)
    d.polygon = None
    for (x0, x1, y0) in ((9, 14, 12), (13, 19, 8), (18, 23, 13)):
        for y in range(y0, 23):
            half = ((y - y0) // 2) + 1
            cx = (x0 + x1) // 2
            for x in range(cx - half, cx + half + 1):
                if x0 <= x <= x1:
                    d.set(x, y, 1 if x <= cx else 2)
        d.vline((x0 + x1) // 2, y0, 11, 3)
    d.hline(9, 22, 14, 3)
    out.append(d)
    e = mass()  # a brazier
    e.cell(1, 1, YELLOW, 2, 2)
    e.rect(8, 8, 16, 16, 0)
    e.rect(11, 17, 10, 5, 3)
    e.rect(12, 17, 8, 4, 2)
    e.hline(10, 16, 12, 3)
    for (x, y, c) in ((15, 9, 2), (14, 11, 2), (15, 11, 1), (16, 11, 2), (13, 13, 2), (14, 13, 1), (15, 13, 1), (16, 13, 1), (17, 13, 2), (14, 15, 1), (15, 15, 1), (16, 15, 1)):
        e.set(x, y, c)
    out.append(e)
    return out


# ---------------------------------------------------------------- Pokecenter, Mart, houses, rift
def roof_corner(side_, band=None):
    cv = mass()
    cv.cell(0, 0, GRAY, 4, 1)
    for x in range(32):
        h = 3 + (4 if x % 8 == 3 else (3 if x % 8 in (2, 4) else (1 if x % 8 in (1, 5) else 0)))
        for y in range(8):
            cv.set(x, y, 0 if y < 8 - h else (3 if y == 8 - h else (1 if y == 9 - h else 0 if (x + y) % 3 else 2)))
    if band is not None:
        cv.cell(1, 2, band, 2, 1)
        for y in range(16, 24):
            for x in range(8, 24):
                cv.set(x, y, 0)
        cv.rect(14, 16, 4, 8, 1)
        cv.rect(11, 18, 10, 4, 1)
        cv.box(11, 18, 10, 4, 3) if False else None
    ex = 0 if side_ == "l" else 31
    for y in range(8, 32):
        cv.set(ex, y, 3)
    return cv


def door_block(slot):
    cv = front(None)
    cv.cell(0, 1, GRAY, 2, 3)
    fill(cv, 0, 1, 2, 3, GRAY, block_wall)
    cv.cell(0, 2, slot, 2, 2)
    cv.rect(0, 16, 16, 16, 0)
    cv.disc(8, 20, 7, 3)
    cv.rect(1, 20, 14, 12, 3)
    cv.disc(8, 20, 6, 2)
    cv.rect(2, 20, 12, 11, 2)
    cv.vline(8, 14, 17, 3)
    for y in (22, 26):
        cv.hline(2, y, 12, 3)
    cv.rect(5, 17, 2, 3, 1)
    cv.rect(9, 17, 2, 3, 1)
    cv.hline(0, 31, 16, 3)
    cv.cell(0, 1, GRAY, 2, 1)
    cv.cell(2, 1, YELLOW, 2, 2)
    _arch(cv, 16, YELLOW, 1)
    return cv


def sign_block(kind, word):
    return front(f_sign(kind, word))


def house_side():
    return front(f_glow)


def rift():
    """The way down: a black arch with a ring of fire."""
    cv = front(None)
    cv.cell(0, 1, RED, 2, 3)
    cv.rect(0, 8, 16, 24, 0)
    cv.disc(8, 16, 7, 3)
    cv.rect(1, 16, 14, 16, 3)
    cv.disc(8, 16, 6, 2)
    cv.rect(2, 16, 12, 15, 2)
    for k in range(4):
        cv.hline(3 + k, 18 + k * 3, 10 - 2 * k, 1 if k % 2 == 0 else 2)
    cv.hline(0, 31, 16, 3)
    cv.cell(2, 1, YELLOW, 2, 2)
    _arch(cv, 16, YELLOW, 1)
    return cv


class P:
    border = staticmethod(mass)
    floors = staticmethod(lambda: [floor_plain(), floor_ash(), floor_crack()])
    rares = staticmethod(lambda: [rare_embers(), rare_icepatch(), rare_bones()])
    plazas = staticmethod(lambda: [plaza_sigil(), plaza_slab()])
    facades = staticmethod(facades)
    roof_n = staticmethod(roof_n)
    side = staticmethod(crag)
    side_wins = staticmethod(lambda w: [side_win(w, (1, 3)), side_win(w, (0, 2))])
    mass = staticmethod(mass)
    mass_rares = staticmethod(mass_rares)
    center_roof = staticmethod(lambda s: roof_corner(s, RED))
    center_door = staticmethod(lambda: door_block(RED))
    center_sign = staticmethod(lambda: sign_block(RED, "POKE"))
    mart_door = staticmethod(lambda: door_block(YELLOW))
    mart_sign = staticmethod(lambda: sign_block(YELLOW, "MART"))
    house_roof = staticmethod(lambda s: roof_corner(s, None))
    house_door = staticmethod(lambda: door_block(BROWN))
    house_side = staticmethod(house_side)
    rift = staticmethod(rift)
    grass = staticmethod(lambda: __import__("grass").grass_pair("dis"))


def build():
    return build_set("Dis", "TILESET_DIS", "dis", P)
