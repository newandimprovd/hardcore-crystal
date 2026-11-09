MACRO scene_var
; map, variable
	map_id \1
	dw \2
ENDM

MapScenes::
	scene_var NEW_BARK_TOWN,                               wNewBarkTownSceneID
	scene_var ELMS_LAB,                                    wElmsLabSceneID
	scene_var PLAYERS_HOUSE_1F,                            wPlayersHouse1FSceneID
	scene_var ROUTE_29,                                    wRoute29SceneID
	scene_var CHERRYGROVE_CITY,                            wCherrygroveCitySceneID
	db -1 ; end
