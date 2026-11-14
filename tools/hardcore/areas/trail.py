"""Winding trails: the forced-fight corridor of a lane drawn like an old-school route instead of a straight pipe.

Techniques taken from the Game Boy era route maps (Routes 29, 30, 31, 32, 38 of Crystal, the Viridian Forest and Mt. Moon mazes):
  * S-bends: the corridor drifts one block sideways per row for a few rows, then runs straight (a stagger, never a long diagonal).
  * wide/narrow rhythm: three blocks of corridor while the trainers watch it, a breather clearing near the exit where nobody does.
  * the walls are a landscape, not a box: a dense tree line or building row along the corridor with lakes, groves, gardens and
    meadows set into it, each reached through a one block mouth and a dead end, so a detour never skips a fight.
  * what a glade holds is the reward for leaving the road: the lane's item ball, a hidden item, a hermit who talks.
  * every glade is different (pond, orchard, garden, meadow) and sits on a different side and height in every lane.

Contract with the rest of the generator (see layout.lane, which this replaces for the area tilesets): the corridor is `cw` blocks wide in
every row, trainers stand on its edge cells so their sight line crosses all of it, the bottom `neck` rows are a one block neck with the item
gate, and the map records m.a (corridor column at the bottom edge), m.a_out (at the top edge) and m.cw for chain().  Layout choices come from
a random source of their own (seeded by the map name), so the parties and flags of the rest of the world stay where they were."""
import random

from . import counts
from .layout import Slot, autotile, gate_objects, reach
from .model import MapDef

ROW0 = 5  # first block row (from the top) of trainers; rows above it are the breather
KINDS_WILD = ["pond", "orchard", "meadow", "garden"]
KINDS_URBAN = ["garden", "pond", "orchard", "meadow"]


def walk(R, H, W, cw, a):
    """Corridor column of every block row (0 = top): straight stub at the bottom, a few bends, straight stub at the top."""
    lo, hi = 1, W - cw - 1
    a = max(lo, min(hi, a))
    c = [a] * H
    pos, r = a, H - 4
    while r >= 2:
        if R.random() < 0.3:
            dc = 0
        else:
            left, right = pos - lo, hi - pos
            dc = -1 if (left > right) != (R.random() < 0.25) else 1
            if (dc < 0 and left == 0) or (dc > 0 and right == 0):
                dc = -dc
        for _ in range(R.randint(2, 4)):
            if r < 2:
                break
            pos = max(lo, min(hi, pos + dc))
            c[r] = pos
            r -= 1
    c[0] = c[1] = c[2]
    return c


def find_spot(lo, hi, W, H, used, R):
    """A rectangle of blocks beside the corridor for a glade: (side, x0, x1, r0, r1, mouth row, lim) or None.
    lo/hi: first and last corridor block of every row."""
    best = None
    for _ in range(40):
        h = R.choice((3, 4, 5, 5))
        r0 = R.randint(4, H - 3 - h + 1)
        r1 = r0 + h - 1
        if any(r in used for r in range(r0 - 1, r1 + 2)):
            continue
        for side in ("L", "R"):
            if side == "L":
                lim = min(lo[r] for r in range(r0, r1 + 1))
                width = lim - 2
                x0, x1 = 1, lim - 2
                edge = lambda r: lo[r] == lim
            else:
                lim = max(hi[r] + 1 for r in range(r0, r1 + 1))
                width = W - 2 - lim
                x0, x1 = lim + 1, W - 2
                edge = lambda r: hi[r] + 1 == lim
            if width < 3:
                continue
            gw = min(width, 6)
            if side == "L":
                x0 = x1 - gw + 1
            else:
                x1 = x0 + gw - 1
            score = gw * h + R.random()
            mouths = [r for r in range(r0, r1 + 1) if edge(r)]
            if mouths and (best is None or score > best[0]):
                best = (score, side, x0, x1, r0, r1, R.choice(mouths), lim)
    return best[1:] if best else None


