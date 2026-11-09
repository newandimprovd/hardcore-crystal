Magikarp_LoadFeetInchesChars:
	ld hl, vTiles2 tile '′' ; $6e
	ld de, .feetinchchars
	lb bc, BANK(.feetinchchars), 2
	call Request2bpp
	ret

.feetinchchars
INCBIN "gfx/font/feet_inches.2bpp"

PrintMagikarpLength:
	call Magikarp_LoadFeetInchesChars
	ld hl, wStringBuffer1
	ld de, wMagikarpLength
	lb bc, PRINTNUM_LEFTALIGN | 1, 2
	call PrintNum
	ld [hl], '′'
	inc hl
	ld de, wMagikarpLength + 1
	lb bc, PRINTNUM_LEFTALIGN | 1, 2
	call PrintNum
	ld [hl], '″'
	inc hl
	ld [hl], '@'
	ret

INCLUDE "data/events/magikarp_lengths.asm"

MagikarpHouseSign:
	ld a, [wBestMagikarpLengthFeet]
	ld [wMagikarpLength], a
	ld a, [wBestMagikarpLengthInches]
	ld [wMagikarpLength + 1], a
	call PrintMagikarpLength
	ld hl, .KarpGuruRecordText
	call PrintText
	ret

.KarpGuruRecordText:
	text_far _KarpGuruRecordText
	text_end
