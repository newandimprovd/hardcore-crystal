"""The special encounters: named duelists, six to an area, one in each of the plazas 1 to 6, found by talking to them.

Each asks first (yes or no, so a player who is not ready can walk away), fights once with a team of its own (the area's theme, a level
that follows the plaza's place in the area), counts as a kill like a boss does and pays a vitamin or a PP Up the first time it is beaten.
They are scripted duels, not trainer objects, so they do not take part in the 500 mandatory kills (battle_budget.py counts them apart,
the cap is 650 battles in all).  The proposal and the rest of the 74 free slots: docs/SPECIAL_ENCOUNTERS.md."""
from .cameos import find, free_cells
from .layout import FACE
from .party import make_party
from .text import Text

AREA_OF = {"Tithe": "AREA1", "Grove": "AREA2", "Axiom": "AREA3", "Lotus": "AREA4", "Dis": "AREA5"}
REWARD = ["HP_UP", "PROTEIN", "IRON", "CALCIUM", "CARBOS", "PP_UP"]  # by plaza 1..6, in every area
ASK = "Fight {name}?"

# (plaza, name of at most 10 letters, class, sprite, face, [what he says before, when he falls, afterwards])
SPECIALS = {
    "Tithe": [
        (1, "FR GRIFT", "T_PRIEST", "PRIEST", "DOWN", ["Child, giving is voluntary. So is breathing. We are working on that.",
                                                       "A donation to the Almighty has been declined.", "Bless you. The blessing costs ten percent."]),
        (2, "SGT SLOW", "T_COP", "COP", "LEFT", ["I'm off duty. I'm also on duty. Both are for your protection.",
                                                 "Use of force. Noted. By me. As the witness.", "I didn't see anything. It's the job."]),
        (3, "BIG SAL", "T_THUG", "THUG", "RIGHT", ["I'm not in the mafia. I'm in the Kabbalah. Totally different bees.",
                                                   "We will discuss this in a hidden dimension.", "The bees are fine. Don't ask about the bees."]),
        (4, "MS LEDGER", "T_ACCOUNTANT", "SUIT_F", "DOWN", ["Your balance is zero. Your debt is also zero. So why are you here?",
                                                            "That was off the books. Everything is.", "I'll deduct this from your karma. It's the only account you have."]),
        (5, "DEAN DRIP", "T_BANKER", "SUIT", "LEFT", ["Interest is just love that compounds. Let me show you some affection.",
                                                      "A write-off. How romantic.", "Come back with collateral. Or a pulse."]),
        (6, "BRO HUSH", "T_DEACON", "CHOIR", "DOWN", ["Silence is golden. Silence is also billable.",
                                                      "Amen. That was loud for a prayer.", "Keep this quiet. Hush costs extra."]),
    ],
    "Grove": [
        (1, "AUNT KALE", "G_GRANNY", "ELDER_F", "DOWN", ["We share everything here. I'm sharing a beating.",
                                                         "Oh dear. Take the pantry key. Don't eat the ham.", "A fair fight is still a fight, dear."]),
        (2, "DRUM DAN", "G_DRUMMER", "HIPPIE_M", "RIGHT", ["I've been drumming for three days. This is my break.",
                                                           "My rhythm. Where is my rhythm?", "I'll go back to the drum. The drum doesn't hit back."]),
        (3, "SEER MOSS", "G_SHAMAN", "SHAMAN", "DOWN", ["The spirits say you carry a ledger. They also say you owe me.",
                                                        "The spirits are never wrong. They are sometimes late.", "Walk gently. Bring snacks. The forest likes both."]),
        (4, "NANA BIRD", "G_BIRDER", "BIRDER", "LEFT", ["I watch birds. Today I will watch you fall like one.",
                                                        "A rare species. Please don't land on my tent.", "I logged you. Species: trouble. Habitat: everywhere."]),
        (5, "FERN FRY", "G_FORAGER", "FORAGER", "DOWN", ["I only fight on an empty stomach. Yours.",
                                                         "Ow. That was a mushroom's worth of pain.", "Eat something. You look like a fighter."]),
        (6, "GRAN OAK", "G_ELDER", "ELDER_M", "RIGHT", ["I've seen four hundred winters. This one is harder.",
                                                        "Hm. A good one. The winter is yours.", "The young ones never ask. You asked with fists."]),
    ],
    "Axiom": [
        (1, "UNIT 7", "U_BOTCOP", "BOT_COP", "DOWN", ["Citizen. Compliance is mandatory. Fainting is optional.",
                                                      "Error 404: authority not found.", "Resume your day. Your day has been resumed."]),
        (2, "DR MADD", "U_MADDOC", "DOC_MAD", "LEFT", ["Hold still. This hurts me more than it hurts you. I enjoy that.",
                                                       "Fascinating. A control subject with opinions.", "Come back for a follow-up. Preferably in pieces."]),
        (3, "MATCH-9", "U_MATCHMAKER", "MATCHMAKER", "RIGHT", ["Genetic compatibility: 0.2. Let's fight and call it love.",
                                                               "Match failed. Please try again with someone approved.", "I wish you a legal partnership."]),
        (4, "AGENT ZED", "U_EXEC", "BOT_EXEC", "DOWN", ["Your file is closed. I will close you too.",
                                                        "Reopening your file. Please wait.", "Process complete. Your file is now longer."]),
        (5, "CASE 44", "U_CASEWORKER", "SERF_F", "LEFT", ["Your appeal has been denied. By force.",
                                                          "Appeal approved. Do not make it a habit.", "File under: resolved. Underline: for now."]),
        (6, "WARDEN-3", "U_WARDBOT", "BOT_WARDEN", "DOWN", ["Cell 14 is yours. The door is a courtesy.",
                                                            "Cell 14 is now empty. This is a clerical error.", "I'll keep the cell warm for next time."]),
    ],
    "Lotus": [
        (1, "MR SUNNY", "L_MANAGER", "RESORT_BOSS", "DOWN", ["Welcome! Smile! That's an order.",
                                                             "Oh. You're not smiling. I'm not smiling either. Delightful.", "Enjoy the rest of your stay. Indefinitely."]),
        (2, "DIVE DAVE", "L_LIFEGUARD", "LIFEGUARD", "LEFT", ["I'm here to save you. From what, I haven't decided.",
                                                              "I was saving my energy. Look where that got me.", "Safety is a mindset. Mine is on break."]),
        (3, "NURSE NIL", "L_CLINICIAN", "CLINICIAN", "RIGHT", ["I'm here to take your pain. Gently. And bill for it.",
                                                               "The pain is gone. So is your balance.", "Subscribe to forget. First month is free."]),
        (4, "LAZY LEO", "L_BEACHBUM", "BEACH_BUM", "DOWN", ["I'll fight you after my nap. Which is forever.",
                                                            "Ow. Okay. That's enough effort for the year.", "Wake me when something matters. Don't."]),
        (5, "MS MOJITO", "L_WAITER", "WAITER", "LEFT", ["Another round? Of fighting? It's on the house.",
                                                        "The house always wins. Except now.", "Tip appreciated. The tip is the fight."]),
        (6, "AMNESIA", "L_FORGOTTEN", "FORGOTTEN", "DOWN", ["Who are you? Who am I? Let's fight to find out.",
                                                            "I don't remember losing. So I didn't.", "Have we met? We should. Again."]),
    ],
    "Dis": [
        (1, "JUDGE HOLE", "D_JUDGE", "JUDGE", "DOWN", ["Order in the pit! Your verdict: guilty.",
                                                       "The court is adjourned. So are you.", "Appeals are heard on Judgment Day. Ask for the long line."]),
        (2, "MAG PYRE", "D_MAGISTRATE", "JUDGE", "LEFT", ["The court of Dis will now fry you.",
                                                          "Objection! Sustained. By you.", "Case dismissed. The dismissal is also on fire."]),
        (3, "HAG HEX", "D_HAG", "WITCH", "RIGHT", ["I grew old waiting for you. I can wait some more.",
                                                   "Child. You're not as dead as I'd hoped.", "I'll put the kettle on. For both of us."]),
        (4, "JEST ERR", "D_JESTER", "JESTER", "DOWN", ["Knock knock. Who's there? Your last moment.",
                                                       "The joke's on me. It's always on me.", "Come back for the encore. There's no exit."]),
        (5, "WARDEN KIM", "D_WARDEN", "WARDEN", "LEFT", ["Visiting hours are over. Forever.",
                                                         "Fine. Take the key. It opens nothing.", "Mind the doors. They also mind you."]),
        (6, "SPEC TER", "D_SPECTRE", "SHADE", "DOWN", ["I'm not dead. I'm just not here.",
                                                       "Boo. Seriously. That was the plan.", "I'll haunt you gently. It's the least I can do."]),
    ],
}


