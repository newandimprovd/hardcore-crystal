"""Shared building blocks for the five areas: acts (a run of lanes ending in a plaza), town interiors, bosses."""
from .flags import flag_once
from . import boutique as shops
from .layout import (FACE, boss_room, chain, gatehouse, house_interior, boutique_interior, lane, mart_interior, plaza, pokecenter_interior)
from .town import plaza2
from .wayfolk import GIFT, GIFT_AFTER, GIFT_ITEMS, HERMIT, TOWNIE, TOWNIE2
from .trail import trail
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
        plain_npc(m, x, y, sp, R.choice(NPC_PALS), R.choice(["LEFT", "RIGHT", "UP", "DOWN"]), f"{m.name}Hermit", R.choice(HERMIT[tag]))


def crowd(w, g, m, n=9, plaza_no=1):
    """Townsfolk for a plaza: n talkers on its free floor cells (from the front of the seeded list; cameos take from the end).  The first
    is the plaza's gift-giver (areas/wayfolk.py GIFT: a named stranger who hands over one item, once), the rest plain talkers."""
    import random
    from .people import plain_npc
    R = random.Random("crowd:" + m.name)
    tag = area_tag(m)
    if not hasattr(m, "npc_cells"):  # the box plaza of the Johto road has no seeded cell list
        return
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


def build_act(w, g, rng, roster, act, prev, plaza_no, lane_no, area_theme, stocks):
    """Builds act.lanes lanes north of `prev` (a plaza), a mid-act plaza after act.split lanes if asked, then the
    final plaza with its interiors and boss room. stocks: Mart item lists, one per plaza built here.
    Returns (lanes, plaza, doors, boss_info, next lane number, next plaza number)."""
    kit, tag = act.kit, act.tag
    lanes = []
    below = prev
    stocks = list(stocks)
    for i in range(act.lanes):
        first = i == 0
        gate = act.gate if first else None
        tr = act.trainers[i] if isinstance(act.trainers, (list, tuple)) else act.trainers
        if kit.extra.get("scn"):
            m, s = trail(g, f"{tag}Street{lane_no}", kit, rng, trainers=tr, landmark=act.landmark, a=below.a_out,
                         music=act.music, neck=2 if gate else 0, gate=gate, w=w, pal=act.pal)
        else:
            la = rng.choice((1, 2, 3, 4))  # the road drifts sideways from lane to lane, so it winds instead of running straight north
            m, s = lane(g, f"{tag}Street{lane_no}", kit, rng, trainers=tr, landmark=act.landmark, a=la, right=6 - la,
                        music=act.music, neck=2 if gate else 0, gate=gate, w=w, pal=act.pal)
        pickup(w, m, reserve=len(s))
        furnish_lane(w, g, m, reserve=len(s))
        chain(below, m, below.a_out - m.a)
        lanes.append((m, s))
        below = m
        lane_no += 1
        if act.split and i + 1 == act.split:
            nh = act.split_houses + (1 if act.boutique is not None else 0)
            pm, dm = make_plaza(g, f"{tag}Plaza{plaza_no}", kit, rng, landmark=act.landmark, music=act.music,
                                houses=nh, width=max(act.plaza_width, 2 * (2 + nh) + 9), pal=act.pal, index=plaza_no)
            chain(below, pm, below.a_out - pm.a)
            town(w, g, tag, plaza_no, pm, dm, kit, act.landmark, f"{tag.upper()}_{plaza_no}", stocks.pop(0), act.texts,
                 f"{tag.upper()}_{plaza_no}", boutique=shops.spec(tag, act.boutique) if act.boutique is not None else None)
            below = pm
            plaza_no += 1
    p, doors = make_plaza(g, f"{tag}Plaza{plaza_no}", kit, rng, landmark=act.landmark, music=act.music,
                          houses=act.houses, extra=1 if act.boss else 0, width=act.plaza_width, pal=act.pal, rift=act.rift,
                          index=plaza_no)
    chain(below, p, below.a_out - p.a)
    if act.rift:
        door = doors["rift"]
        short = "A" + g.key[-1]
        flag = flag_once(w, f"EVENT_PURG_OPEN_{short}")
        p.coords.append((door.x, door.y + 1, -1, f"{p.name}PurgFlagScript"))
        p.scripts.append(f"{p.name}PurgFlagScript:\n\tsetevent {flag}\n\tend\n")
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
