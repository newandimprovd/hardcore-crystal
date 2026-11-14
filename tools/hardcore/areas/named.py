"""The named duels: the historic characters and the rival.  Scripted duels (loadtrainer, startbattle, reloadmapafterbattle), so nobody dies:
the trainer-death engine only reacts to trainer objects, and battle_budget.py counts them with the other scripted fights.

  * KEY BEARERS (mandatory).  Eight fights that hand over the key items that replace the HMs, the way Steven and Cynthia do: the road does not
    go on until the prize is in the bag.  A coordinate trigger across the plaza's exit sends the player back with a hint until it is.
        Steiner  TithePlaza1 CHAINSAW       GrovePlaza4 BASEBALL_BAT      Crowley  TithePlaza4 CROWBAR      the Amphitheater JET_SKI
        Sabbah   AxiomPlaza1 FLASHLIGHT     AxiomPlaza4 SLEDGEHAMMER      Cioran   LotusPlaza1 GRAPPLE_HOOK LotusPlaza4 SHOVEL
  * LATE PHILOSOPHERS (optional).  Steiner in Purgatorio and in Lotus, Suhrawardi in Axiom, Abd al-Jabbar in Purgatorio, Mulla Sadra in Dis.
    Each pays a consumable the first time and pins a page of the CORKBOARD; with all of them the board shows its last page.
  * THE RIVAL.  Five duels (Cherrygrove junction, plaza 2 of Areas 1 to 3, the Purgatorio hub); the sixth is the boss of the mansion.
Levels follow the place in the game (the area's range at the plaza's position), the teams a theme of the character's own."""
import random

from . import named_text as N
from .flags import flag_once
from .layout import FACE
from .party import make_party
from .text import Text

AREA_OF = {"Tithe": "AREA1", "Grove": "AREA2", "Axiom": "AREA3", "Lotus": "AREA4", "Dis": "AREA5"}

THEMES = {
    "STEINER": {"PSYCHIC_TYPE": 3, "GHOST": 2, "FAIRY": 2, "STEEL": 1, "FLYING": 1},
    "CROWLEY": {"DARK": 3, "GHOST": 2, "FIRE": 2, "PSYCHIC_TYPE": 1.5, "POISON": 1},
    "SABBAH": {"POISON": 3, "DARK": 2, "GROUND": 1.5, "FIRE": 1, "BUG": 1},
    "CIORAN": {"GHOST": 3, "ICE": 2, "WATER": 1.5, "DARK": 2, "PSYCHIC_TYPE": 1},
    "SUHRAWARDI": {"PSYCHIC_TYPE": 3, "FAIRY": 2.5, "ELECTRIC": 1.5, "FLYING": 1.5, "FIRE": 1},
    "QADI": {"STEEL": 2.5, "NORMAL": 2, "FIGHTING": 2, "ROCK": 1.5, "DARK": 1},
    "SADRA": {"FIRE": 2.5, "DRAGON": 2, "PSYCHIC_TYPE": 1.5, "GRASS": 1.5, "WATER": 1},
    "RIVAL": {"DARK": 3, "NORMAL": 2, "FIGHTING": 1.5, "FIRE": 1, "GHOST": 1, "STEEL": 1},
}

