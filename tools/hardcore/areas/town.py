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

DECOR = ["park", "market", "garden", "terrace", "lake", "orchard", "cloister", "avenue", "maze"]  # the fountain square is placed on its own (build_plaza)


def plaza2(g, name, kit, rng, **kw):
    """Builds the town, trying new street and district layouts until every door, the exit and the grass can be walked to."""
    for attempt in range(40):
        m, doors = build_plaza(g, name, kit, random.Random(f"town:{name}:{attempt}"), **kw)
        if m.bad:
            continue
        e, xo, jr = m.street
        r = reach(m, kit, (2 * e + 1, 2 * (m.h - 2) + 1))
        ok = all(((wp.x, wp.y - 1) if wp.y == 2 * m.h - 1 else (wp.x, wp.y + 1)) in r for wp in m.warps) and (2 * xo + 1, 0) in r  # a mat is read from above
        ok = ok and all((2 * fx + dx, 2 * fy + 4) in r for fx, fy in getattr(m, "fountains", []) for dx in (1, 2))  # the plaque can be read
        if kit.extra.get("grass"):  # every town has tall grass (wild.py gives each plaza a table), and it can be walked to
            ok = ok and bool(getattr(m, "grass_cell", None)) and m.grass_cell[:2] in r
        if ok:
            m.npc_cells = [c for c in m.npc_cells if c in r]
            g.add(m)
            return m, doors
    raise AssertionError(f"{name}: no walkable layout found")


def border_cells(W, H):
    """The cells of the edge of a town in a walking order (top rows, then the two sides and the bottom row)."""
    out = [(x, y) for y in range(2) for x in range(W)]
    out += [(x, y) for y in range(2, H - 1) for x in (0, W - 1)]
    out += [(x, H - 1) for x in range(W)]
    return out


def path_between(start, goals, free, halo, R):
    """Cheapest walk over free blocks from `start` to any block of `goals` (steps cost 1, a turn 1.5, a block beside a building 2), as a list of
    blocks including both ends, or None.  Dijkstra over (block, heading)."""
    import heapq
    if start in goals:
        return [start]
    heap = [(0.0, 0, start, None, None)]
    best = {}
    tie = 0
    while heap:
        cost, _, cur, heading, prev = heapq.heappop(heap)
        if (cur, heading) in best:
            continue
        best[(cur, heading)] = prev
        if cur in goals:
            path, key = [], (cur, heading)
            while key:
                path.append(key[0])
                key = best[key]
            return path[::-1]
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx = (cur[0] + d[0], cur[1] + d[1])
            if nx not in free and nx not in goals:
                continue
            c = cost + 1 + (1.5 if heading is not None and heading != d else 0) + (1 if nx in halo else 0)
            tie += 1
            heapq.heappush(heap, (c, tie, nx, d, (cur, heading)))
    return None


def free_rects(free, minw=3, minh=3):
    """Greedy cover of a set of blocks by its largest all free rectangles of at least minw by minh: [(x0, x1, y0, y1)]."""
    free = set(free)
    out = []
    while free:
        best = None
        for (x0, y0) in sorted(free, key=lambda c: (c[1], c[0])):
            w_max = 0
            while (x0 + w_max, y0) in free:
                w_max += 1
            h, wmin = 0, w_max
            while wmin >= 1:
                row = 0
                while row < wmin and (x0 + row, y0 + h) in free:
                    row += 1
                if row < minw:
                    break
                wmin = row
                h += 1
                if h >= minh and (best is None or wmin * h > best[0]):
                    best = (wmin * h, x0, x0 + wmin - 1, y0, y0 + h - 1)
        if best is None:
            break
        _, x0, x1, y0, y1 = best
        out.append((x0, x1, y0, y1))
        free -= {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}
    return out


