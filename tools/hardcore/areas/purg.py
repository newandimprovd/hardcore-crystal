"""PURGATORIO: the cave network under the first four areas.  A hub (the Threshold), five floors down ending in the Abyss and five
floors up ending at Nick's Landing.  Fights down here are plain fights (engine: HC_IsSafeGroup): nobody dies, nothing counts toward
the kill milestones.  The floors are generated caves (cave.py) with item gates in necks, hidden hermits who give presents,
balls, and a text pool of the dead and the stuck."""
import random

from art.classes import by_const, sprite as csprite

from . import cast_text as C
from . import named
from . import named_text as N
from . import purg_text as PT
from .cave import (LADDER_DOWN, LADDER_UP, MOUTH, Grid, render)
from .flags import flag_once
from .kits import load_collision
from .layout import FACE, GATES, Slot
from .model import MapDef, link
from .party import NAMES, make_party, party_size
from .people import ball, lore_npc, plain_npc, sign
from .populate import populate
from .specbase import SpecBase
from .text import Text

CAVE_COLL = load_collision("cave")
LM = "LANDMARK_PURGATORIO"
LM_ABYSS = "LANDMARK_THE_ABYSS"
LM_NICK = "LANDMARK_NICKS_LANDING"

CLASS_IDS = ["T_PRIEST", "T_NUN", "T_BEGGAR", "G_ELDER", "G_GRANNY", "G_SHAMAN", "U_DOCTOR", "U_SERF", "L_SAILOR",
             "T_SUIT", "G_BARD", "U_SERFF"]
HERMIT_CLASSES = [("G_ELDER", "SPRITE_HC_ELDER_M", "PAL_NPC_BROWN"), ("G_GRANNY", "SPRITE_HC_ELDER_F", "PAL_NPC_RED"),
                  ("G_SHAMAN", "SPRITE_HC_SHAMAN", "PAL_NPC_GREEN")]
THEME = {"GHOST": 3, "DARK": 3, "PSYCHIC_TYPE": 2.5, "FAIRY": 1.5, "POISON": 1.5, "NORMAL": 1.5, "DRAGON": 1, "ICE": 1,
         "STEEL": 1, "FIGHTING": 1, "ROCK": 1, "GROUND": 1, "BUG": 1, "FLYING": 1, "WATER": 0.8, "GRASS": 0.8,
         "FIRE": 0.8, "ELECTRIC": 0.8}

# floor table: name, direction, level range, necks (travel order, from the ladder you arrive by), ball items, hermit gifts, size
FLOORS = [
    ("PurgDown1", "D", (14, 20), [], ["ETHER", "POTION"], ["PROTEIN", "IRON"]),
    ("PurgDown2", "D", (20, 28), ["roots"], ["SUPER_POTION", "ETHER"], ["CALCIUM", "CARBOS"]),
    ("PurgDown3", "D", (28, 38), ["boulder"], ["OUTBOARD", "REVIVE"], ["HP_UP", "LUCKY_EGG"]),
    ("PurgDown4", "D", (38, 50), ["whirl"], ["HYPER_POTION", "MAX_ETHER"], ["PP_UP", "RARE_CANDY"]),
    ("PurgAbyss", "D", (52, 70), ["hook", "rubble"], ["MAX_ELIXER"], ["MAX_ELIXER", "MAX_REVIVE"]),
    ("PurgUp1", "U", (36, 42), [], ["SUPER_POTION", "REVIVE"], ["PROTEIN", "IRON"]),
    ("PurgUp2", "U", (42, 50), ["river"], ["HYPER_POTION", "ELIXER"], ["CALCIUM", "CARBOS"]),
    ("PurgUp3", "U", (50, 60), ["dark"], ["MAX_POTION", "MAX_ETHER"], ["HP_UP", "PP_UP"]),
    ("PurgUp4", "U", (60, 72), ["slab"], ["FULL_RESTORE", "MAX_REVIVE"], ["RARE_CANDY", "MAX_REVIVE"]),
]


def even(v):
    return v - (v % 2)


class PurgSpec(SpecBase):
    pool = "PG"
    T = PT
    theme = THEME

    def __init__(self, l0, l1, classes):
        self.l0, self.l1, self.classes = l0, l1, classes


