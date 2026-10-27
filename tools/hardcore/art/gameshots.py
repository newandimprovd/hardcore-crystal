#!/usr/bin/env python3
"""Screenshots from a test ROM: gameshots.py ROM OUTPREFIX "shot u8 shot r4 shot" (u/d/l/r + steps, 'shot' takes a screenshot).
Fights are not handled: use a strong test monster (TEST_MON level 100) and god mode or walk where there are no trainers."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from gbtest import T  # noqa: E402

rom, prefix, script = sys.argv[1], sys.argv[2], sys.argv[3]
t = T(rom)
for i in range(600):
    t.pb.button("a" if i % 2 else "start", 4)
    t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"):
        break
t.tick(200)
n = 0
D = {"u": "up", "d": "down", "l": "left", "r": "right"}
for tok in script.split():
    if tok == "shot":
        n += 1
        t.shot(f"{prefix}_{n}.png", 3)
        print("shot", n, t.where())
    else:
        d, k = D[tok[0]], int(tok[1:] or 1)
        for _ in range(k):
            t.press(d, hold=16, wait=4)
            if t.mem("wScriptRunning") or t.mem("wBattleMode"):
                print("event/battle at", t.where())
                for _ in range(40):
                    t.pb.button("a", 4)
                    t.tick(20)
t.stop()
