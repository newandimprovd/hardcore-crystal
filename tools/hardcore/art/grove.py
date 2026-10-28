"""THE COMMUNE (Grove) outdoor tileset: cob huts under thatch, timber posts, forest canopy, packed earth, smoldering fire pits.

Palette slots (areapal AREA2 out): GRAY earth/clay/fieldstone, RED paint/coals, GREEN grass, WATER glass/puddles, YELLOW thatch and lantern
light, BROWN timber, ROOF forest canopy (its own mid-green base).  See common.py for the roles."""
from tilebuild import Canvas, GRAY, RED, GREEN, WATER, YELLOW, BROWN, ROOF
from common import AUTO, FACADE_WEIGHTS, build_set, fill, speckle  # noqa: F401
import paint

# ---------------------------------------------------------------- textures (all periodic over 8 pixels so the tiles dedupe)
EARTH_A = {(1, 1): 1, (5, 2): 2, (3, 5): 1, (6, 6): 2, (7, 4): 1}
EARTH_B = {(2, 0): 2, (6, 1): 1, (0, 4): 1, (4, 5): 2, (2, 7): 1, (5, 7): 1}
CLAY = {(2, 1): 1, (3, 1): 1, (6, 4): 2, (1, 5): 1, (2, 5): 1, (5, 7): 2, (7, 2): 2}


