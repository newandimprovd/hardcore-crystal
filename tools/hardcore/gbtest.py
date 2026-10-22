"""PyBoy helpers for the Crystal hack. WRAMX bank switching is the classic pitfall:
reading 0xD000-0xDFFF while the game has another SVBK bank mapped returns garbage, so
memory reads go through pb.memory[bank, addr] with the bank taken from the symbol file."""
import re, sys, faulthandler
from pyboy import PyBoy

class T:
    def __init__(self, rom, sym=None, window="null", speed=0):
        self.pb = PyBoy(rom, window=window, sound_emulated=False)
        self.pb.set_emulation_speed(speed)
        self.sym = {}
        self.syms = {}
        sym = sym or rom.replace(".gbc", ".sym")
        for line in open(sym):
            m = re.match(r"([0-9a-f]{2}):([0-9a-f]{4}) (\S+)", line)
            if m:
                b, a, n = int(m[1], 16), int(m[2], 16), m[3]
                self.sym[n] = (b, a)
                self.syms.setdefault((b, a), n)

    def tick(self, n=1):
        self.pb.tick(n, False)

    def addr(self, name):
        return self.sym[name][1]

    def mem(self, name, off=0, n=1):
        b, a = self.sym[name]
        a += off
        out = []
        for i in range(n):
            if 0xD000 <= a + i < 0xE000:
                out.append(self.pb.memory[max(b, 1), a + i])
            else:
                out.append(self.pb.memory[a + i])
        return out[0] if n == 1 else out

    def poke(self, name, val, off=0):
        b, a = self.sym[name]
        a += off
        if 0xD000 <= a < 0xE000:
            self.pb.memory[max(b, 1), a] = val
        else:
            self.pb.memory[a] = val

    def press(self, btn, hold=4, wait=12):
        self.pb.button(btn, hold)
        self.tick(hold + wait)

    def where(self):
        return self.mem("wMapGroup"), self.mem("wMapNumber"), self.mem("wXCoord"), self.mem("wYCoord")

    def shot(self, path, scale=1):
        self.pb.tick(1, True)  # screen buffer is only filled on a rendered frame
        im = self.pb.screen.image.convert("RGB")
        if scale != 1:
            im = im.resize((im.width * scale, im.height * scale))
        im.save(path)

    def hook(self, label, fn):
        b, a = self.sym[label]
        self.pb.hook_register(0 if a < 0x4000 else b, a, fn, None)

    def stop(self):
        self.pb.stop(save=False)

def boot_to_overworld(t, max_frames=6000):
    """Skip intro/new game screens until a map is loaded. Mash A/Start."""
    faulthandler.dump_traceback_later(300, exit=True)
    for i in range(max_frames // 20):
        t.pb.button("a", 4)
        t.tick(20)
        if t.mem("wMapGroup") and t.mem("wMapNumber") and t.mem("wPlayerState") is not None and i > 20:
            pass
    return t.where()
