"""Area 2: THE COMMUNE, a hunter-gatherer commune with no locks, no money and no body shame."""
from . import a2_text as T
from . import kits
from .builder import ActSpec, BossSpec, build_act, start_plaza
from .populate import populate


class Spec:
    pool = "A2"
    l0, l1 = 24, 44
    theme = {"GRASS": 3, "BUG": 3, "FLYING": 2, "NORMAL": 2, "GROUND": 2, "WATER": 2, "FIGHTING": 1.5,
             "FAIRY": 1.5, "POISON": 1, "ROCK": 1, "ELECTRIC": 0.5, "FIRE": 0.5, "PSYCHIC_TYPE": 0.5,
             "DARK": 0.3, "GHOST": 0.3, "ICE": 0.3, "DRAGON": 0.2, "STEEL": 0.2}
    classes = [("HIKER", "SPRITE_POKEFAN_M", "PAL_NPC_BROWN", 4),
               ("CAMPER", "SPRITE_YOUNGSTER", "PAL_NPC_GREEN", 3),
               ("PICNICKER", "SPRITE_LASS", "PAL_NPC_PINK", 3),
               ("BUG_CATCHER", "SPRITE_BUG_CATCHER", "PAL_NPC_GREEN", 2),
               ("FISHER", "SPRITE_FISHER", "PAL_NPC_BLUE", 2),
               ("BEAUTY", "SPRITE_BEAUTY", "PAL_NPC_PINK", 2),
               ("POKEFANM", "SPRITE_GRAMPS", "PAL_NPC_BROWN", 2),
               ("POKEFANF", "SPRITE_GRANNY", "PAL_NPC_RED", 2),
               ("SAGE", "SPRITE_SAGE", "PAL_NPC_BROWN", 2),
               ("KIMONO_GIRL", "SPRITE_KIMONO_GIRL", "PAL_NPC_RED", 2),
               ("SWIMMERM", "SPRITE_SWIMMER_GUY", "PAL_NPC_BLUE", 2),
               ("SWIMMERF", "SPRITE_SWIMMER_GIRL", "PAL_NPC_PINK", 2),
               ("BLACKBELT_T", "SPRITE_BLACK_BELT", "PAL_NPC_BROWN", 1),
               ("GUITARIST", "SPRITE_ROCKER", "PAL_NPC_RED", 2),
               ("SUPER_NERD", "SPRITE_SUPER_NERD", "PAL_NPC_BLUE", 1),
               ("BIRD_KEEPER", "SPRITE_POKEFAN_F", "PAL_NPC_GREEN", 2)]
    sprites = sorted({c[1] for c in classes}) + ["SPRITE_POKE_BALL", "SPRITE_ROCK", "SPRITE_BOULDER", "SPRITE_FRUIT_TREE"]

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


TIERS = [
    ["POKE_BALL", "GREAT_BALL", "POTION", "SUPER_POTION", "ANTIDOTE", "PARLYZ_HEAL", "AWAKENING", "BURN_HEAL", "REVIVE"],
    ["POKE_BALL", "GREAT_BALL", "SUPER_POTION", "HYPER_POTION", "ANTIDOTE", "PARLYZ_HEAL", "AWAKENING", "BURN_HEAL",
     "ICE_HEAL", "REVIVE", "REPEL"],
    ["GREAT_BALL", "ULTRA_BALL", "HYPER_POTION", "FULL_HEAL", "REVIVE", "SUPER_REPEL", "ESCAPE_ROPE"],
]


def build(w, roster, rng, entry_doors, open_exit=False):
    """entry_doors: the two unlinked exit warps of Area 1's last boss room. Returns (group, exits)."""
    spec = Spec()
    g = w.group("AREA2", spec.sprites)
    w.pools[spec.pool] = dict(seen=T.SEEN, beaten=T.BEATEN, after=T.AFTER)
    johto = kits.johto()
    w.landmarks.append(("GROVE_COMMUNE", 60, 66, "THE<BSP>COMMUNE"))
    w.landmarks.append(("GROVE_ORCHARD", 56, 62, "THE<BSP>ORCHARD"))
    w.landmarks.append(("GROVE_HEARTH", 52, 58, "THE<BSP>GREAT<BSP>HEARTH"))
    LM1, LM2, LM3 = "LANDMARK_GROVE_COMMUNE", "LANDMARK_GROVE_ORCHARD", "LANDMARK_GROVE_HEARTH"
    texts = dict(center=T.CENTER, mart=T.MART, house=T.HOUSE)
    items = [TIERS[0]] + [TIERS[t] for t in (0, 1, 1, 2, 2, 2)]
    p1 = start_plaza(w, g, rng, johto, "Grove", LM1, "MUSIC_AZALEA_TOWN", texts, items[0], entry_doors,
                     "GroveGate", T.GATE[0])
    boss1 = BossSpec("GroveBoathouse", "REEVE OTTO", "FISHER", "SPRITE_FISHER", "PAL_NPC_BLUE", 33, 5,
                     T.BOATHOUSE_SEEN, T.BOATHOUSE_BEATEN, T.BOATHOUSE_AFTER, template="karen", item="JET_SKI")
    boss2 = BossSpec("GroveSmokehouse", "ELDER FERN", "SAGE", "SPRITE_GRANNY", "PAL_NPC_GREEN", 39, 5,
                     T.SMOKEHOUSE_SEEN, T.SMOKEHOUSE_BEATEN, T.SMOKEHOUSE_AFTER, template="will", item="BASEBALL_BAT")
    boss3 = BossSpec("GroveCouncil", "MATRIARCH", "MEDIUM", "SPRITE_KIMONO_GIRL", "PAL_NPC_RED", 46, 6,
                     T.COUNCIL_SEEN, T.COUNCIL_BEATEN, T.COUNCIL_AFTER, template="bruno", landmark=LM3,
                     music="MUSIC_ROCKET_HIDEOUT", open_exit=open_exit)
    acts = [ActSpec("Grove", 5, johto, LM1, "MUSIC_ROUTE_36", boss=boss1, texts=texts, split=3),
            ActSpec("Grove", 5, johto, LM2, "MUSIC_ROUTE_36", gate="river", boss=boss2, texts=texts, split=2),
            ActSpec("Grove", 5, johto, LM3, "MUSIC_ROUTE_36", gate="hive", boss=boss3, texts=texts, split=3)]
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
