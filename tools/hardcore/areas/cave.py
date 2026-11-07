"""Cave maps from the vanilla cave tileset (TILESET_CAVE / TILESET_DARK_CAVE share their block table).

A cave is drawn per tile: a wall/floor grid with two tiles per block.  Every block then gets the vanilla block whose collision
pattern equals its four tiles, so the rock edges come out the way the vanilla caves have them.  The two diagonal patterns do not exist
in the tileset and are repaired before the blocks are chosen.  Ladders are the blocks with a ladder tile in the lower right quadrant
and cave mouths are block 0x37 (wall with a cave tile), so a warp always sits at (2*bx+1, 2*by+1)."""
import random

from .layout import FACE, Slot
from .model import MapDef

# pattern (top left, top right, bottom left, bottom right), 1 = wall, mapped to candidate blocks (the stair-like and arrow blocks are left out)
PATTERNS = {
    (0, 0, 0, 0): [0x02, 0x09],
    (1, 1, 1, 1): [0x1d, 0x2d, 0x2e, 0x2f, 0x34],
    (0, 1, 0, 1): [0x0a, 0x1e, 0x35],
    (1, 0, 1, 0): [0x08, 0x1c],
    (0, 0, 1, 1): [0x0d, 0x21],
    (1, 1, 0, 0): [0x19],
    (1, 0, 1, 1): [0x0c, 0x20],
    (0, 1, 1, 1): [0x0e, 0x22],
    (1, 1, 0, 1): [0x1a],
    (1, 1, 1, 0): [0x18],
    (1, 0, 0, 0): [0x28],
    (0, 1, 0, 0): [0x17, 0x2a],
    (0, 0, 1, 0): [0x11, 0x29],
    (0, 0, 0, 1): [0x2b],
}
VOID = [0x00, 0x01]  # black rock far from any floor
LADDER_UP = [0x07, 0x1b]
LADDER_DOWN = [0x0b, 0x1f]
MOUTH = 0x37  # wall block with a cave tile bottom right: a doorway into the rock, entered from the south
PIT = 0x3f


