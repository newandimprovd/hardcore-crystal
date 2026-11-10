#!/usr/bin/env python3
"""Remove the songs nothing plays: MUSIC_* constant, row of the Music table, INCLUDE of the song file (and the file).
A song is used when its MUSIC_ name appears in any asm/python source other than the table's own constant line.
Usage: prune_music.py [--delete]"""
import glob, os, re, subprocess, sys
C = "constants/music_constants.asm"
P = "audio/music_pointers.asm"
A = "audio.asm"
cs = open(C).read().split("\n")
a = next(i for i, l in enumerate(cs) if l.strip() == "const_def")
b = next(i for i, l in enumerate(cs) if l.startswith("DEF NUM_MUSIC_SONGS"))
cl = [(re.match(r"\s*const (MUSIC_\w+)", cs[i]).group(1), i) for i in range(a + 1, b) if re.match(r"\s*const MUSIC_\w+", cs[i])]
tail = "\n".join(cs[b:])
text = tail
for f in glob.glob("**/*.asm", recursive=True) + glob.glob("tools/hardcore/**/*.py", recursive=True):
    if f in (C, P) or f.endswith("prune_music.py"): continue
    text += open(f, errors="replace").read()
# Area themes (towns, routes, dungeons) and encounter themes stay: the pending map and special-encounter passes may still pick them.
KEEP = ("ROUTE_", "TOWN", "CITY", "MT_MOON", "TIN_TOWER", "BURNED_TOWER", "LIGHTHOUSE", "LAKE_OF_RAGE", "INDIGO_PLATEAU", "DRAGONS_DEN",
        "VICTORY_ROAD", "NATIONAL_PARK", "RUINS_OF_ALPH", "PROF_OAK", "CLAIR", "MYSTICALMAN", "MUSIC_NONE")
keep = {n for n, _ in cl if any(k in n for k in KEEP) and n not in ("MUSIC_LAKE_OF_RAGE_ROCKET_RADIO", "MUSIC_MT_MOON_SQUARE")}
dead = [(n, i) for n, i in cl if n not in keep and not re.search(r"\b" + n + r"\b", text)]
print(len(cl), "songs;", len(dead), "unused:", " ".join(n for n, _ in dead))
if "--delete" not in sys.argv: sys.exit(0)
pl = open(P).read().split("\n")
s = next(i for i, l in enumerate(pl) if l.strip() == "table_width 3")
e = next(i for i, l in enumerate(pl) if l.strip().startswith("assert_table_length NUM_MUSIC_SONGS"))
rows = [i for i in range(s + 1, e) if re.match(r"\s*dba ", pl[i])]
assert len(rows) == len(cl), (len(rows), len(cl))
pos = {n: k for k, (n, _) in enumerate(cl)}
labels = [re.match(r"\s*dba (\w+)", pl[r]).group(1) for r in rows]
asm = open(A).read()
gone = []
for n, _ in dead:
    lab = labels[pos[n]]
    for f in glob.glob("audio/music/*.asm"):
        if re.search(r"^" + lab + r":", open(f).read(), re.M):
            inc = 'INCLUDE "%s"\n' % f
            if inc in asm: asm = asm.replace(inc, "")
            gone.append(f); break
    else:
        print("no file for", lab)
for k in sorted((pos[n] for n, _ in dead), reverse=True): del pl[rows[k]]
open(P, "w").write("\n".join(pl))
for _, i in sorted(dead, key=lambda x: -x[1]): del cs[i]
open(C, "w").write("\n".join(cs))
open(A, "w").write(asm)
for f in gone: subprocess.run(["git", "rm", "-qf", f])
print("removed", len(gone), "song files")
