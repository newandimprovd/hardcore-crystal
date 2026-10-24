#!/usr/bin/env python3
"""Whiteout test: touch the first plaza's Pokecenter (sets the respawn point), walk into Tithe Street 1,
lose the next fight on purpose and check that the player wakes up in the plaza with a healed party.
usage: test_whiteout.py ROM   (ROM built like the walker's: testbuild.sh cg1 ...)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_walk import Walker  # noqa: E402

wk = Walker(sys.argv[1])
t = wk.t
for g in ("TithePokecenter1", "TitheStreet1"):
    assert wk.go(g), f"could not reach {g}"
print("in street", wk.state(), "party hp", t.mem("wPartyMon1HP", 0, 2))
wk.die = True
for i in range(4000):
    t.pb.button("up" if i % 40 == 0 and not wk.busy() else "a", 4)
    t.tick(16)
    if wk.state()[0] == "TithePlaza1" and not wk.busy() and i > 100:
        break
t.tick(120)
t.shot("/home/claude/scratch/walk/whiteout.png", 3)
st = wk.state()
hp = t.mem("wPartyMon1HP", 0, 2)
mx = t.mem("wPartyMon1MaxHP", 0, 2)
print("after whiteout", st, "hp", hp, "max", mx)
ok = st[0] == "TithePlaza1" and hp == mx and hp != [0, 0]
print("PASS" if ok else "FAIL")
t.stop()
sys.exit(0 if ok else 1)
