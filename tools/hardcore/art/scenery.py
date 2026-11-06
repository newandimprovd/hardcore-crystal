"""Scenery blocks shared by the five area tilesets: ponds with shores, fences, a one-way ledge, trees and flower beds.

Everything is drawn from the palette slots (WATER, BROWN, GREEN, RED), so the same picture takes the colors of each area (a glass-blue canal in
the city, a pond in the Commune, a coolant pool in the robot state, a lagoon on the coast, black ice in Dis).  The ground cells use the
tile of the area's own plain floor, so they dedupe against it.  Costs about 30 tiles and 19 blocks per tileset.

Roles added (after the grass blocks, so no existing block id changes):
  pond_c, pond_n, pond_s, pond_e, pond_w, pond_nw, pond_ne, pond_se, pond_sw   a rectangular pond is made of these nine
  pool        a small round pond (four corner tiles), a fountain basin or a puddle
  fence_h, fence_v   a rail, wall to the quadrants it covers (bottom half, right half)
  ledge       one way drop: the bottom quadrants hop down
  tree        a canopy over a trunk, a whole block of wall
  flowers     two passable flower beds
Collision of the pond blocks is WALL (this hack has no Surf, the water is scenery that shapes the path)."""
from tilebuild import Canvas, GRAY, RED, GREEN, WATER, BROWN

SPARK = ["11111111", "11100111", "11111111", "11111111", "11111001", "11111111", "10011111", "11111111"]


def cell_px(cv, cx, cy, rows, slot):
    cv.cell(cx, cy, slot)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            cv.set(cx * 8 + x, cy * 8 + y, int(ch))


