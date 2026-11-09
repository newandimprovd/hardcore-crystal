; TEMPORARY: sizes that the RAM layout still needs while the removal of the vanilla features is going on.
; tools/hardcore/remove_baggage.py ram deletes the RAM of the removed features and this file with it.
DEF BATTLETOWER_PARTY_LENGTH EQU 3
DEF BATTLETOWER_STREAK_LENGTH EQU 7
DEF BATTLETOWER_TRAINERDATALENGTH EQU 18 * 2
DEF BATTLE_TOWER_STRUCT_LENGTH EQU NAME_LENGTH + BATTLETOWER_PARTY_LENGTH * NICKNAMED_MON_STRUCT_LENGTH + BATTLETOWER_TRAINERDATALENGTH