# key: Corkboard page and name of the flags; who: theme and speaker; text: the dict of named_text; cls, sprite, pal: the class and the NPC;
# where: (area tag, plaza number) or a map name for the odd places; item: the prize (the key item of a bearer, a consumable for the rest);
# block: the key of N.BLOCK when the duel is mandatory (a trigger across the plaza's exit)
DUELS = [
    dict(key="STEINER", who="STEINER", name="STEINER", text=N.STEINER1, cls="T_STEINER", sprite="STEINER", pal="BROWN", face="LEFT",
         where=("Tithe", 1), item="CHAINSAW", block="STEINER1"),
    dict(key="CROWLEY", who="CROWLEY", name="CROWLEY", text=N.CROWLEY1, cls="T_CROWLEY", sprite="CROWLEY", pal="BROWN", face="LEFT",
         where=("Tithe", 4), item="CROWBAR", block="CROWLEY1", crowd=True),
    dict(key="STEINER2", who="STEINER", name="STEINER", text=N.STEINER2, cls="T_STEINER", sprite="STEINER", pal="BROWN", face="LEFT",
         where=("Grove", 4), item="BASEBALL_BAT", block="STEINER2"),
    dict(key="SABBAH", who="SABBAH", name="SABBAH", text=N.SABBAH1, cls="U_SABBAH", sprite="SABBAH", pal="BROWN", face="LEFT",
         where=("Axiom", 1), item="FLASHLIGHT", block="SABBAH1"),
    dict(key="SABBAH2", who="SABBAH", name="SABBAH", text=N.SABBAH2, cls="U_SABBAH", sprite="SABBAH", pal="BROWN", face="LEFT",
         where=("Axiom", 4), item="SLEDGEHAMMER", block="SABBAH2"),
    dict(key="CIORAN", who="CIORAN", name="CIORAN", text=N.CIORAN1, cls="L_CIORAN", sprite="CIORAN", pal="BROWN", face="LEFT",
         where=("Lotus", 1), item="GRAPPLE_HOOK", block="CIORAN1"),
    dict(key="CIORAN2", who="CIORAN", name="CIORAN", text=N.CIORAN2, cls="L_CIORAN", sprite="CIORAN", pal="BROWN", face="LEFT",
         where=("Lotus", 4), item="SHOVEL", block="CIORAN2"),
    dict(key="AMPH", who="CROWLEY", name="CROWLEY", text=N.CROWLEY2, cls="T_CROWLEY", sprite="CROWLEY", pal="BROWN", face="DOWN",
         where="GroveAmphitheater", at=(8, 8), lvl_at=("Grove", 2), size=3, item="JET_SKI", block="CROWLEY2", block_in=("Grove", 2),
         gate="EVENT_AMPH_DONE", wait="Sit. Do not take notes. The circle is not yet full."),
    # the optional ones
    dict(key="STEINER4", who="STEINER", name="STEINER", text=N.STEINER4, cls="T_STEINER", sprite="STEINER", pal="BROWN", face="LEFT",
         where=("Lotus", 6), item="PP_UP"),
    dict(key="SUHRAWARDI", who="SUHRAWARDI", name="SUHRAWARDI", text=N.SUHRAWARDI, cls="U_SUHRAWARDI", sprite="ELDER_M", pal="GREEN",
         face="RIGHT", where=("Axiom", 6), item="PP_UP"),
    dict(key="SADRA", who="SADRA", name="SADRA", text=N.SADRA, cls="D_SADRA", sprite="ELDER_M", pal="RED", face="LEFT",
         where=("Dis", 6), item="PP_UP"),
    dict(key="STEINER3", who="STEINER", name="STEINER", text=N.STEINER3, cls="T_STEINER", sprite="STEINER", pal="BROWN", face="LEFT",
         where="PurgThreshold", at=(32, 22), level=40, item="RARE_CANDY"),
    dict(key="QADI", who="QADI", name="ABD JABBAR", text=N.QADI, cls="D_QADI", sprite="JUDGE", pal="BLUE", face="UP",
         where="PurgThreshold", at=(21, 27), level=46, item="RARE_CANDY"),
]

def _spec(tag):
    from . import a1, a2, a3, a4, a5
    return {"Tithe": a1.Spec, "Grove": a2.Spec, "Axiom": a3.Spec, "Lotus": a4.Spec, "Dis": a5.Spec}[tag]()


def level_at(tag, plaza):
    spec = _spec(tag)
    return int(round(spec.l0 + (spec.l1 - spec.l0) * (plaza - 0.5) / 7)) + 3


def name_object(m, idx, name):
    """Gives the object number idx (1 based, as m.obj returns it) a map constant; the earlier objects get filler names."""
    while len(m.object_consts) < idx - 1:
        m.object_consts.append(f"OBJ{len(m.object_consts)}")
    assert len(m.object_consts) == idx - 1, f"{m.name}: constants out of step"
    m.object_consts.append(name)
    return f"{m.const}_{name}"


