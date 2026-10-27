"""Shared building blocks for the five areas: acts (a run of lanes ending in a plaza), town interiors, bosses."""
from .layout import (boss_room, chain, gatehouse, house_interior, lane, mart_interior, plaza, pokecenter_interior)
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
        self.story = story  # 2 = the rival (kill 800), 3 = the final boss: scripts in engine/hardcore/story.asm


class ActSpec:
    """lanes lanes of `trainers` fighters each, then a plaza (Pokecenter, Mart, a house, the boss door)."""

    def __init__(self, tag, lanes, kit, landmark, music, trainers=13, gate=None, boss=None, houses=1,
                 mart=None, texts=None, plaza_width=13, lane_names=None, split=None, pal="PALETTE_DAY"):
        self.pal = pal
        self.tag, self.lanes, self.kit, self.landmark, self.music = tag, lanes, kit, landmark, music
        self.split = split  # a second, smaller plaza (Pokecenter, Mart, house) after this many lanes
        self.trainers, self.gate, self.boss, self.houses = trainers, gate, boss, houses
        self.mart, self.texts, self.plaza_width = mart, texts or {}, plaza_width
        self.lane_names = lane_names


def pick(lst, i):
    return Text(lst[i % len(lst)]) if lst else None


def town(w, g, tag, n, p, doors, kit, landmark, spawn_const, mart_items, texts, martconst):
    """Pokecenter, Mart and house interiors for plaza p (doors from layout.plaza). texts: dict of lists."""
    w.spawns.append((spawn_const, p, *p.spawn_cell))
    w.marts.append((martconst, f"Mart{tag}{n}", mart_items))
    center = [pick(texts.get("center", []), n * 3 + i) for i in range(1)]
    pokecenter_interior(g, f"{tag}Pokecenter{n}", doors["center"], landmark, [t for t in center if t])
    mart = [pick(texts.get("mart", []), n * 2)]
    mart_interior(g, f"{tag}Mart{n}", doors["mart"], landmark, martconst, [t for t in mart if t])
    for i, hd in enumerate(doors["houses"]):
        h = [pick(texts.get("house", []), n * 2 + i), pick(texts.get("house", []), n * 2 + i + 5)]
        house_interior(g, f"{tag}House{n}" if i == 0 else f"{tag}House{n}b", hd, landmark, [t for t in h if t])


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
        m, s = lane(g, f"{tag}Street{lane_no}", kit, rng, trainers=tr, landmark=act.landmark,
                    music=act.music, neck=2 if gate else 0, gate=gate, w=w, pal=act.pal)
        chain(below, m)
        lanes.append((m, s))
        below = m
        lane_no += 1
        if act.split and i + 1 == act.split:
            pm, dm = plaza(g, f"{tag}Plaza{plaza_no}", kit, rng, landmark=act.landmark, music=act.music,
                           houses=1, width=act.plaza_width, pal=act.pal)
            chain(below, pm)
            town(w, g, tag, plaza_no, pm, dm, kit, act.landmark, f"{tag.upper()}_{plaza_no}", stocks.pop(0), act.texts,
                 f"{tag.upper()}_{plaza_no}")
            below = pm
            plaza_no += 1
    p, doors = plaza(g, f"{tag}Plaza{plaza_no}", kit, rng, landmark=act.landmark, music=act.music,
                     houses=act.houses, extra=1 if act.boss else 0, width=act.plaza_width, pal=act.pal)
    chain(below, p)
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
    p, d = plaza(g, f"{tag}Plaza1", kit, rng, landmark=landmark, music=music, rift=True, houses=1, south="closed",
                 pal=pal)
    gatehouse(g, gate_name, entry_doors, d["rift"], landmark, music, [Text(gate_text)])
    town(w, g, tag, 1, p, d, kit, landmark, f"{tag.upper()}_1", stock, texts, f"{tag.upper()}_1")
    return p


class AreaCfg:
    """Everything that makes one area different. Acts are built three at a time: boss1 gives the key item for
    the gate of act 2, boss2 the one for the gate of act 3, boss3 ends the area."""

    def __init__(self, key, tag, spec, kit, pal, landmarks, music, texts, tiers, bosses, gates, splits,
                 gate_name, gate_text, stock_ix=(0, 0, 1, 1, 2, 2, 2), lanes=(5, 5, 5), trainers=(13, 13, 13)):
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
        acts.append(ActSpec(cfg.tag, cfg.lanes[k], cfg.kit, lms[k], cfg.music, trainers=cfg.trainers[k],
                            boss=cfg.bosses[k], texts=cfg.texts, split=cfg.splits[k], gate=cfg.gates[k], pal=cfg.pal))
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
