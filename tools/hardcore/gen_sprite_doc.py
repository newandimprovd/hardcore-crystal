#!/usr/bin/env python3
"""Write docs/SPRITE_STATUS.md: which new species have which kind of picture, and how to hand over sprites.  Idempotent."""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools/hardcore/roster"))
sys.path.insert(0, os.path.join(ROOT, "tools/hardcore/sprites"))
import roster_data as R  # noqa: E402
from recipes import RECIPES  # noqa: E402

out = json.load(open(os.path.join(ROOT, "tools/hardcore/roster/roster_out.json")))
rows = []
for s in out:
    if not s["new"]:
        continue
    nd = R.NEW[s["name"]]
    rec = RECIPES.get(s["name"])
    if nd.get("art") == "cthu":
        st = "own art (hand coded)"
    elif rec and rec.get("import_front"):
        st = "IMPORTED front" + (" and back" if rec.get("import_back") else ", mirrored back placeholder")
    elif rec:
        st = "generated placeholder"
    else:
        st = "reused sprite of " + s["gfx"]
    rows.append((s["id"], s["name"], s["stage"], "/".join(sorted(set(s["types"]))), st, s["gfx"]))
n_imp = sum(1 for r in rows if r[4].startswith("IMPORTED"))
n_gen = sum(1 for r in rows if r[4].startswith("generated"))
n_own = sum(1 for r in rows if r[4].startswith("own"))
n_re = sum(1 for r in rows if r[4].startswith("reused"))
L = ["# Sprite status of the new species", "",
     f"{len(rows)} new species: {n_imp} imported from author sprites, {n_gen} generated placeholders, {n_own} hand coded, {n_re} still reusing a vanilla sprite.", "",
     "## How to hand over a sprite", "",
     "Put the finished front sprite at `tools/hardcore/sprites/imports/<species>.png` (lower case name, for example `typhoneus.png`) and, if you have",
     "it, the back sprite at `imports/<species>_back.png`.  Pixel art at any size is fine (an integer upscale such as 3x is undone), with a transparent",
     "or empty background.  The importer picks two colours from the image, keeps white and black, and shrinks it to the 56x56 front (48x48 back) picture",
     "of the Game Boy Color.  Without a back sprite the front is mirrored as a stand-in.  Palette colours can be overridden in `sprites/recipes.py`.", "",
     "| # | species | stage | types | picture | base sprite |", "|---|---|---|---|---|---|"]
for r in rows:
    L.append("| %d | %s | %d | %s | %s | %s |" % r)
open(os.path.join(ROOT, "docs/SPRITE_STATUS.md"), "w").write("\n".join(L) + "\n")
print(len(rows), "rows;", n_imp, "imported,", n_gen, "generated,", n_own, "own,", n_re, "reused")
