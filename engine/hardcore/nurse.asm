; Hardcore Crystal: healing costs money everywhere except in the Cherrygrove POKéCENTER, the only free one (HC_FreeCenters).
; Cost = 40 * highest party level + 200 dollars (ten times the alpha 3.1 price). A player who cannot pay is turned away, unless the whole party has fainted
; (then the nurse heals for free, so nobody is locked out of the game).

HC_NurseComputeCost:
; hMoneyTemp = cost
	ld a, [wPartyCount]
	ld b, a
	ld hl, wPartyMon1Level
	ld de, PARTYMON_STRUCT_LENGTH
	ld c, 0
.loop
	ld a, [hl]
	cp c
	jr c, .next
	ld c, a
.next
	add hl, de
	dec b
	jr nz, .loop
	ld h, 0
	ld l, c
	add hl, hl
	add hl, hl
	add hl, hl ; 8 * level
	ld d, h
	ld e, l
	add hl, hl
	add hl, hl ; 32 * level
	add hl, de ; 40 * level
	ld de, 200
	add hl, de
	xor a
	ldh [hMoneyTemp], a
	ld a, h
	ldh [hMoneyTemp + 1], a
	ld a, l
	ldh [hMoneyTemp + 2], a
	ret

HC_NurseCost:
; wScriptVar: 0 = free here, 1 = the player pays (cost in hMoneyTemp), 2 = cannot pay, 3 = cannot pay but the whole party has fainted (free)
	ld a, [wMapGroup]
	ld b, a
	ld a, [wMapNumber]
	ld c, a
	ld hl, HC_FreeCenters
.free_loop
	ld a, [hli]
	cp -1
	jr z, .charge
	cp b
	ld a, [hli]
	jr nz, .free_loop
	cp c
	jr nz, .free_loop
	xor a
	ld [wScriptVar], a
	ret

.charge
	call HC_NurseComputeCost
	ld bc, hMoneyTemp
	ld de, wMoney
	farcall CompareMoney
	jr c, .poor
	ld a, 1
	ld [wScriptVar], a
	ret

.poor
	ld a, [wPartyCount]
	ld b, a
	ld hl, wPartyMon1HP
	ld de, PARTYMON_STRUCT_LENGTH
.alive_loop
	ld a, [hli]
	or [hl]
	jr nz, .someone_alive
	dec hl
	add hl, de
	dec b
	jr nz, .alive_loop
	ld a, 3
	ld [wScriptVar], a
	ret

.someone_alive
	ld a, 2
	ld [wScriptVar], a
	ret

HC_FreeCenters:
; the only POKéCENTER where healing costs nothing
	map_id CHERRYGROVE_POKECENTER_1F
	db -1

HC_NurseTakeMoney:
	call HC_NurseComputeCost
	ld bc, hMoneyTemp
	ld de, wMoney
	farcall TakeMoney
	ret

HC_NurseAskPaidText:
	text "Healing costs"
	line "¥@"
	text_decimal hMoneyTemp, 3, 6
	text " today."

	para "Pay up and heal"
	line "your #MON?"
	done

HC_NurseNoMoneyText:
	text "Cash up front."
	line "That's ¥@"
	text_decimal hMoneyTemp, 3, 6
	text "."

	para "Come back when"
	line "you have it."
	done

HC_NurseCharityText:
	text "You have nothing"
	line "left. Not even a"
	cont "living #MON."

	para "This one is on"
	line "the house."
	done
