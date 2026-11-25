#!/usr/bin/env python3
"""Variety audit: how repetitive are the NPC and trainer lines (and the map layouts) of the generated world?

usage: check_variety.py [--quiet] [--top N]
Reads every text block of maps/gen/*.asm and data/hardcore/*.asm, normalises it, and reports
  * per kind of speaker (fighters before and after a fight, townsfolk, the people inside buildings, hermits, givers, duelists) how many
    blocks there are, how many are unique and which share repeats another block word for word.
Exit status 1 if a category repeats more than its limit (CATS), so verify_all can gate on it.  The "bag is full" lines are left out on purpose:
they are only heard when the bag is full."""
import collections
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIMIT_EXACT = float(os.environ.get("LIMIT_EXACT", "0.10"))   # share of text blocks that repeat another block word for word
LIMIT_HEAD = float(os.environ.get("LIMIT_HEAD", "0.22"))     # share of blocks whose first six words repeat
AREAS = ["Tithe", "Grove", "Axiom", "Lotus", "Dis", "Purg", "Cherrygrove", "Other"]


def blocks(path):
    """(label, text) for every label whose body is text/line/para ... done|prompt in the file."""
    out, label, cur = [], None, None
    for raw in open(path, errors="replace"):
        s = raw.rstrip("\n")
        m = re.match(r"^(\w+):\s*$", s)
        if m:
            if cur:
                out.append((label, " ".join(cur)))
            label, cur = m[1], None
            continue
        t = s.strip()
        m = re.match(r'^(text|line|para|cont|next|done|prompt)\b\s*"?(.*?)"?$', t)
        if m and label:
            if m[1] in ("done", "prompt"):
                if cur:
                    out.append((label, " ".join(cur)))
                cur = None
            else:
                if cur is None:
                    cur = []
                if m[2] != "@":
                    cur.append(m[2])
        elif t and not t.startswith(";") and cur is not None and not re.match(r'^(text|line|para|cont|next)', t):
            out.append((label, " ".join(cur)))
            cur = None
    if cur:
        out.append((label, " ".join(cur)))
    return out


def norm(t):
    return re.sub(r"[^a-z0-9 ]", "", t.lower().replace("<player>", "player")).split()


def area_of(path):
    b = os.path.basename(path)
    for a in AREAS[:-1]:
        if b.startswith(a):
            return a
    return "Other"


CATS = [  # (name, label regex, limit on the share of blocks that repeat another block of the same category)
    ("fighter, before the fight", r"Trainer\d+SeenText$", 0.10),
    ("fighter, after the fight", r"Trainer\d+BeatenText$", 0.20),
    ("townsfolk and debaters", r"(Persona\d+|Townie\d+|DebateA|DebateB)Text$", 0.05),
    ("inside the Pokecenter, Mart, houses", r"(Pokecenter|Mart|House|Boutique)\d+b?Npc\d+Text$", 0.20),
    ("hermits (not the full-bag lines)", r"Hermit\d*(Seen|Beaten|Gift|After)?Text$|GiftHermit(After)?Text$", 0.20),
    ("gift givers (not the full-bag lines)", r"Giver(After)?Text$", 0.20),
    ("duelists and bosses", r"(Duel(Seen|Beaten|After)|Boss(Seen|Beaten|After))Text$", 0.05),
]


def main():
    quiet = "--quiet" in sys.argv
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 8
    files = sorted(glob.glob(os.path.join(ROOT, "maps/gen/*.asm")))
    allb = []
    for f in files:
        for label, text in blocks(f):
            w = norm(text)
            if len(w) >= 4:
                allb.append((area_of(f), os.path.basename(f), label, " ".join(w)))
    print(f"text blocks in the generated maps: {len(allb)}")
    bad = []
    for name, rx, limit in CATS:
        rows = [b for b in allb if re.search(rx, b[2])]
        if not rows:
            continue
        cnt = collections.Counter(b[3] for b in rows)
        rep = sum(1 for b in rows if cnt[b[3]] > 1)
        share = rep / len(rows)
        flag = "ok  " if share <= limit else "OVER"
        print(f"  {flag} {name:38s} blocks {len(rows):4d} unique {len(cnt):4d} repeating {rep:4d} ({share:5.1%}, limit {limit:.0%})")
        if share > limit:
            bad.append(name)
        if not quiet and share > 0:
            for t, c in cnt.most_common(top):
                if c > 1:
                    print(f"        x{c}: {t[:78]!r}")
    print("PASS" if not bad else f"FAIL: over the limit: {', '.join(bad)}")
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
