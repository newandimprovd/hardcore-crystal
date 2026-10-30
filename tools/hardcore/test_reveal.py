#!/usr/bin/env python3
"""Stage 3 test: walk into TIMMY in Cherrygrove, win, and check the reveal, kill counter and corpse.
usage: test_reveal.py ROM   (ROM built with: testbuild.sh rv TEST_MAP=CHERRYGROVE_CITY TEST_X=15 TEST_Y=6 ; TIMMY stands at 14,4 and sees 15..18,4)"""
import sys, os
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from gbtest import T

rom = sys.argv[1]
shots = os.environ.get("SHOTS", "/home/claude/scratch/rv")
os.makedirs(shots, exist_ok=True)
t = T(rom)
for i in range(600):
    t.pb.button("a" if i % 2 else "start", 4)
    t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"):
        break
t.tick(200)
print("start", t.where(), "revealed flag", end=" ")
# event flag check: read EVENT_KILLER_REVEALED bit through wEventFlags
import re
consts = {}
for ln in open("/home/claude/pokecrystal/constants/event_flags.asm"):
    pass

def flag(name):
    # compute index by counting 'const' lines before the name
    n = 0
    for ln in open("/home/claude/pokecrystal/constants/event_flags.asm"):
        m = re.match(r"\s*const (\w+)", ln)
        if m:
            if m[1] == name:
                return n
            n += 1
        m2 = re.match(r"\s*const_next (\d+)", ln)
        if m2:
            n = int(m2[1])
    raise KeyError(name)

def getflag(name):
    i = flag(name)
    return (t.mem("wEventFlags", i // 8) >> (i % 8)) & 1

print(getflag("EVENT_KILLER_REVEALED"))
t.shot(f"{shots}/0_start.png", 2)
kills0 = t.mem("wHCKillCount", 0, 2)
# walk north until the trainer spots us
for k in range(8):
    t.press("up", hold=16, wait=4)
    if t.mem("wBattleMode") or t.mem("wScriptRunning"):
        break
print("after walking", t.where())
def menu_hook(ctx):
    t.poke("wBattleMonMoves", 33, 0)   # TACKLE in slot 1 so the fight ends quickly
    t.poke("wBattleMonPP", 30, 0)
    t.poke("wCurMoveNum", 0)
t.hook("BattleMenu", menu_hook)
n = 0
phase = "overworld"
last = None
seen_battle = False
for i in range(3000):
    t.pb.button("a", 4)
    t.tick(16)
    bm = t.mem("wBattleMode")
    if bm:
        seen_battle = True
    if i % 25 == 0:
        t.shot(f"{shots}/f{i:04d}.png", 2)
    if seen_battle and not bm and getflag("EVENT_BEAT_YOUNGSTER_TIMMY") and not t.mem("wScriptRunning") and i > 100:
        n += 1
        if n > 40:
            break
print("battle seen", seen_battle, "beat timmy", getflag("EVENT_BEAT_YOUNGSTER_TIMMY"), "revealed", getflag("EVENT_KILLER_REVEALED"),
      "pending", getflag("EVENT_HC_REVEAL_PENDING"), "kills", t.mem("wHCKillCount", 0, 2), "pos", t.where())
t.shot(f"{shots}/9_end.png", 3)
ok = seen_battle and getflag("EVENT_KILLER_REVEALED") and not getflag("EVENT_HC_REVEAL_PENDING") and t.mem("wHCKillCount", 0, 2) == [1, 0]
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
