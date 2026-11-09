MACRO treemon_map
	map_id \1
	db \2 ; treemon set
ENDM

TreeMonMaps:
	treemon_map ROUTE_29,                  TREEMON_SET_ROUTE
	treemon_map NEW_BARK_TOWN,             TREEMON_SET_NONE
	treemon_map CHERRYGROVE_CITY,          TREEMON_SET_NONE
	db -1

RockMonMaps:
	db -1
