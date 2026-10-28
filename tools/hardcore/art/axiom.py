"""THE UNION (Axiom) outdoor tileset: gunmetal bulkheads, hazard plinths, monitor banks, red camera lenses, server racks, grating.

Palette slots (areapal AREA3 out): GRAY steel, RED alarm, GREEN terminal, WATER screens, YELLOW hazard and lamps, BROWN rust and pipes,
ROOF hull plates.  Index 0 is the shared gunmetal; floors are drawn light (index 1), walls dark (index 0)."""
import math

from tilebuild import Canvas, GRAY, RED, GREEN, WATER, YELLOW, BROWN, ROOF
from common import AUTO, FACADE_WEIGHTS, build_set, fill, speckle  # noqa: F401
import paint


# ---------------------------------------------------------------- textures
def grate(x, y):
    """Light steel floor plate 8x8: dark seams on two edges, a rivet in the corner."""
    X, Y = x % 8, y % 8
    if X == 7 or Y == 7:
        return 0
    if X == 6 or Y == 6:
        return 2
    if (X, Y) == (1, 1):
        return 2
    if (X, Y) in ((3, 3), (4, 4)) and (x // 8 + y // 8) % 2:
        return 2  # perforation on every other plate
    return 1


def plate(x, y):
    """Dark wall plate: seams every 8, rivets, a lit edge."""
    X, Y = x % 8, y % 8
    if Y == 7:
        return 3 if X % 4 else 2
    if X == 7:
        return 2
    if Y == 0:
        return 1 if X in (1, 2, 3, 4, 5) else 0
    if (X, Y) in ((1, 2), (5, 2), (1, 5), (5, 5)):
        return 1
    return 0


def hull(x, y, var=0):
    X, Y = (x + var * 4) % 8, y % 8
    if X == 0 or Y == 0:
        return 2
    if X == 1 or Y == 1:
        return 1
    if (X, Y) in ((3, 3), (6, 6)):
        return 3
    return 0


def hazard(x, y):
    return 1 if (x + y) % 8 < 4 else 3


# ---------------------------------------------------------------- floors
def floor_plain():
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, GRAY, grate)
    return cv


