"""Shared building blocks for the five areas: acts (a run of lanes ending in a plaza), town interiors, bosses."""
import random

from .flags import flag_once
from . import boutique as shops
from .layout import (FACE, boss_room, chain, gatehouse, house_interior, boutique_interior, lane, mart_interior, plaza, pokecenter_interior)
from .town import plaza2
from .wayfolk import GIFT, GIFT_AFTER, GIFT_HERMITS, GIFT_ITEMS, HERMIT, TOWNIE, TOWNIE2
from .trail import trail
from . import hollows
from . import turn
from .party import make_party
from .text import Text


class BossSpec:
    """A boss at the end of an act. level is the highest level of the party, size the party size."""

    def __init__(self, room, name, cls, sprite, pal, level, size, seen, beaten, after, template="karen",
                 item=None, theme=None, landmark=None, music="MUSIC_GYM", open_exit=False, story=0):
        self.room, self.name, self.cls, self.sprite, self.pal = room, name, cls, sprite, pal
        self.level, self.size = level, size
        self.seen, self.beaten, self.after = seen, beaten, after
        self.template, self.item, self.theme = template, item, theme
        self.landmark, self.music, self.open_exit = landmark, music, open_exit
        self.story = story  # 2 = the rival (the crater), 3 = the final boss: scripts in engine/hardcore/story.asm


class ActSpec:
    """lanes lanes of `trainers` fighters each, then a plaza (Pokecenter, Mart, a house, the boss door)."""

    def __init__(self, tag, lanes, kit, landmark, music, trainers=13, gate=None, boss=None, houses=1,
                 mart=None, texts=None, plaza_width=13, lane_names=None, split=None, pal="PALETTE_DAY", rift=False,
                 split_houses=1, boutique=None):
        self.index = 0  # the act's place in its area (0..2), set by build_area
        self.spec = None  # the area spec (level range), set by build_area
        self.boutique = boutique  # 0..2: the mid-act plaza gets the rare held-item boutique of this act (areas/boutique.py)
        self.pal = pal
        self.rift = rift  # the end plaza of this act gets a door to PURGATORIO (it needs a plaza width of 15)
        self.split_houses = split_houses
        self.tag, self.lanes, self.kit, self.landmark, self.music = tag, lanes, kit, landmark, music
        self.split = split  # a second, smaller plaza (Pokecenter, Mart, house) after this many lanes
        self.trainers, self.gate, self.boss, self.houses = trainers, gate, boss, houses
        self.mart, self.texts, self.plaza_width = mart, texts or {}, plaza_width
        self.lane_names = lane_names


# TMs come in a fixed order, weak and handy ones first, so the player keeps finding better ones as the world opens up.
TM_ORDER = [
    "HEADBUTT", "ROCK_SMASH", "DOUBLE_TEAM", "SWAGGER", "SNORE", "SLEEP_TALK", "REST", "DEFENSE_CURL", "MUD_SLAP",
    "DETECT", "ENDURE", "PROTECT", "FURY_CUTTER", "ATTRACT", "THIEF", "ROLLOUT", "SWIFT", "FIRE_PUNCH", "ICE_PUNCH",
    "THUNDERPUNCH", "ICY_WIND", "SWEET_SCENT", "SUNNY_DAY", "RAIN_DANCE", "SANDSTORM", "IRON_TAIL", "STEEL_WING",
    "DRAGONBREATH", "GIGA_DRAIN", "CURSE", "TOXIC", "NIGHTMARE", "DREAM_EATER", "ROAR", "PSYCH_UP", "DIG",
    "SLUDGE_BOMB", "SOLARBEAM", "SHADOW_BALL", "PSYCHIC_M", "THUNDER", "FIRE_BLAST", "BLIZZARD", "EARTHQUAKE",
    "ZAP_CANNON", "HIDDEN_POWER", "FRUSTRATION", "RETURN", "DYNAMICPUNCH", "HYPER_BEAM",
]
# What the other pickups are, by how far through the game the lane is (global lane counter).
PICKUPS = [
    ["POTION", "ANTIDOTE", "POKE_BALL", "PARLYZ_HEAL", "AWAKENING", "ETHER"],
    ["SUPER_POTION", "GREAT_BALL", "BURN_HEAL", "ICE_HEAL", "REVIVE", "ETHER", "REPEL"],
    ["HYPER_POTION", "ULTRA_BALL", "FULL_HEAL", "REVIVE", "MAX_REPEL", "ELIXER", "MAX_ETHER"],
]


