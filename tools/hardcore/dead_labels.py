#!/usr/bin/env python3
"""Delete global labels that nothing names (comments do not count), with their code or data up to the next global label.  Runs to a fixpoint.
Only engine/ and home/ are touched (maps, audio and the map tables are handled by their own tools).  A block is also kept when the block above it
falls through into it (no ret/jp/jr at the end), and it is reported.
Usage: dead_labels.py [--delete] [--prefix engine/pokemon]"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
LABEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?(?!\w)")
SKIP = ("engine/hardcore/",)
TERMINATORS = ("ret", "reti", "jp", "jr", "rst", "farjp", "tailcall", "predef_jump", "ret_", "text_end", "done", "end", "db -1", "db $ff", "dbw", "dba", "dw", "db")
def strip(line):
    i = line.find(";")
    return line if i < 0 else line[:i]
def all_files():
    out = []
    for d, _, fs in os.walk(ROOT):
        rel = os.path.relpath(d, ROOT)
        if rel.split(os.sep)[0] in (".git", "build", "tools", "scratch"): continue   # (gfx/ holds asm too: engine/gfx must count)
        for f in fs:
            if f.endswith((".asm", ".inc", ".link")):
                out.append(os.path.relpath(os.path.join(d, f), ROOT))
    return out
def terminal(block_lines):
    """does control stop at the end of this block?"""
    for l in reversed(block_lines):
        t = strip(l).strip()
        if not t or LABEL.match(t) and t.rstrip(":") == t.split()[0].rstrip(":") and len(t.split()) == 1: continue
        if t.startswith("."): 
            if len(t.split()) == 1: continue
        if re.match(r"(ret|reti|jp|jr|rst|farjp|jmp|predef_jump|tailcall|text_end|done|end|db|dw|dba|dbw|dn|bigdw|INCBIN|ds|assert|sound|note|rest|volume|tempo|notetype|octave|dutycycle|intensity|vibrato|stereopanning|loopchannel|endchannel|callchannel|dwb|raw|trainer|dt|map_|bg_event|coord_event|object_event|warp_event|connection|text|line|para|cont|next|done|prompt|page|scroll|sjump|jumptext|jumpstd|end|endall|endtext|closetext|waitbutton|opentext|pause|stopfollow|special|ld|call|callasm|farcall|callfar|jumpstd)\b", t):
            cmd = t.split()[0]
            if cmd in ("ret", "reti", "jp", "jr", "jmp", "farjp", "predef_jump", "tailcall", "rst", "text_end", "done", "end", "endchannel", "jumptext", "jumpstd", "sjump", "endall", "loopchannel"):
                # conditional jumps / returns do not stop
                if re.match(r"(ret|jp|jr)\s+(z|nz|c|nc)\b", t): return False
                return True
            if cmd in ("db", "dw", "dba", "dbw", "dn", "bigdw", "INCBIN", "ds", "dt", "dwb", "raw"): return True   # data keeps going into the next table on purpose
            return False
        return False
    return True
def main():
    pre = sys.argv[sys.argv.index("--prefix") + 1] if "--prefix" in sys.argv else ""
    files = {p: open(os.path.join(ROOT, p), errors="replace").read().splitlines(keepends=True) for p in all_files()}
    cand = [p for p in files if p.startswith(("engine/", "home/")) and not p.startswith(SKIP) and p.endswith(".asm") and p.startswith(pre)]
    removed_total, skipped = [], []
    for rnd in range(30):
        counts = {}
        for p, L in files.items():
            for l in L:
                for w in WORD.findall(strip(l)):
                    counts[w] = counts.get(w, 0) + 1
        dead_any = False
        for p in cand:
            L = files[p]
            blocks, start = [], 0
            in_macro = False
            for i, l in enumerate(L):
                if re.match(r"MACRO\b", l): in_macro = True
                brk = (LABEL.match(l) and not in_macro) or re.match(r"(INCLUDE|SECTION|MACRO|DEF|def|IF|if|ELIF|ELSE|ENDC|endc|PUSHS|POPS|for|endr|rept|ENDR)\b", l)
                if re.match(r"ENDM\b", l): in_macro = False
                if brk:
                    if i > start: blocks.append((start, i))
                    start = i
            blocks.append((start, len(L)))
            drop = []
            for bi, (a, b) in enumerate(blocks):
                if a >= len(L): continue
                m = LABEL.match(L[a])
                if not m: continue
                name = m.group(1)
                if counts.get(name, 0) != 1: continue
                # leading comment lines belong to the block
                if bi > 0:
                    pa, pb = blocks[bi - 1]
                    prev = [x for x in L[pa:pb] if (pa, pb) not in [(c, d) for c, d in drop]]
                    if (pa, pb) not in drop and not terminal(L[pa:pb]):
                        skipped.append((p, name)); continue
                drop.append((a, b))
            if drop:
                dead_any = True
                keep = []
                for i, l in enumerate(L):
                    if any(a <= i < b for a, b in drop): continue
                    keep.append(l)
                for a, b in drop:
                    removed_total.append((p, LABEL.match(L[a]).group(1), b - a))
                files[p] = keep
        if not dead_any: break
    for p, n, k in removed_total: print(f"{p}: {n} ({k} lines)")
    print(len(removed_total), "dead labels,", sum(k for _, _, k in removed_total), "lines;", len(set(skipped)), "kept because the block above falls into them")
    for p, n in sorted(set(skipped))[:40]: print("  fallthrough kept:", p, n)
    if "--delete" in sys.argv:
        for p in cand:
            open(os.path.join(ROOT, p), "w").write("".join(files[p]))
        print("written")
main()
