# Grandia: Parallel Trippers, how rooms, maps and movement work

Study only, nothing in the game changed. Every number here was measured in the emulator or read from the ROM file with the scripts in `tools/hardcore/refstudy/`
(`grandia_rooms.py`, `grandia_crawl.py`, `grandia_collision.py`, `grandia_stats.py`, `gbdis.py`). Things I observed are written as facts. Things I guessed are marked as guesses.
The last section lists what I could not reach. The ROM is the English patch v1.03 in the repo root.

This corrects one line of `docs/REFERENCE_STUDY.md`. I said Grandia's map data looked compressed. The room maps are not compressed at all.

**Correction, read first.** The first version of this study and of `docs/REFERENCE_STUDY.md` judged Grandia's art from the opening chapter only, and concluded that it has a small art budget and one hue family per place. That was wrong.
You pointed out that the ROM holds far more tiles and assets and that the colours after the opening are much more vibrant. You were right, and section 9 shows why. The opening is displayed through a monochrome pink filter that the game applies to its own full colour palettes,
so every screenshot I measured was a filtered picture. Underneath there are 48 areas with 572 rooms, 3,568 distinct background tiles, and a saturated palette set for every area. Where an older sentence below talks about the "opening" art budget or colours, read it with section 9 next to it.
Rendered pictures of the real art are not in the repo, only the scripts that draw them from your own ROM copy.

## Summary in five lines
1. The game is built from whole screens. A room is exactly one 20 by 18 tile screen, and the camera never scrolls inside it.
2. All 572 room records I found sit in the ROM as raw 900 byte records (556 of them 18 to a bank in banks `$84` to `$A2`, 16 more inside bank `$83`), with a tile layer, an attribute layer and a 10 by 9 collision grid of 16 bit words. They belong to 48 areas, each with its own tileset and palette set (section 9).
3. Neighbouring screens of an area are stored next to each other (the three areas I walked), and walking off an edge scrolls the whole screen over in 44 frames.
4. The hero moves one pixel per frame in four directions, slides around corners by himself, turns in place for a few frames first, and jumps with A. Pits are a cell type, and falling costs health.
5. Collision is per cell and per side, for entering and for leaving separately, which gives one way edges and ledges for free.

## 1. What a room is
- The visible screen is a 20 by 18 tile map. The game keeps it in three WRAM buffers that I located and checked against the live VRAM map: tile ids at `$C4A0` (360 bytes),
  attributes at `$C608` (360 bytes) and the collision grid in WRAM bank 1 at `$D082` (180 bytes). The tile buffer equals the VRAM map cell for cell. The background uses map page `$9C00` or `$9800` (see section 4).
- Map layers use the signed tile id mode and every one of the 50,040 cells in all rooms has attribute bit 3 set, so all background tiles come from VRAM bank 1. Bank 0 is left to sprites and text.
- Rooms never scroll internally. Scroll registers stay at zero while the hero walks. The hero position is a screen position, not a world position.
- The hero position lives in WRAM bank 1. `$D022` is the X of the left edge in screen pixels and `$D021` is the Y of the bottom pixel row of the 16 by 16 body (63 when the body fills pixel rows 48 to 63).
  The sprite object copy is at `$D542` (X) and `$D541` (top Y). Several other bytes that count up while you walk are timers, not positions. I excluded them by checking that they also count while standing still.

## 2. The room database in the ROM
- Banks `$84` to `$A2` (decimal 132 to 162) hold 556 room records. Each bank starts with a record at offset 0 and holds 18 of them (the last bank holds 16). Nothing is compressed, nothing is padded between records, and the rest of the bank is filled with `$FF`.
- One record is 900 bytes: 360 tile ids (20 per row, 18 rows), 360 attribute bytes (same order, standard CGB bits: palette 0 to 2, VRAM bank 3, x flip 5, y flip 6), then 90 collision words
  (10 per row, 9 rows, little endian, one per 16 by 16 pixel cell).
