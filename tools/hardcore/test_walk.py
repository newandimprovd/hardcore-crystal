#!/usr/bin/env python3
"""Area walker: plans over the emitted map files (areamodel.py) and drives PyBoy step by step.

usage: test_walk.py ROM [goal,goal,...]
ROM built with: testbuild.sh cg1 TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=8 TEST_MON=CTHULUDON TEST_LEVEL=60 TEST_REVEALED=1 TEST_ITEMS=1
Goals are map names to reach in order. Every divergence between the model and the emulator is printed,
every fight is logged, and a screenshot is saved the first time each map is entered.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gbtest import T  # noqa: E402
from areamodel import DIRS, World  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/walk")
os.makedirs(SHOTS, exist_ok=True)
GOD = os.environ.get("WALK_GOD") == "1"


def find_ids(world):
    """Map name -> (group, number)."""
    ids = {}
    g = 0
    n = 0
    cons = {}
    for l in open(os.path.join(ROOT, "constants/map_constants.asm")):
        if re.match(r"\s*newgroup", l):
            g += 1
            n = 0
        m = re.match(r"\s*map_const (\w+),", l)
        if m:
            n += 1
            cons[m[1]] = (g, n)
    # the area group is appended after the vanilla groups by the generated file included at the end
    g = max(v[0] for v in cons.values())
    n = 0
    for l in open(os.path.join(ROOT, "constants/area_map_constants.asm")):
        if re.match(r"\s*newgroup", l):
            g += 1
            n = 0
        m = re.match(r"\s*map_const (\w+),", l)
        if m:
            n += 1
            cons[m[1]] = (g, n)
    for name, mp in world.maps.items():
        if mp.const in cons:
            ids[cons[mp.const]] = name
    return ids


def const_table(path):
    """Name -> value for a constants file made of const_def / const / const_next / const_skip lines."""
    out, v = {}, 0
    for l in open(os.path.join(ROOT, path)):
        l = l.split(";")[0].strip()
        m = re.match(r"const_def\s*(\d*)", l)
        if m:
            v = int(m[1]) if m[1] else 0
            continue
        m = re.match(r"const_next\s+(\$?[0-9a-fA-F]+)", l)
        if m:
            v = int(m[1].replace("$", "0x"), 0)
            continue
        if l.startswith("const_skip"):
            v += 1
            continue
        m = re.match(r"const (\w+)", l)
        if m:
            out[m[1]] = v
            v += 1
    return out


def load_best_moves():
    """One plain damaging move per type and the type chart, so the walker can always hurt the enemy: this ROM
    gives Normal and Bug immunities (Dark cannot hit Normal, and so on), so a single move is not enough."""
    types = const_table("constants/type_constants.asm")
    moves = const_table("constants/move_constants.asm")
    best = {}
    for l in open(os.path.join(ROOT, "data/moves/moves.asm")):
        m = re.match(r"\s*move (\w+),\s*(EFFECT_NORMAL_HIT),\s*(\d+),\s*(\w+),", l)
        if m and int(m[3]) >= 40 and m[1] in moves and m[4] in types:
            t = types[m[4]]
            if t not in best or int(m[3]) > best[t][1]:
                best[t] = (moves[m[1]], int(m[3]))
    chart = {}
    for l in open(os.path.join(ROOT, "data/types/type_matchups.asm")):
        m = re.match(r"\s*db (\w+),\s*(\w+),\s*(NO_EFFECT|NOT_VERY_EFFECTIVE|SUPER_EFFECTIVE)", l)
        if m and m[1] in types and m[2] in types:
            chart[(types[m[1]], types[m[2]])] = {"NO_EFFECT": 0, "NOT_VERY_EFFECTIVE": 5, "SUPER_EFFECTIVE": 20}[m[3]]
    return best, chart


BEST, CHART = load_best_moves()


def pick_move(t1, t2):
    top = None
    for ty, (mv, pw) in BEST.items():
        mult = CHART.get((ty, t1), 10) * (CHART.get((ty, t2), 10) if t2 != t1 else 10)
        key = (mult * pw, pw)
        if top is None or key > top[0]:
            top = (key, mv)
    return top[1]


class Walker:
    def __init__(self, rom):
        self.w = World()
        self.ids = find_ids(self.w)
        self.t = T(rom)
        self.fights = []
        self.log = []
        self.entered = set()
        self.cur = None
        t = self.t
        for i in range(600):
            t.pb.button("a" if i % 2 else "start", 4)
            t.tick(20)
            if t.mem("wMapGroup") and t.mem("wXCoord"):
                break
        t.tick(200)
        self.battle_seen = False
        self.die = False  # tests set this to lose the next fight on purpose
        t.hook("BattleMenu", self.menu_hook)

    # ------------------------------------------------------------------ helpers
    def menu_hook(self, ctx):
        t = self.t
        if self.die:
            for off in (0, 1):
                t.poke("wBattleMonHP", 0, off)
                t.poke("wPartyMon1HP", 0, off)
            return
        if GOD:  # map tests only: one Pokemon cannot carry 13 fights of later areas, a real player has six and items
            for off, b in enumerate((0x03, 0xE7)):  # 999 HP: later enemies one-shot a 358 HP level 100 mon
                for sym in ("wBattleMonHP", "wBattleMonMaxHP", "wPartyMon1HP", "wPartyMon1MaxHP"):
                    t.poke(sym, b, off)
        t.poke("wBattleMonMoves", pick_move(t.mem("wEnemyMonType1"), t.mem("wEnemyMonType2")), 0)
        t.poke("wBattleMonPP", 30, 0)
        for sym in ("wBattleMonStatus", "wPlayerSubStatus1", "wPlayerSubStatus2", "wPlayerSubStatus3",
                    "wPlayerSubStatus4", "wPlayerSubStatus5", "wPlayerConfuseCount", "wPlayerDisableCount",
                    "wPlayerEncoreCount", "wDisabledMove"):
            t.poke(sym, 0)  # the walker only tests maps: no sleep, confusion, Disable or Encore stalls
        t.poke("wEnemySubStatus5", t.mem("wEnemySubStatus5") & ~0x40)  # Destiny Bond would take the lone test mon along
        t.poke("wCurMoveNum", 0)
        if not self.battle_seen:
            self.battle_seen = True
            n = t.mem("wOTPartyCount")
            self.fights.append(dict(cls=t.mem("wTempTrainerClass"), id=t.mem("wTempTrainerID"), n=n,
                                    party=t.mem("wOTPartySpecies", 0, max(n, 1)), lvl=t.mem("wEnemyMonLevel"),
                                    at=self.state()))

    def raw_state(self):
        t = self.t
        g, n, x, y = t.where()
        return (self.ids.get((g, n), f"?{g}:{n}"), x, y)

    def state(self):
        """Position once the player has stopped moving: map and coordinates change at different moments
        while a step or a map connection is being crossed, so wait for three equal readings."""
        last, same = None, 0
        for _ in range(40):
            cur = self.raw_state()
            same = same + 1 if cur == last else 0
            if same >= 2:
                return cur
            last = cur
            self.t.tick(3)
        return last

    def busy(self):
        t = self.t
        return bool(t.mem("wScriptRunning") or t.mem("wBattleMode"))

    def settle(self, limit=3000):
        """Mash A while a script or battle is running."""
        t = self.t
        quiet = 0
        for i in range(limit):
            if self.busy():
                quiet = 0
                t.pb.button("a", 4)
                t.tick(16)
            else:
                quiet += 1
                t.tick(6)
                if quiet > 6:
                    break
        if not t.mem("wBattleMode"):
            self.battle_seen = False
        return i

    def note(self, msg):
        self.log.append(msg)
        print("  !!", msg)

    def seen_map(self):
        name = self.state()[0]
        if name not in self.entered:
            self.entered.add(name)
            self.t.shot(f"{SHOTS}/{name}.png", 3)
            print(f"  entered {name} at {self.state()[1:]}")

    # ------------------------------------------------------------------ movement
    def press_dir(self, d):
        t = self.t
        before = self.state()
        for attempt in range(4):
            t.pb.button(d, 9)
            t.tick(9 + 14)  # the coordinates only change when the 16 frame step ends
            self.settle_if_event()
            if self.state() != before:
                return
        return

    def settle_if_event(self):
        if self.busy():
            kills0 = self.t.mem("wHCKillCount", 0, 2)
            self.settle()
            kills1 = self.t.mem("wHCKillCount", 0, 2)
            if kills1 != kills0:
                print(f"  kill {kills1[0] + 256 * kills1[1]} at {self.state()}")

    def go(self, goal_map, max_replans=60):
        return self.go_state(lambda s: s[0] == goal_map, goal_map, max_replans)

    def go_state(self, pred, goal_map, max_replans=60):
        w = self.w
        print(f"-> {goal_map}")
        replans = 0
        while replans < max_replans:
            cur = self.state()
            if pred(cur):
                return True
            if cur[0] not in w.maps:
                self.note(f"unknown map {cur}")
                return False
            path = w.route(cur, pred)
            if path is None:
                path = w.route(cur, pred, ignore_obj=True)
            if path is None:
                self.note(f"no model route from {cur} to {goal_map}")
                return False
            replans += 1
            if os.environ.get("WALKDEBUG") and replans > 2:
                print("   plan", cur, [(d, e[1:], kd) for d, e, kd in path[:6]])
            for k, (d, exp, kind) in enumerate(path):
                before = self.state()
                self.press_dir(d)
                self.seen_map()
                actual = self.state()
                if actual == exp:
                    continue
                later = [j for j in range(k + 1, len(path)) if path[j][1] == actual]
                if later:  # took more than one step, still on the planned route
                    for _ in range(later[0] - k):
                        pass
                    path = path[:k + 1] + path[later[0] + 1:]
                    break
                if kind in ("warp", "conn") and actual[0] == exp[0]:
                    if kind in ("warp", "conn") and abs(actual[1] - exp[1]) + abs(actual[2] - exp[2]) <= 1:
                        break  # a door arrival steps down, and a held key may take one more step across a connection
                    if actual != exp:
                        self.note(f"{kind} {before}->{exp[0]} landed {actual[1:]} expected {exp[1:]}")
                    break
                if actual == before:
                    self.note(f"blocked: {before} {d} (expected {exp}, {kind}); marking")
                    w.blocked.add(exp)
                elif actual[0] == exp[0] and abs(actual[1] - exp[1]) + abs(actual[2] - exp[2]) <= 1:
                    print(f"  (drift: {actual} instead of {exp}, replanning)")  # a held key took one more step
                elif actual[0] != before[0] or abs(actual[1] - before[1]) + abs(actual[2] - before[2]) > 1:
                    self.note(f"unexpected position {actual} after {d} from {before}, expected {exp}")
                break
        self.note(f"gave up on {goal_map}")
        return False


def has_item(wk, const_value):
    t = wk.t
    n = t.mem("wNumKeyItems")
    items = t.mem("wKeyItems", 0, max(n, 2))
    return const_value in (items if isinstance(items, list) else [items])


def item_value(name):
    for l in open(os.path.join(ROOT, "constants/item_constants.asm")):
        m = re.match(r"\s*const (\w+)\s*;\s*([0-9a-f]+)", l)
        if m and m[1] == name:
            return int(m[2], 16)
    raise KeyError(name)


def open_gate(wk, name):
    """Open the gate of a lane: tree gates need the CHAINSAW, boulder gates the CROWBAR (pushed two cells)."""
    w = wk.w
    mp = w.maps[name]
    gates = [(i, o) for i, o in enumerate(mp.objects)
             if o["script"].endswith(("GateScript", "BoulderScript")) and (name, i) not in w.removed]
    if not gates:
        wk.note(f"{name}: no gate objects")
        return False
    i0, o0 = min(gates, key=lambda g: g[1]["x"])
    print(f"gate {o0['script']} at {o0['x']},{o0['y']}")
    gx, gy = o0["x"], o0["y"]
    if not wk.go_state(lambda s: s == (name, gx, gy + 1), f"{name} below the gate"):
        return False
    wk.t.pb.button("up", 9)  # face the object
    wk.t.tick(24)
    wk.t.pb.button("a", 4)
    wk.t.tick(20)
    wk.settle()
    if o0["script"].endswith("GateScript"):
        for i, o in gates:
            w.removed.add((name, i))
        wk.t.tick(30)
        return True
    # boulder: the first A asks to use the CROWBAR; push it up twice to clear the neck
    for _ in range(2):
        wk.press_dir("up")
    st = wk.state()
    if st != (name, gx, gy - 1):
        wk.note(f"{name}: boulder push left the player at {st}, expected {(name, gx, gy - 1)}")
        return False
    w.moved[(name, i0)] = (gx, gy - 2)
    return True


def heal(wk, name):
    """Go into a Pokecenter, stand at the counter and talk to the nurse; checks the party is at full HP after."""
    t = wk.t
    if not wk.go_state(lambda s: s == (name, 3, 3), f"{name} counter"):
        return False
    t.pb.button("up", 9)
    t.tick(24)
    t.pb.button("a", 4)
    t.tick(20)
    wk.settle()
    t.tick(60)
    hp = t.mem("wPartyMon1HP", 0, 2)
    mx = t.mem("wPartyMon1MaxHP", 0, 2)
    if hp != mx:
        wk.note(f"{name}: after healing HP {hp} != max {mx}")
        return False
    return True


def pick_item(wk, name):
    w = wk.w
    mp = w.maps[name]
    balls = [(i, o) for i, o in enumerate(mp.objects) if o["otype"] == "OBJECTTYPE_ITEMBALL" and (name, i) not in w.removed]
    if not balls:
        wk.note(f"{name}: no item ball")
        return False
    i0, o = balls[0]
    bx, by = o["x"], o["y"]
    if not wk.go_state(lambda s: s[0] == name and abs(s[1] - bx) + abs(s[2] - by) == 1, f"{name} next to the ball"):
        return False
    st = wk.state()
    d = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}[(bx - st[1], by - st[2])]
    wk.t.pb.button(d, 9)
    wk.t.tick(24)
    wk.t.pb.button("a", 4)
    wk.t.tick(20)
    wk.settle()
    wk.t.tick(30)
    w.removed.add((name, i0))
    return True


def auto_plan(world, first, prefix=None):
    """Goal list that visits everything of an area: the maps in route order, every plaza building (Pokecenter with
    healing, Mart, houses), boss rooms with their item balls, and the gates of lanes."""
    maps = world.maps
    prefix = prefix or re.match(r"[A-Z][a-z]+", first)[0]
    goals = []
    seen = set()

    def add(g):
        if g not in seen or g.split(":")[0] in ("heal", "item", "gate"):
            goals.append(g)
        seen.add(g)

    cur = first
    guard = 0
    gate_next = None
    while cur and guard < 200:
        guard += 1
        gate_next = None
        mp = maps[cur]
        add(cur)
        # gatehouses and doors to other generated maps from this one
        for (x, y, dest, dw) in mp.warps:
            dm = world.consts.get(dest)
            if dm is None or dm.name in seen:
                continue
            n = dm.name
            if not n.startswith(prefix):
                continue
            if "Pokecenter" in n:
                add("heal:" + n)
            elif "Mart" in n or "House" in n:
                add(n)
            elif "Checkpoint" in n or n.endswith("Gate"):
                add(n)
                gate_next = next((world.consts[d].name for (_, _, d, _) in dm.warps
                                  if d in world.consts and world.consts[d].name != cur
                                  and world.consts[d].name.startswith(prefix)), None)
            else:  # a boss room
                m_item = re.search(r"itemball (\w+)", open(os.path.join(ROOT, f"maps/gen/{n}.asm")).read())
                if m_item:
                    add(f"item:{n}={m_item[1]}")
                else:
                    add(n)
                add(cur)
        if any(o["script"].endswith(("GateScript", "BoulderScript")) for o in mp.objects):
            add("gate:" + cur)
        nxt = mp.conns.get("north")
        cur = nxt[0] if nxt and nxt[0] in maps else gate_next
    return goals


def main():
    rom = sys.argv[1]
    goals = sys.argv[2].split(",") if len(sys.argv) > 2 and not sys.argv[2].startswith("auto") else None
    if goals is None and len(sys.argv) > 2:
        goals = auto_plan(World(), sys.argv[2].partition(":")[2] or "TitheRoad")
        print("plan:", ",".join(goals))
    goals = goals or [
        "TitheRoad", "TitheCheckpoint", "TithePlaza1", "TithePokecenter1", "TitheMart1", "TitheHouse1",
        "TitheStreet1", "TitheStreet2", "TitheStreet3", "TithePlaza2", "TithePokecenter2", "TitheMart2", "TitheHouse2"]
    wk = Walker(rom)
    wk.seen_map()
    ok = True
    for g in goals:
        if g.startswith("gate:"):
            res = open_gate(wk, g[5:])
        elif g.startswith("heal:"):
            res = heal(wk, g[5:])
        elif g.startswith("item:"):
            name, _, const = g[5:].partition("=")
            res = wk.go(name) and pick_item(wk, name)
            if res and const and not has_item(wk, item_value(const)):
                wk.note(f"{const} is not in the key item pocket after the pickup")
                res = False
        else:
            res = wk.go(g)
        if not res:
            ok = False
            break
        wk.t.tick(30)
    k = wk.t.mem("wHCKillCount", 0, 2)
    print("kills", k[0] + 256 * k[1], "fights logged", len(wk.fights), "pos", wk.state())
    for f in wk.fights[:8]:
        print("  ", f)
    print("problems:", len(wk.log))
    wk.t.shot(f"{SHOTS}/end.png", 3)
    print("PASS" if ok and not wk.log else "FAIL")
    wk.t.stop()
    sys.exit(0 if ok and not wk.log else 1)


if __name__ == "__main__":
    main()
