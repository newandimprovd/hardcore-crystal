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
         where=("Tithe", 1), item="CHAINSAW", block="STEINER1", forced=True),
    dict(key="CROWLEY", who="CROWLEY", name="CROWLEY", text=N.CROWLEY1, cls="T_CROWLEY", sprite="CROWLEY", pal="BROWN", face="LEFT",
         where=("Tithe", 4), item="CROWBAR", block="CROWLEY1", flight=True, size=6),
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
         where="GroveAmphitheater", at=(8, 8), lvl_at=("Grove", 2), size=6, item="JET_SKI", block="CROWLEY2", block_in=("Grove", 2),
         gate="EVENT_AMPH_DONE", wait=N.CROWLEY_MID_WAIT),
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


def later_block(w, key, label, t):
    """Script lines that tell the `more` paragraphs of a character (named_text.slow) one on each visit after the prize, then fall back to
    `.After`, and the text blocks they use.  Needs the labels .After in the same script."""
    more = t.get("more") or []
    flags = [w.flag(f"EVENT_NAMED_{key}_TALK{i}") for i in range(len(more))]
    s = [".Later:"]
    for i, f in enumerate(flags):
        s += [f"\tcheckevent {f}", f"\tiffalse .More{i}"]
    s += ["\tsjump .After", ""]
    for i, f in enumerate(flags):
        s += [f".More{i}:", f"\twritetext {label}MoreText{i}", "\twaitbutton", f"\tsetevent {f}", "\tclosetext", "\tend", ""]
    return s, [Text(p).emit(f"{label}MoreText{i}") for i, p in enumerate(more)]


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
          ".Beaten:", f"\tcheckevent {paid}", "\tiftrue .Later", f"\twritetext {label}GiveText", "\twaitbutton",
          f"\tverbosegiveitem {item}", "\tiffalse .NoRoom", f"\tsetevent {paid}",
          ".After:", f"\twritetext {label}AfterText", "\twaitbutton", "\tclosetext", "\tend", "",
          ".No:", f"\twritetext {label}NoText", "\twaitbutton", "\tclosetext", "\tend", "",
          ".NoRoom:", f"\twritetext {label}NoRoomText", "\twaitbutton", "\tclosetext", "\tend", ""]
    later, more_texts = later_block(w, key, label, texts)
    s += later
    if gate:
        s += ["", ".Wait:", f"\twritetext {label}WaitText", "\twaitbutton", "\tclosetext", "\tend"]
    m.scripts.append("\n".join(s) + "\n")
    t = texts
    m.scripts.append(Text(t["seen"] + f"\n\nFight {who}?").emit(f"{label}SeenText"))
    m.scripts.append(Text(t["beaten"]).emit(f"{label}BeatenText"))
    m.scripts.append(Text(t["give"]).emit(f"{label}GiveText"))
    m.scripts.append(Text(t["after"]).emit(f"{label}AfterText"))
    m.scripts += more_texts
    m.scripts.append(Text(N.NO).emit(f"{label}NoText"))
    m.scripts.append(Text(N.NOROOM).emit(f"{label}NoRoomText"))
    if gate:
        m.scripts.append(Text(wait).emit(f"{label}WaitText"))
    return paid


def forced_duel_script(w, m, key, label, cls, tid, item, texts, const, *, who=""):
    """A bearer who stands in the street and does not let the player pass: stepping on one of the trigger cells starts the talk at once,
    there is no question and no way to refuse.  The talk script (the same flow, after faceplayer) serves for later visits.  After the
    prize he steps out of the lane."""
    done = w.flag(f"EVENT_NAMED_{key}_DONE")
    paid = w.flag(f"EVENT_NAMED_{key}_PAID")
    lf = flag_once(w, f"EVENT_LORE_{key}")
    flow = f"{label}Flow"
    s = [f"{label}Trigger:", f"\tcheckevent {done}", "\tiftrue .Done", f"\tturnobject {const}, DOWN",
         f"\tshowemote EMOTE_SHOCK, {const}, 15", f"\tsjump {flow}", ".Done:", "\tend", "",
         f"{label}:", "\tfaceplayer", f"{flow}:", "\topentext", f"\tcheckevent {done}", "\tiftrue .Beaten", f"\tsetevent {lf}",
         f"\twritetext {label}SeenText", "\twaitbutton", "\tclosetext", f"\twinlosstext {label}BeatenText, 0",
         f"\tloadtrainer {cls}, {tid}", "\tstartbattle", "\treloadmapafterbattle", f"\tsetevent {done}", "\topentext",
         ".Beaten:", f"\tcheckevent {paid}", "\tiftrue .Later", f"\twritetext {label}GiveText", "\twaitbutton",
         f"\tverbosegiveitem {item}", "\tiffalse .NoRoom", f"\tsetevent {paid}", f"\twritetext {label}AfterText", "\twaitbutton",
         "\tclosetext", f"\tapplymovement {const}, {label}Aside", "\tend", "",
         ".After:", f"\twritetext {label}AfterText", "\twaitbutton", "\tclosetext", "\tend", "",
         ".NoRoom:", f"\twritetext {label}NoRoomText", "\twaitbutton", "\tclosetext", "\tend", ""]
    later, more_texts = later_block(w, key, label, texts)
    s += later  # the local labels of the flow must all come before the next global label
    s += [f"{label}Aside:", "\tstep RIGHT", "\tstep RIGHT", "\tstep RIGHT", "\tstep_end"]
    m.scripts.append("\n".join(s) + "\n")
    t = texts
    m.scripts.append(Text(t["seen"]).emit(f"{label}SeenText"))
    m.scripts.append(Text(t["beaten"]).emit(f"{label}BeatenText"))
    m.scripts.append(Text(t["give"]).emit(f"{label}GiveText"))
    m.scripts.append(Text(t["after"]).emit(f"{label}AfterText"))
    m.scripts += more_texts
    m.scripts.append(Text(N.NOROOM).emit(f"{label}NoRoomText"))
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


