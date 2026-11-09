#!/usr/bin/env python3
"""Reachability of the maps: which vanilla maps can the player still get to, and which are dead weight.

An edge exists whenever the source of a map (maps/X.asm, its warp_events and scripts, and its `connection` lines in data/maps/attributes.asm)
names another map constant.  The roots are the start of the game and every map constant that the engine, the data tables or the tests name outside
the map files.  Everything not reachable can be removed (tools/hardcore/remove_baggage.py).
Usage: python3 tools/hardcore/map_reach.py [--list]"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read(p):
    with open(os.path.join(ROOT, p), errors="replace") as f:
        return f.read()


def load():
    consts = re.findall(r"^\s*map_const ([A-Z0-9_]+),", read("constants/map_constants.asm"), re.M)
    attrs = {}  # label -> const
    for lab, c in re.findall(r"^\tmap_attributes (\w+), ([A-Z0-9_]+),", read("data/maps/attributes.asm"), re.M):
        attrs[lab] = c
    return consts, attrs


def edges():
    consts, attrs = load()
    cset = set(consts)
    by_const = {c: l for l, c in attrs.items()}
    tok = re.compile(r"\b([A-Z][A-Z0-9_]{2,})\b")
    graph = {c: set() for c in consts}
    for c in consts:
        lab = by_const.get(c)
        if not lab:
            continue
        p = f"maps/{lab}.asm"
        if os.path.exists(os.path.join(ROOT, p)):
            for m in tok.findall(read(p)):
                if m in cset and m != c:
                    graph[c].add(m)
    # connections live in attributes.asm: the block of one map starts at its map_attributes line
    src = read("data/maps/attributes.asm")
    cur = None
    for line in src.splitlines():
        m = re.match(r"\tmap_attributes (\w+), ([A-Z0-9_]+),", line)
        if m:
            cur = m.group(2)
            continue
        m = re.match(r"\t(?:connection|connections) .*", line)
        if m and cur:
            for t in tok.findall(line):
                if t in cset and t != cur:
                    graph[cur].add(t)
    return consts, attrs, graph


def outside_refs(consts):
    """Map constants named by the engine, the tables and the tests (not by a map file and not by the constant files)."""
    cset = set(consts)
    found = {}
    skip = ("maps/", "constants/map_constants.asm", "constants/area_map_constants.asm", "data/maps/attributes.asm", "data/maps/maps.asm",
            "data/maps/blocks.asm", "data/maps/scripts.asm", "data/maps/scenes.asm", "data/maps/map_data.asm")
    tok = re.compile(r"\b([A-Z][A-Z0-9_]{2,})\b")
    for top in ("engine", "home", "data", "macros", "ram", "constants", "audio", "mobile", "main.asm", "tools/hardcore"):
        base = os.path.join(ROOT, top)
        files = [base] if os.path.isfile(base) else [os.path.join(d, f) for d, _, fs in os.walk(base) for f in fs]
        for fp in files:
            rel = os.path.relpath(fp, ROOT)
            if rel.startswith(skip) or not rel.endswith((".asm", ".py", ".sh")):
                continue
            try:
                s = open(fp, errors="replace").read()
            except OSError:
                continue
            for m in set(tok.findall(s)):
                if m in cset:
                    found.setdefault(m, set()).add(rel)
    return found


def main():
    consts, attrs, graph = edges()
    ext = outside_refs(consts)
    roots = {"PLAYERS_HOUSE_2F"}
    # every generated map is part of the game
    gen = set(re.findall(r"^\s*map_const ([A-Z0-9_]+),", read("constants/area_map_constants.asm"), re.M))
    roots |= gen
    seen, todo = set(), list(roots)
    while todo:
        c = todo.pop()
        if c in seen:
            continue
        seen.add(c)
        todo.extend(graph.get(c, ()))
    dead = [c for c in consts if c not in seen]
    print(f"maps {len(consts)}, generated {len(gen)}, reachable {len(seen)}, unreachable {len(dead)}")
    vanilla_kept = sorted(c for c in seen if c not in gen)
    print("vanilla maps still reachable:", ", ".join(vanilla_kept))
    if "--list" in sys.argv:
        print("unreachable:", ", ".join(dead))
    pinned = {c: sorted(ext[c]) for c in dead if c in ext}
    if pinned:
        print("unreachable but named outside the map files:")
        for c, fs in pinned.items():
            print(f"  {c}: {', '.join(fs[:4])}{' ...' if len(fs) > 4 else ''}")


if __name__ == "__main__":
    main()