def pickup(w, m, reserve=0, total_lanes=75):
    """Put one item ball in lane m: a TM on three lanes out of four (in TM_ORDER), else a consumable by progress.
    Uses its own random generator so the existing layout stays exactly as it was."""
    import random
    if len(m.objects) + reserve + 1 > 15:  # no room: trainers are added after this call, so they are counted in `reserve`
        return None
    rnd = random.Random("pickup:" + m.name)
    n = getattr(w, "pickups", 0)
    w.pickups = n + 1
    idx = n // 4 * 3 + n % 4
    if n % 4 != 3 and idx < len(TM_ORDER):
        item = "TM_" + TM_ORDER[idx]
    else:
        tier = min(2, n * 3 // total_lanes)
        item = rnd.choice(PICKUPS[tier])
    a, cw = m.a, m.cw
    taken = {(o["x"], o["y"]) for o in m.objects}
    cells = [(x, y) for y in range(5, 2 * m.h - 8, 2) for x in range(2 * a + 1, 2 * (a + cw) - 1)
             if (x, y) not in taken]
    if hasattr(m, "corridor"):
        cells = [(x, 2 * r + dy) for r in range(2, m.h - 3) for dy in (0, 1) for x in range(2 * m.corridor[r] + 1, 2 * (m.corridor[r] + cw) - 1)
                 if (x, 2 * r + dy) not in taken]
    gl = [cl for gd in getattr(m, "glades", []) for cl in gd["cells"] if cl not in taken]
    if gl:  # the ball is the reward for leaving the road: it lies in a glade
        cells = gl
    x, y = rnd.choice(cells)
    flag = w.flag(f"EVENT_GEN_{m.const}_PICKUP")
    m.scripts.append(f"{m.name}Pickup:\n\titemball {item}\n")
    m.obj(x, y, "SPRITE_POKE_BALL", "SPRITEMOVEDATA_STILL", f"{m.name}Pickup", otype="OBJECTTYPE_ITEMBALL", flag=flag)
    return item


HIDDEN = [["ETHER", "ANTIDOTE", "REVIVE", "AWAKENING"], ["ETHER", "ELIXER", "REVIVE", "PP_UP"], ["MAX_ETHER", "ELIXER", "MAX_REVIVE", "PP_UP"]]
NPC_PALS = ["PAL_NPC_BROWN", "PAL_NPC_GREEN", "PAL_NPC_BLUE", "PAL_NPC_RED", "PAL_NPC_PINK"]


def people_sprites(g):
    """The overworld sprites a group's outdoor maps can show (its sprite list) that are people."""
    return [sp for sp in g.sprites if sp not in ("SPRITE_POKE_BALL", "SPRITE_ROCK", "SPRITE_BOULDER", "SPRITE_FRUIT_TREE")]


def area_tag(m):
    return next(t for t in ("Tithe", "Grove", "Axiom", "Lotus", "Dis") if m.name.startswith(t))


def furnish_lane(w, g, m, reserve, total_lanes=75):
    """What a glade holds besides the item ball: a hermit who talks (if the lane has an object left) and a hidden item under the
    ground (a bg event, which costs no object).  Own random generator, seeded by the map name."""
    import random
    from .people import plain_npc
    R = random.Random("furnish:" + m.name)
    cells = [cl for gd in getattr(m, "glades", []) for cl in gd["cells"]]
    if not cells:
        return
    taken = {(o["x"], o["y"]) for o in m.objects}
    cells = [cl for cl in cells if cl not in taken]
    tier = min(2, w.hidden * 3 // total_lanes) if hasattr(w, "hidden") else 0
    w.hidden = getattr(w, "hidden", 0)
    if R.random() < 0.8:
        x, y = R.choice(cells)
        cells.remove((x, y))
        item = R.choice(HIDDEN[tier])
        flag = w.flag(f"EVENT_GEN_{m.const}_HIDDEN")
        m.scripts.append(f"{m.name}Hidden:\n\thiddenitem {item}, {flag}\n")
        m.bg(x, y, "BGEVENT_ITEM", f"{m.name}Hidden")
        w.hidden += 1
    if len(m.objects) + reserve + 1 <= 15 and cells:
        x, y = R.choice(cells)
        tag = area_tag(m)
        sp = R.choice(people_sprites(g))
        queue = gift_queue(w)[tag]
        lane = int(m.name[len(tag) + 6:]) if m.name.startswith(tag + "Street") else 0
        if queue and queue[0][0] <= lane:  # a hermit with a present is due in this area: this glade's hermit is him
            _, item, speech, after = queue.pop(0)
            gift_hermit(w, m, x, y, sp, R.choice(NPC_PALS), R.choice(["LEFT", "RIGHT", "UP", "DOWN"]), f"{m.name}GiftHermit", item, speech, after)
        else:
            plain_npc(m, x, y, sp, R.choice(NPC_PALS), R.choice(["LEFT", "RIGHT", "UP", "DOWN"]), f"{m.name}Hermit", R.choice(HERMIT[tag]))


def gift_queue(w):
    """The gift hermits still to be placed, per area, in lane order (areas/wayfolk.py GIFT_HERMITS); emit.py checks that none is left over."""
    if not hasattr(w, "gift_hermits"):
        w.gift_hermits = {t: [] for t in ("Tithe", "Grove", "Axiom", "Lotus", "Dis")}
        for tag, lane, item, speech, after in GIFT_HERMITS:
            w.gift_hermits[tag].append((lane, item, speech, after))
        for q in w.gift_hermits.values():
            q.sort(key=lambda e: e[0])
    return w.gift_hermits


def gift_hermit(w, m, x, y, sprite, pal, face, label, item, speech, after):
    """A hermit in a glade who hands over one item (a charm or a stat item) without a fight, once."""
    flag = w.flag(f"EVENT_GEN_{m.const}_HGIFT")
    m.scripts.append(
        f"{label}:\n\tfaceplayer\n\topentext\n\tcheckevent {flag}\n\tiftrue .Done\n\twritetext {label}Text\n\twaitbutton\n"
        f"\tverbosegiveitem {item}\n\tiffalse .NoRoom\n\tsetevent {flag}\n"
        f".Done:\n\twritetext {label}AfterText\n\twaitbutton\n\tclosetext\n\tend\n\n"
        f".NoRoom:\n\twritetext {label}NoRoomText\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(Text(speech).emit(f"{label}Text"))
    m.scripts.append(Text(after).emit(f"{label}AfterText"))
    m.scripts.append(Text("Your bag is full. The gift will wait. So will I. I have nothing else on.").emit(f"{label}NoRoomText"))
    m.obj(x, y, sprite, FACE[face], label, pal=pal)


def crowd(w, g, m, n=9, plaza_no=1):
    """Townsfolk for a plaza: n talkers on its free floor cells (from the front of the seeded list; cameos take from the end).  The first
    is the plaza's gift-giver (areas/wayfolk.py GIFT: a named stranger who hands over one item, once), the rest plain talkers."""
    import random
    from .people import plain_npc
    R = random.Random("crowd:" + m.name)
    tag = area_tag(m)
    if not hasattr(m, "npc_cells"):  # the box plaza of the Johto road has no seeded cell list
        return
    if debate_pair(m, g, tag, plaza_no):
        n -= 2  # the debaters are two of the plaza's talkers
    n = min(n, 15 - len(m.objects) - 3)  # three object slots stay free for the cameos
    lines = list(TOWNIE[tag]) + list(TOWNIE2[tag])
    R.shuffle(lines)
    for i, (x, y) in enumerate(m.npc_cells[:n]):
        sp = R.choice(people_sprites(g))
        pal = R.choice(NPC_PALS)
        face = R.choice(["LEFT", "RIGHT", "UP", "DOWN"])
        if i == 0:
            giver(w, m, x, y, sp, pal, face, f"{m.name}Giver", GIFT[tag][plaza_no % 4], GIFT_ITEMS[(plaza_no - 1) % len(GIFT_ITEMS)],
                  GIFT_AFTER[plaza_no % len(GIFT_AFTER)])
        else:
            plain_npc(m, x, y, sp, pal, face, f"{m.name}Townie{i}", lines[i % len(lines)])
    m.npc_cells = m.npc_cells[n:]


def debate_pair(m, g, tag, plaza_no):
    """Two townsfolk who stand side by side facing each other and argue (areas/debates.py: seven pairs per area, the plaza number picks one)."""
    import random
    from .debates import DEBATES
    from .people import plain_npc
    if 15 - len(m.objects) - 3 < 5:
        return False
    cells = set(m.npc_cells)
    pair = next(((x, y) for (x, y) in m.npc_cells if (x + 1, y) in cells), None)
    if not pair:
        return False
    x, y = pair
    R = random.Random("debate:" + m.name)
    left, right = DEBATES[tag][(plaza_no - 1) % len(DEBATES[tag])]
    for (cx, cy, face, text, tail) in ((x, y, "RIGHT", left, "A"), (x + 1, y, "LEFT", right, "B")):
        plain_npc(m, cx, cy, R.choice(people_sprites(g)), R.choice(NPC_PALS), face, f"{m.name}Debate{tail}", text)
    m.npc_cells = [c for c in m.npc_cells if c not in ((x, y), (x + 1, y))]
    return True


def giver(w, m, x, y, sprite, pal, face, label, gift, item, after):
    """A stranger who introduces himself with a name built like a Pokemon's (a pun and what it is made of) and gives one item, once."""
    name, etym, offer = gift
    flag = w.flag(f"EVENT_GEN_{m.const}_GIFT")
    m.scripts.append(
        f"{label}:\n\tfaceplayer\n\topentext\n\tcheckevent {flag}\n\tiftrue .Done\n\twritetext {label}Text\n\twaitbutton\n"
        f"\tverbosegiveitem {item}\n\tiffalse .NoRoom\n\tsetevent {flag}\n"
        f".Done:\n\twritetext {label}AfterText\n\twaitbutton\n\tclosetext\n\tend\n\n"
        f".NoRoom:\n\twritetext {label}NoRoomText\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(Text(f"I'm {name}. {etym} {offer}").emit(f"{label}Text"))
    m.scripts.append(Text(after).emit(f"{label}AfterText"))
    m.scripts.append(Text("Your bag is full. The gift will wait. So will I.").emit(f"{label}NoRoomText"))
    m.obj(x, y, sprite, FACE[face], label, pal=pal)


def make_plaza(g, name, kit, rng, *, index=0, width=None, **kw):
    """The street town of the area tilesets (town.py); the old box plaza for the vanilla tilesets (the Johto road)."""
    if kit.extra.get("scn"):
        return plaza2(g, name, kit, rng, index=index, **kw)
    return plaza(g, name, kit, rng, width=width or 13, **kw)


def pick(lst, i):
    return Text(lst[i % len(lst)]) if lst else None


def town(w, g, tag, n, p, doors, kit, landmark, spawn_const, mart_items, texts, martconst, reminders=None, boutique=None):
    """Pokecenter, Mart and house interiors for plaza p (doors from layout.plaza). texts: dict of lists.
    reminders: optional (pokecenter text, mart text) that replace the random picks, used for the rules reminders."""
    w.spawns.append((spawn_const, p, *p.spawn_cell))
    w.marts.append((martconst, f"Mart{tag}{n}", mart_items))
    center = [pick(texts.get("center", []), n * 3 + i) for i in range(1)]
    if reminders:
        center = [Text(reminders[0])]
    pokecenter_interior(g, f"{tag}Pokecenter{n}", doors["center"], landmark, [t for t in center if t])
    mart = [pick(texts.get("mart", []), n * 2)]
    if reminders:
        mart = [Text(reminders[1])]
    mart_interior(g, f"{tag}Mart{n}", doors["mart"], landmark, martconst, [t for t in mart if t])
    for i, hd in enumerate(doors["houses"]):
        h = [pick(texts.get("house", []), n * 2 + i), pick(texts.get("house", []), n * 2 + i + 5)]
        if boutique and i == len(doors["houses"]) - 1:  # the last house door is the shop
            w.marts.append((f"{martconst}B", f"Mart{tag}{n}Boutique", boutique["items"]))
            boutique_interior(g, f"{tag}Boutique{n}", hd, landmark, f"{martconst}B", boutique["greet"], [t for t in h[:1] if t])
            continue
        house_interior(g, f"{tag}House{n}" if i == 0 else f"{tag}House{n}b", hd, landmark, [t for t in h if t])
    crowd(w, g, p, plaza_no=n)


def boss_party(roster, rng, boss, theme):
    return make_party(roster, rng, boss.level, boss.size, boss.theme or theme)


def turn_plan(w, act):
    """{lane index: 'E' or 'W'}: the lane of this act that runs sideways (alpha 3.2 point 19).  One per act that is long enough, never the
    first lane (it carries the gate), never the lane of a hidden portal (Purgatorio, the Undercroft),
    and never the lane before a mid-act plaza.  East and west alternate through the world."""
    if act.lanes < 4 or not act.kit.extra.get("scn"):
        return {}
    gone = set()
    if act.rift:
        gone.add(act.lanes - 1)
    if act.tag == "Axiom" and not act.rift:
        gone.add(act.lanes - 2)
    ok = [i for i in range(1, act.lanes - 1) if i not in gone and not (act.split and i + 1 == act.split)]
    if not ok:
        return {}
    R = random.Random("turn:" + act.tag + str(w.turn_count if hasattr(w, "turn_count") else 0) + str(act.lanes))
    i = R.choice(ok)
    w.turn_count = getattr(w, "turn_count", 0) + 1
    return {i: "EW"[w.turn_count % 2]}


def turned_lane(w, g, rng, act, below, name, trainers, direction, lane_no):
    """One lane that runs east (direction 'E') or west ('W'), with a bend map before it and one after it that join it to the vertical road.
    Returns (lane, trainer slots, the last bend), all connected."""
    from . import counts
    kit, tag = act.kit, act.tag
    k = 1 if direction == "E" else 3
    cw, W, BH = 3, 12, 14
    R = random.Random("turnlane:" + name)
    east = direction == "E"
    lane_side_in = "W" if east else "E"
    # the bend before: the road comes up from below on the column the previous map ends on and turns to the lane's side
    a1 = max(1, min(W - cw - 1, turn.edges_of(below)[1][1]))
    b1 = turn.bend(g, f"{tag}BendA{lane_no}", kit, kind="R" if east else "L", a=a1, r_t=R.randint(2, 4), landmark=act.landmark,
                   music=act.music, cw=cw, pal=act.pal)
    furnish_lane(w, g, b1, reserve=0)
    turn.rotate(b1, [], kit, 0, R)
    turn.join(below, b1)
    # the lane, built like any other and then turned: its entry (west for an eastbound lane) meets the exit row of the bend
    rows = trainers - trainers // 3
    H = rows * counts.GAP + 7
    a_lane = turn.arg_for(lane_side_in, b1.exit[1], cw, W, H, k)
    m, s = trail(g, name, kit, rng, trainers=trainers, landmark=act.landmark, a=a_lane, music=act.music, neck=0, gate=None, w=w,
                 pal=act.pal, raw=True)
    m.entry, m.exit = ("S", m.a), ("N", m.a_out)
    pickup(w, m, reserve=len(s))
    furnish_lane(w, g, m, reserve=len(s))
    turn.rotate(m, s, kit, k, R)
    assert m.entry[0] == lane_side_in, (name, m.entry)
    turn.join(b1, m)
    # the bend after: from the lane's far side back to the vertical road
    k2 = 1 if east else 3
    a2 = turn.arg_for("W" if east else "E", m.exit[1], cw, W, BH, k2)
    b2 = turn.bend(g, f"{tag}BendB{lane_no}", kit, kind="L" if east else "R", a=a2, r_t=R.randint(2, 4), landmark=act.landmark,
                   music=act.music, cw=cw, pal=act.pal)
    furnish_lane(w, g, b2, reserve=0)
    turn.rotate(b2, [], kit, k2, R)
    assert b2.exit[0] == "N", (b2.name, b2.exit)
    turn.join(m, b2)
    return m, s, b2


def build_act(w, g, rng, roster, act, prev, plaza_no, lane_no, area_theme, stocks):
    """Builds act.lanes lanes north of `prev` (a plaza), a mid-act plaza after act.split lanes if asked, then the
    final plaza with its interiors and boss room. stocks: Mart item lists, one per plaza built here.
    Returns (lanes, plaza, doors, boss_info, next lane number, next plaza number)."""
    kit, tag = act.kit, act.tag
    lanes = []
    below = prev
    stocks = list(stocks)
    turns = turn_plan(w, act)
    hollow = hollows.lanes_for(act, turns)  # lanes that hide a hollow behind a gap in the tree line (areas/hollows.py)
    for i in range(act.lanes):
        first = i == 0
        gate = act.gate if first else None
        tr = act.trainers[i] if isinstance(act.trainers, (list, tuple)) else act.trainers
        if i in turns:
            m, s, below = turned_lane(w, g, rng, act, below, f"{tag}Street{lane_no}", tr, turns[i], lane_no)
            lanes.append((m, s))
            lane_no += 1
            if act.split and i + 1 == act.split:
                raise AssertionError("a turned lane may not be the last lane before a mid-act plaza")
            continue
        if kit.extra.get("scn"):
            m, s = trail(g, f"{tag}Street{lane_no}", kit, rng, trainers=tr, landmark=act.landmark, a=turn.edges_of(below)[1][1],
                         music=act.music, neck=2 if gate else 0, gate=gate, w=w, pal=act.pal,
                         rift=bool(act.rift) and i == act.lanes - 1,
                         vault=(tag == "Axiom" and not act.rift and i == act.lanes - 2 and not hasattr(w, "vault_door")),
                         hollow=i in hollow)
        else:
            la = rng.choice((1, 2, 3, 4))  # the road drifts sideways from lane to lane, so it winds instead of running straight north
            m, s = lane(g, f"{tag}Street{lane_no}", kit, rng, trainers=tr, landmark=act.landmark, a=la, right=6 - la,
                        music=act.music, neck=2 if gate else 0, gate=gate, w=w, pal=act.pal)
        if getattr(m, "hollow_door", None) is not None:
            hollows.register(w, act, i, hollow[i], m)
        if getattr(m, "vault_door", None) is not None:
            w.vault_door = m.vault_door  # the hidden portal to the Undercroft (areas/vault.py), found in a glade
        pickup(w, m, reserve=len(s))
        furnish_lane(w, g, m, reserve=len(s))
        turn.join(below, m)
        lanes.append((m, s))
        below = m
        lane_no += 1
        if act.split and i + 1 == act.split:
            nh = act.split_houses + (1 if act.boutique is not None else 0)
            pm, dm = make_plaza(g, f"{tag}Plaza{plaza_no}", kit, rng, landmark=act.landmark, music=act.music,
                                houses=nh, width=max(act.plaza_width, 2 * (2 + nh) + 9), pal=act.pal, index=plaza_no)
            turn.join(below, pm)
            town(w, g, tag, plaza_no, pm, dm, kit, act.landmark, f"{tag.upper()}_{plaza_no}", stocks.pop(0), act.texts,
                 f"{tag.upper()}_{plaza_no}", boutique=shops.spec(tag, act.boutique) if act.boutique is not None else None)
            below = pm
            plaza_no += 1
    p, doors = make_plaza(g, f"{tag}Plaza{plaza_no}", kit, rng, landmark=act.landmark, music=act.music,
                          houses=act.houses, extra=1 if act.boss else 0, width=act.plaza_width, pal=act.pal,
                          index=plaza_no)
    turn.join(below, p)
    if act.rift:
        # the way into Purgatorio is the hidden portal in a glade of the last lane before the plaza, not a door in the town
        hidden = lanes[-1][0]
        door = hidden.rift_door
        short = "A" + g.key[-1]
        flag = flag_once(w, f"EVENT_PURG_OPEN_{short}")
        hidden.coords.append((door.x, door.y + 1, -1, f"{hidden.name}PurgFlagScript"))
        hidden.scripts.append(f"{hidden.name}PurgFlagScript:\n\tsetevent {flag}\n\tend\n")
        if not hasattr(w, "purg_doors"):
            w.purg_doors = {}
        w.purg_doors[short] = door
    town(w, g, tag, plaza_no, p, doors, kit, act.landmark, f"{tag.upper()}_{plaza_no}", stocks.pop(0), act.texts,
         f"{tag.upper()}_{plaza_no}")
    plaza_no += 1
    info = None
    if act.boss:
        b = act.boss
        party = boss_party(roster, rng, b, area_theme)
        boss = dict(cls=b.cls, sprite=b.sprite, pal=b.pal, name=b.name, party=party, seen=Text(b.seen),
                    beaten=Text(b.beaten), after=Text(b.after))
        room, exits = boss_room(g, w, b.room, doors["extra"][0], b.landmark or act.landmark, b.music, b.template,
                                boss, item=b.item, open_exit=b.open_exit, story=b.story)
        info = (room, boss, exits)
    return lanes, p, doors, info, lane_no, plaza_no


def start_plaza(w, g, rng, kit, tag, landmark, music, texts, stock, entry_doors, gate_name, gate_text, pal="PALETTE_DAY"):
    """First plaza of an area (south side closed), reached through a gate house from the unlinked doors
    `entry_doors` of the previous area's last boss room. Returns the plaza."""
    p, d = make_plaza(g, f"{tag}Plaza1", kit, rng, landmark=landmark, music=music, houses=1, south="gate", pal=pal, index=1)
    gatehouse(g, gate_name, entry_doors, d["south"], landmark, music, [Text(gate_text)])
    town(w, g, tag, 1, p, d, kit, landmark, f"{tag.upper()}_1", stock, texts, f"{tag.upper()}_1")
    return p


class AreaCfg:
    """Everything that makes one area different. Acts are built three at a time: boss1 gives the key item for
    the gate of act 2, boss2 the one for the gate of act 3, boss3 ends the area."""

    def __init__(self, key, tag, spec, kit, pal, landmarks, music, texts, tiers, bosses, gates, splits,
                 gate_name, gate_text, stock_ix=(0, 0, 1, 1, 2, 2, 2), lanes=(5, 5, 5), trainers=(13, 13, 13),
                 split_houses=(1, 1, 1), purg=True):
        self.split_houses = split_houses
        self.purg = purg  # the end plaza of act 2 gets a door into PURGATORIO
        self.trainers = trainers  # per act: one number for every lane, or a list with one number per lane
        self.key, self.tag, self.spec, self.kit, self.pal = key, tag, spec, kit, pal
        self.landmarks, self.music, self.texts, self.tiers = landmarks, music, texts, tiers
        self.bosses, self.gates, self.splits = bosses, gates, splits
        self.gate_name, self.gate_text, self.stock_ix, self.lanes = gate_name, gate_text, stock_ix, lanes


def build_area(w, roster, rng, cfg, entry_doors):
    """Builds a whole area behind entry_doors (unlinked exit warps of the previous area's last boss room).
    Returns (group, exits of the last boss room, if it was built with open_exit)."""
    from .populate import populate
    spec = cfg.spec
    g = w.group(cfg.key, spec.sprites)
    g.hub = getattr(spec, "hub", {})
    w.pools[spec.pool] = dict(seen=spec.T.SEEN, beaten=spec.T.BEATEN, after=spec.T.AFTER)
    lms = []
    for const, x, y, name in cfg.landmarks:
        w.landmarks.append((const, x, y, name))
        lms.append("LANDMARK_" + const)
    items = [cfg.tiers[i] for i in cfg.stock_ix]
    p1 = start_plaza(w, g, rng, cfg.kit, cfg.tag, lms[0], cfg.music, cfg.texts, items[0], entry_doors,
                     cfg.gate_name, cfg.gate_text, pal=cfg.pal)
    acts = []
    for k in range(3):
        acts.append(ActSpec(cfg.tag, cfg.lanes[k], cfg.kit, lms[k], cfg.music, trainers=cfg.trainers[k], boutique=k,
                            boss=cfg.bosses[k], texts=cfg.texts, split=cfg.splits[k], gate=cfg.gates[k], pal=cfg.pal,
                            plaza_width=15 if (k == 1 and cfg.purg) else 13, rift=(k == 1 and cfg.purg),
                            split_houses=cfg.split_houses[k]))
    for k, act in enumerate(acts):
        act.index, act.spec = k, spec
    all_lanes = []
    prev, lane_no, plaza_no = p1, 1, 2
    exits = []
    for k, act in enumerate(acts):
        lanes, prev, doors, info, lane_no, plaza_no = build_act(
            w, g, rng, roster, act, prev, plaza_no, lane_no, spec.theme, items[2 * k + 1:2 * k + 3])
        all_lanes += lanes
        exits = info[2]
    total = sum(len(s) for _, s in all_lanes)
    done = 0
    for m, s in all_lanes:
        n = len(s)
        populate(w, m, s, spec, rng, roster, done / total, (done + n) / total)
        done += n
    return g, exits