def flight_lane(m):
    """The start cell of a man who runs down the street towards the player (Crowley fleeing the playground at the head of the plaza).
    The engine only keeps the objects that are inside the screen and one cell around it (an object outside is neither loaded nor moved by
    a script), so the flight has to start inside that window: the trigger row is the entry row of the plaza (2 * (h - 2)), the player
    stands on it when the scene starts, and the window reaches five rows up.  The man starts three rows above the trigger row, the
    followers right behind him (two in his column, one beside the last), and he runs two steps down.  The lane is a column of the street
    stem that no object stands on."""
    e, xo, jr = m.street
    y0 = 2 * (m.h - 4)
    taken = {(o["x"], o["y"]) for o in m.objects}
    for dx in (0, 1, -1, 2, -2):
        x = 2 * e + m.cw + dx
        if all((x, y) not in taken for y in range(y0 - 1, y0 + 4)) and (x + 1, y0 - 1) not in taken:
            return x, y0 + 1
    raise AssertionError(f"{m.name}: no free lane for the flight")


def flight_duel(w, g, m, d, label, tid, x, y):
    """Crowley at the head of the plaza, fleeing a mob: when the player steps into the street (the row of triggers four cells below the lane
    end) he runs down the lane, the mob staggers after him, and the talk starts at once.  After the prize he leaves the map with the mob.
    The man and the mob carry the event flag of the prize, so they are gone from the plaza for good."""
    from . import cameos as K
    key, cls, item = d["key"], d["cls"], d["item"]
    K.add_sprite(g, "SPRITE_HC_SUIT", "SPRITE_HC_HOODIE", "SPRITE_HC_COP")
    done = w.flag(f"EVENT_NAMED_{key}_DONE")
    paid = w.flag(f"EVENT_NAMED_{key}_PAID")
    ran = w.flag(f"EVENT_NAMED_{key}_RAN")
    lf = flag_once(w, f"EVENT_LORE_{key}")
    const = name_object(m, len(m.objects) + 1, f"RUNNER_{key}")
    m.obj(x, y, f"SPRITE_HC_{d['sprite']}", FACE["DOWN"], label, pal=f"PAL_NPC_{d['pal']}", flag=paid)
    mob = [("SPRITE_HC_SUIT", "PAL_NPC_BROWN"), ("SPRITE_HC_HOODIE", "PAL_NPC_GREEN"), ("SPRITE_HC_COP", "PAL_NPC_BLUE")]
    cs = []
    for i, (sp, pal) in enumerate(mob):
        cs.append(name_object(m, len(m.objects) + 1, f"MOB_{key}_{i}"))
        m.obj(x + (i == 2), y - 1 - min(i, 1), sp, FACE["DOWN"], f"{label}Mob{i}", pal=pal, flag=paid)
        m.scripts.append(f"{label}Mob{i}:\n\tjumptextfaceplayer {label}Mob{i}Text\n")
        m.scripts.append(Text(N.CROWLEY_FLIGHT[i]).emit(f"{label}Mob{i}Text"))
    flow = f"{label}Flow"
    down3 = ["\tstep DOWN"] * 2
    s = [f"{label}Trigger:", f"\tcheckevent {ran}", "\tiftrue .Done", f"\tsetevent {ran}",
         f"\tapplymovement {const}, {label}Run", f"\tturnobject {const}, DOWN", f"\tshowemote EMOTE_SHOCK, {const}, 15"]
    s += [f"\tapplymovement {c}, {label}Chase" for c in cs]
    s += ["\topentext", f"\twritetext {label}MobText", "\twaitbutton", "\tclosetext", f"\tsjump {flow}", ".Done:", "\tend", "",
          f"{label}:", "\tfaceplayer", f"{flow}:", "\topentext", f"\tcheckevent {done}", "\tiftrue .Beaten", f"\tsetevent {lf}",
          f"\twritetext {label}SeenText", "\twaitbutton", "\tclosetext", f"\twinlosstext {label}BeatenText, 0",
          f"\tloadtrainer {cls}, {tid}", "\tstartbattle", "\treloadmapafterbattle", f"\tsetevent {done}", "\topentext",
          ".Beaten:", f"\tcheckevent {paid}", "\tiftrue .After", f"\twritetext {label}GiveText", "\twaitbutton",
          f"\tverbosegiveitem {item}", "\tiffalse .NoRoom", f"\tsetevent {paid}", f"\twritetext {label}AfterText", "\twaitbutton",
          "\tclosetext", "\tplaysound SFX_EXIT_BUILDING", f"\tdisappear {const}"]
    s += [f"\tdisappear {c}" for c in cs]
    s += ["\twaitsfx", "\tend", "", ".After:", f"\twritetext {label}AfterText", "\twaitbutton", "\tclosetext", "\tend", "",
          ".NoRoom:", f"\twritetext {label}NoRoomText", "\twaitbutton", "\tclosetext", "\tend", "",
          f"{label}Run:"] + ["\tbig_step DOWN"] * 2 + ["\tstep_end", "", f"{label}Chase:"] + down3 + ["\tstep_end"]
    m.scripts.append("\n".join(s) + "\n")
    t = d["text"]
    m.scripts.append(Text(t["seen"]).emit(f"{label}SeenText"))
    m.scripts.append(Text(t["beaten"]).emit(f"{label}BeatenText"))
    m.scripts.append(Text(t["give"]).emit(f"{label}GiveText"))
    m.scripts.append(Text(t["after"]).emit(f"{label}AfterText"))
    m.scripts.append(Text(N.NOROOM).emit(f"{label}NoRoomText"))
    m.scripts.append(Text("\n\n".join(N.CROWLEY_FLIGHT)).emit(f"{label}MobText"))
    e, xo, jr = m.street
    for tx in range(2 * e, 2 * (e + m.cw)):
        m.coords.append((tx, 2 * (m.h - 2), -1, f"{label}Trigger"))
    return paid


