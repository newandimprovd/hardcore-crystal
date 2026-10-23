# Progress log (read this first after any reset or context loss)

Goal: a complete, ready-to-run Hardcore Crystal .gbc (2 MB MBC3), built as clean source edits on pret/pokecrystal
at base commit 3bc8daa with RGBDS 1.0.4. Design: docs/Hardcore_Crystal_complete_idea.md (also in the repo root of
newandimprovd/hardcore-crystal under docs/). Standing rules are in that document, section "Standing rules".

## How the work is saved
- Working tree: /home/claude/pokecrystal (branch hardcore-crystal, no remote on purpose, never push to pret).
- Backup: tools/hardcore/backup.sh "message" [rom] snapshots the tree into /home/claude/hardcore-crystal and pushes
  branch claude/work to https://github.com/newandimprovd/hardcore-crystal . Run it after every meaningful step.
- Toolchain: RGBDS 1.0.4 is built from source (gbdev/rgbds tag v1.0.4, cmake) and copied to /home/claude/bin.
  PyBoy 2.x via pip. Showdown data via npm package @pkmn/dex (dump to tools/hardcore/showdown_moves.json).
- Test builds: tools/hardcore/testbuild.sh NAME [TEST_MAP=.. TEST_X=.. TEST_Y=.. TEST_MON=.. TEST_LEVEL=..].
  Emulator helpers: tools/hardcore/gbtest.py.

## Stage status
- [x] 1  key items, trainer death, corpses (restored from the surviving patch)
- [x] 1b test harness (testbuild.sh, gbtest.py, test-mode intro bypass)
- [x] 2  type chart with Fairy (typecheck.py PASS), 39 Showdown move replacements (gen_moves.py), per-move physical/special split
         (home/hardcore.asm GetMoveCategory; tools/hardcore/test_split.py: 104 side/move pairs, 59 of 60 moves seen, 0 mismatches)
- [x] 3  first kill reveal, kill counters (tools/hardcore/test_reveal.py PASS). Trainer tips still to write along the path to Area 2 (type chart pages, split)
- [x] 4  roster: 62 four-stage lines, 248 species (97 new), Fairy 24 / Poison 31. Built and checked in the emulator
         (test_roster.py 0 failures, dex list and entries, party stats screen, wild battle with a new species). Placeholder art:
         new species reuse source sprites with tinted palettes; real sprites and cries are stage 10. Full table in docs/ROSTER.md
- [ ] 5  area generator (Area 1), forced fights, plazas, respawn
- [ ] 6  Areas 2-4
- [ ] 7  milestones (200/800), rival crimelord, mansion bedroom ending, Area 5
- [ ] 8  Purgatorio, Abyss, Nick's Landing, Steiner, Sabbah, Cioran, Crowley quest, Corkboard, true ending
- [ ] 9  wild encounters (every base form catchable), key item placement, QOL, balance
- [ ] 10 music loops, new sprites/cries, Pokedex text, credits, adults-only warning
- [ ] 11 final ROM

## Notes for the next session
- Move category design: per-move bitset looked up by move ID; call sites that did `cp SPECIAL` on the move type byte
  (effect_commands.asm x4, counter.asm, mirror_coat.asm, ai/scoring.asm) are redirected through a helper that returns
  0 (physical) or SPECIAL (special) so the existing carry logic is unchanged.
- Normal/Bug immunity wording was ambiguous; reading used is in tools/hardcore/gen_types.py.

## Stage 2 notes
- Move IDs are unchanged; 39 vanilla slots were renamed in place. Retired moves in learnsets/trainers/eggs map to survivors (REMAP in gen_moves.py).
- Category lookup: MoveCategoryBits (32 bytes, ROM0 gap at $0063) read by GetMoveCategory; call sites in effect_commands.asm,
  counter.asm, mirror_coat.asm and ai/scoring.asm use the move ID in the move struct (animation byte == move ID).
- Moonblast uses Showdown's 30% Special Attack drop (the earlier build used Special Defense).
- PyBoy note: poking register_file to call routines is unreliable; test through real battles with hook_register instead.

## Stage 4 notes (roster)
- Regenerate everything: python3 tools/hardcore/gen_moves.py && python3 tools/hardcore/gen_roster.py && python3 tools/hardcore/gen_roster_doc.py
  (generators read the vanilla data with git show from base commit 3bc8daa, so they are deterministic).
- Roster rules: 62 lines x 4 stages, evolve at 25/50/75, no branching, no legendaries, every base form catchable. Data: tools/hardcore/roster/roster_data.py.
- New species fill the IDs freed by removed vanilla species (all <= 248). Removed names stay as aliases (DEF NAME EQU SURVIVOR);
  names the engine special-cases (UNOWN, DITTO, FARFETCH_D, MEW, MEWTWO, LUGIA, HO_OH, CELEBI, TOGEPI, SHUCKLE) are parked at $fe.
- JOHTO_POKEMON=152 used to pick the sprite bank; engine/gfx/pic_animation.asm now reads a per-species FramesBanks table instead.
- Pokedex flag arrays stay 32 bytes (flag_array 251). EvosAttacks must fit one bank, so new species keep only earlier moves of level 20+.
- Pokedex text is 18 columns, two pages of three lines. Dex weights are 16-bit (max 6553.5 lb). Species names max 10 characters.
- Tests: test_roster.py ROM (static table check), dexshots.py ROM OUTDIR NAME... (dex screenshots), typecheck.py, test_reveal.py, test_split.py.
- Known polish items: dex "No." shows species ID not line order; unused gfx of removed species still in ROM (prune later if space is needed).
