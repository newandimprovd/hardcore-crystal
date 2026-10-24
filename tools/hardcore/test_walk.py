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
        t.hook("BattleMenu", self.menu_hook)

    # ------------------------------------------------------------------ helpers
    def menu_hook(self, ctx):
        t = self.t
        t.poke("wBattleMonMoves", 33, 0)
        t.poke("wBattleMonPP", 30, 0)
        t.poke("wCurMoveNum", 0)
        if not self.battle_seen:
            self.battle_seen = True
            n = t.mem("wOTPartyCount")
            self.fights.append(dict(cls=t.mem("wTempTrainerClass"), id=t.mem("wTempTrainerID"), n=n,
                                    party=t.mem("wOTPartySpecies", 0, max(n, 1)), lvl=t.mem("wEnemyMonLevel"),
                                    at=self.state()))

    def state(self):
        t = self.t
        g, n, x, y = t.where()
        return (self.ids.get((g, n), f"?{g}:{n}"), x, y)

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
        for attempt in range(2):
            t.pb.button(d, 9)
            t.tick(9 + 12)
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
        w = self.w
        print(f"-> {goal_map}")
        replans = 0
        while replans < max_replans:
            cur = self.state()
            if cur[0] == goal_map:
                return True
            if cur[0] not in w.maps:
                self.note(f"unknown map {cur}")
                return False
            path = w.route(cur, lambda s: s[0] == goal_map)
            if path is None:
                path = w.route(cur, lambda s: s[0] == goal_map, ignore_obj=True)
            if path is None:
                self.note(f"no model route from {cur} to {goal_map}")
                return False
            replans += 1
            for (d, exp, kind) in path:
                before = self.state()
                self.press_dir(d)
                self.seen_map()
                actual = self.state()
                if actual == exp:
                    continue
                if kind in ("warp", "conn") and actual[0] == exp[0]:
                    if actual != exp:
                        self.note(f"{kind} {before}->{exp[0]} landed {actual[1:]} expected {exp[1:]}")
                    break
                if actual == before:
                    self.note(f"blocked: {before} {d} (expected {exp}, {kind}); marking")
                    w.blocked.add(exp)
                elif actual[0] != before[0] or abs(actual[1] - before[1]) + abs(actual[2] - before[2]) > 1:
                    self.note(f"unexpected position {actual} after {d} from {before}, expected {exp}")
                break
        self.note(f"gave up on {goal_map}")
        return False


def main():
    rom = sys.argv[1]
    goals = sys.argv[2].split(",") if len(sys.argv) > 2 else [
        "TitheRoad", "TitheCheckpoint", "TithePlaza1", "TithePokecenter1", "TitheMart1", "TitheHouse1",
        "TitheStreet1", "TitheStreet2", "TitheStreet3", "TithePlaza2", "TithePokecenter2", "TitheMart2", "TitheHouse2"]
    wk = Walker(rom)
    wk.seen_map()
    ok = True
    for g in goals:
        if not wk.go(g):
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
