Reference ROM study tools (alpha 3.1 to 3.2 study pass).

- `boot.py`: opens a ROM in PyBoy headless (`boot("c16" | "grandia" | "van")`), `press`, `shot`.
- `drive.py`: key sequences, save states, `sheet` (contact sheets), `pos` (player map/x/y, valid for crystal16-bit only: wMapGroup at $dc64 in bank 1).
- `tilestats.py`: `analyze(pb)` reads the visible background (map, attributes, both VRAM banks) and returns unique tiles,
  unique pixel tiles after flip folding, unique 2x2 groups, palettes used, flipped cells, sprite count and colours on screen.

The scripts keep the reference ROM paths of the session that made them. Change `ROMS` in `boot.py` for another checkout.
Findings and ideas are in `docs/REFERENCE_STUDY.md`.

Battle engine study (see `docs/BATTLE_ENGINE_STUDY.md`)
- `aimeasure.py ROM`: plays the rival fight of a test ROM (build it with `testbuild.sh aim TEST_MAP=TITHE_JUNCTION TEST_X=19 TEST_Y=20 TEST_MON=CTHULUDON TEST_LEVEL=14 TEST_REVEALED=1`)
  and measures how many cycles `AIChooseMove` and `AIDamageCalc` take. The clock is completed frames times 70224 plus the scanline counter LY times 456, so the resolution is about 456 cycles.
  The game's own VBlank counter (`hVBlankCounter`) is read next to it as an independent cross-check.

Grandia room, map and movement study (see `docs/GRANDIA_ENGINE_STUDY.md`)
- `grandia_rooms.py`: `rec(n)` reads room record n (900 bytes: tiles, attributes, collision words), `room_index_from_buffer(m)` identifies the live room, `show_col(n)` prints its collision grid.
- `grandia_stats.py`: ROM-wide statistics over all 556 room records, no save state needed (`python3 grandia_stats.py` from this folder).
- `grandia_crawl.py N`: automatic crawler that walks the hero to open edges and records which room appears. Needs `gr_s4.state` (restaurant, after the intro) in the working directory. Save states are not committed.
- `grandia_collision.py`: writes a collision word into the live grid (WRAM bank 1 `$D082`) and tests walking into the cell from each side.
- `gbdis.py`: small Game Boy CPU disassembler (`show(rom, file_offset, length)`).

Grandia world database, palettes and tiles (see `docs/GRANDIA_ENGINE_STUDY.md`, section 9). These read only the ROM and need no save state.
- `grandia_db.py`: class `Grandia(rom_path)` with `palette_set(area)`, `areas`, `room(area, n)`, `tileset(id)` and `render(area, n)`. Command line: `grandia_db.py ROM AREA ROOM out.png`.
- `grandia_areas.py ROM [--json out.json]`: decodes the 48 areas and 572 room records in bank `$83` and checks that each record belongs to exactly one area.
- `grandia_palettes.py ROM OUTDIR [--crystal gfx/tilesets/bg_tiles.pal]`: draws the 48 palette sets and prints hue and saturation statistics, with Crystal's tileset palettes for comparison.
- `grandia_atlas.py ROM OUTDIR [--tilesets gfx/tilesets]`: one picture with a representative room per area and a statistics table. Pictures show the original game's art, so keep them out of the repo.
- `explore/`: the scratch tools for walking the school block of the opening (`gnav.goto2`, pit aware planning in `gcrawl3`, `gsweep2.live_grid`, `gexplore.clear_dialogue`). They import each other and `drive.py`, take their save states from `crawl/` and `gr_s4.state` in the working directory, and are kept as a record of how the study went, not as a polished tool.
