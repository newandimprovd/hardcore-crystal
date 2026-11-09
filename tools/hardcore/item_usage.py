#!/usr/bin/env python3
"""Which items does the game still use?  An item is used when its constant appears anywhere except in its own table rows
(constants, names, descriptions, attributes, the effect table).  Prints the unused ones.  Usage: item_usage.py [--tm]"""
import re, glob, sys
consts = [c for c in re.findall(r"^\s*const (\w+)", open("constants/item_constants.asm").read(), re.M)]
n = consts.index("MASTER_BALL") if "MASTER_BALL" in consts else 0
defs = {"constants/item_constants.asm", "data/items/names.asm", "data/items/descriptions.asm", "data/items/attributes.asm", "engine/items/item_effects.asm"}
words = {}
def add(path, text):
    for w in set(re.findall(r"[A-Z][A-Z0-9_]+", text)):
        words.setdefault(w, set()).add(path)
for f in glob.glob("**/*.asm", recursive=True) + glob.glob("tools/hardcore/**/*.py", recursive=True):
    if f not in defs:
        add(f, open(f, errors="replace").read())
ie = open("engine/items/item_effects.asm").read()
add("item_effects", "\n".join(l for l in ie.splitlines() if not re.match(r"\s*dw \w+\s*; [A-Z0-9_]+\s*$", l)))
# the table rows in attributes use "; NAME" comments only; descriptions and names carry no constants
unused = [c for c in consts if c not in words]
print(len(consts), "constants,", len(unused), "unused")
print(" ".join(unused))
