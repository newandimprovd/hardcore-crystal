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
	call InitCrystalData
	ld hl, wPlayerName
	ld de, .name
	call InitName
	ret

.name
	db "TEST@"

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
	ld de, ENGINE_POKEDEX
	ld b, SET_FLAG
	farcall EngineFlagAction
	if TEST_BEATEN
	test_setevent EVENT_BEAT_YOUNGSTER_JOEY
	endc
	if TEST_REVEALED
	test_setevent EVENT_KILLER_REVEALED
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
	test_giveitem BICYCLE, 1
	endc
	test_giveitem POKE_BALL, 20
	test_giveitem SUPER_POTION, 10
	ret
endc
