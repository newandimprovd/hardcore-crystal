#!/usr/bin/env python3
"""List (or delete) source/asset files the crystal11 ROM never reads.  rgbasm -M gives the exact include/INCBIN set of every object
(macro-pasted INCLUDEs included), so a file is unused when no object lists it and, for assets, no listed INCBIN has the same stem
(gfx/a/b.png <-> gfx/a/b.2bpp.lz).  Usage: unref_asm.py [--delete] [--assets]"""
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
RGBASM = os.path.join(os.environ.get("RGBDS", "/home/claude/bin/"), "rgbasm") if os.path.exists("/home/claude/bin/rgbasm") else "rgbasm"
mk = open("Makefile").read()
blk = mk[mk.index("rom_obj := "):mk.index("pokecrystal_obj")]
roots = [o[:-2] + ".asm" for o in re.findall(r"(\S+\.o)", blk)]
used = set()
for r in roots:
    d = "/tmp/_unref.d"
    subprocess.run([RGBASM, "-D", "_CRYSTAL11", "-Q8", "-P", "includes.asm", "-M", d, "-o", "/tmp/_unref.o", r],
                   check=True, capture_output=True)
    t = open(d).read().replace("\\\n", " ")
    for tok in t.split(":", 1)[1].split():
        used.add(os.path.normpath(tok))
    for tok in t.split():
        pass
incstems = set()
ASSET = (".png", ".2bpp", ".1bpp", ".lz", ".pal", ".tilemap", ".bin", ".attrmap", ".blk", ".rle", ".gbcpal", ".bit")
def stem(p):
    while True:
        s2, ext = os.path.splitext(p)
        if ext in ASSET or ext == ".animated": p = s2
        else: return p
for u in used:
    if u.endswith(ASSET): incstems.add(stem(u))
tracked = set(os.path.normpath(x) for x in subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split("\n") if x)
dead = []
BUILD_FILES = {"rgbdscheck.asm", "test_config.asm", "includes.asm"}   # named by the Makefile / test harness, not by an INCLUDE
for d, ds, fs in os.walk("."):
    ds[:] = [x for x in ds if x not in (".git", "tools", "scratch", "__pycache__", "docs")]
    for f in fs:
        p = os.path.normpath(os.path.join(d, f))
        if p in BUILD_FILES or p.startswith("vc" + os.sep): continue
        if p not in tracked: continue          # build products (.2bpp, .lz ...) are made from the tracked sources
        if f.endswith((".asm", ".inc")) and p not in used and p != "includes.asm":
            dead.append(p)
        elif "--assets" in sys.argv and f.endswith(ASSET) and stem(p) not in incstems and p not in used:
            dead.append(p)
dead.sort(key=lambda p: -os.path.getsize(p))
for p in dead[:200]: print(f"{os.path.getsize(p):8d} {p}")
print(len(roots), "objects,", len(used), "files read,", len(dead), "unused (", sum(os.path.getsize(p) for p in dead) // 1024, "KB )")
if "--delete" in sys.argv:
    for p in dead: os.remove(p)
    print("deleted")
