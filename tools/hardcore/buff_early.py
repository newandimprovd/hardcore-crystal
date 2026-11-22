#!/usr/bin/env python3
"""Alpha 3.2 playtest point 11: the weak early lines have to fend for themselves until their evolution level.

Run as post-processing like the prune scripts, because gen_roster.py is not maintained against the removed data (a rerun would recreate
removed files).  Idempotent: every run starts from the line's stage totals and the moves it adds are skipped when they are there.

  * stage totals: the weak starts (Caterpie and Weedle at 230, the babies at 250, the small birds and rodents at 260 to 270) come up to the
    normal curve 300 / 395 / 485 / 565 (+35 HP on the last stage).  Magikarp stays at 200 on purpose, Gyarados at 25 is its whole point.
  * the cocoons (Metapod, Kakuna) get a spread that keeps the shell but is no longer a wall that cannot hurt anything.
  * moves: the cocoons and the early forms with a thin set of attacks learn damaging moves between their first level and their evolution level.
  * writes data/pokemon/base_stats/*.asm, data/pokemon/evos_attacks.asm and tools/hardcore/roster/roster_out.json (the party generator reads it).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

CURVE = [300, 395, 485, 565]
FINAL_HP_BONUS = 35
# lines brought to the normal curve (stage 1 total, and for the two bug lines every stage that was scaled by 0.96)
STAGE1_UP = ["PIDGEY", "RATTATA", "SENTRET", "HOOTHOOT", "SPEAROW", "ZUBAT", "PICHU", "CLEFFA", "IGGLYBUFF", "HOPPIP", "SWINUB",
             "MARILL", "SPINARAK"]
BUG_LINES = ["CATERPIE", "WEEDLE"]
# the cocoons keep a share of their vanilla shell spread (vanilla base stats) and the rest is spread evenly
COCOONS = {"METAPOD": [50, 20, 55, 30, 25, 25], "KAKUNA": [45, 25, 50, 35, 25, 25]}
COCOON_BLEND = 0.55

# (level, move) added to a species' learnset
ADD_MOVES = {
    "CATERPIE": [(7, "LEECH_LIFE"), (17, "HEADBUTT"), (21, "X_SCISSOR")],
    "WEEDLE": [(7, "LEECH_LIFE"), (16, "SLUDGE"), (21, "X_SCISSOR")],
    "METAPOD": [(27, "X_SCISSOR"), (33, "HEADBUTT"), (40, "BUG_BUZZ")],
    "KAKUNA": [(27, "X_SCISSOR"), (33, "POISON_JAB"), (40, "BUG_BUZZ")],
    "BUTTERFREE": [(50, "BUG_BUZZ"), (56, "HURRICANE")],
    "BEEDRILL": [(50, "X_SCISSOR"), (55, "POISON_JAB")],
    "PICHU": [(5, "QUICK_ATTACK"), (12, "SPARK"), (18, "SWIFT")],
    "CLEFFA": [(17, "DOUBLESLAP"), (21, "DAZZLE_GLEAM")],
    "IGGLYBUFF": [(12, "ROLLOUT"), (17, "DOUBLESLAP"), (21, "BODY_SLAM")],
    "SENTRET": [(13, "HYPER_FANG"), (21, "SLASH")],
    "HOPPIP": [(18, "RAZOR_LEAF")],
    "SPINARAK": [(20, "X_SCISSOR"), (26, "POISON_JAB")],
    "ARIADOS": [(28, "X_SCISSOR"), (32, "POISON_JAB")],
}


def distribute(props, total):
    s = sum(props)
    raw = [p / s * total for p in props]
    out = [max(5, min(255, int(r))) for r in raw]
    order = sorted(range(6), key=lambda i: raw[i] - int(raw[i]), reverse=True)
    i = 0
    while sum(out) < total:
        k = order[i % 6]
        if out[k] < 255:
            out[k] += 1
        i += 1
    while sum(out) > total:
        k = max(range(6), key=lambda j: out[j])
        out[k] -= 1
    return out


def main():
    path = HERE / "roster/roster_out.json"
    roster = json.loads(path.read_text())
    by = {m["const"]: m for m in roster}
    changes = []

    def restat(c, total):
        m = by[c]
        props = list(m["stats"])
        if m["stage"] == 4:
            props[0] -= FINAL_HP_BONUS  # the bonus is added again below, so a second run changes nothing
        if c in COCOONS:
            tot = sum(COCOONS[c])
            props = [COCOON_BLEND * p / tot + (1 - COCOON_BLEND) / 6 for p in COCOONS[c]]
        stats = distribute(props, total)
        if m["stage"] == 4:
            stats[0] = min(255, stats[0] + FINAL_HP_BONUS)
        if stats != m["stats"]:
            changes.append((c, m["stats"], stats))
            m["stats"] = stats

    for line in STAGE1_UP:
        restat(line, CURVE[0])
    for line in BUG_LINES:
        c = line
        while c:
            m = by[c]
            restat(c, CURVE[m["stage"] - 1])
            c = m["next"]
    # learnsets
    for c, adds in ADD_MOVES.items():
        m = by[c]
        have = {mv for _, mv in m["learnset"]}
        for lv, mv in adds:
            if mv not in have:
                m["learnset"].append([lv, mv])
        m["learnset"].sort(key=lambda x: x[0])
    path.write_text(json.dumps(roster, indent=1, ensure_ascii=False))

    # base stats files
    n_stats = 0
    for c, old, new in changes:
        slug = by[c]["name"].lower().replace(" ", "_")
        f = ROOT / f"data/pokemon/base_stats/{slug}.asm"
        t = f.read_text()
        t2 = re.sub(r"^\tdb\s+\d+,\s+\d+,\s+\d+,\s+\d+,\s+\d+,\s+\d+$", "\tdb " + ", ".join(f"{x:3d}" for x in new), t, count=1, flags=re.M)
        bexp = max(36, min(255, int(round(sum(new) * 0.38))))
        t2 = re.sub(r"^\tdb \d+ ; base exp", f"\tdb {bexp} ; base exp", t2, count=1, flags=re.M)
        assert t2 != t or old == new, c
        f.write_text(t2)
        n_stats += 1

    # evos_attacks.asm: insert the moves in level order into the species' block
    ea = ROOT / "data/pokemon/evos_attacks.asm"
    text = ea.read_text()
    n_moves = 0
    for c, adds in ADD_MOVES.items():
        label = "".join(p.capitalize() for p in by[c]["name"].split("_")) + "EvosAttacks"
        m = re.search(rf"^{label}:\n(.*?)\n\n", text, flags=re.M | re.S)
        assert m, label
        block = m.group(1).split("\n")
        i_end = block.index("\tdb 0 ; no more evolutions")
        moves = []
        for ln in block[i_end + 1:]:
            mm = re.match(r"\tdb (\d+), (\w+)$", ln)
            if mm:
                moves.append((int(mm.group(1)), mm.group(2)))
        have = {mv for _, mv in moves}
        for lv, mv in adds:
            if mv not in have:
                moves.append((lv, mv))
                n_moves += 1
        moves.sort(key=lambda x: x[0])  # stable: equal levels keep their order
        new_block = block[:i_end + 1] + [f"\tdb {lv}, {mv}" for lv, mv in moves] + ["\tdb 0 ; no more level-up moves"]
        text = text[:m.start(1)] + "\n".join(new_block) + text[m.end(1):]
    ea.write_text(text)

    # the line options of the generator, so that its own curve agrees with what this script did
    ro = HERE / "roster/roster_data.py"
    s = ro.read_text()
    for line in BUG_LINES + STAGE1_UP:
        s = re.sub(rf'^    "{line}": \{{[^\n]*\}},\n', "", s, flags=re.M)
    if "# alpha 3.2 point 11" not in s:
        s = s.replace("LINE_OPT = {", "LINE_OPT = {  # alpha 3.2 point 11: the weak starts of the other lines are on the normal curve now (tools/hardcore/buff_early.py)", 1)
    ro.write_text(s)
    print(f"{len(changes)} species restated, {n_moves} moves added")
    for c, old, new in changes:
        print(f"  {c:<11} {sum(old):3d} -> {sum(new):3d}  {new}")


if __name__ == "__main__":
    sys.exit(main())
