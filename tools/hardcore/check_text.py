#!/usr/bin/env python3
"""Text box check: every text/line/cont/para/next string of the hack's own texts must fit the 18 column text box (tokens count as their usual width).
usage: check_text.py [glob ...]   (default: maps/*.asm, data/hardcore/*.asm, data/text/*.asm)"""
import glob, re, sys
ROOT = __file__.rsplit("/tools/", 1)[0]
TOK = {"<PLAYER>": 7, "<RIVAL>": 7, "<PK>": 1, "<MN>": 1, "<PKMN>": 4, "<ENEMY>": 17, "<TARGET>": 17, "<USER>": 17, "<LF>": 0, "<DONE>": 0, "<NEXT>": 0}
pats = sys.argv[1:] or ["maps/*.asm", "data/hardcore/*.asm", "data/text/*.asm"]
CMD = re.compile(r'^\s*(text|line|cont|para|next|done|prompt|text_start)\b\s*(?:"(.*)")?\s*(;.*)?$')
bad = 0
for pat in pats:
    for f in sorted(glob.glob(f"{ROOT}/{pat}")):
        for n, l in enumerate(open(f, errors="replace"), 1):
            m = re.match(r'^\s*(text|line|cont|para|next)\s+"(.*)"\s*(?:;.*)?$', l)
            if not m:
                continue
            s = m.group(2)
            w = len(re.sub(r"<[A-Z_]+>", lambda t: "x" * TOK.get(t.group(0), 1), s.replace("@", "")))
            if w > 18:
                bad += 1
                print(f"{f[len(ROOT)+1:]}:{n}: {w} cols: {s}")
print(bad, "lines over 18 columns")
sys.exit(1 if bad else 0)
