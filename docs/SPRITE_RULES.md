# Sprite rules for the generated creatures

These are the rules the user gave for the sprites of the 97 new species, and how the generator under tools/hardcore/sprites follows them today. They are written down so the beta sprite pass starts from the same ground and nobody has to guess what was asked.

## The rules as given

Pokémon get their look from expressive eyes, and every one of them conveys itself through posture and face details. As a general rule a Pokémon gets bigger as it evolves. Kingpin, the last stage of the Meowth line, should be about four times bigger than Meowth. Fourth stages are bigger and more menacing than the stages before them, some of them centipedal with many limbs or chimeric like a centaur, and the sprites of all 97 new species ship in the beta. The user said they are unhappy with the sprites generally, and called the Alleycat sprite horrendous, so the standard to meet is a recognisable animal first and a menacing one second.

## How the generator follows them

Eyes live in `sprites/rig.py` and the mood of every species is a single table in `sprites/faces.py`. There are nine looks. Angry has a brow slanted down toward the nose and the pupil pulled to the same side. Sly is a smug squint with the lid climbing toward the outer corner. Tired has heavy lids and a bag under the eye. Round is a wide startled eye with a pin prick pupil. Addled has no lid and both pupils pushed toward the nose. Blank is white and lifeless, hollow is two black sockets, and slit and dot are the older animal looks that a few heads still use. Every eye is at least four pixels wide and five when the table marks the species as big eyed, so it still reads at the size of a Game Boy picture. Veterans such as Kingpin, Berserker, Headsman and Tyrant also carry a white scar across the brow.

Growth is handled twice. A stage 3 form is drawn with a silhouette that fills 76 percent of the canvas and a stage 4 form fills 97 percent, so the last form of a line is always the biggest thing in it. Every creature also stands on one shared ground line, one pixel above the bottom of the picture, so a small form sits low in the frame the way vanilla sprites do and the size difference between stages is visible instead of being hidden by automatic fitting. The vanilla forms before the new ones are smaller still.

Kingpin measures roughly 3.8 times the area of Meowth and about twice its length. A full four times in length would not fit the 56 by 56 picture, so the area figure is the honest reading of the rule.

Outlines go through a clean up pass in `sprites/toon.py` that removes the lone dither pixels the shading leaves behind, while eyes are left alone. The shading band is narrower than it was, which keeps edges crisp.

## What is still weak

Posture is shaped by the body plan and the recipe parameters and not by the mood table, so a tired creature and an angry one of the same plan still stand the same way. Cat and dog heads read alike from the front, which is why Kingpin looks like a bulldog with a coin on its head. A few palettes are garish, Alleycat's magenta most of all. Typhoneus and Hellhound come from imported author art and do not follow these tables at all. All of these are open for the beta pass.

## Rebuilding

`python3 tools/hardcore/sprites/gen.py all` rebuilds every generated species and skips the ones whose inputs have not changed. `gen.py sheet NAME ...` writes a contact sheet to the scratch folder. The tile budget is 49 changed tiles per picture and the build log prints the tile count of each species, which is currently never above 49.

## The player

Chris is drawn by `tools/hardcore/art/player.py` from the same figure code as the trainers. It writes the overworld sheet, the 56 by 56 front picture, the trainer card picture and the 48 by 48 battle back picture, so all four agree. He is a scruffy man with tired eyes in a jacket, with a duffel over one shoulder and a ball in his hand. Kris, the female player option, still has the vanilla art.
