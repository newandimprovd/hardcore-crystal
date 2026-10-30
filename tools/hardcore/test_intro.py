#!/usr/bin/env python3
"""Smoke test of the real game start on the real (non-test) ROM: new game, intro, bedroom, Mom, New Bark Town, Elm's lab and the
starter, Route 29, Cherrygrove, the rival and the first fight (TIMMY, the reveal).

usage: test_intro.py ROM [last_step]       (steps: 0 intro, 1 house, 2 Elm and starter, 3 Route 29, 4 Cherrygrove, 5 Timmy)
The test needs only the ROM.  It drives the real intro with the A button and walks the vanilla maps with the area model's collision
data (areamodel.World plus the vanilla early maps).  Battles are helped along: the player's Pokemon gets TACKLE and a lot of HP, the
enemy's HP is set to 1, so the test is about scripts and flow, not about balance.  TRACE=1 prints every step.
Screenshots go to $SHOTS (default /home/claude/scratch/intro)."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gbtest import T  # noqa: E402
from areamodel import Map, World  # noqa: E402
from test_walk import const_table  # noqa: E402

SHOTS = os.environ.get("SHOTS", "/home/claude/scratch/intro")
os.makedirs(SHOTS, exist_ok=True)
TRACE = bool(os.environ.get("TRACE"))

# name -> (tileset, width in blocks, map constant)
VANILLA = {
    "PlayersHouse2F": ("TILESET_PLAYERS_ROOM", 4, "PLAYERS_HOUSE_2F"),
    "PlayersHouse1F": ("TILESET_PLAYERS_HOUSE", 5, "PLAYERS_HOUSE_1F"),
    "NewBarkTown": ("TILESET_JOHTO", 10, "NEW_BARK_TOWN"),
    "ElmsLab": ("TILESET_LAB", 5, "ELMS_LAB"),
    "Route29": ("TILESET_JOHTO", 30, "ROUTE_29"),
}
IDS = {(24, 7): "PlayersHouse2F", (24, 6): "PlayersHouse1F", (24, 4): "NewBarkTown", (24, 5): "ElmsLab",
       (24, 3): "Route29", (26, 3): "CherrygroveCity"}


def event_index(name):
    n = 0
    for ln in open(os.path.join(HERE, "..", "..", "constants", "event_flags.asm")):
        m = re.match(r"\s*const (\w+)", ln)
        if m:
            if m[1] == name:
                return n
            n += 1
        m2 = re.match(r"\s*const_next (\d+)", ln)
        if m2:
            n = int(m2[1])
    raise KeyError(name)


def build_world():
    w = World()
    for n, (ts, wd, const) in VANILLA.items():
        m = Map(n, ts, wd, f"maps/{n}.blk", f"maps/{n}.asm")
        m.const = const
        w.maps[n] = m
        w.consts[const] = m
    w.consts["CHERRYGROVE_CITY"] = w.maps["CherrygroveCity"]
    w.maps["NewBarkTown"].conns["west"] = ("Route29", 0)
    w.maps["Route29"].conns["east"] = ("NewBarkTown", 0)
    w.maps["Route29"].conns["west"] = ("CherrygroveCity", 0)
    w.maps["CherrygroveCity"].conns["east"] = ("Route29", 0)
    return w


class Run:
    def __init__(self, rom):
        self.t = T(rom)
        self.world = build_world()
        self.species = {}
        for k, v in const_table("constants/pokemon_constants.asm").items():
            self.species.setdefault(v, k)
        self.fights = 0
        self.t.hook("BattleMenu", self.battle_menu)

    # -- helpers
    def say(self, *a):
        print(" ".join(str(x) for x in a))

    def shot(self, name):
        self.t.shot(os.path.join(SHOTS, f"{name}.png"), 2)

    def where(self):
        g, n, x, y = self.t.where()
        return IDS.get((g, n), f"?{g}:{n}"), x, y

    def flag(self, name):
        i = event_index(name)
        return (self.t.mem("wEventFlags", i // 8) >> (i % 8)) & 1

    def kills(self):
        lo, hi = self.t.mem("wHCKillCount", 0, 2)
        return lo + 256 * hi

    def party(self):
        n = self.t.mem("wPartyCount")
        return [self.species.get(self.t.mem("wPartySpecies", i), "?") for i in range(n)]

    def busy(self):
        return bool(self.t.mem("wScriptRunning")) or bool(self.t.mem("wBattleMode"))

    def battle_menu(self, ctx):
        """Hook at the battle menu: TACKLE in the first slot, lots of HP for us, 1 HP for them."""
        t = self.t
        if t.mem("wBattleType") != 0:  # the catching tutorial and friends run themselves
            return
        t.poke("wBattleMonMoves", 33, 0)
        t.poke("wBattleMonPP", 30, 0)
        t.poke("wCurMoveNum", 0)
        t.poke("wBattleMonHP", 1, 0)  # big endian
        t.poke("wBattleMonHP", 255, 1)
        t.poke("wEnemyMonHP", 0, 0)
        t.poke("wEnemyMonHP", 1, 1)
        t.poke("wPlayerAccLevel", 13)
        self.fights += 1

    def mash(self, frames=3000):
        """Press A (B once there is a party: the nickname question says NO to B) while a script or a battle runs."""
        free = 0
        t = self.t
        for _ in range(frames // 20):
            if self.busy():
                free = 0
                t.pb.button("b" if t.mem("wPartyCount") and not t.mem("wBattleMode") else "a", 3)
            else:
                free += 1
                if free >= 4:
                    return True
            t.tick(20)
        return not self.busy()

    def step(self, d):
        t = self.t
        before = t.where()
        t.pb.button(d, 12)
        t.tick(30)
        for _ in range(10):
            if not t.mem("wScriptRunning"):
                break
            t.tick(10)
        if TRACE:
            print("   step", d, before, "->", t.where(), "script", t.mem("wScriptRunning"))
        return t.where() != before

    def goto(self, goal_fn, label="", maxiter=60):
        """Walk (BFS over the model, replanning whenever reality differs) until goal_fn(state) holds."""
        w = self.world
        for it in range(maxiter):
            st = self.where()
            if st[0].startswith("?"):
                self.say(f"!! unknown map {st}")
                return False
            if goal_fn(st):
                return True
            route = w.route(st, goal_fn) or w.route(st, goal_fn, ignore_obj=True)
            if route is None:
                self.say(f"!! no route from {st} ({label})")
                return False
            for d, exp, kind in route:
                self.step(d)
                if self.busy():
                    self.mash()
                now = self.where()
                if goal_fn(now):
                    return True
                if now != exp:
                    break
        self.say(f"!! gave up at {self.where()} ({label})")
        return False

    def at(self, name, x, y):
        return lambda s: s == (name, x, y)

    def in_map(self, name):
        return lambda s: s[0] == name


def intro(r):
    t = r.t
    r.say("boot, title, new game, Oak's intro with A")
    for i in range(400):
        if i % 40 == 20:
            t.pb.button("start", 3)
        t.tick(1)
    for i in range(1200):
        t.pb.button("a", 3)
        t.tick(20)
        if r.where()[0] == "PlayersHouse2F" and i > 50:
            break
    r.mash(1200)
    r.shot("00_bedroom")
    return r.where()[0] == "PlayersHouse2F"


def house(r):
    ok = r.goto(r.in_map("NewBarkTown"), "house")
    r.mash(600)
    r.say("out of the house:", r.where())
    r.shot("01_newbark")
    return ok and r.where()[0] == "NewBarkTown"


def elm(r):
    t = r.t
    if not r.goto(r.in_map("ElmsLab"), "to the lab"):
        return False
    r.mash()
    r.shot("02_lab")
    if not r.goto(r.at("ElmsLab", 6, 4), "to the balls"):
        return False
    t.press("up", hold=12, wait=20)
    for _ in range(4):
        t.press("a", hold=4, wait=30)
        if r.busy():
            break
    r.mash(4000)
    party = r.party()
    r.say("party:", party, "at", r.where())
    r.shot("03_starter")
    if len(party) != 1:
        return False
    # Elm's talk, the aide's potion, the officer: walk out into New Bark Town
    if not r.goto(lambda s: s[0] == "NewBarkTown", "out of the lab"):
        return False
    r.mash(1200)
    r.say("out of the lab:", r.where())
    return r.where()[0] == "NewBarkTown"


def route29(r):
    if not r.goto(r.in_map("Route29"), "to Route 29"):
        return False
    r.mash(800)
    r.shot("04_route29")
    # across the catching tutorial at x=53
    if not r.goto(lambda s: s[0] == "Route29" and s[1] < 45, "past the tutorial"):
        return False
    r.mash(2000)
    r.say("route 29:", r.where())
    return r.where()[0] == "Route29"


def cherrygrove(r):
    if not r.goto(r.in_map("CherrygroveCity"), "to Cherrygrove"):
        return False
    r.mash(3000)
    r.say("in Cherrygrove:", r.where(), "fights so far", r.fights, "kills", r.kills())
    r.shot("05_cherrygrove")
    return r.where()[0] == "CherrygroveCity"


def timmy(r):
    # the rival scene and the Guide Gent hold the player at the east gate; walk on to the trainer's line of sight
    # TIMMY stands at (14, 4) facing east and sees (15..18, 4)
    if not r.goto(lambda s: s[0] == "CherrygroveCity" and s[2] == 4 and 15 <= s[1] <= 18, "toward Timmy"):
        return False
    r.mash(4000)
    r.say("after the first fight:", r.where(), "timmy", r.flag("EVENT_BEAT_YOUNGSTER_TIMMY"), "revealed",
          r.flag("EVENT_KILLER_REVEALED"), "kills", r.kills(), "fights", r.fights)
    r.shot("06_timmy")
    return bool(r.flag("EVENT_BEAT_YOUNGSTER_TIMMY")) and bool(r.flag("EVENT_KILLER_REVEALED")) and r.kills() == 1


def main():
    rom = sys.argv[1]
    last = int(sys.argv[2]) if len(sys.argv) > 2 else 99
    r = Run(rom)
    steps = [("intro", intro), ("house", house), ("Elm and the starter", elm), ("Route 29", route29),
             ("Cherrygrove", cherrygrove), ("Timmy", timmy)]
    for i, (name, fn) in enumerate(steps):
        if i > last:
            break
        r.say(f"== step {i}: {name}")
        ok = fn(r)
        r.say(f"   {'OK' if ok else 'FAIL'} at {r.where()}")
        if not ok:
            r.shot(f"fail_{i}")
            print("FAIL")
            return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
