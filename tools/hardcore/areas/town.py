"""Towns for the area tilesets: a plaza is a street layout, not a box.

Techniques taken from the towns of the Game Boy era (New Bark, Cherrygrove, Violet, Goldenrod, Saffron) and the route maps:
  * the main street is an S-bend: it enters at the bottom, runs up one side, jogs across the middle and leaves at the top on
    the other side, so nobody sees the whole town at once and the exit is not in line with the entrance.
  * a row of buildings along the north wall (Pokecenter, Mart, houses, the door of the next story beat), each town in its own order and
    spacing, with a street in front of the doors.
  * the pockets beside the street are districts with a landmark of their own: a fountain square, a park with a pond, a market,
    a walled garden, a terrace with a ledge, a lake, a thicket, and the tall grass the wild Pokemon live in.
  * trees or a building row close the town in, the way the town edges close it in the classics.

Contract with the rest of the generator (see layout.plaza, which this replaces for the area tilesets): returns (map, doors) with the
doors dict {center, mart, houses[], extra[], rift?}, sets m.a (street column at the bottom edge), m.a_out (at the top edge), m.cw, m.grass,
m.spawn_cell (the cell below the Pokecenter door) and m.npc_cells (free floor cells, in a seeded random order, for townsfolk and the
named characters of cameos.py).  Layout choices come from a random source seeded by the map name."""
import random

from .layout import autotile, reach
from .people import sign
from .wayfolk import FOUNTAIN
from .model import MapDef

DECOR = ["park", "market", "garden", "terrace", "lake"]  # the fountain square is placed on its own (build_plaza)


def plaza2(g, name, kit, rng, **kw):
    """Builds the town, trying new street and district layouts until every door, the exit and the grass can be walked to."""
    for attempt in range(40):
        m, doors = build_plaza(g, name, kit, random.Random(f"town:{name}:{attempt}"), **kw)
        e, xo, jr = m.street
        r = reach(m, kit, (2 * e + 1, 2 * (m.h - 2) + 1))
        ok = all((wp.x, wp.y + 1) in r for wp in m.warps) and (2 * xo + 1, 0) in r
        ok = ok and all((2 * fx + dx, 2 * fy + 3) in r for fx, fy in getattr(m, "fountains", []) for dx in (0, 1))  # the plaque can be read
        if kit.extra.get("grass"):  # every town has tall grass (wild.py gives each plaza a table), and it can be walked to
            ok = ok and bool(getattr(m, "grass_cell", None)) and m.grass_cell[:2] in r
        if ok:
            m.npc_cells = [c for c in m.npc_cells if c in r]
            g.add(m)
            return m, doors
    raise AssertionError(f"{name}: no walkable layout found")


