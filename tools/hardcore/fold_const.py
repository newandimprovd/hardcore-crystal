#!/usr/bin/env python3
"""Constant folding for the removed features: there is no link cable, no mobile adapter and no Battle Tower, so
   hSerialConnectionStatus never says USING_*_CLOCK, wLinkMode is 0 (LINK_NULL) and wInBattleTowerBattle is 0.
   Folds the three-line tests, deletes the code that can then no longer be reached and the local labels nothing jumps to.
Usage: fold_const.py [--delete] files...      (without --delete only reports)"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAB = re.compile(r"^(\.[A-Za-z_][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*(?=::?))(::?)?(?=\s|$|;)")
def strip(l):
    i = l.find(";"); return (l if i < 0 else l[:i]).strip()
LOAD_PATTERNS = [
    # (load lines, compare line regex) -> the test is "never equal"
    (r"ldh a, \[hSerialConnectionStatus\]", r"cp USING_(?:EXTERNAL|INTERNAL)_CLOCK", "never"),
    (r"ld a, \[wLinkMode\]", r"cp LINK_\w+", "never"),
    (r"ld a, \[wLinkMode\]", r"and a", "zero"),
    (r"ld a, \[wInBattleTowerBattle\]", r"and a", "zero"),
]
JMP = re.compile(r"(jr|jp)\s+(z|nz),\s*(\S+)$")
def fold(lines):
    out, i, n, uncond = [], 0, 0, []
    while i < len(lines):
        done = False
        if i + 2 < len(lines):
            a, b, c = strip(lines[i]), strip(lines[i + 1]), strip(lines[i + 2])
            m = JMP.match(c)
            if m:
                for la, lb, kind in LOAD_PATTERNS:
                    if re.fullmatch(la, a) and re.fullmatch(lb, b):
                        # the test result: kind never -> Z is false (nz); kind zero -> Z true (z)
                        taken = (m.group(2) == "nz") if kind == "never" else (m.group(2) == "z")
                        if taken:
                            out.append(f"\t{m.group(1)} {m.group(3)}\n"); uncond.append(len(out) - 1)
                        n += 1; i += 3; done = True
                        break
        if not done:
            # call IsMobileBattle / IsMobileBattle2 then jr z / nz : mobile never
            if i + 1 < len(lines) and re.fullmatch(r"call IsMobileBattle2?", strip(lines[i])):
                m = JMP.match(strip(lines[i + 1]))
                if m:
                    if m.group(2) == "nz":
                        out.append(f"\t{m.group(1)} {m.group(3)}\n"); uncond.append(len(out) - 1)
                    n += 1; i += 2; continue
            out.append(lines[i]); i += 1
    return out, n, uncond
def is_term(t):
    return bool(re.match(r"(ret|reti|jp\s+hl|jp\s+[^z nc,]\S*|jr\s+[^z nc,]\S*)$", t)) and not re.match(r"(jp|jr)\s+(z|nz|c|nc),", t)
def drop_unreachable(lines, uncond):
    """After a folded unconditional jump, instructions up to the next label are unreachable."""
    kill = set()
    for u in uncond:
        j = u + 1
        while j < len(lines):
            t = strip(lines[j])
            if LAB.match(lines[j]) or re.match(r"(INCLUDE|SECTION|MACRO|ENDM|DEF|def|if|IF|else|ELSE|endc|ENDC|for|endr|rept|assert|ASSERT|db|dw|dba|dbw|ds|INCBIN|text_|line|para|cont|done|next|page)\b", t):
                break
            kill.add(j); j += 1
    return [l for k, l in enumerate(lines) if k not in kill], len(kill)
def dead_locals(lines):
    removed, changed = 0, True
    while changed:
        changed = False
        # scope = from a global label to the next global label
        scopes, start = [], 0
        for i, l in enumerate(lines):
            m = LAB.match(l)
            if m and not m.group(1).startswith("."):
                if i > start: scopes.append((start, i))
                start = i
        scopes.append((start, len(lines)))
        for a, b in scopes:
            body = lines[a:b]
            code = "\n".join(strip(x) for x in body)
            for k in range(a, b):
                m = LAB.match(lines[k])
                if not m or not m.group(1).startswith("."): continue
                name = m.group(1)
                if len(re.findall(re.escape(name) + r"(?![A-Za-z0-9_])", code)) > 1: continue
                if strip(lines[k]) not in (name, name + ":", name + "::"):
                    continue   # label with code on the same line: keep
                # previous significant line
                p = k - 1
                while p >= a and not strip(lines[p]): p -= 1
                prev_t = strip(lines[p]) if p >= a else ""
                falls = not is_term(prev_t) and not LAB.match(lines[p] if p >= a else "") 
                if p >= a and LAB.match(lines[p]) and not strip(lines[p]).endswith(":") : falls = False
                if falls:
                    del lines[k]; removed += 1; changed = True; break
                # unreachable: delete up to next label
                j = k + 1
                while j < len(lines):
                    if LAB.match(lines[j]) or re.match(r"(INCLUDE|SECTION|MACRO|ENDM|DEF|def)\b", lines[j]): break
                    j += 1
                del lines[k:j]; removed += j - k; changed = True; break
            if changed: break
    return lines, removed
def drop_redundant_jumps(lines):
    out, n, i = [], 0, 0
    while i < len(lines):
        m = re.fullmatch(r"(?:jr|jp)\s+(\.[A-Za-z_]\w*)", strip(lines[i]))
        if m:
            j = i + 1
            while j < len(lines) and (not strip(lines[j])):
                j += 1
            lm = LAB.match(lines[j]) if j < len(lines) else None
            if lm and lm.group(1) == m.group(1):
                n += 1; i += 1; continue
        out.append(lines[i]); i += 1
    return out, n
def main():
    files = [f for f in sys.argv[1:] if not f.startswith("--")]
    tot = [0, 0, 0]
    for f in files:
        p = os.path.join(ROOT, f)
        L = open(p).read().splitlines(keepends=True)
        L2, n, unc = fold(L)
        L2, k = drop_unreachable(L2, unc)
        L2, j = drop_redundant_jumps(L2)
        L2, r = dead_locals(L2)
        if not (n or k or r or j): continue
        n += j
        print(f"{f}: {n} tests folded, {k} unreachable lines, {r} dead local label lines")
        tot[0] += n; tot[1] += k; tot[2] += r
        if "--delete" in sys.argv: open(p, "w").write("".join(L2))
    print("total", tot)
main()
