"""THE UNDERCROFT: an optional three floor cold archive under Axiom, entered through a hidden portal in a glade of an Axiom lane.  It is where
the late game item, the EXP CHARM, is hidden (alpha 3.1 feedback: a late item for after level 55, deep in a cave of Area 3).  The floors are
generated caves (purg.build_floor), the fights are plain fights (the maps are in the Purgatorio group: nobody dies, nothing counts toward the
kill milestones), the last floor has no way down and holds the charm in a ball."""
import random

from . import vault_text as VT
from .model import link
from . import purg
from .purg import PurgSpec, build_floor, class_table, verify

VAULT_CLASSES = ["U_BOT", "U_DRONE", "U_BOTCOP", "U_WARDBOT", "U_MADDOC", "U_DOCTOR", "U_GUARD", "U_COURIER"]
LM_VAULT = "LANDMARK_UNDERCROFT"


class VaultSpec(PurgSpec):
    pool = "VT"
    T = VT

# name, level range, ball items, hermit gifts
FLOORS = [
    ("AxiomVault1", (62, 66), ["MAX_POTION", "ELIXER", "PP_UP"], ["MAX_ETHER", "ELIXER"]),
    ("AxiomVault2", (66, 70), ["FULL_RESTORE", "MAX_REVIVE"], ["MAX_REVIVE", "FULL_RESTORE"]),
    ("AxiomVault3", (70, 75), ["MAX_ELIXER", "EXP_CHARM"], ["RARE_CANDY", "PP_UP"]),
]


def build(w, roster, rng):
    """Builds the three floors in the PURG group and links the first one to the hidden portal of Axiom (w.vault_door)."""
    g = w.groups["PURG"]
    w.pools["VT"] = dict(seen=VT.SEEN, beaten=VT.BEATEN, after=VT.AFTER)
    w.landmarks.append(("UNDERCROFT", 84, 60, "THE<BSP>UNDERCROFT"))
    old = purg.CLASS_IDS
    purg.CLASS_IDS = VAULT_CLASSES
    try:
        table = class_table()
    finally:
        purg.CLASS_IDS = old
    prev = w.vault_door
    for i, (name, lv, balls, gifts) in enumerate(FLOORS):
        last = i == len(FLOORS) - 1
        m, G, info = build_floor(g, w, roster, rng, table, 20 + i, name, "D", lv, [], balls, gifts, LM_VAULT, "MUSIC_HC_PURGATORIO",
                                 tr_target=7, extra_objs=0, last=last, spec_cls=VaultSpec)
        link(prev, m.warps_in)
        if m.warps_out is not None:
            prev = m.warps_out
        m.obj_area = 2  # the colours of Axiom (the engine reads it from data/hardcore/purg_obj_areas.asm): the fighters are Axiom classes
        g.add(m)
        verify(m, (info["entry"][0] + 1, info["entry"][1]))
