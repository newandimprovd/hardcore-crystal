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
- [x] 7  milestones (tidal wave news at kill 400, crater with the rival's fall), rival crimelord, mansion hall and bedroom, Area 5 entered through the New Bark crater portal, normal ending
         (final boss falls -> crater rim -> Elm checks the fully evolved starter -> hall of fame + credits -> Continue in the bedroom).
         Tests: tools/hardcore/test_story.py milestone | newbark | rival | ending | notyet (see the docstring for the testbuild line of each).
         Still open from stage 7: credits text naming Claude, chauffeur trip and hall NPC checks, Getaway Car use, Elm hands the mon back
         instead of keeping it (design says "return it"; keeping it avoids losing a party member without a safe removal routine).
- [~] 8  art pass DONE (original tilesets for all 5 areas, 62 original NPC sprites with per-area colorways, 85 original trainer classes with
         portraits, see Stage 8 notes). Still open: Purgatorio, Abyss, Nick's Landing, Steiner, Sabbah, Cioran, Crowley quest, Corkboard, true ending
- [~] 9  wild encounters DONE (tall grass in all 35 plazas, every base form catchable, checker + in-game test, see Stage 9 notes);
         still open: key item placement (Outboard), QOL, balance
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
  Kind 1 = the kill counter has reached HC_TSUNAMI_KILLS = 400 and the news has not run (tidal wave news, flag based), 2 = the rival (class RIVAL2, boss 3 of Area 4: stolen starter back at L75, EVENT_HC_CRATER),
  3 = the final boss FINNEGAN (EVENT_HC_FINN_FELL, warp to NEW_BARK_TOWN 10,10, the crater rim). Story texts: tools/hardcore/gen_story.py STORY.
- New Bark Town (maps/NewBarkTown.asm): tiles callback floods (tidal wave, kill 400) or craters (the rival's fall) the town, swirl block at block (5,4) leads to DIS_GATE;
  object visibility goes through event flags: teacher/fisher carry EVENT_HC_CRATER, Elm carries EVENT_HC_ELM_HIDDEN (callback appears him with the crater).
  A flagless `disappear` in a MAPCALLBACK_OBJECTS callback does NOT hide an object (the callback runs before the object structs exist).
- Ending: Elm checks `special FindPartyMonThatSpecies` (wScriptVar = species in, TRUE/FALSE out) for ELDERWOOD / CALDERA / DEATHROLL depending on
  the starter the rival had (player took TOTODILE -> CHIKORITA line, CHIKORITA -> CYNDAQUIL line, CYNDAQUIL -> TOTODILE line), sets EVENT_HC_ENDED and
  runs `halloffame` (saves, hall of fame, vanilla credits, reset). `.SpawnAfterE4` in intro_menu.asm spawns at SPAWN_LOTUS_BEDROOM (generated in a4.py mansion()).
- Test pitfall: after a script ends, another A press talks to the NPC again; stop mashing A when wScriptRunning is 0.

## Stage 8 notes (art pass: original graphics) - DONE except interiors and Pokemon sprites
Goal: stop reusing vanilla graphics that clash with the dark-comedy vibe.
- Pipeline order (rerun in this order, each step is idempotent): gen_moves, gen_roster, gen_roster_doc, **gen_tilesets**, **gen_sprites**, **gen_classes**,
  gen_areas. gen_tilesets writes tileset png/metatiles/collision/palette map; gen_sprites the NPC sheets; gen_classes the trainer classes; gen_areas the maps.
- tools/hardcore/art/: tilebuild.py (Canvas 32x32 block painter + Tileset.pack: dedups tiles, assigns ids 0x00-0x5f bank 0 / 0x80-0xdf bank 1, writes png, metatiles,
  collision, palette map), paint.py, common.py (build_set: the block order shared by Grove/Axiom/Lotus/Dis), tithe.py grove.py axiom.py lotus.py disart.py (one
  tileset per area), grass.py (tall grass), areapal.py (palette sets per area: out / road / inn, plus the NPC colorways), npcs.py + cast.py (62 characters, recipe based),
  classes.py (85 trainer classes), portraits.py (56x56 battle portrait made from the front sprite), register.py, render.py, gameshots.py.
- Palette hooks (engine/hardcore/area_pals.asm): LoadMapPals -> HC_LoadAreaPalette (BG, 3 sets per area by wEnvironment) and HC_LoadAreaObjPalette (OBJ: slot 0 red is
  the player and stays vanilla; the other slots are per-area BLUE/GREEN/BROWN/PINK, always day colors). Custom outdoor palettes share index 0 (base) across slots,
  index 3 is the outline. A tile has one palette slot, so one 8x8 cell can use only one slot's colors.
- **Engine quirk: LoadMetatiles draws block id 0 as the map's border block.** Block 0 of every custom tileset is the border (Tileset.pack asserts it).
- Autotile roles: facade/side_e/side_w/roof/mass (+ rare variants); layout.autotile runs in lane() and plaza().
- TitheRoad stays TILESET_JOHTO (connects to vanilla Cherrygrove, connected maps must share the tileset) and gets the road palette.
- NPC sprites: 16x96 png (6 frames), STANDING_SPRITE, 12 tiles; human ids $68..$a5 (SPRITE_HC_*), SPRITE_POKEMON moved to $b0. Outdoor maps load all sprites of
  their group (<= 23) plus object sprites; only 8 OBJ palettes.
- Trainer classes: ids 68..152 (85 new, 17 per area incl. bosses). Generated trainers use ids >= 128 and HC_FindGenTrainer (**class*3 must be 16-bit**: the 8-bit
  version overflowed from class 87 and gave areas 2-5 garbage parties; fixed). Encounter music of classes >= T_COP is capped to OFFICER (audio/engine.asm).
- ROM space: the Audio bank is full; "Trainer Pic Pointers" moved to ROMX $7c in layout.link; portraits live in "Pics 20" (65 B each). Pic bank byte = BANK - $36 and the
  FixPicBank table only covers Pics 1..24 (extend with identity entries up to bank $7f before adding pics elsewhere). Free ROM is about 250 KB, scattered.
- Still open in this stage: real bust art for the portraits (4x scaled sprites for now), interior art, original Pokemon sprites for the 95 new species (stage 10).
- Testing: tools/hardcore/walk_all.sh [1..5] builds a god-mode test ROM per area and runs the full walker (all five areas PASS).

## Stage 9 notes (wild encounters)
- Every plaza (7 per area, 35 in all) has two tall-grass patches (east x=7..11, west x=1..2, rows 4..8 in blocks; own RNG in layout.grass_patches so the rest of the
  layout does not change). Each tileset has two grass blocks (role "grass", collision TALL_GRASS; art/grass.py: weedy lot, wild grass, bio-turf, resort lawn, ash weed).
- The areas' landmarks lie above KANTO_LANDMARK, so the engine reads wild data from **KantoGrassWildMons**. data/hardcore/gen_wild_grass.asm (areas/wild.py) is
  included in place of data/wild/kanto_grass.asm (vanilla Kanto is unreachable, and the extra table did not fit into bank $0A otherwise).
- areas/wild.py: the 62 base forms are split over the areas by type theme with capacities 16/16/12/10/8 (early areas are played first); inside an area a round robin
  gives each plaza six main slots (30/30/20/10/5/4 percent; every form gets at least one slot of 10+ percent and shows up in 2+ plazas) plus a 1 percent visitor from the
  next area. Level = plaza position inside the area's level range. At night dark/ghost/poison forms move up. Rate 20 percent per step. Output: docs/WILD.md,
  tools/hardcore/wild_out.json.
- tools/hardcore/check_wild.py [ROM]: static proof from the built ROM (table equals generator, grass reachable, every base form catchable, levels in range). PASS.
- tools/hardcore/test_wild.py ROM MAP [N] + wild_all.sh: in-game test (encounters match the table for the time of day, run, fight, catch a mon with a ball,
  kill counter unchanged by wild battles). The walker avoids grass (areamodel.route).
- Open: wild water encounters on the Lotus Coast, Outboard placement, balance of wild levels vs trainers, a few evolved forms in rare slots.

## Alpha 2, pass 1 (bugs and rules from the alpha-1 list) - state
- Done in code: Unown-slot pic table fix, vanilla trainer battle pics, Timmy party/position, paid healing, 70/30 EXP share, half encounter rate, double catch rates
  (gen_roster CATCH_MULT, baked into data/pokemon/base_stats/*.asm), rare mature death texts, intro movie skipped, text overflow guard, Pokecenter 2F and the map card
  removed, loot text terminator fix, trainer tips sign + trainer-reminder NPCs, TMs and consumables as item balls in the lanes (68 pickups, all 50 TMs), bag 45 slots /
  16 balls / 20 PC items, trainer item drops (HC_RollItemDrop), run animation (stride cadence), PHYSICAL/SPECIAL/STATUS label in the summary, wider Cthuludon back sprite,
  unreachable vanilla maps stubbed (tools/hardcore/stub_maps.py; +275 KB free).
- **Tithe Road must end in the checkpoint gate hall.** A plain map connection from the Johto-tileset road into the Tithe plaza (different tileset) crashed the game (reset or
  hang ~10 frames after the crossing, Quilava and Cthuludon alike); same rule as "connected maps must share the tileset". Route -> gate hall -> town is the classic Pokemon
  transition, so the gatehouse is back (areas/a1.py: lane north="door", plaza rift + south="closed", gatehouse "TitheCheckpoint").
- Combined verification (tools/hardcore/verify_all.sh builds the real ROM and every test ROM, then runs): check_wild, test_roster (248 species), test_category (251 moves),
  test_intro (new game to Timmy), test_cross (Cherrygrove <-> Tithe Road connection), test_road (road -> gate hall -> plaza and back), test_features (sign, ball, TM count),
  test_pack (45 items scroll), walk_all 1-5 (192..200 kills each), test_whiteout, test_wild, test_split (0 mismatches), test_story milestone/newbark/ending: all PASS.
- Test notes: test_category needs a 120 frame warm-up since the boot got shorter; the walker's "soft block" lines are detours around item balls and dead trainers (a dead
  trainer stays where he walked up to the player); check_text reports 44 vanilla "<USER>'s" lines at the worst-case name width, not defects.
- Not done in pass 1 (pass 2 / later): bicycle, multiplayer, mobile, phone and Battle Tower code removal beyond the map stubs (about 200 KB more possible), real run sprite
  art, sprite polish, first-kill reveal rewrite, story/world rework (see the alpha-1 triage).

## Alpha 3 (maps, creatures, Purgatorio, crowds) - state
- Maps reworked from the old-school playbook, see docs/MAP_DESIGN_NOTES.md: winding lanes with a wide/narrow rhythm, tree-line borders with ponds, fenced meadows, flower beds
  and groves behind them, glades with item ball, hermit and a hidden item behind a one-block mouth, hub towns with an S-shaped main street and districts with landmarks.
  Scenery blocks (ponds with shores, fences, ledge, tree, flowers, doormat) exist in all five area tilesets (about 33 tiles each, 168..188 of 192 used).
- Townsfolk: every plaza gets up to six neutral locals with lore lines (areas/wayfolk.py, builder.crowd), the 15 object limit is kept (three slots stay free for cameos).
- Creatures: the 16 flat star/blob/orb species were redrawn with real structure (tools/hardcore/sprites/orbs.py: pill, puffball, coil, cubes, clam, starfish, heap, magnets,
  ghost with halo, beach ball with hat, a log-spiral nautilus) and all pictures regenerated with gen_roster.py.
- Purgatorio: test_purg.py passes end to end (junction, Mr. Pokemon, Joyce and the corkboard, four floors down, the Abyss, four floors up, Bruno, Nick's lift).
- Bugs found by the new tests and fixed:
  1. **A door tile on the last row of a map resets the game.** Arriving on a COLL_DOOR / COLL_CAVE cell makes the engine walk the player one step down, off the map edge.
     Open-air rooms and the Purgatorio south mouth now exit over a warp carpet (scenery "mat" block, cave block 0x24). The model scan in docs says: no DOOR-type warp on a last row.
  2. A beaten trainer stays where it stopped, so two of them could seal a one or two tile wide cave corridor for good (PurgUp1). cave.trainer_slots now refuses any slot that
     would split the cave into more pieces when every cell a trainer could stop on is rock.
  3. Some new towns had no tall grass, which starved four Grove forms of wild slots; plaza2 now requires a reachable grass patch.
  4. Boulders return to their original cells whenever a map is entered, so the test pushes them again on the way back up.
- Battle budget (author's decision, Nov 2026, all numbers in tools/hardcore/areas/counts.py, checked by battle_budget.py as a verify_all step): 500 mandatory normal trainers
  (100 per area, Tithe 99 plus Timmy), bosses and scripted duels counted apart (15 plus 1), Purgatorio apart (60), 576 battles of the 650 allowed, room for 74 more special encounters.
  Lanes keep their length (trail() spaces trainer rows GAP = 2 block rows apart). The tidal wave news comes with kill 400 (HC_TSUNAMI_KILLS) wherever it happens, the radio is
  the dead trainer's; the crater comes with the rival, the last boss of Area 4 (kill 412 on the shortest path). Item drop tiers scale with the 500 (50, 100, 175 kills).
- Verification on the final tree: verify_all.sh all PASS (check_text still lists the 44 vanilla lines), walk_all 1-5 pass.
- Not done: TitheRoad (Johto tileset) keeps its old lane, the Tithe junction and the Purgatorio hub were not redesigned, hermits are 18 lanes of 30, unique trainer teams,
  bike/multiplayer/phone/Battle Tower code removal, real run sprite art, first-kill reveal rewrite.

## Baggage removal (Nov 2026, before the special encounters and the Tithe Road rework)
Author's order: remove the vanilla Crystal baggage completely (bicycle data included), get the ROM building and passing the tests, only then add the essential special
encounters and redesign Tithe Road, then walk. Free ROM went from 346 KB (old measure) to 976 KB (432 KB of that are 27 completely empty banks); `python3 tools/hardcore/romfree.py`.
- Gone: decorations and the Mom bank, mail, debug room and colour picker, breeding / daycare / eggs, fruit trees, Unown, 32 vanilla marts, 15 items, the mobile / link / phone /
  Battle Tower engine, 19 songs, 63 overworld sprites, 14 SCGB layouts, the vanilla intro movie (never reachable since alpha 1), 35 of 45 sprite-anim objects, 24 of 35 anim functions,
  53 of 66 framesets, 116 OAM sets, 25 of 41 tilesets (only the 16 the maps use remain), about 1240 of 1300 vanilla event flags, 65 of 67 vanilla trainer party groups and 62 trainer pictures.
- How: each removal is a script in tools/hardcore (unref_asm, dead_labels, prune_items, prune_music, prune_sprites, prune_scgb, prune_spriteanims, prune_tilesets, prune_trainer_data),
  run as post-processing because gen_moves / gen_roster / vanilla.py are NOT maintained against removed data (rerunning them would recreate removed files). Index-aligned tables are
  always pruned together (constants <-> table rows). `rgbasm -M` gives the exact include / INCBIN closure, so assets are deleted only when no object reads them.
- Kept on purpose: field-move code (HM key items replace HMs), Pokegear clock and map, area-theme songs and HC sprites for the map pass, the Johto landmarks table (Pokegear map layout
  depends on it, to be redone with the map pass), vanilla trainer-class slots (rows stay, data is gone, the engine indexes them by class id).
- Still open (small, none blocks the content work): RAM / SRAM leftovers (wLinkMode, unused `ds` areas), ENGINE_* flag pruning, base-stat egg group and step fields (about 700 bytes),
  vanilla trainer attributes / DVs / names rows of dead classes, Sfx_IntroSuicune* and other unused SFX (index aligned with sfx_pointers), empty sections left in layout.link,
  unused landmark names, tileset-animation helper leftovers.


## Tithe Road, fountains, boutiques, NPC density, special encounters (Nov 2026)
- **Tithe Road** is now a winding forest trail (`trail()` on `kits.road()`, vanilla Johto blocks: solid trees 0x05, the Cherrygrove pond rim, boulders as rails, a gate hall of house
  blocks at the north end with the door into TitheCheckpoint, a hermit and a hidden item). Johto tileset kept so the Junction connection is seamless. `tools/hardcore/mapshot.py MAP out.png`
  renders any generated map from its blocks (used to look at it before building a ROM).
- **Generator repair**: `gen_areas.py` could not run after the baggage removal (NorthSouthGate.blk and the Elite Four room blocks were deleted). The gate and boss room blocks are now
  embedded in layout.py (GATE_BLOCKS, BOSS_TEMPLATES) and `gen_tilesets.py` skips the register step that needs a pruned anchor. Regenerating re-rolled every generated trainer team and the Purgatorio layout once (58 trainers there, 60 planned).
- **Fountains**: a new `fountain` scenery block (4 tiles over plain floor, wall collision, last block id so nothing moves; Axiom's tileset is now full at 192 tiles) in every third plaza
  (1, 4, 7) with a plaque to read (wayfolk.FOUNTAIN, names built like Pokemon names).
- **Rare held-item boutiques**: `restore_items.py` brought back LEFTOVERS, QUICK_CLAW, SCOPE_LENS, AMULET_COIN, BRIGHTPOWDER, SMOKE_BALL into every item table (names, descriptions,
  attributes, effects); prices of the held items raised (800 to 6000). Every area has three shops (the mid plaza of each act, a living room with a clerk behind the table; areas/boutique.py:
  PAWNDORA, BARTEROOT, ESCROWBOT, TRADEWIND, DEVILDEAL) with stock that climbs by act and two type boosters of the area's theme. 15 new maps.
- **NPCs**: 9 townsfolk per plaza (was 6), the first of them a named gift-giver (one item, once; 35 more event flags), 40 new gossip lines pointing at the shops, fountains and held items.
- **Special encounters**: 30 named optional duelists (areas/specials.py), see docs/SPECIAL_ENCOUNTERS.md; 604 of 650 battles, 46 slots free.