class Grid:
    """Tile grid of a cave: True = wall."""

    def __init__(self, bw, bh):
        self.bw, self.bh = bw, bh
        self.tw, self.th = 2 * bw, 2 * bh
        self.wall = [[True] * self.tw for _ in range(self.th)]

    def floor(self, x, y):
        return 0 <= x < self.tw and 0 <= y < self.th and not self.wall[y][x]

    def carve(self, x, y, r=1):
        for dy in range(-r + 1, r + 1):
            for dx in range(-r + 1, r + 1):
                xx, yy = x + dx, y + dy
                if 2 <= xx < self.tw - 2 and 2 <= yy < self.th - 2:
                    self.wall[yy][xx] = False

    def tunnel(self, rng, a, b, r=1, wiggle=0.35):
        """A winding 2 tile wide tunnel from tile a to tile b (never straight for long)."""
        x, y = a
        tx, ty = b
        guard = 0
        while (x, y) != (tx, ty) and guard < 4000:
            guard += 1
            self.carve(x, y, r)
            dx, dy = tx - x, ty - y
            if rng.random() < wiggle:
                if rng.random() < 0.5:
                    x += rng.choice((-1, 1)) if abs(dx) < 3 else (1 if dx > 0 else -1)
                else:
                    y += rng.choice((-1, 1)) if abs(dy) < 3 else (1 if dy > 0 else -1)
            elif abs(dx) > abs(dy) or (abs(dx) == abs(dy) and rng.random() < 0.5):
                x += 1 if dx > 0 else -1
            else:
                y += 1 if dy > 0 else -1
            x = max(3, min(self.tw - 4, x))
            y = max(3, min(self.th - 4, y))
        self.carve(tx, ty, r)

    def room(self, cx, cy, rw, rh):
        for y in range(cy - rh, cy + rh + 1):
            for x in range(cx - rw, cx + rw + 1):
                # rounded corners
                if abs(x - cx) == rw and abs(y - cy) == rh:
                    continue
                if 2 <= x < self.tw - 2 and 2 <= y < self.th - 2:
                    self.wall[y][x] = False

    def blobs(self, rng, n, rmin=2, rmax=4):
        """Caverns: n random rounded rooms."""
        for _ in range(n):
            cx = rng.randint(6, self.tw - 7)
            cy = rng.randint(6, self.th - 7)
            self.room(cx, cy, rng.randint(rmin, rmax), rng.randint(rmin, rmax))

    def smooth(self, rounds=1):
        """Fills one tile pockets and removes lone wall tiles so the rock edges stay readable."""
        for _ in range(rounds):
            new = [row[:] for row in self.wall]
            for y in range(2, self.th - 2):
                for x in range(2, self.tw - 2):
                    n = sum(self.floor(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if self.wall[y][x] and n >= 3:
                        new[y][x] = False
                    elif not self.wall[y][x] and n <= 1:
                        new[y][x] = True
            self.wall = new

    def fix_diagonals(self):
        """No block may hold a diagonal wall pair: open one of the two wall tiles."""
        for by in range(self.bh):
            for bx in range(self.bw):
                tl, tr = self.wall[2 * by][2 * bx], self.wall[2 * by][2 * bx + 1]
                bl, br = self.wall[2 * by + 1][2 * bx], self.wall[2 * by + 1][2 * bx + 1]
                if (tl, tr, bl, br) in ((True, False, False, True), (False, True, True, False)):
                    if tl:
                        self.wall[2 * by][2 * bx] = False
                    else:
                        self.wall[2 * by][2 * bx + 1] = False

    def reach(self, start):
        seen = {start}
        todo = [start]
        while todo:
            x, y = todo.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if p not in seen and self.floor(*p):
                    seen.add(p)
                    todo.append(p)
        return seen

    def drop_islands(self, start):
        """Fills every floor tile that cannot be reached from start."""
        ok = self.reach(start)
        for y in range(self.th):
            for x in range(self.tw):
                if not self.wall[y][x] and (x, y) not in ok:
                    self.wall[y][x] = True


def render(grid, m, rng, near_void=True):
    """Chooses the blocks of map m from the tile grid."""
    ground = {(x, y) for y in range(grid.th) for x in range(grid.tw) if not grid.wall[y][x]}

    def near_floor(bx, by, d=2):
        for yy in range(by - d, by + d + 1):
            for xx in range(bx - d, bx + d + 1):
                if 0 <= xx < grid.bw and 0 <= yy < grid.bh:
                    for ty in (2 * yy, 2 * yy + 1):
                        for tx in (2 * xx, 2 * xx + 1):
                            if (tx, ty) in ground:
                                return True
        return False

    for by in range(grid.bh):
        for bx in range(grid.bw):
            pat = tuple(int(grid.wall[2 * by + dy][2 * bx + dx]) for dy in (0, 1) for dx in (0, 1))
            if pat == (1, 1, 1, 1):
                b = rng.choice(PATTERNS[pat]) if near_floor(bx, by, 1) or not near_void else rng.choice(VOID)
            else:
                b = rng.choice(PATTERNS[pat])
            m.set(bx, by, b)


def door_free(grid, x, y):
    return grid.floor(x, y)


def free_line(grid, x, y, dx, dy, n):
    """How many floor tiles lie in a row from (x, y) in direction (dx, dy), up to n."""
    k = 0
    while k < n and grid.floor(x + dx * (k + 1), y + dy * (k + 1)):
        k += 1
    return k


def components(grid, blocked):
    """Number of 4-connected floor regions of the grid when the cells in blocked count as wall."""
    seen, n = set(blocked), 0
    for y in range(grid.th):
        for x in range(grid.tw):
            if (x, y) in seen or not grid.floor(x, y):
                continue
            n += 1
            todo = [(x, y)]
            seen.add((x, y))
            while todo:
                cx, cy = todo.pop()
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if (nx, ny) not in seen and grid.floor(nx, ny):
                        seen.add((nx, ny))
                        todo.append((nx, ny))
    return n


def stop_cells(x, y, face, n):
    """Where a trainer can end up standing: the trainer walks up to the player, so any cell of its line of sight (and its own cell) may be
    the one it stays on after the fight."""
    dx, dy = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}[face]
    return {(x + dx * k, y + dy * k) for k in range(0, n)}


def trainer_slots(grid, rng, count, avoid, minsep=5, sight=5):
    """Places trainers on floor tiles that look along a free line of at least 3 tiles.  avoid: tiles that must stay clear (ladders,
    objects).  A beaten trainer stays on the cell where it stopped, and the cells of two of them can seal a narrow passage for good, so a
    slot is only accepted when the cave stays in as many pieces as it was with every cell a trainer could stop on counted as rock (a
    trainer never ends in a one or two tile wide corridor).  Returns Slot objects."""
    cands = []
    for y in range(3, grid.th - 3):
        for x in range(3, grid.tw - 3):
            if not grid.floor(x, y) or (x, y) in avoid:
                continue
            for face, (dx, dy) in (("UP", (0, -1)), ("DOWN", (0, 1)), ("LEFT", (-1, 0)), ("RIGHT", (1, 0))):
                n = free_line(grid, x, y, dx, dy, sight)
                if n >= 3:
                    cands.append((x, y, face, n))
    rng.shuffle(cands)
    base = components(grid, set())
    slots, used, blocked = [], [], set()
    for x, y, face, n in cands:
        if len(slots) >= count:
            break
        if any(abs(x - ux) + abs(y - uy) < minsep for ux, uy in used) or (x, y) in avoid:
            continue
        more = blocked | stop_cells(x, y, face, n)
        if components(grid, more) > base:
            continue
        used.append((x, y))
        blocked = more
        slots.append(Slot(x, y, face, n))
    return slots
