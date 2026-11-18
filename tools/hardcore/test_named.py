#!/usr/bin/env python3
"""The named duels (areas/named.py): the key bearers are mandatory, the rival fights come at their triggers.

usage: test_named.py ROM block|rival
  block  ROM built at TithePlaza1 (verify_all.sh: stA.gbc, walk_all.sh 1: w1.gbc, TEST_ITEMS=0).  Steiner stands in the street and is not
         optional: the first step onto the trigger row below the street mouth starts his talk and the fight (god mode wins), the CHAINSAW is
         handed over, he steps aside and the exit opens.  Scripted duels are not kills.
  rival  ROM built at the Tithe junction (testbuild.sh gt1 TEST_MAP=TITHE_JUNCTION TEST_X=19 TEST_Y=20 ... TEST_ITEMS=0).  Walking north on the
         stem starts the first rival fight, the flag is set and the rival is gone, the kill count did not move.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SHOTS", "/home/claude/scratch/named")
os.environ.setdefault("WALK_GOD", "1")
from test_walk import Walker, give, has_item, item_value  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
rom, kind = sys.argv[1], sys.argv[2]
wk = Walker(rom)
t = wk.t
bad = []


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


def flag_number(name):
    for ln in open(os.path.join(ROOT, "constants/area_event_flags.asm")):
        m = re.match(r"DEF (\w+) EQU (\d+)", ln)
        if m and m[1] == name:
            return int(m[2])
    raise KeyError(name)


def flag_get(name):
    n = flag_number(name)
    return (t.mem("wEventFlags", n // 8) >> (n % 8)) & 1


def species_id(name):
    for ln in open(os.path.join(ROOT, "constants/pokemon_constants.asm")):
        m = re.match(r"\s*const (\w+)\s*; ([0-9A-Fa-f]{2})", ln)
        if m and m[1] == name:
            return int(m[2], 16)
    raise KeyError(name)


def kills():
    k = t.mem("wHCKillCount", 0, 2)
    return k[0] + 256 * k[1]


if kind == "block":
    plaza = "TithePlaza1"
    src = open(os.path.join(ROOT, f"maps/gen/{plaza}.asm")).read()
    trig = sorted((int(a), int(b)) for a, b, lab in re.findall(r"coord_event\s+(\d+),\s*(\d+),\s*-1,\s*(\w+BearerScriptTrigger)", src))
    check("the street mouth has trigger cells", len(trig) >= 4, f"{trig}")
    x, y = trig[0][0] + 1, trig[0][1]
    check("start in the plaza", wk.state()[0] == plaza, f"{wk.state()}")
    # the corridor in front of the street is two cells wide: row y is the trigger row, row y+1 is free, so the approach runs along row y+1
    check("walk to the corridor next to the street mouth", wk.go_state(lambda s: s == (plaza, x - 2, y + 1), f"{plaza} left of the street mouth"))
    wk.press_dir("right")
    wk.press_dir("right")
    check("below the trigger row, no fight yet", wk.state() == (plaza, x, y + 1) and not wk.fights, f"{wk.state()}")
    n0 = len(wk.fights)
    check("no CHAINSAW yet and no fight yet", not has_item(wk, item_value("CHAINSAW")) and not flag_get("EVENT_NAMED_STEINER_DONE"))
    k0 = kills()
    t.shot("/home/claude/scratch/named/block0.png", 3)
    wk.press_dir("up")  # the first step onto the trigger row: Steiner stops the player, talks and fights, nobody asks
    wk.settle()
    t.tick(60)
    wk.settle()
    check("Steiner fought the player without being asked", len(wk.fights) == n0 + 1, f"{wk.fights[n0:]}")
    check("the duel paid the CHAINSAW", has_item(wk, item_value("CHAINSAW")) and flag_get("EVENT_NAMED_STEINER_PAID"))
    check("the Corkboard page is pinned", flag_get("EVENT_LORE_STEINER"))
    check("a scripted duel is not a kill", kills() == k0, f"{k0} -> {kills()}")
    t.shot("/home/claude/scratch/named/block1.png", 3)
    # he steps aside: the street is open and the exit trigger does not send the player back
    st = wk.state()
    check("the player stayed on the road", st[0] == plaza, f"{st}")
    for _ in range(6):
        wk.press_dir("up")
    st = wk.state()
    check("the way out is open now", st[0] != plaza or st[2] < y - 2, f"{st}")
else:
    st = wk.state()
    check("start on the stem", st[0] == "TitheJunction", f"{st}")
    k0 = kills()
    party = None
    for _ in range(8):
        t.pb.button("up", 9)
        for i in range(240):
            t.tick(3)
            if i % 7 == 6 and not t.mem("wBattleMode"):
                t.pb.button("a", 4)  # the rival's lines wait for a button
            if t.mem("wBattleMode") and t.mem("wOTPartyCount"):
                party = [t.mem("wOTPartyMon1Species", i * 48) for i in range(t.mem("wOTPartyCount"))]
                break
        if party:
            t.pb.button("up", 1)
        wk.settle_if_event()
        if flag_get("EVENT_NAMED_RIVAL0_DONE"):
            break
    # the test ROM's player took CYNDAQUIL, so the rival has TOTODILE: it is his last (strongest) mon
    check("the rival's last mon is his starter", party is not None and party[-1] == species_id("TOTODILE"), f"{party}")
    t.tick(60)
    wk.settle()
    check("the rival fight happened", flag_get("EVENT_NAMED_RIVAL0_DONE"))
    check("a scripted duel is not a kill", kills() == k0, f"{k0} -> {kills()}")
    t.shot("/home/claude/scratch/named/rival.png", 3)
    st = wk.state()
    check("the player can walk on", wk.go_state(lambda s: s[0] == "TitheJunction" and s[2] <= 13, "TitheJunction north"), f"{st}")
print("PASS" if not bad else "FAIL: " + ", ".join(bad))
t.stop()
sys.exit(1 if bad else 0)
