"""Static model of the generated area maps, parsed from the emitted files (not from generator state).

Used by test_walk.py to plan routes. Everything here is read from the same assembly and .blk files
that the build uses, so a mismatch between this model and the emulator points at a real bug.
"""
import os
import re
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
DOORISH = {0x71, 0x75, 0x79, 0x7d, 0x7a, 0x7b, 0x73, 0x74}  # arrival here steps the player down
WARPTILE = set(range(0x70, 0x80)) - {0x7c}
CARPET = {0x70: "down", 0x76: "left", 0x78: "up", 0x7e: "right"}  # directional warp carpets
WALKABLE = {0x00, 0x10, 0x14, 0x18, 0x48, 0x49, 0x4c}  # floor and grass


def camel_to_const(name):
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", s)
    return s.upper()


def rd(path):
    return open(os.path.join(ROOT, path)).read()


def collision_names():
    d = {}
    for l in rd("constants/collision_constants.asm").splitlines():
        m = re.match(r"DEF COLL_(\w+)\s+EQU \$([0-9a-f]+)", l)
        if m:
            d.setdefault(m[1], int(m[2], 16))
    # the tilecoll macro uses these short names; aliases for the ones with suffix-free names
    return d


_COLL = {}


def tileset_collision(stem):
    if stem in _COLL:
        return _COLL[stem]
    names = collision_names()
    out = []
    for l in rd(f"data/tilesets/{stem}_collision.asm").splitlines():
        m = re.match(r"\s*tilecoll\s+(.*?)\s*;", l)
        if not m:
            continue
        row = []
        for v in [x.strip() for x in m[1].split(",")]:
            if re.fullmatch(r"[0-9a-fA-F]{2}", v) and v not in names:
                row.append(int(v, 16))
            else:
                row.append(names.get(v, 0x07))
        out.append(row)
    _COLL[stem] = out
    return out