def put(m, x, y, b):
    if 0 <= x < m.w and 0 <= y < m.h:
        m.set(x, y, b)


def glade(m, kit, S, R, spot):
    """Carve and dress one glade. Returns its floor cells (cell coordinates) for the item, the hermit and the hidden item."""
    side, x0, x1, r0, r1, mr, lim = spot
    ground = kit.extra.get("ground", kit.floor)  # what a glade or a clearing is floored with (the road kit: grass, not the path)
    floor = set(kit.floor) | set(ground)
    gw, gh = x1 - x0 + 1, r1 - r0 + 1
    for y in range(r0, r1 + 1):
        for x in range(x0, x1 + 1):
            m.set(x, y, R.choice(ground))
    mx = lim - 1 if side == "L" else lim
    m.set(mx, mr, R.choice(ground))
    flowers = S["flowers"]
    kinds = list(KINDS_WILD if kit.extra["style"] == "wild" else KINDS_URBAN)
    if gw < 4 or gh < 4:
        kinds = [k for k in kinds if k != "pond"]
    kind = R.choice(kinds)
    # blocks that stay open for the walk: the mouth and the block beside it
    keep = {(x1 if side == "L" else x0, mr)}
    if kind == "pond":  # the pond fills the glade but for a one block ring of shore, which carries the path from the mouth
        px0, px1, py0, py1 = x0 + 1, x1 - 1, r0 + 1, r1 - 1
        for yy in range(py0, py1 + 1):
            for xx in range(px0, px1 + 1):
                top, bot = yy == py0, yy == py1
                lef, rig = xx == px0, xx == px1
                role = ("pond_nw" if lef else "pond_ne" if rig else "pond_n") if top else \
                       ("pond_sw" if lef else "pond_se" if rig else "pond_s") if bot else \
                       ("pond_w" if lef else "pond_e" if rig else "pond_c")
                m.set(xx, yy, S[role])
    elif kind == "orchard":
        for yy in range(r0, r1 + 1):
            for xx in range(x0, x1 + 1):
                if (xx - x0) % 2 == 1 and (yy - r0) % 2 == 1 and (xx, yy) not in keep:
                    m.set(xx, yy, S["tree"])
    elif kind == "garden":
        for xx in range(x0, x1 + 1):  # a rail across the top row of the glade, beds below
            if (xx, r0) not in keep:
                m.set(xx, r0, S.get("fence_h", S["pool"]))  # a rail, or a row of boulders where the tileset has no rail
        for yy in range(r0 + 1, r1 + 1):
            for xx in range(x0, x1 + 1):
                if (xx, yy) not in keep and R.random() < 0.55:
                    m.set(xx, yy, R.choice(flowers))
    else:  # meadow
        for yy in range(r0, r1 + 1):
            for xx in range(x0, x1 + 1):
                if (xx, yy) not in keep and R.random() < 0.4:
                    m.set(xx, yy, R.choice(flowers))
        for cx, cy in ((x0, r0), (x1, r1)):
            if (cx, cy) not in keep and R.random() < 0.7:
                m.set(cx, cy, S["tree"])
    cells = []
    for yy in range(r0, r1 + 1):
        for xx in range(x0, x1 + 1):
            b = m.get(xx, yy)
            if b in floor or b in flowers:
                for dx in (0, 1):
                    for dy in (0, 1):
                        cells.append((2 * xx + dx, 2 * yy + dy))
    mouth_cells = {(2 * mx + dx, 2 * mr + dy) for dx in (0, 1) for dy in (0, 1)}
    cells = [cl for cl in cells if cl not in mouth_cells and abs(cl[0] - (2 * mx + 1)) + abs(cl[1] - (2 * mr + 1)) > 2]
    return dict(kind=kind, cells=cells, mouth=(mx, mr), side=side, rows=(r0, r1))


