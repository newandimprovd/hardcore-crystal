"""HOLLOWS: ten small hidden caves, two to an area (alpha 3.2, playtest feedback: "a lot to fight but nothing to explore").

A hollow is entered through the same kind of hidden portal as the Undercroft: a door in the back wall of a glade beside one lane, reached through a
one block gap in the tree line that nothing on the road points at (trail.py, hollow=True).  Behind it is one cave floor of the Purgatorio group, so
the fights are plain fights (nobody dies, nothing counts toward the kill milestones).  Every hollow holds five fighters, two hermits who give a
present once they have been beaten, two item balls, a sign by the ladder that names the place and a plaque at the far end that tells its story.
The floors are built here, after all areas exist (gen_areas.py), from the doors that builder.build_act registered in w.hollow_doors."""
import random
from types import SimpleNamespace

from art.classes import by_const, sprite as csprite

from . import hollow_text as HT
from .model import link
from .people import sign
from .purg import PurgSpec, build_floor, post_spot, verify

MUSIC = "MUSIC_HC_PURGATORIO"

THEMES = {
    "Tithe": {"GHOST": 3, "DARK": 2.5, "NORMAL": 2, "FIGHTING": 1.5, "POISON": 1.5, "FAIRY": 1.5, "ROCK": 1, "PSYCHIC_TYPE": 1, "FIRE": 1, "STEEL": 1},
    "Grove": {"GRASS": 3, "BUG": 2.5, "POISON": 2, "FAIRY": 2, "NORMAL": 1.5, "GROUND": 1.5, "FLYING": 1.5, "WATER": 1, "GHOST": 1, "ROCK": 1},
    "Axiom": {"STEEL": 3, "ELECTRIC": 2.5, "PSYCHIC_TYPE": 2.5, "NORMAL": 2, "POISON": 1.5, "FIGHTING": 1, "GHOST": 1, "DARK": 1, "FIRE": 1},
    "Lotus": {"WATER": 3, "ICE": 2, "FLYING": 2, "GHOST": 2, "PSYCHIC_TYPE": 1.5, "FAIRY": 1.5, "NORMAL": 1.5, "GRASS": 1, "FIRE": 1, "DARK": 1},
    "Dis": {"FIRE": 3, "DARK": 3, "GHOST": 2.5, "DRAGON": 2, "POISON": 1.5, "PSYCHIC_TYPE": 1.5, "FIGHTING": 1, "ROCK": 1, "STEEL": 1},
}
AREA_INDEX = {"Tithe": 0, "Grove": 1, "Axiom": 2, "Lotus": 3, "Dis": 4}
POOL = {"Tithe": "HL1", "Grove": "HL2", "Axiom": "HL3", "Lotus": "HL4", "Dis": "HL5"}

# key, act the lane lies in, trainer classes (existing ones, they carry the look of the area), the two item balls (the first is the better one)
# and the two presents of the hermits
PLAN = {
    "Tithe": [
        dict(key="AlmsCellar", act=0, classes=["T_BEGGAR", "T_NUN", "T_ALTARBOY", "T_DRIFTER", "T_SISTER", "T_PRIEST"],
             balls=["RARE_CANDY", "SUPER_POTION"], gifts=["PROTEIN", "IRON"]),
        dict(key="Ossuary", act=1, classes=["T_PRIEST", "T_DEACON", "T_NUN", "T_BEGGAR", "T_COP", "T_SUIT"],
             balls=["MAX_ETHER", "HYPER_POTION"], gifts=["HP_UP", "CALCIUM"]),
    ],
    "Grove": [
        dict(key="HollowOak", act=0, classes=["G_ELDER", "G_GRANNY", "G_SHAMAN", "G_FORAGER", "G_BIRDER", "G_SPROUT"],
             balls=["PP_UP", "HYPER_POTION"], gifts=["CARBOS", "PROTEIN"]),
        dict(key="MossChapel", act=1, classes=["G_DRUIDESS", "G_ELDRESS", "G_SHAMAN", "G_BARD", "G_ELDER", "G_FLOWERKID"],
             balls=["RARE_CANDY", "FULL_RESTORE"], gifts=["HP_UP", "IRON"]),
    ],
    "Axiom": [
        dict(key="SpareRoom", act=2, classes=["U_SERF", "U_SERFF", "U_DOCTOR", "U_CASEWORKER", "U_DRONE", "U_BOT"],
             balls=["MAX_ELIXER", "PP_UP"], gifts=["RARE_CANDY", "CALCIUM"]),
        dict(key="BreakRoom", act=1, classes=["U_EXEC", "U_MATCHMAKER", "U_GUARD", "U_COURIER", "U_MADDOC", "U_WARDBOT"],
             balls=["FULL_RESTORE", "MAX_REVIVE"], gifts=["PP_UP", "CARBOS"]),
    ],
    "Lotus": [
        dict(key="DryPool", act=0, classes=["L_LIFEGUARD", "L_SWIMMERM", "L_SWIMMERF", "L_SUNBATHER", "L_BEACHBUM", "L_TOURISTF"],
             balls=["MAX_POTION", "PP_UP"], gifts=["MAX_REVIVE", "HP_UP"]),
        dict(key="LastCabana", act=2, classes=["L_FORGOTTEN", "L_CLINICIAN", "L_WAITER", "L_LOUNGER", "L_BELLHOP", "L_MANAGER"],
             balls=["RARE_CANDY", "MAX_ELIXER"], gifts=["PP_UP", "PROTEIN"]),
    ],
    "Dis": [
        dict(key="FilingPit", act=0, classes=["D_JUDGE", "D_SHADE", "D_HAG", "D_IMP", "D_WARDEN", "D_JESTER"],
             balls=["MAX_ELIXER", "FULL_RESTORE"], gifts=["MAX_REVIVE", "PP_UP"]),
        dict(key="FurnaceRoom", act=2, classes=["D_FIREEATER", "D_BRUTE", "D_IMP", "D_SHADE", "D_WARDEN", "D_JUDGE"],
             balls=["MAX_REVIVE", "MAX_ELIXER"], gifts=["PP_UP", "FULL_RESTORE"]),
    ],
}


