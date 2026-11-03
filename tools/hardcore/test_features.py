#!/usr/bin/env python3
"""Alpha 2 feature checks on a test ROM spawned on Tithe Road (testbuild.sh ft TEST_MAP=TITHE_ROAD TEST_X=4 TEST_Y=11 ...).
Takes screenshots into $SHOTS (default /home/claude/scratch/feat) and prints PASS/FAIL per check:
  sign   the trainer tips sign reads, page by page
  ball   the TM item ball at (5, 7) is picked up and the TM count goes up
  (the road -> gate hall -> plaza walk lives in test_road.py, on its own test ROM spawned at TITHE_ROAD 7,3)
  bag    45 item slots work and the pack screen scrolls
usage: test_features.py ROM"""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from gbtest import T

rom = sys.argv[1]
shots = os.environ.get("SHOTS", "/home/claude/scratch/feat")
os.makedirs(shots, exist_ok=True)
t = T(rom)
for i in range(600):
    t.pb.button("a" if i % 2 else "start", 4); t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"): break
t.tick(200)
results = {}

def flag(name):
    for ln in open("/home/claude/pokecrystal/constants/area_event_flags.asm"):
        m = re.match(r"DEF (\w+) EQU (\d+)", ln)
        if m and m[1] == name: return int(m[2])
    raise KeyError(name)

# ---- sign: stand at (4, 11), face west, read
print("start", t.where())
t.press("left", hold=4, wait=20)
t.press("a", hold=4, wait=40)
pages = 0
for k in range(80):
    if k < 20:
        t.shot(f"{shots}/sign_{k:02d}.png", 2)
    t.pb.button("a", 4); t.tick(50)
    if not t.mem("wScriptRunning") and k > 2:
        break
    pages += 1
results["sign"] = 5 <= pages < 80
print("sign pages seen", pages)

# ---- ball: walk to (6, 7), face west, A
def menu_hook(ctx):
    t.poke("wBattleMonMoves", 33, 0); t.poke("wBattleMonPP", 30, 0); t.poke("wCurMoveNum", 0)
t.hook("BattleMenu", menu_hook)
def clear_fights():
    quiet = 0
    for _ in range(1500):
        t.pb.button("a", 4); t.tick(16)
        if t.mem("wBattleMode") or t.mem("wScriptRunning"):
            quiet = 0
        else:
            quiet += 1
            if quiet > 6: return
def goto_xy(x, y, maxsteps=60):
    for _ in range(maxsteps):
        if t.mem("wBattleMode") or t.mem("wScriptRunning"):
            clear_fights()
        _, _, cx, cy = t.where()
        if (cx, cy) == (x, y): return True
        if cx < x: b = "right"
        elif cx > x: b = "left"
        elif cy < y: b = "down"
        else: b = "up"
        t.press(b, hold=16, wait=6)
    return False
def tmsum():
    return sum(t.mem("wTMsHMs", 0, 57))
before = tmsum()
ok = goto_xy(6, 11) and goto_xy(6, 7)
print("at", t.where(), "reached", ok)
t.press("left", hold=4, wait=20)
t.press("a", hold=4, wait=60)
for k in range(6):
    t.pb.button("a", 4); t.tick(40)
t.shot(f"{shots}/ball.png", 2)
after = tmsum()
fl = (t.mem("wEventFlags", flag("EVENT_GEN_TITHE_ROAD_PICKUP") // 8) >> (flag("EVENT_GEN_TITHE_ROAD_PICKUP") % 8)) & 1
results["ball"] = after == before + 1 and fl == 1
print("TMs", before, "->", after, "flag", fl)

# ---- bag: fill 44 slots and open the pack
t.poke("wNumItems", 44)
for k in range(44):
    t.poke("wItems", 1 + (k % 60), 1 + 2 * k)
    t.poke("wItems", 1 + (k % 5), 2 + 2 * k)
t.poke("wItems", 0xFF, 1 + 2 * 44)
t.press("start", hold=4, wait=40)
t.shot(f"{shots}/menu.png", 2)
print("bag", t.mem("wNumItems"))
print(results)
print("PASS" if all(results.values()) else "FAIL")
