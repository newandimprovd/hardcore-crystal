#!/usr/bin/env python3
"""Pack check on any test ROM: fill 45 item slots, open START > PACK, scroll to the end, screenshots to $SHOTS.
usage: test_pack.py ROM"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gbtest import T
t = T(sys.argv[1])
shots = os.environ.get("SHOTS", "/home/claude/scratch/feat"); os.makedirs(shots, exist_ok=True)
for i in range(600):
    t.pb.button("a" if i % 2 else "start", 4); t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"): break
t.tick(200)
N = 45
t.poke("wNumItems", N)
for k in range(N):
    t.poke("wItems", 1 + (k % 60), 1 + 2 * k)   # item ids 1..60 (some are not valid pack items; ok for scrolling)
    t.poke("wItems", 1 + (k % 5), 2 + 2 * k)
t.poke("wItems", 0xFF, 1 + 2 * N)
t.press("start", hold=4, wait=30)
t.press("down", hold=4, wait=8); t.press("down", hold=4, wait=8)
t.press("a", hold=4, wait=40)
t.shot(f"{shots}/pack_top.png", 2)
for k in range(N + 2):
    t.press("down", hold=4, wait=6)
t.tick(20)
t.shot(f"{shots}/pack_bottom.png", 2)
print("numitems", t.mem("wNumItems"), "cursor", t.mem("wItemsPocketCursor") if "wItemsPocketCursor" in t.sym else "?",
      "scroll", t.mem("wItemsPocketScrollPosition") if "wItemsPocketScrollPosition" in t.sym else "?")
print("alive", t.where())
