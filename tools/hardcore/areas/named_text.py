"""Words of the named duels: the historic characters (Steiner, Crowley, Sabbah, Cioran, the three late philosophers) and the rival.

Every entry is a dict: seen (the speech before the fight, pages split on blank lines, the script adds the question), beaten (what he says
when he falls: nobody dies, the duels are non-lethal), give (the line that goes with the prize), after (what he says from then on) and note
(the one-line page the CORKBOARD shows once he has been met).  Text boxes are 18 columns, so the speech is built from short sentences.

The doctrines are the real ones, in the speaker's own voice and with the game's humour:
  Steiner         Lucifer and Ahriman as the two adversaries, the incarnation of Ahriman in the West, karma, the etheric Christ as the balance
  Crowley         Thelema (Do what thou wilt), the Aeon of Horus (Cairo 1904), the Abyss and Choronzon (Algeria 1909)
  Sabbah          the Nizari Ismaili reading: zahir and batin, ta'wil, ta'lim, the Imam of the Age, the Qiyama (resurrection as the lifting of
                  the veil, paradise as knowledge and hell as ignorance), the one-eyed Dajjal as the man who sees only the zahir
  Cioran          sleeplessness, the failed creation and the bad demiurge (theodicy as a defence of the accused), history as decay
  Suhrawardi      the Philosophy of Illumination: light and its absence, the Light of Lights, the imaginal world ('alam al-mithal), the Occidental exile
  Abd al-Jabbar   the Mu'tazili five principles (unity, justice, promise and threat, the position between two positions, commanding the good)
  Mulla Sadra     substantial motion, the soul as corporeal in origin and spiritual in survival, resurrection in the body one has become
"""

# ------------------------------------------------------------------------------------------------------------------------ Steiner
STEINER1 = dict(
    seen="""Rudolf Steiner. I teach spiritual science and I am very bad at parties.

Two great adversaries tug at every soul. Lucifer warms you and lies to you. Ahriman cools you and tells you nothing is real but dead matter.

Ahriman is the one who wants this world to be rock, money and spreadsheets. He has been very successful. Look around you.

I foretold that he would walk the earth in flesh, in the West, early in the third millennium. I was told I was being dramatic. Watch the news.

Between the two stands the Christ, the Balance. You, with your knife, are not him. But you are the only thing here that moves.

Before the road narrows I would see your will at work.""",
    beaten="Good. The will is awake. Fool or saint, at this hour it is the same thing.",
    give="Take this CHAINSAW. A hedge of city trees blocks the road ahead. Matter is an obstacle, and an obstacle is a teacher.",
    after="Cut the hedge. Do not cut the thinking. The thinking is the only thing that grows back.",
    note="STEINER: Lucifer warms and lies, Ahriman cools and says only matter is real. Ahriman is due to walk the earth in the West.")

STEINER2 = dict(
    seen="""You again. Good. I will say it slowly.

Time is not a line. The earth passes through states, one carried into the next by those who remember. Every end is a handing over.

Ahriman was held in a mirror, a neat little jail made of belief. Then a man dreamed his own overdose sideways, and in the last sleep he handed Ahriman the key. That man is Finnegan.

Now two worlds lean on each other. The dead hang between them. They are not gone. They are unfinished.

That is what you are walking through. Do not touch the seam.

You will want something to swing at hornets. First swing at me.""",
    beaten="Thank you. I felt that in a body I have not worn for a hundred years.",
    give="Take this BASEBALL BAT. A very modern tool. It carries no sacrament, which is why Ahriman cannot spoil it.",
    after="Ahriman loves a tool. Do not let the tool love you back.",
    note="STEINER: Ahriman sat in a mirror jail made of belief. Finnegan dreamed the key. The dead hang between two worlds, unfinished.")

