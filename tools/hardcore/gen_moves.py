#!/usr/bin/env python3
"""Hardcore Crystal move generator.

* Replaces 39 vanilla moves in place (same move ID, new constant, name, data,
  description and animation) using Pokemon Showdown data
  (tools/hardcore/showdown_moves.json, produced by dump_showdown.js).
* Remaps every use of a retired move in learnsets, trainers, egg moves, the
  Battle Tower and odd eggs to a surviving vanilla move; the AI move lists just
  lose the retired entries.
* Writes the per-move physical/special bit table the engine reads through
  GetMoveCategory (home/hardcore.asm).
* Retypes Charm, Sweet Kiss and Moonlight to Fairy.

Everything is regenerated from the files at the base commit, so it is safe to
run repeatedly.  Approximations (where the engine has no matching effect) are
listed in APPROX and printed at the end.
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "3bc8daa"


def base(path):
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"], text=True)


def write(path, text):
    (ROOT / path).write_text(text)


SD = json.load(open(ROOT / "tools/hardcore/showdown_moves.json"))

TYPE = {
    "Normal": "NORMAL", "Fighting": "FIGHTING", "Flying": "FLYING", "Poison": "POISON",
    "Ground": "GROUND", "Rock": "ROCK", "Bug": "BUG", "Ghost": "GHOST", "Steel": "STEEL",
    "Fire": "FIRE", "Water": "WATER", "Grass": "GRASS", "Electric": "ELECTRIC",
    "Psychic": "PSYCHIC_TYPE", "Ice": "ICE", "Dragon": "DRAGON", "Dark": "DARK",
    "Fairy": "FAIRY",
}

# retired constant -> (new constant, display name, showdown id, effect, animation label, description)
# The effect is chosen to match Showdown as closely as Crystal's effects allow.
NEW = [
    # --- Fairy ---
    ("VICEGRIP", "FAIRY_WIND", "FAIRY WIND", "fairywind", "NORMAL_HIT", "BattleAnim_Gust",
     ("A gentle gust of", "pixie dust.")),
    ("SUPER_FANG", "DRAIN_KISS", "DRAIN KISS", "drainingkiss", "LEECH_HIT", "BattleAnim_Absorb",
     ("A kiss that saps", "the foe's vigor.")),
    ("FURY_ATTACK", "PLAY_ROUGH", "PLAY ROUGH", "playrough", "ATTACK_DOWN_HIT", "BattleAnim_DoubleEdge",
     ("Cute, until it", "isn't. Hits hard.")),
    ("FURY_SWIPES", "DAZZLE_GLEAM", "DAZZLE GLEAM", "dazzlinggleam", "NORMAL_HIT", "BattleAnim_Flash",
     ("A blinding flash", "of fairy light.")),
    ("PIN_MISSILE", "MOONBLAST", "MOONBLAST", "moonblast", "SP_ATK_DOWN_HIT", "BattleAnim_Psybeam",
     ("Borrows the moon's", "power to strike.")),
    # --- the rest ---
    ("DRAGON_RAGE", "DRAGON_CLAW", "DRAGON CLAW", "dragonclaw", "NORMAL_HIT", "BattleAnim_Slash",
     ("Slashes the foe", "with sharp claws.")),
    ("SONICBOOM", "DRAGON_PULSE", "DRAGON PULSE", "dragonpulse", "NORMAL_HIT", "BattleAnim_Dragonbreath",
     ("A shock wave from", "the mouth.")),
    ("CONVERSION2", "DARK_PULSE", "DARK PULSE", "darkpulse", "FLINCH_HIT", "BattleAnim_Psybeam",
     ("A horrible aura", "that may flinch.")),
    ("CONVERSION", "NIGHT_SLASH", "NIGHT SLASH", "nightslash", "NORMAL_HIT", "BattleAnim_Slash",
     ("Slashes the foe", "off guard.")),
    ("PSYWAVE", "AURA_SPHERE", "AURA SPHERE", "aurasphere", "ALWAYS_HIT", "BattleAnim_Swift",
     ("A sphere of aura", "that never misses.")),
    ("COMET_PUNCH", "DRAIN_PUNCH", "DRAIN PUNCH", "drainpunch", "LEECH_HIT", "BattleAnim_MegaPunch",
     ("A punch that heals", "the user.")),
    ("LOW_KICK", "BRICK_BREAK", "BRICK BREAK", "brickbreak", "NORMAL_HIT", "BattleAnim_CrossChop",
     ("A swift chop that", "breaks bricks.")),
    ("TRIPLE_KICK", "FOCUS_BLAST", "FOCUS BLAST", "focusblast", "SP_DEF_DOWN_HIT", "BattleAnim_Dynamicpunch",
     ("Focus is unleashed", "in a huge blast.")),
    ("BARRAGE", "POISON_JAB", "POISON JAB", "poisonjab", "POISON_HIT", "BattleAnim_PoisonSting",
     ("A toxic tentacle", "or stinger jab.")),
    ("SPIKE_CANNON", "GUNK_SHOT", "GUNK SHOT", "gunkshot", "POISON_HIT", "BattleAnim_SludgeBomb",
     ("Hurls filthy gunk", "at the foe.")),
    ("SPIDER_WEB", "BUG_BUZZ", "BUG BUZZ", "bugbuzz", "SP_DEF_DOWN_HIT", "BattleAnim_Supersonic",
     ("Vibrates to make", "a damaging buzz.")),
    ("MIND_READER", "SHADOW_SNEAK", "SHADOW SNEAK", "shadowsneak", "PRIORITY_HIT", "BattleAnim_Lick",
     ("A shadow strikes", "first.")),
    ("CONSTRICT", "BULLET_PUNCH", "BULLET PUNCH", "bulletpunch", "PRIORITY_HIT", "BattleAnim_MachPunch",
     ("A punch as fast", "as a bullet.")),
    ("EGG_BOMB", "ENERGY_BALL", "ENERGY BALL", "energyball", "SP_DEF_DOWN_HIT", "BattleAnim_GigaDrain",
     ("A ball of natural", "energy.")),
    ("PRESENT", "ICE_SHARD", "ICE SHARD", "iceshard", "PRIORITY_HIT", "BattleAnim_PowderSnow",
     ("Hurls ice shards.", "Strikes first.")),
    ("DIZZY_PUNCH", "FLARE_BLITZ", "FLARE BLITZ", "flareblitz", "RECOIL_HIT", "BattleAnim_FlameWheel",
     ("A fiery charge", "that hurts you.")),
    ("LICK", "THUNDER_FANG", "THUNDER FANG", "thunderfang", "PARALYZE_HIT", "BattleAnim_Bite",
     ("Bites with", "electrified fangs.")),
    ("SLAM", "FIRE_FANG", "FIRE FANG", "firefang", "BURN_HIT", "BattleAnim_Bite",
     ("Bites with", "fiery fangs.")),
    ("BONE_CLUB", "ICE_FANG", "ICE FANG", "icefang", "FREEZE_HIT", "BattleAnim_Bite",
     ("Bites with", "frosty fangs.")),
    ("HORN_ATTACK", "WOOD_HAMMER", "WOOD HAMMER", "woodhammer", "RECOIL_HIT", "BattleAnim_Strength",
     ("Slams a rugged", "body into the foe.")),
    ("SMOKESCREEN", "FLASH_CANNON", "FLASH CANNON", "flashcannon", "SP_DEF_DOWN_HIT", "BattleAnim_ZapCannon",
     ("Gathers light and", "releases it.")),
    ("SHARPEN", "X_SCISSOR", "X-SCISSOR", "xscissor", "NORMAL_HIT", "BattleAnim_FuryCutter",
     ("Slashes the foe in", "an X shape.")),
    ("POWDER_SNOW", "POWER_GEM", "POWER GEM", "powergem", "NORMAL_HIT", "BattleAnim_Ancientpower",
     ("Beams of light", "from glowing gems.")),
    ("KARATE_CHOP", "WILD_CHARGE", "WILD CHARGE", "wildcharge", "RECOIL_HIT", "BattleAnim_TakeDown",
     ("Charges with", "electricity.")),
    ("ACID", "EARTH_POWER", "EARTH POWER", "earthpower", "SP_DEF_DOWN_HIT", "BattleAnim_Fissure",
     ("Makes the ground", "erupt beneath it.")),
    ("SMOG", "AQUA_JET", "AQUA JET", "aquajet", "PRIORITY_HIT", "BattleAnim_Waterfall",
     ("Strikes first with", "a jet of water.")),
    ("COTTON_SPORE", "ZEN_HEADBUTT", "ZEN HEADBUTT", "zenheadbutt", "FLINCH_HIT", "BattleAnim_Headbutt",
     ("A headbutt using", "mental focus.")),
    ("POISON_GAS", "PSYCHO_CUT", "PSYCHO CUT", "psychocut", "NORMAL_HIT", "BattleAnim_Slash",
     ("Tears with blades", "of psychic power.")),
    ("ROLLING_KICK", "SHADOW_CLAW", "SHADOW CLAW", "shadowclaw", "NORMAL_HIT", "BattleAnim_Scratch",
     ("Slashes with a", "claw of shadow.")),
    ("PECK", "BRAVE_BIRD", "BRAVE BIRD", "bravebird", "RECOIL_HIT", "BattleAnim_SkyAttack",
     ("A reckless dive", "that hurts you.")),
    ("VINE_WHIP", "AQUA_TAIL", "AQUA TAIL", "aquatail", "NORMAL_HIT", "BattleAnim_Waterfall",
     ("Swings a tail like", "a crashing wave.")),
    ("STOMP", "IRON_HEAD", "IRON HEAD", "ironhead", "FLINCH_HIT", "BattleAnim_Headbutt",
     ("Slams the foe with", "a steel head.")),
    ("SPITE", "HURRICANE", "HURRICANE", "hurricane", "CONFUSE_HIT", "BattleAnim_Twister",
     ("Wraps the foe in a", "fierce wind.")),
    ("BUBBLE", "STONE_EDGE", "STONE EDGE", "stoneedge", "NORMAL_HIT", "BattleAnim_RockSlide",
     ("Stabs with stones.", "Often a critical.")),
]
assert len(NEW) == 39, len(NEW)

# Moves whose engine effect cannot match Showdown exactly.
APPROX = {
    "DRAIN_KISS": "Crystal's leech effect drains 50%, Showdown 75%",
    "FLARE_BLITZ": "no burn chance; recoil is Crystal's 25%",
    "BRAVE_BIRD": "recoil is Crystal's 25%",
    "WOOD_HAMMER": "recoil is Crystal's 25%",
    "WILD_CHARGE": "recoil is Crystal's 25%",
    "THUNDER_FANG": "only the 10% paralysis, no flinch",
    "FIRE_FANG": "only the 10% burn, no flinch",
    "ICE_FANG": "only the 10% freeze, no flinch",
    "AURA_SPHERE": "always-hit effect",
    "BRICK_BREAK": "does not remove screens",
    "FOCUS_BLAST": "10% Special Defense drop kept",
    "SHADOW_SNEAK": "priority +1 through Crystal's priority effect",
}

# retired move -> surviving vanilla move used when learnsets/trainers/eggs reference it
REMAP = {
    "VICEGRIP": "TACKLE", "SUPER_FANG": "HYPER_FANG", "FURY_ATTACK": "TACKLE",
    "FURY_SWIPES": "SCRATCH", "PIN_MISSILE": "POISON_STING", "DRAGON_RAGE": "DRAGONBREATH",
    "SONICBOOM": "SWIFT", "CONVERSION2": "GROWL", "CONVERSION": "GROWTH", "PSYWAVE": "CONFUSION",
    "COMET_PUNCH": "DOUBLESLAP", "LOW_KICK": "DOUBLE_KICK", "TRIPLE_KICK": "DOUBLE_KICK",
    "BARRAGE": "DOUBLESLAP", "SPIKE_CANNON": "DOUBLESLAP", "SPIDER_WEB": "STRING_SHOT",
    "MIND_READER": "LOCK_ON", "CONSTRICT": "TACKLE", "EGG_BOMB": "SLASH", "PRESENT": "TACKLE",
    "DIZZY_PUNCH": "MEGA_PUNCH", "LICK": "SCRATCH", "SLAM": "BODY_SLAM", "BONE_CLUB": "BONEMERANG",
    "HORN_ATTACK": "TACKLE", "SMOKESCREEN": "SAND_ATTACK", "SHARPEN": "MEDITATE",
    "POWDER_SNOW": "ICY_WIND", "KARATE_CHOP": "DOUBLE_KICK", "ACID": "SLUDGE", "SMOG": "SLUDGE",
    "COTTON_SPORE": "STRING_SHOT", "POISON_GAS": "TOXIC", "ROLLING_KICK": "DOUBLE_KICK",
    "PECK": "WING_ATTACK", "VINE_WHIP": "RAZOR_LEAF", "STOMP": "HEADBUTT", "SPITE": "CONFUSE_RAY",
    "BUBBLE": "WATER_GUN",
}
RETIRED = [n[0] for n in NEW]
assert set(REMAP) == set(RETIRED)
assert not (set(REMAP.values()) & set(RETIRED))

# existing moves retyped to Fairy
RETYPE_FAIRY = ["CHARM", "SWEET_KISS", "MOONLIGHT"]

# critical hit list changes
CRIT_REMOVE = ["KARATE_CHOP"]
CRIT_ADD = ["NIGHT_SLASH", "STONE_EDGE", "SHADOW_CLAW", "PSYCHO_CUT"]

DATA_REMAP_FILES = [
    "data/pokemon/evos_attacks.asm",
    "data/pokemon/egg_moves.asm",
    "data/trainers/parties.asm",
    "data/battle_tower/parties.asm",
    "data/events/odd_eggs.asm",
]
AI_LIST_FILES = [
    "data/battle/ai/encore_moves.asm",
    "data/battle/ai/residual_moves.asm",
    "data/battle/ai/stall_moves.asm",
    "data/battle/ai/useful_moves.asm",
    "data/battle/ai/rain_dance_moves.asm",
    "data/battle/ai/sunny_day_moves.asm",
]


def camel(const):
    return "".join(p.capitalize() for p in const.split("_"))


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def word_sub(text, mapping):
    pat = re.compile(r"\b(" + "|".join(sorted(mapping, key=len, reverse=True)) + r")\b")
    return pat.sub(lambda m: mapping[m[1]], text)


def gen_move_data():
    text = base("data/moves/moves.asm")
    row = re.compile(r"^\tmove (\w+),\s*(\w+),\s*(\d+),\s*(\w+),\s*(\d+),\s*(\d+),\s*(\d+)\s*$")
    lines = text.splitlines()
    by_const = {}
    for i, ln in enumerate(lines):
        m = row.match(ln)
        if m:
            by_const[m[1]] = i
    for old, new, disp, sid, eff, anim, desc in NEW:
        s = SD[sid]
        acc = s["accuracy"] or 100
        power = s["basePower"]
        pp = min(s["pp"], 40)
        chance = s["secondary"]
        if eff in ("NORMAL_HIT", "ALWAYS_HIT", "PRIORITY_HIT", "RECOIL_HIT", "LEECH_HIT"):
            chance = 0
        if new in ("THUNDER_FANG", "FIRE_FANG", "ICE_FANG"):
            chance = 10
        if new == "FLARE_BLITZ":
            chance = 0
        if new == "PLAY_ROUGH":
            chance = 10
        if eff.endswith("_HIT") and eff not in ("NORMAL_HIT", "ALWAYS_HIT", "PRIORITY_HIT", "RECOIL_HIT", "LEECH_HIT"):
            assert chance, (new, eff)
        typ = TYPE[s["type"]]
        new_line = (f"\tmove {new + ',':<16} {'EFFECT_' + eff + ',':<30} {power:>3}, {typ + ',':<13} {acc:>3}, {pp:>2}, {chance:>3}")
        # keep the animation field equal to the move ID (GetMoveCategory relies on it)
        lines[by_const[old]] = new_line
    for const in RETYPE_FAIRY:
        i = by_const[const]
        lines[i] = re.sub(r"(,\s*)(NORMAL)(,\s*)", lambda m: m[1] + "FAIRY".ljust(len("NORMAL")) + m[3], lines[i], count=1) \
            if False else row_retype(lines[i], "FAIRY")
    write("data/moves/moves.asm", "\n".join(lines) + "\n")


def row_retype(line, new_type):
    m = re.match(r"^(\tmove \w+,\s*\w+,\s*\d+,\s*)(\w+)(,.*)$", line)
    return f"{m[1]}{(new_type + ',')[:-1].ljust(len(m[2]))}{m[3]}"


def gen_constants_names_desc_anim():
    ren = {old: new for old, new, *_ in NEW}
    # constants
    t = base("constants/move_constants.asm")
    for old, new in ren.items():
        t = re.sub(rf"(\tconst ){old}(\s*;)", lambda m: f"{m[1]}{new:<13}{m[2]}" if len(new) < 13 else f"{m[1]}{new} {m[2]}", t, count=1)
    write("constants/move_constants.asm", t)
    # names
    t = base("data/moves/names.asm")
    for old, new, disp, *_ in NEW:
        oldname = old.replace("_", " ")
        # vanilla display names: PSYCHIC_M and similar are not retired, so direct matching is enough
        cand = [f'\tli "{oldname}"\n']
        if old == "SONICBOOM":
            cand = ['\tli "SONICBOOM"\n']
        for c in cand:
            if c in t:
                t = t.replace(c, f'\tli "{disp}"\n', 1)
                break
        else:
            raise SystemExit(f"name not found for {old}")
    write("data/moves/names.asm", t)
    # descriptions
    t = base("data/moves/descriptions.asm")
    for old, new, disp, sid, eff, anim, desc in NEW:
        old_label = None
        m = re.search(rf"\n(\w+)Description:\n(?:\t(?:db|next) .*\n)+", t)
        # find the old label by the dw table order: entries correspond to move IDs
    ids = move_ids()
    dw = re.findall(r"\tdw (\w+Description)\n", t)
    for old, new, disp, sid, eff, anim, desc in NEW:
        old_label = dw[ids[old] - 1]
        new_label = camel(new) + "Description"
        assert len(desc[0]) <= 18 and len(desc[1]) <= 18, (new, desc)
        t = re.sub(rf"\tdw {old_label}\n", f"\tdw {new_label}\n", t, count=1)
        block = re.compile(rf"{old_label}:\n(?:\t(?:db|next) .*\n)+")
        assert block.search(t), old_label
        t = block.sub(f'{new_label}:\n\tdb   "{desc[0]}"\n\tnext "{desc[1]}@"\n', t, count=1)
    write("data/moves/descriptions.asm", t)
    # animations
    t = base("data/moves/animations.asm")
    anim_labels = set(re.findall(r"^(BattleAnim_\w+):", t, re.M))
    tbl = re.findall(r"\tdw (BattleAnim_\w+)\n", t.split("BattleAnimations::")[1].split("\n\n")[0])
    for old, new, disp, sid, eff, anim, desc in NEW:
        assert anim in anim_labels, anim
        old_label = tbl[ids[old]]  # entry 0 is BattleAnim_Dummy, so index == move ID
        head, rest = t.split("BattleAnimations::", 1)
        tblpart, tail = rest.split("\n\n", 1)
        tblpart = tblpart.replace(f"\tdw {old_label}\n", f"\tdw {anim}\n", 1) if f"\tdw {old_label}\n" in tblpart else tblpart.replace(f"\tdw {old_label}", f"\tdw {anim}", 1)
        t = head + "BattleAnimations::" + tblpart + "\n\n" + tail
    write("data/moves/animations.asm", t)
    # grammar list (cosmetic list of moves, keep IDs)
    t = base("data/moves/grammar.asm")
    t = word_sub(t, ren)
    write("data/moves/grammar.asm", t)
    # critical hit list
    t = base("data/moves/critical_hit_moves.asm")
    for c in CRIT_REMOVE:
        t = t.replace(f"\tdb {c}\n", "")
    t = t.replace("\tdb -1\n", "".join(f"\tdb {c}\n" for c in CRIT_ADD) + "\tdb -1\n")
    write("data/moves/critical_hit_moves.asm", t)


def move_ids():
    t = base("constants/move_constants.asm")
    ids = {}
    n = 0
    for ln in t.splitlines():
        m = re.match(r"\tconst (\w+)", ln)
        if m and not m[1].startswith("NO_MOVE") and not m[1].startswith("MOVE_"):
            pass
    # parse using the ';' hex comments, which vanilla keeps in sync with the ID
    for ln in t.splitlines():
        m = re.match(r"\tconst (\w+)\s*; ([0-9a-f]{2})\b", ln)
        if m:
            ids[m[1]] = int(m[2], 16)
    return ids


def remap_users():
    for f in DATA_REMAP_FILES:
        t = base(f)
        t = word_sub(t, REMAP)
        write(f, t)
    for f in AI_LIST_FILES:
        try:
            t = base(f)
        except subprocess.CalledProcessError:
            continue
        for r in RETIRED:
            t = re.sub(rf"^\tdb {r}\n", "", t, flags=re.M)
        write(f, t)


def category_table():
    """Return {move id: 'Physical'|'Special'|'Status'} for the final move set."""
    ids = move_ids()
    renamed = {old: new for old, new, *_ in NEW}
    new_sd = {new: sid for old, new, disp, sid, *_ in NEW}
    alias = {"PSYCHIC_M": "psychic", "FAINT_ATTACK": "feintattack", "HI_JUMP_KICK": "highjumpkick"}
    sd_by_norm = {norm(v["name"]): v for v in SD.values()}
    out = {}
    missing = []
    for const, mid in sorted(ids.items(), key=lambda kv: kv[1]):
        if mid < 1 or mid > 251:
            continue
        cur = renamed.get(const, const)
        if cur in new_sd:
            s = SD[new_sd[cur]]
        else:
            key = alias.get(const) or norm(const)
            s = SD.get(key) or sd_by_norm.get(norm(const))
        if s is None:
            missing.append(const)
            continue
        out[mid] = s["category"]
    assert not missing, missing
    assert set(out) == set(range(1, 252)), sorted(set(range(1, 252)) - set(out))
    return out


def gen_categories():
    out = category_table()
    bits = [0] * 32
    for mid, cat in out.items():
        if cat == "Special":
            bits[(mid - 1) // 8] |= 1 << ((mid - 1) % 8)
    lines = ["; Generated by tools/hardcore/gen_moves.py: one bit per move ID (bit 0 of byte 0 = move 1).",
             "; A set bit means the move is special; clear means physical (status moves are clear).",
             "MoveCategoryBits::"]
    for i in range(0, 32, 4):
        lines.append("\tdb " + ", ".join(f"%{b:08b}" for b in bits[i:i + 4]))
    write("data/hardcore/move_category_bits.asm", "\n".join(lines) + "\n")
    n_spec = sum(1 for c in out.values() if c == "Special")
    n_phys = sum(1 for c in out.values() if c == "Physical")
    return n_spec, n_phys


if __name__ == "__main__":
    Path(ROOT / "data/hardcore").mkdir(exist_ok=True)
    gen_move_data()
    gen_constants_names_desc_anim()
    remap_users()
    s, p = gen_categories()
    print(f"moves replaced: {len(NEW)}; special {s}, physical {p}")
    print("approximations:")
    for k, v in APPROX.items():
        print(f"  {k}: {v}")
