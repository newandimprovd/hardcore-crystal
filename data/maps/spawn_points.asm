MACRO spawn
; map, x, y
	map_id \1
	db \2, \3
ENDM

SpawnPoints:
; entries correspond to SPAWN_* constants
	table_width 4

	spawn PLAYERS_HOUSE_2F,            3,  3
if DEF(_TESTMODE)
	TEST_SPAWN_ENTRY
else
	spawn CHERRYGROVE_POKECENTER_1F,   5,  3
endc

	spawn NEW_BARK_TOWN,              13,  6
	spawn CHERRYGROVE_CITY,           29,  4

	INCLUDE "data/maps/area_spawn_points.asm" ; HC-AREAS

	spawn N_A,                        -1, -1

	assert_table_length NUM_SPAWNS + 1