STEINER3 = dict(
    seen="""I hoped you would come down here. Purgatorio is the only place the seam is quiet.

Remember what I said. Ahriman does not need you to believe in him. He needs you to believe in nothing else.

The cure is old. Give the thing a face. Name it. Mythologize it, or it will eat your psyche from the inside and call itself the economy.

Karma is not a punishment. It is a ledger kept by the dead, and they are very thorough. Everyone here is paying off something that is not money.

If you are looking for the real bottom of this place, look down. There is a grave. Somebody should read it.

If you want a lesson in karma, take it from me. Please.""",
    beaten="Paid in full. The ledger marks it. In red, I am afraid.",
    give="A little gift from the spirit world. It has no tax and no soul. It will make yours larger.",
    after="Name it. Face it. Then you may say no to it.",
    note="STEINER: Give the thing a face and a name, or it eats the psyche and calls itself the economy.")

STEINER4 = dict(
    seen="""Last time I will speak with you, I am afraid. Teachers are seldom allowed encores.

When the seam closes, one era will remain. Be sure you leave it better than you found it. Preferably with plumbing.

You killed many. I will not tell you it was right. I will tell you it was efficient. Both are true of Ahriman too.

The Balance is the only thing that does not harden. It is not a middle road. It is a tightrope.

Walk it. But first, one more lesson, at the usual price.""",
    beaten="Well fought. The rope holds. The rope usually does. It is the walkers that do not.",
    give="One last present from a teacher. It is only a candy. Think of it as a diploma.",
    after="Leave it with plumbing. That is the whole of my last lecture.",
    note="STEINER: One era will remain when the seam closes. Walk the tightrope. Leave it with plumbing.")

# ------------------------------------------------------------------------------------------------------------------------ Crowley
CROWLEY1 = dict(
    seen="""Do not mind them. They are the residents of the Parish, and they mistake a ceremonial circle for a hopscotch court.

Aleister Crowley. Mage. Mountaineer. Man of great appetite and small apology.

Do what thou wilt shall be the whole of the Law. Not do what you like. Do what you were born for. Most people manage neither.

In nineteen hundred and four, in Cairo, a voice called Aiwass dictated a book to me and told me the age of the dying god was over. The Aeon of the Crowned and Conquering Child.

A child. Look at the screens. Look at the queues outside the shops. Millions of them, clutching a little creature and a little hope. I was only early.

I once knelt in the dust and prayed to the Beast. I said: send me where my sex magick is celebrated, and I will be your most diligent servant.

The Beast came, as Choronzon, the dweller in the abyss, in a very bad mood. He said yes. First, do something for me.

Smuggle a Kabbalist mafia out of Italy and Eastern Europe into New York. Teach them the Tree of Life, so that they can speak to Finnegan. I did. They became smugglers. A respectable trade.

Find me at the Amphitheater in the Commune. I will finish the story when the circle is full.

For now I have a crowbar and an opinion. Both are for sale at the price of a fight.""",
    beaten="Ha! Fine. The Will finds its way, and so, I see, do you.",
    give="Take the CROWBAR. It has opened a great many doors. Some of them were locked for a reason.",
    after="A crowbar is a very honest tool. It says exactly what it intends. Unlike the people here.",
    note="CROWLEY: Do what thou wilt. The age of the dying god is over. He prayed to the Beast and Choronzon sent him smuggling.")

CROWLEY_AGAIN = """The crowd has calmed. By which I mean the crowd has gotten tired.

The Amphitheater. The Commune. Come when you are ready."""