- I numbered the rooms 0 to 555 in ROM order. The opening restaurant is room 531 (bank `$A1`, record 9, file offset `$285FA4`), the hall next to it is room 534.
  I found the restaurant by searching the ROM for the 360 bytes of the live tile buffer. The search hit exactly once.
- Room graphics are raw 2bpp tiles as well. All 45 non-blank tiles of the restaurant's VRAM bank 1 set were found byte for byte in the ROM (many of them near file offset `$3FB000`). How the engine picks a tileset is solved in section 9.
- Cost: 900 bytes per room. All 556 rooms are 500 KB, about an eighth of the 4 MB cartridge. Bank `$B3` holds variable length records with what looks like custom encoded names, possibly monster data. I did not decode it.

### Statistics over all 556 rooms (`grandia_stats.py`)
| measure | value |
|---|---|
| distinct tile ids used by one room | minimum 1, median 28, mean 32, maximum 120 |
| cells with a flip bit | 23 percent |
| background palettes used | only 0 to 4 (palette 0 is 42 percent of cells, palette 4 is 23 percent), palettes 5 to 7 never |
| collision cells fully blocked | 39 percent, open 60 percent, the rest 711 cells with side rules |
| rooms with an open edge | right 317, left 314, top 320, bottom 340 (out of 556) |
| cells of pit type | 9,575 cells in 264 rooms |

The art budget per screen is modest. A typical room needs about 28 distinct tiles and a quarter of its cells are flips of other tiles, and that holds over all 556 records of the main bank range, not only the opening. The budget of the whole game is not small, because every area brings its own tileset and palette set (section 9: 5,832 tile slots, 3,568 distinct tiles).

## 3. Collision words
Each cell has one 16 bit word. I decoded it by writing values into the live grid (`$D082`) of a running room and trying to walk into and out of the edited cell from all four sides (`grandia_collision.py`).

Low byte, observed:
- Bits 0 to 3 block entering the cell, and the bit is named by the side you come from. `$01` blocks coming from the east (moving left), `$02` from the north (moving down), `$04` from the west (moving right), `$08` from the south (moving up).
- Bits 4 to 7 block leaving the cell. `$10` blocks leaving to the east, `$20` to the north, `$40` to the west, `$80` to the south.
  Test result: with `$80` set the hero could not leave downwards, with `$10`, `$20`, `$40` he moved much less in the matching direction (5, 7 and 5 pixels in 14 frames against 13 free). I did not test the partial blocks further, so they might be a delay or a slide rather than a hard stop.
- `$FF` is therefore a solid cell. `$0F` blocks all four ways in. Combinations such as `$05` (entry blocked from the east and west) give corridor walls, and `$01`, `$02`, `$04`, `$08` alone give one way edges.
  Values with a mixed nibble pattern are rare (711 cells in the whole game).

High byte, observed or guessed:
- `$00` plain floor and `$02` the type used with solid walls (17,807 cells are exactly `$02FF`). Observed.
- Odd values (`$01`, `$03`, `$05` and so on, by far `$0100` with 8,911 cells) are pits. Observed: stepping on one makes the hero fall, a text box appears ("Damage is taken when falling into a hole. You can jump over holes, but be ..."), and the hero is put back at the place where he entered the room
  (the entry cell in my test, `(80, 79)`). I did not read any health value, so the damage is known only from the text.
- `$04` (63 cells) behaves as plain floor, tested by edit. `$08`, `$0A`, `$0C`, `$0E` are walkable when the low byte is zero, also tested by edit. In the game data `$0AFF` appears 1,142 times as a blocked cell, my guess is water or another look-only barrier.
  I did not find out what `$0C00` (197 cells), `$0E55` (83) or `$08FF` (83) are for. Marked as unknown.

## 4. Movement
All measured by pressing keys in headless PyBoy and logging memory and OAM every frame.
- Speed is exactly 1 pixel per frame (60 pixels per second). A cell takes 16 frames. I did not get a clean result for the B button, my test run was blocked by a wall.
- Four directions only. With two directions held and one of them blocked the hero moved along the free one. I did not test two free directions at once, and no trace showed a diagonal step.
- The hero is two 8 by 16 sprites side by side. The pose set is three frames per facing (stand, step A, step B), facing down, up and side, and the right facing is the left facing mirrored by the x flip bit.
  The step cycle is stand, step A, stand, step B with 4 frames each, so one full cycle is 16 frames, exactly one cell of walking. Tile ids step by 4 (0, 4, 8 for facing down, 24, 28, 32 for the side pose). The up pose was blocked in my test so I did not see its ids (12 to 20 would fit, a guess).