def build_plaza(g, name, kit, R, *, landmark, music, rift=False, houses=1, extra=0, south="open", pal="PALETTE_DAY",
                index=0, cw=3, width=None):
    S = kit.extra["scn"]
    style = kit.extra["style"]
    pc, mt, hs = kit.extra["center"], kit.extra["mart"], kit.extra["house"]
    nb = 2 + houses + extra + (1 if rift else 0)
    W = width or (2 * nb + cw + 2 + R.choice((2, 4)))
    H = R.choice((13, 14, 15))
    m = MapDef(g.key, name, W, H, kit.tileset, "TOWN", landmark, music, border=kit.extra["border"], pal=pal)
    plaza_t = kit.extra["plaza"]
    wild = style == "wild"
    perim = (lambda: S["tree"]) if wild else (lambda: R.choice(kit.wall))
    for y in range(H):
        for x in range(W):
            m.set(x, y, R.choice(kit.wall) if y < 2 else perim())
    taken = set()  # blocks no decor may use: street, frontage, buildings

    def floor(x, y, paved=False):
        m.set(x, y, R.choice(plaza_t) if paved and R.random() < 0.6 else R.choice(kit.floor))

    for y in range(2, H - 1):
        for x in range(1, W - 1):
            floor(x, y)
    # the street: bottom stem at e, a two row band at row jr, top stem at xo
    e = R.randint(1, W - cw - 1)
    xo = R.randint(2, W - cw - 2)
    if abs(e - xo) < 3:
        xo = e + 4 if e + 4 <= W - cw - 2 else e - 4
        xo = max(2, min(W - cw - 2, xo))
    jr = R.randint(5, H - 7)
    street = set()
    for y in range(jr + 2, H - 1):
        for x in range(e, e + cw):
            street.add((x, y))
    for y in range(jr, jr + 2):
        for x in range(min(e, xo), max(e, xo) + cw):
            street.add((x, y))
    for y in range(0, jr):
        for x in range(xo, xo + cw):
            street.add((x, y))
    for (x, y) in street:
        floor(x, y, paved=True)
    taken |= street
    for x in range(1, W - 1):  # the frontage street in front of the doors
        taken.add((x, 2))
    # buildings along the north wall, around the gap of the top stem
    blds = ["center", "mart"] + ["house"] * houses + ["extra"] * extra + (["rift"] if rift else [])
    R.shuffle(blds)
    left_w, right_w = xo - 1, W - 1 - (xo + cw)
    cap_l, cap_r = left_w // 2, right_w // 2
    assert cap_l + cap_r >= len(blds), (name, W, xo, len(blds))
    n_l = min(cap_l, R.randint(max(0, len(blds) - cap_r), len(blds)))
    segs = [(1, left_w, blds[:n_l]), (xo + cw, right_w, blds[n_l:])]
    doors = {"houses": [], "extra": []}
    spots = []
    for x0, wd, lst in segs:
        spare = wd - 2 * len(lst)
        x = x0
        for k in lst:
            gap = R.randint(0, spare) if spare else 0
            if R.random() < 0.5:
                gap = min(gap, 1)
            spare -= gap
            x += gap
            spots.append((x, k))
            x += 2
    for x, k in spots:
        for dy in range(2):
            for dx in range(2):
                taken.add((x + dx, dy))
        if k == "center":
            for dy in range(2):
                for dx in range(2):
                    m.set(x + dx, dy, pc[dy][dx])
            doors["center"] = m.warp(*kit.door_cell(x, 1, pc[1][0]))
            m.spawn_cell = (doors["center"].x, doors["center"].y + 1)
        elif k == "mart":
            for dy in range(2):
                for dx in range(2):
                    m.set(x + dx, dy, mt[dy][dx])
            doors["mart"] = m.warp(*kit.door_cell(x, 1, mt[1][0]))
        else:
            m.set(x, 1, hs[0])
            m.set(x + 1, 1, hs[1])
            if "house_roof" in kit.extra:
                m.set(x, 0, kit.extra["house_roof"][0])
                m.set(x + 1, 0, kit.extra["house_roof"][1])
            wp = m.warp(*kit.door_cell(x, 1, hs[0]))
            if k == "house":
                doors["houses"].append(wp)
            elif k == "extra":
                doors["extra"].append(wp)
            else:
                doors["rift"] = wp
    # the south edge: open at the bottom stem, or closed
    if south == "open":
        for x in range(e, e + cw):
            m.set(x, H - 1, R.choice(kit.floor))
    # districts: four pockets around the street
    zones = [("TL", 1, xo - 2, 3, jr - 1), ("TR", xo + cw + 1, W - 2, 3, jr - 1),
             ("BL", 1, e - 2, jr + 3, H - 2), ("BR", e + cw + 1, W - 2, jr + 3, H - 2)]
    zones = split_zones(zones)
    zones.sort(key=lambda z: -((z[2] - z[1] + 1) * (z[4] - z[3] + 1)))
    grass_zone = zones[0] if zones else None
    kinds = DECOR[index % len(DECOR):] + DECOR[:index % len(DECOR)]
    R.shuffle(kinds)
    kinds = [DECOR[index % len(DECOR)]] + [k for k in kinds if k != DECOR[index % len(DECOR)]]
    m.grass = 0
    m.fountains = []
    gr = kit.extra.get("grass")
    used_kinds = []
    # a fountain square in the biggest pocket of every third town (the first, the fourth, the seventh)
    fz = next((zi for zi, z in enumerate(zones) if z is not grass_zone), None) if index % 3 == 1 else None
    for zi, z in enumerate(zones):
        _, x0, x1, y0, y1 = z
        if z is grass_zone and gr:
            gw, gh = min(x1 - x0 + 1, 6), min(y1 - y0 + 1, 3)
            gx, gy = R.randint(x0, x1 - gw + 1), R.randint(y0, y1 - gh + 1)
            m.grass += grass_patch(m, kit, R, gx, gx + gw - 1, gy, gy + gh - 1, gr)
            m.grass_cell = (2 * gx + gw, 2 * gy + gh, max(1, min(3, gw - 1)))  # a cell in the middle of the patch, half width to shuffle
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    if not (gx <= x < gx + gw and gy <= y < gy + gh) and R.random() < 0.3:
                        m.set(x, y, R.choice(S["flowers"]))
            used_kinds.append("grass")
            continue
        kind = "fountain" if zi == fz else kinds[zi % len(kinds)]
        decorate(m, kit, S, R, kind, x0, x1, y0, y1)
        used_kinds.append(kind)
    # the frontage: trees and beds in the gaps between the buildings, never in front of a door
    door_x = {wp.x // 2 for wp in m.warps}
    for x in range(1, W - 1):
        if x in door_x or (x, 2) in street:
            continue
        if m.get(x, 1) in kit.wall and m.get(x, 2) in kit.floor:
            r = R.random()
            if r < 0.35:
                m.set(x, 2, S["tree"])
            elif r < 0.6:
                m.set(x, 2, R.choice(S["flowers"]))
    # the town's edge: street trees along the south and the two sides where nothing else stands
    blocked = {(x, y) for z in zones for y in range(z[3], z[4] + 1) for x in range(z[1], z[2] + 1)} | street
    for y in range(3, H - 1):
        for x in (1, W - 2):
            if (x, y) not in blocked and (x, y + 1) not in street and (x, y - 1) not in street and R.random() < 0.45 \
                    and m.get(x, y) in kit.floor:
                m.set(x, y, S["tree"])
    for x in range(1, W - 1):
        if (x, H - 2) not in blocked and (x, H - 1) not in street and R.random() < 0.35 and m.get(x, H - 2) in kit.floor \
                and not any((xx, H - 2) in street for xx in (x - 1, x, x + 1)):
            m.set(x, H - 2, S["tree"])
    m.districts = used_kinds
    autotile(m, kit, R)
    for i, (fx, fy) in enumerate(m.fountains):  # the plaque on the basin, read from the south
        tag = next(t for t in ("Tithe", "Grove", "Axiom", "Lotus", "Dis") if name.startswith(t))
        sign(m, 2 * fx + 1, 2 * fy + 1, f"{name}Fountain{i}", R.choice(FOUNTAIN[tag]))
    # townsfolk cells: floor cells away from doors, grass and the street's middle
    door_cells = {(wp.x, wp.y) for wp in m.warps}
    cells = []
    for y in range(6, 2 * H - 2):
        for x in range(2, 2 * W - 2):
            b = m.get(x // 2, y // 2)
            q = (x % 2) + 2 * (y % 2)
            if kit.coll[b][q] != "FLOOR" or b in (gr or []):
                continue
            if any(abs(x - dx) + abs(y - dy) < 3 for dx, dy in door_cells):
                continue
            if (x // 2, y // 2) in street and (e + 0 <= x // 2 < e + cw or xo <= x // 2 < xo + cw) and R.random() < 0.8:
                continue
            cells.append((x, y))
    R.shuffle(cells)
    m.npc_cells = cells
    m.a, m.a_out, m.cw = e, xo, cw
    m.street = (e, xo, jr)
    return m, doors


def split_zones(zones):
    """Cut pockets that are too big for one district into two with a block of street between them; drop the tiny ones."""
    out, todo = [], list(zones)
    while todo:
        n, x0, x1, y0, y1 = todo.pop()
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if w >= 3 and h >= 3:
            if w > 6:
                mid = x0 + w // 2
                todo += [(n, x0, mid - 1, y0, y1), (n, mid + 1, x1, y0, y1)]
            elif h > 4:
                mid = y0 + h // 2
                todo += [(n, x0, x1, y0, mid - 1), (n, x0, x1, mid + 1, y1)]
            else:
                out.append((n, x0, x1, y0, y1))
    return out


def grass_patch(m, kit, R, x0, x1, y0, y1, gr):
    """Tall grass over a zone but for a floor edge row on the street side: the wild Pokemon of the town."""
    dense, detail = gr[0], gr[1]
    n = 0
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            corner = x in (x0, x1) and y in (y0, y1)
            if corner and R.random() < 0.6:
                continue
            m.set(x, y, detail if R.random() < 0.08 else dense)
            n += 1
    return n


def pond_rect(m, S, x0, y0, w, h):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            top, bot, lef, rig = y == y0, y == y0 + h - 1, x == x0, x == x0 + w - 1
            role = ("pond_nw" if lef else "pond_ne" if rig else "pond_n") if top else \
                   ("pond_sw" if lef else "pond_se" if rig else "pond_s") if bot else \
                   ("pond_w" if lef else "pond_e" if rig else "pond_c")
            m.set(x, y, S[role])


def decorate(m, kit, S, R, kind, x0, x1, y0, y1):
    w, h = x1 - x0 + 1, y1 - y0 + 1
    flowers = S["flowers"]
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    paved = kit.extra["plaza"]
    if kind == "fountain":  # the round basin on a block of its own, paved all round, trees in the corners of the pocket
        for yy in range(cy - 1, cy + 2):
            for xx in range(cx - 1, cx + 2):
                if x0 <= xx <= x1 and y0 <= yy <= y1:
                    m.set(xx, yy, R.choice(paved))
        m.set(cx, cy, S["fountain"])
        m.fountains.append((cx, cy))
        for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            if (x, y) != (cx, cy) and R.random() < 0.8:
                m.set(x, y, S["tree"])
    elif kind == "park":
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                edge = x in (x0, x1) or y in (y0, y1)
                if edge and R.random() < 0.7:
                    m.set(x, y, S["tree"])
                elif R.random() < 0.4:
                    m.set(x, y, R.choice(flowers))
        if w >= 5 and h >= 4:
            pond_rect(m, S, cx - 1, cy - (1 if h >= 5 else 0), 2, 2)
        # keep one entrance on the street side open
        m.set(x0 if R.random() < 0.5 else x1, y0 + (y1 - y0) // 2, R.choice(kit.floor))
    elif kind == "market":
        for y in range(y0, y1 + 1, 2):
            for x in range(x0, x1 + 1):
                if (x - x0) % 3 != 2:
                    m.set(x, y, S["fence_h"])
        for y in range(y0 + 1, y1 + 1, 2):
            for x in range(x0, x1 + 1):
                if R.random() < 0.25:
                    m.set(x, y, R.choice(flowers))
    elif kind == "garden":
        for x in range(x0, x1 + 1):
            m.set(x, y0, S["fence_h"])
        for y in range(y0 + 1, y1 + 1):
            for x in range(x0, x1 + 1):
                m.set(x, y, R.choice(flowers) if R.random() < 0.7 else R.choice(kit.floor))
    elif kind == "terrace":
        for x in range(x0, x1 + 1):
            m.set(x, y0 + 1, S["ledge"])
        for y in range(y0 + 2, y1 + 1):
            for x in range(x0, x1 + 1):
                m.set(x, y, R.choice(flowers) if R.random() < 0.5 else R.choice(kit.floor))
        m.set(x0 + (x1 - x0) // 2, y0 + 1, R.choice(kit.floor))  # a gap: the stairs
        for (x, y) in ((x0, y0), (x1, y0)):
            m.set(x, y, S["tree"])
    else:  # lake
        pond_rect(m, S, x0 + 1, y0 + 1, max(2, w - 2), max(2, h - 2))
        for x in range(x0, x1 + 1):
            if R.random() < 0.5:
                m.set(x, y0, S["tree"])
