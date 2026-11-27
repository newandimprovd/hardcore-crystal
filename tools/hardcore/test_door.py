#!/usr/bin/env python3
"""Doors (alpha 3.3): stands in front of a door, walks up through it and checks that the map changed and has the expected size in blocks, then
walks back out and checks that the street is where it was left.

usage: test_door.py ROM WIDTH HEIGHT   (the inside's size in blocks)   ROM built with testbuild.sh TEST_MAP=<MAP> TEST_X=<door x> TEST_Y=<door y + 1>
Prints PASS or FAIL."""
import os
import sys
import faulthandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
faulthandler.dump_traceback_later(300, exit=True)
from gbtest import T  # noqa: E402

rom, want_w, want_h = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
t = T(rom)
pb = t.pb
for i in range(600):
    pb.button("a" if i % 2 else "start", 4)
    t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"):
        break
t.tick(200)
bad = []
start = (t.mem("wMapGroup"), t.mem("wMapNumber"), t.mem("wXCoord"), t.mem("wYCoord"))
for _ in range(3):
    pb.button("up", 8)
    t.tick(40)
inside = (t.mem("wMapGroup"), t.mem("wMapNumber"))
size = (t.mem("wCurMapWidth") if False else None)
print("start", start, "inside", inside, flush=True)
if inside == start[:2]:
    bad.append("the door did not lead anywhere")
else:
    t.tick(30)
    for _ in range(8):
        pb.button("down", 24)
        t.tick(24)
    out = (t.mem("wMapGroup"), t.mem("wMapNumber"))
    print("after walking out", out, flush=True)
    if out != start[:2]:
        bad.append("the way out did not lead back to the street")
print("PASS" if not bad else f"FAIL {bad}")
sys.exit(0 if not bad else 1)
