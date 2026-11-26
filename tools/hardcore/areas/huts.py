"""The huts of alpha 3.3: a house in a glade of a street (areas/trail.py glade kind "hut"), with a small room behind its door and one person in it who
hands over an item the first time and talks afterwards.  Built like a house interior (areas/layout.py) so the room is the same House1 map."""
from .layout import FACE, MapDef, blk, hub
from .text import Text


def hut_interior(g, w, name, outer_warp, landmark, sprite_pal, speech, after, item, music="MUSIC_VIOLET_CITY"):
    m = MapDef(g.key, name, 4, 4, "TILESET_HOUSE", "INDOOR", landmark, music, pal="PALETTE_DAY")
    m.blocks = bytearray(blk("maps/House1.blk"))
    w1, w2 = m.warp(2, 7), m.warp(3, 7)
    outer_warp.dest = w1
    w1.dest = outer_warp
    w2.dest = outer_warp
    m.object_consts = ["NPC0"]
    label = f"{name}Dweller"
    flag = w.flag(f"EVENT_GEN_{m.const}_HGIFT")
    m.scripts.append(
        f"{label}:\n\tfaceplayer\n\topentext\n\tcheckevent {flag}\n\tiftrue .Done\n\twritetext {label}Text\n\twaitbutton\n"
        f"\tverbosegiveitem {item}\n\tiffalse .NoRoom\n\tsetevent {flag}\n"
        f".Done:\n\twritetext {label}AfterText\n\twaitbutton\n\tclosetext\n\tend\n\n"
        f".NoRoom:\n\twritetext {label}NoRoomText\n\twaitbutton\n\tclosetext\n\tend\n")
    m.scripts.append(Text(speech).emit(f"{label}Text"))
    m.scripts.append(Text(after).emit(f"{label}AfterText"))
    m.scripts.append(Text("Your bag is full. Come back with a free hand. I'll be here. I'm always here.").emit(f"{label}NoRoomText"))
    sp, pal = sprite_pal
    m.obj(2, 3, sp, FACE["DOWN"], label, pal=pal)
    g.add(m)
    return m
