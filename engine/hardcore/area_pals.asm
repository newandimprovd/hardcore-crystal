; Hardcore Crystal: every map of the five generated areas has its own background palettes (outdoor and indoor set per area),
; whatever the time of day.  Source: tools/hardcore/art/areapal.py -> gfx/tilesets/area_bg.pal

DEF NUM_AREAS EQU 5

HC_LoadAreaPalette::
; Loads the 8 background palettes of the area into wBGPals1.  Carry is set if the current map belongs to an area.
; Three sets per area: 0 = outdoor maps with the area's own tilesets, 1 = outdoor maps with vanilla tiles (the road out of
; Cherrygrove), 2 = everything indoors.
	ld a, [wMapGroup]
	sub MAPGROUP_AREA1
	jr c, .none
	cp NUM_AREAS
	jr nc, .none
	ld b, a
	add a
	add b ; * 3
	ld b, a
	ld a, [wMapTileset]
	cp TILESET_TITHE
	jr nc, .set_out ; the area tilesets come last in the tileset list
	ld a, [wEnvironment]
	cp TOWN
	jr z, .set_road
	cp ROUTE
	jr z, .set_road
	inc b ; indoor
.set_road
	inc b
.set_out
	ld a, b
	ld l, a
	ld h, 0
	add hl, hl
	add hl, hl
	add hl, hl
	add hl, hl
	add hl, hl
	add hl, hl ; * 64 bytes (8 palettes)
	ld de, HC_AreaBGPals
	add hl, de
	ld a, BANK(wBGPals1)
	ld de, wBGPals1
	ld bc, 8 palettes
	call FarCopyWRAM
	scf
	ret

.none
	and a
	ret

HC_AreaBGPals:
INCLUDE "gfx/tilesets/area_bg.pal"
