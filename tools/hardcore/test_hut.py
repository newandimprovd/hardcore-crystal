#!/usr/bin/env python3
"""Huts (alpha 3.3): a house in a glade of a street, with a room and a dweller who gives an item once.  Stands in front of the door, walks in, talks to the
dweller until the item arrives, and checks that the player is inside the hut, that an item came in (the bag grew) and that the way out leads back to the street.

usage: test_hut.py ROM STREET_CONST DOOR_X DOOR_Y   ROM built like testbuild.sh hut TEST_MAP=<STREET_CONST> TEST_X=<DOOR_X> TEST_Y=<DOOR_Y+1> TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
Prints PASS or FAIL."""
import os
import sys
import faulthandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
faulthandler.dump_traceback_later(400, exit=True)
from gbtest import T  # noqa: E402

rom = sys.argv[1]
t = T(rom)
pb = t.pb
for i in range(600):
    pb.button("a" if i % 2 else "start", 4)
    t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"):
        break
t.tick(200)


def bag_total():
    n = t.mem("wNumItems")
    items = t.mem("wItems", 0, 2 * n + 1) if n else []
    return sum(items[1 + 2 * k] for k in range(n)) if n else 0


bad = []
start = (t.mem("wMapGroup"), t.mem("wMapNumber"), t.mem("wXCoord"), t.mem("wYCoord"))
print("start", start, "bag", bag_total(), flush=True)
for _ in range(2):
    pb.button("up", 8)
    t.tick(40)
inside = (t.mem("wMapGroup"), t.mem("wMapNumber"))
print("after walking up", inside, flush=True)
if inside == start[:2]:
    bad.append("the door did not lead anywhere")
else:
    before = bag_total()
    for _ in range(5):  # up to the dweller, who stands in the way
        pb.button("up", 8)
        t.tick(30)
    after = before
    for _ in range(60):  # the speech is three or four boxes, then the item message
        pb.button("a", 4)
        t.tick(40)
        after = bag_total()
        if after > before:
            break
    for _ in range(3):  # the item message, then what the dweller says afterwards: A moves the text on, B only closes it (A would start the talk again)
        pb.button("a", 4)
        t.tick(60)
    for _ in range(20):
        pb.button("b", 4)
        t.tick(40)
    print("bag", before, "->", after, flush=True)
    if after <= before:
        bad.append("no item was given")
    print("before leaving", t.mem("wXCoord"), t.mem("wYCoord"), flush=True)
    for _ in range(6):
        pb.button("down", 24)
        t.tick(24)
    print("after down", t.mem("wXCoord"), t.mem("wYCoord"), flush=True)
    out = (t.mem("wMapGroup"), t.mem("wMapNumber"))
    print("after walking out", out, flush=True)
    if out != start[:2]:
        bad.append("the way out did not lead back to the street")
print("PASS" if not bad else f"FAIL {bad}")
sys.exit(0 if not bad else 1)