def duel_script(w, m, key, label, cls, tid, item, texts, *, wait=None, gate=None, lore=True, who=""):
    """The talk script of a named duel.  Returns the flag that says the prize has been handed over."""
    done = w.flag(f"EVENT_NAMED_{key}_DONE")
    paid = w.flag(f"EVENT_NAMED_{key}_PAID")
    lf = flag_once(w, f"EVENT_LORE_{key}") if lore else None
    s = [f"{label}:", "\tfaceplayer", "\topentext"]
    if gate:  # something has to happen first (the Amphitheater ritual)
        s += [f"\tcheckevent {gate}", "\tiffalse .Wait"]
    s += [f"\tcheckevent {done}", "\tiftrue .Beaten"]
    if lf:
        s += [f"\tsetevent {lf}"]
    s += [f"\twritetext {label}SeenText", "\tyesorno", "\tiffalse .No", "\tclosetext", f"\twinlosstext {label}BeatenText, 0",
          f"\tloadtrainer {cls}, {tid}", "\tstartbattle", "\treloadmapafterbattle", f"\tsetevent {done}", "\topentext",
          ".Beaten:", f"\tcheckevent {paid}", "\tiftrue .After", f"\twritetext {label}GiveText", "\twaitbutton",
          f"\tverbosegiveitem {item}", "\tiffalse .NoRoom", f"\tsetevent {paid}",
          ".After:", f"\twritetext {label}AfterText", "\twaitbutton", "\tclosetext", "\tend", "",
          ".No:", f"\twritetext {label}NoText", "\twaitbutton", "\tclosetext", "\tend", "",
          ".NoRoom:", f"\twritetext {label}NoRoomText", "\twaitbutton", "\tclosetext", "\tend"]
    if gate:
        s += ["", ".Wait:", f"\twritetext {label}WaitText", "\twaitbutton", "\tclosetext", "\tend"]
    m.scripts.append("\n".join(s) + "\n")
    t = texts
    m.scripts.append(Text(t["seen"] + f"\n\nFight {who}?").emit(f"{label}SeenText"))
    m.scripts.append(Text(t["beaten"]).emit(f"{label}BeatenText"))
    m.scripts.append(Text(t["give"]).emit(f"{label}GiveText"))
    m.scripts.append(Text(t["after"]).emit(f"{label}AfterText"))
    m.scripts.append(Text(N.NO).emit(f"{label}NoText"))
    m.scripts.append(Text(N.NOROOM).emit(f"{label}NoRoomText"))
    if gate:
        m.scripts.append(Text(wait).emit(f"{label}WaitText"))
    return paid


def block_exit(m, key, paid, hint):
    """A trigger across the exit of the plaza (the top end of the street): until the prize is in the bag the player is sent back one step."""
    e, xo, jr = m.street
    label = f"{m.name}{key.title()}BlockScript"
    m.scripts.append(
        f"{label}:\n\tcheckevent {paid}\n\tiftrue .Pass\n\topentext\n\twritetext {label}Text\n\twaitbutton\n\tclosetext\n"
        f"\tapplymovement PLAYER, {label}Step\n.Pass:\n\tend\n\n{label}Step:\n\tstep_down\n\tstep_end\n")
    m.scripts.append(Text(hint).emit(f"{label}Text"))
    for x in range(2 * xo, 2 * (xo + m.cw)):
        m.coords.append((x, 1, -1, label))


