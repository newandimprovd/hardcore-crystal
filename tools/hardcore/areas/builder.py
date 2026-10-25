"""Shared building blocks for the five areas: acts (a run of lanes ending in a plaza), town interiors, bosses."""
from .layout import (boss_room, chain, house_interior, lane, mart_interior, plaza, pokecenter_interior)
from .party import make_party
from .text import Text


class BossSpec:
    """A boss at the end of an act. level is the highest level of the party, size the party size."""

    def __init__(self, room, name, cls, sprite, pal, level, size, seen, beaten, after, template="karen",
                 item=None, theme=None, landmark=None, music="MUSIC_GYM"):
        self.room, self.name, self.cls, self.sprite, self.pal = room, name, cls, sprite, pal
        self.level, self.size = level, size
        self.seen, self.beaten, self.after = seen, beaten, after
        self.template, self.item, self.theme = template, item, theme
        self.landmark, self.music = landmark, music


class ActSpec:
    """lanes lanes of `trainers` fighters each, then a plaza (Pokecenter, Mart, a house, the boss door)."""

    def __init__(self, tag, lanes, kit, landmark, music, trainers=13, gate=None, boss=None, houses=1,
                 mart=None, texts=None, plaza_width=13, lane_names=None, split=None):
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
        m, s = lane(g, f"{tag}Street{lane_no}", kit, rng, trainers=act.trainers, landmark=act.landmark,
                    music=act.music, neck=2 if gate else 0, gate=gate, w=w)
        chain(below, m)
        lanes.append((m, s))
        below = m
        lane_no += 1
        if act.split and i + 1 == act.split:
            pm, dm = plaza(g, f"{tag}Plaza{plaza_no}", kit, rng, landmark=act.landmark, music=act.music,
                           houses=1, width=act.plaza_width)
            chain(below, pm)
            town(w, g, tag, plaza_no, pm, dm, kit, act.landmark, f"{tag.upper()}_{plaza_no}", stocks.pop(0), act.texts,
                 f"{tag.upper()}_{plaza_no}")
            below = pm
            plaza_no += 1
    p, doors = plaza(g, f"{tag}Plaza{plaza_no}", kit, rng, landmark=act.landmark, music=act.music,
                     houses=act.houses, extra=1 if act.boss else 0, width=act.plaza_width)
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
                                boss, item=b.item, open_exit=False)
        info = (room, boss)
    return lanes, p, doors, info, lane_no, plaza_no
