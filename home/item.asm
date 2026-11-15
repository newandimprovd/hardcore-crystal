DoItemEffect::
	farcall _DoItemEffect
	ret

CheckTossableItem::
	push hl
	push de
	push bc
	farcall _CheckTossableItem
	pop bc
	pop de
	pop hl
	ret

TossItem::
	push hl
	push de
	push bc
	ldh a, [hROMBank]
	push af
	ld a, BANK(_TossItem)
	rst Bankswitch

	call _TossItem

	pop bc
	ld a, b
	rst Bankswitch
	pop bc
	pop de
	pop hl
	ret

ReceiveItem::
	push bc
	ldh a, [hROMBank]
	push af
	ld a, BANK(_ReceiveItem)
	rst Bankswitch
	push hl
	push de

	call _ReceiveItem

	pop de
	pop hl
	pop bc
	ld a, b
	rst Bankswitch
	pop bc
	ret

CheckItem::
	push hl
	push de
	push bc
	ldh a, [hROMBank]
	push af
	ld a, BANK(_CheckItem)
	rst Bankswitch

	call _CheckItem

	pop bc
	ld a, b
	rst Bankswitch
	pop bc
	pop de
	pop hl
	ret

HC_HasCharm::
; a = a charm (key item). Carry set if the player carries it. Keeps bc, de, hl and wCurItem.
	push hl
	push bc
	ld c, a
	ld a, [wCurItem]
	ld b, a
	ld a, c
	ld [wCurItem], a
	push bc
	ld hl, wNumItems
	call CheckItem
	pop bc
	ld a, b
	ld [wCurItem], a ; loads leave the carry flag alone
	pop bc
	pop hl
	ret
