#!/usr/bin/env python3
"""In-battle test of the physical/special split.

Starts a wild battle on Route 29 (test build, see testbuild.sh), then every turn pokes a different
move into the player's and the enemy's first slots and records which damage branch the engine
took (PlayerAttackDamage / EnemyAttackDamage .special vs .physicalcrit). The observed category for
every move is compared with the table the generator wrote.

usage: test_split.py ROM [max_turns]
"""
import importlib.util
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from gbtest import T

rom = sys.argv[1]
max_turns = int(sys.argv[2]) if len(sys.argv) > 2 else 400
root = __file__.rsplit("/tools/", 1)[0]
spec = importlib.util.spec_from_file_location("g", root + "/tools/hardcore/gen_moves.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
want = g.category_table()
ids = g.move_ids()
for old, new, *_ in g.NEW:
    ids[new] = ids[old]

# moves worth checking: damaging, accurate, not charge/multi-turn/static-damage
NAMES = ("SHADOW_BALL TACKLE THUNDERPUNCH FIRE_PUNCH ICE_PUNCH BITE CRUNCH PSYCHIC_M SURF EARTHQUAKE "
         "FLAMETHROWER THUNDERBOLT ICE_BEAM GUST WING_ATTACK SLUDGE_BOMB WATER_GUN EMBER SCRATCH "
         "FAIRY_WIND PLAY_ROUGH DAZZLE_GLEAM MOONBLAST DRAGON_CLAW DRAGON_PULSE DARK_PULSE NIGHT_SLASH "
         "AURA_SPHERE DRAIN_PUNCH BRICK_BREAK POISON_JAB BUG_BUZZ SHADOW_SNEAK BULLET_PUNCH ENERGY_BALL "
         "ICE_SHARD FLARE_BLITZ THUNDER_FANG FIRE_FANG ICE_FANG WOOD_HAMMER FLASH_CANNON X_SCISSOR "
         "POWER_GEM WILD_CHARGE EARTH_POWER AQUA_JET ZEN_HEADBUTT PSYCHO_CUT SHADOW_CLAW BRAVE_BIRD "
         "AQUA_TAIL IRON_HEAD HURRICANE STONE_EDGE CROSS_CHOP SLASH HEADBUTT SWIFT SPARK").split()
TEST = [ids[n] for n in NAMES]

log = {"player": {}, "enemy": {}}
turn = 0


def seen_all():
    seen = {m for s_ in log.values() for m in s_}
    return all(ids[n] in seen for n in NAMES)


def run_one(seed):
    """One emulator instance, one wild battle; stops when the battle ends or everything was seen."""
    global turn
    t = T(rom)
    state = {"menu": False}

    def mk(side, branch):
        def cb(ctx):
            mv = t.pb.memory[0xC60F] if side == "player" else t.mem("wEnemyMoveStructAnimation")
            log[side].setdefault(mv, set()).add(branch)
        return cb

    t.hook("PlayerAttackDamage.special", mk("player", "special"))
    t.hook("PlayerAttackDamage.physicalcrit", mk("player", "physical"))
    t.hook("EnemyAttackDamage.special", mk("enemy", "special"))
    t.hook("EnemyAttackDamage.physicalcrit", mk("enemy", "physical"))
    t.hook("BattleMenu", lambda ctx: state.__setitem__("menu", True))
    for i in range(600):
        t.pb.button("a" if i % 2 else "start", 4)
        t.tick(20)
        if t.mem("wMapGroup") and t.mem("wXCoord"):
            break
    t.tick(120)
    rnd = random.Random(seed)
    steps = 0
    while t.mem("wBattleMode") == 0 and steps < 3000:
        for n in ("wMornEncounterRate", "wDayEncounterRate", "wNiteEncounterRate"):
            t.poke(n, 255)
        t.press(rnd.choice(["up", "down", "left", "right"]), hold=16, wait=4)
        steps += 1
    if t.mem("wBattleMode") == 0:
        print("seed", seed, "no battle started, skipping")
        t.stop()
        return
    print("seed", seed, "battle after", steps, "steps at", t.where())
    frames = 0
    t0 = turn
    while frames < 80000:
        t.tick(10)
        frames += 10
        if t.mem("wBattleMode") == 0:
            break
        if not state["menu"]:
            t.pb.button("a", 4)
            continue
        state["menu"] = False
        mv = TEST[(turn + seed * 11) % len(TEST)]
        emv = TEST[((turn + seed * 11) * 7 + 3) % len(TEST)]
        t.poke("wBattleMonMoves", mv, 0)
        t.poke("wBattleMonPP", 30, 0)
        t.poke("wEnemyMonMoves", emv, 0)
        for i in (1, 2, 3):
            t.poke("wEnemyMonMoves", 0, i)
        t.poke("wEnemyMonPP", 30, 0)
        mh = t.mem("wBattleMonMaxHP", 0, 2)
        t.poke("wBattleMonHP", mh[0], 0); t.poke("wBattleMonHP", mh[1], 1)
        for n, v in (("wEnemyMonMaxHP", 999), ("wEnemyMonHP", 999)):
            t.poke(n, v >> 8, 0); t.poke(n, v & 0xFF, 1)
        t.poke("wCurMoveNum", 0)
        t.press("a", hold=4, wait=20)
        t.press("a", hold=4, wait=20)
        turn += 1
        if seen_all():
            break
    print("  turns this battle:", turn - t0)
    t.stop()


seed = 0
while seed < 12 and not seen_all():
    run_one(seed)
    seed += 1

bad = 0
checked = 0
for side in ("player", "enemy"):
    for mv, br in sorted(log[side].items()):
        exp = "special" if want.get(mv) == "Special" else "physical"
        checked += 1
        if br != {exp}:
            bad += 1
            print("MISMATCH", side, mv, "observed", br, "expected", exp)
seen = {m for s in log.values() for m in s}
print(f"turns {turn}; {checked} (side, move) pairs checked; {len(seen)} distinct moves seen of {len(TEST)}; mismatches {bad}")
missing = [n for n in NAMES if ids[n] not in seen]
print("never observed (missed or immune):", missing)
sys.exit(1 if bad else 0)