- Turning: after a change of direction the pose switches 4 frames later and the walking pose starts at frame 7. An earlier run in this study also showed that a short first press only turns him.
- Corner assist. Pressing down while the body overlaps a blocked cell by a few pixels makes the hero slide sideways, one pixel per frame, towards the free column, and then walk on. Started at 4 pixels off a chair he slid 11 pixels sideways and then moved down.
  This is why the game never feels stuck on furniture. The hitbox seems to be about one pixel narrower than the 16 pixel body (the slide stopped with the left edge one pixel inside the blocked column), a guess from three runs.
- Jump. Pressing A while walking starts a jump. The sprites lift in a parabola with a peak of 18 pixels and about 28 frames in the air, while the hero keeps moving one pixel per frame, so a jump covers roughly 28 pixels.
  Airborne, he passed over a pit cell without falling. In a second try I pressed A when he was already standing at the pit edge, he did not clear it and fell, so timing matters. This is the mechanic the pit text refers to.

## 5. Changing rooms
### Edge transition, measured on 531 to 534 and 534 to 535
1. The hero walks to the last cell of the screen and keeps pushing. At the edge the game loads the next room's tiles, attributes and collision into the buffers (the buffer content changes 14 frames after the hero reaches the edge).
2. 4 frames later the screen scrolls by 8 pixels per frame. A horizontal change takes 20 steps (160 pixels), a vertical one 18 steps (144 pixels). I did not test whether input is read while it runs.
3. When the scroll ends, the game flips the background map page (LCDC bit 3 changes between `$9800` and `$9C00`), resets the scroll registers to zero and the new room sits at the origin of the other page.
   I take this as a double buffer: the new room is drawn into the wrapped area of the 32 by 32 map while the old one scrolls away, then both pages are made identical so the next change can start clean.
4. Total about 44 frames (0.73 seconds). The hero arrives at the facing edge of the new room (X went from 144 to 0 on the 531 to 534 change, same row).
5. VRAM tile data is not reloaded during an edge change. I hashed VRAM tile memory in all twelve rooms I reached. It is identical inside each block (six rooms of one, six of the other) and different between the blocks.

### Door warp, measured on 536 to 527
No scroll. The LCD is switched off for a few frames (LCDC bit 7 was cleared on frame 15 and on frames 17 to 23, and the LCD was on again at 24), the room is replaced, and the hero is placed on a given cell (here the door cell `(row 4, column 5)` of the street room 527, pixel `(80, 79)`).
The cut takes about 24 frames. I saw no fade on the DMG palette registers, the game is a Color game, so a fade would run on the Color palette registers that I did not log.

## 6. World layout
I walked the connections with an automatic crawler (`grandia_crawl.py`): it reads the collision grid of the current room from the ROM, plans a path over free cells to an open edge, drives the hero there with key presses and records which room appears. It reached 12 rooms and then ran out of reachable edges.

Three blocks, which are areas 45, 46 and 47 of section 9. They are stored column by column (record index goes down a column first, then to the next column on the right):

| block | rooms | grid (columns by rows) | what it is |
|---|---|---|---|
| street (area 45) | 525 to 530 | 3 by 2 | outdoor grounds: a long building with a clock tower, a running track, a playground, a gate (it reads as a school, a guess) |
| restaurant (area 46) | 531 to 536 | 2 by 3 | three look-alike restaurant rooms (531 to 533, not connected to each other) that each open on their right edge into one screen of a 3 screen hall (534 to 536, connected top to bottom) |
| ruined school (area 47) | 537 to 551 in a 3 by 5 grid, the area has 19 records up to 555 | 3 by 5 | wooden classrooms and corridors full of rubble. I reached 537 to 539, 542 to 544 and 547 to 549. Entering 544 and 547 starts a dialogue that locks input until A is pressed several times |