def landscape(m, kit, S, R, base, protect):
    """Lakes, clearings and groves behind the tree line / building row, never reachable: each sits on blocks that are all plain
    base fill and keep one block of base fill between them and any block of the corridor or a glade (`protect`)."""
    style = kit.extra["style"]
    flowers = S["flowers"]
    ground = kit.extra.get("ground", kit.floor)
    base_set = {base} if base is not None else set(kit.wall)
    made = 0
    # open ground and a thinner forest / more courtyards between the features: the margins are not a solid wall
    for y in range(m.h):
        for x in range(m.w):
            if (x, y) in protect:
                continue
            r = R.random()
            if style == "wild":
                if r > 0.58:
                    m.set(x, y, R.choice(ground) if r < 0.85 else R.choice(flowers))
            elif r > 0.82:
                m.set(x, y, R.choice(ground) if r < 0.92 else S["tree"] if r < 0.97 else R.choice(flowers))
    for _ in range(80):
        if made >= 7:
            break
        kind = R.choice(("lake", "lake", "clearing", "clearing", "grove"))
        w_, h_ = R.randint(2, 4), R.randint(2, 4)
        if kind == "lake" and (w_ < 2 or h_ < 2):
            continue
        x0, y0 = R.randint(0, m.w - w_), R.randint(0, m.h - h_)
        if any((x, y) in protect for x in range(x0 - 1, x0 + w_ + 1) for y in range(y0 - 1, y0 + h_ + 1)):
            continue
        if any(m.get(x, y) not in base_set for x in range(x0, x0 + w_) for y in range(y0, y0 + h_)):
            continue
        for y in range(y0, y0 + h_):
            for x in range(x0, x0 + w_):
                if kind == "lake":
                    top, bot, lef, rig = y == y0, y == y0 + h_ - 1, x == x0, x == x0 + w_ - 1
                    role = ("pond_nw" if lef else "pond_ne" if rig else "pond_n") if top else \
                           ("pond_sw" if lef else "pond_se" if rig else "pond_s") if bot else \
                           ("pond_w" if lef else "pond_e" if rig else "pond_c")
                    m.set(x, y, S[role])
                elif kind == "clearing":
                    m.set(x, y, R.choice(flowers) if R.random() < 0.5 else R.choice(ground))
                else:  # grove: a checker of trees on open ground (urban: a pocket park)
                    m.set(x, y, S["tree"] if (x + y) % 2 == 0 else R.choice(ground))
        made += 1


