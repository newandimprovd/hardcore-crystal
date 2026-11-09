#!/usr/bin/env python3
"""Delete data blocks (text, small tables) whose label nothing mentions any more.
A label counts as used when its name appears anywhere else in the .asm/.link/.py files (macro-pasted names such as \\1Frontpic are
therefore NOT touched: only the directories given are scanned, default data/text data/items data/events data/battle).
Block = label line up to the first blank line; a label directly followed by another label only loses its own line.
Usage: dead_data.py [--delete] [dir ...]"""
import os, re, sys, collections
dirs = [a for a in sys.argv[1:] if not a.startswith("--")] or ["data/text", "data/items", "data/events", "data/battle", "data/trainers", "data/pokemon"]
files = []
for d, _, fs in os.walk("."):
    if d.startswith(("./.git", "./build")): continue
    for f in fs:
        if f.endswith((".asm", ".inc", ".link", ".py", ".sh")): files.append(os.path.join(d, f))
tok = collections.Counter()
for f in files:
    tok.update(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", open(f, errors="replace").read()))
LAB = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)(::?)\s*(;.*)?$")
total = 0
for d in dirs:
    for dp, _, fs in os.walk(d):
        for f in sorted(fs):
            if not f.endswith(".asm"): continue
            p = os.path.join(dp, f)
            L = open(p).read().split("\n")
            out, i, dead = [], 0, []
            while i < len(L):
                m = LAB.match(L[i])
                if m and tok[m[1]] == 1:
                    j = i + 1
                    if j < len(L) and LAB.match(L[j]):          # aliases a following label: drop only this line
                        dead.append(m[1]); i += 1; continue
                    while j < len(L) and L[j].strip() != "" and not LAB.match(L[j]) and not re.match(r"\s*(SECTION|INCLUDE|MACRO|DEF|if|endc|ENDM)\b", L[j]): j += 1
                    dead.append(m[1]); i = j
                    while i < len(L) and L[i].strip() == "" and out and out[-1].strip() == "": i += 1
                    continue
                out.append(L[i]); i += 1
            if dead:
                total += len(dead)
                print(f"{p}: {len(dead)} labels  {dead[:4]}")
                if "--delete" in sys.argv: open(p, "w").write("\n".join(out))
print(total, "dead labels")
