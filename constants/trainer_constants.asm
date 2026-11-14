DEF __trainer_class__ = 0

MACRO trainerclass
	DEF \1 EQU __trainer_class__
	DEF __trainer_class__ += 1
	const_def 1
ENDM

; trainer class ids
; `trainerclass` indexes are for:
; - TrainerClassNames (see data/trainers/class_names.asm)
; - TrainerClassAttributes (see data/trainers/attributes.asm)
; - TrainerClassDVs (see data/trainers/dvs.asm)
; - TrainerGroups (see data/trainers/party_pointers.asm)
; - TrainerEncounterMusic (see data/trainers/encounter_music.asm)
; - TrainerPicPointers (see data/trainers/pic_pointers.asm)
; - TrainerPalettes (see data/trainers/palettes.asm)
; - BTTrainerClassSprites (see data/trainers/sprites.asm)
; - BTTrainerClassGenders (see data/trainers/genders.asm)
; trainer constants are Trainers indexes, for the sub-tables of TrainerGroups (see data/trainers/parties.asm)
DEF CHRIS EQU __trainer_class__
	trainerclass TRAINER_NONE ; 0
	const PHONECONTACT_MOM
	const PHONECONTACT_BIKESHOP
	const PHONECONTACT_BILL
	const PHONECONTACT_ELM
	const PHONECONTACT_BUENA
DEF NUM_NONTRAINER_PHONECONTACTS EQU const_value - 1

DEF KRIS EQU __trainer_class__
	trainerclass FALKNER ; 1

	trainerclass WHITNEY ; 2

	trainerclass BUGSY ; 3

	trainerclass MORTY ; 4

	trainerclass PRYCE ; 5

	trainerclass JASMINE ; 6

	trainerclass CHUCK ; 7

	trainerclass CLAIR ; 8

	trainerclass RIVAL1 ; 9
	const RIVAL1_1_CHIKORITA
	const RIVAL1_1_CYNDAQUIL
	const RIVAL1_1_TOTODILE
	const RIVAL1_2_CHIKORITA
	const RIVAL1_2_CYNDAQUIL
	const RIVAL1_2_TOTODILE
	const RIVAL1_3_CHIKORITA
	const RIVAL1_3_CYNDAQUIL
	const RIVAL1_3_TOTODILE
	const RIVAL1_4_CHIKORITA
	const RIVAL1_4_CYNDAQUIL
	const RIVAL1_4_TOTODILE
	const RIVAL1_5_CHIKORITA
	const RIVAL1_5_CYNDAQUIL
	const RIVAL1_5_TOTODILE

	trainerclass POKEMON_PROF ; a

	trainerclass WILL ; b

	trainerclass CAL ; c
	const CAL2

	trainerclass BRUNO ; d

	trainerclass KAREN ; e

	trainerclass KOGA ; f

	trainerclass CHAMPION ; 10
	const LANCE

	trainerclass BROCK ; 11

	trainerclass MISTY ; 12

	trainerclass LT_SURGE ; 13

	trainerclass SCIENTIST ; 14
	const JED

	trainerclass ERIKA ; 15

	trainerclass YOUNGSTER ; 16
	const JOEY1
	const MIKEY
	const ALBERT
	const GORDON
	const SAMUEL
	const IAN
	const JOEY2
	const JOEY3
	const WARREN
	const JIMMY
	const OWEN
	const JASON
	const JOEY4
	const JOEY5
	const TIMMY

	trainerclass SCHOOLBOY ; 17
	const NATE

	trainerclass BIRD_KEEPER ; 18
	const ROD
	const TOBY
	const HANK
	const ROY

	trainerclass LASS ; 19
	const LAURA

	trainerclass JANINE ; 1a

	trainerclass COOLTRAINERM ; 1b
	const NICK
	const PAUL
	const JAKE
	const BLAKE
	const SEAN

	trainerclass COOLTRAINERF ; 1c
	const LOLA
	const KATE
	const JOYCE
	const QUINN
	const EMMA
	const CARA

	trainerclass BEAUTY ; 1d
	const BRENDA ; unused

	trainerclass POKEMANIAC ; 1e
	const LARRY
	const BEN

	trainerclass GRUNTM ; 1f

	trainerclass GENTLEMAN ; 20

	trainerclass SKIER ; 21

	trainerclass TEACHER ; 22

	trainerclass SABRINA ; 23

	trainerclass BUG_CATCHER ; 24
	const DON
	const ROB
	const ED
	const KEN
	const DOUG

	trainerclass FISHER ; 25
	const ANDRE

	trainerclass SWIMMERM ; 26
	const KIRK
	const TONY ; unused
	const RICK ; unused
	const SETH

	trainerclass SWIMMERF ; 27
	const LISA ; unused
	const JILL ; unused
	const MARY ; unused
	const DAWN
	const TARA ; unused
	const LORI
	const DIANA

	trainerclass SAILOR ; 28

	trainerclass SUPER_NERD ; 29
	const STAN
	const ERIC
	const JAY ; unused
	const SAM
	const TOM
	const PAT
	const TERU
	const RUSS ; unused
	const HUGH

	trainerclass RIVAL2 ; 2a
	const RIVAL2_2_CHIKORITA

	trainerclass GUITARIST ; 2b
	const CLYDE

	trainerclass HIKER ; 2c
	const ERIK
	const TIM
	const JIM

	trainerclass BIKER ; 2d
	const DWAYNE

	trainerclass BLAINE ; 2e

	trainerclass BURGLAR ; 2f

	trainerclass FIREBREATHER ; 30
	const NED ; unused
	const BILL
	const WALT
	const RAY
	const LYLE

	trainerclass JUGGLER ; 31

	trainerclass BLACKBELT_T ; 32
	const NOB

	trainerclass EXECUTIVEM ; 33

	trainerclass PSYCHIC_T ; 34
	const GREG
	const PHIL

	trainerclass PICNICKER ; 35
	const KIM
	const HOPE
	const HEIDI
	const EDNA

	trainerclass CAMPER ; 36
	const BARRY
	const SID
	const DALE ; unused
	const TED
	const THOMAS ; unused

	trainerclass EXECUTIVEF ; 37

	trainerclass SAGE ; 38

	trainerclass MEDIUM ; 39
	const GRACE

	trainerclass BOARDER ; 3a
	const BRAD

	trainerclass POKEFANM ; 3b
	const REX
	const ALLAN

	trainerclass KIMONO_GIRL ; 3c
	const NAOKO

	trainerclass TWINS ; 3d

	trainerclass POKEFANF ; 3e
	const RUTH

	trainerclass RED ; 3f

	trainerclass BLUE ; 40

	trainerclass OFFICER ; 41
	const DIRK

	trainerclass GRUNTF ; 42

	trainerclass MYSTICALMAN ; 43

