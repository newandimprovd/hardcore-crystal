#!/usr/bin/env python3
"""Tithe Road -> checkpoint gate hall -> Tithe Plaza 1 and back, on a test ROM spawned at TITHE_ROAD (7, 3).
usage: test_road.py ROM"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gbtest import T
t = T(sys.argv[1])
shots = os.environ.get("SHOTS", "/home/claude/scratch/feat"); os.makedirs(shots, exist_ok=True)
for i in range(600):
    t.pb.button("a" if i % 2 else "start", 4); t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"): break
t.tick(200)
road = t.where()[:2]
print("start", t.where(), flush=True)
def walk(d, maxn, until):
    for _ in range(maxn):
        t.press(d, hold=16, wait=6)
        w = t.where()
        if w[0] == 0: print("RESET", flush=True); return None
        if until(w): break
    t.tick(60)
    return t.where()
w1 = walk("up", 10, lambda w: w[:2] != road)
print("up from road ->", w1, flush=True)
gate = w1[:2] if w1 else None
w2 = walk("up", 12, lambda w: w[:2] != gate) if w1 else None
print("up through gate ->", w2, flush=True)
if w2: t.shot(f"{shots}/plaza_enter.png", 2)
ok = bool(w1 and w2 and w1[:2] != road and w2[:2] != gate and w2[:2] != road)
w3 = walk("up", 4, lambda w: w[:2] == gate) if ok else None
print("back into the hall ->", w3, flush=True)
w4 = walk("down", 12, lambda w: w[:2] == road) if (w3 and w3[:2] == gate) else None
print("down to road ->", w4, flush=True)
if w4: t.shot(f"{shots}/road_back.png", 2)
good = ok and w3 and w4 and w4[:2] == road
print("PASS" if good else "FAIL")
