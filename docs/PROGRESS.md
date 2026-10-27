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
- [x] 5  area generator: engine support for generated trainers, 2848 event flags, generator package, Area 1 at full size
         (TITHE CITY: 204 trainers, 3 bosses, tree and boulder gates, Chainsaw and Crowbar pickups). Walk PASS, 0 problems.
- [x] 6  Areas 2-5 from the same generator: A2 the Commune (197 fights), A3 the Union (197), A4 the Lotus Coast (197, ends at the rival's
         mansion), A5 Dis/Cocytus/Judecca (196). 996 mandatory trainers, 236 maps, 5 map groups. Every area passes the full walk
         (WALK_GOD=1 for A3-A5, see below) and every boss-room-to-next-gate transition passes. Key items: A1 Chainsaw+Crowbar, A2 Jet Ski+
         Baseball Bat, A3 Flashlight+Sledgehammer, A4 Grapple Hook+Shovel, A5 Getaway Car; Outboard still TBD (plan: Purgatorio).
         Final boss FINNEGAN text is a placeholder until the ending is designed. Art is kit-based (johto/modern/kanto kits), palettes per area.
- [x] 7  milestones (200/800), rival crimelord, mansion hall and bedroom, Area 5 entered through the New Bark crater portal, normal ending
         (final boss falls -> crater rim -> Elm checks the fully evolved starter -> hall of fame + credits -> Continue in the bedroom).
         Tests: tools/hardcore/test_story.py milestone | newbark | rival | ending | notyet (see the docstring for the testbuild line of each).
         Still open from stage 7: credits text naming Claude, chauffeur trip and hall NPC checks, Getaway Car use, Elm hands the mon back
         instead of keeping it (design says "return it"; keeping it avoids losing a party member without a safe removal routine).
- [ ] 8  Purgatorio, Abyss, Nick's Landing, Steiner, Sabbah, Cioran, Crowley quest, Corkboard, true ending
- [ ] 9  wild encounters (every base form catchable), key item placement, QOL, balance
- [ ] 10 music loops, new sprites/cries, Pokedex text, credits, adults-only warning.
         Own sprites so far: CTHUSPAWN and CTHULUDON (tools/hardcore/sprites/cthu.py); the other 95 new species still borrow art.
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

