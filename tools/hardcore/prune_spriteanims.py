#!/usr/bin/env python3
"""Prune the sprite-animation tables in one pass, in dependency order:
  SPRITE_ANIM_OBJ_*      unused when no code names it            (constant + 2-line row in data/sprite_anims/objects.asm)
  SPRITE_ANIM_FUNC_*     unused when no live object row / code names it  (constant + dw row in DoSpriteAnimFrame.Jumptable)
  SPRITE_ANIM_FRAMESET_* unused when no live object row / code names it  (constant + dw row + .Frameset_x data block)
  SPRITE_ANIM_OAMSET_*   unused when no live frameset block names it     (constant + spriteanimoam row, shared .OAMData_x blocks)
Function bodies of removed funcs still name framesets, so run `prune_spriteanims.py --delete`, `dead_labels.py --delete` and repeat
until it reports nothing.   Usage: prune_spriteanims.py [--delete]"""
import glob, re, sys
CONST = "constants/sprite_anim_constants.asm"
OBJ = "data/sprite_anims/objects.asm"
FRM = "data/sprite_anims/framesets.asm"
OAM = "data/sprite_anims/oam.asm"
FNC = "engine/sprite_anims/functions.asm"
DEL = "--delete" in sys.argv

def rd(p): return open(p).read()
def consts(prefix, endname, src):
    L = src.split("\n")
    a = next(i for i, l in enumerate(L) if re.match(r"\s*const " + prefix, l))
    b = next(i for i, l in enumerate(L) if l.startswith("DEF " + endname))
    out = [(re.match(r"\s*const (\w+)", L[i]).group(1), i) for i in range(a, b) if re.match(r"\s*const " + prefix, L[i])]
    return out
cs = rd(CONST)
objs = consts("SPRITE_ANIM_OBJ_", "NUM_SPRITE_ANIM_OBJS", cs)
funcs = consts("SPRITE_ANIM_FUNC_", "NUM_SPRITE_ANIM_FUNCS", cs)
frames = consts("SPRITE_ANIM_FRAMESET_", "NUM_SPRITE_ANIM_FRAMESETS", cs)
oams = consts("SPRITE_ANIM_OAMSET_", "NUM_SPRITE_ANIM_OAMSETS", cs)

code = ""
for f in glob.glob("**/*.asm", recursive=True) + glob.glob("tools/hardcore/**/*.py", recursive=True):
    if f in (CONST, OBJ, FRM, OAM) or f.endswith("prune_spriteanims.py"): continue
    code += rd(f)
def named(n, text): return re.search(r"\b" + n + r"\b", text) is not None

# objects --------------------------------------------------------------------------------------------------
deadobj = {n for n, _ in objs if not named(n, code)}
ol = rd(OBJ).split("\n")
s = next(i for i, l in enumerate(ol) if l.strip().startswith("table_width"))
orows = [i for i in range(s + 1, len(ol)) if ol[i].startswith("\tdb ")]
assert len(orows) == len(objs), (len(orows), len(objs))
alive_rows = [ol[orows[k]] for k, (n, _) in enumerate(objs) if n not in deadobj]
objtext = "\n".join(alive_rows)
# funcs / framesets ----------------------------------------------------------------------------------------
deadfunc = {n for n, _ in funcs if not named(n, code) and not named(n, objtext)}
deadframe = {n for n, _ in frames if not named(n, code) and not named(n, objtext)}
# oamsets: named by live frameset blocks or by code
fl = rd(FRM).split("\n")
fs = next(i for i, l in enumerate(fl) if l.strip().startswith("table_width"))
frows = [i for i in range(fs + 1, len(fl)) if fl[i].startswith("\tdw .Frameset_")]
assert len(frows) == len(frames), (len(frows), len(frames))
blocks = {}
cur = None
for i, l in enumerate(fl):
    m = re.match(r"\.(Frameset_\w+):", l)
    if m: cur = m.group(1); blocks[cur] = []
    elif cur: blocks[cur].append(l)