def class_table():
    out = []
    for c in CLASS_IDS:
        _, e = by_const(c)
        out.append((e[0], csprite(e[2]), "PAL_NPC_" + e[3], 3))
    return out


def subset(rng, table, n=6):
    order = table[:]
    rng.shuffle(order)
    sprites, out = set(), []
    for c in order:
        if c[1] in sprites or len(sprites) < n:
            sprites.add(c[1])
            out.append(c)
    return out


# ---------------------------------------------------------------------------------------------------- geometry checks

def tile_grid(m):
    g = [[None] * (2 * m.w) for _ in range(2 * m.h)]
    for by in range(m.h):
        for bx in range(m.w):
            c = CAVE_COLL[m.get(bx, by)]
            for q in range(4):
                g[2 * by + q // 2][2 * bx + q % 2] = c[q]
    return g


def passable(c):
    return c in ("FLOOR", "LADDER", "CAVE", "TALL_GRASS", "WARP_CARPET_DOWN")


def reach(m, start):
    g = tile_grid(m)
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if 0 <= p[0] < 2 * m.w and 0 <= p[1] < 2 * m.h and p not in seen and passable(g[p[1]][p[0]]):
                seen.add(p)
                todo.append(p)
    return seen


def verify(m, start):
    """Every object, sign and warp of the map must stand on a walkable tile that can be reached from start."""
    ok = reach(m, start)
    g = tile_grid(m)
    for o in m.objects:
        p = (o["x"], o["y"])
        assert p in ok, f"{m.name}: object at {p} is not reachable ({g[p[1]][p[0]]})"
    for wp in m.warps:
        assert (wp.x, wp.y) in ok, f"{m.name}: warp at {(wp.x, wp.y)} is not reachable"
    for (x, y, _, _) in m.bgs:
        assert any(((x + dx, y + dy) in ok) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (0, 0))), f"{m.name}: sign {(x, y)}"


def near_any(p, pts, d):
    return any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) <= d for q in pts)


# ---------------------------------------------------------------------------------------------------- floors

def carve_floor(rng, bw, bh, nneck, nher):
    """Entry region, nneck necks (two tile wide, four rows long, block aligned) and the regions between them.  Returns the grid and
    a dict: entry/exit tiles (even, the 2x2 brush there becomes the ladder block), neck columns and rows, hermit tiles, regions."""
    G = Grid(bw, bh)
    tw, th = G.tw, G.th
    seg = th // (nneck + 1)
    mids = [even(seg * (i + 1)) for i in range(nneck)]
    cxs = [even(rng.randint(10, tw - 12)) for _ in range(nneck)]
    regions = []
    for i in range(nneck + 1):
        lo = 4 if i == 0 else mids[i - 1] + 5
        hi = th - 5 if i == nneck else mids[i] - 5
        regions.append((lo, hi))
    entry = exit_ = None
    for i, (lo, hi) in enumerate(regions):
        if i == 0:
            S = (even(rng.randint(8, tw - 10)), even(rng.randint(lo + 2, min(lo + 6, hi - 2))))
            entry = S
        else:
            S = (cxs[i - 1], mids[i - 1] + 6)
        if i == nneck:
            E = (even(rng.randint(8, tw - 10)), even(rng.randint(max(lo + 2, hi - 6), hi - 2)))
            exit_ = E
        else:
            E = (cxs[i], mids[i] - 6)
        W = (even(rng.randint(8, tw - 10)), even(rng.randint(lo + 2, hi - 2)))
        G.tunnel(rng, S, W)
        G.tunnel(rng, W, E)
        for _ in range(2):
            bx_ = even(rng.randint(8, tw - 10))
            by_ = even(rng.randint(lo + 2, hi - 2))
            G.room(bx_, by_, rng.randint(2, 3), rng.randint(2, 3))
            G.tunnel(rng, (bx_, by_), W)
    # hermit pockets: far from every floor tile, tied in by a tunnel to the nearest one
    hermits = []
    for _ in range(nher):
        floors = [(x, y) for y in range(th) for x in range(tw) if G.floor(x, y)]
        best = None
        for _try in range(300):
            px, py = even(rng.randint(8, tw - 10)), even(rng.randint(8, th - 10))
            if any(abs(py - m_) <= 7 for m_ in mids):
                continue
            if near_any((px, py), floors, 4):
                continue
            best = (px, py)
            break
        if not best:
            return None
        near = min(floors, key=lambda f: abs(f[0] - best[0]) + abs(f[1] - best[1]))
        G.room(best[0], best[1], 1, 1)
        G.tunnel(rng, best, near)
        hermits.append(best)
    G.smooth(1)
    for i, mid in enumerate(mids):
        for y in range(mid - 4, mid + 5):
            for x in range(2, tw - 2):
                G.wall[y][x] = True
        for y in range(mid - 4, mid + 5):
            G.wall[y][cxs[i]] = False
            G.wall[y][cxs[i] + 1] = False
    for (x, y) in (entry, exit_):
        for dy in (0, 1):
            for dx in (0, 1):
                G.wall[y + dy][x + dx] = False
    G.fix_diagonals()
    G.drop_islands(entry)
    ok = G.reach(entry)
    if exit_ not in ok or any(h not in ok for h in hermits):
        return None
    return G, dict(entry=entry, exit=exit_, mids=mids, cxs=cxs, hermits=hermits, regions=regions)