; HC-CLASSES begin
	trainerclass T_COP ; 44
	trainerclass T_SUIT ; 45
	trainerclass T_HOODIE ; 46
	trainerclass T_BANKER ; 47
	trainerclass T_CHOIR ; 48
	trainerclass T_THUG ; 49
	trainerclass T_PRIEST ; 4a
	trainerclass T_NUN ; 4b
	trainerclass T_BEGGAR ; 4c
	trainerclass T_ALTARBOY ; 4d
	trainerclass T_PUNK ; 4e
	trainerclass T_SISTER ; 4f
	trainerclass T_DRIFTER ; 50
	trainerclass T_ENFORCER ; 51
	trainerclass T_BUSKER ; 52
	trainerclass T_ACCOUNTANT ; 53
	trainerclass T_DEACON ; 54
	trainerclass T_COPCHIEF ; 55
	trainerclass T_MONSIGNOR ; 56
	trainerclass T_STEINER ; 57
	trainerclass T_CROWLEY ; 58
	trainerclass G_HIKER ; 59
	trainerclass G_SCOUT ; 5a
	trainerclass G_SPROUT ; 5b
	trainerclass G_URCHIN ; 5c
	trainerclass G_ANGLER ; 5d
	trainerclass G_FLOWERKID ; 5e
	trainerclass G_ELDER ; 5f
	trainerclass G_GRANNY ; 60
	trainerclass G_SHAMAN ; 61
	trainerclass G_DRUIDESS ; 62
	trainerclass G_NATURISTM ; 63
	trainerclass G_NATURISTF ; 64
	trainerclass G_DRUMMER ; 65
	trainerclass G_BARD ; 66
	trainerclass G_FORAGER ; 67
	trainerclass G_BIRDER ; 68
	trainerclass G_REEVE ; 69
	trainerclass G_ELDRESS ; 6a
	trainerclass G_MATRIARCH ; 6b
	trainerclass U_DOCTOR ; 6c
	trainerclass U_BOT ; 6d
	trainerclass U_DRONE ; 6e
	trainerclass U_BOTCOP ; 6f
	trainerclass U_EXEC ; 70
	trainerclass U_MATCHMAKER ; 71
	trainerclass U_SERF ; 72
	trainerclass U_GUARD ; 73
	trainerclass U_SERFF ; 74
	trainerclass U_CASEWORKER ; 75
	trainerclass U_WARDBOT ; 76
	trainerclass U_MADDOC ; 77
	trainerclass U_COURIER ; 78
	trainerclass U_MAYOR ; 79
	trainerclass U_SABBAH ; 7a
	trainerclass U_SUHRAWARDI ; 7b
	trainerclass L_SUNBATHER ; 7c
	trainerclass L_SWIMMERM ; 7d
	trainerclass L_SWIMMERF ; 7e
	trainerclass L_SAILOR ; 7f
	trainerclass L_MANAGER ; 80
	trainerclass L_TOURISTF ; 81
	trainerclass L_BEACHBUM ; 82
	trainerclass L_LIFEGUARD ; 83
	trainerclass L_FORGOTTEN ; 84
	trainerclass L_CLINICIAN ; 85
	trainerclass L_WAITER ; 86
	trainerclass L_TOURISTG ; 87
	trainerclass L_TOURISTM ; 88
	trainerclass L_BELLHOP ; 89
	trainerclass L_LOUNGER ; 8a
	trainerclass L_CIORAN ; 8b
	trainerclass D_BRUTE ; 8c
	trainerclass D_SHADE ; 8d
	trainerclass D_HAG ; 8e
	trainerclass D_JUDGE ; 8f
	trainerclass D_IMP ; 90
	trainerclass D_FIREEATER ; 91
	trainerclass D_JESTER ; 92
	trainerclass D_WARDEN ; 93
	trainerclass D_IMPF ; 94
	trainerclass D_DAMNED ; 95
	trainerclass D_MAGISTRATE ; 96
	trainerclass D_CRONE ; 97
	trainerclass D_SINNER ; 98
	trainerclass D_BRAWLER ; 99
	trainerclass D_IMPB ; 9a
	trainerclass D_SPECTRE ; 9b
	trainerclass D_DEMON ; 9c
	trainerclass D_FINNEGAN ; 9d
	trainerclass D_SADRA ; 9e
	trainerclass D_QADI ; 9f
; HC-CLASSES end
DEF NUM_TRAINER_CLASSES EQU __trainer_class__ - 1
