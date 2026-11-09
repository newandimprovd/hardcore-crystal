#!/usr/bin/env python3
"""Drop the overworld script commands no script uses: the const + MACRO pair in macros/scripts/events.asm and the entry in
ScriptCommandTable (engine/overworld/scripting.asm).  The handler routines then fall to dead_labels.py.
Usage: prune_script_cmds.py [--delete]"""
import glob, re, sys
EV = "macros/scripts/events.asm"
SC = "engine/overworld/scripting.asm"
ev = open(EV).read()
pat = re.compile(r"(\tconst (\w+)_command[^\n]*\n)(MACRO (\w+)\n.*?\nENDM\n\n?)", re.S)
cmds = [(m.group(2), m.group(4), m.start(), m.end()) for m in pat.finditer(ev)]
sc = open(SC).read().splitlines(keepends=True)
a = next(i for i, l in enumerate(sc) if l.startswith("ScriptCommandTable:"))
b = next(i for i, l in enumerate(sc) if "assert_table_length NUM_EVENT_COMMANDS" in l)
entries = [i for i in range(a, b) if re.match(r"\tdw \w+", sc[i])]
print(len(cmds), "commands,", len(entries), "table entries")
assert len(cmds) == len(entries), "table and macros disagree"
texts = {}
for f in glob.glob("**/*.asm", recursive=True) + glob.glob("tools/hardcore/**/*.py", recursive=True):
    if f != EV: texts[f] = open(f, errors="replace").read()
# macros in events.asm that other macros use
inner = ev
def used(name):
    rx_asm = re.compile(r"^[ \t]+" + re.escape(name) + r"(?=[\s;]|$)", re.M)
    rx_py = re.compile(r"(?:\\t|\\n|\t)" + re.escape(name) + r"(?=[\\\s\"'])")
    for f, t in texts.items():
        rx = rx_py if f.endswith(".py") else rx_asm
        if rx.search(t): return True
    for cn, mn, s, e in cmds:
        if mn == name and any(re.search(r"\b" + re.escape(cn) + r"_command\b", t) for t in texts.values()): return True
    for cn, mn, s, e in cmds:      # another command macro of events.asm calls it
        if mn != name and re.search(r"^\t" + re.escape(name) + r"\b", ev[s:e], re.M): return True
    return False
dead = [(i, c) for i, c in enumerate(cmds) if not used(c[1])]
print(len(dead), "unused:", " ".join(c[1] for _, c in dead))
if "--delete" in sys.argv:
    drop = {i for i, _ in dead}
    out, last = "", 0
    for i, (cn, mn, s, e) in enumerate(cmds):
        if i in drop:
            out += ev[last:s]; last = e
    out += ev[last:]
    open(EV, "w").write(out)
    for i in sorted([entries[k] for k in drop], reverse=True):
        del sc[i]
    open(SC, "w").write("".join(sc))
    print("deleted")
