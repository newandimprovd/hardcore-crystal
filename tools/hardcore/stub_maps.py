#!/usr/bin/env python3
"""ROM diet: replace every vanilla map nobody can reach with an empty stub.

The hardcore world only uses New Bark Town, Route 29, Cherrygrove and the generated areas (maps/gen/). The rest of
Crystal's maps are still in the group tables (so every map constant stays valid) but nothing leads to them, so their
scripts and texts are dead weight.  A stub keeps the two labels the map tables expect and nothing else.
Safe to run any number of times.  The original files stay in git history (base commit 3bc8daa)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

KEEP = {
    "NewBarkTown", "PlayersHouse1F", "PlayersHouse2F", "PlayersNeighborsHouse", "ElmsHouse", "ElmsLab",
    "Route29", "CherrygroveCity", "CherrygroveMart", "CherrygrovePokecenter1F", "CherrygroveGymSpeechHouse",
    "CherrygroveEvolutionSpeechHouse", "GuideGentsHouse",
}
# maps whose scripts other code still jumps into; add names here when the linker reports missing labels
KEEP |= set((ROOT / "tools/hardcore/stub_keep.txt").read_text().split()) if (ROOT / "tools/hardcore/stub_keep.txt").exists() else set()

STUB = """{n}_MapScripts:
	def_scene_scripts

	def_callbacks

{n}_MapEvents:
	db 0, 0 ; filler

	def_warp_events

	def_coord_events

	def_bg_events

	def_object_events
"""


def main():
    done = kept = saved = 0
    for p in sorted((ROOT / "maps").glob("*.asm")):
        n = p.stem
        if n in KEEP:
            kept += 1
            continue
        new = STUB.format(n=n)
        old = p.read_text()
        if old != new:
            saved += len(old) - len(new)
            p.write_text(new)
        done += 1
    print(f"stubbed {done} maps, kept {kept}, source bytes removed this run {saved}")


if __name__ == "__main__":
    main()
