"""TITHE CITY outdoor tileset: gothic towers, a corrupt cathedral, neon loan sharks.

Roles (see kits.tithe): floor, plaza, facade (floor to the south of the wall), roof (floor to the north), side_e (floor to the
east), side_w (floor to the west), mass (deep inside), center/mart/house blocks, rift (cathedral portal), border."""
from tilebuild import Tileset, Canvas, GRAY, RED, GREEN, WATER, YELLOW, BROWN, ROOF
import paint


def cornice(cv):
    """Row 0 of a facade: a stone cornice over brick."""
    paint.brick(cv, 0, 0, 4, 1)
    for x in range(32):
        cv.set(x, 0, 3)
        cv.set(x, 1, 1)
        cv.set(x, 2, 0 if x % 4 else 2)  # corbel teeth
        cv.set(x, 3, 2)
        cv.set(x, 4, 3 if x % 8 == 0 else 2)


def plinth(cv):
    """Row 3 of a facade: the base of the wall on the street."""
    paint.brick(cv, 0, 3, 4, 1)
    for x in range(32):
        cv.set(x, 24, 1)
        cv.set(x, 25, 0)
        cv.set(x, 26, 2)
        cv.set(x, 27, 0)
        cv.set(x, 28, 0 if x % 8 else 2)
        cv.set(x, 29, 0)
        cv.set(x, 30, 2)
        cv.set(x, 31, 3)


def facade(windows, name=None):
    cv = Canvas()
    paint.brick(cv, 0, 0, 4, 4)
    cornice(cv)
    plinth(cv)
    for bay, kind in enumerate(windows):
        x = bay * 16
        if kind is None:
            continue
        slot = kind[1]
        cv.cell(bay * 2, 1, slot, 2, 2)
        cv.rect(x, 8, 16, 16, 0)
        if kind[0] == "gothic":
            cv.box(x + 1, 8, 14, 16, 3)
            paint.pointed_arch(cv, x + 3, 9, 10, 13)
            paint.sill(cv, x + 2, 22, 12)
            cv.rect(x, 8, 1, 16, 2)
            cv.rect(x + 15, 8, 1, 16, 2)
        elif kind[0] == "round":
            paint.rose(cv, x + 8, 15, 7)
    return cv


