"""Turns: lanes that run east or west, and the bend maps that join them to the road that runs north (alpha 3.2, playtest point 19).

The way through an area used to be a stack of vertical lanes, every one entered at the bottom and left at the top.  Hoenn and Sinnoh routes bend
and cross the region, so now one lane of every act is built as usual and then turned a quarter turn: its corridor is entered from the west and
left on the east (or the other way round), and a small bend map before and after it joins it to the vertical road.

  * rotate() turns a finished lane (or bend) map by quarter turns, blocks, objects, trainer slots, glades and all.  A block keeps its own art,
    so the blocks that have a direction (the pond edges, the rails) are swapped for the block that has the matching edge afterwards, and the
    plain wall of an urban tileset is picked again after the turn (autotile), so the building fronts still face the street.
  * bend() draws the bend map in the frame of a vertical lane (entered at the bottom) with the corridor turning right (R) or left (L), a nook
    beside the road with a hermit and a hidden item, and the rest as landscape.  Turned by 0 to 3 quarters the two shapes make every turn.
  * join() connects two maps along the edges that face each other, with the offset of the corridors, for any pair of directions.

The map edges are kept on every map as m.entry and m.exit: (side, block position of the corridor along that side), sides N E S W."""
import random

from .layout import autotile, reach
from .model import MapDef
from .trail import find_spot, glade, landscape

OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}
CONN = {"N": "north", "S": "south", "E": "east", "W": "west"}
CW_SIDE = {"N": "E", "E": "S", "S": "W", "W": "N"}
CW_FACE = {"UP": "RIGHT", "RIGHT": "DOWN", "DOWN": "LEFT", "LEFT": "UP"}
# where the part of a pond block that faced `role` ends up after one quarter turn clockwise
POND_CW = {"nw": "ne", "ne": "se", "se": "sw", "sw": "nw", "n": "e", "e": "s", "s": "w", "w": "n", "c": "c"}
# the rails, by number of quarter turns clockwise: a rail block that has no turned twin becomes a tree
RAILS = {1: {"fence_h": "fence_vl", "fence_v": "fence_h", "fence_vl": None},
         2: {"fence_h": None, "fence_v": "fence_vl", "fence_vl": "fence_v"},
         3: {"fence_h": "fence_v", "fence_v": None, "fence_vl": "fence_h"}}


def block_swap(kit, k):
    """{block id: block id} for the blocks that have a direction, for k quarter turns clockwise."""
    S = kit.extra["scn"]
    swap = {}
    for role in POND_CW:
        r = role
        for _ in range(k):
            r = POND_CW[r]
        swap[S["pond_" + role]] = S["pond_" + r]
    for role, to in RAILS.get(k, {}).items():
        if role in S:
            swap[S[role]] = S[to] if to else S["tree"]
    return swap


def turn_pt(x, y, w, h, k):
    """A point (block or cell) of a w by h grid after k quarter turns clockwise, and the new size."""
    for _ in range(k):
        x, y, w, h = h - 1 - y, x, h, w
    return x, y, w, h


def edge_turn(side, pos, cw, w, h, k):
    """(side, position) of a corridor of width cw that runs along `side` of a w by h block map from block `pos`, after k quarter turns."""
    if side in "NS":
        y = 0 if side == "N" else h - 1
        pts = [(pos, y), (pos + cw - 1, y)]
    else:
        x = 0 if side == "W" else w - 1
        pts = [(x, pos), (x, pos + cw - 1)]
    ww, hh = w, h
    for _ in range(k):
        pts = [(hh - 1 - y, x) for x, y in pts]
        ww, hh = hh, ww
        side = CW_SIDE[side]
    return side, (min(y for _, y in pts) if side in "EW" else min(x for x, _ in pts))


def arg_for(side, pos, cw, w, h, k, lo=1):
    """The corridor start `a` at the bottom edge of an unturned map such that after k quarter turns it sits at `pos` along its side."""
    best = None
    for a in range(lo, w - cw):
        s, p = edge_turn("S", a, cw, w, h, k)
        if s == side and (best is None or abs(p - pos) < abs(best[1] - pos)):
            best = (a, p)
    return best[0]


def cell_of(side, pos, cw, w, h):
    """The middle cell of the corridor on its edge, in cell coordinates."""
    c = 2 * pos + cw
    return {"S": (c, 2 * h - 1), "N": (c, 0), "W": (0, c), "E": (2 * w - 1, c)}[side]


