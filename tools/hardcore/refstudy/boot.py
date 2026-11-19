import sys, os
from pyboy import PyBoy
ROMS = {
 "c16": "/home/claude/pokecrystal/crystal16-bit.gbc",
 "grandia": "/home/claude/pokecrystal/Grandia - Parallel Trippers (Japan) [T-En by Adventurous Translations v1.03].gbc",
 "van": "/home/claude/pokecrystal/Pokemon - Crystal Version (USA, Europe) (Rev 1).gbc",
}
def boot(key):
    pb = PyBoy(ROMS[key], window="null", sound_emulated=False)
    pb.set_emulation_speed(0)
    return pb
def press(pb, key, hold=6, wait=12):
    pb.button(key, hold); pb.tick(hold + wait, False)
def shot(pb, path, scale=2):
    pb.tick(1, True)
    im = pb.screen.image.convert("RGB")
    if scale != 1: im = im.resize((im.width*scale, im.height*scale))
    im.save(path)