In the school block the live collision grid differs from the ROM record. The bottom row of room 544 is open in the ROM but blocked while playing, which means the game edits the grid at run time (a closed gate or barricade, my guess). Interacting with the sprite at cell (6, 4) of room 547 with A did nothing from any side, and walking into it only blocks.
I did not find what opens the barricade, so I did not get past this block by playing. The later areas were measured from the ROM instead (section 9).

Observed links: 525 right to 527 right to 529, 525 down to 526, 527 down to 528, 529 down to 530, 528 left to 526 and right to 530, 531 right to 534, 534 down to 535 down to 536, 532 right to 535, 533 right to 536,
and one door warp from the south edge of 536 to 527 at its door cell. Every link between two different rooms had a matching return link, except two cases. Two attempts in room 526 (up and right) ended without a room change, so those two links are inferred from the opposite direction (525 down to 526 and 528 left to 526), and the door warp was only tried one way. Open cells lined up with the neighbouring screen in every pair I checked.

Static evidence, weaker: of the 340 rooms with an open south edge, 216 have a matching open north edge on the next record. A plain chance match is not impossible, so this suggests that column-by-column storage is the rule for most blocks but does not prove it.

What this says about the layout:
- Design is done in screens. Each screen is composed as a picture, with a front building wall on top, open ground below and the exits on the screen edges. Nothing depends on a camera.
- Rooms are reused, not unique. Three variants of the same restaurant open onto three copies of the same hall, so one tileset serves a whole floor.
- The street block has the shape of a real place (building, yard, gate) stitched from six screens that share one tileset (tile ids reach 200), while the interior block needs ids only up to 78.
- Connectivity is explicit. Edge openings (free cells on the screen border) decide where a screen can join its neighbour, and everything else, doors and stairs, goes through warps.

## 7. What could be useful for our game
These are ideas, none of them is decided. Our engine is Crystal's, so each one is tagged with how big the change would be.
1. Screen sized interiors as a design rule (small data question). Compose every interior as one picture. Crystal's blocks are 4 by 4 tiles, so 18 tile rows are 4.5 blocks, an exact screen would need a 5 by 5 block map with the player kept inside the visible part, which I have not tried. This is what the earlier reference study called open plan interiors.
2. One tileset per block and an art budget per screen (no engine change). Aim at 28 distinct tiles for a typical screen and 45 for a busy one, with a quarter of the cells being flips. Crystal already uses one tileset per map. This is a per screen number only. Grandia spends its game budget on many areas, each with its own tileset of 60 to 200 tiles and its own saturated palette set, see idea 8.
3. Per side collision (medium). Crystal's collision is per tile with a few directional types such as ledges and counters. Grandia stores entry and exit bits for all four sides in every cell. We could add a small table of side rules for the cells that need them (one way doors, half walls, step edges).
4. Pits with a jump over them (large, mostly design). A pit cell that costs the lead Pokemon some health and puts you back at the screen entry would fit the dark comedy, and Crystal already has ledge jumps. The A button jump over an arbitrary gap is a different engine and would need new player states. I would only borrow the pit, not the jump.
5. Corner assist (not portable). It works because Grandia moves by pixels. Crystal moves by whole 16 pixel steps, so nothing to slide. Mentioned so we do not look for it.
6. Edge scroll between linked screens (not needed). Crystal already scrolls continuously across map connections. Our connections can behave like Grandia's block grids if we keep the outside world as screens that join edge to edge.
7. Tooling. Raw fixed size room records make it easy to inspect and to diff. Our `.blk` files are already raw. A small export that prints a map as a 10 by 9 grid like the one used here would help review maps.
8. A palette set per area, and a screen wide colour filter (small data change, small engine change for the filter). Grandia gives each of its 48 areas its own five background palettes, mostly saturated and each area in its own colour mood (jungle green, temple blue, lava red, ice cyan, space black and violet).
   Crystal already loads palettes per tileset, so the data side is just more colourful tables. The pink filter of the opening is also worth copying as an effect. The game keeps its palettes in a normal buffer and a second, filtered buffer, and a single flag chooses which one goes to the hardware.
   The filter maps every colour through its brightness onto one ramp, so a flashback, a fever, a blackout or a gas room could reuse the same trick without new art. In Crystal this would be a hook in the palette copy, which I have not read.

