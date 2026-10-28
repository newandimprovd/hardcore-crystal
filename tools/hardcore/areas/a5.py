"""Area 5: the walled city of DIS, the frozen lake COCYTUS, and JUDECCA at its centre where the Sleeper lies."""
from . import a5_text as T
from . import kits
from .builder import AreaCfg, BossSpec, build_area
from .specbase import SpecBase
from .a2 import TIERS


class Spec(SpecBase):
    pool = "A5"
    l0, l1 = 78, 92
    T = T
    theme = {"DARK": 3, "GHOST": 3, "FIRE": 2, "ICE": 2.5, "POISON": 2, "DRAGON": 1.5, "PSYCHIC_TYPE": 1.5,
             "STEEL": 1.5, "FIGHTING": 1.5, "ROCK": 1, "GROUND": 1, "FLYING": 1, "ELECTRIC": 0.8, "NORMAL": 0.8,
             "BUG": 0.7, "WATER": 0.7, "FAIRY": 0.5, "GRASS": 0.3}
    classes = [("BLACKBELT_T", "SPRITE_BLACK_BELT", "PAL_NPC_RED", 2),
               ("PSYCHIC_T", "SPRITE_SAGE", "PAL_NPC_BROWN", 3),
               ("MEDIUM", "SPRITE_GRANNY", "PAL_NPC_RED", 2),
               ("SAGE", "SPRITE_GRAMPS", "PAL_NPC_BROWN", 2),
               ("BURGLAR", "SPRITE_ROCKET", "PAL_NPC_RED", 2),
               ("FIREBREATHER", "SPRITE_SUPER_NERD", "PAL_NPC_RED", 2),
               ("JUGGLER", "SPRITE_ROCKER", "PAL_NPC_BLUE", 2),
               ("GRUNTM", "SPRITE_ROCKET", "PAL_NPC_BROWN", 2),
               ("GRUNTF", "SPRITE_ROCKET_GIRL", "PAL_NPC_RED", 2),
               ("SCIENTIST", "SPRITE_SCIENTIST", "PAL_NPC_GREEN", 1),
               ("GENTLEMAN", "SPRITE_GENTLEMAN", "PAL_NPC_BROWN", 1),
               ("BEAUTY", "SPRITE_BEAUTY", "PAL_NPC_RED", 1),
               ("POKEFANM", "SPRITE_POKEFAN_M", "PAL_NPC_BROWN", 2),
               ("BIKER", "SPRITE_BIKER", "PAL_NPC_RED", 2),
               ("COOLTRAINERM", "SPRITE_COOLTRAINER_M", "PAL_NPC_RED", 1),
               ("COOLTRAINERF", "SPRITE_COOLTRAINER_F", "PAL_NPC_RED", 1)]


def build(w, roster, rng, entry_doors):
    texts = dict(center=T.CENTER, mart=T.MART, house=T.HOUSE)
    bosses = [
        BossSpec("DisGatehouse", "GATEKEEPER", "SAGE", "SPRITE_GRAMPS", "PAL_NPC_BROWN", 83, 5, T.WARDEN_SEEN,
                 T.WARDEN_BEATEN, T.WARDEN_AFTER, template="karen", item="GETAWAY_CAR"),
        BossSpec("CocytusIceHall", "BETRAYER", "BURGLAR", "SPRITE_ROCKET", "PAL_NPC_RED", 87, 5, T.CAGE_SEEN,
                 T.CAGE_BEATEN, T.CAGE_AFTER, template="will"),
        BossSpec("JudeccaCentre", "FINNEGAN", "MYSTICALMAN", "SPRITE_GRAMPS", "PAL_NPC_BLUE", 95, 6, T.SLEEPER_SEEN,
                 T.SLEEPER_BEATEN, T.SLEEPER_AFTER, template="bruno", landmark="LANDMARK_DIS_JUDECCA",
                 music="MUSIC_ROCKET_HIDEOUT", story=3)]
    cfg = AreaCfg("AREA5", "Dis", Spec(), kits.dis(), "PALETTE_DAY",
                  [("DIS_CITY", 24, 50, "THE<BSP>CITY<BSP>OF<BSP>DIS"), ("DIS_COCYTUS", 20, 46, "LAKE<BSP>COCYTUS"),
                   ("DIS_JUDECCA", 16, 42, "JUDECCA")],
                  "MUSIC_ROCKET_HIDEOUT", texts, TIERS, bosses, [None, None, None], [3, 2, 3], "DisGate",
                  T.GATE[0], trainers=([14, 13, 14, 13, 13], [13, 14, 13, 13, 14], 13), stock_ix=(2, 2, 2, 2, 2, 2, 2))
    return build_area(w, roster, rng, cfg, entry_doors)
