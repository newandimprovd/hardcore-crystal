#!/usr/bin/env python3
"""Viability audit of the 62 fourth-stage forms (read-only: changes no game data).

The design goal: every fourth stage must be competitively viable.  Crystal has no abilities, so viability comes from four things this
script measures from the generated data: stats (BST, speed tier, bulk), a strong STAB attack in the category of the better attacking
stat, enough coverage in that category, and a little utility (setup, recovery, status).  The moves counted are every level-up move
(all of them: a level 100 mon knows them) plus the TM/HM list of the species.

usage: audit_viability.py            writes docs/VIABILITY_AUDIT.md and prints the summary
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def rd(p):
    return open(os.path.join(ROOT, p)).read()


def move_ids():
    out, n = {}, -1
    for ln in rd("constants/move_constants.asm").splitlines():
        m = re.match(r"\s*const (\w+)", ln)
        if m:
            n += 1
            out[m[1]] = n
    return out


def move_table(ids):
    names = [k for k, v in sorted(ids.items(), key=lambda kv: kv[1]) if 1 <= v <= 251]
    rows = []
    for ln in rd("data/moves/moves.asm").splitlines():
        m = re.match(r"\s*move (\w+),\s*(\w+),\s*(\d+),\s*(\w+)\s*,\s*(\d+),\s*(\d+),\s*(\d+)", ln)
        if m:
            rows.append(dict(name=m[1], effect=m[2], power=int(m[3]), type=m[4], acc=int(m[5]), pp=int(m[6])))
    assert len(rows) == 251, len(rows)
    return {r["name"]: r for r in rows}


def special_set(ids):
    bits = []
    for ln in rd("data/hardcore/move_category_bits.asm").splitlines():
        m = re.match(r"\s*db (%[01]{8}(?:, %[01]{8})*)", ln)
        if m:
            bits += [int(b[1:], 2) for b in m[1].split(", ")]
    byid = {v: k for k, v in ids.items()}
    return {byid[i + 1] for i in range(251) if bits[i // 8] >> (i % 8) & 1 and (i + 1) in byid}


def tm_moves(slug):
    t = rd(f"data/pokemon/base_stats/{slug}.asm")
    m = re.search(r"^\s*tmhm (.*)$", t, re.M)
    return [x.strip() for x in m[1].split(",")] if m else []


RECOVERY = {"RECOVER", "SOFTBOILED", "MILK_DRINK", "MOONLIGHT", "SYNTHESIS", "MORNING_SUN", "REST", "WISH", "ROOST"}
SETUP = {"SWORDS_DANCE", "AGILITY", "AMNESIA", "CURSE", "BELLY_DRUM", "CALM_MIND", "NASTY_PLOT", "DRAGON_DANCE", "BULK_UP", "GROWTH",
         "HARDEN", "IRON_DEFENSE", "ACID_ARMOR", "BARRIER", "COSMIC_POWER", "QUIVER_DANCE", "SHELL_SMASH", "ROCK_POLISH", "COIL"}
STATUS = {"TOXIC", "THUNDER_WAVE", "WILL_O_WISP", "SLEEP_POWDER", "SPORE", "HYPNOSIS", "LOVELY_KISS", "STUN_SPORE", "SING", "GLARE",
          "SPIKES", "LEECH_SEED", "SUBSTITUTE", "PROTECT", "DESTINY_BOND", "PERISH_SONG", "TAUNT", "ENCORE", "SLEEP_TALK"}
CHARGE_OR_DRAWBACK = {"HYPER_BEAM", "GIGA_IMPACT", "SELFDESTRUCT", "EXPLOSION", "FOCUS_PUNCH", "SOLARBEAM", "SKY_ATTACK", "DREAM_EATER"}


def main():
    ids = move_ids()
    mv = move_table(ids)
    special = special_set(ids)
    roster = json.load(open(os.path.join(HERE, "roster/roster_out.json")))
    base = {r["const"]: r for r in roster}
    finals = [r for r in roster if r["stage"] == 4]
    rows = []
    for r in finals:
        hp, at, df, sp, sa, sd = r["stats"]
        slug = re.sub(r"_", "", r["const"]).lower()
        slug = r.get("slug") or slug
        try:
            tms = tm_moves(slug)
        except FileNotFoundError:
            tms = []
        known = {m for _, m in r["learnset"]} | set(tms)
        known = {m for m in known if m in mv}
        dmg = [mv[m] for m in known if mv[m]["power"] > 1 and mv[m]["name"] not in CHARGE_OR_DRAWBACK]
        side = "special" if sa > at else "physical"
        main = [m for m in dmg if (m["name"] in special) == (side == "special")]
        stab = [m for m in main if m["type"] in r["types"]]
        best_stab = max((m["power"] * min(100, m["acc"]) / 100 for m in stab), default=0)
        best_stab_name = max(stab, key=lambda m: m["power"] * min(100, m["acc"]), default={"name": "-"})["name"]
        cover = sorted({m["type"] for m in main if m["type"] not in r["types"] and m["power"] >= 60 and m["acc"] >= 85})
        other_side = [m for m in dmg if (m["name"] in special) != (side == "special") and m["type"] in r["types"] and m["power"] >= 80]
        rec = sorted(known & RECOVERY)
        setup = sorted(known & SETUP)
        status = sorted(known & STATUS)
        bst = sum(r["stats"])
        bulk = hp * (df + sd) / 1000.0
        problems = []
        if bst < 590:
            problems.append(f"BST {bst}")
        if best_stab < 75:
            problems.append(f"best {side} STAB only {best_stab:.0f} ({best_stab_name})")
        if len(cover) < 3:
            problems.append(f"coverage {len(cover)} type(s)")
        if not (rec or setup):
            problems.append("no recovery or setup")
        if sp < 60 and bulk < 25:
            problems.append("slow and frail")
        rows.append(dict(const=r["const"], types="/".join(sorted(set(r["types"]), key=r["types"].index)), bst=bst, spe=sp, side=side,
                         best=f"{best_stab_name} {best_stab:.0f}", cover=len(cover), rec=rec, setup=setup, status=len(status),
                         bulk=round(bulk), problems=problems, new=r["new"]))
    rows.sort(key=lambda r: (-len(r["problems"]), r["bst"]))
    n_bad = sum(1 for r in rows if r["problems"])
    out = ["# Fourth-stage viability audit (generated by tools/hardcore/audit_viability.py, read-only)", "",
           "Goal: every fourth stage is competitively viable. There are no abilities in Crystal, so viability here means stats, a strong STAB attack in the "
           "category of the better attacking stat, three or more coverage types in that category, and recovery or setup. Moves counted: every level-up move "
           "plus the TM/HM list. Charge, recharge and self-KO moves do not count as attacks.", "",
           f"{n_bad} of {len(rows)} forms have at least one flag.", "",
           "| Species | Types | BST | Spe | Bulk | Attacks as | Best STAB (power x acc) | Coverage types | Recovery / setup | Flags |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in rows:
        us = ", ".join(r["rec"] + r["setup"]) or "-"
        out.append(f"| {r['const']}{'*' if r['new'] else ''} | {r['types']} | {r['bst']} | {r['spe']} | {r['bulk']} | {r['side']} | {r['best']} | "
                   f"{r['cover']} | {us} | {'; '.join(r['problems']) or 'ok'} |")
    open(os.path.join(ROOT, "docs/VIABILITY_AUDIT.md"), "w").write("\n".join(out) + "\n")
    # summary
    from collections import Counter
    c = Counter(p.split(" ")[0] if not p.startswith("best") else "STAB" for r in rows for p in r["problems"])
    print(f"{n_bad} of {len(rows)} fourth stages flagged; flag counts: {dict(c)}")
    print("BST of final forms:", min(r["bst"] for r in rows), "-", max(r["bst"] for r in rows))
    print("worst 10:")
    for r in rows[:10]:
        print("  ", r["const"], r["types"], r["bst"], "|", "; ".join(r["problems"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
