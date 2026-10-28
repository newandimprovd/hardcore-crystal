"""Shared structure of the area tilesets (Grove, Axiom, Lotus, Dis): the block order and the role table.

An area module defines a painter class P with one method per block type (see build()), the constants AUTO and FACADE_WEIGHTS
and gets its Tileset from build_set().  Block 0 is always the border (the engine draws map block id 0 as the border block).
Roles (areas/layout.py autotile): floor / floor_rare, plaza, facade (floor to the south of the wall), roof (floor to the north),
side_e (floor to the east), side_w (floor to the west), mass (deep inside), the Pokecenter / Mart / house blocks, rift, border."""
from tilebuild import Tileset

AUTO = {"facade": [("facade", 1)], "side_e": [("side_e", 1), ("side_e_win", 2)], "side_w": [("side_w", 1), ("side_w_win", 2)],
        "roof": [("roof", 1)], "mass": [("mass", 6), ("mass_rare", 1)]}
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
    t.ids = ids
    return t


def fill(cv, cx, cy, cw, ch, slot, fn):
    """Give the cells the slot and set every pixel to fn(x, y) (absolute pixel coordinates on the block)."""
    cv.cell(cx, cy, slot, cw, ch)
    for y in range(cy * 8, (cy + ch) * 8):
        for x in range(cx * 8, (cx + cw) * 8):
            cv.set(x, y, fn(x, y))


def speckle(table, x, y):
    """table: {(X, Y): index} within an 8x8 tile, 0 elsewhere."""
    return table.get((x % 8, y % 8), 0)