def add_duel(w, g, d, roster, m=None):
    from . import cameos as K
    where = d["where"]
    if isinstance(where, tuple):
        tag, plaza = where
        m = K.find(g, f"{tag}Plaza{plaza}")
        level = level_at(tag, plaza)
        size = d.get("size", min(6, 3 + plaza // 3))
    else:
        m = m or K.find(g, where)
        level = d["level"] if "level" in d else level_at(*d["lvl_at"])
        size = d.get("size", 6)
    K.add_sprite(g, f"SPRITE_HC_{d['sprite']}")
    party = make_party(roster, random.Random("named-" + d["key"]), level, size, THEMES[d["who"]], hard=True)
    tid = w.trainer(d["cls"], d["name"], party)
    label = f"{m.name}{d['key'].title()}{'Bearer' if d.get('block') else 'Duel'}Script"
    if d.get("forced"):
        x = y = 0
    elif "at" in d:
        x, y = d["at"]
        assert (x, y) not in {(o["x"], o["y"]) for o in m.objects}, f"{m.name}: {d['key']} spot taken"
    elif d.get("flight"):
        x, y = flight_lane(m)
    else:
        x, y = K.free_cells(m)[-1]
    if d.get("forced"):
        # the bearer stands in the lane of the street at the top of the plaza.  The street is entered from the two-cell corridor that runs along
        # the foot of the buildings: the trigger row is the corridor cell right below the street mouth (one cell below the bearer), and the
        # row can not be walked around because the street is only reachable through it
        e, xo, jr = m.street
        x, y = 2 * xo + 2, 3
        assert (x, y) not in {(o["x"], o["y"]) for o in m.objects}, f"{m.name}: {d['key']} spot taken"
        const = name_object(m, len(m.objects) + 1, f"BEARER_{d['key']}")
        paid = forced_duel_script(w, m, d["key"], label, d["cls"], tid, d["item"], d["text"], const, who=d["name"])
        m.obj(x, y, f"SPRITE_HC_{d['sprite']}", FACE["DOWN"], label, pal=f"PAL_NPC_{d['pal']}")
        for tx in range(2 * xo, 2 * (xo + m.cw)):
            m.coords.append((tx, 4, -1, f"{label}Trigger"))
    elif d.get("flight"):
        paid = flight_duel(w, g, m, d, label, tid, x, y)
    else:
        paid = duel_script(w, m, d["key"], label, d["cls"], tid, d["item"], d["text"], who=d["name"], wait=d.get("wait"), gate=d.get("gate"))
        m.obj(x, y, f"SPRITE_HC_{d['sprite']}", FACE[d["face"]], label, pal=f"PAL_NPC_{d['pal']}")
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
