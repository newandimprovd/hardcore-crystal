"""Places generated trainers into a map."""
from .layout import FACE
from .party import NAMES, make_party, party_size


def populate(w, m, slots, spec, rng, roster, prog0, prog1):
    """slots: list of layout.Slot. prog0..prog1 is this map's share of the area's progress (0..1)."""
    pool = spec.pool
    n = len(slots)
    m.scripts.append(
        f"{m.name}SeenText:\n\ttext_far HC_SeenText_{pool}\n\ttext_end\n\n"
        f"{m.name}BeatenText:\n\ttext_far HC_BeatenText_{pool}\n\ttext_end\n\n"
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
        m.scripts.append(f"{label}:\n\ttrainer {cls}, {tid}, {flag}, {m.name}SeenText, {m.name}BeatenText, 0, {m.name}AfterScript\n")
        m.obj(s.x, s.y, sprite, FACE[s.face], label, pal=pal, otype="OBJECTTYPE_TRAINER", sight=s.sight)
    return n