def panel(kind, lines):
    """A sign filling the 32x16 window band of a facade."""
    cv = Canvas()
    paint.brick(cv, 0, 0, 4, 4)
    cornice(cv)
    plinth(cv)
    slot = kind
    cv.cell(0, 1, slot, 4, 2)
    cv.rect(0, 8, 32, 16, 3)
    cv.box(1, 9, 30, 14, 2)
    cv.box(2, 10, 28, 12, 0)
    n = len(lines)
    y = 10 + (12 - (5 * n + (n - 1) * 2)) // 2
    for t in lines:
        w = cv.text_width(t)
        cv.text(2 + (28 - w) // 2, y, t, 1)
        y += 7
    return cv


def boards():
    cv = Canvas()
    paint.brick(cv, 0, 0, 4, 4)
    cornice(cv)
    plinth(cv)
    cv.cell(0, 1, BROWN, 4, 2)
    for y in range(8, 24):
        for x in range(32):
            cv.set(x, y, 3 if (y - 8) % 4 == 3 else (1 if (x + (y - 8) // 4 * 5) % 11 else 2))
    cv.line(2, 9, 29, 22, 3)
    cv.line(3, 9, 30, 22, 2)
    for yy in (9, 13, 17, 21):
        cv.set(1, yy, 3)
        cv.set(30, yy, 3)
    return cv


def roof_fill(hi=True):
    cv = Canvas()
    cv.all_slot(ROOF)
    for y in range(32):
        for x in range(32):
            Y = y % 4
            jx = 0 if (y // 4) % 2 == 0 else 4
            v = 0
            if Y == 0:
                v = 1
            elif Y == 3:
                v = 2
            elif x % 8 == jx:
                v = 2
            cv.set(x, y, v)
    return cv


def roof_edge(side):
    """Parapet on one side of a roof: side in 'n', 'e', 'w'."""
    cv = roof_fill()
    if side == "n":
        cv.cell(0, 0, GRAY, 4, 1)
        for x in range(32):
            cv.set(x, 0, 3)
            cv.set(x, 1, 1)
            cv.set(x, 2, 0)
            cv.set(x, 3, 2)
            cv.set(x, 4, 3 if x % 8 else 2)
            for y in range(5, 8):
                cv.set(x, y, 0 if (x + y) % 4 else 2)
        for y in range(5, 8):
            for x in range(32):
                cv.set(x, y, 2 if y == 7 else (0 if x % 8 else 2))
    elif side == "e":
        cv.cell(3, 0, GRAY, 1, 4)
        for y in range(32):
            cv.set(24, y, 3)
            cv.set(25, y, 2)
            cv.set(26, y, 0)
            cv.set(27, y, 0)
            cv.set(28, y, 1)
            cv.set(29, y, 0)
            cv.set(30, y, 2)
            cv.set(31, y, 3)
            if y % 8 == 3:
                for x in range(24, 32):
                    cv.set(x, y, 2 if x not in (24, 31) else 3)
    else:
        cv.cell(0, 0, GRAY, 1, 4)
        for y in range(32):
            cv.set(0, y, 3)
            cv.set(1, y, 2)
            cv.set(2, y, 0)
            cv.set(3, y, 1)
            cv.set(4, y, 0)
            cv.set(5, y, 0)
            cv.set(6, y, 2)
            cv.set(7, y, 3)
            if y % 8 == 3:
                for x in range(0, 8):
                    cv.set(x, y, 2 if x not in (0, 7) else 3)
    return cv


def chimney(cv, cx, cy):
    cv.cell(cx, cy, GRAY, 1, 1)
    paint.brick(cv, cx, cy)
    x, y = cx * 8, cy * 8
    cv.box(x + 1, y + 1, 6, 6, 3)
    cv.rect(x + 2, y + 2, 4, 4, 2)
    cv.set(x + 3, y + 3, 3)


def skylight(cv, cx, cy):
    cv.cell(cx, cy, WATER, 2, 2)
    x, y = cx * 8, cy * 8
    cv.rect(x, y, 16, 16, 0)
    cv.box(x + 1, y + 1, 14, 14, 3)
    for k in range(2, 14):
        cv.hline(x + 2, y + k, 12, 1 if (k + 0) % 3 else 2)
    cv.line(x + 2, y + 13, x + 13, y + 2, 2)


def side_windows(side, rows):
    """A side wall with a column of lit window slits; rows lists the cell rows that get a window."""
    cv = roof_edge(side)
    cx = 3 if side == "e" else 0
    for cy in rows:
        cv.cell(cx, cy, YELLOW)
        x0 = cx * 8
        for y in range(8):
            for x in range(8):
                cv.set(x0 + x, cy * 8 + y, 0)
        edge = 7 if side == "e" else 0
        cv.vline(x0 + edge, cy * 8, 8, 3)
        wx = x0 + (2 if side == "e" else 3)
        cv.box(wx - 1, cy * 8 + 1, 5, 7, 3)
        cv.rect(wx, cy * 8 + 2, 3, 5, 1)
        cv.vline(wx + 1, cy * 8 + 2, 5, 2)
        cv.hline(wx, cy * 8 + 4, 3, 2)
    return cv


def roof_ridge():
    cv = roof_fill()
    for x in range(32):
        cv.set(x, 12, 3)
        cv.set(x, 13, 1)
        cv.set(x, 14, 1)
        cv.set(x, 15, 0)
        cv.set(x, 16, 2)
        cv.set(x, 17, 3)
    return cv


def roof_tank():
    cv = roof_fill()
    cv.cell(1, 1, BROWN, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, 0)
    cv.disc(16, 16, 7, 3)
    cv.disc(16, 16, 6, 1)
    for y in (12, 16, 20):
        cv.hline(11, y, 11, 2)
    cv.disc(14, 14, 1, 0)
    return cv


def roof_spire():
    cv = roof_fill()
    cv.cell(1, 1, GRAY, 2, 2)
    for y in range(8, 24):
        for x in range(8, 24):
            cv.set(x, y, 0)
    cv.box(8, 8, 16, 16, 3)
    for y in range(9, 23):
        for x in range(9, 23):
            dx, dy = x - 15.5, y - 15.5
            if abs(dx) > abs(dy):
                v = 0 if dx < 0 else 2
            else:
                v = 1 if dy < 0 else 2
            cv.set(x, y, v)
    cv.line(9, 9, 22, 22, 3)
    cv.line(22, 9, 9, 22, 3)
    cv.disc(15, 15, 1, 3)
    return cv


def cobbles(variant=0):
    cv = Canvas()
    paint.slabs(cv, 0, 0, 4, 4)
    if variant == 1:  # cracked
        for (x, y) in ((4, 2), (5, 3), (6, 4), (6, 5), (7, 6), (18, 11), (19, 12), (20, 12), (21, 13), (21, 14), (9, 24), (10, 25), (11, 25)):
            cv.set(x, y, 0)
    elif variant == 2:  # manhole
        cv.disc(15, 15, 6, 3)
        cv.disc(15, 15, 5, 2)
        cv.hline(10, 15, 11, 1)
        cv.vline(15, 10, 11, 1)
        cv.ring(15, 15, 3, 0)
    elif variant == 3:  # puddle
        cv.cell(1, 1, WATER, 2, 2)
        cv.rect(8, 8, 16, 16, 0)
        for (y, a, b) in ((10, 11, 20), (11, 9, 22), (12, 8, 23), (13, 8, 23), (14, 8, 23), (15, 9, 22), (16, 9, 22), (17, 11, 21), (18, 13, 19)):
            cv.hline(a, y, b - a, 1)
        cv.hline(11, 12, 5, 2)
        cv.hline(15, 15, 6, 2)
        for (y, a, b) in ((9, 11, 20), (19, 13, 19)):
            cv.hline(a, y, b - a, 2)
    elif variant == 4:  # oil stain
        for (y, a, b) in ((10, 11, 19), (11, 9, 22), (12, 8, 23), (13, 8, 24), (14, 9, 23), (15, 10, 21), (16, 12, 19)):
            cv.hline(a, y, b - a, 2)
    return cv


def plaza_tile(coin):
    cv = Canvas()
    # big slabs 16x16 with a bevel
    for y in range(32):
        for x in range(32):
            X, Y = x % 16, y % 16
            v = 1
            if X == 15 or Y == 15:
                v = 0
            elif X == 14 or Y == 14:
                v = 2
            cv.set(x, y, v)
    if coin:
        cv.cell(1, 1, YELLOW, 2, 2)
        cv.rect(8, 8, 16, 16, 0)
        cv.disc(15, 15, 7, 3)
        cv.disc(15, 15, 6, 1)
        cv.ring(15, 15, 4, 2)
        cv.text(13, 12, "$", 3)
        cv.rect(9, 14, 1, 2, 0)
    return cv


def side_house_roof(side):
    return roof_edge(side)


def door_art(cv, x, y, lamp_slot=None):
    """A 16x16 arched door whose cells (x/8.., y/8..) are BROWN."""
    cv.cell(x // 8, y // 8, BROWN, 2, 2)
    cv.rect(x, y, 16, 16, 0)
    paint.pointed_arch(cv, x + 1, y, 14, 15, glass=1, dark=2, line=3, lattice=False)
    cv.vline(x + 5, y + 5, 10, 2)
    cv.vline(x + 8, y + 3, 12, 3)
    cv.vline(x + 10, y + 5, 10, 2)
    cv.set(x + 6, y + 9, 3)
    cv.set(x + 11, y + 9, 3)
    cv.hline(x, y + 15, 16, 3)


def door_facade(lamp):
    """Facade block with a door in the bottom-left quadrant and a lit window to its right."""
    cv = Canvas()
    paint.brick(cv, 0, 0, 4, 4)
    cornice(cv)
    plinth(cv)
    # transom lamp above the door
    cv.cell(0, 1, lamp, 2, 1)
    cv.rect(0, 8, 16, 8, 0)
    cv.box(2, 9, 12, 7, 3)
    paint.pointed_arch(cv, 3, 9, 10, 7, glass=1, dark=2, line=3, lattice=False)
    door_art(cv, 0, 16)
    # window right bay
    cv.cell(2, 1, YELLOW, 2, 2)
    cv.rect(16, 8, 16, 16, 0)
    cv.box(17, 8, 14, 16, 3)
    paint.pointed_arch(cv, 19, 9, 10, 13)
    paint.sill(cv, 18, 22, 12)
    return cv


def roof_corner(side, chim=False):
    cv = roof_edge("n")
    edge = roof_edge("e" if side == "r" else "w")
    cx = 3 if side == "r" else 0
    for cy in range(1, 4):
        cv.cell(cx, cy, GRAY)
        for y in range(8):
            for x in range(8):
                cv.set(cx * 8 + x, cy * 8 + y, edge.p[(cy * 8 + y) * 32 + cx * 8 + x])
    if chim:
        chimney(cv, 2 if side == "l" else 1, 2)
    return cv


def portal():
    """The cathedral portal: a lit rose-less gothic door in the bottom-left quadrant, a buttress beside it."""
    cv = Canvas()
    paint.brick(cv, 0, 0, 4, 4)
    cornice(cv)
    cv.cell(0, 1, WATER, 2, 1)
    cv.rect(0, 8, 16, 8, 0)
    cv.box(0, 8, 16, 8, 3)
    paint.pointed_arch(cv, 1, 8, 14, 8, glass=1, dark=2, line=3, lattice=False)
    door_art(cv, 0, 16)
    cv.cell(2, 1, GRAY, 2, 3)
    paint.brick(cv, 2, 1, 2, 3)
    for y in range(8, 32):
        cv.set(16, y, 3)
        cv.set(17, y, 1)
        cv.set(30, y, 3)
        cv.set(31, y, 2)
    cv.rect(21, 11, 2, 9, 3)  # arrow slits
    cv.rect(26, 11, 2, 9, 3)
    cv.hline(16, 31, 16, 3)
    cv.hline(0, 30, 16, 2)
    cv.hline(0, 31, 16, 3)
    return cv


def border_block():
    cv = Canvas()
    paint.brick(cv, 0, 0, 4, 4, hi=None)
    return cv


# which block roles the autotiler may use where (see areas/layout.py autotile)
AUTO = {"facade": [("facade", 1)], "side_e": [("side_e", 1), ("side_e_win", 2)], "side_w": [("side_w", 1), ("side_w_win", 2)],
        "roof": [("roof", 1)], "mass": [("mass", 6), ("mass_rare", 1)]}
# facade order in build(): gothic blue, gothic gold, mixed, rose, red, LOANS, PRAY. PAY., boards
FACADE_WEIGHTS = [3, 3, 3, 1, 1, 1, 1, 1]


def build():
    t = Tileset("Tithe", "TILESET_TITHE", "tithe")
    ids = {}
    # block 0 MUST be the border: LoadMetatiles draws block id 0 as wMapBorderBlock, so a real block can never have id 0
    ids["border"] = t.add(border_block(), "WALL", "border")
    # floors
    t.add(cobbles(0), "FLOOR", "floor")
    t.add(cobbles(0), "FLOOR", "floor")
    t.add(cobbles(1), "FLOOR", "floor")
    t.add(cobbles(2), "FLOOR", "floor_rare")
    t.add(cobbles(3), "FLOOR", "floor_rare")
    t.add(cobbles(4), "FLOOR", "floor_rare")
    t.add(plaza_tile(True), "FLOOR", "plaza")
    t.add(plaza_tile(False), "FLOOR", "plaza")
    # facades facing south
    g, y_, r_, b_ = ("gothic", WATER), ("gothic", YELLOW), ("gothic", RED), ("round", YELLOW)
    t.add(facade([g, g]), "WALL", "facade")
    t.add(facade([y_, y_]), "WALL", "facade")
    t.add(facade([y_, g]), "WALL", "facade")
    t.add(facade([None, b_]), "WALL", "facade")
    t.add(facade([r_, r_]), "WALL", "facade")
    t.add(panel(RED, ["LOANS"]), "WALL", "facade")
    t.add(panel(YELLOW, ["PRAY.", "PAY."]), "WALL", "facade")
    t.add(boards(), "WALL", "facade")
    # roofs
    t.add(roof_edge("n"), "WALL", "roof")
    t.add(roof_edge("e"), "WALL", "side_e")
    t.add(roof_edge("w"), "WALL", "side_w")
    t.add(side_windows("e", (1, 3)), "WALL", "side_e_win")
    t.add(side_windows("e", (0, 2)), "WALL", "side_e_win")
    t.add(side_windows("w", (1, 3)), "WALL", "side_w_win")
    t.add(side_windows("w", (0, 2)), "WALL", "side_w_win")
    t.add(roof_fill(), "WALL", "mass")
    m1 = roof_fill()
    chimney(m1, 1, 1)
    t.add(m1, "WALL", "mass_rare")
    m2 = roof_fill()
    skylight(m2, 2, 2)
    t.add(m2, "WALL", "mass_rare")
    t.add(roof_ridge(), "WALL", "mass_rare")
    t.add(roof_tank(), "WALL", "mass_rare")
    t.add(roof_spire(), "WALL", "mass_rare")
    # the Pokecenter and Mart (2x2 blocks: roof, roof / door, sign), houses, the portal, the border
    ids["cr_l"] = t.add(roof_corner("l"), "WALL", "center_roof")
    ids["cr_r"] = t.add(roof_corner("r"), "WALL", "center_roof")
    ids["c_door"] = t.add(door_facade(RED), ("WALL", "WALL", "DOOR", "WALL"), "center_door")
    ids["c_sign"] = t.add(panel(RED, ["POKE"]), "WALL", "center_sign")
    ids["m_door"] = t.add(door_facade(YELLOW), ("WALL", "WALL", "DOOR", "WALL"), "mart_door")
    ids["m_sign"] = t.add(panel(YELLOW, ["MART"]), "WALL", "mart_sign")
    ids["hr_l"] = t.add(roof_corner("l", True), "WALL", "house_roof")
    ids["hr_r"] = t.add(roof_corner("r", True), "WALL", "house_roof")
    ids["h_door"] = t.add(door_facade(WATER), ("WALL", "WALL", "DOOR", "WALL"), "house_door")
    ids["h_side"] = t.add(facade([y_, None]), "WALL", "house_side")
    ids["rift"] = t.add(portal(), ("WALL", "WALL", "DOOR", "WALL"), "rift")
    t.ids = ids
    return t


if __name__ == "__main__":
    t = build().pack()
    print("tiles", t.used, "blocks", len(t.blocks))
