"""Area 2: THE COMMUNE, a hunter-gatherer commune with no locks, no money and no body shame."""
from . import a2_text as T
from . import kits
from .builder import AreaCfg, BossSpec, build_area
from .specbase import SpecBase


class Spec(SpecBase):
    pool = "A2"
    l0, l1 = 24, 44
    T = T
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


TIERS = [
    ["POKE_BALL", "GREAT_BALL", "POTION", "SUPER_POTION", "ANTIDOTE", "PARLYZ_HEAL", "AWAKENING", "BURN_HEAL", "REVIVE"],
    ["POKE_BALL", "GREAT_BALL", "SUPER_POTION", "HYPER_POTION", "ANTIDOTE", "PARLYZ_HEAL", "AWAKENING", "BURN_HEAL",
     "ICE_HEAL", "REVIVE", "REPEL"],
    ["GREAT_BALL", "ULTRA_BALL", "HYPER_POTION", "FULL_HEAL", "REVIVE", "SUPER_REPEL", "ESCAPE_ROPE"],
]


def build(w, roster, rng, entry_doors, open_exit=False):
    """entry_doors: the two unlinked exit warps of Area 1's last boss room. Returns (group, exits)."""
    texts = dict(center=T.CENTER, mart=T.MART, house=T.HOUSE)
    bosses = [
        BossSpec("GroveBoathouse", "REEVE OTTO", "FISHER", "SPRITE_FISHER", "PAL_NPC_BLUE", 33, 5, T.BOATHOUSE_SEEN,
                 T.BOATHOUSE_BEATEN, T.BOATHOUSE_AFTER, template="karen", item="JET_SKI"),
        BossSpec("GroveSmokehouse", "ELDER FERN", "SAGE", "SPRITE_GRANNY", "PAL_NPC_GREEN", 39, 5, T.SMOKEHOUSE_SEEN,
                 T.SMOKEHOUSE_BEATEN, T.SMOKEHOUSE_AFTER, template="will", item="BASEBALL_BAT"),
        BossSpec("GroveCouncil", "MATRIARCH", "MEDIUM", "SPRITE_KIMONO_GIRL", "PAL_NPC_RED", 46, 6, T.COUNCIL_SEEN,
                 T.COUNCIL_BEATEN, T.COUNCIL_AFTER, template="bruno", landmark="LANDMARK_GROVE_HEARTH",
                 music="MUSIC_ROCKET_HIDEOUT", open_exit=open_exit)]
    cfg = AreaCfg("AREA2", "Grove", Spec(), kits.grove(), "PALETTE_DAY",
                  [("GROVE_COMMUNE", 60, 66, "THE<BSP>COMMUNE"), ("GROVE_ORCHARD", 56, 62, "THE<BSP>ORCHARD"),
                   ("GROVE_HEARTH", 52, 58, "THE<BSP>GREAT<BSP>HEARTH")],
                  "MUSIC_ROUTE_36", texts, TIERS, bosses, [None, "river", "hive"], [3, 2, 3], "GroveGate", T.GATE[0],
                  trainers=([13, 14, 13, 13, 13], [13, 13, 13, 14, 13], 13), stock_ix=(0, 0, 1, 1, 2, 2, 2))
    return build_area(w, roster, rng, cfg, entry_doors)