## 8. What I could not find or check
- The table that links rooms and the table of warps. I searched the ROM for room numbers next to the door coordinates and for the block start numbers, without a hit, and the engine does not keep the room number as a plain byte or word in WRAM that I could match. The room database itself (which rooms exist and which area each belongs to) is solved in section 9, but not which screen joins which. The block shapes are derived from the rooms I reached, not read from the ROM.
- Event scripts, NPC lists and the battle engine. The pit text shows that stepping on an event cell starts a text box, I did not see anything beyond that.
- Play beyond the three opening areas. I reached 21 rooms and then stopped at the school block, whose barricade I could not open. The debug menu route is still unusable (it jumps into code a developer link supplies). Everything I say about the later areas comes from the ROM tables, not from watching the game run there. That means no live look at their sprites, sprite animation, enemies, or whether the pink filter flag is ever cleared (it was set in all 21 states I saved).
- Meaning of the high byte values `$03`, `$04`, `$08`, `$0A`, `$0C`, `$0E`, the partial exit blocks, and the B button.
- What the pit does to health. The text says damage but I did not read the health value.
- The second list that follows the tile pointers of a tileset (a count byte that is 0 for area 47, so I never saw a non empty one), the indexing of sprite palettes in bank `$09`, the BG 5 to 7 palette source, and every sprite tile and its animation frames.

## 9. The whole world: areas, palettes and tiles (found by reading the loader code)
I got here from the loader code instead of from play. The palette copy routine writes the colour registers from a WRAM buffer, so I read the ROM code around it (bank `$02`, `$699A`), followed the routines that fill the buffer and the VRAM, and then decoded the tables they use. Everything below was checked against live emulator state where I could.

Loader routines in bank 00: `$1622` loads a room (area id in `L`, room number in `E`, stored in WRAM `$D014` and `$D015`), `$12CC` copies a palette set into the buffer, `$12F9` loads the tiles. Their table pointers sit in WRAM at `$D3C0` to `$D3C9` (bank and address of each table, plus the bank base for tile pictures).
- **Areas and rooms.** Bank `$83` at `$4000` holds 48 entries of three bytes, a tileset id and a pointer to the area's room list. A room list is a run of three byte entries, bank and address of each 900 byte record. There are 572 records. 556 are in banks `$84` to `$A2` and 16 are inside bank `$83` at offsets that are not on the 900 byte grid (areas 0 and 1 begin there).
  Every record is listed by exactly one area and none is unlisted. Rooms per area: minimum 1, median 8, maximum 42 (area 1). The area id is also the tileset id and the palette set id. The last three areas, 45, 46 and 47, are the street, restaurant and school of the opening.
- **Background palettes.** Bank `$82` at `$4000` holds 48 pointers, each to five palettes (BG 0 to 4) of four RGB555 colours. Over the game these are 156 distinct palettes and 186 distinct colours. Palettes 5 and 6 come from a shared table elsewhere (I saw them at bank `$7B`, `$4044`) and no map cell uses 5 to 7.
- **The filter.** The buffer at WRAM `$C10F` holds 64 bytes of background and 64 of sprite palettes. The copy routine sends it to the hardware, except that when WRAM `$C2DC` is not zero it sends a second buffer at `$D9EA` (WRAM bank 7). In the opening that second buffer is the first one mapped through brightness onto a pink ramp.
  Colours of equal brightness collapse onto one pink, for example the red `(31,0,4)`, the blue `(7,7,24)` and the green `(9,11,6)` all become `(15,9,11)`. That is why every opening screenshot looked like a single hue family. The real school palette set (area 47) has a green chalkboard, red and blue books and a gold floor. I saw the flag set in all 21 states I saved and have not seen it cleared.