def cave_gate(w, m, kind, x, y, idx):
    """Two blocking objects across a two tile wide neck, removed by using the key item.  Must be created before any other object."""
    item, sprite, how, no_text, use_text = GATES[kind]
    n = m.name
    c0, c1 = f"GATE{2 * idx}", f"GATE{2 * idx + 1}"
    m.object_consts += [c0, c1]
    if how == "push":
        for i in range(2):
            m.obj(x + i, y, sprite, "SPRITEMOVEDATA_STRENGTH_BOULDER", f"{n}BoulderScript", pal="PAL_NPC_BROWN")
        if f"{n}BoulderScript:" not in "".join(m.scripts):
            m.scripts.append(f"{n}BoulderScript:\n\tjumpstd StrengthBoulderScript\n")
        return
    flag = w.flag(f"EVENT_GEN_{m.const}_GATE{idx}")
    for i in range(2):
        m.obj(x + i, y, sprite, "SPRITEMOVEDATA_STILL", f"{n}Gate{idx}Script", pal="PAL_NPC_BROWN", flag=flag)
    m.scripts.append(
        f"{n}Gate{idx}Script:\n\tcheckitem {item}\n\tiffalse .Missing\n\topentext\n\twritetext {n}Gate{idx}UseText\n"
        f"\twaitbutton\n\tclosetext\n\tplaysound SFX_STRENGTH\n\tearthquake 12\n\twaitsfx\n"
        f"\tdisappear {m.const}_{c0}\n\tdisappear {m.const}_{c1}\n\tsetevent {flag}\n\tend\n\n"
        f".Missing:\n\tjumptext {n}Gate{idx}NoText\n")
    m.scripts.append(Text(no_text).emit(f"{n}Gate{idx}NoText"))
    m.scripts.append(Text(use_text).emit(f"{n}Gate{idx}UseText"))


