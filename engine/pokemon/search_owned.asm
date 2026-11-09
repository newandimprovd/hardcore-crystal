rept NAME_LENGTH_JAPANESE - 2
	ld a, [de]
	cp [hl]
	jr nz, .notfound
	cp '@'
	jr z, .found
	inc hl
	inc de
endr

	ld a, [de]
	cp [hl]
	jr z, .found

.notfound
	pop de
	pop hl
	pop bc
	and a
	ret

.found
	pop de
	pop hl
	pop bc
	scf
	ret

