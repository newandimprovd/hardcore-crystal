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
- [ ] 2  type chart with Fairy (tools/hardcore/gen_types.py written, not yet built/tested), move categories, Showdown moves
- [ ] 3  first kill reveal, kill counters, trainer tips
- [ ] 4  roster: 62 four-stage lines, 248 species, Fairy/Poison spread
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
