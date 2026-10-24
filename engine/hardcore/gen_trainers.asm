; Generated trainers (id >= HC_GEN_ID_BASE).
; Each trainer class has an optional group of generated trainers. The group table below says
; in which bank and at which address a class' group starts. A group is a list of trainers:
;   db "NAME@"
;   db level, species ; one to six times
;   db -1
; Parties are always TRAINERTYPE_NORMAL, so moves come from the level-up learnsets.

HC_FindGenTrainer:
; in: c = trainer class (1-based), b = trainer id (>= HC_GEN_ID_BASE)
; out: wHCGenBank = bank of the group, hl = address of the trainer's name; carry if there is no such trainer
	ld hl, HC_GenGroupTable
	ld a, c
	dec a
	ld e, a
	add a
	add e ; a = 3 * (class - 1)
	ld e, a
	ld d, 0
	add hl, de
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
	ld a, OTPARTYMON
	ld [wMonType], a
	push hl
	predef TryAddMonToParty
	pop hl
	jr .mon

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
