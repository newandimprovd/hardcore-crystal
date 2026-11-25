"""Shared structure of the area tilesets (Grove, Axiom, Lotus, Dis): the block order and the role table.

An area module defines a painter class P with one method per block type (see build()), the constants AUTO and FACADE_WEIGHTS
and gets its Tileset from build_set().  Block 0 is always the border (the engine draws map block id 0 as the border block).
Roles (areas/layout.py autotile): floor / floor_rare, plaza, facade (floor to the south of the wall), roof (floor to the north),
side_e (floor to the east), side_w (floor to the west), mass (deep inside), the Pokecenter / Mart / house blocks, rift, border."""
import scenery
from tilebuild import Tileset

AUTO = {"facade": [("facade", 1)], "side_e": [("side_e", 1), ("side_e_win", 2)], "side_w": [("side_w", 1), ("side_w_win", 2)],
        "roof": [("roof", 1)], "mass": [("mass", 6), ("mass_rare", 1)],
        # the box kit (add_box_kit): corners of a building, composed from the cells of the blocks above
        "facade_e": [("facade_e", 1)], "facade_w": [("facade_w", 1)], "facade_ew": [("facade_ew", 1)],
        "corner_ne": [("corner_ne", 1)], "corner_nw": [("corner_nw", 1)], "roof_ew": [("roof_ew", 1)], "roof_new": [("roof_new", 1)]}
FACADE_WEIGHTS = [3, 3, 3, 1, 1, 1, 1, 1]  # eight facades: three common, two decorated, three signs


def build_set(name, const, stem, P):
    t = Tileset(name, const, stem)
    ids = {}
    ids["border"] = t.add(P.border(), "WALL", "border")
    for cv in P.floors():  # three
        t.add(cv, "FLOOR", "floor")
    for cv in P.rares():  # three
        t.add(cv, "FLOOR", "floor_rare")
    for cv in P.plazas():  # two, the first is the decorated one
        t.add(cv, "FLOOR", "plaza")
    for cv in P.facades():  # eight
        t.add(cv, "WALL", "facade")
    t.add(P.roof_n(), "WALL", "roof")
    t.add(P.side("e"), "WALL", "side_e")
    t.add(P.side("w"), "WALL", "side_w")
    for cv in P.side_wins("e"):  # two
        t.add(cv, "WALL", "side_e_win")
    for cv in P.side_wins("w"):  # two
        t.add(cv, "WALL", "side_w_win")
    t.add(P.mass(), "WALL", "mass")
    for cv in P.mass_rares():
        t.add(cv, "WALL", "mass_rare")
    ids["cr_l"] = t.add(P.center_roof("l"), "WALL", "center_roof")
    ids["cr_r"] = t.add(P.center_roof("r"), "WALL", "center_roof")
    ids["c_door"] = t.add(P.center_door(), ("WALL", "WALL", "DOOR", "WALL"), "center_door")
    ids["c_sign"] = t.add(P.center_sign(), "WALL", "center_sign")
    ids["m_door"] = t.add(P.mart_door(), ("WALL", "WALL", "DOOR", "WALL"), "mart_door")
    ids["m_sign"] = t.add(P.mart_sign(), "WALL", "mart_sign")
    ids["hr_l"] = t.add(P.house_roof("l"), "WALL", "house_roof")
    ids["hr_r"] = t.add(P.house_roof("r"), "WALL", "house_roof")
    ids["h_door"] = t.add(P.house_door(), ("WALL", "WALL", "DOOR", "WALL"), "house_door")
    ids["h_side"] = t.add(P.house_side(), "WALL", "house_side")
    ids["rift"] = t.add(P.rift(), ("WALL", "WALL", "DOOR", "WALL"), "rift")
    for cv in P.grass():  # two blocks: wild encounters (stage 9)
        t.add(cv, "TALL_GRASS", "grass")
    scenery.add(t, P.floors()[0])  # ponds, fences, ledge, tree, flower beds (after the grass: no earlier block id moves)
    if hasattr(P, "extras"):  # blocks only one tileset has, after all the others (Dis: the volcano summit)
        t.scn.update(P.extras(t, P.floors()[0]))
    t.ids = ids
    add_box_kit(t)
    return t


def _cell(cv, cx, cy):
    """(pixels, slot) of one 8x8 tile of a block canvas."""
    return [cv.p[(cy * 8 + y) * cv.w + cx * 8 + x] for y in range(8) for x in range(8)], cv.s[cy][cx]


