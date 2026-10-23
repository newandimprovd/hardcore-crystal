#!/usr/bin/env python3
"""Open the Pokedex in a test ROM with every species seen and screenshot the entry pages of the
given species (dex order = line order).  usage: dexshots.py ROM OUTDIR NAME [NAME ...]"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gbtest import T

rom, outdir, names = sys.argv[1], sys.argv[2], sys.argv[3:]
root = __file__.rsplit("/tools/", 1)[0]
exp = json.load(open(root + "/tools/hardcore/roster/roster_out.json"))
import importlib.util
spec = importlib.util.spec_from_file_location("R", root + "/tools/hardcore/roster/roster_data.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
order = [s[1:] if s.startswith("*") else s for _, st in R.LINES for s in st]
os.makedirs(outdir, exist_ok=True)
t = T(rom)
for i in range(600):
    t.pb.button("a" if i % 2 else "start", 4); t.tick(20)
    if t.mem("wMapGroup") and t.mem("wXCoord"): break
t.tick(120)
for i in range(32):
    t.poke("wPokedexSeen", 0xFF, i); t.poke("wPokedexCaught", 0xFF, i)
t.press("start", hold=4, wait=60)
t.press("a", hold=4, wait=60)
t.press("a", hold=4, wait=80)
def cur_index():
    return t.mem("wDexListingScrollOffset") + t.mem("wDexListingCursor")

def species_at(i):
    return t.mem("wPokedexOrder", i)

for nm in names:
    want = next(r["id"] for r in exp if r["const"] == nm)
    guard = 0
    while species_at(cur_index()) != want and guard < 400:
        guard += 1
        # find where the wanted species sits in the displayed order
        tgt = next(i for i in range(248) if species_at(i) == want)
        d = tgt - cur_index()
        if d >= 7:
            t.press("right", hold=2, wait=8)
        elif d > 0:
            t.press("down", hold=2, wait=6)
        elif d <= -7:
            t.press("left", hold=2, wait=8)
        else:
            t.press("up", hold=2, wait=6)
    t.tick(40)
    print(nm, "selected", species_at(cur_index()), "want", want)
    t.press("a", hold=4, wait=120)
    t.shot(f"{outdir}/{nm}_1.png", 3)
    t.press("a", hold=4, wait=60)   # next page of text
    t.tick(60)
    t.shot(f"{outdir}/{nm}_2.png", 3)
    t.press("b", hold=4, wait=60)
    t.tick(30)
t.stop()
