"""Area 1: TITHE CITY, a megacity of towers around a vast cathedral, run by corrupt priests and policemen."""
from art.classes import area_mix
import random

from . import a1_text as T
from . import counts, kits
from .builder import ActSpec, BossSpec, build_act, furnish_lane, make_plaza, pickup, town
from .layout import chain, gatehouse, lane, plaza
from .trail import trail
from .populate import populate
from .text import Text


class Spec:
    pool = "A1"
    l0, l1 = 5, 24
    theme = {"DARK": 3, "NORMAL": 3, "FIGHTING": 2, "STEEL": 2, "PSYCHIC_TYPE": 1.5, "POISON": 1.5,
             "GHOST": 1, "BUG": 1, "FIRE": 0.7, "WATER": 0.7, "GRASS": 0.5, "FLYING": 1, "GROUND": 0.7,
             "ELECTRIC": 0.7, "ROCK": 0.5, "ICE": 0.3, "DRAGON": 0.1, "FAIRY": 0.3}
    hub = dict(nurse=("SPRITE_HC_NUN", "PAL_NPC_BROWN"),
               clerk=("SPRITE_HC_SUIT", "PAL_NPC_BROWN"),
               pc=[("SPRITE_HC_BEGGAR", "PAL_NPC_GREEN"), ("SPRITE_HC_SUIT", "PAL_NPC_BLUE"), ("SPRITE_HC_CHOIR", "PAL_NPC_PINK")],
               mart=[("SPRITE_HC_HOODIE", "PAL_NPC_GREEN"), ("SPRITE_HC_PUNK", "PAL_NPC_RED")],
               house=[("SPRITE_HC_BEGGAR", "PAL_NPC_BROWN"), ("SPRITE_HC_CHOIR", "PAL_NPC_BLUE")],
               gate=[("SPRITE_HC_COP", "PAL_NPC_BLUE"), ("SPRITE_HC_HOODIE", "PAL_NPC_GREEN")])
    classes = area_mix("AREA1")
    @property
    def sprites(self):
        return sorted({c[1] for c in self.classes}) + ["SPRITE_POKE_BALL", "SPRITE_ROCK", "SPRITE_BOULDER", "SPRITE_FRUIT_TREE"]

    def pick_class(self, rng):
        total = sum(c[3] for c in self.classes)
        r = rng.uniform(0, total)
        for c in self.classes:
            r -= c[3]
            if r <= 0:
                return c[0], c[1], c[2]
        return self.classes[0][:3]

    def size_progress(self, prog):
        return prog


