#!/usr/bin/env python3
"""List RAM labels (w..., s..., h...) that no file outside ram/ uses.  Usage: ram_unused.py [prefix-filter]"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAB = re.compile(r"^([wsh][A-Za-z0-9_]*)::?", re.M)
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
def files(top):
    for d, _, fs in os.walk(os.path.join(ROOT, top)):
        for f in fs:
            if f.endswith((".asm", ".inc")):
                yield os.path.join(d, f)
defs = {}
for p in files("ram"):
    for i, l in enumerate(open(p, errors="replace").read().splitlines(), 1):
        m = LAB.match(l)
        if m: defs[m.group(1)] = (os.path.relpath(p, ROOT), i)
used = set()
for top in ("engine", "home", "data", "maps", "macros", "constants", "audio", "gfx", "text", "main.asm", "tools/hardcore/areas"):
    pth = os.path.join(ROOT, top)
    for p in ([pth] if os.path.isfile(pth) else files(top)):
        used.update(WORD.findall(open(p, errors="replace").read()))
# ram files use each other (union members, EQUs): count references inside ram/ other than the definition line
inram = {}
for p in files("ram"):
    for i, l in enumerate(open(p, errors="replace").read().splitlines(), 1):
        if l.lstrip().startswith(";"): continue
        for w in WORD.findall(l):
            if w in defs and not (defs[w] == (os.path.relpath(p, ROOT), i)):
                inram.setdefault(w, 0); inram[w] += 1
flt = sys.argv[1] if len(sys.argv) > 1 else ""
n = 0
for k, (f, i) in sorted(defs.items(), key=lambda kv: kv[1]):
    if k not in used and k.startswith(flt):
        print(f"{f}:{i}\t{k}\t(refs in ram/: {inram.get(k,0)})"); n += 1
print(n, "unused of", len(defs))