def planned(tag, act_index):
    """The hollows of this area that lie in this act."""
    return [h for h in PLAN.get(tag, []) if h["act"] == act_index]


def lanes_for(act, turns):
    """{lane index: hollow plan} for the lanes of this act that hide a hollow: never the first lane (the gate), the last one of an act with a
    rift (the Purgatorio portal), the lane of the Undercroft, or a lane that is turned."""
    out = {}
    for h in planned(act.tag, act.index):
        ok = [i for i in range(1, act.lanes - 1) if i not in turns and i not in out
              and not (act.tag == "Axiom" and i == act.lanes - 2)]
        if ok:
            R = random.Random("hollow:" + act.tag + h["key"])
            out[R.choice(ok)] = h
    return out


def table_of(consts):
    out = []
    for c in consts:
        _, e = by_const(c)
        out.append((e[0], csprite(e[2]), "PAL_NPC_" + e[3], 3))
    return out


def spec_class(tag):
    class HollowSpec(PurgSpec):
        pool = POOL[tag]
        T = SimpleNamespace(**HT.POOLS[POOL[tag]])
        theme = THEMES[tag]
    return HollowSpec


def level_of(act, lane_i):
    """Level of the fighters of a hollow: the level of the lane it hides next to, a little above (the reward for finding it)."""
    prog = (act.index * act.lanes + lane_i + 0.5) / (3 * act.lanes)
    s = act.spec
    return int(round(s.l0 + (s.l1 - s.l0) * prog)) + 2


def register(w, act, lane_i, h, lane_map):
    """Remembers the hidden door of lane_map for build()."""
    if not hasattr(w, "hollow_doors"):
        w.hollow_doors = []
    w.hollow_doors.append(dict(h=h, tag=act.tag, door=lane_map.hollow_door, lm=act.landmark, level=level_of(act, lane_i),
                               lane=lane_map.name))


def build(w, roster, rng):
    """Builds one cave floor in the PURG group for every registered door and links it to the hidden portal."""
    g = w.groups["PURG"]
    for key, pool in HT.POOLS.items():
        w.pools[key] = dict(seen=pool["seen"], beaten=pool["beaten"], after=pool["after"])
    for n, reg in enumerate(getattr(w, "hollow_doors", [])):
        h, tag = reg["h"], reg["tag"]
        name = tag + h["key"]
        lv = reg["level"]
        m, G, info = build_floor(g, w, roster, random.Random(f"hollow:{name}"), table_of(h["classes"]), 30 + n, name, "D", (lv, lv + 3), [],
                                 h["balls"], h["gifts"], reg["lm"], MUSIC, tr_target=5, extra_objs=0, last=True, spec_cls=spec_class(tag))
        m.obj_area = AREA_INDEX[tag]  # the fighters wear the colours of their area, like their battle portraits do
        link(reg["door"], m.warps_in)
        g.add(m)
        entry, far = info["entry"], info["exit"]
        taken = [(o["x"], o["y"]) for o in m.objects] + [(entry[0] + 1, entry[1] + 1)]
        near_text, far_text = HT.SIGNS[h["key"]]
        sx, sy = post_spot(G, entry, taken)
        sign(m, sx, sy, f"{name}Sign", near_text)
        px, py = post_spot(G, far, taken + [(sx, sy)])
        sign(m, px, py, f"{name}Plaque", far_text)
        verify(m, (entry[0] + 1, entry[1]))
