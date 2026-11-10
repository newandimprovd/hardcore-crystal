#!/usr/bin/env python3
"""Remove the overworld sprites (SPRITE_*) no map, table or generator names: the constant, the OverworldSprites row, and via
dead_labels.py the sprite graphics label.  Only the vanilla block of constants/sprite_constants.asm is touched (not HC-ART sprites,
pokemon sprites or the special value blocks).   Usage: prune_sprites.py [--delete]"""
import glob, re, sys
C = "constants/sprite_constants.asm"
T = "data/sprites/sprites.asm"
cs = open(C).read().split("\n")
a = next(i for i, l in enumerate(cs) if l.strip() == "const_def")
b = next(i for i, l in enumerate(cs) if "hc_sprite_constants" in l)
cl = [(re.match(r"\s*const (SPRITE_\w+)", cs[i]).group(1), i) for i in range(a + 1, b) if re.match(r"\s*const SPRITE_\w+", cs[i])]
assert cl[0][0] == "SPRITE_NONE"
text = ""
for f in glob.glob("**/*.asm", recursive=True) + glob.glob("tools/hardcore/**/*.py", recursive=True):
    if f == C or f.endswith("prune_sprites.py"): continue
    text += open(f, errors="replace").read()
dead = [(n, i) for n, i in cl[1:] if not re.search(r"\b" + n + r"\b", text)]
print(len(cl) - 1, "sprites;", len(dead), "unused:", " ".join(n for n, _ in dead))
if "--delete" not in sys.argv: sys.exit(0)
tl = open(T).read().split("\n")
s = next(i for i, l in enumerate(tl) if l.strip().startswith("table_width"))
e = next(i for i, l in enumerate(tl) if "hc_sprites.asm" in l)
rows = [i for i in range(s + 1, e) if tl[i].strip().startswith("overworld_sprite ")]
assert len(rows) == len(cl) - 1, (len(rows), len(cl) - 1)
pos = {n: k for k, (n, _) in enumerate(cl[1:])}
for k in sorted((pos[n] for n, _ in dead), reverse=True): del tl[rows[k]]
open(T, "w").write("\n".join(tl))
for _, i in sorted(dead, key=lambda x: -x[1]): del cs[i]
open(C, "w").write("\n".join(cs))
print("done")