def trail(g, name, kit, rng, *, trainers, a, landmark, music, cw=3, gate=None, neck=0, w=None, pal="PALETTE_DAY", W=12, north="open"):
    S = kit.extra["scn"]
    style = kit.extra["style"]
    rows = trainers - trainers // 3
    pairs = trainers - rows
    gap = counts.GAP  # block rows between two trainer rows: fewer fighters, the same long lane
    H = rows * gap + 7
    R = random.Random("trail:" + name)
    m = MapDef(g.key, name, W, H, kit.tileset, "ROUTE", landmark, music, border=kit.extra["border"], pal=pal)
    base = S["tree"] if style == "wild" else None
    wall_pick = (lambda: base) if base is not None else (lambda: R.choice(kit.wall))
    for y in range(H):
        for x in range(W):
            m.set(x, y, wall_pick())
    c = walk(R, H, W, cw, a)
    lo, hi = list(c), [x + cw - 1 for x in c]
    # the clearing before the exit: two rows one block wider on each side, with an island of its own in the middle
    island = None
    if H >= 12:
        for r in (2, 3):
            lo[r], hi[r] = max(1, lo[r] - 1), min(W - 2, hi[r] + 1)
        mid = (lo[2] + hi[2]) // 2
        island = (mid, 2 + R.randint(0, 1))
    carved = set()
    for y in range(H):
        for x in range(lo[y], hi[y] + 1):
            if y >= H - neck and x != c[y] + cw // 2:
                continue
            m.set(x, y, R.choice(kit.floor))
            carved.add((x, y))
    if island:
        ix, iy = island
        m.set(ix, iy, R.choice((S["tree"], S["pool"], S["pool"], R.choice(S["flowers"]))))
    if gate:
        assert neck >= 2, "a gate needs a neck"
        gate_objects(m, gate, w, 2 * (c[H - neck] + cw // 2), 2 * (H - neck))
    door = None
    fixed = set()  # blocks of the gate house: landscape() must leave them alone
    if north == "door":  # the road ends at a classic gate house: brown plank roof over a pink front with the door (Route 35), two blocks wide
        dx = c[0] + cw // 2
        roof, front = kit.extra["gate_roof"], kit.extra["gate_front"]
        for y in (0, 1):
            for x in range(lo[y], hi[y] + 1):
                m.set(x, y, base)
                carved.discard((x, y))
        for k in range(2):
            m.set(dx + k, 0, roof[k])
            m.set(dx + k, 1, front[k])
        door = m.warp(*kit.door_cell(dx, 1, front[0]))
        m.set(dx, 2, R.choice(kit.floor))
        carved.add((dx, 2))
        fixed = {(dx, 0), (dx + 1, 0), (dx, 1), (dx + 1, 1)}
    # trainers: one block row each (a pair on some), on the cells at the two edges of that row of the corridor
    ys = [H - 3 - i * gap for i in range(rows)]
    assert ys[-1] >= ROW0, (name, ys)
    pair_rows = set(R.sample(range(rows), pairs))
    slots, side = [], 0
    for i, r in enumerate(ys):
        cx0, cx1 = 2 * c[r], 2 * (c[r] + cw) - 1
        y = 2 * r
        if i in pair_rows:
            slots.append(Slot(cx0, y, "RIGHT", cx1 - cx0))
            slots.append(Slot(cx1, y, "LEFT", cx1 - cx0))
        else:
            slots.append(Slot(cx0 if side == 0 else cx1, y, "RIGHT" if side == 0 else "LEFT", cx1 - cx0))
            side ^= 1
    # glades beside the corridor
    used, glades = set(), []
    for _ in range(3):
        spot = find_spot(lo, hi, W, H, used, R)
        if not spot:
            break
        side_, x0, x1, r0, r1, mr, lim = spot
        glades.append(glade(m, kit, S, R, spot))
        used.update(range(r0 - 1, r1 + 2))
        for yy in range(r0, r1 + 1):
            for xx in range(x0, x1 + 1):
                carved.add((xx, yy))
        carved.add(glades[-1]["mouth"])
    protect = {(x + dx, y + dy) for (x, y) in carved for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    protect |= carved | fixed
    landscape(m, kit, S, R, base, protect)
    # rails along the corridor's long edges instead of tree line (wild areas)
    if base is not None and "fence_v" in S:
        for (x, y) in sorted(carved):
            if (x, y) in {(gd["mouth"]) for gd in glades}:
                continue
            for dx, role in ((-1, "fence_v"), (1, "fence_vl")):
                nx = x + dx
                if (nx, y) in carved or not (1 <= nx < W - 1) or m.get(nx, y) != base:
                    continue
                if (nx, y - 1) in carved or (nx, y + 1) in carved or R.random() > 0.3:
                    continue
                if m.get(nx + dx, y) == base:
                    m.set(nx, y, S[role])
    if style == "urban":
        autotile(m, kit, R)
    r = reach(m, kit, (2 * c[H - 1] + 1, 2 * H - 1))
    assert ((door.x, door.y + 1) if door else (2 * c[0] + 1, 0)) in r, (name, "exit not reachable")
    for gd in glades:
        gd["cells"] = [cl for cl in gd["cells"] if cl in r]
    g.add(m)
    m.a, m.a_out, m.cw = c[H - 1], c[0], cw
    m.glades = glades
    m.door = door
    m.corridor = c
    return m, slots