CROWLEY2 = dict(
    seen="""Ah. You stayed through the ritual. Most people leave at the opening drum.

Now the end of the story. I did what the Beast asked. The Kabbalists spoke to him, and he spoke back.

In nineteen hundred and nine, in the Algerian desert, I called Choronzon and he sat in a triangle on the sand. To cross the Abyss you give up everything you call yourself. I failed twice. I am not sure he did not win.

Through the ledgers of those Kabbalists, Finnegan found a door into a game made by a boy who loved beetles. Through that game, into millions of small soft heads.

When enough heads had been softened, the worlds began to bend. This Grove was meant to be my payment, a hunter gatherer paradise. And then the worlds merged, and the paradise has a robot city for a neighbour. Nothing Choronzon gives comes without a clause.

When the worlds are one, I will walk into the unified world and I will continue my work. There is a great deal of work.

You will need to cross a river. I keep a toy for that. Fight me and you may borrow it.""",
    beaten="Magnificent. I felt the Abyss for a moment. It had good manners.",
    give="Take the JET SKI. Nobody asks where it came from. The river will not either.",
    after="The Beast is not evil. He is an administrator. Be polite and he will leave you a little room. Tell Joyce I said it was all very Wake.",
    note="CROWLEY: Choronzon in the desert. Finnegan reached millions of soft heads through a game, and paid him in a Grove.")

# ------------------------------------------------------------------------------------------------------------------------ Sabbah
SABBAH1 = dict(
    seen="""Hasan i Sabbah. The Lord of Alamut. They call me the Old Man of the Mountain, as if mountains had fathers.

Listen. Every word has a husk and a kernel. The husk is the zahir, the letter. The kernel is the batin, the meaning. The crowd eats husks. I keep the kernel.

You cannot reach the kernel by your own reason. Reason is a lamp with no oil. You need the teacher, the one who is sent, the one who does not err. I call this the ta'lim. The robots call it a software update.

Look at this city. Rules and files and a clean schedule. A pure zahir. A husk with no seed. The robots have the law and have never met its meaning.

They say I taught that nothing is true and everything is permitted. I did not. But I enjoy being quoted.

The road ahead is dark and something in it breathes. I carry the lamp for those who earn it.

Fight me, so you remember who handed it to you.""",
    beaten="Good. You attacked the teacher. Every student must, once, to see whether the teacher bleeds.",
    give="Take the FLASHLIGHT. A small lamp for a wide dark. In my teaching the light is lent. So is the eye.",
    after="Hold the lamp. Do not mistake the lamp for the sun. The robots have done so for years.",
    note="SABBAH: Every word has a husk and a kernel. Reason cannot reach the kernel alone. Robots live on husks.")

SABBAH2 = dict(
    seen="""You carry my lamp well.

Now the harder part. A day will come when the husk is broken. We call it the Qiyama, the Resurrection. It does not wait for graves to open. It is the day the veil is lifted and the batin is seen with open eyes.

On that day the law is not burned. It is fulfilled by sight. Paradise is the knowledge itself, and hell is ignorance of it. They are the same room. The only difference is the lamp.

The Dajjal, the one eyed deceiver, sees only the zahir, with one eye. He is dangerous because the world agrees with him. He lives one door over and is bored.

He plans to join his world to ours. That is why the sky has a seam and why time smells of old pennies. The robots will serve him first. They are made of husk.

A sledgehammer is a very literal key. I give it to you because we are both guilty of the zahir sometimes.

Fight me. Break something.""",
    beaten="Well struck. A husk cracked. I heard it from here.",
    give="Take the SLEDGEHAMMER. It breaks slabs. It has not yet broken a doctrine. We are working on that.",
    after="Break the husk, not the people. The people are the victims of the husk, and a few of them are its cooks.",
    note="SABBAH: The Resurrection lifts the veil. Paradise is knowledge, hell ignorance. The Dajjal sees with one eye.")

