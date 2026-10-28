#!/usr/bin/env python3
"""Builds the area tilesets (tools/hardcore/art/<area>.py), writes their files and registers them.
Run before gen_areas.py (the kits read the collision tables written here)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art  # noqa: E402,F401
import register  # noqa: E402
import tithe  # noqa: E402
import grove  # noqa: E402
import axiom  # noqa: E402
import lotus  # noqa: E402
import disart  # noqa: E402


def build_all():
    sets = []
    for mod in (tithe, grove, axiom, lotus, disart):
        t = mod.build().pack()
        t.write()
        print(f"{t.name}: {t.used} tiles, {len(t.blocks)} blocks")
        sets.append(t)
    register.register(sets)
    return sets


if __name__ == "__main__":
    build_all()
