#!/usr/bin/env python3
"""The named duels (areas/named.py): the key bearers are mandatory, the rival fights come at their triggers.

usage: test_named.py ROM block|rival
  block  ROM built at TithePlaza1 (verify_all.sh: stA.gbc, walk_all.sh 1: w1.gbc, TEST_ITEMS=0).  The plaza's exit is guarded: stepping onto the
         trigger cells with no CHAINSAW sends the player one step back; talking to Steiner and winning (god mode) hands over the CHAINSAW and
         the exit opens.  Scripted duels are not kills.
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


def kills():
    k = t.mem("wHCKillCount", 0, 2)
    return k[0] + 256 * k[1]


if kind == "block":
    plaza = "TithePlaza1"
    src = open(os.path.join(ROOT, f"maps/gen/{plaza}.asm")).read()
    cells = [(int(a), int(b)) for a, b, lab in re.findall(r"coord_event\s+(\d+),\s*(\d+),\s*-1,\s*(\w+BlockScript)", src)]
    check("the exit has trigger cells", len(cells) >= 2, f"{cells}")
    x, y = cells[len(cells) // 2]
    check("start in the plaza", wk.state()[0] == plaza, f"{wk.state()}")
    check("walk below the exit", wk.go_state(lambda s: s == (plaza, x, y + 1), f"{plaza} below the exit"))
    k0 = kills()
    t.pb.button("up", 9)
    t.tick(30)
    wk.settle()
    t.tick(40)
    st = wk.state()
    check("sent back one step without the CHAINSAW", st == (plaza, x, y + 1), f"{st}")
    check("no CHAINSAW yet", not has_item(wk, item_value("CHAINSAW")))
    t.shot("/home/claude/scratch/named/block.png", 3)
    check("duel with Steiner pays the CHAINSAW", wk.go(plaza) and give(wk, plaza, "CHAINSAW"))
    check("the prize flag is set", flag_get("EVENT_NAMED_STEINER_PAID"))
    check("the Corkboard page is pinned", flag_get("EVENT_LORE_STEINER"))
    check("a scripted duel is not a kill", kills() == k0, f"{k0} -> {kills()}")
    check("walk below the exit again", wk.go_state(lambda s: s == (plaza, x, y + 1), f"{plaza} below the exit"))
    for _ in range(3):
        t.pb.button("up", 9)
        t.tick(30)
        wk.settle()
    t.tick(40)
    st = wk.state()
    check("the exit is open now", st[0] != plaza or st[2] < y, f"{st}")
else:
    st = wk.state()
    check("start on the stem", st[0] == "TitheJunction", f"{st}")
    k0 = kills()
    for _ in range(8):
        t.pb.button("up", 9)
        t.tick(23)
        wk.settle_if_event()
        if flag_get("EVENT_NAMED_RIVAL0_DONE"):
            break
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
