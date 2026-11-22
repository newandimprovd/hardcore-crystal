; Generated trainers (id >= HC_GEN_ID_BASE).
; Each trainer class has an optional group of generated trainers. The group table below says
; in which bank and at which address a class' group starts. A group is a list of trainers:
;   db "NAME@"
;   db level, species, held item ; one to six times (NO_ITEM for none)
;   db -1
; Parties are always TRAINERTYPE_NORMAL with a held item per mon, so moves come from the level-up learnsets.

HC_FindGenTrainer:
; in: c = trainer class (1-based), b = trainer id (>= HC_GEN_ID_BASE)
; out: wHCGenBank = bank of the group, hl = address of the trainer's name; carry if there is no such trainer
	ld hl, HC_GenGroupTable
	ld a, c
	dec a
	ld e, a
	ld d, 0
	add hl, de
	add hl, de
	add hl, de ; 3 * (class - 1) in 16 bits: 8 bits overflow from class 87 on
	ld a, [hli]
	ld [wHCGenBank], a
	and a
	jr z, .none
	ld a, [hli]
	ld h, [hl]
	ld l, a
	ld a, b
	sub HC_GEN_ID_BASE - 1
	ld b, a
.next
	dec b
	jr z, .found
.skip
	ld a, [wHCGenBank]
	call GetFarByte
	inc hl
	cp -1
	jr nz, .skip
	jr .next
.found
	and a
	ret
.none
	scf
	ret

HC_ReadGeneratedParty::
; Fills wOTPartyMons from the generated trainer wOtherTrainerClass / wOtherTrainerID.
	ld a, [wOtherTrainerID]
	ld b, a
	ld a, [wOtherTrainerClass]
	ld c, a
	call HC_FindGenTrainer
	ret c
.skip_name
	ld a, [wHCGenBank]
	call GetFarByte
	inc hl
	cp '@'
	jr nz, .skip_name
.mon
	ld a, [wHCGenBank]
	call GetFarByte
	inc hl
	cp -1
	ret z
	ld [wCurPartyLevel], a
	ld a, [wHCGenBank]
	call GetFarByte
	inc hl
	ld [wCurPartySpecies], a
	; the last mon of every rival party is the rival's own starter, the one that was meant to beat the player's
	ld a, [wOtherTrainerClass]
	cp RIVAL1
	jr z, .rival
	cp RIVAL2
	jr nz, .add_mon
.rival
; the byte after the item is the end mark of the party when this is the last mon
	inc hl
	ld a, [wHCGenBank]
	call GetFarByte
	dec hl
	cp -1
	jr nz, .add_mon
	push hl
	call HC_RivalStarter
	ld [wCurPartySpecies], a
	pop hl
.add_mon
	ld a, OTPARTYMON
	ld [wMonType], a
	push hl
	predef TryAddMonToParty
	ld a, [wOTPartyCount]
	dec a
	ld hl, wOTPartyMon1Item
	ld bc, PARTYMON_STRUCT_LENGTH
	call AddNTimes
	ld d, h
	ld e, l
	pop hl
	ld a, [wHCGenBank]
	call GetFarByte
	inc hl
	ld [de], a
	jr .mon

HC_RivalStarter:
; out: a = the species of the rival's starter at the stage that fits wCurPartyLevel (stages at 25, 50 and 75 like the rest of the roster).
; The player took TOTODILE: the rival has CHIKORITA. The player took CHIKORITA: the rival has CYNDAQUIL. Otherwise the rival has TOTODILE.
	ld de, EVENT_GOT_TOTODILE_FROM_ELM
	ld b, CHECK_FLAG
	call EventFlagAction
	ld a, c
	and a
	ld hl, .Chikorita
	jr nz, .got_line
	ld de, EVENT_GOT_CHIKORITA_FROM_ELM
	ld b, CHECK_FLAG
	call EventFlagAction
	ld a, c
	and a
	ld hl, .Cyndaquil
	jr nz, .got_line
	ld hl, .Totodile
.got_line
	ld a, [wCurPartyLevel]
	ld c, 0
	cp 25
	jr c, .got_stage
	inc c
	cp 50
	jr c, .got_stage
	inc c
	cp 75
	jr c, .got_stage
	inc c
.got_stage
	ld b, 0
	add hl, bc
	ld a, [hl]
	ret

.Chikorita:
	db CHIKORITA, BAYLEEF, MEGANIUM, ELDERWOOD
.Cyndaquil:
	db CYNDAQUIL, QUILAVA, TYPHLOSION, CALDERA
.Totodile:
	db TOTODILE, CROCONAW, FERALIGATR, DEATHROLL

HC_GetGeneratedTrainerName::
; in: b = trainer id, c = trainer class. out: de = wStringBuffer1 holding the name.
	call HC_FindGenTrainer
	ld de, wStringBuffer1
	jr c, .unknown
	ld c, NAME_LENGTH - 1
.copy
	ld a, [wHCGenBank]
	call GetFarByte
	inc hl
	cp '@'
	jr z, .done
	ld [de], a
	inc de
	dec c
	jr nz, .copy
.done
	ld a, '@'
	ld [de], a
	ld de, wStringBuffer1
	ret
.unknown
	ld a, '?'
	ld [de], a
	inc de
	ld a, '@'
	ld [de], a
	ld de, wStringBuffer1
	ret