def shore_rows(is_water):
    """8x8 pixel rows of a cell from a water mask: water pixels are 1 (0 for sparkles, 2 on the rim), the ground beside water is 0 with a
    3 bank line, the rest of the ground is 0."""
    rows = []
    for y in range(8):
        r = ""
        for x in range(8):
            w = is_water(x, y)
            near = [is_water(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if w:
                r += "2" if not all(near) else SPARK[y][x]
            else:
                r += "3" if any(near) else "0"
        rows.append(r)
    return rows


SHORE = {
    "n": lambda x, y: y >= 4,
    "s": lambda x, y: y <= 3,
    "w": lambda x, y: x >= 4,
    "e": lambda x, y: x <= 3,
    "nw": lambda x, y: x >= 4 and y >= 4 and (x, y) != (4, 4),
    "ne": lambda x, y: x <= 3 and y >= 4 and (x, y) != (3, 4),
    "sw": lambda x, y: x >= 4 and y <= 3 and (x, y) != (4, 3),
    "se": lambda x, y: x <= 3 and y <= 3 and (x, y) != (3, 3),
    "c": lambda x, y: True,
}


def ground(cv, cx, cy, g):
    """Cell (cx, cy) of the area's floor canvas g into the same cell of cv (same pixels and slot: costs no extra tile)."""
    cv.cell(cx, cy, g.s[cy][cx])
    for y in range(8):
        for x in range(8):
            cv.set(cx * 8 + x, cy * 8 + y, g.p[(cy * 8 + y) * g.w + cx * 8 + x])


def new(g):
    cv = Canvas()
    for cy in range(4):
        for cx in range(4):
            ground(cv, cx, cy, g)
    return cv


# 4x4 cell layouts of the pond blocks: G ground, c open water, n s w E shores (E = east shore), 1 2 3 4 = nw ne se sw corners
PONDS = {
    "pond_c": ["cccc", "cccc", "cccc", "cccc"],
    "pond_n": ["GGGG", "nnnn", "cccc", "cccc"],
    "pond_s": ["cccc", "cccc", "ssss", "GGGG"],
    "pond_w": ["Gwcc", "Gwcc", "Gwcc", "Gwcc"],
    "pond_e": ["ccEG", "ccEG", "ccEG", "ccEG"],
    "pond_nw": ["GGGG", "G1nn", "Gwcc", "Gwcc"],
    "pond_ne": ["GGGG", "nn2G", "ccEG", "ccEG"],
    "pond_sw": ["Gwcc", "Gwcc", "G4ss", "GGGG"],
    "pond_se": ["ccEG", "ccEG", "ss3G", "GGGG"],
    "pool": ["GGGG", "G12G", "G43G", "GGGG"],
}


def pond_blocks(g):
    """(role, canvas) for the pond set, see PONDS (E = the east shore tile)."""
    out = []
    keys = {"c": "c", "n": "n", "s": "s", "E": "e", "w": "w", "1": "nw", "2": "ne", "3": "se", "4": "sw"}
    for role, rows in PONDS.items():
        cv = new(g)
        for cy, r in enumerate(rows):
            for cx, ch in enumerate(r):
                if ch == "G":
                    continue
                cell_px(cv, cx, cy, shore_rows(SHORE[keys[ch]]), WATER)
        out.append((role, cv))
    return out


# ----------------------------------------------------------------------------------------------------------- fences
def fence_h(g):
    """A rail across the bottom half of the block: posts at the cell edges, two rails between."""
    cv = new(g)
    post_top = ["00000000", "00000000", "00000000", "00000000", "03333330", "03111130", "03222230", "03111130"]
    rail_top = ["00000000", "00000000", "00000000", "00000000", "33333333", "11111111", "22222222", "11111111"]
    post_bot = ["03222230", "03222230", "03111130", "03222230", "00333300", "00000000", "00000000", "00000000"]
    rail_bot = ["22222222", "11111111", "22222222", "11111111", "00000000", "00000000", "00000000", "00000000"]
    for cx in range(4):
        cell_px(cv, cx, 2, post_top if cx in (0, 3) else rail_top, BROWN)
        cell_px(cv, cx, 3, post_bot if cx in (0, 3) else rail_bot, BROWN)
    return cv


def fence_v(g):
    """A rail down the middle of the right half of the block: a two pixel plank with posts every sixteen pixels."""
    cv = new(g)
    plank_l = ["00000031", "00000032", "00000031", "00000032", "00000031", "00000032", "00000031", "00000032"]
    plank_r = ["13000000", "23000000", "13000000", "23000000", "13000000", "23000000", "13000000", "23000000"]
    post_l = ["00033331", "00032221", "00031111", "00032221", "00033331", "00000032", "00000031", "00000032"]
    post_r = ["13333000", "12223000", "11113000", "12223000", "13333000", "23000000", "13000000", "23000000"]
    for cy in range(4):
        post = cy % 2 == 0
        cell_px(cv, 2, cy, post_l if post else plank_l, BROWN)
        cell_px(cv, 3, cy, post_r if post else plank_r, BROWN)
    return cv


def fence_vl(g):
    """The mirror of fence_v: the rail down the middle of the left half (same tiles, so no tile costs)."""
    cv = new(g)
    plank_l = ["00000031", "00000032", "00000031", "00000032", "00000031", "00000032", "00000031", "00000032"]
    plank_r = ["13000000", "23000000", "13000000", "23000000", "13000000", "23000000", "13000000", "23000000"]
    post_l = ["00033331", "00032221", "00031111", "00032221", "00033331", "00000032", "00000031", "00000032"]
    post_r = ["13333000", "12223000", "11113000", "12223000", "13333000", "23000000", "13000000", "23000000"]
    for cy in range(4):
        post = cy % 2 == 0
        cell_px(cv, 0, cy, post_l if post else plank_l, BROWN)
        cell_px(cv, 1, cy, post_r if post else plank_r, BROWN)
    return cv


# ------------------------------------------------------------------------------------------------------------ ledge
def ledge(g):
    """Top half ground; a lip of grass over a cliff face in the bottom half. The two bottom quadrants hop down."""
    cv = new(g)
    lip = ["00000000", "11011101", "11111111", "22222222", "33333333", "12121212", "21212121", "33333333"]
    face = ["21212121", "12121212", "22222222", "11221122", "22112211", "33333333", "00000000", "00000000"]
    for cx in range(4):
        cell_px(cv, cx, 2, lip, GREEN)
        cell_px(cv, cx, 3, face, GREEN)
    return cv


# ------------------------------------------------------------------------------------------------------------- trees
def tree(g):
    """Canopy of three rows over a short trunk. 10 tiles: four corners, three edges, the fill and the two trunk cells."""
    cv = new(g)
    fill = ["12111211", "11211121", "21112111", "11121112", "12111211", "11211121", "21112111", "11121112"]
    top = ["00000000", "00033330", "00311113", "03111111", "31121112", "31111211", "31112111", "31211121"]
    topl = ["00000000", "00000333", "00033111", "00311112", "03111121", "03112111", "31121112", "31211121"]
    topr = ["00000000", "33300000", "11133000", "21111300", "12111130", "11211130", "21112113", "12111113"]
    left = ["31211121", "31112111", "31121112", "31211121", "31112111", "31121112", "31211121", "31112111"]
    right = ["12111113", "11211113", "21112113", "12111113", "11211113", "21112113", "12111113", "11211113"]
    botl = ["31211121", "32121212", "32212122", "03221221", "03222222", "00332222", "00033322", "00000033"]
    bot = ["12111211", "21212122", "22222222", "22222222", "22222222", "22222222", "33333333", "00000000"]
    botr = ["12111113", "21212123", "22122123", "12212230", "22222230", "22223300", "22333000", "33000000"]
    rows = [[topl, top, top, topr], [left, fill, fill, right], [botl, bot, bot, botr]]
    for cy, r in enumerate(rows):
        for cx, px in enumerate(r):
            cell_px(cv, cx, cy, px, GREEN)
    trunk_l = ["00033333", "00031112", "00031112", "00031112", "00031112", "00031122", "00331222", "03333333"]
    trunk_r = ["33333000", "21113000", "21113000", "21113000", "21113000", "22113000", "22213300", "33333330"]
    cell_px(cv, 1, 3, trunk_l, BROWN)
    cell_px(cv, 2, 3, trunk_r, BROWN)
    return cv


def flowers(g, k):
    """Passable flower bed: a few blossoms on the ground (two tiles per block)."""
    cv = new(g)
    a = ["00000000", "00300030", "03130313", "00300030", "00000000", "00003000", "00031300", "00003000"]
    b = ["00000000", "00003000", "00031300", "00003000", "00000000", "03000300", "31300313", "03000300"]
    cell_px(cv, 1, 1, a if k == 0 else b, RED)
    cell_px(cv, 2, 2, b if k == 0 else a, RED)
    cell_px(cv, 0, 3, a, RED)
    cell_px(cv, 3, 0, b, RED)
    return cv


def add(t, g):
    """Append the scenery blocks to Tileset t; g is the plain floor Canvas of the area. Records the ids in t.scn."""
    scn = {}
    for role, cv in pond_blocks(g):
        scn[role] = t.add(cv, "WALL", role)
    scn["fence_h"] = t.add(fence_h(g), ("FLOOR", "FLOOR", "WALL", "WALL"), "fence_h")
    scn["fence_v"] = t.add(fence_v(g), ("FLOOR", "WALL", "FLOOR", "WALL"), "fence_v")
    scn["fence_vl"] = t.add(fence_vl(g), ("WALL", "FLOOR", "WALL", "FLOOR"), "fence_vl")
    scn["ledge"] = t.add(ledge(g), ("FLOOR", "FLOOR", "HOP_DOWN", "HOP_DOWN"), "ledge")
    scn["tree"] = t.add(tree(g), "WALL", "tree")
    scn["flowers"] = [t.add(flowers(g, k), "FLOOR", "flowers") for k in (0, 1)]
    t.scn = scn
    return scn
