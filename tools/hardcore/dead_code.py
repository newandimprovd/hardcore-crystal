#!/usr/bin/env python3
"""Dead file finder: lists the assembly files of the ROM whose global labels nothing outside the file uses.

A file is live when it holds a root (home code, audio, the maps that are left, the hardcore engine) or when one of its global labels (Name: or Name::)
occurs as a word in a live file.  Everything else is dead, cycles included (the phone and the radio call each other).  Textual references are
enough here: farcall, call, jp, dw and the table macros all name their target.  Files that only hold constants or macros are not looked at, and neither are the top level files.
Usage: python3 tools/hardcore/dead_code.py [--delete] [--prefix engine/phone]       (without --delete it only reports)"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def _tops():
    """The files that make one object each (rom_obj in the Makefile)."""
    m = re.search(r"rom_obj := \\\n((?:\t\S+\.o ?\\?\n?)+)", open(os.path.join(ROOT, "Makefile")).read())
    return [o.replace(".o", ".asm") for o in re.findall(r"(\S+\.o)", m.group(1))]


TOP = _tops()
INC = re.compile(r'^\s*INCLUDE\s+"([^"]+)"', re.M)
LABEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?(?!\w)", re.M)
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def read(p):
    with open(os.path.join(ROOT, p), errors="replace") as f:
        return f.read()


def tree():
    """All source files reachable through INCLUDE from the top level files (ROM code and data, plus ram.asm)."""
    seen, todo = {}, list(TOP)
    while todo:
        p = todo.pop()
        if p in seen or not os.path.exists(os.path.join(ROOT, p)):
            continue
        seen[p] = read(p)
        for inc in INC.findall(seen[p]):
            todo.append(inc)
    return seen


def roots(files):
    """Files that are live because the game starts there: home code, audio, the maps that are left, the hardcore engine and the map tables."""
    r = set()
    for p in files:
        if p.startswith(("home/", "maps/", "data/maps/", "engine/hardcore/", "audio/engine", "audio/")) or p in TOP:
            r.add(p)
    return r


def analyse(files, prefix=None):
    labels = {p: set(LABEL.findall(s)) for p, s in files.items() if p not in TOP}
    words = {p: set(WORD.findall(s)) for p, s in files.items()}
    owner = {}
    for p, ls in labels.items():
        for l in ls:
            owner.setdefault(l, set()).add(p)
    live = set(roots(files))
    todo = list(live)
    while todo:
        p = todo.pop()
        for w in words[p]:
            for q in owner.get(w, ()):
                if q not in live:
                    live.add(q)
                    todo.append(q)
    dead = [p for p in sorted(files) if p not in live and labels.get(p) and (not prefix or p.startswith(prefix))
            and not p.startswith(("constants/", "macros/", "ram/"))]
    return dead, labels


def main():
    files = tree()
    prefix = None
    if "--prefix" in sys.argv:
        prefix = sys.argv[sys.argv.index("--prefix") + 1]
    dead, labels = analyse(files, prefix)
    size = 0
    for p in dead:
        n = os.path.getsize(os.path.join(ROOT, p))
        size += n
        print(f"{p}  ({n} bytes of source, {len(labels[p])} labels)")
    print(f"{len(dead)} dead files, {size} bytes of source")
    if "--delete" in sys.argv:
        for p in dead:
            os.remove(os.path.join(ROOT, p))
        # drop the INCLUDE lines that name them
        gone = set(dead)
        for p in list(files):
            if p in gone:
                continue
            s = files[p]
            t = "".join(l for l in s.splitlines(keepends=True)
                        if not (m := re.match(r'\s*INCLUDE\s+"([^"]+)"', l)) or m.group(1) not in gone)
            if t != s:
                with open(os.path.join(ROOT, p), "w") as f:
                    f.write(t)
        print("deleted, includes removed")


if __name__ == "__main__":
    main()
