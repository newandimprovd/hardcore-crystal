MACRO tilepal
; used in gfx/tilesets/*_palette_map.asm
; vram bank, pals
	DEF x = OAM_BANK\1
	rept (_NARG - 1) / 2
		dn (x | PAL_BG_\3), (x | PAL_BG_\2)
		shift 2
	endr
ENDM

Tileset0PalMap:
TilesetJohtoPalMap:
INCLUDE "gfx/tilesets/johto_palette_map.asm"

TilesetHousePalMap:
INCLUDE "gfx/tilesets/house_palette_map.asm"

TilesetPlayersHousePalMap:
INCLUDE "gfx/tilesets/players_house_palette_map.asm"

TilesetPokecenterPalMap:
INCLUDE "gfx/tilesets/pokecenter_palette_map.asm"

TilesetGatePalMap:
INCLUDE "gfx/tilesets/gate_palette_map.asm"

TilesetLabPalMap:
INCLUDE "gfx/tilesets/lab_palette_map.asm"

TilesetMartPalMap:
INCLUDE "gfx/tilesets/mart_palette_map.asm"

TilesetMansionPalMap:
INCLUDE "gfx/tilesets/mansion_palette_map.asm"

TilesetEliteFourRoomPalMap:
INCLUDE "gfx/tilesets/elite_four_room_palette_map.asm"

TilesetCavePalMap:
INCLUDE "gfx/tilesets/cave_palette_map.asm"

TilesetPlayersRoomPalMap:
INCLUDE "gfx/tilesets/players_room_palette_map.asm"

UnusedMuseumPalMap: ; unreferenced
INCLUDE "gfx/tilesets/unused_museum_palette_map.asm"

MapGroupPalettes: ; unreferenced
; entries correspond to MAPGROUP_* constants
rept NUM_MAP_GROUPS
	db PAL_BG_ROOF
endr

; HC-ART begin
TilesetTithePalMap:
INCLUDE "gfx/tilesets/tithe_palette_map.asm"

TilesetGrovePalMap:
INCLUDE "gfx/tilesets/grove_palette_map.asm"

TilesetAxiomPalMap:
INCLUDE "gfx/tilesets/axiom_palette_map.asm"

TilesetLotusPalMap:
INCLUDE "gfx/tilesets/lotus_palette_map.asm"

TilesetDisPalMap:
INCLUDE "gfx/tilesets/dis_palette_map.asm"

