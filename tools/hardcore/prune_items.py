#!/usr/bin/env python3
"""Remove the items nothing uses from every index-aligned item table at once:
  constants/item_constants.asm   const lines (hex id comments are dropped, they would be wrong)
  data/items/names.asm           li rows
  data/items/descriptions.asm    dw rows (+ description text no row names any more)
  data/items/attributes.asm      "; NAME" + item_attribute pairs
  engine/items/item_effects.asm  dw rows ("; NAME" comments)
and the filler rows past HM07 (ids that no longer exist), with the closing asserts rewritten.
Only items of the regular block (ids 1..NUM_ITEMS) are pruned; TM/HM slots and ITEM_C3/ITEM_DC stay.
Usage: prune_items.py [--delete] [NAME ...]   (default list: item_usage.py output)"""
import re, subprocess, sys
CONST = "constants/item_constants.asm"
NAMES = "data/items/names.asm"
DESC = "data/items/descriptions.asm"
ATTR = "data/items/attributes.asm"
EFF = "engine/items/item_effects.asm"
TOTAL = "NUM_ITEMS + NUM_TMS + 2 + NUM_HMS"

def rd(p): return open(p).read().split("\n")
def wr(p, L): open(p, "w").write("\n".join(L))

cl = rd(CONST)
c0 = next(i for i, l in enumerate(cl) if l.strip() == "const_def")
c1 = next(i for i, l in enumerate(cl) if l.startswith("DEF NUM_ITEMS"))
items = [(re.match(r"\s*const (\w+)", cl[i]).group(1), i) for i in range(c0 + 1, c1)]
names = [n for n, _ in items]
assert names[0] == "NO_ITEM"

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if args:
    drop = set(args)
else:
    out = subprocess.run([sys.executable, "tools/hardcore/item_usage.py"], capture_output=True, text=True).stdout.splitlines()
    drop = set(out[1].split())
drop = {n for n in drop if n in names and n not in ("NO_ITEM", "ITEM_B3", "ITEM_BE")}
print(len(drop), "items to drop:", " ".join(sorted(drop)))
if "--delete" not in sys.argv: sys.exit(0)
idx = sorted(i for i, n in enumerate(names) if n in drop)   # 0 is NO_ITEM, row k of a table is item k+1
rowdrop = [i - 1 for i in idx]

# names ------------------------------------------------------------------------------------------------
L = rd(NAMES)
b = next(i for i, l in enumerate(L) if l.strip() == "assert_list_length NUM_ITEMS")
rows = [i for i in range(b) if L[i].startswith("\tli ")]
assert len(rows) == len(names) - 1, ("names rows", len(rows), len(names) - 1)
for k in reversed(rowdrop): del L[rows[k]]
hm = next(i for i, l in enumerate(L) if l.strip().startswith("assert_list_length " + TOTAL))
wr(NAMES, L[:hm + 1] + [""])

# descriptions -----------------------------------------------------------------------------------------
L = rd(DESC)
b = next(i for i, l in enumerate(L) if l.strip() == "assert_table_length NUM_ITEMS")
rows = [i for i in range(b) if L[i].startswith("\tdw ")]
assert len(rows) == len(names) - 1, ("desc rows", len(rows))
dead = [L[rows[k]].split()[1] for k in rowdrop]
for k in reversed(rowdrop): del L[rows[k]]
end = next((i for i, l in enumerate(L) if l.strip() == "assert_table_length $ff"), None)
if end is not None:                                     # first run: the filler rows are still there
    L[end] = "\tassert_table_length " + TOTAL
    del L[end - 6:end]                                  # filler rows for ids that no longer exist
text = "\n".join(L)
for lab in set(dead):
    if len(re.findall(r"\b" + lab + r"\b", text)) == 1:  # only the label line itself is left
        text = re.sub(r"^" + lab + r":\n(?:[^\n]+\n)+\n?", "", text, flags=re.M)
open(DESC, "w").write(text)

# attributes -------------------------------------------------------------------------------------------
L = rd(ATTR)
b = next(i for i, l in enumerate(L) if l.strip() == "assert_table_length NUM_ITEMS")
pairs = [i for i in range(b) if L[i].startswith("\titem_attribute")]
assert len(pairs) == len(names) - 1, ("attr rows", len(pairs))
for k in reversed(rowdrop):
    i = pairs[k]
    del L[i]
    if L[i - 1].startswith("; "): del L[i - 1]
hm = next(i for i, l in enumerate(L) if l.strip().startswith("assert_table_length " + TOTAL))
wr(ATTR, L[:hm + 1] + [""])

# effects ----------------------------------------------------------------------------------------------
L = rd(EFF)
a = next(i for i, l in enumerate(L) if l.startswith("ItemEffects:"))
b = next(i for i, l in enumerate(L) if l.strip() == "assert_table_length ITEM_B3")
byname = {}
for i in range(a, b):
    m = re.match(r"\tdw \w+\s*; ([A-Z0-9_]+)$", L[i])
    if m: byname[m.group(1)] = i
missing = [n for n in drop if names.index(n) <= names.index("ITEM_B3") and n not in byname]
assert not missing, missing
for n in sorted((n for n in drop if n in byname), key=lambda n: -byname[n]): del L[byname[n]]
wr(EFF, L)

# constants --------------------------------------------------------------------------------------------
L = rd(CONST)
for i in sorted([items[k][1] for k in idx], reverse=True): del L[i]
L = [re.sub(r"\s+; [0-9a-f]{2}$", "", l) if re.match(r"\s*(const|add_tm|add_hm) ", l) else l for l in L]
L = [l for l in L if l.strip() != "const ITEM_FA"]
wr(CONST, L)
print("done")