def build(w, roster, rng, open_exit=False):
    spec = Spec()
    g = w.group("AREA1", spec.sprites)
    g.hub = spec.hub
    w.pools[spec.pool] = dict(seen=T.SEEN, beaten=T.BEATEN, after=T.AFTER)
    modern, johto = kits.tithe(), kits.johto()
    w.landmarks.append(("TITHE_CITY", 80, 70, "TITHE<BSP>LOWTOWN"))
    w.landmarks.append(("TITHE_ROAD", 80, 84, "TITHE<BSP>ROAD"))
    w.landmarks.append(("TITHE_MIDTOWN", 80, 62, "TITHE<BSP>MIDTOWN"))
    w.landmarks.append(("TITHE_PARISH", 80, 54, "THE<BSP>PARISH"))
    LM_CITY, LM_ROAD = "LANDMARK_TITHE_CITY", "LANDMARK_TITHE_ROAD"
    LM_MID, LM_PARISH = "LANDMARK_TITHE_MIDTOWN", "LANDMARK_TITHE_PARISH"
    texts = dict(center=T.CENTER + T.CENTER_B, mart=T.MART, house=T.HOUSE)
    tiers = [
        ["POKE_BALL", "POTION", "ANTIDOTE", "PARLYZ_HEAL", "AWAKENING"],
        ["POKE_BALL", "GREAT_BALL", "POTION", "SUPER_POTION", "ANTIDOTE", "PARLYZ_HEAL", "AWAKENING", "BURN_HEAL", "REVIVE"],
        ["POKE_BALL", "GREAT_BALL", "SUPER_POTION", "HYPER_POTION", "ANTIDOTE", "PARLYZ_HEAL", "AWAKENING", "BURN_HEAL",
         "ICE_HEAL", "REVIVE", "REPEL"],
        ["GREAT_BALL", "ULTRA_BALL", "HYPER_POTION", "FULL_HEAL", "REVIVE", "SUPER_REPEL", "ESCAPE_ROPE"],
    ]
    # one stock per plaza: P1, then (middle, boss door) for each of the three acts
    items = [tiers[0]] + [tiers[t] for t in (1, 1, 2, 2, 3, 3)]

    # Segment 1: the road out of Cherrygrove (outdoor Johto tileset)
    road, s_road = trail(g, "TitheRoad", kits.road(), rng, trainers=counts.ROAD_TRAINERS, a=2, cw=3, landmark=LM_ROAD,
                         music="MUSIC_ROUTE_30", north="door")
    pickup(w, road, reserve=len(s_road))
    furnish_lane(w, g, road, reserve=len(s_road))
    # Segment 2: the city (modern tileset)
    # The road ends at a classic gate house (route -> gate house -> city); the hall's far door lands on the plaza's south edge,
    # so the walk keeps heading north: the way out of a map is always the opposite side of the way into the next one.
    p1, d1 = make_plaza(g, "TithePlaza1", modern, rng, landmark=LM_CITY, music="MUSIC_GOLDENROD_CITY", houses=1, south="gate", index=1)
    gatehouse(g, "TitheCheckpoint", road.door, d1["south"], LM_CITY, "MUSIC_GOLDENROD_CITY", [Text(T.GATE[0])])
    town(w, g, "Tithe", 1, p1, d1, modern, LM_CITY, "TITHE_1", items[0], texts, "TITHE_1", reminders=(T.TIP_A, T.TIP_B))
    # Trainer tips sign: a Johto signpost block just left of the road near its south end. Read it from the road side.
    sx, sy = road.a - 1, road.h - 3
    road.set(sx, sy, 0x47)
    road.bg(2 * sx + 1, 2 * sy + 1, "BGEVENT_READ", "TitheRoadTipsSign")
    road.scripts.append("TitheRoadTipsSign:\n\tjumptext TitheRoadTipsSignText\n")
    road.scripts.append(Text(T.TIPS_SIGN).emit("TitheRoadTipsSignText"))
    # the road's south end is joined to the Tithe Junction by gen_areas.py (opening.py)

    boss1 = BossSpec("TitheVestry", "DEACON", "T_DEACON", "SPRITE_HC_PRIEST", "PAL_NPC_RED", 15, 4, T.VESTRY_SEEN,
                     T.VESTRY_BEATEN, T.VESTRY_AFTER, template="karen")
    boss2 = BossSpec("TitheEvidenceRoom", "CHIEF BRAD", "T_COPCHIEF", "SPRITE_HC_COP_CHIEF", "PAL_NPC_BLUE", 21, 5,
                     T.EVIDENCE_SEEN, T.EVIDENCE_BEATEN, T.EVIDENCE_AFTER, template="will")
    boss3 = BossSpec("TitheCathedral", "MONSIGNOR", "T_MONSIGNOR", "SPRITE_HC_MONSIGNOR", "PAL_NPC_RED", 27, 6,
                     T.CATHEDRAL_SEEN, T.CATHEDRAL_BEATEN, T.CATHEDRAL_AFTER, template="bruno", landmark=LM_PARISH,
                     music="MUSIC_ROCKET_HIDEOUT", open_exit=open_exit)
    # Timmy is kill 1; the tidal wave news is kill counts.TSUNAMI_KILLS (HC_TSUNAMI_KILLS) and does not depend on any one room
    acts = [ActSpec("Tithe", 5, modern, LM_CITY, "MUSIC_GOLDENROD_CITY", boss=boss1, texts=texts, split=3,
                    trainers=counts.lanes_of(1)[0], boutique=0),
            ActSpec("Tithe", 5, modern, LM_MID, "MUSIC_GOLDENROD_CITY", gate="tree", boss=boss2, texts=texts, split=2,
                    trainers=counts.lanes_of(1)[1], plaza_width=15, rift=True, boutique=1),
            ActSpec("Tithe", 5, modern, LM_PARISH, "MUSIC_GOLDENROD_CITY", gate="boulder", boss=boss3, texts=texts, split=3,
                    trainers=counts.lanes_of(1)[2], boutique=2)]

    all_lanes = [(road, s_road)]
    prev, lane_no, plaza_no = p1, 1, 2
    bosses = []
    for k, act in enumerate(acts):
        lanes, prev, doors, info, lane_no, plaza_no = build_act(
            w, g, rng, roster, act, prev, plaza_no, lane_no, spec.theme, items[2 * k + 1:2 * k + 3])
        all_lanes += lanes
        bosses.append(info)
    # trainers
    total = sum(len(s) for _, s in all_lanes)
    done = 0
    for m, s in all_lanes:
        n = len(s)
        populate(w, m, s, spec, rng, roster, done / total, (done + n) / total)
        done += n
    return g, bosses[-1][2]
