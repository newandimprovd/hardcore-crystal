#!/usr/bin/env python3
"""Drop every tileset no map (and no engine code) uses:  TILESET_* constant, row in data/tilesets.asm, and the *GFX/*Meta/*Coll,
*PalMap and *Anim data blocks (gfx/tilesets.asm, gfx/tileset_palette_maps.asm, data/tileset_anims.asm).  Their assets are then
unreferenced: run `unref_asm.py --assets --delete` and `dead_labels.py --delete` afterwards.  Usage: prune_tilesets.py [--delete]"""
import glob, re, sys
DEL = "--delete" in sys.argv
CONST, TABLE = "constants/tileset_constants.asm", "data/tilesets.asm"
BLOCKS = ["gfx/tilesets.asm", "gfx/tileset_palette_maps.asm", "data/tileset_anims.asm"]
rd = lambda p: open(p).read()
cs = rd(CONST)
names = re.findall(r"^\tconst (TILESET_\w+)", cs, re.M)
tl = rd(TABLE).split("\n")
rows = [i for i, l in enumerate(tl) if re.match(r"\ttileset \w+", l)]
camel = [re.match(r"\ttileset (\w+)", tl[i]).group(1) for i in rows]
assert len(camel) == len(names) + 1, (len(camel), len(names))      # row 0 is Tileset0 (no constant)
cam = dict(zip(names, camel[1:]))
code = ""
for f in glob.glob("**/*.asm", recursive=True):
    if f in (CONST, TABLE) or f.startswith("tools/"): continue
    code += rd(f)
used = {n for n in names if re.search(r"\b" + n + r"\b", code)}
dead = [n for n in names if n not in used]
print(f"{len(used)} tilesets used, {len(dead)} unused:", " ".join(n[8:] for n in dead))
if not DEL or not dead: sys.exit(0)
keep = {"Tileset0"} | {cam[n] for n in used}
keepnames = {k + s for k in keep for s in ("GFX", "Meta", "Coll", "PalMap", "Anim")}
# constants + table rows
cl = [l for l in cs.split("\n") if not any(re.match(r"\tconst " + n + r"\b", l) for n in dead)]
open(CONST, "w").write("\n".join(cl))
deadc = {cam[n] for n in dead}
open(TABLE, "w").write("\n".join(l for l in tl if not (re.match(r"\ttileset (\w+)", l) and re.match(r"\ttileset (\w+)", l).group(1) in deadc)))
# data blocks: a block is a run of label lines plus the content up to the next label line
for p in BLOCKS:
    L = rd(p).split("\n")
    out, i = [], 0
    islabel = lambda l: re.match(r"^((?:Unused)?Tileset\w+)::?\s*(?:;.*)?$", l)
    while i < len(L):
        if islabel(L[i]):
            labs, cmt = [], []
            while i < len(L) and islabel(L[i]): labs.append(islabel(L[i]).group(1)); cmt.append(L[i]); i += 1
            body = []
            while i < len(L) and L[i].strip():          # a block ends at the first blank line
                body.append(L[i]); i += 1
            alive = [k for k, l in enumerate(labs) if l in keepnames or l.startswith("Tileset0") or not re.search(r"(GFX|Meta|Coll|PalMap|Anim)$", l)]
            if alive: out += [cmt[k] for k in alive] + body      # labels keep their own punctuation/comment
            # else: dropped whole block
        else:
            out.append(L[i]); i += 1
    txt = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    open(p, "w").write(txt)
print("done")