def add_duel(w, g, d, roster, m=None):
    from . import cameos as K
    where = d["where"]
    if isinstance(where, tuple):
        tag, plaza = where
        m = K.find(g, f"{tag}Plaza{plaza}")
        level = level_at(tag, plaza)
        size = min(6, 3 + plaza // 3)
    else:
        m = m or K.find(g, where)
        level = d["level"] if "level" in d else level_at(*d["lvl_at"])
        size = d.get("size", 6)
    K.add_sprite(g, f"SPRITE_HC_{d['sprite']}")
    party = make_party(roster, random.Random("named-" + d["key"]), level, size, THEMES[d["who"]])
    tid = w.trainer(d["cls"], d["name"], party)
    label = f"{m.name}{d['key'].title()}{'Bearer' if d.get('block') else 'Duel'}Script"
    offs = [(-3, -1), (-3, 1), (-2, 0)]
    if "at" in d:
        x, y = d["at"]
        assert (x, y) not in {(o["x"], o["y"]) for o in m.objects}, f"{m.name}: {d['key']} spot taken"
    elif d.get("crowd"):
        x, y = K.cluster(m, offs)
    else:
        x, y = K.free_cells(m)[-1]
    paid = duel_script(w, m, d["key"], label, d["cls"], tid, d["item"], d["text"], who=d["name"], wait=d.get("wait"), gate=d.get("gate"))
    m.obj(x, y, f"SPRITE_HC_{d['sprite']}", FACE[d["face"]], label, pal=f"PAL_NPC_{d['pal']}")
    if d.get("crowd"):
        from . import cast_text as C
        from .people import plain_npc
        crowd = [("SPRITE_HC_SUIT", "PAL_NPC_BROWN", C.CROWD_1), ("SPRITE_HC_HOODIE", "PAL_NPC_GREEN", C.CROWD_2),
                 ("SPRITE_HC_COP", "PAL_NPC_BLUE", C.CROWD_3)]
        for i, ((dx, dy), (sp, pal, t)) in enumerate(zip(offs, crowd)):
            plain_npc(m, x + dx, y + dy, sp, pal, "RIGHT", f"{m.name}Crowd{i}Script", t)
    if d.get("block"):
        bm = K.find(g, "%sPlaza%d" % d["block_in"]) if "block_in" in d else m
        block_exit(bm, d["key"], paid, N.BLOCK[d["block"]])
    return m


def add_all(w, roster):
    """Every duel that stands in a plaza of an area (run after the plazas, the crowd and cameos.py).  The amphitheater is added by
    cameos.amphitheater, the Purgatorio hub by purg.hub, because those maps are built by them."""
    for d in DUELS:
        if isinstance(d["where"], tuple):
            add_duel(w, w.groups[AREA_OF[d["where"][0]]], d, roster)


def add_one(w, g, key, roster, m=None):
    for d in DUELS:
        if d["key"] == key:
            return add_duel(w, g, d, roster, m)
    raise KeyError(key)


def add_hub(w, g, m, roster):
    """The Purgatorio hub: Steiner and Abd al-Jabbar."""
    for d in DUELS:
        if d["where"] == "PurgThreshold":
            add_duel(w, g, d, roster, m)


# ---------------------------------------------------------------------------------------------------------------- the rival
def rival_duel(w, m, key, cls, level, size, rng, roster, texts, spot, trigger, *, face="DOWN", after=None, requires=None):
    """The rival stands at `spot`; stepping on one of the `trigger` cells (or talking to him) starts the duel, then he walks off the map.
    requires: an event flag that has to be set first (the Purgatorio mouth of Area 3); until then he is not there."""
    party = make_party(roster, rng, level, size, THEMES["RIVAL"])
    tid = w.trainer(cls, "RIVAL", party)
    done = w.flag(f"EVENT_NAMED_{key}_DONE")
    label = f"{m.name}{key.title()}RivalScript"
    idx = len(m.objects) + 1
    const = name_object(m, idx, f"RIVAL_{key}")
    s = [f"{label}:", "\tcheckevent " + done, "\tiftrue .Gone"]
    if requires:
        s += [f"\tcheckevent {requires}", "\tiffalse .Gone"]
    s += ["\tfaceplayer", "\topentext", f"\twritetext {label}SeenText", "\twaitbutton", "\tclosetext",
          f"\twinlosstext {label}BeatenText, 0", f"\tloadtrainer {cls}, {tid}", "\tstartbattle", "\treloadmapafterbattle",
          f"\tsetevent {done}", "\topentext", f"\twritetext {label}AfterText", "\twaitbutton", "\tclosetext",
          "\tplaysound SFX_EXIT_BUILDING", f"\tdisappear {const}", "\twaitsfx", "\tend", "", ".Gone:", "\tend"]
    m.scripts.append("\n".join(s) + "\n")
    m.scripts.append(Text(texts["seen"]).emit(f"{label}SeenText"))
    m.scripts.append(Text(texts["beaten"]).emit(f"{label}BeatenText"))
    m.scripts.append(Text(after or texts["after"]).emit(f"{label}AfterText"))
    m.obj(spot[0], spot[1], "SPRITE_RIVAL", FACE[face], label, pal="PAL_NPC_RED", flag=done)
    for (x, y) in trigger:
        m.coords.append((x, y, -1, label))
    if requires:  # the object is only on the map once the flag is set
        cb = f"{label}Appear"
        m.scripts.append(f"{cb}:\n\tcheckevent {requires}\n\tiftrue .Show\n\tdisappear {const}\n.Show:\n\tendcallback\n")
        m.callbacks.append(("MAPCALLBACK_OBJECTS", cb))
    return label


def plaza_rival(w, g, plaza_name, key, cls, level, size, rng, roster, texts, find, add_sprite):
    """The rival in the bottom stem of the plaza, a row of triggers four cells below him across the whole street."""
    m = find(g, plaza_name)
    e, xo, jr = m.street
    H = m.h
    x0 = 2 * e + m.cw
    taken = {(o["x"], o["y"]) for o in m.objects}
    y0 = 2 * (H - 4)
    for dx in (0, 1, -1, 2):
        if (x0 + dx, y0) not in taken:
            x0 += dx
            break
    else:
        raise AssertionError(f"{m.name}: no free cell for the rival")
    trig = [(x, 2 * (H - 2)) for x in range(2 * e, 2 * (e + m.cw))]
    add_sprite(g, "SPRITE_RIVAL")
    return rival_duel(w, m, key, cls, level, size, rng, roster, texts, (x0, y0), trig)
