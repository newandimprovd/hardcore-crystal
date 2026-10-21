; Hardcore Crystal always-loaded helpers.
; This section sits in the unused gap between the interrupt vectors and the cartridge header.

SECTION "Hardcore Home", ROM0[$0063]

GetMoveCategory::
; Input:  a = move ID (1-251).
; Output: a = SPECIAL if the move is special, 0 if physical (status moves are 0).
; The result is meant to be followed by `cp SPECIAL`, exactly like the type
; byte was in vanilla (carry set = physical). Preserves bc, de and hl.
	push hl
	push bc
	dec a
	ld c, a ; c = move ID - 1
	srl a
	srl a
	srl a ; a = byte offset into MoveCategoryBits
	ld hl, MoveCategoryBits
	add l
	ld l, a
	adc h
	sub l
	ld h, a
	ld a, [hl]
	ld b, a ; b = bit row
	ld a, c
	and %111
	jr z, .test
	ld c, a
.shift
	srl b
	dec c
	jr nz, .shift
.test
	xor a
	bit 0, b
	jr z, .done
	ld a, SPECIAL
.done
	pop bc
	pop hl
	ret

INCLUDE "data/hardcore/move_category_bits.asm"