def hermit(w, m, roster, rng, x, y, i, level, item, texts_idx):
    cls, spr, pal = HERMIT_CLASSES[texts_idx % 3]
    party = make_party(roster, rng, level, 4, THEME)
    name = rng.choice(NAMES)
    tid = w.trainer(cls, name, party)
    beaten = w.flag(f"EVENT_GEN_{m.const}_HERMIT{i}")
    gift = w.flag(f"EVENT_GEN_{m.const}_HGIFT{i}")
    n = f"{m.name}Hermit{i}"
    k = texts_idx
    m.scripts.append(
        f"{n}:\n\tfaceplayer\n\topentext\n\tcheckevent {gift}\n\tiftrue .Done\n\tcheckevent {beaten}\n\tiftrue .Gift\n"
        f"\twritetext {n}SeenText\n\twaitbutton\n\tclosetext\n\twinlosstext {n}BeatenText, 0\n"
        f"\tloadtrainer {cls}, {tid}\n\tstartbattle\n\treloadmapafterbattle\n\tsetevent {beaten}\n\topentext\n"
        f".Gift:\n\twritetext {n}GiftText\n\twaitbutton\n\tverbosegiveitem {item}\n\tiffalse .NoRoom\n\tsetevent {gift}\n"
        f".Done:\n\twritetext {n}AfterText\n\twaitbutton\n\tclosetext\n\tend\n\n"
        f".NoRoom:\n\twritetext {n}NoRoomText\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(Text(C.HERMIT_SEEN[k % len(C.HERMIT_SEEN)]).emit(f"{n}SeenText"))
    m.scripts.append(Text(C.HERMIT_BEATEN[k % len(C.HERMIT_BEATEN)]).emit(f"{n}BeatenText"))
    m.scripts.append(Text(C.HERMIT_GIFT[k % len(C.HERMIT_GIFT)]).emit(f"{n}GiftText"))
    m.scripts.append(Text(C.HERMIT_AFTER[k % len(C.HERMIT_AFTER)]).emit(f"{n}AfterText"))
    m.scripts.append(Text("Your bag is full. The gift will wait. So will I. That is what I do.").emit(f"{n}NoRoomText"))
    m.obj(x, y, spr, FACE["DOWN"], n, pal=pal)


def free_spots(G, rng, avoid, count, minsep=6, rows=None):
    """Open tiles (the whole 3x3 around is floor), spread out.  rows: (y0, y1) the FIRST spot must lie in (the later region)."""
    cands = [(x, y) for y in range(4, G.th - 4) for x in range(4, G.tw - 4)
             if all(G.floor(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)) and not near_any((x, y), avoid, 3)]
    rng.shuffle(cands)
    if rows:
        cands.sort(key=lambda c: 0 if rows[0] <= c[1] < rows[1] else 1)
    out = []
    for c in cands:
        if len(out) >= count:
            break
        if all(abs(c[0] - o[0]) + abs(c[1] - o[1]) >= minsep for o in out):
            out.append(c)
    if rows and out and not (rows[0] <= out[0][1] < rows[1]):
        return []
    return out


def build_floor(g, w, roster, rng, spec_table, idx, name, direction, lv, necks, balls, gifts, lm, music, tr_target=8,
                extra_objs=0, last=False):
    for attempt in range(120):
        r = random.Random(f"{name}:{attempt}:{rng.random()}")
        res = carve_floor(r, 20, 20 if len(necks) < 2 else 28, len(necks), 2)
        if not res:
            continue
        G, info = res
        avoid = [info["entry"], info["exit"]] + [(info["cxs"][i], info["mids"][i]) for i in range(len(necks))]
        zone = set()
        for i in range(len(necks)):
            for y in range(info["mids"][i] - 7, info["mids"][i] + 8):
                for x in range(info["cxs"][i] - 4, info["cxs"][i] + 6):
                    zone.add((x, y))
        spots_avoid = avoid + info["hermits"] + [(x, y) for (x, y) in zone if (x + y) % 3 == 0]
        late = (info["mids"][0] + 7, G.th) if necks and balls[0] == "OUTBOARD" else None
        spots = free_spots(G, r, spots_avoid, len(balls), rows=late)
        if len(spots) == len(balls):
            res = (G, info, avoid, zone, spots)
            break
    else:
        raise RuntimeError(f"no cave for {name}")
    G, info, avoid, avoid_zone, ball_spots = res
    bw, bh = G.bw, G.bh
    m = MapDef(g.key, name, bw, bh, "TILESET_CAVE", "DUNGEON", lm, music, pal="PALETTE_DAY", border=0x00)
    render(G, m, r)
    entry, exit_ = info["entry"], info["exit"]
    travel_down = direction == "D"
    # D floors: arrive by the ladder that leads up (entry), leave by the ladder that leads down; U floors the other way round
    m.set(entry[0] // 2, entry[1] // 2, r.choice(LADDER_UP if travel_down else LADDER_DOWN))
    we = m.warp(entry[0] + 1, entry[1] + 1, "ladder")
    m.warps_in, m.warps_out = we, None
    if not last:
        m.set(exit_[0] // 2, exit_[1] // 2, r.choice(LADDER_DOWN if travel_down else LADDER_UP))
        m.warps_out = m.warp(exit_[0] + 1, exit_[1] + 1, "ladder")
    # gates first (their object constants are GATE0..): the neck's middle row
    for i, kind in enumerate(necks):
        cx, mid = info["cxs"][i], info["mids"][i]
        cave_gate(w, m, kind, cx, mid, i)
    her = info["hermits"]
    lv0, lv1 = lv
    cls_sub = subset(r, spec_table)
    spec = PurgSpec(lv0, lv1, cls_sub)
    items = list(balls)
    n_obj = 2 * len(necks) + 2 + len(balls) + extra_objs
    count = min(tr_target, 15 - n_obj)
    slots = trainer_slots_for(G, r, count, avoid + her + ball_spots, avoid_zone)
    populate(w, m, slots, spec, r, roster, 0.0, 1.0)
    for i, (hx, hy) in enumerate(her):
        hermit(w, m, roster, r, hx, hy, i, lv0 + (lv1 - lv0) * (i + 1) // 3, gifts[i], idx * 2 + i)
    # place balls: for floors with a neck the first listed ball goes beyond the neck (the later region)
    for i, (bx_, by_) in enumerate(ball_spots):
        ball(w, m, bx_, by_, items[i], f"BALL{i}")
    return m, G, info


def trainer_slots_for(G, rng, count, avoid, zone):
    from .cave import trainer_slots
    avoid_all = set(avoid) | set(zone)
    # also keep away from ladders in a radius
    for (x, y) in list(avoid):
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                avoid_all.add((x + dx, y + dy))
    return trainer_slots(G, rng, count, avoid_all)


# ---------------------------------------------------------------------------------------------------- the hub

def hub(g, w, roster, rng):
    """The Threshold: one big cavern, four mouths in the north wall (one to each of the first four areas, sealed from this side
    until that mouth has been used from the other side), a Mouth to the junction in the south, a ladder down (west alcove) and a
    ladder up (east alcove, sealed until the Commune mouth is open)."""
    bw, bh = 24, 20
    G = Grid(bw, bh)
    tw, th = G.tw, G.th
    G.room(24, 22, 16, 10)  # x 8..40, y 12..32
    for y in range(20, 22):  # a central pillar
        for x in range(22, 26):
            G.wall[y][x] = True
    for y in range(24, 26):  # alcoves west and east
        for x in range(4, 8):
            G.wall[y][x] = False
        for x in range(41, 46):
            G.wall[y][x] = False
    ex = 12  # south entrance block column (tiles 24, 25)
    for y in range(33, 39):
        G.wall[y][2 * ex] = False
        G.wall[y][2 * ex + 1] = False
    G.fix_diagonals()
    m = MapDef(g.key, "PurgThreshold", bw, bh, "TILESET_CAVE", "DUNGEON", LM, "MUSIC_UNION_CAVE", pal="PALETTE_DAY", border=0x00)
    render(G, m, rng)
    south = m.warp(2 * ex + 1, 2 * (bh - 1) + 1, "mouth")
    m.set(ex, bh - 1, 0x24)  # floor with a warp carpet bottom right: a cave door (0x13) on the last row walks the player off the map on arrival
    # the four mouths
    mouths = []
    for bx in (6, 10, 14, 18):
        m.set(bx, 5, MOUTH)
        mouths.append(m.warp(2 * bx + 1, 2 * 5 + 1, "mouth"))
    down = m.warp(5, 25, "ladder")
    m.set(2, 12, rng.choice(LADDER_DOWN))
    up = m.warp(45, 25, "ladder")
    m.set(22, 12, rng.choice(LADDER_UP))
    # objects: sealed rocks first (they hide once the flag is set)
    m.scripts.append("PurgThresholdSealedScript:\n\tjumptext PurgThresholdSealedText\n")
    m.scripts.append(Text(C.SEALED).emit("PurgThresholdSealedText"))
    for i, bx in enumerate((6, 10, 14, 18)):
        f = flag_once(w, f"EVENT_PURG_OPEN_A{i + 1}")
        m.obj(2 * bx + 1, 2 * 5 + 2, "SPRITE_ROCK", "SPRITEMOVEDATA_STILL", "PurgThresholdSealedScript", pal="PAL_NPC_BROWN", flag=f)
    f2 = flag_once(w, "EVENT_PURG_OPEN_A2")
    for dy in (24, 25):  # the way up is sealed until the Commune mouth is open
        m.obj(42, dy, "SPRITE_ROCK", "SPRITEMOVEDATA_STILL", "PurgThresholdSealedScript", pal="PAL_NPC_BROWN", flag=f2)
    # people
    m.scripts.append(
        "PurgThresholdHealerScript:\n\tfaceplayer\n\topentext\n\twritetext PurgThresholdHealerText\n\twaitbutton\n\tclosetext\n"
        "\tspecial HealParty\n\tplaysound SFX_FULL_HEAL\n\twaitsfx\n\tend\n")
    m.scripts.append(Text(C.HUB_HEALER).emit("PurgThresholdHealerText"))
    m.obj(24, 18, "SPRITE_HC_SHADE", FACE["DOWN"], "PurgThresholdHealerScript", pal="PAL_NPC_BLUE")
    named.add_hub(w, g, m, roster)  # Steiner and Abd al-Jabbar, two optional duels with a page of the CORKBOARD each
    # the rival, once the Axiom mouth is open: he waits in the middle of the cavern and stops the player at the south corridor
    from .cameos import add_sprite
    add_sprite(g, "SPRITE_RIVAL")
    named.rival_duel(w, m, "RIVAL4", "RIVAL2", 56, 5, random.Random("named-RIVAL4"), roster, N.RIVAL4, (25, 30),
                     [(24, 34), (25, 34)], requires="EVENT_PURG_OPEN_A3")
    spots = [(14, 18, "SPRITE_HC_FORGOTTEN", "PAL_NPC_BLUE", "RIGHT"), (35, 18, "SPRITE_HC_DAMNED", "PAL_NPC_BROWN", "LEFT"),
             (17, 29, "SPRITE_HC_ELDER_M", "PAL_NPC_GREEN", "UP"), (31, 29, "SPRITE_HC_BEGGAR", "PAL_NPC_RED", "UP")]
    for i, (x, y, sp, pal, face) in enumerate(spots):
        plain_npc(m, x, y, sp, pal, face, f"PurgThresholdNpc{i}Script", C.HUB_NPC[i])
    sign(m, 22, 11, "PurgThresholdSign", C.HUB_SIGN)
    sign(m, 6, 23, "PurgThresholdSignDown", C.HUB_SIGN_DOWN)
    sign(m, 44, 23, "PurgThresholdSignUp", C.HUB_SIGN_UP)
    g.add(m)
    verify(m, (2 * ex + 1, 2 * (bh - 1)))
    return m, south, mouths, down, up


# ---------------------------------------------------------------------------------------------------- Abyss and Nick's Landing

def floor_near(G, start, n, spread=3, dmin=2, dmax=9):
    """n floor tiles near start (breadth first order), at least `spread` apart."""
    seen = {start: 0}
    todo = [start]
    out = []
    while todo:
        x, y = todo.pop(0)
        d = seen[(x, y)]
        if dmin <= d <= dmax and all(abs(x - a) + abs(y - b) >= spread for a, b in out) and \
                all(G.floor(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
            out.append((x, y))
            if len(out) == n:
                break
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p not in seen and G.floor(*p):
                seen[p] = d + 1
                todo.append(p)
    assert len(out) == n, "no room near the grave"
    return out


def post_spot(G, start, taken):
    """A wall tile next to a floor tile near start (the post is read from the floor tile)."""
    seen = {start}
    todo = [start]
    while todo:
        x, y = todo.pop(0)
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            p = (x + dx, y + dy)
            if not G.floor(*p) and abs(x - start[0]) + abs(y - start[1]) >= 3 and all(abs(p[0] - t[0]) + abs(p[1] - t[1]) > 2 for t in taken) \
                    and 2 <= p[0] < G.tw - 2 and 2 <= p[1] < G.th - 2:
                return p
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in seen and G.floor(*q):
                seen.add(q)
                todo.append(q)
    raise AssertionError("no wall for the post")


def abyss_extras(w, m, info, G):
    """The last region behind the rubble: the grave (the body of the first victim), the Trumpet and the post."""
    exit_ = info["exit"]
    (gx, gy), (tx, ty) = floor_near(G, (exit_[0], exit_[1]), 2)
    flag = flag_once(w, "EVENT_ABYSS_GRAVE_READ")
    flag_once(w, "EVENT_LORE_GRAVE")
    m.scripts.append(
        f"PurgAbyssGraveScript:\n\topentext\n\twritetext PurgAbyssGraveText\n\twaitbutton\n\tsetevent {flag}\n"
        f"\tsetevent EVENT_LORE_GRAVE\n\tclosetext\n\tend\n")
    m.scripts.append(Text(C.GRAVE).emit("PurgAbyssGraveText"))
    m.obj(gx, gy, "SPRITE_CORPSE", "SPRITEMOVEDATA_STILL", "PurgAbyssGraveScript", pal="PAL_NPC_BROWN")
    ball(w, m, tx, ty, "TRUMPET", "TRUMPET")
    wx, wy = post_spot(G, (exit_[0], exit_[1]), [(gx, gy), (tx, ty)])
    sign(m, wx, wy, "PurgAbyssPost", C.CAPREAL, flag="EVENT_LORE_CAPREAL", w=w)


def landing(g, w, roster, rng):
    """Nick's Landing: the top floor, one room, Bruno at the far end."""
    bw, bh = 14, 14
    G = Grid(bw, bh)
    G.room(14, 14, 7, 6)
    G.tunnel(rng, (14, 18), (14, 22))
    G.fix_diagonals()
    G.drop_islands((14, 14))
    m = MapDef(g.key, "PurgLanding", bw, bh, "TILESET_CAVE", "DUNGEON", LM_NICK, "MUSIC_SPROUT_TOWER", pal="PALETTE_DAY", border=0x00)
    render(G, m, rng)
    ex, ey = 14, 22
    for dy in (0, 1):
        for dx in (0, 1):
            G.wall[ey + dy][ex + dx] = False
    m.set(ex // 2, ey // 2, rng.choice(LADDER_DOWN))
    entry = m.warp(ex + 1, ey + 1, "ladder")
    # Bruno: a level 100 team of strong fourth stages, one per type where possible
    types, party = set(), []
    pool = roster.by_stage[4][:]
    rng.shuffle(pool)
    for mon in pool:
        t = mon["types"][0]
        if t not in types:
            types.add(t)
            party.append((100, mon["const"]))
        if len(party) == 6:
            break
    tid = w.trainer("MYSTICALMAN", "BRUNO", party)
    for k in ("EVENT_PURG_BRUNO_BEATEN", "EVENT_PURG_NICK", "EVENT_LORE_BRUNO"):
        flag_once(w, k)
    m.scripts.append(
        "PurgLandingBrunoScript:\n\tfaceplayer\n\topentext\n\tcheckevent EVENT_PURG_NICK\n\tiftrue .Nick\n"
        "\tcheckevent EVENT_LORE_BRUNO\n\tiftrue .Ask\n\twritetext PurgLandingBrunoIntro\n\twaitbutton\n\tsetevent EVENT_LORE_BRUNO\n"
        ".Ask:\n\twritetext PurgLandingBrunoAsk\n\tyesorno\n\tiffalse .No\n\twritetext PurgLandingBrunoGo\n\twaitbutton\n"
        "\tclosetext\n\twinlosstext PurgLandingBrunoBeatenText, 0\n"
        f"\tloadtrainer MYSTICALMAN, {tid}\n\tstartbattle\n\treloadmapafterbattle\n"
        "\tsetevent EVENT_PURG_BRUNO_BEATEN\n\tsetevent EVENT_PURG_NICK\n\tsetflag ENGINE_MAP_CARD\n\tpause 20\n"
        "\tspecial FadeOutToWhite\n\tpause 20\n\tspecial FadeInFromWhite\n\topentext\n\twritetext PurgLandingReborn\n\twaitbutton\n"
        "\twritetext PurgLandingLift\n\tyesorno\n\tiffalse .Stay\n\tclosetext\n\tspecial FadeOutToBlack\n"
        "\twarp PURG_THRESHOLD, 24, 30\n\tend\n"
        ".Stay:\n\tclosetext\n\tend\n"
        ".No:\n\twritetext PurgLandingBrunoNo\n\twaitbutton\n\tclosetext\n\tend\n"
        ".Nick:\n\twritetext PurgLandingNick\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(Text(C.BRUNO_1).emit("PurgLandingBrunoIntro"))
    m.scripts.append(Text(C.BRUNO_ASK).emit("PurgLandingBrunoAsk"))
    m.scripts.append(Text(C.BRUNO_GO).emit("PurgLandingBrunoGo"))
    m.scripts.append(Text(C.BRUNO_NO).emit("PurgLandingBrunoNo"))
    m.scripts.append(Text(C.BRUNO_BEATEN).emit("PurgLandingBrunoBeatenText"))
    m.scripts.append(Text(C.BRUNO_REBORN).emit("PurgLandingReborn"))
    m.scripts.append(Text("NICK: Want a lift back down? I know a shortcut. It is called a time machine. It is mostly a bucket.").emit("PurgLandingLift"))
    m.scripts.append(Text(C.BRUNO_AFTER).emit("PurgLandingNick"))
    m.obj(14, 10, "SPRITE_HC_BRUNO", FACE["DOWN"], "PurgLandingBrunoScript", pal="PAL_NPC_BROWN")
    lore_npc(w, m, 10, 14, "SPRITE_HC_SHADE", "PAL_NPC_BLUE", "RIGHT", "PurgLandingShadeScript",
             "Do not mind Bruno. He is always on fire. Mostly figuratively. The rest is a long story about a Thursday.")
    g.add(m)
    verify(m, (ex + 1, ey))
    return m, entry


# ---------------------------------------------------------------------------------------------------- main

def build(w, roster, rng, plaza_doors, junction_warp):
    """plaza_doors: {'A1'..'A4': the unlinked rift door warp of that area's 60 percent plaza}; junction_warp: the cave mouth warp of the
    Tithe Junction.  Returns the group."""
    w.landmarks.append(("PURGATORIO", 84, 76, "PURGATORIO"))
    w.landmarks.append(("THE_ABYSS", 84, 84, "THE<BSP>ABYSS"))
    w.landmarks.append(("NICKS_LANDING", 84, 68, "NICKS<BSP>LANDING"))
    sprites = ["SPRITE_HC_SHADE", "SPRITE_HC_STEINER", "SPRITE_HC_BRUNO", "SPRITE_HC_FORGOTTEN", "SPRITE_HC_DAMNED",
               "SPRITE_ROCK", "SPRITE_BOULDER", "SPRITE_POKE_BALL", "SPRITE_CORPSE"]
    g = w.group("PURG", sprites)
    w.pools["PG"] = dict(seen=PT.SEEN, beaten=PT.BEATEN, after=PT.AFTER)
    table = class_table()
    hubm, south, mouths, down, up = hub(g, w, roster, rng)
    link(south, junction_warp)
    for k, key in enumerate(("A1", "A2", "A3", "A4")):
        link(mouths[k], plaza_doors[key])
    prevs = {"D": down, "U": up}
    for i, (name, direction, lv, necks, balls, gifts) in enumerate(FLOORS):
        lm = LM_ABYSS if name == "PurgAbyss" else LM
        music = "MUSIC_NONE" if name == "PurgAbyss" else "MUSIC_DARK_CAVE"
        tn = list(necks)
        if direction == "U" and False:
            tn.reverse()
        abyss = name == "PurgAbyss"
        m, G, info = build_floor(g, w, roster, rng, table, i, name, direction, lv, tn, balls, gifts, lm, music,
                                 tr_target=5 if abyss else 8, extra_objs=2 if abyss else 0, last=abyss)
        link(prevs[direction], m.warps_in)
        if m.warps_out is not None:
            prevs[direction] = m.warps_out
        g.add(m)
        if name == "PurgAbyss":
            abyss_extras(w, m, info, G)
        verify(m, (info["entry"][0] + 1, info["entry"][1]))
    land, lentry = landing(g, w, roster, rng)
    link(prevs["U"], lentry)
    # the last D ladder (below the Abyss) does not exist: the Abyss exit ladder is replaced by a plain floor
    return g