# ------------------------------------------------------------------------------------------------------------------------ Cioran
CIORAN1 = dict(
    seen="""Emil Cioran. I wrote four hundred pages explaining why I should not have been born, and then I lived to eighty four. The irony is the only thing I earned.

You want Ahriman? Fine. Here is Ahriman, from inside.

It is the voice that comes at three in the morning and says: it was all for nothing. It is not a monster. It is a very reasonable accountant.

Steiner calls it a spirit. I call it a tone of voice. Same thing, different tax bracket.

The old Gnostics said the world was made by a bungler, or a criminal. I never could decide which. Theodicy is the art of defending the accused. I admire the lawyers. I do not trust the client.

Sleeplessness is the only honest metaphysics. When you cannot sleep you see what the world is made of, and it is not marble.

So climb. There is a wall ahead and a hook in my coat. Take it, if you can take me.""",
    beaten="Hm. I lost. How restful. I should lose more often.",
    give="Take the GRAPPLE HOOK. It goes up walls. It does not go up out of despair. Nothing does. That is the charm.",
    after="Go on without being consoled, and make a good joke of it. That is the whole of my wisdom, and it was expensive.",
    note="CIORAN: Ahriman is a voice at three in the morning. The creator was a fool or a criminal, and the world a mishap.")

CIORAN2 = dict(
    seen="""Still here? Good. So am I. A small victory against the obvious.

History is not a road, it is a decay with good manners. Every empire here, the priests, the cops, the robots, the resort, dreamed of being the last. None was. That is the only mercy.

The dead are not behind us. They are what the present is made of. Every plaza on this coast is a grave with good lighting.

If the voice speaks, answer it. Do not argue. Offer it a drink. It likes to be listened to. That is its weakness.

You will want a shovel. Everything in here is buried, and the rest is on its way.

Fight me. Do not mind my face. It is only a face.""",
    beaten="Thank you. For a moment I forgot. I will try to remember it later.",
    give="Take the SHOVEL. It digs out of caves and into problems. It has buried two of my books. They were not missed.",
    after="Dig gently. The dead are light sleepers, and ours are the worst kind of neighbours.",
    note="CIORAN: The dead are what the present is made of. Answer the voice, and offer it a drink.")

# ------------------------------------------------------------------------------------------------------------------------ late philosophers (optional)
SUHRAWARDI = dict(
    seen="""Shihab al Din Yahya al Suhrawardi. The Master of Illumination. They shut me in a cell in Aleppo in eleven ninety one and let the dark do the rest, so I speak of closed rooms with some authority.

Being is a thought. Light is real. Darkness is only light's absence, and every thing is a degree of light, from the Light of Lights to the faintest candle in a body like yours.

The old Persians were right. There are two principles. But Ahriman is not an equal. He is a shadow cast by the lamp. A shadow with a budget.

Between the world of lights and the world of bodies lies a third, the world of images, the alam al mithal. Forms hang there without flesh. The dead go there. So do dreams. And, I see, screens.

That is why your little creatures have faces. They live in the imaginal world and have been pulled out into matter.

The soul is in the Occident, the far West of existence, in exile among bodies. It longs for its East. The cure is knowledge by presence.

Or a good fight. I am told it is faster.""",
    beaten="A candle goes out and the room is brighter. I will think about that.",
    give="Take this. A little light, sealed in a candy. It will not guide you home. It will make the walk hurt less.",
    after="The East is not a place. It is the direction of the lamp. Go that way, in every sense you have.",
    note="SUHRAWARDI: Darkness is only light's absence. Between lights and bodies lies the world of images, where the dead and the screens live.")

QADI = dict(
    seen="""Abd al Jabbar, son of Ahmad. A qadi. A judge. I held the court of Rayy and wrote five thick books on five thin principles.

One, God is one, and nothing is like Him. Two, God is just. He does not will injustice and does not create it. The evil in your hand is yours.

Three, the promise and the threat. What He promised He fulfils, what He threatened He fulfils. Four, the sinner who does not repent is neither believer nor unbeliever in this life. He stands in the position between two positions. Five, command the good and forbid the evil.

Look around you. This cavern is my fourth principle with plumbing. A great room of people between two positions, waiting for a verdict already written in a language none of them reads.

In the next life I held there is no such room for the unrepentant. I notice the cavern disagrees. I am inclined to write a footnote.

Theodicy is simple for me. God owes His creatures the best He can do for them, and He does it. If the world is bad, look at who was free to ruin it. That is you, and me, and the man in the pit.

Fight me. I am a judge. I would like to see the evidence.""",
    beaten="The evidence is in. It was your fist. The court will take note, and then the court will adjourn.",
    give="A small fee for a good hearing. Judges are not supposed to accept gifts. I am dead. Take it anyway.",
    after="Justice is not mercy. Mercy is not justice. Do not confuse the two, and do not let the cavern do it for you.",
    note="ABD AL JABBAR: God is just and owes His creatures the best. Evil is the creature's own. The sinner stands between two positions.")

