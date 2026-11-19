# Grandia: Parallel Trippers, how rooms, maps and movement work

Study only, nothing in the game changed. Every number here was measured in the emulator or read from the ROM file with the scripts in `tools/hardcore/refstudy/`
(`grandia_rooms.py`, `grandia_crawl.py`, `grandia_collision.py`, `grandia_stats.py`, `gbdis.py`). Things I observed are written as facts. Things I guessed are marked as guesses.
The last section lists what I could not reach. The ROM is the English patch v1.03 in the repo root.

This corrects one line of `docs/REFERENCE_STUDY.md`. I said Grandia's map data looked compressed. The room maps are not compressed at all.

## Summary in five lines
1. The game is built from whole screens. A room is exactly one 20 by 18 tile screen, and the camera never scrolls inside it.
2. All 556 rooms I found sit in the ROM as raw 900 byte records, 18 to a bank, with a tile layer, an attribute layer and a 10 by 9 collision grid of 16 bit words.
3. Rooms are grouped into blocks that share one tileset. Neighbouring screens of a block are stored next to each other, and walking off an edge scrolls the whole screen over in 44 frames.
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
- Room graphics are raw 2bpp tiles as well. All 45 non-blank tiles of the restaurant's VRAM bank 1 set were found byte for byte in the ROM (many of them near file offset `$3FB000`). I did not trace how the engine picks a tileset for a block.
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

The art budget is small. A typical room needs about 28 distinct tiles and a quarter of its cells are flips of other tiles. That is how the opening rooms measured in the earlier study (41 to 44 distinct tiles on a whole busy screen) fit the numbers.

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

Two blocks, both stored column by column (record index goes down a column first, then to the next column on the right):

| block | rooms | grid (columns by rows) | what it is |
|---|---|---|---|
| street | 525 to 530 | 3 by 2 | outdoor grounds: a long building with a clock tower, a running track, a playground, a gate (it reads as a school, a guess) |
| restaurant | 531 to 536 | 2 by 3 | three look-alike restaurant rooms (531 to 533, not connected to each other) that each open on their right edge into one screen of a 3 screen hall (534 to 536, connected top to bottom) |

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
2. One tileset per block and an art budget per screen (no engine change). Aim at 28 distinct tiles for a typical screen and 45 for a busy one, with a quarter of the cells being flips. Crystal already uses one tileset per map.
3. Per side collision (medium). Crystal's collision is per tile with a few directional types such as ledges and counters. Grandia stores entry and exit bits for all four sides in every cell. We could add a small table of side rules for the cells that need them (one way doors, half walls, step edges).
4. Pits with a jump over them (large, mostly design). A pit cell that costs the lead Pokemon some health and puts you back at the screen entry would fit the dark comedy, and Crystal already has ledge jumps. The A button jump over an arbitrary gap is a different engine and would need new player states. I would only borrow the pit, not the jump.
5. Corner assist (not portable). It works because Grandia moves by pixels. Crystal moves by whole 16 pixel steps, so nothing to slide. Mentioned so we do not look for it.
6. Edge scroll between linked screens (not needed). Crystal already scrolls continuously across map connections. Our connections can behave like Grandia's block grids if we keep the outside world as screens that join edge to edge.
7. Tooling. Raw fixed size room records make it easy to inspect and to diff. Our `.blk` files are already raw. A small export that prints a map as a 10 by 9 grid like the one used here would help review maps.

## 8. What I could not find or check
- The table that links rooms and the table of warps. I searched the ROM for room numbers next to the door coordinates and for the block start numbers, without a hit, and the engine does not keep the room number as a plain byte or word in WRAM that I could match. So the block shapes are derived from the 12 rooms I reached, not read from the ROM.
- The current room variable, event scripts, NPC lists and the battle engine. The pit text shows that stepping on an event cell starts a text box, I did not see anything beyond that.
- Everything beyond the 12 reachable rooms. The crawler stopped because the remaining edges are closed by walls or doors. The debug menu route is still unusable (it jumps into code a developer link supplies).
- Meaning of the high byte values `$03`, `$04`, `$08`, `$0A`, `$0C`, `$0E`, the partial exit blocks, and the B button.
- What the pit does to health. The text says damage but I did not read the health value.
- Tileset selection. I know a block loads one tileset and that tiles 0 to 45 of the restaurant come from the start of bank 1, but not which table points to it.

## Tools
- `grandia_rooms.py`: finds a room index from the live tile buffer, reads a record (`rec(n)`), prints collision grids (`show_col(n)`).
- `grandia_crawl.py N`: the room crawler (needs a save state `gr_s4.state` taken in the restaurant after the intro and name entry, saved with `drive.save`; the states are not in the repo). Writes `crawl/edges.json` and one state per room.
- `grandia_collision.py`: edits a collision word in the live grid and tests walking into the cell from each side.
- `grandia_stats.py`: statistics over all 556 records, runs without save states.
- `gbdis.py`: a small disassembler for the Game Boy CPU that I used to look at code near data tables.
