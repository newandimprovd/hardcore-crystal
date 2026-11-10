#!/usr/bin/env python3
"""Drop the vanilla trainer parties and pictures the Hardcore Crystal ROM never uses.
Live vanilla party groups are the ones a `trainer`/`loadtrainer CLASS, id` with id < HC_GEN_ID_BASE reaches (YOUNGSTER, RIVAL1);
live pictures are those of the classes the game still shows (YOUNGSTER, RIVAL1, RIVAL2, POKEMON_PROF, MYSTICALMAN) plus every HC class.
Table rows keep their index (the engine indexes them by class id): dead rows point at HC_EmptyGroup / the YOUNGSTER pic instead.
Usage: prune_trainer_data.py [--delete]    (then unref_asm.py --assets --delete)"""
import re, sys
DEL = "--delete" in sys.argv
rd = lambda p: open(p).read()
LIVE_GROUPS = {"YOUNGSTER", "RIVAL1"}
LIVE_PICS = {"YOUNGSTER", "RIVAL1", "RIVAL2", "POKEMON_PROF", "MYSTICALMAN"}
cons = rd("constants/trainer_constants.asm")
classes = re.findall(r"^\ttrainerclass (\w+)", cons, re.M)[1:]           # [0] is TRAINER_NONE
pp = rd("data/trainers/party_pointers.asm").split("\n")
pr = [i for i, l in enumerate(pp) if re.match(r"\tdw \w+Group$", l) and "HC_EmptyGroup" not in l]
pic = rd("data/trainers/pic_pointers.asm").split("\n")
cr = [i for i, l in enumerate(pic) if re.match(r"\tdba_pic \w+", l)]
nvan = len(pr)
assert len(cr) >= nvan
deadg = [k for k in range(nvan) if classes[k] not in LIVE_GROUPS]
deadp = [k for k in range(nvan) if classes[k] not in LIVE_PICS]
print(f"{nvan} vanilla classes: {len(deadg)} dead party groups, {len(deadp)} dead pictures")
if not DEL: sys.exit(0)
dead_labels = set()
for k in deadg:
    dead_labels.add(re.match(r"\tdw (\w+)", pp[pr[k]]).group(1))
    pp[pr[k]] = "\tdw HC_EmptyGroup"
open("data/trainers/party_pointers.asm", "w").write("\n".join(pp))
# party blocks
t = rd("data/trainers/parties.asm")
for lab in dead_labels:
    t = re.sub(r"^" + lab + r":\n(?:(?!\w+Group:)[^\n]*\n)*", "", t, flags=re.M)
open("data/trainers/parties.asm", "w").write(t)
# dead classes' trainer-id constants (only those nothing references; live classes keep theirs, ids are positional)
src = cons.split("\n")
cur, out = None, []
allsrc = ""
import glob
for f in glob.glob("**/*.asm", recursive=True):
    if f != "constants/trainer_constants.asm": allsrc += rd(f)
deadset = {classes[k] for k in deadg}
for l in src:
    m = re.match(r"\ttrainerclass (\w+)", l)
    if m: cur = m.group(1)
    m = re.match(r"\tconst (\w+)", l)
    if m and cur in deadset and not re.search(r"\b" + m.group(1) + r"\b", allsrc): continue
    out.append(l)
open("constants/trainer_constants.asm", "w").write("\n".join(out))
# pictures
deadpic_labels = []
for k in deadp:
    lab = re.match(r"\tdba_pic (\w+)", pic[cr[k]]).group(1)
    deadpic_labels.append(lab)
    pic[cr[k]] = "\tdba_pic YoungsterPic"
open("data/trainers/pic_pointers.asm", "w").write("\n".join(pic))
pl = rd("gfx/pics.asm")
for lab in deadpic_labels:
    pl = re.sub(r"^" + lab + r":[^\n]*\n", "", pl, flags=re.M)
open("gfx/pics.asm", "w").write(pl)
print("done")