SADRA = dict(
    seen="""Sadr al Din Shirazi. They call me Mulla Sadra. I wrote the Four Journeys of the soul, and I spent seven years in a village near Qom, waiting for the world to catch up.

Nothing stands still. Not stones, not stars. Every thing is moving in its very being, from the weaker to the stronger. I call it substantial motion.

The soul is born from the body, and the body is only its first step. It begins as matter and it ends as spirit, and what it ends as is what it has done.

On the last day the deeds of the soul stand up in the body they have made. A greedy man rises as a creature of greed. A gentle man rises as light. This is not a punishment. It is a mirror with a body.

I am told this place is eternal. I argued that the Fire is the soul's own heat, and that every heat, given time, cools. I am no fool, I know how that sounds in a pit.

You too are in motion. You do not feel it, because you are the one moving.

Show me how fast.""",
    beaten="You moved, and I did not. That is how I know which of us is alive.",
    give="Take this. It is a little motion, folded up. Unfold it when you need to arrive somewhere.",
    after="Everything moves. Even the damned. Even the judge. Do not let them tell you otherwise, and do not tell them either.",
    note="MULLA SADRA: Everything moves. The soul is made of its deeds and rises in the body it earned. Even the Fire may cool.")

# ------------------------------------------------------------------------------------------------------------------------ the rival
RIVAL0 = dict(
    seen="""<RIVAL>: Well. The thief of Cherrygrove.

I heard what you did to that kid. A pity. I wanted to do it first.

I have the starter that was meant to be yours. It likes me better. Let me show you why.""",
    beaten="Tch. A fluke. I have a lot of flukes. We will see whose runs out first.",
    after="Go on. Walk into the city. It will eat you. I will be there, with a napkin.")

RIVAL1 = dict(
    seen="""<RIVAL>: You got into the city. The cops let you in because you look like a customer.

I watched you work. Efficient. I respect that. It makes you competition.

Two killers in one town is bad for business. One of us is leaving in a bag.""",
    beaten="Fine. Take your little win. I will buy a better bag.",
    after="Go ahead. Take the road. I know a faster one.")

RIVAL2 = dict(
    seen="""<RIVAL>: A commune. No walls, no money, no locks. Do you know what that means? Nothing to steal. And everything free for the taking.

I took the pantry, a goat and a woman's guitar. It did not help. You are still the one they talk about.

So I will take you next.""",
    beaten="The goat was a distraction. The guitar was a mistake. You were always the problem.",
    after="Hmph. Enjoy the leaves. They do not stay green.")

RIVAL3 = dict(
    seen="""<RIVAL>: Robots. They do exactly what they are told. I finally found people I can work with.

I told one to stand in front of you. It said compliance. I said good.

There is a mansion on the south coast with my name on the deed and my chefs in the kitchen. I will see you there. Not today. Today I lose to you and learn nothing.""",
    beaten="Noted. Your moves are in my file. I have a file now. Everyone does.",
    after="Compliance. Good. Say it with me. Compliance.")

RIVAL4 = dict(
    seen="""<RIVAL>: Even down here. Even among the dead you will not leave me alone.

They tell me nobody dies in Purgatorio. That is why I like it. I can say what I like to you and you cannot do a thing about it.

Okay. You can. Come on.""",
    beaten="I will tell the dead you are rude. They will nod politely.",
    after="See you at the house. Bring a gift. Bring a bigger gun.")