def rotate(m, slots, kit, k, R=None):
    """Turns the finished map m k quarter turns clockwise in place, with the trainer slots of its lane."""
    k %= 4
    if k == 0:
        if kit.extra["style"] == "urban":
            autotile(m, kit, R or random.Random("turn:" + m.name))
        return
    swap = block_swap(kit, k)
    w, h, cw = m.w, m.h, m.cw
    nb = bytearray(m.w * m.h)
    for y in range(h):
        for x in range(w):
            nx, ny, nw, nh = turn_pt(x, y, w, h, k)
            b = m.get(x, y)
            nb[ny * nw + nx] = swap.get(b, b)
    side_in, pos_in = m.entry
    side_out, pos_out = m.exit
    m.entry = edge_turn(side_in, pos_in, cw, w, h, k)
    m.exit = edge_turn(side_out, pos_out, cw, w, h, k)
    m.blocks, m.w, m.h = nb, h if k % 2 else w, w if k % 2 else h

    def cell(x, y):
        nx, ny, _, _ = turn_pt(x, y, 2 * w, 2 * h, k)
        return nx, ny

    def face(s):
        for _ in range(k):
            s = CW_FACE[s]
        return s

    for o in m.objects:
        o["x"], o["y"] = cell(o["x"], o["y"])
        tail = o["move"].rsplit("_", 1)[-1]
        if o["move"].startswith("SPRITEMOVEDATA_STANDING_") and tail in CW_FACE:
            o["move"] = "SPRITEMOVEDATA_STANDING_" + face(tail)
    for wp in m.warps:
        wp.x, wp.y = cell(wp.x, wp.y)
    m.coords = [(*cell(x, y), sc, sn) for (x, y, sc, sn) in m.coords]
    m.bgs = [(*cell(x, y), f, s) for (x, y, f, s) in m.bgs]
    for s in slots:
        s.x, s.y = cell(s.x, s.y)
        s.face = face(s.face)
    for gd in getattr(m, "glades", []):
        gd["cells"] = [cell(x, y) for x, y in gd["cells"]]
        mx, my, _, _ = turn_pt(*gd["mouth"], w, h, k)
        gd["mouth"] = (mx, my)
    if kit.extra["style"] == "urban":
        autotile(m, kit, R or random.Random("turn:" + m.name))
    # the road must still lead from one side to the other, and every glade cell must still be reachable
    r = reach(m, kit, cell_of(*m.entry, cw, m.w, m.h))
    assert cell_of(*m.exit, cw, m.w, m.h) in r, (m.name, "the turned road is cut")
    for gd in getattr(m, "glades", []):
        gd["cells"] = [c for c in gd["cells"] if c in r]


def bend(g, name, kit, *, kind, a, r_t, landmark, music, cw=3, pal="PALETTE_DAY", W=12, H=14):
    """A bend in the frame of a vertical lane: entered at the bottom on columns a.., the corridor runs up to the block row r_t and then
    right (kind R, to the east edge) or left (kind L, to the west edge) on rows r_t..r_t+cw-1.  Returns the map, not yet turned."""
    S = kit.extra["scn"]
    style = kit.extra["style"]
    R = random.Random("bend:" + name)
    m = MapDef(g.key, name, W, H, kit.tileset, "ROUTE", landmark, music, border=kit.extra["border"], pal=pal)
    base = S["tree"] if style == "wild" else None
    for y in range(H):
        for x in range(W):
            m.set(x, y, base if base is not None else R.choice(kit.wall))
    carved = set()

    def floor(x, y):
        m.set(x, y, R.choice(kit.floor))
        carved.add((x, y))

    x_end = W - 1 if kind == "R" else 0
    lo, hi = [a] * H, [a + cw - 1] * H
    for y in range(r_t, H):
        for x in range(a, a + cw):
            floor(x, y)
    for y in range(r_t, r_t + cw):
        for x in range(min(a, x_end), max(a + cw - 1, x_end) + 1):
            floor(x, y)
        lo[y], hi[y] = (a, W - 1) if kind == "R" else (0, a + cw - 1)
    used = set(range(0, r_t + cw))
    spot = find_spot(lo, hi, W, H, used, R)
    glades = []
    if spot:
        side_, x0, x1, r0, r1, mr, lim = spot
        glades.append(glade(m, kit, S, R, spot))
        for yy in range(r0, r1 + 1):
            for xx in range(x0, x1 + 1):
                carved.add((xx, yy))
        carved.add(glades[-1]["mouth"])
    protect = {(x + dx, y + dy) for (x, y) in carved for dx in (-1, 0, 1) for dy in (-1, 0, 1)} | carved
    landscape(m, kit, S, R, base, protect)
    g.add(m)
    m.a, m.cw = a, cw
    m.glades = glades
    m.entry = ("S", a)
    m.exit = ("E" if kind == "R" else "W", r_t)
    r = reach(m, kit, cell_of(*m.entry, cw, W, H))
    assert cell_of(*m.exit, cw, W, H) in r, (name, "the bend is cut")
    for gd in glades:
        gd["cells"] = [c for c in gd["cells"] if c in r]
    return m


def edges_of(m):
    """(entry, exit) of a map: the turned ones carry them, the vertical ones (lanes, plazas) are entered at the bottom and left at the top."""
    if hasattr(m, "entry"):
        return m.entry, m.exit
    return ("S", m.a), ("N", m.a_out)


def join(lower, upper):
    """Connects the exit of lower to the entry of upper along the sides that face each other."""
    (_, _), (sl, pl) = edges_of(lower)
    (su, pu), (_, _) = edges_of(upper)
    assert OPP[sl] == su, (lower.name, sl, upper.name, su)
    off = pl - pu
    lower.connect(CONN[sl], upper, off)
    upper.connect(CONN[su], lower, -off)