- **Tiles.** Bank `$F9` at `$4000` holds 48 entries of three bytes, a tile count `N` and a pointer to a list of `N` two byte tile pointers. The top two bits of the entry's pointer are a bank offset from `$F9` for the list. In each tile pointer the top two bits are a bank offset from `$FB`, and the other 14 bits are an address in `$4000` to `$7FFF`. Each tile pointer addresses 16 bytes of 2bpp pixels, and tile id `i` is entry `i` of the list.
  Tiles are therefore scattered one by one, which is why my first search found them in many short runs. Check: all 162 tiles of area 47 equal the live VRAM bank 1 byte for byte.
- **Size of the art.** Tileset sizes run from 2 to 201 tiles (mean 121), with area 45 the largest. The 48 tilesets together have 5,832 tile slots and 3,568 distinct tiles. For comparison, our own `gfx/tilesets` have 96 or 192 tiles each and 16 tilesets.
- **Sprite palettes.** I found the live sprite palettes in bank `$09` in a run from `$41A8` to `$5658` with about 295 non empty four colour entries (280 distinct). Together they hold 709 distinct colours, 475 of them vivid, spread over all six hue families.
  Treat these numbers as an upper bound. I judged the region from three live sprite palettes that matched exact entries and from its look, not from the code that indexes it. Crystal draws overworld sprites from eight fixed palettes, so this is a real difference in sprite colour, but I have not seen the later sprites move.
- **What the areas look like** (drawn from the ROM with each area's own palettes, `grandia_atlas.py`). Areas 0 to 2 are jungle and forest in saturated greens, 4 and 5 are blue stone temples with water, 6 to 10 are desert, brick and lava in oranges and reds, 11 and 12 are stone towns,
  13, 14 and 17 are sky or sea with cyan backgrounds, 19 is a ship, 21 to 23 are temples in blue, gold and magenta, 25 to 27 are ice in pale cyans, and 33 to 40 are a family of chambers in the same drawing style, each in its own single bright colour (grey, yellow, purple, red, green, blue, cyan, orange). Areas 43 and 44 are space. The opening areas 45 to 47 are gold and brown outdoors, violet in the restaurant and brown in the school, all hidden under the pink filter.
  On one screen the true palettes give 4 to 13 distinct colours (a few more with sprites), so the low colour count per screen was right. What was wrong is "one hue family per place". The busiest screens show 4 or 5 vivid hue families at once.
  Areas 36 to 40 do not share records, but 20 to 38 of their tiles are identical between neighbours, so the chambers look like one tile style reused with a new palette set and a new layout.

## Tools
- `grandia_rooms.py`: finds a room index from the live tile buffer, reads a record (`rec(n)`), prints collision grids (`show_col(n)`).
- `grandia_crawl.py N`: the room crawler (needs a save state `gr_s4.state` taken in the restaurant after the intro and name entry, saved with `drive.save`; the states are not in the repo). Writes `crawl/edges.json` and one state per room.
- `grandia_collision.py`: edits a collision word in the live grid and tests walking into the cell from each side.
- `grandia_stats.py`: statistics over all 556 records, runs without save states.
- `gbdis.py`: a small disassembler for the Game Boy CPU that I used to look at code near data tables.
- `grandia_db.py`: a reader for the world database of section 9 (palette sets, areas and rooms, tilesets) and a room renderer with the true palettes. `grandia_db.py ROM AREA ROOM out.png` draws one room.
- `grandia_areas.py ROM`: decodes the area and room tables and checks that all 572 records belong to exactly one area.
- `grandia_palettes.py ROM OUTDIR --crystal gfx/tilesets/bg_tiles.pal`: draws the 48 palette sets and prints saturation and hue statistics next to Crystal's.
- `grandia_atlas.py ROM OUTDIR`: draws one room per area into one picture and prints per area statistics. Output pictures are not committed because they show the original game's art.
- `explore/`: the scratch tools I used to walk and crawl the school block (pit aware path planning, live grid sweep, dialogue clearing). They need save states that are not in the repo and ROM paths set in `boot.py`.
