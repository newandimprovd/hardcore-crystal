; wEventFlags bit flags

	const_def
; The first eight flags are reset upon reloading the map
	const EVENT_TEMPORARY_UNTIL_MAP_RELOAD_1
	const EVENT_TEMPORARY_UNTIL_MAP_RELOAD_2
	const EVENT_TEMPORARY_UNTIL_MAP_RELOAD_3
	const EVENT_TEMPORARY_UNTIL_MAP_RELOAD_4
	const EVENT_TEMPORARY_UNTIL_MAP_RELOAD_5
	const EVENT_TEMPORARY_UNTIL_MAP_RELOAD_6
	const EVENT_TEMPORARY_UNTIL_MAP_RELOAD_7
	const EVENT_TEMPORARY_UNTIL_MAP_RELOAD_8
; Johto story events
	const EVENT_GOT_A_POKEMON_FROM_ELM
	const EVENT_GOT_CYNDAQUIL_FROM_ELM
	const EVENT_GOT_TOTODILE_FROM_ELM
	const EVENT_GOT_CHIKORITA_FROM_ELM
	const EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON
	const EVENT_GAVE_MYSTERY_EGG_TO_ELM
	const EVENT_GOT_SS_TICKET_FROM_ELM
	const EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE
	const EVENT_INITIALIZED_EVENTS
	const EVENT_TALKED_TO_MOM_AFTER_MYSTERY_EGG_QUEST
	const EVENT_DUDE_TALKED_TO_YOU
	const EVENT_LEARNED_TO_CATCH_POKEMON
	const EVENT_BEAT_ELITE_FOUR
	const EVENT_GOT_MYSTIC_WATER_IN_CHERRYGROVE
	const EVENT_TOGEPI_HATCHED
	const EVENT_SHOWED_TOGEPI_TO_ELM
	const EVENT_GOT_EVERSTONE_FROM_ELM
	const EVENT_MET_TUSCANY_OF_TUESDAY
	const EVENT_GOT_PINK_BOW_FROM_TUSCANY
	const EVENT_FIRST_TIME_BANKING_WITH_MOM
	const EVENT_TOLD_ELM_ABOUT_TOGEPI_OVER_THE_PHONE
	const EVENT_GOT_MASTER_BALL_FROM_ELM
	const EVENT_LISTENED_TO_INITIAL_RADIO
	const EVENT_WELCOMED_TO_POKECOM_CENTER
; Youngster
	const EVENT_BEAT_YOUNGSTER_JOEY
; Unused: next 116 events
; Sprite visibility flags
; When these events are cleared, the sprite becomes visible; when set, the sprite is hidden.
; The map script command macros `disappear` and `appear` set/clear these flags and immediately apply the effect on visibility.
; The map script command macros `setevent` and `clearevent` set/clear these flags, and their effects will be seen when the map is reloaded.
; Johto itemballs
	const EVENT_CYNDAQUIL_POKEBALL_IN_ELMS_LAB
	const EVENT_TOTODILE_POKEBALL_IN_ELMS_LAB
	const EVENT_CHIKORITA_POKEBALL_IN_ELMS_LAB
	const EVENT_GOT_HM07_WATERFALL
	const EVENT_ROUTE_29_POTION
; Johto people
	const EVENT_RIVAL_NEW_BARK_TOWN
	const EVENT_RIVAL_CHERRYGROVE_CITY
	const EVENT_PLAYERS_HOUSE_MOM_1
	const EVENT_PLAYERS_HOUSE_MOM_2
	const EVENT_GUIDE_GENT_IN_HIS_HOUSE
	const EVENT_GUIDE_GENT_VISIBLE_IN_CHERRYGROVE
	const EVENT_ELMS_AIDE_IN_LAB
	const EVENT_COP_IN_ELMS_LAB
	const EVENT_ROUTE_30_BATTLE
	const EVENT_ROUTE_30_YOUNGSTER_JOEY
	const EVENT_ROUTE_29_TUSCANY_OF_TUESDAY
	const EVENT_PLAYERS_HOUSE_1F_NEIGHBOR
	const EVENT_PLAYERS_NEIGHBORS_HOUSE_NEIGHBOR
	const EVENT_KILLER_REVEALED
	const EVENT_BEAT_YOUNGSTER_TIMMY
	const EVENT_HC_REVEAL_PENDING
	const EVENT_HC_TIDAL_WAVE ; kill 400 (HC_TSUNAMI_KILLS): New Bark Town is flooded
	const EVENT_HC_CRATER ; the rival fell (the last boss of Area 4): New Bark Town is a crater with a portal
	const EVENT_HC_RIVAL_FELL
	const EVENT_HC_FINN_FELL ; the Sleeper in Judecca fell
	const EVENT_HC_ENDED ; the normal ending has played
	const EVENT_HC_ELM_AT_RIM ; Elm waits at the crater rim (set with the crater)
	const EVENT_HC_STOLEN_BACK ; the stolen Pokemon was recovered
	const EVENT_HC_ELM_HIDDEN ; set = PROF. ELM is not on the map (New Bark Town callback clears it with the crater)
	const EVENT_HC_TRUE_ENDING ; the true ending has played (endings task)
	const EVENT_HC_BRUNO_DOWN ; Bruno at Nick's Landing (Purgatorio task)
	const EVENT_HC_GRAVE_SEEN ; the grave of Marcus Fischer
	const EVENT_HC_TRUMPET ; the Trumpet was taken
	const_next 2848 ; Hardcore Crystal: the array grew by 100 bytes (wram.asm), flags 2048-2847 are for generated areas
DEF NUM_EVENTS EQU const_value
