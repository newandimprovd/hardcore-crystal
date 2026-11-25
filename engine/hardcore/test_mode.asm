; Test-only setup for emulator runs. Compiled out of the real ROM.
if DEF(_TESTMODE)

MACRO test_setevent
	ld de, \1
	ld b, SET_FLAG
	call EventFlagAction
ENDM

MACRO test_giveitem
	ld a, \1
	ld [wCurItem], a
	ld a, \2
	ld [wItemQuantityChange], a
	ld hl, wNumItems
	call ReceiveItem
ENDM

HC_TestIntro::
	farcall InitCrystalData
if STRLEN("{TEST_NAME}") > 0 ; the player's name (the ending ROM: CHRIS); InitName would leave a zeroed name alone, so copy it
	ld hl, .name
	ld de, wPlayerName
	ld bc, NAME_LENGTH
	call CopyBytes
endc
	ret

if STRLEN("{TEST_NAME}") > 0
.name
	db "{TEST_NAME}@@@@@@@@@@@"
endc

HC_TestSetup::
	ld a, TEST_MON
	ld [wCurPartySpecies], a
	ld a, TEST_LEVEL
	ld [wCurPartyLevel], a
	xor a
	ld [wMonType], a
	farcall TryAddMonToParty
	test_setevent EVENT_GOT_A_POKEMON_FROM_ELM
	test_setevent EVENT_GOT_CYNDAQUIL_FROM_ELM
	ld de, ENGINE_POKEGEAR
	ld b, SET_FLAG
	farcall EngineFlagAction
	ld de, ENGINE_MAP_CARD
	ld b, SET_FLAG
	farcall EngineFlagAction
	ld de, ENGINE_POKEDEX
	ld b, SET_FLAG
	farcall EngineFlagAction
	if TEST_BEATEN
	test_setevent EVENT_BEAT_YOUNGSTER_JOEY
	endc
	if TEST_REVEALED
	test_setevent EVENT_KILLER_REVEALED
	endc
	if TEST_STORY >= 1
	test_setevent EVENT_HC_TIDAL_WAVE
	endc
	if TEST_STORY >= 2
	test_setevent EVENT_HC_CRATER
	test_setevent EVENT_HC_ELM_AT_RIM
	test_setevent EVENT_HC_RIVAL_FELL
	endc
	if TEST_STORY >= 3
	test_setevent EVENT_HC_FINN_FELL
	endc
	if TEST_ITEMS
	test_giveitem CHAINSAW, 1
	test_giveitem JET_SKI, 1
	test_giveitem CROWBAR, 1
	test_giveitem FLASHLIGHT, 1
	test_giveitem OUTBOARD, 1
	test_giveitem GRAPPLE_HOOK, 1
	test_giveitem SLEDGEHAMMER, 1
	test_giveitem BASEBALL_BAT, 1
	test_giveitem SHOVEL, 1
	test_giveitem GETAWAY_CAR, 1
	endc
	test_giveitem POKE_BALL, 20
	test_giveitem SUPER_POTION, 10
	if TEST_FULLDEX
	call HC_TestFillBoxes
	endc
	ret

if TEST_FULLDEX
; Alpha 3.3 (the ending ROM): every species caught, level 100, stored in the PC boxes (20 to a box, species order) and so the Pokedex is complete too:
; SendMonIntoBox marks each species seen and caught.  The boxes are saved one by one; the last step opens box 1 again.
HC_TestFillBoxes:
	farcall EraseBoxes
	xor a
	ld [wCurBox], a
	ld b, 1
.next
	push bc
	ld a, BANK(sBoxCount)
	call OpenSRAM
	ld a, [sBoxCount]
	call CloseSRAM
	cp MONS_PER_BOX
	jr c, .room
	farcall SaveBox
	ld hl, wCurBox
	inc [hl]
	farcall LoadBox
.room
	pop bc
	push bc
	ld a, b
	ld [wCurPartySpecies], a
	ld [wTempEnemyMonSpecies], a
	ld a, 100
	ld [wCurPartyLevel], a
	callfar LoadEnemyMon
	farcall SendMonIntoBox
	pop bc
	inc b
	ld a, b
	cp NUM_POKEMON + 1
	jr c, .next
	farcall SaveBox
	xor a
	ld [wCurBox], a
	farcall LoadBox
	ret
endc
endc
