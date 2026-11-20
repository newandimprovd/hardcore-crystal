#!/usr/bin/env python3
"""Decode Grandia's two-level room database (bank $83) and map every room record to its area.

Usage: grandia_areas.py GRANDIA.gbc [--json OUT.json]

Layout, as read from the loader at bank 00:$1622 and confirmed against the ROM:
  * Bank $83 at $4000 holds 48 three-byte area entries: (tileset id, pointer to the room list).
    The loader keeps this table pointer in WRAM at $D3C6 (bank) and $D3C7/$D3C8 (address).
  * Each room list is a run of three-byte entries (bank, address low, address high), one per
    room in the area, so the number of rooms in an area is the pointer gap divided by three.
  * Area id is stored in WRAM $D014, room number inside the area in $D015.
  * The area id doubles as the palette set id: bank $82 has 48 pointers at $4000, each to
    five BG palettes (see grandia_palettes.py).
  * A room record is 900 bytes: 360 tile ids, 360 attributes, 180 collision bytes.
"""
import json, struct, sys

REC = 900


def main():
    rom = open(sys.argv[1], "rb").read()
    base = 0x83 * 0x4000
    areas = []
    for i in range(48):
        tile, ptr = rom[base + 3 * i], struct.unpack_from("<H", rom, base + 3 * i + 1)[0]
        areas.append((tile, ptr))
    ends = [p for _, p in areas[1:]] + [areas[-1][1] + 3 * 0]
    out = []
    total = 0
    claimed = {}
    for i, (tile, ptr) in enumerate(areas):
        # the next area's pointer bounds this one, the last area runs to the first record pointer gap
        nxt = areas[i + 1][1] if i + 1 < 48 else None
        rooms = []
        a = ptr
        while True:
            if nxt is not None and a >= nxt:
                break
            off = base + (a - 0x4000)
            bank, lo, hi = rom[off], rom[off + 1], rom[off + 2]
            addr = lo | (hi << 8)
            if not (0x83 <= bank <= 0xA2 and 0x4000 <= addr <= 0x8000 - REC):
                break
            # records in banks $84.. sit on a 900-byte grid from $4000, the ones in bank $83 do not
            g = (bank - 0x84) * 18 + (addr - 0x4000) // REC if bank >= 0x84 else (bank << 16) | addr
            rooms.append(g)
            a += 3
        for g in rooms:
            claimed.setdefault(g, []).append(i)
        out.append({"area": i, "tileset": tile, "list_ptr": ptr, "rooms": rooms})
        total += len(rooms)
    print("areas", len(out), "room entries", total, "distinct rooms", len(claimed))
    dup = {g: a for g, a in claimed.items() if len(a) > 1}
    print("rooms listed by more than one area:", len(dup))
    for o in out:
        r = o["rooms"]
        r2 = [g for g in r if g < 0x10000]
        rng = f"{min(r2)}..{max(r2)}" if r2 else "-"
        print(f"area {o['area']:2d} tileset {o['tileset']:2d} rooms {len(r):3d} global {rng}")
    inb83 = sorted(g for g in claimed if g >= 0x10000)
    print("records inside bank $83:", len(inb83), [f"{g>>16:02X}:{g&0xFFFF:04X}" for g in inb83])
    missing = [g for g in range(556) if g not in claimed]
    print("records not listed by any area:", len(missing), missing[:40])
    if "--json" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"))


if __name__ == "__main__":
    main()