def add_area(w, g, tag, spec, roster, rng):
    """Place the six duelists of area `tag` into its plazas 1..6 (after the crowd and the cameos took theirs)."""
    for k, (plaza, name, cls, sprite, face, (seen, beaten, after)) in enumerate(SPECIALS[tag]):
        m = find(g, f"{tag}Plaza{plaza}")
        cells = free_cells(m)
        assert cells, f"{m.name}: no free cell for {name}"
        x, y = cells[-1 - 3]  # the cameos take from the very end, the named characters just before
        prog = (plaza - 0.5) / 7
        level = int(round(spec.l0 + (spec.l1 - spec.l0) * prog)) + 3
        party = make_party(roster, rng, level, min(6, 3 + plaza // 3), spec.theme)
        tid = w.trainer(cls, name, party)
        done = w.flag(f"EVENT_GEN_{m.const}_DUEL")
        paid = w.flag(f"EVENT_GEN_{m.const}_DUELPAID")
        label = f"{m.name}Duel"
        item = REWARD[plaza - 1]
        m.scripts.append(
            f"{label}:\n\tfaceplayer\n\topentext\n\tcheckevent {done}\n\tiftrue .Beaten\n\twritetext {label}SeenText\n\tyesorno\n\tiffalse .No\n"
            f"\tclosetext\n\twinlosstext {label}BeatenText, 0\n\tloadtrainer {cls}, {tid}\n\tstartbattle\n\treloadmapafterbattle\n"
            f"\tsetevent {done}\n\topentext\n"
            f".Beaten:\n\tcheckevent {paid}\n\tiftrue .After\n\twritetext {label}PayText\n\twaitbutton\n\tverbosegiveitem {item}\n\tiffalse .NoRoom\n"
            f"\tsetevent {paid}\n"
            f".After:\n\twritetext {label}AfterText\n\twaitbutton\n\tclosetext\n\tend\n\n"
            f".No:\n\twritetext {label}NoText\n\twaitbutton\n\tclosetext\n\tend\n\n"
            f".NoRoom:\n\twritetext {label}NoRoomText\n\twaitbutton\n\tclosetext\n\tend\n")
        m.scripts.append(Text(f"{name}: {seen} Fight?").emit(f"{label}SeenText"))
        m.scripts.append(Text(beaten).emit(f"{label}BeatenText"))
        m.scripts.append(Text("A prize for the winner. Keep it. I'd only lose it.").emit(f"{label}PayText"))
        m.scripts.append(Text(after).emit(f"{label}AfterText"))
        m.scripts.append(Text("Fine. Another day. I'll be here. I'm always here.").emit(f"{label}NoText"))
        m.scripts.append(Text("Your bag is full. The prize will wait. So will I.").emit(f"{label}NoRoomText"))
        m.obj(x, y, f"SPRITE_HC_{sprite}", FACE[face], label, pal="PAL_NPC_RED")


def add_all(w, roster, rng):
    from . import a1, a2, a3, a4, a5
    specs = {"Tithe": a1.Spec(), "Grove": a2.Spec(), "Axiom": a3.Spec(), "Lotus": a4.Spec(), "Dis": a5.Spec()}
    for tag, spec in specs.items():
        add_area(w, w.groups[AREA_OF[tag]], tag, spec, roster, rng)
