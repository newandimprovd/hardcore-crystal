; Footprints are 2x2 tiles each, but are stored as a 16x64-tile image
; (32 rows of 8 footprints per row).
; That means there's a row of the top two tiles for eight footprints,
; then a row of the bottom two tiles for those eight footprints.

; These macros help extract the first and the last two tiles, respectively.
DEF footprint_top    EQUS "0,                  2 * TILE_1BPP_SIZE"
DEF footprint_bottom EQUS "2 * TILE_1BPP_SIZE, 2 * TILE_1BPP_SIZE"

Footprints:
; Entries correspond to Pokémon species, two apiece, 8 tops then 8 bottoms
	table_width TILE_1BPP_SIZE * 4

; 001-008 top halves
INCBIN "gfx/footprints/bulbasaur.1bpp", footprint_top
INCBIN "gfx/footprints/ivysaur.1bpp", footprint_top
INCBIN "gfx/footprints/venusaur.1bpp", footprint_top
INCBIN "gfx/footprints/charmander.1bpp", footprint_top
INCBIN "gfx/footprints/charmeleon.1bpp", footprint_top
INCBIN "gfx/footprints/charizard.1bpp", footprint_top
INCBIN "gfx/footprints/squirtle.1bpp", footprint_top
INCBIN "gfx/footprints/wartortle.1bpp", footprint_top
; 001-008 bottom halves
INCBIN "gfx/footprints/bulbasaur.1bpp", footprint_bottom
INCBIN "gfx/footprints/ivysaur.1bpp", footprint_bottom
INCBIN "gfx/footprints/venusaur.1bpp", footprint_bottom
INCBIN "gfx/footprints/charmander.1bpp", footprint_bottom
INCBIN "gfx/footprints/charmeleon.1bpp", footprint_bottom
INCBIN "gfx/footprints/charizard.1bpp", footprint_bottom
INCBIN "gfx/footprints/squirtle.1bpp", footprint_bottom
INCBIN "gfx/footprints/wartortle.1bpp", footprint_bottom
; 009-016 top halves
INCBIN "gfx/footprints/blastoise.1bpp", footprint_top
INCBIN "gfx/footprints/caterpie.1bpp", footprint_top
INCBIN "gfx/footprints/metapod.1bpp", footprint_top
INCBIN "gfx/footprints/butterfree.1bpp", footprint_top
INCBIN "gfx/footprints/weedle.1bpp", footprint_top
INCBIN "gfx/footprints/kakuna.1bpp", footprint_top
INCBIN "gfx/footprints/beedrill.1bpp", footprint_top
INCBIN "gfx/footprints/pidgey.1bpp", footprint_top
; 009-016 bottom halves
INCBIN "gfx/footprints/blastoise.1bpp", footprint_bottom
INCBIN "gfx/footprints/caterpie.1bpp", footprint_bottom
INCBIN "gfx/footprints/metapod.1bpp", footprint_bottom
INCBIN "gfx/footprints/butterfree.1bpp", footprint_bottom
INCBIN "gfx/footprints/weedle.1bpp", footprint_bottom
INCBIN "gfx/footprints/kakuna.1bpp", footprint_bottom
INCBIN "gfx/footprints/beedrill.1bpp", footprint_bottom
INCBIN "gfx/footprints/pidgey.1bpp", footprint_bottom
; 017-024 top halves
INCBIN "gfx/footprints/pidgeotto.1bpp", footprint_top
INCBIN "gfx/footprints/pidgeot.1bpp", footprint_top
INCBIN "gfx/footprints/rattata.1bpp", footprint_top
INCBIN "gfx/footprints/raticate.1bpp", footprint_top
INCBIN "gfx/footprints/spearow.1bpp", footprint_top
INCBIN "gfx/footprints/fearow.1bpp", footprint_top
INCBIN "gfx/footprints/ekans.1bpp", footprint_top
INCBIN "gfx/footprints/arbok.1bpp", footprint_top
; 017-024 bottom halves
INCBIN "gfx/footprints/pidgeotto.1bpp", footprint_bottom
INCBIN "gfx/footprints/pidgeot.1bpp", footprint_bottom
INCBIN "gfx/footprints/rattata.1bpp", footprint_bottom
INCBIN "gfx/footprints/raticate.1bpp", footprint_bottom
INCBIN "gfx/footprints/spearow.1bpp", footprint_bottom
INCBIN "gfx/footprints/fearow.1bpp", footprint_bottom
INCBIN "gfx/footprints/ekans.1bpp", footprint_bottom
INCBIN "gfx/footprints/arbok.1bpp", footprint_bottom
; 025-032 top halves
INCBIN "gfx/footprints/pikachu.1bpp", footprint_top
INCBIN "gfx/footprints/raichu.1bpp", footprint_top
INCBIN "gfx/footprints/meganium.1bpp", footprint_top
INCBIN "gfx/footprints/typhlosion.1bpp", footprint_top
INCBIN "gfx/footprints/nidoran_f.1bpp", footprint_top
INCBIN "gfx/footprints/nidorina.1bpp", footprint_top
INCBIN "gfx/footprints/nidoqueen.1bpp", footprint_top
INCBIN "gfx/footprints/nidoran_m.1bpp", footprint_top
; 025-032 bottom halves
INCBIN "gfx/footprints/pikachu.1bpp", footprint_bottom
INCBIN "gfx/footprints/raichu.1bpp", footprint_bottom
INCBIN "gfx/footprints/meganium.1bpp", footprint_bottom
INCBIN "gfx/footprints/typhlosion.1bpp", footprint_bottom
INCBIN "gfx/footprints/nidoran_f.1bpp", footprint_bottom
INCBIN "gfx/footprints/nidorina.1bpp", footprint_bottom
INCBIN "gfx/footprints/nidoqueen.1bpp", footprint_bottom
INCBIN "gfx/footprints/nidoran_m.1bpp", footprint_bottom
; 033-040 top halves
INCBIN "gfx/footprints/nidorino.1bpp", footprint_top
INCBIN "gfx/footprints/nidoking.1bpp", footprint_top
INCBIN "gfx/footprints/clefairy.1bpp", footprint_top
INCBIN "gfx/footprints/clefable.1bpp", footprint_top
INCBIN "gfx/footprints/vulpix.1bpp", footprint_top
INCBIN "gfx/footprints/ninetales.1bpp", footprint_top
INCBIN "gfx/footprints/jigglypuff.1bpp", footprint_top
INCBIN "gfx/footprints/wigglytuff.1bpp", footprint_top
; 033-040 bottom halves
INCBIN "gfx/footprints/nidorino.1bpp", footprint_bottom
INCBIN "gfx/footprints/nidoking.1bpp", footprint_bottom
INCBIN "gfx/footprints/clefairy.1bpp", footprint_bottom
INCBIN "gfx/footprints/clefable.1bpp", footprint_bottom
INCBIN "gfx/footprints/vulpix.1bpp", footprint_bottom
INCBIN "gfx/footprints/ninetales.1bpp", footprint_bottom
INCBIN "gfx/footprints/jigglypuff.1bpp", footprint_bottom
INCBIN "gfx/footprints/wigglytuff.1bpp", footprint_bottom
; 041-048 top halves
INCBIN "gfx/footprints/zubat.1bpp", footprint_top
INCBIN "gfx/footprints/golbat.1bpp", footprint_top
INCBIN "gfx/footprints/oddish.1bpp", footprint_top
INCBIN "gfx/footprints/gloom.1bpp", footprint_top
INCBIN "gfx/footprints/feraligatr.1bpp", footprint_top
INCBIN "gfx/footprints/paras.1bpp", footprint_top
INCBIN "gfx/footprints/parasect.1bpp", footprint_top
INCBIN "gfx/footprints/venonat.1bpp", footprint_top
; 041-048 bottom halves
INCBIN "gfx/footprints/zubat.1bpp", footprint_bottom
INCBIN "gfx/footprints/golbat.1bpp", footprint_bottom
INCBIN "gfx/footprints/oddish.1bpp", footprint_bottom
INCBIN "gfx/footprints/gloom.1bpp", footprint_bottom
INCBIN "gfx/footprints/feraligatr.1bpp", footprint_bottom
INCBIN "gfx/footprints/paras.1bpp", footprint_bottom
INCBIN "gfx/footprints/parasect.1bpp", footprint_bottom
INCBIN "gfx/footprints/venonat.1bpp", footprint_bottom
; 049-056 top halves
INCBIN "gfx/footprints/venomoth.1bpp", footprint_top
INCBIN "gfx/footprints/venusaur.1bpp", footprint_top
INCBIN "gfx/footprints/charizard.1bpp", footprint_top
INCBIN "gfx/footprints/meowth.1bpp", footprint_top
INCBIN "gfx/footprints/persian.1bpp", footprint_top
INCBIN "gfx/footprints/psyduck.1bpp", footprint_top
INCBIN "gfx/footprints/golduck.1bpp", footprint_top
INCBIN "gfx/footprints/mankey.1bpp", footprint_top
; 049-056 bottom halves
INCBIN "gfx/footprints/venomoth.1bpp", footprint_bottom
INCBIN "gfx/footprints/venusaur.1bpp", footprint_bottom
INCBIN "gfx/footprints/charizard.1bpp", footprint_bottom
INCBIN "gfx/footprints/meowth.1bpp", footprint_bottom
INCBIN "gfx/footprints/persian.1bpp", footprint_bottom
INCBIN "gfx/footprints/psyduck.1bpp", footprint_bottom
INCBIN "gfx/footprints/golduck.1bpp", footprint_bottom
INCBIN "gfx/footprints/mankey.1bpp", footprint_bottom
; 057-064 top halves
INCBIN "gfx/footprints/primeape.1bpp", footprint_top
INCBIN "gfx/footprints/growlithe.1bpp", footprint_top
INCBIN "gfx/footprints/arcanine.1bpp", footprint_top
INCBIN "gfx/footprints/poliwag.1bpp", footprint_top
INCBIN "gfx/footprints/poliwhirl.1bpp", footprint_top
INCBIN "gfx/footprints/poliwrath.1bpp", footprint_top
INCBIN "gfx/footprints/abra.1bpp", footprint_top
INCBIN "gfx/footprints/kadabra.1bpp", footprint_top
; 057-064 bottom halves
INCBIN "gfx/footprints/primeape.1bpp", footprint_bottom
INCBIN "gfx/footprints/growlithe.1bpp", footprint_bottom
INCBIN "gfx/footprints/arcanine.1bpp", footprint_bottom
INCBIN "gfx/footprints/poliwag.1bpp", footprint_bottom
INCBIN "gfx/footprints/poliwhirl.1bpp", footprint_bottom
INCBIN "gfx/footprints/poliwrath.1bpp", footprint_bottom
INCBIN "gfx/footprints/abra.1bpp", footprint_bottom
INCBIN "gfx/footprints/kadabra.1bpp", footprint_bottom
; 065-072 top halves
INCBIN "gfx/footprints/alakazam.1bpp", footprint_top
INCBIN "gfx/footprints/machop.1bpp", footprint_top
INCBIN "gfx/footprints/machoke.1bpp", footprint_top
INCBIN "gfx/footprints/machamp.1bpp", footprint_top
INCBIN "gfx/footprints/bellsprout.1bpp", footprint_top
INCBIN "gfx/footprints/weepinbell.1bpp", footprint_top
INCBIN "gfx/footprints/victreebel.1bpp", footprint_top
INCBIN "gfx/footprints/tentacool.1bpp", footprint_top
; 065-072 bottom halves
INCBIN "gfx/footprints/alakazam.1bpp", footprint_bottom
INCBIN "gfx/footprints/machop.1bpp", footprint_bottom
INCBIN "gfx/footprints/machoke.1bpp", footprint_bottom
INCBIN "gfx/footprints/machamp.1bpp", footprint_bottom
INCBIN "gfx/footprints/bellsprout.1bpp", footprint_bottom
INCBIN "gfx/footprints/weepinbell.1bpp", footprint_bottom
INCBIN "gfx/footprints/victreebel.1bpp", footprint_bottom
INCBIN "gfx/footprints/tentacool.1bpp", footprint_bottom
; 073-080 top halves
INCBIN "gfx/footprints/tentacruel.1bpp", footprint_top
INCBIN "gfx/footprints/geodude.1bpp", footprint_top
INCBIN "gfx/footprints/graveler.1bpp", footprint_top
INCBIN "gfx/footprints/golem.1bpp", footprint_top
INCBIN "gfx/footprints/ponyta.1bpp", footprint_top
INCBIN "gfx/footprints/rapidash.1bpp", footprint_top
INCBIN "gfx/footprints/slowpoke.1bpp", footprint_top
INCBIN "gfx/footprints/slowbro.1bpp", footprint_top
; 073-080 bottom halves
INCBIN "gfx/footprints/tentacruel.1bpp", footprint_bottom
INCBIN "gfx/footprints/geodude.1bpp", footprint_bottom
INCBIN "gfx/footprints/graveler.1bpp", footprint_bottom
INCBIN "gfx/footprints/golem.1bpp", footprint_bottom
INCBIN "gfx/footprints/ponyta.1bpp", footprint_bottom
INCBIN "gfx/footprints/rapidash.1bpp", footprint_bottom
INCBIN "gfx/footprints/slowpoke.1bpp", footprint_bottom
INCBIN "gfx/footprints/slowbro.1bpp", footprint_bottom
; 081-088 top halves
INCBIN "gfx/footprints/magnemite.1bpp", footprint_top
INCBIN "gfx/footprints/magneton.1bpp", footprint_top
INCBIN "gfx/footprints/blastoise.1bpp", footprint_top
INCBIN "gfx/footprints/furret.1bpp", footprint_top
INCBIN "gfx/footprints/furret.1bpp", footprint_top
INCBIN "gfx/footprints/seel.1bpp", footprint_top
INCBIN "gfx/footprints/dewgong.1bpp", footprint_top
INCBIN "gfx/footprints/grimer.1bpp", footprint_top
; 081-088 bottom halves
INCBIN "gfx/footprints/magnemite.1bpp", footprint_bottom
INCBIN "gfx/footprints/magneton.1bpp", footprint_bottom
INCBIN "gfx/footprints/blastoise.1bpp", footprint_bottom
INCBIN "gfx/footprints/furret.1bpp", footprint_bottom
INCBIN "gfx/footprints/furret.1bpp", footprint_bottom
INCBIN "gfx/footprints/seel.1bpp", footprint_bottom
INCBIN "gfx/footprints/dewgong.1bpp", footprint_bottom
INCBIN "gfx/footprints/grimer.1bpp", footprint_bottom
; 089-096 top halves
INCBIN "gfx/footprints/muk.1bpp", footprint_top
INCBIN "gfx/footprints/shellder.1bpp", footprint_top
INCBIN "gfx/footprints/cloyster.1bpp", footprint_top
INCBIN "gfx/footprints/gastly.1bpp", footprint_top
INCBIN "gfx/footprints/haunter.1bpp", footprint_top
INCBIN "gfx/footprints/gengar.1bpp", footprint_top
INCBIN "gfx/footprints/onix.1bpp", footprint_top
INCBIN "gfx/footprints/drowzee.1bpp", footprint_top
; 089-096 bottom halves
INCBIN "gfx/footprints/muk.1bpp", footprint_bottom
INCBIN "gfx/footprints/shellder.1bpp", footprint_bottom
INCBIN "gfx/footprints/cloyster.1bpp", footprint_bottom
INCBIN "gfx/footprints/gastly.1bpp", footprint_bottom
INCBIN "gfx/footprints/haunter.1bpp", footprint_bottom
INCBIN "gfx/footprints/gengar.1bpp", footprint_bottom
INCBIN "gfx/footprints/onix.1bpp", footprint_bottom
INCBIN "gfx/footprints/drowzee.1bpp", footprint_bottom
; 097-104 top halves
INCBIN "gfx/footprints/hypno.1bpp", footprint_top
INCBIN "gfx/footprints/krabby.1bpp", footprint_top
INCBIN "gfx/footprints/kingler.1bpp", footprint_top
INCBIN "gfx/footprints/noctowl.1bpp", footprint_top
INCBIN "gfx/footprints/noctowl.1bpp", footprint_top
INCBIN "gfx/footprints/raticate.1bpp", footprint_top
INCBIN "gfx/footprints/raticate.1bpp", footprint_top
INCBIN "gfx/footprints/cubone.1bpp", footprint_top
; 097-104 bottom halves
INCBIN "gfx/footprints/hypno.1bpp", footprint_bottom
INCBIN "gfx/footprints/krabby.1bpp", footprint_bottom
INCBIN "gfx/footprints/kingler.1bpp", footprint_bottom
INCBIN "gfx/footprints/noctowl.1bpp", footprint_bottom
INCBIN "gfx/footprints/noctowl.1bpp", footprint_bottom
INCBIN "gfx/footprints/raticate.1bpp", footprint_bottom
INCBIN "gfx/footprints/raticate.1bpp", footprint_bottom
INCBIN "gfx/footprints/cubone.1bpp", footprint_bottom
; 105-112 top halves
INCBIN "gfx/footprints/marowak.1bpp", footprint_top
INCBIN "gfx/footprints/pidgeot.1bpp", footprint_top
INCBIN "gfx/footprints/butterfree.1bpp", footprint_top
INCBIN "gfx/footprints/beedrill.1bpp", footprint_top
INCBIN "gfx/footprints/koffing.1bpp", footprint_top
INCBIN "gfx/footprints/weezing.1bpp", footprint_top
INCBIN "gfx/footprints/rhyhorn.1bpp", footprint_top
INCBIN "gfx/footprints/rhydon.1bpp", footprint_top
; 105-112 bottom halves
INCBIN "gfx/footprints/marowak.1bpp", footprint_bottom
INCBIN "gfx/footprints/pidgeot.1bpp", footprint_bottom
INCBIN "gfx/footprints/butterfree.1bpp", footprint_bottom
INCBIN "gfx/footprints/beedrill.1bpp", footprint_bottom
INCBIN "gfx/footprints/koffing.1bpp", footprint_bottom
INCBIN "gfx/footprints/weezing.1bpp", footprint_bottom
INCBIN "gfx/footprints/rhyhorn.1bpp", footprint_bottom
INCBIN "gfx/footprints/rhydon.1bpp", footprint_bottom
; 113-120 top halves
INCBIN "gfx/footprints/chansey.1bpp", footprint_top
INCBIN "gfx/footprints/jumpluff.1bpp", footprint_top
INCBIN "gfx/footprints/fearow.1bpp", footprint_top
INCBIN "gfx/footprints/horsea.1bpp", footprint_top
INCBIN "gfx/footprints/seadra.1bpp", footprint_top
INCBIN "gfx/footprints/fearow.1bpp", footprint_top
INCBIN "gfx/footprints/arbok.1bpp", footprint_top
INCBIN "gfx/footprints/staryu.1bpp", footprint_top
; 113-120 bottom halves
INCBIN "gfx/footprints/chansey.1bpp", footprint_bottom
INCBIN "gfx/footprints/jumpluff.1bpp", footprint_bottom
INCBIN "gfx/footprints/fearow.1bpp", footprint_bottom
INCBIN "gfx/footprints/horsea.1bpp", footprint_bottom
INCBIN "gfx/footprints/seadra.1bpp", footprint_bottom
INCBIN "gfx/footprints/fearow.1bpp", footprint_bottom
INCBIN "gfx/footprints/arbok.1bpp", footprint_bottom
INCBIN "gfx/footprints/staryu.1bpp", footprint_bottom
; 121-128 top halves
INCBIN "gfx/footprints/starmie.1bpp", footprint_top
INCBIN "gfx/footprints/arbok.1bpp", footprint_top
INCBIN "gfx/footprints/scyther.1bpp", footprint_top
INCBIN "gfx/footprints/jynx.1bpp", footprint_top
INCBIN "gfx/footprints/raichu.1bpp", footprint_top
INCBIN "gfx/footprints/clefable.1bpp", footprint_top
INCBIN "gfx/footprints/wigglytuff.1bpp", footprint_top
INCBIN "gfx/footprints/nidoqueen.1bpp", footprint_top
; 121-128 bottom halves
INCBIN "gfx/footprints/starmie.1bpp", footprint_bottom
INCBIN "gfx/footprints/arbok.1bpp", footprint_bottom
INCBIN "gfx/footprints/scyther.1bpp", footprint_bottom
INCBIN "gfx/footprints/jynx.1bpp", footprint_bottom
INCBIN "gfx/footprints/raichu.1bpp", footprint_bottom
INCBIN "gfx/footprints/clefable.1bpp", footprint_bottom
INCBIN "gfx/footprints/wigglytuff.1bpp", footprint_bottom
INCBIN "gfx/footprints/nidoqueen.1bpp", footprint_bottom
; 129-136 top halves
INCBIN "gfx/footprints/magikarp.1bpp", footprint_top
INCBIN "gfx/footprints/gyarados.1bpp", footprint_top
INCBIN "gfx/footprints/nidoking.1bpp", footprint_top
INCBIN "gfx/footprints/crobat.1bpp", footprint_top
INCBIN "gfx/footprints/bellossom.1bpp", footprint_top
INCBIN "gfx/footprints/victreebel.1bpp", footprint_top
INCBIN "gfx/footprints/parasect.1bpp", footprint_top
INCBIN "gfx/footprints/parasect.1bpp", footprint_top
; 129-136 bottom halves
INCBIN "gfx/footprints/magikarp.1bpp", footprint_bottom
INCBIN "gfx/footprints/gyarados.1bpp", footprint_bottom
INCBIN "gfx/footprints/nidoking.1bpp", footprint_bottom
INCBIN "gfx/footprints/crobat.1bpp", footprint_bottom
INCBIN "gfx/footprints/bellossom.1bpp", footprint_bottom
INCBIN "gfx/footprints/victreebel.1bpp", footprint_bottom
INCBIN "gfx/footprints/parasect.1bpp", footprint_bottom
INCBIN "gfx/footprints/parasect.1bpp", footprint_bottom
; 137-144 top halves
INCBIN "gfx/footprints/porygon.1bpp", footprint_top
INCBIN "gfx/footprints/venomoth.1bpp", footprint_top
INCBIN "gfx/footprints/venomoth.1bpp", footprint_top
INCBIN "gfx/footprints/ariados.1bpp", footprint_top
INCBIN "gfx/footprints/ariados.1bpp", footprint_top
INCBIN "gfx/footprints/persian.1bpp", footprint_top
INCBIN "gfx/footprints/persian.1bpp", footprint_top
INCBIN "gfx/footprints/golduck.1bpp", footprint_top
; 137-144 bottom halves
INCBIN "gfx/footprints/porygon.1bpp", footprint_bottom
INCBIN "gfx/footprints/venomoth.1bpp", footprint_bottom
INCBIN "gfx/footprints/venomoth.1bpp", footprint_bottom
INCBIN "gfx/footprints/ariados.1bpp", footprint_bottom
INCBIN "gfx/footprints/ariados.1bpp", footprint_bottom
INCBIN "gfx/footprints/persian.1bpp", footprint_bottom
INCBIN "gfx/footprints/persian.1bpp", footprint_bottom
INCBIN "gfx/footprints/golduck.1bpp", footprint_bottom
; 145-152 top halves
INCBIN "gfx/footprints/golduck.1bpp", footprint_top
INCBIN "gfx/footprints/primeape.1bpp", footprint_top
INCBIN "gfx/footprints/dratini.1bpp", footprint_top
INCBIN "gfx/footprints/dragonair.1bpp", footprint_top
INCBIN "gfx/footprints/dragonite.1bpp", footprint_top
INCBIN "gfx/footprints/primeape.1bpp", footprint_top
INCBIN "gfx/footprints/machamp.1bpp", footprint_top
INCBIN "gfx/footprints/chikorita.1bpp", footprint_top
; 145-152 bottom halves
INCBIN "gfx/footprints/golduck.1bpp", footprint_bottom
INCBIN "gfx/footprints/primeape.1bpp", footprint_bottom
INCBIN "gfx/footprints/dratini.1bpp", footprint_bottom
INCBIN "gfx/footprints/dragonair.1bpp", footprint_bottom
INCBIN "gfx/footprints/dragonite.1bpp", footprint_bottom
INCBIN "gfx/footprints/primeape.1bpp", footprint_bottom
INCBIN "gfx/footprints/machamp.1bpp", footprint_bottom
INCBIN "gfx/footprints/chikorita.1bpp", footprint_bottom
; 153-160 top halves
INCBIN "gfx/footprints/bayleef.1bpp", footprint_top
INCBIN "gfx/footprints/meganium.1bpp", footprint_top
INCBIN "gfx/footprints/cyndaquil.1bpp", footprint_top
INCBIN "gfx/footprints/quilava.1bpp", footprint_top
INCBIN "gfx/footprints/typhlosion.1bpp", footprint_top
INCBIN "gfx/footprints/totodile.1bpp", footprint_top
INCBIN "gfx/footprints/croconaw.1bpp", footprint_top
INCBIN "gfx/footprints/feraligatr.1bpp", footprint_top
; 153-160 bottom halves
INCBIN "gfx/footprints/bayleef.1bpp", footprint_bottom
INCBIN "gfx/footprints/meganium.1bpp", footprint_bottom
INCBIN "gfx/footprints/cyndaquil.1bpp", footprint_bottom
INCBIN "gfx/footprints/quilava.1bpp", footprint_bottom
INCBIN "gfx/footprints/typhlosion.1bpp", footprint_bottom
INCBIN "gfx/footprints/totodile.1bpp", footprint_bottom
INCBIN "gfx/footprints/croconaw.1bpp", footprint_bottom
INCBIN "gfx/footprints/feraligatr.1bpp", footprint_bottom
; 161-168 top halves
INCBIN "gfx/footprints/sentret.1bpp", footprint_top
INCBIN "gfx/footprints/furret.1bpp", footprint_top
INCBIN "gfx/footprints/hoothoot.1bpp", footprint_top
INCBIN "gfx/footprints/noctowl.1bpp", footprint_top
INCBIN "gfx/footprints/alakazam.1bpp", footprint_top
INCBIN "gfx/footprints/golem.1bpp", footprint_top
INCBIN "gfx/footprints/spinarak.1bpp", footprint_top
INCBIN "gfx/footprints/ariados.1bpp", footprint_top
; 161-168 bottom halves
INCBIN "gfx/footprints/sentret.1bpp", footprint_bottom
INCBIN "gfx/footprints/furret.1bpp", footprint_bottom
INCBIN "gfx/footprints/hoothoot.1bpp", footprint_bottom
INCBIN "gfx/footprints/noctowl.1bpp", footprint_bottom
INCBIN "gfx/footprints/alakazam.1bpp", footprint_bottom
INCBIN "gfx/footprints/golem.1bpp", footprint_bottom
INCBIN "gfx/footprints/spinarak.1bpp", footprint_bottom
INCBIN "gfx/footprints/ariados.1bpp", footprint_bottom
; 169-176 top halves
INCBIN "gfx/footprints/crobat.1bpp", footprint_top
INCBIN "gfx/footprints/steelix.1bpp", footprint_top
INCBIN "gfx/footprints/steelix.1bpp", footprint_top
INCBIN "gfx/footprints/pichu.1bpp", footprint_top
INCBIN "gfx/footprints/cleffa.1bpp", footprint_top
INCBIN "gfx/footprints/igglybuff.1bpp", footprint_top
INCBIN "gfx/footprints/arcanine.1bpp", footprint_top
INCBIN "gfx/footprints/arcanine.1bpp", footprint_top
; 169-176 bottom halves
INCBIN "gfx/footprints/crobat.1bpp", footprint_bottom
INCBIN "gfx/footprints/steelix.1bpp", footprint_bottom
INCBIN "gfx/footprints/steelix.1bpp", footprint_bottom
INCBIN "gfx/footprints/pichu.1bpp", footprint_bottom
INCBIN "gfx/footprints/cleffa.1bpp", footprint_bottom
INCBIN "gfx/footprints/igglybuff.1bpp", footprint_bottom
INCBIN "gfx/footprints/arcanine.1bpp", footprint_bottom
INCBIN "gfx/footprints/arcanine.1bpp", footprint_bottom
; 177-184 top halves
INCBIN "gfx/footprints/ninetales.1bpp", footprint_top
INCBIN "gfx/footprints/ninetales.1bpp", footprint_top
INCBIN "gfx/footprints/mareep.1bpp", footprint_top
INCBIN "gfx/footprints/flaaffy.1bpp", footprint_top
INCBIN "gfx/footprints/ampharos.1bpp", footprint_top
INCBIN "gfx/footprints/bellossom.1bpp", footprint_top
INCBIN "gfx/footprints/marill.1bpp", footprint_top
INCBIN "gfx/footprints/azumarill.1bpp", footprint_top
; 177-184 bottom halves
INCBIN "gfx/footprints/ninetales.1bpp", footprint_bottom
INCBIN "gfx/footprints/ninetales.1bpp", footprint_bottom
INCBIN "gfx/footprints/mareep.1bpp", footprint_bottom
INCBIN "gfx/footprints/flaaffy.1bpp", footprint_bottom
INCBIN "gfx/footprints/ampharos.1bpp", footprint_bottom
INCBIN "gfx/footprints/bellossom.1bpp", footprint_bottom
INCBIN "gfx/footprints/marill.1bpp", footprint_bottom
INCBIN "gfx/footprints/azumarill.1bpp", footprint_bottom
; 185-192 top halves
INCBIN "gfx/footprints/rapidash.1bpp", footprint_top
INCBIN "gfx/footprints/rapidash.1bpp", footprint_top
INCBIN "gfx/footprints/hoppip.1bpp", footprint_top
INCBIN "gfx/footprints/skiploom.1bpp", footprint_top
INCBIN "gfx/footprints/jumpluff.1bpp", footprint_top
INCBIN "gfx/footprints/houndoom.1bpp", footprint_top
INCBIN "gfx/footprints/houndoom.1bpp", footprint_top
INCBIN "gfx/footprints/ampharos.1bpp", footprint_top
; 185-192 bottom halves
INCBIN "gfx/footprints/rapidash.1bpp", footprint_bottom
INCBIN "gfx/footprints/rapidash.1bpp", footprint_bottom
INCBIN "gfx/footprints/hoppip.1bpp", footprint_bottom
INCBIN "gfx/footprints/skiploom.1bpp", footprint_bottom
INCBIN "gfx/footprints/jumpluff.1bpp", footprint_bottom
INCBIN "gfx/footprints/houndoom.1bpp", footprint_bottom
INCBIN "gfx/footprints/houndoom.1bpp", footprint_bottom
INCBIN "gfx/footprints/ampharos.1bpp", footprint_bottom
; 193-200 top halves
INCBIN "gfx/footprints/magneton.1bpp", footprint_top
INCBIN "gfx/footprints/magneton.1bpp", footprint_top
INCBIN "gfx/footprints/porygon2.1bpp", footprint_top
INCBIN "gfx/footprints/porygon2.1bpp", footprint_top
INCBIN "gfx/footprints/gengar.1bpp", footprint_top
INCBIN "gfx/footprints/marowak.1bpp", footprint_top
INCBIN "gfx/footprints/marowak.1bpp", footprint_top
INCBIN "gfx/footprints/muk.1bpp", footprint_top
; 193-200 bottom halves
INCBIN "gfx/footprints/magneton.1bpp", footprint_bottom
INCBIN "gfx/footprints/magneton.1bpp", footprint_bottom
INCBIN "gfx/footprints/porygon2.1bpp", footprint_bottom
INCBIN "gfx/footprints/porygon2.1bpp", footprint_bottom
INCBIN "gfx/footprints/gengar.1bpp", footprint_bottom
INCBIN "gfx/footprints/marowak.1bpp", footprint_bottom
INCBIN "gfx/footprints/marowak.1bpp", footprint_bottom
INCBIN "gfx/footprints/muk.1bpp", footprint_bottom
; 201-208 top halves
INCBIN "gfx/footprints/muk.1bpp", footprint_top
INCBIN "gfx/footprints/weezing.1bpp", footprint_top
INCBIN "gfx/footprints/weezing.1bpp", footprint_top
INCBIN "gfx/footprints/rhydon.1bpp", footprint_top
INCBIN "gfx/footprints/rhydon.1bpp", footprint_top
INCBIN "gfx/footprints/scizor.1bpp", footprint_top
INCBIN "gfx/footprints/scizor.1bpp", footprint_top
INCBIN "gfx/footprints/steelix.1bpp", footprint_top
; 201-208 bottom halves
INCBIN "gfx/footprints/muk.1bpp", footprint_bottom
INCBIN "gfx/footprints/weezing.1bpp", footprint_bottom
INCBIN "gfx/footprints/weezing.1bpp", footprint_bottom
INCBIN "gfx/footprints/rhydon.1bpp", footprint_bottom
INCBIN "gfx/footprints/rhydon.1bpp", footprint_bottom
INCBIN "gfx/footprints/scizor.1bpp", footprint_bottom
INCBIN "gfx/footprints/scizor.1bpp", footprint_bottom
INCBIN "gfx/footprints/steelix.1bpp", footprint_bottom
; 209-216 top halves
INCBIN "gfx/footprints/tentacruel.1bpp", footprint_top
INCBIN "gfx/footprints/tentacruel.1bpp", footprint_top
INCBIN "gfx/footprints/poliwrath.1bpp", footprint_top
INCBIN "gfx/footprints/scizor.1bpp", footprint_top
INCBIN "gfx/footprints/slowbro.1bpp", footprint_top
INCBIN "gfx/footprints/slowbro.1bpp", footprint_top
INCBIN "gfx/footprints/dewgong.1bpp", footprint_top
INCBIN "gfx/footprints/dewgong.1bpp", footprint_top
; 209-216 bottom halves
INCBIN "gfx/footprints/tentacruel.1bpp", footprint_bottom
INCBIN "gfx/footprints/tentacruel.1bpp", footprint_bottom
INCBIN "gfx/footprints/poliwrath.1bpp", footprint_bottom
INCBIN "gfx/footprints/scizor.1bpp", footprint_bottom
INCBIN "gfx/footprints/slowbro.1bpp", footprint_bottom
INCBIN "gfx/footprints/slowbro.1bpp", footprint_bottom
INCBIN "gfx/footprints/dewgong.1bpp", footprint_bottom
INCBIN "gfx/footprints/dewgong.1bpp", footprint_bottom
; 217-224 top halves
INCBIN "gfx/footprints/cloyster.1bpp", footprint_top
INCBIN "gfx/footprints/cloyster.1bpp", footprint_top
INCBIN "gfx/footprints/kingler.1bpp", footprint_top
INCBIN "gfx/footprints/swinub.1bpp", footprint_top
INCBIN "gfx/footprints/piloswine.1bpp", footprint_top
INCBIN "gfx/footprints/kingler.1bpp", footprint_top
INCBIN "gfx/footprints/starmie.1bpp", footprint_top
INCBIN "gfx/footprints/starmie.1bpp", footprint_top
; 217-224 bottom halves
INCBIN "gfx/footprints/cloyster.1bpp", footprint_bottom
INCBIN "gfx/footprints/cloyster.1bpp", footprint_bottom
INCBIN "gfx/footprints/kingler.1bpp", footprint_bottom
INCBIN "gfx/footprints/swinub.1bpp", footprint_bottom
INCBIN "gfx/footprints/piloswine.1bpp", footprint_bottom
INCBIN "gfx/footprints/kingler.1bpp", footprint_bottom
INCBIN "gfx/footprints/starmie.1bpp", footprint_bottom
INCBIN "gfx/footprints/starmie.1bpp", footprint_bottom
; 225-232 top halves
INCBIN "gfx/footprints/kingdra.1bpp", footprint_top
INCBIN "gfx/footprints/gyarados.1bpp", footprint_top
INCBIN "gfx/footprints/gyarados.1bpp", footprint_top
INCBIN "gfx/footprints/houndour.1bpp", footprint_top
INCBIN "gfx/footprints/houndoom.1bpp", footprint_top
INCBIN "gfx/footprints/kingdra.1bpp", footprint_top
INCBIN "gfx/footprints/azumarill.1bpp", footprint_top
INCBIN "gfx/footprints/azumarill.1bpp", footprint_top
; 225-232 bottom halves
INCBIN "gfx/footprints/kingdra.1bpp", footprint_bottom
INCBIN "gfx/footprints/gyarados.1bpp", footprint_bottom
INCBIN "gfx/footprints/gyarados.1bpp", footprint_bottom
INCBIN "gfx/footprints/houndour.1bpp", footprint_bottom
INCBIN "gfx/footprints/houndoom.1bpp", footprint_bottom
INCBIN "gfx/footprints/kingdra.1bpp", footprint_bottom
INCBIN "gfx/footprints/azumarill.1bpp", footprint_bottom
INCBIN "gfx/footprints/azumarill.1bpp", footprint_bottom
; 233-240 top halves
INCBIN "gfx/footprints/porygon2.1bpp", footprint_top
INCBIN "gfx/footprints/hypno.1bpp", footprint_top
INCBIN "gfx/footprints/hypno.1bpp", footprint_top
INCBIN "gfx/footprints/blissey.1bpp", footprint_top
INCBIN "gfx/footprints/blissey.1bpp", footprint_top
INCBIN "gfx/footprints/smoochum.1bpp", footprint_top
INCBIN "gfx/footprints/piloswine.1bpp", footprint_top
INCBIN "gfx/footprints/piloswine.1bpp", footprint_top
; 233-240 bottom halves
INCBIN "gfx/footprints/porygon2.1bpp", footprint_bottom
INCBIN "gfx/footprints/hypno.1bpp", footprint_bottom
INCBIN "gfx/footprints/hypno.1bpp", footprint_bottom
INCBIN "gfx/footprints/blissey.1bpp", footprint_bottom
INCBIN "gfx/footprints/blissey.1bpp", footprint_bottom
INCBIN "gfx/footprints/smoochum.1bpp", footprint_bottom
INCBIN "gfx/footprints/piloswine.1bpp", footprint_bottom
INCBIN "gfx/footprints/piloswine.1bpp", footprint_bottom
; 241-248 top halves
INCBIN "gfx/footprints/jynx.1bpp", footprint_top
INCBIN "gfx/footprints/blissey.1bpp", footprint_top
INCBIN "gfx/footprints/jynx.1bpp", footprint_top
INCBIN "gfx/footprints/dragonite.1bpp", footprint_top
INCBIN "gfx/footprints/tyranitar.1bpp", footprint_top
INCBIN "gfx/footprints/larvitar.1bpp", footprint_top
INCBIN "gfx/footprints/pupitar.1bpp", footprint_top
INCBIN "gfx/footprints/tyranitar.1bpp", footprint_top
; 241-248 bottom halves
INCBIN "gfx/footprints/jynx.1bpp", footprint_bottom
INCBIN "gfx/footprints/blissey.1bpp", footprint_bottom
INCBIN "gfx/footprints/jynx.1bpp", footprint_bottom
INCBIN "gfx/footprints/dragonite.1bpp", footprint_bottom
INCBIN "gfx/footprints/tyranitar.1bpp", footprint_bottom
INCBIN "gfx/footprints/larvitar.1bpp", footprint_bottom
INCBIN "gfx/footprints/pupitar.1bpp", footprint_bottom
INCBIN "gfx/footprints/tyranitar.1bpp", footprint_bottom
; 249-256 top halves
INCBIN "gfx/footprints/252.1bpp", footprint_top
INCBIN "gfx/footprints/252.1bpp", footprint_top
INCBIN "gfx/footprints/252.1bpp", footprint_top
INCBIN "gfx/footprints/252.1bpp", footprint_top
INCBIN "gfx/footprints/253.1bpp", footprint_top
INCBIN "gfx/footprints/254.1bpp", footprint_top
INCBIN "gfx/footprints/255.1bpp", footprint_top
INCBIN "gfx/footprints/256.1bpp", footprint_top
; 249-256 bottom halves
INCBIN "gfx/footprints/252.1bpp", footprint_bottom
INCBIN "gfx/footprints/252.1bpp", footprint_bottom
INCBIN "gfx/footprints/252.1bpp", footprint_bottom
INCBIN "gfx/footprints/252.1bpp", footprint_bottom
INCBIN "gfx/footprints/253.1bpp", footprint_bottom
INCBIN "gfx/footprints/254.1bpp", footprint_bottom
INCBIN "gfx/footprints/255.1bpp", footprint_bottom
INCBIN "gfx/footprints/256.1bpp", footprint_bottom

	assert_table_length $100
