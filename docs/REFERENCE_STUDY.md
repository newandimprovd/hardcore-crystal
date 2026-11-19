# Reference ROM study: crystal16-bit and Grandia: Parallel Trippers

Done after alpha 3.1. This is a study, nothing in the game changed. Every number below was measured in the emulator or from the ROM files with the scripts in
`tools/hardcore/refstudy/`. Ideas are marked as ideas. Things I could not reach are listed at the end.

## crystal16-bit.gbc
- Header says 4 MB MBC3 with the title PM_CRYSTAL, but the file is padded. The last byte that is not padding sits in bank 128, so the content is about 2.01 MB.
- The name table holds 707 species entries, from BULBASAUR to FARIGIRAF (generation 9 names such as TATSUGIRI and CLODSIRE are in it).
- The intro, the bedroom, the house, the neighbour houses and New Bark Town play and look like vanilla Crystal. Side by side with our own New Bark Town (same engine,
  a night palette against a day palette) 29 of the 34 distinct pixel tiles on the two screens are byte identical and the rest are screen differences.
  So this ROM is not a graphics overhaul. I said it was in a status message while working, that was wrong.
- Most likely identification, from the species count and the public project of that name (vulcandth/pokecrystal16): a Crystal build with 16-bit species indexes.
  That makes it a programming reference (more than 253 species, bigger tables, bank layout), not a map or tile reference. I did not read its source, only its ROM.
- Compared in 12 byte windows, 40 percent of this ROM's non-padding data also exists in vanilla Crystal and 52 percent of vanilla exists in it, so a large part of the tables and graphics was moved or rebuilt.

## Grandia: Parallel Trippers (English patch v1.03), measured on the opening rooms only
Measured on one full screen (20 by 18 cells, 360 cells) with `analyze()`.

| screen | tile ids | distinct pixel tiles | distinct 2x2 groups | flipped cells | palettes used | colours on screen | sprites |
|---|---|---|---|---|---|---|---|
| Grandia restaurant | 45 | 44 | 32 | 101 | 5 | 12 | 8x16 |
| Grandia hall | 43 | 41 | 23 | 50 | 5 | 14 | 8x16 |
| crystal16-bit New Bark Town | 36 | 33 | 22 | 0 | 6 | 19 | 8x8 |
| our Tithe Plaza 1 | 61 | 51 | 35 | 0 | 7 | 9 | 8x8 |
| our New Bark Town (vanilla tiles) | 33 | 30 | 19 | 0 | 6 | 18 | 8x8 |
| our Judecca centre | 22 | 19 | 11 | 0 | 4 | 14 | 8x8 |

What the screens show.
- A whole Grandia room is drawn with 41 to 44 distinct tiles and 11 to 13 empty cells out of 360, so the screen is dense. flip flags are set on 50 to 101 of the 360 cells (14 to 28 percent)
  and the mirrored pieces are pillars, chairs, counters and wall ends. Our screens flip nothing.
- Each location keeps one hue family. The restaurant and hall are pink with five palettes of the same family and 12 to 14 colours on screen in total.
  Depth comes from tone steps inside that family. The floor is a two tone diamond check, the walls have a striped band and a dark base line, furniture shows a lit top face and a darker front face.
- Rooms flow into each other. The restaurant, the hall and an outdoor flower strip appeared as one continuous scrolling area in step by step captures, with no black frame between them.
- Dialogue shows a face portrait in the text box (several characters, left or right end of the box), and the box sits at the top of the screen when the speakers are at the bottom, and the other way round.
- The game keeps the hardware scroll registers at zero at rest, sprites are 8x16, and no window layer was in use on the map screens.

## Ideas (not built, none is a promise)
1. Mirror aware tilesets. Teach the tileset generator to fold mirrored tiles into one tile and use the flip bits of the tile attributes. Grandia sets flip flags on 14 to 28 percent of the cells of a screen.
   The tile slots this frees can go to detail, for example roof edges, worn stone and the shaded front faces that give buildings depth. This is a generator change, not an engine change.
2. Open plan interiors. A market hall, an arcade or a cathedral nave drawn as part of the outdoor map, so the player walks in without a warp fade like Grandia does.
   It needs map work and some blocks, not engine work, and it gives the Tithe and Axiom plazas a reason to feel connected.
3. One hue family per place with tone steps for depth. Our areas already do this in spirit. Grandia suggests keeping the on screen colour count low (12 to 14) and spending the effort on tile detail.
4. Two faced furniture and counters (lit top, darker front) in the interior tileset, in line with the whole two row building rule you asked for.
5. Dialogue portraits for the named cast (Mr. Pokemon, Joyce, Steiner, Crowley, Sabbah, Cioran). Grandia shows what it adds. In Crystal it is engine work (VRAM for 16 tiles per face while a box is open),
   so it should wait for a version that touches the text engine. Moving the text box to the top when the speaker is at the bottom is a smaller first step.

## What I could not see
- Grandia beyond the restaurant and its hall. The documented debug menu (code 9003EFCF, then Start on the main menu) does open, but every entry jumps into RAM code that a developer link loads,
  so each one crashes in the emulator. The exit of the hall was found later (see `docs/GRANDIA_ENGINE_STUDY.md`, 12 rooms reached), the rest of Grandia is still unseen.
- crystal16-bit beyond New Bark Town. The east exit of the town was not reachable in my tests, so routes, caves and cities of that ROM are unseen. Its Pokemon sprites and icons were not examined.
- Grandia's map format: found afterwards, see `docs/GRANDIA_ENGINE_STUDY.md`. The room maps and the tile graphics I checked are stored raw. My earlier guess from the entropy scan, that most of its data is compressed, was wrong for those.
