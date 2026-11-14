#!/usr/bin/env python3
"""Gate transitions keep their heading: the way out of a map is the opposite side of the way into the next one.

Two ROMs (god mode walker, areamodel plans over the emitted maps):
  road:  testbuild.sh gt1 TEST_MAP=TITHE_JUNCTION TEST_X=19 TEST_Y=20 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1
         Junction -> Tithe Road -> checkpoint gate hall -> Tithe Plaza 1: you arrive on the mat at the plaza's south edge, facing north;
         walking back south onto the mat puts you at the top of the hall, facing south.
  area:  testbuild.sh gt2 TEST_MAP=TITHE_CATHEDRAL TEST_X=4 TEST_Y=6 ... (the last boss room of Area 1)
         boss room -> Grove gate hall -> Grove Plaza 1: same rule.
usage: test_gates.py ROM road|area"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SHOTS", "/home/claude/scratch/gates")
os.environ.setdefault("WALK_GOD", "1")
from test_walk import Walker  # noqa: E402

FACING = {0x00: "south", 0x04: "north", 0x08: "west", 0x0C: "east"}
rom, kind = sys.argv[1], sys.argv[2]
wk = Walker(rom)
t = wk.t
bad = []


def facing():
    return FACING.get(t.mem("wPlayerDirection") & 0x0C, "?")


def check(label, ok, info=""):
    print(("ok   " if ok else "FAIL ") + label, info, flush=True)
    if not ok:
        bad.append(label)


if kind == "road":
    first, hall, plaza, back = "TitheRoad", "TitheCheckpoint", "TithePlaza1", "TitheRoad"
else:
    first, hall, plaza, back = None, "GroveGate", "GrovePlaza1", None
if first:
    check(f"reach {first}", wk.go(first))
check(f"reach {hall}", wk.go(hall))
st = wk.state()
check("hall entered heading north", facing() == "north", f"{st} facing {facing()}")
check(f"reach {plaza}", wk.go(plaza))
st = wk.state()
t.tick(30)
h = wk.t.mem("wMapGroup"), wk.t.mem("wMapNumber")
mx, my = st[1], st[2]
check("arrived at the south edge of the plaza", my >= 2 * 12 and st[0] == plaza, f"{st}")
check("arrived facing north", facing() == "north", facing())
t.shot("/home/claude/scratch/gates/%s_arrival.png" % kind, 3)
# walk back south onto the mat and off the south edge
t.press("up", hold=16, wait=6)
t.press("down", hold=16, wait=6)  # onto the mat
t.press("down", hold=16, wait=6)  # a directional carpet fires when you walk on in its direction
wk.t.tick(60)
st2 = wk.state()
check("south onto the mat leads back into the hall", st2[0] == hall, f"{st2}")
check("back in the hall facing south", facing() == "south", facing())
t.shot("/home/claude/scratch/gates/%s_back.png" % kind, 3)
print("PASS" if not bad else "FAIL: " + ", ".join(bad))
t.stop()
sys.exit(1 if bad else 0)
