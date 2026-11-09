; Special routines can be used with the "special" map script command.
; They often use wScriptVar for arguments and return values.

MACRO add_special
\1Special::
	dba \1
ENDM

SpecialsPointers::

; Communications

; Map events
	add_special HealParty ; this is both a special and a predef
	add_special PokemonCenterPC
	add_special NameRival
	add_special SetDayOfWeek
	add_special OverworldTownMap
	add_special FadeOutToWhite
	add_special FadeOutToBlack
	add_special FadeInFromWhite
	add_special FadeInFromBlack
	add_special UpdateTimePals ; bank 0
	add_special UpdatePlayerSprite ; bank 0
	add_special WaitSFX ; bank 0
	add_special PlayMapMusic ; bank 0
	add_special RestartMapMusic ; bank 0
	add_special HealMachineAnim
	add_special SurfStartStep
	add_special FindPartyMonThatSpecies
	add_special FindPartyMonThatSpeciesYourTrainerID
	add_special CheckPokerus
	add_special FadeOutMusic

; Crystal only

	add_special InitialSetDSTFlag
	add_special InitialClearDSTFlag
