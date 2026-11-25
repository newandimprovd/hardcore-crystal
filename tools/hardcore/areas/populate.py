"""Places generated trainers into a map."""
import random

from .layout import FACE
from .party import NAMES, make_party, party_size
from .text import Text


class Deck:
    """The lines of one pool in shuffled order, one card per fighter.  When the deck runs out it is shuffled again, and the first cards of the new
    round are never among the last third of the old one, so a line is not heard twice within a long stretch of the road (alpha 3.3)."""

    def __init__(self, key, lines):
        self.R = random.Random("deck:" + key)
        self.lines = list(lines)
        self.cards, self.last = [], []

    def draw(self):
        if not self.cards:
            c = list(self.lines)
            self.R.shuffle(c)
            gap = set(self.last[-max(1, len(self.lines) // 3):])
            c = [x for x in c if x in gap] + [x for x in c if x not in gap]  # recently used ones go to the end (drawn last: cards pop from the end)
            c.reverse()
            self.cards = c
        t = self.cards.pop()
        self.last.append(t)
        return t


def deck(w, pool, kind):
    ds = w.__dict__.setdefault("decks", {})
    if (pool, kind) not in ds:
        ds[(pool, kind)] = Deck(f"{pool}:{kind}", w.pools[pool][kind])
    return ds[(pool, kind)]


def populate(w, m, slots, spec, rng, roster, prog0, prog1):
    """slots: list of layout.Slot. prog0..prog1 is this map's share of the area's progress (0..1)."""
    pool = spec.pool
    n = len(slots)
    m.scripts.append(
        f"{m.name}AfterText:\n\ttext_far HC_AfterText_{pool}\n\ttext_end\n\n"
        f"{m.name}AfterScript:\n\tendifjustbattled\n\topentext\n\twritetext {m.name}AfterText\n"
        f"\twaitbutton\n\tclosetext\n\tend\n")
    for i, s in enumerate(slots):
        prog = prog0 + (prog1 - prog0) * (i + 0.5) / n
        cls, sprite, pal = spec.pick_class(rng)
        level = int(round(spec.l0 + (spec.l1 - spec.l0) * prog))
        size = party_size(rng, min(1.0, spec.size_progress(prog)))
        party = make_party(roster, rng, level, size, spec.theme)
        name = rng.choice(NAMES)
        tid = w.trainer(cls, name, party)
        flag = w.flag(f"EVENT_GEN_{m.const}_{i}")
        label = f"{m.name}Trainer{i}"
        m.scripts.append(Text(deck(w, pool, "seen").draw()).emit(f"{label}SeenText"))
        m.scripts.append(Text(deck(w, pool, "beaten").draw()).emit(f"{label}BeatenText"))
        m.scripts.append(f"{label}:\n\ttrainer {cls}, {tid}, {flag}, {label}SeenText, {label}BeatenText, 0, {m.name}AfterScript\n")
        m.obj(s.x, s.y, sprite, FACE[s.face], label, pal=pal, otype="OBJECTTYPE_TRAINER", sight=s.sight)
    return n