def floor_lane():
    cv = floor_plain()  # painted guide line
    for y in range(32):
        cv.set(15, y, 0 if y % 8 < 6 else 1)
        cv.set(16, y, 0 if y % 8 < 6 else 1)
    cv.cell(1, 1, YELLOW)
    cv.cell(2, 1, YELLOW)
    cv.cell(1, 2, YELLOW)
    cv.cell(2, 2, YELLOW)
    for cy in (1, 2):
        for cx in (1, 2):
            for y in range(8):
                for x in range(8):
                    cv.set(cx * 8 + x, cy * 8 + y, 0)
    for k in range(3):  # chevrons
        y0 = 9 + k * 5
        for i in range(7):
            cv.set(15 - i, y0 + i // 2 + 1, 1)
            cv.set(16 + i, y0 + i // 2 + 1, 1)
    return cv


def floor_drain():
    cv = floor_plain()
    cv.cell(2, 2, GRAY)
    for y in range(16, 24):
        for x in range(16, 24):
            cv.set(x, y, 0)
    cv.box(16, 16, 8, 8, 3)
    for k in (18, 20, 22):
        cv.hline(17, k, 6, 2)
    for k in range(6):
        cv.set(23 - k, 23, 0)
    return cv


def rare_hazard():
    cv = floor_plain()
    cv.cell(1, 1, YELLOW, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, hazard(x, y))
    cv.box(8, 8, 16, 16, 3)
    cv.rect(12, 12, 8, 8, 0)
    cv.box(12, 12, 8, 8, 3)
    cv.text(14, 13, "!", 1)
    return cv


def rare_coolant():
    cv = floor_plain()
    cv.cell(1, 1, WATER, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    for (y, a, b) in ((10, 11, 21), (11, 9, 23), (12, 8, 24), (13, 8, 24), (14, 8, 24), (15, 9, 24), (16, 9, 23), (17, 11, 21), (18, 14, 20)):
        cv.hline(a, y, b - a, 2)
        cv.hline(a + 1, y, max(0, b - a - 4), 1)
    cv.hline(11, 12, 5, 0)
    cv.hline(16, 15, 6, 0)
    return cv


def rare_hatch():
    cv = floor_plain()
    cv.cell(1, 1, GRAY, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, 1)
    cv.disc(15, 15, 7, 3)
    cv.disc(15, 15, 6, 0)
    cv.disc(15, 15, 5, 2)
    cv.disc(15, 15, 4, 0)
    cv.hline(10, 15, 11, 2)
    cv.vline(15, 10, 11, 2)
    cv.disc(15, 15, 1, 1)
    return cv


def plaza_emblem():
    """The state emblem: a ring around a compliant check mark."""
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, GRAY, lambda x, y: 0 if (x % 16 in (0, 15) or y % 16 in (0, 15)) else (2 if (x % 16 == 14 or y % 16 == 14) else 1))
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.disc(15, 15, 7, 3)
    cv.disc(15, 15, 6, 1)
    cv.disc(15, 15, 4, 0)
    cv.line(11, 15, 14, 18, 1)
    cv.line(14, 18, 19, 11, 1)
    cv.line(11, 16, 14, 19, 2)
    cv.line(14, 19, 19, 12, 2)
    return cv


def plaza_slab():
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, GRAY, lambda x, y: 0 if (x % 16 in (0, 15) or y % 16 in (0, 15)) else (2 if (x % 16 == 14 or y % 16 == 14) else 1))
    return cv


# ---------------------------------------------------------------- facades: rail, plated wall, hazard plinth
def rail(x, y):
    Y = y % 8
    return (3, 1, 1, 0, 0, 2, 0, 2)[Y] if (x % 8 != 7 or Y not in (1, 2)) else 2


def module(inner=None):
    cv = Canvas()
    fill(cv, 0, 0, 4, 1, GRAY, rail)
    fill(cv, 0, 1, 4, 2, GRAY, plate)
    fill(cv, 0, 3, 4, 1, YELLOW, hazard)
    cv.hline(0, 24, 32, 3)
    if inner:
        inner(cv)
    return cv


def _screen(cv, x, kind):
    cx = x // 8
    cv.cell(cx, 1, WATER, 2, 2)
    cv.rect(x, 8, 16, 16, 0)
    cv.box(x + 1, 9, 14, 13, 3)
    cv.rect(x + 2, 10, 12, 11, 2)
    for k in range(10, 21):
        for xx in range(x + 2, x + 14):
            if kind == "scan":
                cv.set(xx, k, 1 if k % 3 else 2)
            elif kind == "text":
                cv.set(xx, k, 2)
    if kind == "text":
        for k, w in enumerate((9, 6, 10, 4, 8)):
            cv.hline(x + 3, 11 + 2 * k, w, 1)
    cv.hline(x + 5, 23, 6, 2)


def f_monitors(cv):
    _screen(cv, 0, "scan")
    _screen(cv, 16, "text")


def f_monitor1(cv):
    _screen(cv, 8, "text")


def f_lens(cv):
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.disc(15, 15, 7, 3)
    cv.disc(15, 15, 6, 2)
    cv.disc(15, 15, 4, 1)
    cv.disc(15, 15, 2, 3)
    cv.set(13, 13, 1)
    cv.set(14, 12, 1)


def f_rack(cv):
    for bay in (0, 1):
        x = 4 + bay * 12
        cv.cell(x // 8, 1, GREEN, 2, 2)
    cv.cell(0, 1, GREEN, 4, 2)
    cv.rect(0, 8, 32, 16, 0)
    for bay in (0, 1):
        x = 2 + bay * 15
        cv.box(x, 8, 13, 16, 3)
        for r in range(4):
            y = 10 + r * 3
            cv.hline(x + 2, y, 9, 2)
            for k in range(4):
                cv.set(x + 3 + k * 2, y, 1 if (k + r + bay) % 3 else 2)
            cv.hline(x + 2, y + 1, 9, 3)


def f_fans(cv):
    cv.cell(0, 1, GRAY, 4, 2)
    for bay in (0, 1):
        cx, cy = 8 + bay * 16, 16
        cv.disc(cx, cy, 6, 3)
        cv.disc(cx, cy, 5, 0)
        for a in (0, 2, 4):
            ang = a * math.pi / 3
            cv.line(cx, cy, int(round(cx + 4 * math.cos(ang))), int(round(cy + 4 * math.sin(ang))), 1)
            cv.line(cx, cy, int(round(cx - 4 * math.cos(ang))), int(round(cy - 4 * math.sin(ang))), 1)
        cv.disc(cx, cy, 1, 2)


def f_blast(cv):
    cv.cell(0, 1, YELLOW, 4, 2)
    for y in range(8, 24):
        for x in range(32):
            cv.set(x, y, hazard(x, y))
    cv.box(0, 8, 32, 16, 3)
    cv.vline(15, 8, 16, 3)
    cv.vline(16, 8, 16, 3)
    cv.rect(11, 14, 3, 4, 3)
    cv.rect(18, 14, 3, 4, 3)


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
    return [module(f_monitors), module(f_monitor1), module(f_lens), module(f_rack), module(f_fans),
            module(f_sign(RED, "OPTIMAL")), module(f_sign(YELLOW, "SORTING")), module(f_blast)]


# ---------------------------------------------------------------- hull
def mass():
    cv = Canvas()
    for cy in range(4):
        for cx in range(4):
            fill(cv, cx, cy, 1, 1, ROOF, lambda x, y, v=(cx + cy) % 2: hull(x, y, v))
    return cv


def roof_n():
    cv = mass()
    cv.cell(0, 0, GRAY, 4, 1)
    for x in range(32):
        for y in range(8):
            cv.set(x, y, (3, 1, 1, 0, 0, 2, 0, 2)[y])
    for x in range(0, 32, 8):
        cv.set(x + 3, 1, 2)
    return cv


def pipes(which):
    cv = mass()
    cx = 3 if which == "e" else 0
    cv.cell(cx, 0, BROWN, 1, 4)
    x0 = cx * 8
    for y in range(32):
        for x in range(8):
            X = x
            v = 0
            if X in (1, 6):
                v = 3
            elif X in (2, 3, 4, 5):
                v = (1, 1, 2, 2)[X - 2] if X > 2 else 1
                v = {2: 1, 3: 1, 4: 2, 5: 2}[X]
            cv.set(x0 + x, y, v)
    for y in (4, 12, 20, 28):  # clamps
        cv.hline(x0, y, 8, 3)
        cv.hline(x0, y + 1, 8, 2)
    return cv


def side_win(which, rows):
    cv = pipes(which)
    cx = 3 if which == "e" else 0
    for cy in rows:
        cv.cell(cx, cy, YELLOW)
        x0 = cx * 8
        for y in range(8):
            for x in range(8):
                cv.set(x0 + x, cy * 8 + y, 0)
        cv.box(x0 + 1, cy * 8 + 1, 6, 6, 3)
        cv.rect(x0 + 2, cy * 8 + 2, 4, 4, 1)
        cv.hline(x0 + 2, cy * 8 + 4, 4, 2)
    return cv


def mass_rares():
    out = []
    a = mass()  # radar dish
    a.cell(1, 1, GRAY, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            a.set(x, y, 0)
    a.disc(15, 15, 7, 3)
    a.disc(15, 15, 6, 1)
    a.disc(15, 15, 4, 0)
    a.disc(15, 15, 2, 2)
    a.line(15, 15, 20, 9, 3)
    a.set(20, 9, 1)
    out.append(a)
    b = mass()  # exhaust stack
    b.cell(1, 1, GRAY, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            b.set(x, y, 0)
    b.rect(9, 9, 14, 14, 3)
    b.rect(10, 10, 12, 12, 2)
    for k in range(10, 22, 2):
        b.hline(10, k, 12, 3)
    b.disc(15, 15, 3, 3)
    out.append(b)
    c = mass()  # warning beacon
    c.cell(1, 1, RED, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            c.set(x, y, 0)
    c.disc(15, 15, 6, 3)
    c.disc(15, 15, 5, 2)
    c.disc(15, 15, 3, 1)
    c.set(14, 13, 0)
    out.append(c)
    d = mass()  # antenna mast
    d.cell(1, 1, GRAY, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            d.set(x, y, 0)
    d.vline(15, 8, 16, 3)
    d.vline(16, 8, 16, 1)
    for k in (10, 14, 18):
        d.hline(15 - (22 - k) // 3, k, 2 * ((22 - k) // 3) + 2, 3)
    out.append(d)
    e = mass()  # solar array
    e.cell(1, 1, WATER, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            e.set(x, y, 2)
    e.box(8, 8, 16, 16, 3)
    for k in range(8, 24, 4):
        e.hline(8, k, 16, 3)
        e.vline(k, 8, 16, 3)
    e.hline(9, 9, 3, 1)
    e.hline(13, 13, 3, 1)
    e.hline(17, 17, 3, 1)
    out.append(e)
    return out


# ---------------------------------------------------------------- Pokecenter, Mart, houses, rift, border
def roof_corner(side_, band=None):
    cv = mass()
    cv.cell(0, 0, GRAY, 4, 1)
    for x in range(32):
        for y in range(8):
            cv.set(x, y, (3, 1, 1, 0, 0, 2, 0, 2)[y])
    if band is not None:
        cv.cell(0, 2, band, 4, 1)
        for y in range(16, 24):
            for x in range(32):
                cv.set(x, y, hazard(x, y) if y in (18, 19, 20, 21) else (3 if y in (17, 22) else 0))
    ex = 0 if side_ == "l" else 31
    for y in range(8, 32):
        cv.set(ex, y, 3)
    return cv


def door_block(lamp_slot):
    cv = module(None)
    cv.cell(0, 1, GRAY, 2, 3)
    # the sliding door: two panels of glass in a frame
    cv.cell(0, 2, WATER, 2, 2)
    cv.rect(0, 8, 16, 8, 0)
    cv.rect(0, 16, 16, 16, 0)
    cv.box(0, 15, 16, 17, 3)
    cv.rect(1, 16, 6, 15, 2)
    cv.rect(9, 16, 6, 15, 2)
    for y in range(17, 30, 3):
        cv.hline(2, y, 4, 1)
        cv.hline(10, y, 4, 1)
    cv.vline(7, 16, 15, 3)
    cv.vline(8, 16, 15, 3)
    cv.hline(0, 31, 16, 3)
    cv.cell(0, 1, lamp_slot, 2, 1)
    cv.rect(0, 8, 16, 7, 0)
    cv.box(2, 9, 12, 5, 3)
    cv.rect(3, 10, 10, 3, 1)
    cv.cell(2, 1, WATER, 2, 2)
    cv.rect(16, 8, 16, 16, 0)
    cv.box(17, 9, 14, 13, 3)
    cv.rect(18, 10, 12, 11, 2)
    for k in range(10, 21, 3):
        cv.hline(18, k, 12, 1)
    return cv


def sign_block(kind, word):
    return module(f_sign(kind, word))


def center_door():
    return door_block(RED)


def mart_door():
    return door_block(YELLOW)


def house_door():
    return door_block(GREEN)


def house_side():
    return module(f_monitor1)


def rift():
    """A vault door: round, red light, hazard frame."""
    cv = module(None)
    cv.cell(0, 1, YELLOW, 2, 3)
    cv.rect(0, 8, 16, 24, 0)
    cv.box(0, 8, 16, 24, 3)
    cv.disc(8, 20, 6, 3)
    cv.disc(8, 20, 5, 1)
    cv.disc(8, 20, 3, 2)
    cv.set(8, 20, 1)
    cv.hline(0, 31, 16, 3)
    cv.cell(2, 1, GRAY, 2, 2)
    paint_wall = fill
    paint_wall(cv, 2, 1, 2, 2, GRAY, plate)
    cv.cell(0, 1, YELLOW, 2, 1)
    for y in range(8, 16):
        for x in range(16):
            cv.set(x, y, hazard(x, y))
    cv.cell(0, 2, RED, 2, 2)
    cv.rect(0, 16, 16, 16, 0)
    cv.disc(8, 24, 7, 3)
    cv.disc(8, 24, 6, 2)
    cv.disc(8, 24, 4, 1)
    cv.disc(8, 24, 2, 2)
    cv.hline(0, 31, 16, 3)
    return cv


class P:
    border = staticmethod(mass)
    floors = staticmethod(lambda: [floor_plain(), floor_lane(), floor_drain()])
    rares = staticmethod(lambda: [rare_hazard(), rare_coolant(), rare_hatch()])
    plazas = staticmethod(lambda: [plaza_emblem(), plaza_slab()])
    facades = staticmethod(facades)
    roof_n = staticmethod(roof_n)
    side = staticmethod(pipes)
    side_wins = staticmethod(lambda w: [side_win(w, (1, 3)), side_win(w, (0, 2))])
    mass = staticmethod(mass)
    mass_rares = staticmethod(mass_rares)
    center_roof = staticmethod(lambda s: roof_corner(s, RED))
    center_door = staticmethod(center_door)
    center_sign = staticmethod(lambda: sign_block(RED, "POKE"))
    mart_door = staticmethod(mart_door)
    mart_sign = staticmethod(lambda: sign_block(YELLOW, "MART"))
    house_roof = staticmethod(lambda s: roof_corner(s, None))
    house_door = staticmethod(house_door)
    house_side = staticmethod(house_side)
    rift = staticmethod(rift)


def build():
    return build_set("Axiom", "TILESET_AXIOM", "axiom", P)