## Stage 5 notes (area generator)
- Pipeline order: gen_moves.py, gen_roster.py, gen_roster_doc.py, gen_areas.py (all deterministic from base commit 3bc8daa).
- tools/hardcore/areas/: model.py (World, MapDef, warps), kits.py (tileset block kits), layout.py (lane, plaza, gatehouse, interiors),
  populate.py + party.py (trainer parties from the roster by level and theme), text.py (dialogue pools), emit.py (writes every table),
  a1.py (Area 1 spec and dialogue). gen_areas.py writes maps/gen/*, data/maps/area_*.asm, constants/area_*.asm and generated trainers.
- One-time patches to vanilla tables are marked `; HC-AREAS` (map constants, map lists, roofs, spawn points, landmarks, marts, outdoor sprites).
- Generated trainer IDs are >= 128 per class; HC_FindGenTrainer looks the record up in the "Gen Trainers N" banks. Event flags EVENT_GEN_* use the
  free flags 2048..2847 plus the holes below 2048.
- Lane design: a channel of trainers on both sides, each facing across the channel with a straight line of sight, so walking the lane forces every fight.
  Corpses (after the first kill) lie where the trainer stopped, next to the player, and do not block the channel.
- Warp rules the walker model relies on: door tiles (0x71 etc.) warp on arrival and step the player down; WARP_CARPET_* tiles warp when the player
  stands on them and walks in the carpet's direction (Pokecenter door mats); plain floor warp cells are arrival points only.
- Tests: test_walk.py ROM [goal,...] (ROM from testbuild.sh cg1 TEST_MAP=CHERRYGROVE_CITY TEST_X=17 TEST_Y=8 TEST_MON=CTHULUDON TEST_LEVEL=60
  TEST_REVEALED=1 TEST_ITEMS=1), test_whiteout.py ROM. areamodel.py is the static map model they plan on.

## Sprite notes
- Species with own art: roster_data.N(..., art="cthu", pal=(body, accent), shiny=(body, accent)). gen_roster.py runs tools/hardcore/sprites/<art>.py to
  write gfx/pokemon/<slug>/front.png (4 stacked animation frames), back.png, shiny.pal and copies the anim scripts of TENTACRUEL, then emits
  gfx/pokemon/hc_pics.asm (in "Pics 20", the first unused pic bank), hc_anims.asm and hc_frames.asm. Palettes come from the PNGs like a vanilla species.
- GBC limit: four colours per sprite (white, body, accent, black). A 7x7 front pic may use at most about 98 tiles after animation (vanilla maximum);
  keep animation frames to a few changed tiles (cthu.py animates only the tentacles and the gem glint).

## Stage 5c/6 notes (full areas)
- Pipeline for an area: areas/aN.py (Spec = classes, sprites, type theme, level range; build() returns (group, last boss exits)) built on
  areas/builder.py: BossSpec, ActSpec, build_act, start_plaza (rift plaza + gatehouse), AreaCfg + build_area (A3-A5 use this, A2 too).
  areas/specbase.py holds the shared Spec base class. Text lives in areas/aN_text.py (SEEN/BEATEN/AFTER pools, CENTER/MART/HOUSE/GATE, boss text).
  gen_areas.py chains the areas: each area's entry is the previous area's last boss room exits (open_exit=True on the last boss that has a next area).
- Act layout: start plaza, then three acts of 5 street lanes (13 trainers each) with a split plaza 3/2/3, ending in a plaza with the boss door.
  Act 2 and 3 begin with a key-item gate (areas/layout.py GATES: tree/CHAINSAW, boulder/CROWBAR, river/JET_SKI, hive/BASEBALL_BAT, dark/FLASHLIGHT,
  slab/SLEDGEHAMMER, hook/GRAPPLE_HOOK, rubble/SHOVEL). The boss of the previous act holds the item ball.
- Limits to keep: boss names at most 10 characters, at most 15 objects per map, trainer IDs under 128 per class, ROMX bank $75 holds Events.
  ROM: ~330 KB ROMX free after five areas (per area ~22 KB).
- Walker (tools/hardcore/test_walk.py): `auto:FirstMap` plans an area from its first plaza (heal at each Pokecenter, item pickups, gates).
  Build with testbuild.sh NAME TEST_MAP=AXIOM_PLAZA1 TEST_X=3 TEST_Y=4 TEST_MON=CTHULUDON TEST_LEVEL=100 TEST_REVEALED=1 TEST_ITEMS=0.
  WALK_GOD=1 gives the lone test mon 999 HP and clears enemy Destiny Bond (a level-100 Cthuludon has 358 HP and the later areas one-shot it
  or take it down with Destiny Bond; those whiteouts are balance, not map bugs). Transition goals: `GroveCouncil,AxiomGate,AxiomPlaza1` etc.
- Balance notes seen in the walk: enemies at L85-92 with 120-power STAB moves can one-shot a 358 HP mon; Destiny Bond exists on APPARITION and MIASMA lines.

## Stage 7 notes (story and ending)
- Story hook: TrainerDeathScript -> HC_CheckStory (engine/hardcore/story.asm, section "Hardcore Story") -> farsjump HC_StoryDispatch.
  Kind 1 = kill 200 (tidal wave news), 2 = the rival (class RIVAL2, boss 3 of Area 4: stolen starter back at L75, EVENT_HC_CRATER),
  3 = the final boss FINNEGAN (EVENT_HC_FINN_FELL, warp to NEW_BARK_TOWN 10,10, the crater rim). Story texts: tools/hardcore/gen_story.py STORY.
- New Bark Town (maps/NewBarkTown.asm): tiles callback floods (kill 200) or craters (kill 800) the town, swirl block at block (5,4) leads to DIS_GATE;
  object visibility goes through event flags: teacher/fisher carry EVENT_HC_CRATER, Elm carries EVENT_HC_ELM_HIDDEN (callback appears him with the crater).
  A flagless `disappear` in a MAPCALLBACK_OBJECTS callback does NOT hide an object (the callback runs before the object structs exist).
- Ending: Elm checks `special FindPartyMonThatSpecies` (wScriptVar = species in, TRUE/FALSE out) for ELDERWOOD / CALDERA / DEATHROLL depending on
  the starter the rival had (player took TOTODILE -> CHIKORITA line, CHIKORITA -> CYNDAQUIL line, CYNDAQUIL -> TOTODILE line), sets EVENT_HC_ENDED and
  runs `halloffame` (saves, hall of fame, vanilla credits, reset). `.SpawnAfterE4` in intro_menu.asm spawns at SPAWN_LOTUS_BEDROOM (generated in a4.py mansion()).
- Test pitfall: after a script ends, another A press talks to the NPC again; stop mashing A when wScriptRunning is 0.

## Stage 8 notes (art pass: original graphics) - IN PROGRESS
Goal: stop reusing vanilla graphics that clash with the dark-comedy vibe. Pilot: Area 1 (Tithe City); the same kit goes to Areas 2-5.
- Pipeline order is now: gen_moves, gen_roster, gen_roster_doc, **gen_tilesets**, gen_areas (gen_tilesets writes the tileset png/metatiles/collision/palette map
  and gfx/area_tilesets.asm; gen_areas autotiles the maps with the new blocks).
- tools/hardcore/art/: tilebuild.py (Canvas 32x32 block painter + Tileset.pack: dedups tiles, assigns ids 0x00-0x5f / 0x80-0xdf, writes png, metatiles, collision,
  palette map), paint.py (brick, slabs, windows...), tithe.py (the Tithe tileset: gothic windows, neon POKE/MART signs, slate roofs, cobbles, plaza coins, rift portal),
  areapal.py (3 palette sets per area: out / road / inn), register.py (one-time `; HC-ART` patches), render.py (static renderer), gameshots.py (in-game screenshots).
- Palette hook: LoadMapPals -> HC_LoadAreaPalette (engine/hardcore/area_pals.asm) picks the set by wMapTileset >= TILESET_TITHE and wEnvironment. Custom outdoor
  palettes share index 0 (base color) across slots; index 3 is the shared outline. A tile has one palette slot, so one 8x8 cell can use only one slot's colors.
- **Engine quirk: LoadMetatiles draws block id 0 as the map's border block.** Block 0 of every custom tileset must therefore be the border itself (Tileset.pack asserts it)
  and maps use border block 0. (Symptom was a dark brick rectangle wherever the generator placed block 0 as a plain floor.)
- Tileset autotile roles (AUTO in tithe.py): facade/side_e/side_w/roof/mass (+ rare variants); layout.autotile runs in lane()/plaza() of areas/layout.py.
- TitheRoad stays TILESET_JOHTO (it connects to vanilla Cherrygrove, connected maps must share the tileset) and gets the road palette.
- Still to do in this stage: tilesets for Areas 2-5 (Grove, Axiom, Lotus, Dis/Cocytus), original NPC overworld sprites and area-specific trainer classes,
  original sprites for the new Pokemon (tinted vanilla art for now), interior art, wild-grass patches.
