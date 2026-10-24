"""Area 1: TITHE CITY, a megacity of towers around a vast cathedral, run by corrupt priests and policemen."""
import random

from . import kits
from .layout import chain, gatehouse, house_interior, lane, mart_interior, plaza, pokecenter_interior
from .populate import populate
from .text import Text


class Spec:
    pool = "A1"
    l0, l1 = 5, 24
    theme = {"DARK": 3, "NORMAL": 3, "FIGHTING": 2, "STEEL": 2, "PSYCHIC_TYPE": 1.5, "POISON": 1.5,
             "GHOST": 1, "BUG": 1, "FIRE": 0.7, "WATER": 0.7, "GRASS": 0.5, "FLYING": 1, "GROUND": 0.7,
             "ELECTRIC": 0.7, "ROCK": 0.5, "ICE": 0.3, "DRAGON": 0.1, "FAIRY": 0.3}
    classes = [("OFFICER", "SPRITE_OFFICER", "PAL_NPC_BLUE", 6),
               ("GENTLEMAN", "SPRITE_GENTLEMAN", "PAL_NPC_BROWN", 3),
               ("COOLTRAINERM", "SPRITE_COOLTRAINER_M", "PAL_NPC_RED", 2),
               ("COOLTRAINERF", "SPRITE_COOLTRAINER_F", "PAL_NPC_RED", 2),
               ("BEAUTY", "SPRITE_BEAUTY", "PAL_NPC_PINK", 2),
               ("BIKER", "SPRITE_BIKER", "PAL_NPC_GREEN", 2),
               ("GRUNTM", "SPRITE_ROCKET", "PAL_NPC_BROWN", 3),
               ("GRUNTF", "SPRITE_ROCKET_GIRL", "PAL_NPC_RED", 2),
               ("SUPER_NERD", "SPRITE_SUPER_NERD", "PAL_NPC_BLUE", 2),
               ("SCHOOLBOY", "SPRITE_YOUNGSTER", "PAL_NPC_GREEN", 2),
               ("LASS", "SPRITE_LASS", "PAL_NPC_PINK", 2),
               ("TEACHER", "SPRITE_TEACHER", "PAL_NPC_GREEN", 1),
               ("POKEFANM", "SPRITE_POKEFAN_M", "PAL_NPC_BROWN", 1),
               ("BLACKBELT_T", "SPRITE_BLACK_BELT", "PAL_NPC_BROWN", 1),
               ("GUITARIST", "SPRITE_ROCKER", "PAL_NPC_RED", 1),
               ("SCIENTIST", "SPRITE_SCIENTIST", "PAL_NPC_GREEN", 1)]
    sprites = ["SPRITE_OFFICER", "SPRITE_GENTLEMAN", "SPRITE_COOLTRAINER_M", "SPRITE_COOLTRAINER_F", "SPRITE_BEAUTY",
               "SPRITE_BIKER", "SPRITE_ROCKET", "SPRITE_ROCKET_GIRL", "SPRITE_SUPER_NERD", "SPRITE_YOUNGSTER",
               "SPRITE_LASS", "SPRITE_TEACHER", "SPRITE_POKEFAN_M", "SPRITE_BLACK_BELT", "SPRITE_ROCKER",
               "SPRITE_SCIENTIST", "SPRITE_POKE_BALL", "SPRITE_ROCK", "SPRITE_BOULDER"]

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


SEEN = [
    "Tithe's due. I take cash, cards or teeth.",
    "Move along, citizen. Or don't. I could use the overtime.",
    "This street has a collection plate. You are the collection.",
    "Do you know who my uncle is? Neither do I. Fight me.",
    "The parish blesses this block. I just bill it.",
    "You look unaccompanied. Let me fix that with a bruise.",
    "I'm not corrupt. I'm just very good at accepting gifts. Hand it over.",
    "Rent's up again. So is my temper.",
    "Oh good. Another witness for the fight. Wait, you're the fight.",
    "Nobody gets past without a donation. Your face counts as one.",
    "I forgave myself for what I'm about to do. Saves time.",
    "Hold it. The cathedral bell tolls for thee. I just paid it to.",
    "Big city, small hospitality. Let's get on with it.",
    "You have the right to remain broke. Everything you say may be billed.",
    "My shift ended an hour ago. You owe me for that hour.",
    "Heard a nutcase is walking around killing trainers. Lucky for me, that's a rumor.",
]
BEATEN = [
    "Ow. That's coming out of my overtime.",
    "Fine. You win. Please forget my face.",
    "Tell the parish I tried. They'll still dock my pay.",
    "My mom told me about people like you. She was too optimistic.",
    "I should've taken the bribe.",
    "Oof. I feel strangely forgiven.",
    "I lost? The union is going to hear about this. Ow.",
    "That was a hell of a lot more than a donation.",
    "Rest in peace, my pension.",
    "Please don't take my wallet. Wait, you already did.",
    "You hit like landlords evict.",
    "Okay, okay, okay. That's enough. Why are you smiling?",
]
AFTER = [
    "Don't look at me. I'm on break.",
    "Go ahead. Everyone else does.",
    "I'm filing a complaint. To nobody.",
    "The city is not what it seems. Mostly it's worse.",
    "I used to believe in something. Now I believe in lunch.",
    "Keep moving. The towers are watching.",
    "Please stop making eye contact with the dead.",
    "I'll pray for you. Priced separately.",
]


