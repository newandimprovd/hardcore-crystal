"""THE LOTUS COAST (Lotus) outdoor tileset: white stucco hotels, terracotta roofs, striped awnings, rooftop pools, palms, sun-bleached pavers.

Palette slots (areapal AREA4 out): GRAY stucco/sand (cream base), RED coral and awnings, GREEN palms, WATER pools and windows, YELLOW sun,
BROWN shutters and wood, ROOF terracotta (own coral base).  Index 0 of every slot except ROOF is the shared cream."""
import math

from tilebuild import Canvas, GRAY, RED, GREEN, WATER, YELLOW, BROWN, ROOF
from common import AUTO, FACADE_WEIGHTS, build_set, fill, speckle  # noqa: F401
import paint

PAVER_A = {(2, 2): 1, (5, 5): 1, (6, 1): 1}
PAVER_B = {(1, 6): 1, (4, 3): 1, (6, 6): 1, (3, 0): 1}


def paver(x, y):
    X, Y = x % 16, y % 16
    if X == 15 or Y == 15:
        return 1  # grout
    return speckle(PAVER_A if (x // 8 + y // 8) % 2 == 0 else PAVER_B, x, y)


def stucco(x, y):
    return speckle({(1, 2): 1, (5, 6): 1, (6, 3): 1}, x, y)


def terracotta(x, y, var=0):
    Y = y % 4
    jx = 0 if (y // 4) % 2 == 0 else 4
    X = (x + var * 2) % 8
    if Y == 0:
        return 1
    if Y == 3:
        return 3 if (X - jx) % 8 in (0, 7) else 2
    return 2 if (X - jx) % 8 == 0 else 0


def eave(x, y):
    """Row-0 eave under a stucco facade: terracotta with a deep shadow line."""
    Y = y % 8
    if Y == 7:
        return 3
    if Y == 6:
        return 2
    return terracotta(x, y)


def awning(x, y):
    X, Y = x % 8, y % 8
    if Y == 7:
        return 3 if X % 4 in (0, 3) else (2 if X % 4 == 1 else 0)  # scalloped hem
    return 1 if (X // 2) % 2 == 0 else 0


# ---------------------------------------------------------------- floors
def floor_plain():
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, GRAY, paver)
    return cv


def floor_sand():
    cv = floor_plain()
    for (x, y) in ((6, 5), (7, 5), (8, 6), (21, 12), (22, 12), (23, 13), (12, 22), (13, 22), (14, 23)):
        cv.set(x, y, 2)
    return cv


def floor_cracks():
    cv = floor_plain()
    for (x, y) in ((17, 3), (18, 4), (18, 5), (19, 6), (4, 19), (5, 20), (6, 20), (7, 21)):
        cv.set(x, y, 2)
    return cv


def rare_tidepool():
    cv = floor_plain()
    cv.cell(1, 1, WATER, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    for (y, a, b) in ((10, 11, 21), (11, 9, 23), (12, 8, 24), (13, 8, 24), (14, 8, 24), (15, 9, 24), (16, 9, 23), (17, 11, 21), (18, 14, 20)):
        cv.hline(a, y, b - a, 2)
        cv.hline(a + 1, y, max(0, b - a - 4), 1)
    cv.hline(11, 12, 4, 0)
    cv.hline(17, 15, 5, 0)
    return cv


def rare_starfish():
    cv = floor_plain()
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        x1, y1 = int(round(15.5 + 6 * math.cos(a))), int(round(15.5 + 6 * math.sin(a)))
        cv.line(15, 15, x1, y1, 2)
        cv.line(16, 15, x1, y1, 1)
    cv.disc(15, 15, 2, 1)
    cv.set(15, 15, 2)
    return cv


def rare_sandal():
    cv = floor_plain()
    cv.cell(1, 1, BROWN, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    # one flip-flop, nobody coming back for it
    for (y, a, b) in ((10, 13, 18), (11, 12, 19), (12, 12, 19), (13, 12, 19), (14, 12, 19), (15, 12, 19), (16, 12, 19), (17, 13, 18), (18, 13, 18), (19, 14, 17)):
        cv.hline(a, y, b - a, 1)
        cv.set(a, y, 3)
        cv.set(b - 1, y, 3)
    cv.hline(14, 9, 3, 3)
    cv.hline(14, 20, 3, 3)
    cv.line(15, 12, 13, 15, 2)
    cv.line(16, 12, 18, 15, 2)
    return cv


def plaza_lotus():
    """The lotus: coral petals around a golden heart on the pavers."""
    cv = floor_plain()
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    for k in range(8):
        a = k * math.pi / 4
        cx, cy = 15.5 + 5 * math.cos(a), 15.5 + 5 * math.sin(a)
        cv.disc(int(round(cx)), int(round(cy)), 2, 2)
        cv.disc(int(round(cx)), int(round(cy)), 1, 1)
    cv.disc(15, 15, 3, 0)
    return cv


def plaza_checker():
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, GRAY, lambda x, y: 0 if (x % 16 in (0, 15) or y % 16 in (0, 15)) else (1 if (x // 16 + y // 16) % 2 else 0))
    return cv


# ---------------------------------------------------------------- hotel fronts
def hotel(inner=None):
    cv = Canvas()
    fill(cv, 0, 0, 4, 1, ROOF, eave)
    fill(cv, 0, 1, 4, 2, GRAY, stucco)
    fill(cv, 0, 3, 4, 1, GRAY, lambda x, y: (3, 1, 1, 0, 0, 0, 1, 2)[y % 8] if (x // 8) % 2 == 0 else (3, 1, 0, 0, 0, 1, 1, 2)[y % 8])
    if inner:
        inner(cv)
    return cv


def _arch_window(cv, x, slot=WATER):
    cv.cell(x // 8, 1, slot, 2, 2)
    cv.rect(x, 8, 16, 16, 0)
    cv.disc(x + 7, 14, 5, 3)
    cv.rect(x + 2, 14, 11, 9, 3)
    cv.disc(x + 7, 14, 4, 1)
    cv.rect(x + 3, 14, 9, 8, 1)
    cv.vline(x + 7, 10, 12, 2)
    cv.hline(x + 3, 17, 9, 2)
    cv.hline(x + 1, 23, 13, 3)
    cv.hline(x + 2, 22, 11, 2)


def f_arch(cv):
    _arch_window(cv, 8)


def f_awning(cv):
    _arch_window(cv, 8)
    cv.cell(1, 1, RED, 2, 1)
    for y in range(8, 16):
        for x in range(8, 24):
            cv.set(x, y, awning(x, y))


def f_two(cv):
    for x in (2, 18):
        cv.cell(x // 8, 1, WATER, 2, 2)
        cv.rect(x, 8, 12, 16, 0)
        cv.box(x + 1, 10, 10, 13, 3)
        cv.rect(x + 2, 11, 8, 11, 1)
        cv.vline(x + 5, 11, 11, 2)
        cv.hline(x + 2, 16, 8, 2)
    cv.cell(0, 1, BROWN, 1, 2)
    cv.cell(3, 1, BROWN, 1, 2)
    for sx in (0, 24):
        for y in range(8, 24):
            for x in range(8):
                cv.set(sx + x, y, (3, 1, 2, 1, 2, 1, 2, 3)[x] if y % 3 else 3)


def f_wave(cv):
    cv.cell(0, 1, WATER, 4, 2)
    cv.rect(0, 8, 32, 16, 0)
    for k in range(3):
        y = 11 + k * 5
        for x in range(32):
            yy = y + int(round(1.6 * math.sin((x + k * 5) * 0.5)))
            cv.set(x, yy, 1)
            cv.set(x, yy + 1, 2)


def f_palm(cv):
    _arch_window(cv, 2)
    cv.cell(2, 1, GREEN, 2, 2)
    cv.rect(16, 8, 16, 16, 0)
    cv.rect(22, 15, 3, 9, 0)
    cv.vline(23, 12, 12, 3)
    cv.vline(24, 12, 12, 1)
    for (dx, dy) in ((-6, 2), (-5, -1), (-3, -3), (5, 2), (4, -1), (2, -3), (0, -4)):
        cv.line(23, 11, 23 + dx, 11 + dy + 3, 2)
        cv.line(24, 11, 24 + dx, 11 + dy + 2, 1)


def f_sign(kind, word):
    def inner(cv):
        cv.cell(0, 1, kind, 4, 2)
        cv.rect(0, 8, 32, 16, 3)
        cv.rect(1, 9, 30, 14, 2)
        cv.rect(2, 10, 28, 12, 0)
        w = cv.text_width(word)
        cv.text(2 + (28 - w) // 2, 13, word, 1)
    return inner


def facades():
    return [hotel(f_arch), hotel(f_awning), hotel(f_two), hotel(f_wave), hotel(f_palm),
            hotel(f_sign(RED, "BAR")), hotel(f_sign(WATER, "LETHE")), hotel(f_sign(YELLOW, "SPA"))]


# ---------------------------------------------------------------- terracotta roofs
def mass():
    cv = Canvas()
    for cy in range(4):
        for cx in range(4):
            fill(cv, cx, cy, 1, 1, ROOF, lambda x, y, v=(cx + cy) % 2: terracotta(x, y, v))
    return cv


def roof_n():
    cv = mass()
    cv.cell(0, 0, GRAY, 4, 1)
    for x in range(32):
        for y in range(8):
            cv.set(x, y, (3, 1, 0, 0, 0, 1, 2, 3)[y] if x % 16 else (3, 1, 1, 1, 1, 1, 2, 3)[y])
    return cv


def parapet(which):
    cv = mass()
    cx = 3 if which == "e" else 0
    cv.cell(cx, 0, GRAY, 1, 4)
    x0 = cx * 8
    for y in range(32):
        for x in range(8):
            ex = 7 - x if which == "e" else x
            v = (3, 1, 0, 0, 0, 0, 2, 3)[ex] if which == "w" else (3, 2, 0, 0, 0, 0, 1, 3)[7 - ex] if False else None
            col = (3, 1, 0, 0, 0, 0, 2, 3)[x] if which == "w" else (3, 2, 0, 0, 0, 0, 1, 3)[x]
            if y % 8 == 7:
                col = 2 if x not in (0, 7) else 3
            cv.set(x0 + x, y, col)
    return cv


def side_win(which, rows):
    cv = parapet(which)
    cx = 3 if which == "e" else 0
    for cy in rows:
        cv.cell(cx, cy, WATER)
        x0 = cx * 8
        for y in range(8):
            for x in range(8):
                cv.set(x0 + x, cy * 8 + y, 0)
        cv.vline(x0 + (7 if which == "e" else 0), cy * 8, 8, 3)
        wx = x0 + (2 if which == "e" else 3)
        cv.rect(wx - 1, cy * 8 + 2, 5, 6, 3)
        cv.rect(wx, cy * 8 + 1, 3, 1, 3)
        cv.rect(wx, cy * 8 + 2, 3, 5, 1)
        cv.vline(wx + 1, cy * 8 + 2, 5, 2)
    return cv


def mass_rares():
    out = []
    a = mass()  # rooftop pool
    a.cell(1, 1, WATER, 2, 2)
    a.rect(8, 8, 16, 16, 0)
    a.box(8, 8, 16, 16, 1)
    a.rect(10, 10, 12, 12, 1)
    for k in range(10, 22, 3):
        a.hline(10, k, 12, 2)
    a.rect(10, 10, 12, 1, 3)
    a.hline(12, 14, 3, 0)
    a.hline(17, 18, 3, 0)
    out.append(a)
    b = mass()  # beach umbrella on the roof deck
    b.cell(1, 1, RED, 2, 2)
    b.rect(8, 8, 16, 16, 0)
    b.disc(15, 15, 7, 3)
    for y in range(8, 24):
        for x in range(8, 24):
            dx, dy = x - 15.5, y - 15.5
            if dx * dx + dy * dy <= 42:
                ang = (math.atan2(dy, dx) + math.pi) / (2 * math.pi) * 8
                b.set(x, y, 1 if int(ang) % 2 == 0 else 0)
    b.disc(15, 15, 1, 2)
    out.append(b)
    c = mass()  # a palm on the terrace
    c.cell(1, 1, GREEN, 2, 2)
    c.rect(8, 8, 16, 16, 0)
    for k in range(8):
        ang = k * math.pi / 4
        x1, y1 = int(round(15.5 + 7 * math.cos(ang))), int(round(15.5 + 7 * math.sin(ang)))
        c.line(15, 15, x1, y1, 2)
        c.line(16, 16, x1, y1, 1)
    c.disc(15, 15, 1, 3)
    out.append(c)
    d = mass()  # a stucco chimney
    d.cell(1, 1, GRAY, 2, 2)
    d.rect(8, 8, 16, 16, 0)
    d.box(9, 9, 14, 14, 3)
    d.rect(10, 10, 12, 12, 1)
    d.rect(12, 12, 8, 8, 3)
    d.rect(13, 13, 6, 6, 2)
    out.append(d)
    e = mass()  # a sun deck of loungers
    e.cell(1, 1, YELLOW, 2, 2)
    e.rect(8, 8, 16, 16, 0)
    for y in (10, 17):
        e.rect(9, y, 14, 5, 1)
        e.box(9, y, 14, 5, 3)
        e.rect(9, y, 4, 5, 2)
    out.append(e)
    return out


# ---------------------------------------------------------------- Pokecenter, Mart, houses, rift
def roof_corner(side_, awn=None):
    cv = mass()
    cv.cell(0, 0, GRAY, 4, 1)
    for x in range(32):
        for y in range(8):
            cv.set(x, y, (3, 1, 0, 0, 0, 1, 2, 3)[y])
    ex = 0 if side_ == "l" else 31
    for y in range(8, 32):
        cv.set(ex, y, 3)
        cv.set(ex + (1 if side_ == "l" else -1), y, 1)
    return cv


def door_block(awn_slot):
    cv = hotel(None)
    cv.cell(0, 1, GRAY, 2, 3)
    # arched doorway with a striped awning over it
    cv.cell(0, 2, BROWN, 2, 2)
    cv.rect(0, 16, 16, 16, 0)
    cv.disc(8, 20, 7, 3)
    cv.rect(1, 20, 14, 12, 3)
    cv.disc(8, 20, 6, 1)
    cv.rect(2, 20, 12, 11, 1)
    cv.vline(8, 14, 17, 2)
    cv.set(6, 25, 3)
    cv.set(10, 25, 3)
    cv.hline(0, 31, 16, 3)
    cv.cell(0, 1, awn_slot, 2, 1)
    for y in range(8, 16):
        for x in range(16):
            cv.set(x, y, awning(x, y))
    cv.cell(2, 1, WATER, 2, 2)
    _arch_window(cv, 16)
    return cv


def sign_block(kind, word):
    return hotel(f_sign(kind, word))


def house_side():
    return hotel(f_two)


def rift():
    """The grand portico: an arch into the dark with the lotus above it."""
    cv = hotel(None)
    cv.cell(0, 1, GRAY, 4, 3)
    fill(cv, 0, 1, 4, 3, GRAY, stucco)
    cv.cell(0, 1, WATER, 2, 3)
    cv.rect(0, 8, 16, 24, 0)
    cv.disc(8, 16, 7, 3)
    cv.rect(1, 16, 14, 16, 3)
    cv.disc(8, 16, 6, 2)
    cv.rect(2, 16, 12, 15, 2)
    for k in range(3):
        cv.hline(3 + k, 20 + k * 3, 10 - 2 * k, 1)
    cv.hline(0, 31, 16, 3)
    cv.cell(2, 1, RED, 2, 2)
    cv.rect(16, 8, 16, 16, 0)
    for k in range(6):
        a = k * math.pi / 3
        cx, cy = 23.5 + 4 * math.cos(a), 15.5 + 4 * math.sin(a)
        cv.disc(int(round(cx)), int(round(cy)), 2, 2)
        cv.disc(int(round(cx)), int(round(cy)), 1, 1)
    cv.disc(23, 15, 2, 0)
    return cv


class P:
    border = staticmethod(mass)
    floors = staticmethod(lambda: [floor_plain(), floor_sand(), floor_cracks()])
    rares = staticmethod(lambda: [rare_tidepool(), rare_starfish(), rare_sandal()])
    plazas = staticmethod(lambda: [plaza_lotus(), plaza_checker()])
    facades = staticmethod(facades)
    roof_n = staticmethod(roof_n)
    side = staticmethod(parapet)
    side_wins = staticmethod(lambda w: [side_win(w, (1, 3)), side_win(w, (0, 2))])
    mass = staticmethod(mass)
    mass_rares = staticmethod(mass_rares)
    center_roof = staticmethod(roof_corner)
    center_door = staticmethod(lambda: door_block(RED))
    center_sign = staticmethod(lambda: sign_block(RED, "POKE"))
    mart_door = staticmethod(lambda: door_block(YELLOW))
    mart_sign = staticmethod(lambda: sign_block(YELLOW, "MART"))
    house_roof = staticmethod(roof_corner)
    house_door = staticmethod(lambda: door_block(WATER))
    house_side = staticmethod(house_side)
    rift = staticmethod(rift)
    grass = staticmethod(lambda: __import__("grass").grass_pair("lotus"))


def build():
    return build_set("Lotus", "TILESET_LOTUS", "lotus", P)
