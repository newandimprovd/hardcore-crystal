"""Little helpers for the named characters: a talker that sets a lore flag, a sign, a floor ball, placed on any map."""
from .flags import flag_once
from .layout import FACE
from .text import Text


def lore_npc(w, m, x, y, sprite, pal, face, label, first, again=None, flag=None, hide_flag=None, move=None):
    """An NPC that says `first` (and sets event `flag`, the corkboard page); `again` replaces the speech afterwards."""
    s = [f"{label}:", "\tfaceplayer", "\topentext"]
    if flag:
        flag_once(w, flag)
        s += [f"\tcheckevent {flag}", "\tiftrue .Again"]
    s += [f"\twritetext {label}Text", "\twaitbutton"]
    if flag:
        s += [f"\tsetevent {flag}"]
    s += ["\tclosetext", "\tend"]
    if flag:
        s += ["", ".Again:", f"\twritetext {label}AgainText", "\twaitbutton", "\tclosetext", "\tend"]
    m.scripts.append("\n".join(s) + "\n")
    m.scripts.append(Text(first).emit(f"{label}Text"))
    if flag:
        m.scripts.append(Text(again or first).emit(f"{label}AgainText"))
    return m.obj(x, y, sprite, move or FACE[face], label, pal=pal, flag=hide_flag or "-1")


def plain_npc(m, x, y, sprite, pal, face, label, text, move=None):
    m.scripts.append(f"{label}:\n\tjumptextfaceplayer {label}Text\n")
    m.scripts.append(Text(text).emit(f"{label}Text"))
    return m.obj(x, y, sprite, move or FACE[face], label, pal=pal)


def sign(m, x, y, label, text, flag=None, w=None):
    """A bg_event read (the tile may be wall or floor)."""
    if flag:
        flag_once(w, flag)
        m.scripts.append(f"{label}:\n\topentext\n\twritetext {label}Text\n\twaitbutton\n\tsetevent {flag}\n\tclosetext\n\tend\n")
    else:
        m.scripts.append(f"{label}:\n\tjumptext {label}Text\n")
    m.scripts.append(Text(text).emit(f"{label}Text"))
    m.bg(x, y, "BGEVENT_READ", label)


def ball(w, m, x, y, item, name):
    flag = w.flag(f"EVENT_GEN_{m.const}_{name}")
    m.scripts.append(f"{m.name}{name}:\n\titemball {item}\n")
    return m.obj(x, y, "SPRITE_POKE_BALL", "SPRITEMOVEDATA_STILL", f"{m.name}{name}", otype="OBJECTTYPE_ITEMBALL", flag=flag)