def build(w, roster, rng):
    spec = Spec()
    g = w.group("AREA1", spec.sprites)
    w.pools[spec.pool] = dict(seen=SEEN, beaten=BEATEN, after=AFTER)
    modern, johto = kits.modern(), kits.johto()
    w.landmarks.append(("TITHE_CITY", 80, 70, "TITHE<BSP>CITY"))
    w.landmarks.append(("TITHE_ROAD", 80, 84, "TITHE<BSP>ROAD"))
    LM_CITY, LM_ROAD = "LANDMARK_TITHE_CITY", "LANDMARK_TITHE_ROAD"
    w.marts.append(("TITHE_1", "MartTithe1", ["POKE_BALL", "POTION", "ANTIDOTE", "PARLYZ_HEAL", "AWAKENING"]))
    w.marts.append(("TITHE_2", "MartTithe2", ["POKE_BALL", "GREAT_BALL", "POTION", "SUPER_POTION", "ANTIDOTE",
                                             "PARLYZ_HEAL", "AWAKENING", "BURN_HEAL", "REVIVE"]))
    plan = []  # (map, slots)

    # Segment 1: the road out of Cherrygrove (outdoor Johto tileset)
    road, s_road = lane(g, "TitheRoad", johto, rng, trainers=6, a=2, cw=3, right=3, landmark=LM_ROAD,
                        music="MUSIC_ROUTE_30", north="door", neck=2)
    # Segment 2: the city (modern tileset)
    p1, d1 = plaza(g, "TithePlaza1", modern, rng, landmark=LM_CITY, music="MUSIC_GOLDENROD_CITY", rift=True,
                   houses=1, south="closed")
    gate = gatehouse(g, "TitheCheckpoint", road.door, d1["rift"], LM_CITY, "MUSIC_GOLDENROD_CITY",
                     [Text("Papers? No? Great. That's a fine too. Pay at the end.")])
    lanes = []
    for i in range(3):
        m, s = lane(g, f"TitheStreet{i + 1}", modern, rng, trainers=13, landmark=LM_CITY,
                    music="MUSIC_GOLDENROD_CITY")
        lanes.append((m, s))
    p2, d2 = plaza(g, "TithePlaza2", modern, rng, landmark=LM_CITY, music="MUSIC_GOLDENROD_CITY", houses=1)
    chain(p1, lanes[0][0])
    chain(lanes[0][0], lanes[1][0])
    chain(lanes[1][0], lanes[2][0])
    chain(lanes[2][0], p2)
    # interiors
    pc1 = pokecenter_interior(g, "TithePokecenter1", d1["center"], LM_CITY,
                              [Text("They say the nurse used to be a priest. Or a cop. Or both.")])
    mt1 = mart_interior(g, "TitheMart1", d1["mart"], LM_CITY, "TITHE_1", [Text("Everything here is overpriced by divine right.")])
    h1 = house_interior(g, "TitheHouse1", d1["houses"][0], LM_CITY,
                        [Text("I own this whole apartment. The rest of the block is my closet. We don't talk about the closet.")])
    pc2 = pokecenter_interior(g, "TithePokecenter2", d2["center"], LM_CITY, [])
    mt2 = mart_interior(g, "TitheMart2", d2["mart"], LM_CITY, "TITHE_2", [])
    h2 = house_interior(g, "TitheHouse2", d2["houses"][0], LM_CITY, [Text("The cathedral bell is a recording. Don't tell anyone.")])
    w.spawns.append(("TITHE_1", p1, *p1.spawn_cell))
    w.spawns.append(("TITHE_2", p2, *p2.spawn_cell))
    # Cherrygrove link
    class Cherry:
        name, const = "CherrygroveCity", "CHERRYGROVE_CITY"
    road.connections["south"] = (Cherry, -5)
    # trainers
    total = sum(len(s) for _, s in [(road, s_road)] + lanes)
    done = 0
    for m, s in [(road, s_road)] + lanes:
        n = len(s)
        populate(w, m, s, spec, rng, roster, done / total, (done + n) / total)
        done += n
    return g