def build_plaza(g, name, kit, R, *, landmark, music, rift=False, houses=1, extra=0, south="open", pal="PALETTE_DAY",
                index=0, cw=3, width=None):
    """A town of buildings that stand apart (alpha 3.2, "like the maps of Sinnoh and Unova"): every building is a free standing block of two by two
    on open ground with at least one block of grass between it and the next, its own yard, a doormat of paving in front of the door and a path from
    there to the street.  Layout is in blocks (a block is two by two cells)."""
    S = kit.extra["scn"]
    style = kit.extra["style"]
    pc, mt, hs = kit.extra["center"], kit.extra["mart"], kit.extra["house"]
    nb = 2 + houses + extra + (1 if rift else 0)
    W = (width or (2 * nb + cw + 2 + R.choice((2, 4)))) + 4  # open ground between the buildings takes room
    H = R.choice((15, 16, 17))
    m = MapDef(g.key, name, W, H, kit.tileset, "TOWN", landmark, music, border=kit.extra["border"], pal=pal)
    m.bad = False
    plaza_t = kit.extra["plaza"]
    wild = style == "wild"
    for y in range(H):
        for x in range(W):
            m.set(x, y, S["tree"] if wild and y >= 2 else R.choice(kit.wall))
    if not wild:  # the edge of a city: runs of houses' backs and runs of trees, so no wall of fused facades closes the town in
        kind, left = "wall", R.randint(2, 4)
        for (x, y) in border_cells(W, H):
            m.set(x, y, R.choice(kit.wall) if kind == "wall" else S["tree"])
            left -= 1
            if left == 0:
                kind = "tree" if kind == "wall" else "wall"
                left = R.randint(1, 3) if kind == "tree" else R.randint(2, 4)

    def floor(x, y, paved=False, p=0.6):
        m.set(x, y, R.choice(plaza_t) if paved and R.random() < p else R.choice(kit.floor))

    for y in range(2, H - 1):
        for x in range(1, W - 1):
            floor(x, y)
    # the street: bottom stem at e, a two row band at row jr, top stem at xo
    e = R.randint(1, W - cw - 1)
    xo = R.randint(2, W - cw - 2)
    if abs(e - xo) < 4:
        xo = e + 5 if e + 5 <= W - cw - 2 else e - 5
        xo = max(2, min(W - cw - 2, xo))
    jr = R.randint(5, H - 8)
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
    reserved = set()  # blocks no building may stand on (the avenue of honour at the gate)
    # a tree on each side of the bottom stem at the entry row: the trigger row of the scenes at the foot of a plaza (the Crowley flight) spans the stem
    # and has to be unavoidable
    for x in (e - 1, e + cw):
        if 1 <= x <= W - 2:
            m.set(x, H - 2, S["tree"])
            reserved.add((x, H - 2))
    # the south edge: open at the bottom stem, or closed
    doors = {"houses": [], "extra": []}
    if south == "open":
        for x in range(e, e + cw):
            m.set(x, H - 1, R.choice(kit.floor))
    elif south == "gate":  # the way in from the gate hall: a doormat at the foot of the bottom stem, walls either side (builder.start_plaza)
        mx = e + cw // 2
        for x in range(e, e + cw):
            m.set(x, H - 1, S["mat"] if x == mx else R.choice(kit.wall))
        doors["south"] = m.warp(2 * mx, 2 * (H - 1) + 1)
        # the way in is an avenue of honour (alpha 3.2, "the entrance of the Commune needs glory"): the stem from the gate to the first bend is lined
        # by a column of trees and flower beds on both sides, so the first sight of an area is a procession
        for y in range(jr + 2, H - 1):
            for x in (e - 1, e + cw):
                if 1 <= x <= W - 2 and (x, y) not in street:
                    m.set(x, y, S["tree"] if (H - 2 - y) % 2 == 0 else R.choice(S["flowers"]))
                    reserved.add((x, y))
    # the buildings, one after the other: a spot with a free block all round it, a front block under the door that a path can reach
    kinds = ["center", "mart"] + ["house"] * houses + ["extra"] * extra + (["rift"] if rift else [])
    R.shuffle(kinds[2:])
    foot, halo, centers = set(), set(), []
    paved = set(street)
    paths = set()
    placed = []
    interior = lambda x, y: 1 <= x <= W - 2 and 2 <= y <= H - 2

    def valid(bx, by):
        if not (1 <= bx <= W - 3 and 2 <= by <= H - 5):
            return False
        cells = [(bx, by), (bx + 1, by), (bx, by + 1), (bx + 1, by + 1)]
        if any(c in street or c in halo or c in reserved or c in paths for c in cells):
            return False
        front = (bx, by + 2)
        return front not in foot and front not in cells and front not in reserved

    def weight(bx, by):
        front = (bx, by + 2)
        d = min(abs(front[0] - px) + abs(front[1] - py) for (px, py) in paved)
        w = (3, 3, 2.5, 2, 1, 0.5)[min(d, 5)] if d < 6 else 0.1
        if centers:
            dc = min(abs(bx - cx) + abs(by - cy) for (cx, cy) in centers)
            w *= 1.0 if dc >= 5 else 0.5 if dc >= 4 else 0.25
        if by in {c[1] for c in centers}:
            w *= 0.7
        return w

    for k in kinds:
        cand = [(bx, by) for by in range(2, H - 4) for bx in range(1, W - 2) if valid(bx, by)]
        R.shuffle(cand)
        done = False
        for _ in range(30):
            if not cand:
                break
            bx, by = R.choices(cand, [weight(bx, by) for bx, by in cand])[0]
            cand.remove((bx, by))
            front = (bx, by + 2)
            fp = {(bx, by), (bx + 1, by), (bx, by + 1), (bx + 1, by + 1)}
            hl = {(x + dx, y + dy) for (x, y) in fp for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
            free = {(x, y) for y in range(2, H - 1) for x in range(1, W - 1)
                    if (x, y) not in foot and (x, y) not in fp and (x, y) not in reserved and (x, y) not in street}
            path = path_between(front, paved, free, halo | hl, R)
            if path is None:
                continue
            foot |= fp
            halo |= hl
            paths |= set(path) - set(street)
            paved |= set(path)
            centers.append((bx, by))
            placed.append((bx, by, k, front))
            done = True
            break
        if not done:
            m.bad = True
            return m, doors
    spots = placed
    for bx, by, k, front in spots:
        if k == "center":
            for dy in range(2):
                for dx in range(2):
                    m.set(bx + dx, by + dy, pc[dy][dx])
            doors["center"] = m.warp(*kit.door_cell(bx, by + 1, pc[1][0]))
            m.spawn_cell = (doors["center"].x, doors["center"].y + 1)
        elif k == "mart":
            for dy in range(2):
                for dx in range(2):
                    m.set(bx + dx, by + dy, mt[dy][dx])
            doors["mart"] = m.warp(*kit.door_cell(bx, by + 1, mt[1][0]))
        else:
            m.set(bx, by + 1, hs[0])
            m.set(bx + 1, by + 1, hs[1])
            m.set(bx, by, kit.extra["house_roof"][0])
            m.set(bx + 1, by, kit.extra["house_roof"][1])
            wp = m.warp(*kit.door_cell(bx, by + 1, hs[0]))
            if k == "house":
                doors["houses"].append(wp)
            elif k == "extra":
                doors["extra"].append(wp)
            else:
                doors["rift"] = wp
    for (x, y) in paths:
        floor(x, y, paved=True, p=0.9)
    # the yards: flowers and a tree here and there on the ring of grass round every building, the front left clear
    front_zone = {(bx + dx, by + 2) for bx, by, _, _ in spots for dx in (-1, 0, 1, 2)}
    for (x, y) in sorted(halo - foot - paved - front_zone):
        if interior(x, y) and m.get(x, y) in kit.floor and R.random() < 0.45:
            m.set(x, y, S["tree"] if R.random() < 0.3 else R.choice(S["flowers"]))
    # districts in the open ground that is left: the biggest all free rectangles, one block back from every street and path
    near = {(x + dx, y + dy) for (x, y) in paved for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
    used = foot | halo | paved | near | reserved | front_zone
    free = {(x, y) for y in range(2, H - 1) for x in range(1, W - 1) if (x, y) not in used}
    zones = [("Z", x0, x1, y0, y1) for (x0, x1, y0, y1) in free_rects(free)]
    zones = split_zones(zones)
    zones.sort(key=lambda z: -((z[2] - z[1] + 1) * (z[4] - z[3] + 1)))
    grass_zone = zones[0] if zones else None
    gr = kit.extra.get("grass")
    if gr and (grass_zone is None or grass_zone[2] - grass_zone[1] < 3):
        m.bad = True
        return m, doors
    dk = DECOR[index % len(DECOR):] + DECOR[:index % len(DECOR)]
    R.shuffle(dk)
    dk = [DECOR[index % len(DECOR)]] + [k for k in dk if k != DECOR[index % len(DECOR)]]
    m.grass = 0
    m.fountains = []
    used_kinds = []
    # a fountain square in the biggest pocket of every third town (the first, the fourth, the seventh)
    fz = next((zi for zi, z in enumerate(zones) if z is not grass_zone and z[2] - z[1] >= 2 and z[4] - z[3] >= 2), None) if index % 3 == 1 else None
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
        kind = "fountain" if zi == fz else dk[zi % len(dk)]
        decorate(m, kit, S, R, kind, x0, x1, y0, y1)
        used_kinds.append(kind)
    # open ground that no district took: flowers and now and then a tree
    taken_z = {(x, y) for z in zones for y in range(z[3], z[4] + 1) for x in range(z[1], z[2] + 1)}
    for (x, y) in sorted(free - taken_z):
        if R.random() < 0.3:
            m.set(x, y, S["tree"] if R.random() < 0.25 else R.choice(S["flowers"]))
    # the town's edge: street trees along the south and the two sides where nothing else stands
    blocked = taken_z | used
    for y in range(3, H - 1):
        for x in (1, W - 2):
            if (x, y) not in blocked and (x, y + 1) not in paved and (x, y - 1) not in paved and R.random() < 0.45 and m.get(x, y) in kit.floor:
                m.set(x, y, S["tree"])
    for x in range(1, W - 1):
        if (x, H - 2) not in blocked and (x, H - 1) not in paved and R.random() < 0.35 and m.get(x, H - 2) in kit.floor \
                and not any((xx, H - 2) in paved for xx in (x - 1, x, x + 1)):
            m.set(x, H - 2, S["tree"])
    m.districts = used_kinds
    autotile(m, kit, R)
    for i, (fx, fy) in enumerate(m.fountains):  # the plaque on the basin, read from the south
        tag = next(t for t in ("Tithe", "Grove", "Axiom", "Lotus", "Dis") if name.startswith(t))
        sign(m, 2 * fx + 2, 2 * fy + 3, f"{name}Fountain{i}", R.choice(FOUNTAIN[tag]))
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
    if kind == "fountain":  # a pool of two by two blocks with a jet at the centre, paved all round, trees in the corners of the pocket
        px0, py0 = x0 + (w - 2) // 2, y0 + (h - 2) // 2
        for yy in range(py0 - 1, py0 + 3):
            for xx in range(px0 - 1, px0 + 3):
                if x0 <= xx <= x1 and y0 <= yy <= y1:
                    m.set(xx, yy, R.choice(paved))
        for (dx, dy, role) in ((0, 0, "fountain_nw"), (1, 0, "fountain_ne"), (0, 1, "fountain_sw"), (1, 1, "fountain_se")):
            m.set(px0 + dx, py0 + dy, S[role])
        m.fountains.append((px0, py0))
        for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            if not (px0 <= x <= px0 + 1 and py0 <= y <= py0 + 1) and R.random() < 0.8:
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
    elif kind == "orchard":  # trees on a grid with the paths between them, flowers in the gaps
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if (x - x0) % 2 == 0 and (y - y0) % 2 == 0:
                    m.set(x, y, S["tree"])
                elif R.random() < 0.3:
                    m.set(x, y, R.choice(flowers))
    elif kind == "cloister":  # a rail round a square of flower beds, trees at the corners, one gap on the south side
        for x in range(x0, x1 + 1):
            m.set(x, y0, S["fence_h"])
            m.set(x, y1, S["fence_h"])
        for y in range(y0 + 1, y1):
            m.set(x0, y, S["fence_v"])
            m.set(x1, y, S["fence_v"])
        for y in range(y0 + 1, y1):
            for x in range(x0 + 1, x1):
                m.set(x, y, R.choice(flowers) if R.random() < 0.6 else R.choice(kit.floor))
        gx = x0 + (x1 - x0) // 2
        m.set(gx, y1, R.choice(kit.floor))
        if y1 - y0 >= 2:
            m.set(gx, y1 - 1, R.choice(kit.floor))
        for (x, y) in ((x0, y0), (x1, y0)):
            m.set(x, y, S["tree"])
    elif kind == "avenue":  # a paved promenade across the pocket between two rows of trees
        for x in range(x0, x1 + 1):
            m.set(x, cy, R.choice(paved))
            for yy in (cy - 1, cy + 1):
                if y0 <= yy <= y1:
                    m.set(x, yy, S["tree"] if (x - x0) % 2 == 0 else R.choice(flowers))
        m.set(x0, cy, R.choice(paved))
    elif kind == "maze":  # a hedge maze of trees, rooms on the odd cells, passages carved by a depth first walk
        if w < 5 or h < 5:
            return decorate(m, kit, S, R, "orchard", x0, x1, y0, y1)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                m.set(x, y, S["tree"])
        rooms = [(x, y) for y in range(y0 + 1, y1, 2) for x in range(x0 + 1, x1, 2)]
        seen = {rooms[0]}
        todo = [rooms[0]]
        m.set(*rooms[0], R.choice(kit.floor))
        while todo:
            cx_, cy_ = todo[-1]
            nxt = [(cx_ + dx, cy_ + dy) for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)) if (cx_ + dx, cy_ + dy) in rooms and (cx_ + dx, cy_ + dy) not in seen]
            if not nxt:
                todo.pop()
                continue
            nx_, ny_ = R.choice(nxt)
            m.set((cx_ + nx_) // 2, (cy_ + ny_) // 2, R.choice(kit.floor))
            m.set(nx_, ny_, R.choice(kit.floor))
            seen.add((nx_, ny_))
            todo.append((nx_, ny_))
        ry = max(y for _, y in rooms)  # the way in, on the south side of the pocket
        door = R.choice([x for x, y in rooms if y == ry])
        for y in range(ry + 1, y1 + 1):
            m.set(door, y, R.choice(kit.floor))
        for (x, y) in ((x0 + 1, y0 + 1), (x1 - 1, y1 - 1)):
            if (x, y) in seen and R.random() < 0.5:
                m.set(x, y, R.choice(flowers))
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
