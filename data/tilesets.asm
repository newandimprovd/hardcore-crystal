MACRO tileset
	dba \1GFX, \1Meta, \1Coll
	dw \1Anim
	dw NULL
	dw \1PalMap
ENDM

; Associated data:
; - The *GFX, *Meta, and *Coll are defined in gfx/tilesets.asm
; - The *PalMap are defined in gfx/tileset_palette_maps.asm
; - The *Anim are defined in data/tileset_anims.asm

Tilesets::
; entries correspond to TILESET_* constants (see constants/tileset_constants.asm)
	table_width TILESET_LENGTH
	tileset Tileset0
	tileset TilesetJohto
	tileset TilesetHouse
	tileset TilesetPlayersHouse
	tileset TilesetPokecenter
	tileset TilesetGate
	tileset TilesetLab
	tileset TilesetMart
	tileset TilesetMansion
	tileset TilesetEliteFourRoom
	tileset TilesetPlayersRoom
	tileset TilesetCave
	tileset TilesetTithe ; HC-ART
	tileset TilesetGrove ; HC-ART
	tileset TilesetAxiom ; HC-ART
	tileset TilesetLotus ; HC-ART
	tileset TilesetDis ; HC-ART
	assert_table_length NUM_TILESETS + 1