def _put(dst, cx, cy, cell):
    px, slot = cell
    dst.s[cy][cx] = slot
    for i, v in enumerate(px):
        dst.p[(cy * 8 + i // 8) * dst.w + cx * 8 + i % 8] = v


def add_box_kit(t):
    """The corners that make a mass of wall blocks read as a box with a roof (alpha 3.3): one shared roof surface and base, and a separate
    wall piece for each of the four directions.  The roles roof, side_e, side_w, facade already face north, east, west and south; this adds what
    happens where two of them meet.  Every new block is composed of whole 8x8 cells copied from the existing blocks, so it costs no new tile:
      corner_ne / corner_nw  parapet along the north, the side wall along the east (west), they meet in the corner
      roof_ew, roof_new      a roof one block wide: both side walls (and the parapet)
      facade_e, facade_w     a building front that ends in a corner post on the east (west) side, one window and a plain bay beside it
      facade_ew              a one block building front: a post at each end and one window between them
    The three windows of the facades (the common ones) give three versions of each front.  Added after every other block: no id moves."""
    r = t.roles
    cvs = lambda role, i=0: t.blocks[r[role][i]][0]  # noqa: E731
    n_, e_, w_, mass = cvs("roof"), cvs("side_e"), cvs("side_w"), cvs("mass")
    blank = t.blocks[t.ids["h_side"]][0]  # facade with the right bay empty: a plain wall in columns 2 and 3
    ALL = ("WALL",) * 4

    def base(src):
        from tilebuild import Canvas
        cv = Canvas()
        for cy in range(4):
            for cx in range(4):
                _put(cv, cx, cy, _cell(src, cx, cy))
        return cv

    def post_e(cv, rows=range(4)):
        for cy in rows:
            _put(cv, 3, cy, _cell(e_, 3, cy))

    def post_w(cv, rows=range(4)):
        for cy in rows:
            _put(cv, 0, cy, _cell(w_, 0, cy))

    def parapet(cv):
        for cx in range(4):
            _put(cv, cx, 0, _cell(n_, cx, 0))

    ids = {}
    cv = base(mass)  # NE: parapet, then the east wall over its end
    parapet(cv)
    post_e(cv)
    ids["corner_ne"] = t.add(cv, ALL, "corner_ne")
    cv = base(mass)
    parapet(cv)
    post_w(cv)
    ids["corner_nw"] = t.add(cv, ALL, "corner_nw")
    cv = base(mass)
    post_e(cv)
    post_w(cv)
    ids["roof_ew"] = t.add(cv, ALL, "roof_ew")
    cv = base(mass)
    parapet(cv)
    post_e(cv)
    post_w(cv)
    ids["roof_new"] = t.add(cv, ALL, "roof_new")
    for fi in range(3):  # the three common facades: their left bay is a window
        win = cvs("facade", fi)
        # window in columns 0 and 1, plain wall in column 2, the post in column 3
        cv = base(blank)
        for cy in range(4):
            for cx in (0, 1):
                _put(cv, cx, cy, _cell(win, cx, cy))
        post_e(cv)
        t.add(cv, ALL, "facade_e")
        # the post in column 0, plain wall in column 1, the window in columns 2 and 3
        cv = base(blank)
        for cy in range(4):
            for cx in (2, 3):
                _put(cv, cx, cy, _cell(win, cx - 2, cy))
            _put(cv, 1, cy, _cell(blank, 3, cy))
        post_w(cv)
        t.add(cv, ALL, "facade_w")
        # a post at each end and the window between
        cv = base(blank)
        for cy in range(4):
            for cx in (1, 2):
                _put(cv, cx, cy, _cell(win, cx - 1, cy))
        post_e(cv)
        post_w(cv)
        t.add(cv, ALL, "facade_ew")
    t.ids.update(ids)


def fill(cv, cx, cy, cw, ch, slot, fn):
    """Give the cells the slot and set every pixel to fn(x, y) (absolute pixel coordinates on the block)."""
    cv.cell(cx, cy, slot, cw, ch)
    for y in range(cy * 8, (cy + ch) * 8):
        for x in range(cx * 8, (cx + cw) * 8):
            cv.set(x, y, fn(x, y))


def speckle(table, x, y):
    """table: {(X, Y): index} within an 8x8 tile, 0 elsewhere."""
    return table.get((x % 8, y % 8), 0)
