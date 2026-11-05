#!/usr/bin/env python3
"""Cherrygrove -> junction map connection, both ways (the vanilla town joining the generated crossroads).
usage: test_cross.py ROM   ROM = testbuild.sh vc TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=3 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gbtest import T
t = T(sys.argv[1])
shots = os.environ.get("SHOTS", "/home/claude/scratch/feat"); os.makedirs(shots, exist_ok=True)
for i in range(600):
    t.pb.button("a" if i % 2 else "start", 4); t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"): break
t.tick(200)
def busy(): return bool(t.mem("wScriptRunning") or t.mem("wBattleMode"))
def settle():
    quiet = 0
    for _ in range(600):
        if busy():
            quiet = 0; t.pb.button("a", 4); t.tick(16)
        else:
            quiet += 1; t.tick(6)
            if quiet > 6: return
def walk(d, maxn, until):
    for _ in range(maxn):
        t.press(d, hold=16, wait=6)
        if busy(): settle()
        w = t.where()
        if w[0] == 0: print("RESET", flush=True); return None
        if until(w): break
    t.tick(60)
    return t.where()
home = t.where()[:2]
print("start", t.where(), flush=True)
# the exit corridor is x 16..17 wide; Timmy stands at (16, 1) facing east and fights the player at (17, 1)
w1 = walk("up", 12, lambda w: w[:2] != home)
print("north ->", w1, flush=True)
t.shot(f"{shots}/cross_road.png", 2)
w2 = walk("down", 20, lambda w: w[:2] == home) if w1 and w1[:2] != home else None
print("south ->", w2, flush=True)
t.shot(f"{shots}/cross_town.png", 2)
good = bool(w1 and w2 and w1[:2] != home and w2[:2] == home)
print("PASS" if good else "FAIL")
sys.exit(0 if good else 1)