def earth(x, y):
    return speckle(EARTH_A if ((x // 8) + (y // 8)) % 2 == 0 else EARTH_B, x, y)


def clay(x, y):
    return speckle(CLAY, x, y)


def thatch(x, y):
    X, Y = x % 8, y % 8
    if Y == 7:
        return 3
    if Y == 6:
        return 2 if X % 2 == 0 else 1
    return 2 if (X + 2 * Y) % 8 in (0, 1) else 1


def timber(x, y):
    X, Y = x % 8, y % 8
    v = (3, 1, 1, 1, 2, 1, 2, 3)[X]
    if (X, Y) in ((2, 2), (5, 6)):
        v = 2
    return v


def canopy(x, y, var=0):
    """Leaf clumps: light top-left, dark under, in two offset rows."""
    X, Y = (x + 4 * ((y // 4) % 2) + var * 3) % 8, y % 4
    if Y == 0:
        return 1 if X in (1, 2, 3) else 0
    if Y == 1:
        return 0 if X in (1, 2, 3) else 2
    if Y == 2:
        return 2 if X in (2, 3, 4) else 0
    return 3 if X in (3, 4) else 0


def canopy_cell(cv, cx, cy, cw=1, ch=1, var=0):
    fill(cv, cx, cy, cw, ch, ROOF, lambda x, y: canopy(x, y, var))


def fieldstone(cv, cx, cy, cw, ch):
    paint.slabs(cv, cx, cy, cw, ch)  # GRAY: light stones in earth-colored mortar


# ---------------------------------------------------------------- floors
def floor_plain():
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, GRAY, earth)
    return cv


def floor_pebbles():
    cv = floor_plain()
    for (px, py) in ((10, 10), (13, 12), (19, 18), (21, 20)):
        cv.rect(px, py, 3, 2, 1)
        cv.hline(px, py + 2, 3, 2)
        cv.set(px, py, 3) if (px + py) % 2 else None
    return cv


def floor_tufts():
    cv = floor_plain()
    cv.cell(2, 1, GREEN)
    cv.rect(16, 8, 8, 8, 0)
    for (bx, by, h) in ((18, 15, 5), (20, 15, 7), (22, 15, 4), (19, 15, 3)):
        cv.vline(bx, by - h, h, 1)
        cv.set(bx, by - h, 2)
    cv.hline(17, 15, 7, 2)
    return cv


def rare_firepit():
    cv = floor_plain()
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.disc(15, 15, 7, 3)
    cv.disc(15, 15, 6, 2)
    cv.disc(15, 15, 4, 0)
    for k in range(12):
        import math
        a = 2 * math.pi * k / 12
        cv.set(int(round(15.5 + 6.5 * math.cos(a))), int(round(15.5 + 6.5 * math.sin(a))), 0 if k % 2 else 3)
    cv.disc(15, 15, 2, 2)
    cv.set(14, 14, 1)
    cv.set(15, 15, 1)
    cv.set(16, 14, 1)
    cv.set(15, 13, 1)
    return cv


def rare_puddle():
    cv = floor_plain()
    cv.cell(1, 1, WATER, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    for (y, a, b) in ((10, 11, 20), (11, 9, 22), (12, 8, 23), (13, 8, 24), (14, 8, 24), (15, 9, 23), (16, 10, 22), (17, 12, 20)):
        cv.hline(a, y, b - a, 2)
        cv.hline(a + 1, y, max(0, b - a - 3), 1) if y < 15 else None
    cv.hline(11, 12, 5, 1)
    cv.hline(15, 14, 6, 1)
    cv.hline(10, 16, 3, 1)
    return cv


def rare_bones():
    cv = floor_plain()
    cv.cell(1, 1, GRAY, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, earth(x, y))
    # a femur and half a rib cage, left by somebody who really did leave no locks
    cv.line(9, 20, 20, 12, 3)
    cv.line(9, 19, 20, 11, 1)
    cv.line(10, 20, 21, 12, 1)
    cv.rect(8, 18, 3, 3, 1)
    cv.rect(19, 10, 3, 3, 1)
    cv.set(8, 18, 3)
    cv.set(21, 10, 3)
    for k in range(3):
        cv.hline(13 + k * 3, 21 + k, 4, 1)
        cv.hline(13 + k * 3, 22 + k, 4, 3)
    return cv


def plaza_spiral():
    cv = floor_plain()
    cv.cell(1, 1, GRAY, 2, 2)
    import math
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, 1 if (x + y) % 2 == 0 else 0)
    cv.disc(15, 15, 8, 2)
    cv.disc(15, 15, 7, 1)
    pts = []
    for i in range(0, 60):
        a = i * 0.36
        r = 0.4 + i * 0.105
        pts.append((int(round(15.5 + r * math.cos(a))), int(round(15.5 + r * math.sin(a)))))
    for (x, y) in pts:
        cv.set(x, y, 2)
    return cv


def plaza_stones():
    cv = Canvas()
    for y in range(32):
        for x in range(32):
            X, Y = x % 16, y % 16
            v = 1
            if X in (0, 15) or Y in (0, 15):
                v = 0
            elif X == 14 or Y == 14:
                v = 2
            elif (X, Y) in ((4, 4), (9, 7), (11, 11), (5, 10)):
                v = 2
            cv.set(x, y, v)
    return cv


# ---------------------------------------------------------------- huts: thatch eave, cob wall between timber posts, fieldstone foot
def hut(inner=None):
    """A hut front: row 0 thatch eave, rows 1-2 cob wall with a timber post at each end, row 3 fieldstone."""
    cv = Canvas()
    fill(cv, 0, 0, 4, 1, YELLOW, thatch)
    fill(cv, 0, 1, 4, 2, GRAY, clay)
    fill(cv, 0, 1, 1, 2, BROWN, timber)
    fill(cv, 3, 1, 1, 2, BROWN, timber)
    fieldstone(cv, 0, 3, 4, 1)
    cv.hline(0, 24, 32, 3)  # the foot line
    if inner:
        inner(cv)
    return cv


def _window(cv, slot, glass, ring=3, shutters=False):
    cv.cell(1, 1, slot, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.disc(15, 15, 6, ring)
    cv.disc(15, 15, 5, glass)
    cv.vline(15, 10, 11, 2 if glass == 1 else 3)
    cv.hline(10, 15, 11, 2 if glass == 1 else 3)
    cv.hline(11, 8, 9, 0)
    if shutters:
        for sx in (8, 22):
            cv.rect(sx, 10, 2, 11, 2)
            cv.vline(sx, 10, 11, 3)


def f_round(cv):
    _window(cv, WATER, 1)


def f_lit(cv):
    _window(cv, YELLOW, 1, shutters=False)


def f_shutters(cv):
    _window(cv, WATER, 1, shutters=True)


def f_mural(cv):
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    import math
    for i in range(0, 80):
        a = i * 0.33
        r = 0.5 + i * 0.085
        x, y = int(round(15.5 + r * math.cos(a))), int(round(15.5 + r * math.sin(a)))
        cv.set(x, y, 1)
        if i % 3 == 0:
            cv.set(x + 1, y, 2)
    cv.disc(15, 15, 1, 2)


def f_rack(cv):
    cv.cell(1, 1, RED, 2, 2)
    cv.rect(8, 8, 16, 16, 0)
    cv.hline(7, 9, 18, 3)
    cv.hline(7, 10, 18, 2)
    for x, l in ((9, 8), (12, 11), (15, 9), (18, 12), (21, 7)):
        cv.vline(x, 11, l, 1)
        cv.vline(x + 1, 11, l, 2)
        cv.set(x, 11 + l, 3)
        cv.set(x + 1, 11 + l, 3)


def f_board(*lines):
    def inner(cv):
        cv.cell(0, 1, BROWN, 4, 2)
        cv.rect(0, 8, 32, 16, 3)
        cv.rect(1, 9, 30, 14, 1)
        for y in (12, 16, 20):
            cv.hline(1, y, 30, 2)
        cv.box(1, 9, 30, 14, 2)
        n = len(lines)
        y = 9 + (14 - (5 * n + (n - 1) * 2)) // 2
        for t in lines:
            w = cv.text_width(t)
            cv.text(1 + (30 - w) // 2, y, t, 3)
            y += 7
    return inner


def facades():
    return [hut(f_round), hut(f_lit), hut(f_shutters), hut(f_mural), hut(f_rack),
            hut(f_board("ALL", "FREE")), hut(f_board("NO", "LOCKS")), hut(f_board("WELCOME"))]


# ---------------------------------------------------------------- the forest around: canopy, a log palisade on the path side
def mass():
    cv = Canvas()
    for cy in range(4):
        for cx in range(4):
            canopy_cell(cv, cx, cy, 1, 1, var=(cx + cy) % 2)
    return cv


def roof_n():
    """Floor to the north: the top row is a scalloped crown over bare earth."""
    cv = mass()
    cv.cell(0, 0, GREEN, 4, 1)
    for x in range(32):
        top = 2 + (3 if (x % 8) in (0, 7) else (1 if (x % 8) in (1, 6) else 0))
        for y in range(8):
            if y < top:
                cv.set(x, y, 0)
            elif y == top:
                cv.set(x, y, 3)
            elif y == top + 1:
                cv.set(x, y, 1)
            else:
                cv.set(x, y, 2 if (x + y) % 4 else 1)
    return cv


def side(which):
    cv = mass()
    cx = 3 if which == "e" else 0
    fill(cv, cx, 0, 1, 4, BROWN, timber)
    # the trunk wall faces the path: one outline on the path side, a dirt-colored gap on the other
    px = 7 if which == "e" else 0
    for y in range(32):
        cv.set(cx * 8 + (0 if which == "e" else 7), y, 2)
    return cv


def side_win(which, rows):
    cv = side(which)
    cx = 3 if which == "e" else 0
    for cy in rows:
        cv.cell(cx, cy, YELLOW)
        x0 = cx * 8
        for y in range(8):
            for x in range(8):
                cv.set(x0 + x, cy * 8 + y, 0)
        cv.vline(x0 + 3, cy * 8, 2, 3)  # rope
        cv.rect(x0 + 2, cy * 8 + 2, 4, 5, 3)
        cv.rect(x0 + 3, cy * 8 + 3, 2, 3, 1)
        cv.hline(x0 + 2, cy * 8 + 7, 4, 2)
    return cv


def mass_rares():
    out = []
    a = mass()  # a stump with a ring of mushrooms
    a.cell(1, 1, GREEN, 2, 2)
    a.rect(8, 8, 16, 16, 0)
    a.disc(15, 15, 6, 3)
    a.disc(15, 15, 5, 2)
    a.disc(15, 15, 3, 1)
    a.disc(15, 15, 1, 2)
    out.append(a)
    b = mass()  # a hollow log
    b.cell(0, 1, BROWN, 4, 2)
    for y in range(8, 24):
        for x in range(32):
            b.set(x, y, 0)
    for x in range(32):
        for y in range(10, 22):
            b.set(x, y, timber(x, y))
        b.set(x, 9, 3)
        b.set(x, 22, 3)
    b.disc(26, 16, 5, 3)
    b.disc(26, 16, 4, 2)
    b.disc(26, 16, 2, 3)
    out.append(b)
    c = mass()  # a totem pole
    c.cell(1, 0, BROWN, 2, 4)
    for y in range(32):
        for x in range(8, 24):
            c.set(x, y, 0)
    for y in range(32):
        for x in range(10, 22):
            c.set(x, y, timber(x, y))
    for (y0, col) in ((3, 3), (14, 3), (23, 3)):
        c.rect(10, y0, 12, 7, 2)
        c.box(10, y0, 12, 7, 3)
        c.rect(12, y0 + 2, 2, 2, 1)
        c.rect(18, y0 + 2, 2, 2, 1)
        c.hline(13, y0 + 5, 6, 3)
    out.append(c)
    d = mass()  # a smoke hole in a roof
    d.cell(1, 1, YELLOW, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            d.set(x, y, thatch(x, y))
    d.disc(15, 15, 5, 3)
    d.disc(15, 15, 4, 2)
    d.disc(15, 14, 2, 3)
    out.append(d)
    e = mass()  # a drying hide
    e.cell(1, 1, BROWN, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            e.set(x, y, 0)
    e.rect(9, 9, 14, 14, 1)
    e.box(9, 9, 14, 14, 3)
    e.line(10, 10, 21, 21, 2)
    e.line(21, 10, 10, 21, 2)
    for k in range(4):
        e.set(9 + k * 4, 8, 3)
        e.set(9 + k * 4, 23, 3)
    out.append(e)
    return out


# ---------------------------------------------------------------- Pokecenter, Mart, houses, rift, border
def thatch_roof(side_, ridge=True):
    cv = Canvas()
    fill(cv, 0, 0, 4, 4, YELLOW, thatch)
    if ridge:
        for x in range(32):
            cv.set(x, 0, 3)
            cv.set(x, 1, 1)
            cv.set(x, 2, 2)
    edge_x = 0 if side_ == "l" else 31
    for y in range(32):
        cv.set(edge_x, y, 3)
        cv.set(edge_x + (1 if side_ == "l" else -1), y, 2)
    return cv


def door_block(lamp_slot):
    """Cob wall with a round-topped timber door in the bottom-left quadrant and a lit round window right of it."""
    cv = Canvas()
    fill(cv, 0, 0, 4, 1, YELLOW, thatch)
    fill(cv, 0, 1, 4, 3, GRAY, clay)
    fill(cv, 3, 1, 1, 2, BROWN, timber)
    fieldstone(cv, 2, 3, 2, 1)
    cv.hline(16, 24, 16, 3)
    # the door
    cv.cell(0, 1, BROWN, 2, 3)
    cv.rect(0, 8, 16, 24, 0)
    cv.disc(8, 16, 7, 3)
    cv.rect(1, 16, 14, 16, 3)
    cv.disc(8, 16, 6, 1)
    cv.rect(2, 16, 12, 15, 1)
    for x in (5, 8, 11):
        cv.vline(x, 11, 20, 2)
    cv.set(12, 22, 3)
    cv.hline(0, 31, 16, 3)
    cv.hline(0, 30, 16, 2)
    # a lamp above the door
    cv.cell(0, 1, lamp_slot, 2, 1)
    cv.rect(0, 8, 16, 8, 0)
    cv.rect(6, 9, 4, 5, 3)
    cv.rect(7, 10, 2, 3, 1)
    cv.vline(8, 8, 1, 3)
    # the window
    cv.cell(2, 1, YELLOW, 2, 2)
    cv.rect(16, 8, 16, 16, 0)
    cv.disc(23, 15, 5, 3)
    cv.disc(23, 15, 4, 1)
    cv.vline(23, 11, 9, 2)
    cv.hline(19, 15, 9, 2)
    return cv


def sign_block(slot, word):
    cv = hut(None)
    cv.cell(0, 1, slot, 4, 2)
    cv.rect(0, 8, 32, 16, 3)
    cv.rect(1, 9, 30, 14, 2)
    cv.rect(2, 10, 28, 12, 0)
    cv.rect(2, 10, 28, 12, 1) if False else None
    w = cv.text_width(word)
    cv.text(2 + (28 - w) // 2, 13, word, 1)
    return cv


def border():
    return mass()


def center_roof(s):
    return thatch_roof(s)


def center_door():
    return door_block(RED)


def center_sign():
    return sign_block(RED, "POKE")


def mart_door():
    return door_block(YELLOW)


def mart_sign():
    return sign_block(YELLOW, "MART")


def house_roof(s):
    cv = thatch_roof(s, ridge=False)
    cv.cell(1 if s == "l" else 2, 2, GRAY)
    return cv


def house_door():
    return door_block(WATER)


def house_side():
    cv = hut(f_lit)
    return cv


def rift():
    """The way into the Grove: a gap between the trees with a painted lintel."""
    cv = door_block(RED)
    return cv


class P:
    border = staticmethod(border)
    floors = staticmethod(lambda: [floor_plain(), floor_pebbles(), floor_tufts()])
    rares = staticmethod(lambda: [rare_firepit(), rare_puddle(), rare_bones()])
    plazas = staticmethod(lambda: [plaza_spiral(), plaza_stones()])
    facades = staticmethod(facades)
    roof_n = staticmethod(roof_n)
    side = staticmethod(side)
    side_wins = staticmethod(lambda w: [side_win(w, (1, 3)), side_win(w, (0, 2))])
    mass = staticmethod(mass)
    mass_rares = staticmethod(mass_rares)
    center_roof = staticmethod(center_roof)
    center_door = staticmethod(center_door)
    center_sign = staticmethod(center_sign)
    mart_door = staticmethod(mart_door)
    mart_sign = staticmethod(mart_sign)
    house_roof = staticmethod(house_roof)
    house_door = staticmethod(house_door)
    house_side = staticmethod(house_side)
    rift = staticmethod(rift)


def build():
    return build_set("Grove", "TILESET_GROVE", "grove", P)
