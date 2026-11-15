#!/usr/bin/env python3
"""Opens the Pokegear map card of a test ROM (testbuild.sh sets the #GEAR and the map card) and takes a picture of every landmark the cursor
visits: the first picture is where the player stands, then Up walks forward through the page's landmarks until it wraps.
usage: test_worldmap.py ROM OUTDIR [MAX_STEPS]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gbtest import T  # noqa: E402

rom, out = sys.argv[1], sys.argv[2]
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
os.makedirs(out, exist_ok=True)
t = T(rom)
for i in range(600):  # past the title screen: the test ROM starts a new game on its own
    t.pb.button("a" if i % 2 else "start", 4)
    t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"):
        break
t.tick(240)
# the start menu: POKEDEX, POKEMON, PACK, #GEAR ...
t.press("start", hold=4, wait=30)
for _ in range(3):
    t.press("down", hold=4, wait=16)
t.press("a", hold=4, wait=60)
t.press("right", hold=4, wait=60)  # clock card -> map card
t.shot(f"{out}/m00.png", 3)
seen = []
for i in range(1, steps):
    t.press("up", hold=4, wait=10)
    lm = t.mem("wPokegearMapCursorLandmark")
    if lm in seen:
        print("wrapped at step", i)
        break
    seen.append(lm)
    t.shot(f"{out}/m{i:02d}.png", 3)
print("landmarks visited:", seen)
print("player landmark:", t.mem("wPokegearMapPlayerIconLandmark"))
t.stop()
