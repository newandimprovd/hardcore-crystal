; Tilesets indexes (see data/tilesets.asm)
	const_def 1
	const TILESET_JOHTO                ; 01
	const TILESET_HOUSE                ; 05
	const TILESET_PLAYERS_HOUSE        ; 06
	const TILESET_POKECENTER           ; 07
	const TILESET_GATE                 ; 08
	const TILESET_LAB                  ; 0a
	const TILESET_MART                 ; 0c
	const TILESET_MANSION              ; 0d
	const TILESET_ELITE_FOUR_ROOM      ; 0f
	const TILESET_PLAYERS_ROOM         ; 14
	const TILESET_CAVE                 ; 18
	const TILESET_TITHE ; HC-ART
	const TILESET_GROVE ; HC-ART
	const TILESET_AXIOM ; HC-ART
	const TILESET_LOTUS ; HC-ART
	const TILESET_DIS ; HC-ART
DEF NUM_TILESETS EQU const_value - 1

; wTileset struct size
DEF TILESET_LENGTH EQU 15

; roof length (see gfx/tilesets/roofs)
DEF ROOF_LENGTH EQU 9

; bg palette values (see gfx/tilesets/*_palette_map.asm)
; TilesetBGPalette indexes (see gfx/tilesets/bg_tiles.pal)
	const_def
	const PAL_BG_GRAY   ; 0
	const PAL_BG_RED    ; 1
	const PAL_BG_GREEN  ; 2
	const PAL_BG_WATER  ; 3
	const PAL_BG_YELLOW ; 4
	const PAL_BG_BROWN  ; 5
	const PAL_BG_ROOF   ; 6
	const PAL_BG_TEXT   ; 7