class Map:
    def __init__(self, name, tileset, w, blk_path, asm_path):
        self.name, self.const = name, camel_to_const(name)
        self.tileset, self.w = tileset, w
        self.blocks = open(os.path.join(ROOT, blk_path), "rb").read()
        self.h = len(self.blocks) // w
        self.coll = tileset_collision(tileset.lower().replace("tileset_", ""))
        self.warps, self.objects, self.conns = [], [], {}
        s = rd(asm_path)
        for m in re.finditer(r"^\s*warp_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(\d+)", s, re.M):
            self.warps.append((int(m[1]), int(m[2]), m[3], int(m[4])))
        for m in re.finditer(r"^\s*object_event\s+(\d+),\s*(\d+),\s*(\w+),\s*(\w+),.*?,\s*(OBJECTTYPE_\w+),\s*(\d+),\s*(\w+),\s*(-?\w+)", s, re.M):
            self.objects.append(dict(x=int(m[1]), y=int(m[2]), sprite=m[3], move=m[4], otype=m[5], sight=int(m[6]),
                                     script=m[7], flag=m[8]))

    def cell(self, x, y):
        """Collision byte of the 16x16 cell, or None outside the map."""
        if not (0 <= x < 2 * self.w and 0 <= y < 2 * self.h):
            return None
        b = self.blocks[(y // 2) * self.w + x // 2]
        return self.coll[b][(y % 2) * 2 + (x % 2)]


def load():
    maps = {}
    dims = {}
    for l in rd("constants/area_map_constants.asm").splitlines():
        m = re.match(r"\s*map_const (\w+),\s*(\d+),\s*(\d+)", l)
        if m:
            dims[m[1]] = (int(m[2]), int(m[3]))
    tsets = {}
    for l in rd("data/maps/area_map_lists.asm").splitlines():
        m = re.match(r"\s*map (\w+), (TILESET_\w+),", l)
        if m:
            tsets[m[1]] = m[2]
    for name, ts in tsets.items():
        c = camel_to_const(name)
        mp = Map(name, ts, dims[c][0], f"maps/gen/{name}.blk", f"maps/gen/{name}.asm")
        maps[name] = mp
    # connections of generated maps
    cur = None
    for l in rd("data/maps/area_data.asm").splitlines():
        m = re.match(r"\s*map_attributes (\w+),", l)
        if m:
            cur = m[1]
        m = re.match(r"\s*connection (\w+), (\w+), (\w+), (-?\d+)", l)
        if m and cur:
            maps[cur].conns[m[1]] = (m[2], int(m[4]))
    # Cherrygrove (vanilla) with its north connection
    cg = Map("CherrygroveCity", "TILESET_JOHTO", 20, "maps/CherrygroveCity.blk", "maps/CherrygroveCity.asm")
    maps["CherrygroveCity"] = cg
    cg.conns["north"] = ("TitheRoad", 5)
    return maps


def by_const(maps):
    return {m.const: m for m in maps.values()}


class World:
    def __init__(self):
        self.maps = load()
        self.consts = by_const(self.maps)
        self.blocked = set()  # (map, x, y) discovered blocked in the emulator

    def solid_objects(self, mp):
        s = set()
        for o in mp.objects:
            s.add((o["x"], o["y"]))
        return s

    def step(self, st, d, ignore_obj=False):
        """Next state when stepping in direction d from state st, or None if blocked.
        Returns (state, kind) with kind 'move', 'warp' or 'conn'."""
        name, x, y = st
        mp = self.maps[name]
        dx, dy = DIRS[d]
        nx, ny = x + dx, y + dy
        here = mp.cell(x, y)
        if here in CARPET and CARPET[here] == d:
            # standing on a warp carpet and walking in its direction warps (the Pokecenter door mat)
            for (wx, wy, dest, dw) in mp.warps:
                if (wx, wy) == (x, y):
                    dm = self.consts.get(dest)
                    if dm is None:
                        return None
                    ddx, ddy = dm.warps[dw - 1][0], dm.warps[dw - 1][1]
                    if dm.cell(ddx, ddy) in DOORISH:
                        ddy += 1
                    return (dm.name, ddx, ddy), "warp"
        c = mp.cell(nx, ny)
        if c is None:
            # connection
            dn = {"up": "north", "down": "south", "left": "west", "right": "east"}[d]
            if dn not in mp.conns:
                return None
            other, off = mp.conns[dn]
            if other not in self.maps:
                return None
            om = self.maps[other]
            if dn in ("north", "south"):
                ox = nx - 2 * off
                oy = 2 * om.h - 1 if dn == "north" else 0
                if not (0 <= ox < 2 * om.w):
                    return None
            else:
                oy = ny - 2 * off
                ox = 2 * om.w - 1 if dn == "west" else 0
                if not (0 <= oy < 2 * om.h):
                    return None
            ns = (other, ox, oy)
            if ns in self.blocked or not self.walkable(om, ox, oy, ignore_obj):
                return None
            return ns, "conn"
        if (name, nx, ny) in self.blocked:
            return None
        if c in CARPET:
            # walking onto a carpet is just walking onto floor; the warp fires on the next step
            if not self.walkable(mp, nx, ny, ignore_obj):
                return None
            return (name, nx, ny), "move"
        if c in WARPTILE:
            for (wx, wy, dest, dw) in mp.warps:
                if (wx, wy) == (nx, ny):
                    dm = self.consts.get(dest)
                    if dm is None:  # a vanilla interior the model does not know
                        return None
                    ddx, ddy = dm.warps[dw - 1][0], dm.warps[dw - 1][1]
                    if dm.cell(ddx, ddy) in DOORISH:
                        ddy += 1
                    return (dm.name, ddx, ddy), "warp"
            return None
        if not self.walkable(mp, nx, ny, ignore_obj):
            return None
        return (name, nx, ny), "move"

    def walkable(self, mp, x, y, ignore_obj=False):
        c = mp.cell(x, y)
        if c not in WALKABLE and c not in WARPTILE:
            return False
        if not ignore_obj and (x, y) in self.solid_objects(mp):
            return False
        return True

    def route(self, start, goal_fn, ignore_obj=False):
        """BFS from start to the first state for which goal_fn(state) is true. Returns list of (dir, expected_state, kind)."""
        prev = {start: None}
        q = deque([start])
        while q:
            s = q.popleft()
            if goal_fn(s):
                path = []
                while prev[s]:
                    p, d, k = prev[s]
                    path.append((d, s, k))
                    s = p
                return path[::-1]
            for d in ("up", "right", "left", "down"):
                r = self.step(s, d, ignore_obj)
                if r and r[0] not in prev:
                    prev[r[0]] = (s, d, r[1])
                    q.append(r[0])
        return None

    def ascii(self, name):
        mp = self.maps[name]
        objs = {(o["x"], o["y"]): o for o in mp.objects}
        wps = {(w[0], w[1]) for w in mp.warps}
        rows = []
        for y in range(2 * mp.h):
            r = ""
            for x in range(2 * mp.w):
                c = mp.cell(x, y)
                if (x, y) in objs:
                    ch = "T" if objs[(x, y)]["otype"] == "OBJECTTYPE_TRAINER" else "N"
                elif (x, y) in wps:
                    ch = "W"
                elif c in WARPTILE:
                    ch = "d"
                elif c in (0x18, 0x14, 0x10):
                    ch = "g"
                elif c in WALKABLE:
                    ch = "."
                else:
                    ch = "#"
                r += ch
            rows.append(r)
        return "\n".join(rows)


if __name__ == "__main__":
    import sys
    w = World()
    for n in sys.argv[1:] or w.maps:
        print(n, w.maps[n].w, w.maps[n].h)
        print(w.ascii(n))
        print()
