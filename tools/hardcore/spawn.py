#!/usr/bin/env python3
"""usage: spawn.py MapName [spawn|street|grass]  ->  "MAP_CONST X Y" from spawns.json (written by gen_areas.py).
spawn is the cell below the Pokecenter door, street a floor cell of the main street, grass a cell in the middle of the tall grass."""
import json
import os
import sys

t = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "spawns.json")))
e = t[sys.argv[1]]
mode = sys.argv[2] if len(sys.argv) > 2 else "spawn"
x, y = e["grass"][:2] if mode == "grass" else e["street" if mode == "street" else "spawn"]
print(e["const"], x, y)
