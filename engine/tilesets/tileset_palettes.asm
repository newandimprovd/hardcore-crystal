LoadSpecialMapPalette:
	ld a, [wMapTileset]
	cp TILESET_HOUSE
	jr nz, .do_nothing
	call LoadHousePalette
	scf
	ret

.do_nothing
	and a
	ret

LoadHousePalette:
	ld a, BANK(wBGPals1)
	ld de, wBGPals1
	ld hl, HousePalette
	ld bc, 8 palettes
	call FarCopyWRAM
	ret

HousePalette:
INCLUDE "gfx/tilesets/house.pal"