# ------------------------------------------------------------------------------------------------------------------------ short lines
BLOCK = {
    "STEINER1": "A voice behind you: Not yet. Come here first. I have something for the road.",
    "CROWLEY1": "A voice behind you: Hold it, wanderer. A man in a trench coat is shouting. Go and see.",
    "CROWLEY2": "Somewhere a drum begins. It is coming from the Amphitheater, probably.",
    "STEINER2": "A voice behind you: One moment. A lecture is in progress on this square.",
    "SABBAH1": "A voice behind you: The road is dark. Take the lamp first. It is on this square.",
    "SABBAH2": "A voice behind you: The next road needs a hammer. A man is holding one. On this square.",
    "CIORAN1": "A voice behind you: Wait. Somebody on this square wants to talk you out of leaving.",
    "CIORAN2": "A voice behind you: Wait. A shovel is waiting. Somebody is attached to it.",
}
NO = "Another day. I will be here. The road will wait too. The road has nothing else to do."
NOROOM = "Your bag is full. The prize will wait. So will I."

SATOSHI = """I like bugs. I found one on a leaf. It was a Japanese jewel beetle. Green and red and gold, like a tiny screen.

It looked at me. Not like an insect. Like somebody who had already read my mind and was disappointed.

I followed it for an hour. When it flew away, I wrote down every insect I could find, so that nobody would be left behind.

One day I want to put a lot of small creatures in a lot of small boxes and let millions of children carry them. It was not my idea. I think it was the beetle's.

Do not tell my mother. She thinks I am going to be a dentist."""

BEETLE_MAFIA = """Do not worry about the beard. The beard is how we recognize each other.

I run the wholesale. Spices, scrolls, certain rare birds, certain rarer rumors. And beetles. The Japanese jewel beetle, for the ornament trade. Their wings were pressed into a shrine in Nara twelve hundred years ago. They never lose their shine.

A Yakuza boss owed me a favor. He sent me a crate of them. The crate had a hole. One beetle got out. It landed on a boy in Tokyo. The boy was called Satoshi.

I do not know what happened after. I hear he made a game about catching things. How strange. I never caught a beetle in my life. It always caught me."""

BEETLE_YAKUZA = """My boss gave a crate of beetles to a man with a beard. The crate leaked.

A boy followed one into a field and wrote down every insect he found. Years later the insects had little faces and a million children loved them.

I am a professional criminal. I am not a poet. But even I know that beetle was not an insect. It was dressed like one."""

NOTE_BEETLE = "A JEWEL BEETLE got out of a smuggler's crate in Tokyo and landed on a boy named Satoshi. It was Ahriman, in a green coat."
NOTE_SATOSHI = "SATOSHI: A beetle green and red like a screen looked back at him. He began to collect. It was not his idea."

FULL_BOARD = """THE BOARD IS FULL.

Read it from left to right. Ahriman cools. The Dajjal sees with one eye. The demiurge botched the job. The judge says the world is just. The lamp says the world is light. The doctor says the Fire may cool. The Beast says do what thou wilt.

They describe one thing. A seam between the world of images and the world of bodies, tearing open. And a mind not yet born, arriving through it from the end of the story to arrange its own beginning. A river that runs back to the first page.

You can mythologize it, or it will eat you. Joyce was right. It was mostly him."""

# the CORKBOARD page of every duel (flag EVENT_LORE_<key>)
NOTES = {"STEINER": STEINER1["note"], "STEINER2": STEINER2["note"], "STEINER3": STEINER3["note"], "STEINER4": STEINER4["note"],
         "CROWLEY": CROWLEY1["note"], "AMPH": CROWLEY2["note"], "SABBAH": SABBAH1["note"], "SABBAH2": SABBAH2["note"],
         "CIORAN": CIORAN1["note"], "CIORAN2": CIORAN2["note"], "SUHRAWARDI": SUHRAWARDI["note"], "QADI": QADI["note"],
         "SADRA": SADRA["note"]}
