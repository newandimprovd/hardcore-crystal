#!/usr/bin/env python3
"""Battle text overflow check: the battle texts print "CLASS NAME" on one 18 column line (plus "!"), so the sum of class + 1 + name must be at most 17.
Also lists the names of generated trainers per class.  usage: check_names.py [-v]"""
import re, sys
ROOT = __file__.rsplit("/tools/", 1)[0]
cls = re.findall(r'li "([^"]*)"', open(ROOT + "/data/trainers/class_names.asm").read())
consts = re.findall(r"trainerclass (\w+)", open(ROOT + "/constants/trainer_constants.asm").read())
consts = [c for c in consts if c != "TRAINER_NONE"]
cname = dict(zip(consts, cls))
bad = []
# vanilla style groups
txt = open(ROOT + "/data/trainers/parties.asm").read()
for g, body in zip(re.split(r"\n(\w+Group):", txt)[1::2], re.split(r"\n(\w+Group):", txt)[2::2]):
    cn = g[:-5]
    for n in re.findall(r'db "([^@"]*)@", TRAINERTYPE', body):
        c = next((v for k, v in cname.items() if k.replace("_", "") == cn.upper()), None)
        if c and len(c) + 1 + len(n) > 17:
            bad.append((c, n, len(c) + 1 + len(n)))
gen = open(ROOT + "/data/hardcore/gen_trainer_data.asm").read()
for g, body in zip(re.split(r"\nHC_GenGroup_(\w+):", gen)[1::2], re.split(r"\nHC_GenGroup_(\w+):", gen)[2::2]):
    c = cname.get(g, g)
    for n in re.findall(r'db "([^@"]*)@"', body):
        if len(c) + 1 + len(n) > 17:
            bad.append((c, n, len(c) + 1 + len(n)))
for b in sorted(set(bad), key=lambda x: -x[2]):
    print(b)
print(len(set(bad)), "overflowing combinations (the engine prints the name alone for these)")
sys.exit(1 if bad and "-s" in sys.argv else 0)
