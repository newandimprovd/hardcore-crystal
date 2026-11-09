#!/usr/bin/env python3
"""Delete whole RAM sections of removed features.  A section goes when none of its labels is used outside it (code, data, other RAM sections).
Usage: ram_prune.py [--delete]   (without --delete it lists the candidates)"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAB = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?", re.M)
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
RAMFILES = ["ram/wram.asm", "ram/sram.asm", "ram/hram.asm"]
def words_of(top):
    out = set()
    for d, _, fs in os.walk(os.path.join(ROOT, top)):
        for f in fs:
            if f.endswith((".asm", ".inc")):
                out.update(WORD.findall(open(os.path.join(d, f), errors="replace").read()))
    return out
def split(text):
    parts, cur = [], []
    for l in text.splitlines(keepends=True):
        if l.startswith("SECTION") and cur:
            parts.append("".join(cur)); cur = []
        cur.append(l)
    parts.append("".join(cur))
    return parts
def main():
    outside = set()
    for top in ("engine", "home", "data", "maps", "macros", "audio", "gfx", "text", "constants", "tools/hardcore/areas"):
        outside |= words_of(top)
    outside.update(WORD.findall(open(os.path.join(ROOT, "main.asm")).read()))
    outside.update(WORD.findall(open(os.path.join(ROOT, "includes.asm")).read()))
    # all sections of the three files, with the words they use (comments left out) and the labels they define
    secs = []
    for rf in RAMFILES:
        for p in split(open(os.path.join(ROOT, rf)).read()):
            code = "".join(l for l in p.splitlines(keepends=True) if not l.lstrip().startswith(";"))
            secs.append(dict(file=rf, text=p, labs=set(LAB.findall(code)), words=set(WORD.findall(code))))
    owner = {}
    for i, sc in enumerate(secs):
        for l in sc["labs"]:
            owner.setdefault(l, i)
    live = {i for i, sc in enumerate(secs) if not sc["text"].startswith("SECTION") or not sc["labs"] or any(l in outside for l in sc["labs"])}
    todo = list(live)
    while todo:
        i = todo.pop()
        for w in secs[i]["words"]:
            j = owner.get(w)
            if j is not None and j not in live:
                live.add(j); todo.append(j)
    total = 0
    for rf in RAMFILES:
        keep = []
        for i, sc in enumerate(secs):
            if sc["file"] != rf:
                continue
            if i in live:
                keep.append(sc["text"]); continue
            print(f"{rf}: drop {sc['text'].splitlines()[0]}  ({len(sc['labs'])} labels, {len(sc['text'].splitlines())} lines)")
            total += len(sc["text"].splitlines())
        if "--delete" in sys.argv:
            open(os.path.join(ROOT, rf), "w").write("".join(keep))
    print("lines dropped:", total)
main()
