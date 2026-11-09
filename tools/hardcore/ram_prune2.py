#!/usr/bin/env python3
"""Second RAM pass: inside the sections that stay, drop the UNION branches and the plain one line labels that nothing uses.
A label is used when code outside ram/ names it, or when other RAM lines do.  Runs to a fixpoint.
Usage: ram_prune2.py [--delete]"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LABD = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?")
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
RAMFILES = ["ram/wram.asm", "ram/sram.asm", "ram/hram.asm"]
# plain labels go only when their name says they belong to a removed feature; the rest may sit inside a struct that is copied whole
DEAD = re.compile(r"Mobile|SDK|Link|Serial|Printer|Slot|Reel|CardFlip|MemoryGame|BattleTower|BT_|Bt[A-Z]|MysteryGift|Mystery|TrainerRanking|Phone|Radio|MagnetTrain|BugContest|Apricorn|Roam|Trade|Elevator|Offer|EZChat|EmailAddress|Seer|Puzzle|Odd|Wc[0-9a-f]{3}|^wc[0-9a-f]{3}|^s[0-9]_|^w[0-9]_|Pokegear|OTMonSelection|Deck|Discard|Payout|Lucky|Dude|WhichBoxMonToPrint|Magikarp|Kenji|FightCount")
SIMPLE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?\s*(db|dw|dl|ds\b[^;]*)\s*(;.*)?$")

def outside_words():
    out = set()
    for top in ("engine", "home", "data", "maps", "macros", "audio", "gfx", "text", "constants", "tools/hardcore/areas"):
        for d, _, fs in os.walk(os.path.join(ROOT, top)):
            for f in fs:
                if f.endswith((".asm", ".inc")):
                    out.update(WORD.findall(open(os.path.join(d, f), errors="replace").read()))
    for f in ("main.asm", "includes.asm"):
        out.update(WORD.findall(open(os.path.join(ROOT, f)).read()))
    return out

class Union:
    def __init__(self): self.branches = []     # list of list of nodes (str lines or Union)
    # a union is written as UNION / NEXTU ... / ENDU
def parse(lines):
    root, stack = [], []
    cur = root
    stack = []
    for l in lines:
        t = l.strip()
        if t == "UNION":
            u = Union(); u.branches.append([]); cur.append(u); stack.append((cur, u)); cur = u.branches[0]
        elif t == "NEXTU" and stack:
            _, u = stack[-1]; u.branches.append([]); cur = u.branches[-1]
        elif t == "ENDU" and stack:
            cur, _ = stack.pop()
        else:
            cur.append(l)
    return root
def flatten(nodes):
    out = []
    for n in nodes:
        if isinstance(n, str): out.append(n)
        else:
            for i, br in enumerate(n.branches):
                out.append("UNION\n" if i == 0 else "NEXTU\n"); out.extend(flatten(br))
            out.append("ENDU\n")
    return out
def labels(nodes):
    s = set()
    for l in flatten(nodes):
        m = LABD.match(l)
        if m: s.add(m.group(1))
    return s
def code_words(lines):
    s = set()
    for l in lines:
        if l.lstrip().startswith(";"): continue
        s.update(WORD.findall(l.split(";")[0]))
    return s

def prune_nodes(nodes, used, dropped):
    out = []
    for n in nodes:
        if isinstance(n, str):
            m = SIMPLE.match(n)
            if m and m.group(1) not in used and DEAD.search(m.group(1)):
                dropped.append(m.group(1)); continue
            out.append(n)
        else:
            keep = []
            for br in n.branches:
                br = prune_nodes(br, used, dropped)
                labs = labels(br)
                if labs and not (labs & used):
                    dropped.extend(sorted(labs)); continue
                keep.append(br)
            if not keep: continue
            n.branches = keep
            out.append(n)
    return out

def main():
    outside = outside_words()
    texts = {rf: open(os.path.join(ROOT, rf)).read().splitlines(keepends=True) for rf in RAMFILES}
    ndrop = 0
    for rnd in range(20):
        # labels in use now: outside code, or named by any RAM line that is not just the definition of that label
        used = set(outside)
        parsed = {}
        for rf, lines in texts.items():
            for l in lines:
                m = LABD.match(l)
                body = l.split(";")[0]
                ws = WORD.findall(body)
                if m: ws = ws[1:]
                used.update(ws)
        dropped = []
        for rf in RAMFILES:
            sections, cur = [], []
            for l in texts[rf]:
                if l.startswith("SECTION") and cur:
                    sections.append(cur); cur = []
                cur.append(l)
            sections.append(cur)
            out = []
            for sec in sections:
                head = sec[0] if sec and sec[0].startswith("SECTION") else None
                body = sec[1:] if head else sec
                tree = parse(body)
                tree = prune_nodes(tree, used, dropped)
                out.extend(([head] if head else []) + flatten(tree))
            texts[rf] = out
        if not dropped: break
        ndrop += len(dropped)
        print(f"round {rnd}: {len(dropped)} labels")
    print("labels dropped:", ndrop)
    if "--delete" in sys.argv:
        for rf, lines in texts.items():
            open(os.path.join(ROOT, rf), "w").write("".join(lines))
main()