frlabel = [re.match(r"\tdw \.(\w+)", fl[r]).group(1) for r in frows]
livetext = "\n".join("\n".join(blocks.get(frlabel[k], [])) for k, (n, _) in enumerate(frames) if n not in deadframe)
deadoam = {n for n, _ in oams if not named(n, code) and not named(n, livetext)}
# index 0 of every list is the "none" entry that engine code addresses by number (zero-filled structs), never remove it
deadobj.discard(objs[0][0]); deadfunc.discard(funcs[0][0]); deadframe.discard(frames[0][0]); deadoam.discard(oams[0][0])
print(f"objects {len(deadobj)}/{len(objs)}  funcs {len(deadfunc)}/{len(funcs)}  framesets {len(deadframe)}/{len(frames)}  oamsets {len(deadoam)}/{len(oams)}")
if not DEL or not (deadobj or deadfunc or deadframe or deadoam): sys.exit(0)

def drop_rows(path, rows_idx, dead_idx, extra_before=0):
    pass
# objects: remove the comment line above each db row too
for k in sorted((k for k, (n, _) in enumerate(objs) if n in deadobj), reverse=True):
    r = orows[k]
    del ol[r]
    if ol[r - 1].startswith("; SPRITE_ANIM_OBJ_"): del ol[r - 1]
open(OBJ, "w").write("\n".join(ol))
# funcs
fnl = rd(FNC).split("\n")
js = next(i for i, l in enumerate(fnl) if l.strip().startswith("table_width"))
je = next(i for i, l in enumerate(fnl) if l.strip().startswith("assert_table_length NUM_SPRITE_ANIM_FUNCS"))
jrows = [i for i in range(js + 1, je) if fnl[i].startswith("\tdw ")]
assert len(jrows) == len(funcs), (len(jrows), len(funcs))
for k in sorted((k for k, (n, _) in enumerate(funcs) if n in deadfunc), reverse=True): del fnl[jrows[k]]
open(FNC, "w").write("\n".join(fnl))
# framesets: rows and data blocks
dead_labels_f = {frlabel[k] for k, (n, _) in enumerate(frames) if n in deadframe}
for k in sorted((k for k, (n, _) in enumerate(frames) if n in deadframe), reverse=True): del fl[frows[k]]
txt = "\n".join(fl)
for lab in dead_labels_f:
    txt = re.sub(r"^\." + lab + r":\n(?:(?!\.\w+:)[^\n]*\n)*", "", txt, flags=re.M)
for lab in set(re.findall(r"^\.(Frameset_\w+):", txt, re.M)):      # also drop orphan "; unreferenced" blocks that no table row names
    if len(re.findall(r"\." + lab + r"\b", txt)) == 1:
        txt = re.sub(r"^\." + lab + r":[^\n]*\n(?:(?!\.\w+:)[^\n]*\n)*", "", txt, flags=re.M)
txt = re.sub(r"\n{3,}", "\n\n", txt)
open(FRM, "w").write(txt)
# oamsets
ol2 = rd(OAM).split("\n")
os_ = next(i for i, l in enumerate(ol2) if l.strip().startswith("table_width"))
orow2 = [i for i in range(os_ + 1, len(ol2)) if ol2[i].strip().startswith("spriteanimoam ")]
assert len(orow2) == len(oams), (len(orow2), len(oams))
for k in sorted((k for k, (n, _) in enumerate(oams) if n in deadoam), reverse=True): del ol2[orow2[k]]
txt = "\n".join(ol2)
for lab in set(re.findall(r"^\.(OAMData_\w+):", txt, re.M)):
    if len(re.findall(r"\." + lab + r"\b", txt)) == 1:       # only the label line itself
        txt = re.sub(r"^\." + lab + r":\n(?:(?!\.\w+:)[^\n]*\n)*", "", txt, flags=re.M)
txt = re.sub(r"\n{3,}", "\n\n", txt)
open(OAM, "w").write(txt)
# constants
cl = cs.split("\n")
for n in deadobj | deadfunc | deadframe | deadoam:
    cl = [l for l in cl if not re.match(r"\s*const " + n + r"\b", l)]
open(CONST, "w").write("\n".join(cl))
print("done")
