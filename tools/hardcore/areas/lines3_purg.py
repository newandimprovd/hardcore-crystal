"""Alpha 3.3 variety pass: the hidden recluses (areas/purg.py hermit()), 44 of them in the caves, vaults and hollows, each with a voice of his own.
Entry k of every list belongs to recluse k, counted in the order they are built.  The sprite is HERMIT_CLASSES[k % 3]: 0 an old man, 1 an old woman,
2 a shaman.  HERMITS holds one (seen, beaten, gift, after) per recluse; the four lists below are what the generator reads."""

HERMITS = [
    # 0 man: a failed saint
    ("Halt. I am a saint in training. I've been training for sixty years. Don't make it sixty-one.",
     "Ah. Another failure. Fine. I'll add it to the collection.",
     "Take this. A saint gives. A failed saint gives and whines about it.",
     "I tried to levitate this morning. The ceiling is very close. Let me show you the bruise."),
    # 1 woman: retired landlady of the dead
    ("Rent's due. I don't care that you're not a tenant. Everyone pays something. Fight me for it.",
     "Fine. I'll waive this month. Not the next. I'm not a monster.",
     "Here, a deposit refund. The room was never yours. Take it before I remember.",
     "Don't touch the walls. I own the walls. I own the dampness. The dampness is a separate fee."),
    # 2 shaman: a cheerful liar
    ("Welcome, welcome! I can see your future. It is brilliant. I'm lying. Fight me.",
     "I told you I'd lose! No, I told you I'd win. One of those was a lie. Probably both.",
     "A gift from the spirits. The spirits are me. I'm very persuasive. Take it.",
     "I never said any of that. You imagined it. I am a respected seer. Mind the door."),
    # 3 man: an ex-executioner
    ("I used to do this for a living. I was better at the other half. Let's see about this half.",
     "Ha. I used to do it in one swing. You took the long way. Respect.",
     "Take it. Among the hangmen of my day there was a custom. You leave something behind.",
     "I still dream of axes. Not mine. Other people's. They're looking for me."),
    # 4 woman: a poet who hates poetry
    ("Don't talk to me in verse. Don't talk to me in anything. I'm here to hate. Come on.",
     "Even losing rhymes with something. I despise that. Take your prize.",
     "I wrote this on a napkin in a fever. It's a gift. It's also my worst. I'm so sorry.",
     "Metaphors are for cowards. I prefer a slab of rock. Please go away, my muse is returning."),
    # 5 shaman: has forgotten who they were
    ("Who are you? Who am I? Fight me and we'll see which of us remembers.",
     "That felt familiar. I think I used to lose often. It's coming back. Awful.",
     "I found this in my pocket. It isn't mine, I think. Maybe it's yours. Take it.",
     "I knew a man who looked like you. Or a rock. Or a priest. Everyone is blurry."),
    # 6 man: a tax collector hiding from his own audit
    ("Don't look at the ledger! You're not from the Bureau, are you? Fight me, just in case.",
     "Audit complete. Result, one defeat. I owe you nothing. You owe me a signature.",
     "Take it. It's a deduction. Don't ask what for. Deductions are never for anything.",
     "They found me once. I paid them in coins and fear. It worked then. It won't work now."),
    # 7 woman: a widow who married the cave
    ("The cave and I have an understanding. You are an intruder in a very private marriage. Fight.",
     "My husband, the cave, will be told. He will be upset. He is quite wet.",
     "Take this. A wedding present from the stone. It's very small. It's a very small cave.",
     "Please keep your voice down. He's an echo. It gets awkward."),
    # 8 shaman: collects echoes
    ("Shh. Don't shout. I collect echoes. You're about to give me a very good one.",
     "Excellent! Your yelp echoed for eleven seconds. A personal best. Keep it.",
     "For you. A jar of your own echo. Open it when you're lonely. It will say your name.",
     "I recorded your defeat. It hums in the third jar. I play it when I'm sad."),
    # 9 man: an ex-judge who sentenced himself
    ("Order. Order! I sentence myself to meet you. The charge is trespass. The penalty, a fight.",
     "The court finds in your favor. The court also finds I'm tired. Adjourned.",
     "Evidence, exhibit A. It has been admitted into your pocket. Don't ask me why.",
     "I'm serving life in this cave. It's a clean sentence. I just wish the neighbors were quieter."),
    # 10 woman: a former nun with a gambling streak
    ("Child, I'll bet you my rosary against your boots. Heads I fight. Tails also I fight.",
     "Lord, I should never have played that hand. Take your winnings. And my blessing, which is worthless.",
     "Here. It's a lucky charm. It has never brought luck. Perfect for a gambler. Take it.",
     "I confessed once to a bishop. He took my chips. That's why I live in a hole."),
    # 11 shaman: speaks only in weather
    ("Low pressure, with a front of fists. Expect pain by evening. Fight me.",
     "Clearing skies. Light bruising to the south. Thank you for your cooperation.",
     "A warm front is moving in. It's a gift, sort of. Carry it where the weather is bad.",
     "Scattered showers. A chance of regret. Wear something dark."),
    # 12 man: a cartographer of a map nobody asked for
    ("Don't step on my map! It's the whole cave in miniature. There is one error. You.",
     "Noted. I'll draw a small man being punched. Right there, near the northern wall.",
     "I made a spare copy of something rare. Take it. Mark your own passage. I'm not jealous.",
     "The map is two years out of date. The cave rearranged itself out of spite."),
    # 13 woman: ex-stewardess of the afterlife shuttle
    ("Please return your seat to the upright position. And your face to the upright position. This is a fight.",
     "Thank you for flying with us. Please check the overhead bin for your dignity.",
     "Complimentary. It is shaped like a snack and weighs like a memory. Enjoy.",
     "Fasten your belt. The turbulence in this cave is mostly grief."),
    # 14 shaman: haunted by their own ghost, who is rude
    ("My ghost tells me you're weak. My ghost is rude and often wrong. Let's find out.",
     "Hah. My ghost owes me an apology. He is already laughing. He always does.",
     "Take it. It was his idea. I never wanted to give it. He insisted. Loudly.",
     "He's behind me. Don't look. He's making a very unflattering face."),
    # 15 man: an ex-cop turned mushroom farmer
    ("You're under arrest. Not really. I'm just practising. Resist, please. It's been a while.",
     "You have the right to remain victorious. Anything you say can and will be fondly remembered.",
     "Evidence, confiscated from a better cave. Take it. I don't have the paperwork. It's the first time I'm happy about that.",
     "The mushrooms are quiet. They know something. I watch them. They watch me. It's a long trial."),
    # 16 woman: baker of bread for the dead
    ("The bread is for the dead. You are not dead. Fight me and we'll fix that.",
     "A crumb. Just a crumb of defeat. Fine. I still sell bread, with or without pride.",
     "Take it. It's warm. It's the only warm thing in this tunnel. Eat it. Or carry it. Same thing.",
     "The dead are very particular about crusts. I take notes."),
    # 17 shaman: believes he is a cave
    ("I am the cave. You are inside me. This is a gentle form of dying. Fight.",
     "Oh. I have been breached. This is how it feels. How curious, I'm not unhappy.",
     "I will give you something from my interior. Do not tell my stalactites.",
     "I'm still the cave. Please don't talk about my acoustics. They're a sore subject."),
    # 18 man: inventor of an unusable religion
    ("I invented a religion with nine commandments and no followers. Join, or fight. I'm easy.",
     "A heretic! In my own cave! I'm delighted. My first heresy.",
     "A relic of the faith. Number three of three. It does nothing. Neither do I. Take it.",
     "I added a tenth commandment. Don't bother the hermit. Please obey."),
    # 19 woman: a serial apologiser
    ("I'm so sorry. I'm so sorry about this. I'm so sorry I'm going to hit you.",
     "I'm sorry I lost. I'm sorry I'm apologising. I'm sorry I said sorry.",
     "Sorry. Take this. Sorry. It's nothing. Sorry. It's a lot, really.",
     "Sorry again. I shouldn't be here. I'm sorry I'm in your way. Sorry."),
    # 20 shaman: sells rumors, all false
    ("Rumor has it you're a coward. I made that up. It will be true in five minutes. Fight.",
     "Rumor has it I lost. That one was true. I'm sorry to see it spread.",
     "A reward, at no charge. The market for rumors is down. I'm paying you to stop listening.",
     "I heard the Mayor is a duck. I made it up. Pass it on. Please."),
    # 21 man: a kind hangman's apprentice
    ("I have never hurt a fly. I've hurt a few people. Lovely people. I'm sorry in advance.",
     "I'm so glad that's over. I'm sure you did your best too. No hard feelings.",
     "I made this myself. It's a little thank you for the fight. Please don't open it near me.",
     "Come by again. I'll bake you a loaf. I can't bake. I mean it kindly."),
    # 22 woman: ex-queen of a very small country
    ("Kneel. Or fight. Our country was one room. We still take protocol very seriously.",
     "My crown! Not the crown! The crown is a hat. Fine, take the hat. Fine.",
     "A royal gift. The treasury was a drawer. This was the best thing in it.",
     "My people are in the next cave. All four of them. Don't tell them I lost."),
    # 23 shaman: a dream thief
    ("I steal dreams for a living. Yours is a poor one. I'm trying to be gentle about it.",
     "That was a very bad dream. A loss. I'll keep it. It's a small collection.",
     "Take this. I stole it from a sleeping king. He won't miss it. He misses everything.",
     "I dreamed of you last night. You were dead. You were also kind. Sleep well."),
    # 24 man: lost a bet with death
    ("I bet Death I could outlast him. He was patient. I'm still waiting for him to win.",
     "Hah. He didn't send you. He's lazy. Tell him I said the bet's still on.",
     "Here. A trophy from our wager. I never won it. I just took it.",
     "He plays cards well. I play cards worse. We have a very long game."),
    # 25 woman: a cat lady whose cats are dead
    ("The cats are watching. They are not alive. They're still judgemental. Fight.",
     "The cats say you cheated. The cats are delusional. The cats are also right.",
     "Take this. The cats insist. They have no use for anything but spite.",
     "Don't pet the nothing at your feet. She bites. She remembers."),
    # 26 shaman: a lighthouse keeper far from the sea
    ("Stay clear of my light! The sea is out there. Somewhere. A very long way.",
     "Ha. The ship runs aground again. You are the ship. I am the light. I'm a poor light.",
     "A flare. I never had a ship to signal. Use it better than I did.",
     "I keep the beam turning. Nobody asked. The rocks seem grateful. It's mutual."),
    # 27 man: a critic of his own funeral
    ("My funeral was dreadful. The music, the hat, the eulogy. Let's talk about your face.",
     "I give it two stars. The fight, I mean. The funeral was one. I've been generous.",
     "Take this. I was buried with it. It never came to a good end. It's yours now.",
     "I hated every word of the eulogy. I'd correct it, but I'm dead. I do it anyway."),
    # 28 woman: a pickpocket of souls
    ("Your soul is a nice one. I'll have it. Fight me for it, or don't. I'm very fast.",
     "Fine, fine. You can keep your soul. I only wanted a look. It's a little worn.",
     "Here. I lifted it from a priest. It's cleaner than anything I've owned.",
     "I'm pocketing something now. Don't check. It's probably nothing. Probably."),
    # 29 shaman: counts stalactites
    ("Eleven thousand and four. Eleven thousand and five. Don't interrupt me. Fight me later. Fight me now.",
     "Eleven thousand and six. You made me lose count. I forgive you. Start again.",
     "Take this. I counted it three times. It's never the same number twice. That's why I give it.",
     "Shh. I'm at eleven thousand seven hundred. Please don't breathe so loudly."),
    # 30 man: an ex-mayor whose term never ended
    ("I'm still the mayor. Nobody voted me out. Nobody voted at all. Salute, or fight.",
     "A mayor can lose a fight. A mayor can never lose a cave. I stay.",
     "A ceremonial gift. The key to a city that no longer exists. It's a nice key.",
     "I opened a gate once. They threw rice. It was a very small gate. It was a very good rice."),
    # 31 woman: conspiracist about the moss
    ("The moss is listening. The moss is reporting. The moss is a spy. Fight me and I'll tell you the rest.",
     "I told you! The moss knew you'd win. It sent you. You are the moss's weapon.",
     "Take this, and don't tell the moss. It's the only thing it hasn't found.",
     "Don't sit on the north wall. The moss there is the chief. It's very sensitive."),
    # 32 shaman: tea ceremony of one
    ("Sit. There's tea. There's only one cup. I'll take it. Now fight me politely.",
     "A very elegant loss. Please accept this tea. It's cold. So is my heart.",
     "A parting gift from the ceremony. The cup is empty. The gift is not.",
     "I'm preparing a second cup. For you. In case you come back. In case I'm still alive."),
    # 33 man: ex-bodyguard of a coward king
    ("I guarded a king who fled. I guarded his horse. I guarded his horse's cousin. Now I guard a hole. Fight.",
     "I should have run with the king. He ran fast. I'm slower. It's the knees.",
     "Take this. His majesty left it behind. In the rush. In the shame.",
     "I still wear the armor. It's rusty. It's also loud. I like being heard."),
    # 34 woman: an undertaker who flirts
    ("Hello, handsome. Hello, anyone. You look very alive. I'd like to measure you. Fight me.",
     "Oh my. A lovely thrashing. I'll hold off on measuring. For now.",
     "A little something to remember me by. It's practical. It's also shiny. Don't make it weird.",
     "Come back when you're a little less alive. I'm sure we'll get along."),
    # 35 shaman: whistles to the dead
    ("Shh. I'm whistling to the dead. They whistle back. Don't speak. Fight.",
     "A rude sound. Your loss was a minor key. They liked it. Take this for the performance.",
     "A tune and a trinket. Whistle it three times. They'll come running. Be careful.",
     "I heard them whistling your name. I can't tell if it was a welcome or a warning."),
    # 36 man: a monk who took a vow of loudness
    ("I TOOK A VOW OF LOUDNESS. IT'S THE MOST DIFFICULT ONE. FIGHT ME AT FULL VOLUME.",
     "HA. IT HURT. I'M SCREAMING TO SHOW IT HURT. HERE, A GIFT, AT FULL VOLUME.",
     "TAKE THIS. DON'T WHISPER. IT'S TOO SMALL FOR WHISPERS. IT'S TOO BIG FOR ME.",
     "I'M SORRY. I CAN'T LOWER MY VOICE. IT'S A VOW. IT'S ALSO A NUISANCE."),
    # 37 woman: a marathon walker going nowhere
    ("I've been walking this tunnel for nine years. It's a loop. Fight me, I need a change of scenery.",
     "A detour! Delightful. I'll add it to my route. Please take this. It's heavy.",
     "I carried it for six thousand laps. It's yours. My legs are very proud of me.",
     "I just passed you again. Or was it the other you? It's hard to tell in a loop."),
    # 38 shaman: a candle merchant
    ("Candles for the dying, candles for the wicked. You look like both. Fight me, then shop.",
     "The flame goes out. Another lesson. Please accept this with the sad smile of a merchant.",
     "A parting offering. A single spark. It's pure. Don't blow on it. Just carry it.",
     "I only sell light. Darkness is free. Take as much as you like. People always do."),
    # 39 man: a spy for a country that dissolved
    ("I am a spy. My country dissolved in 1997. I never got the memo. Fight me, comrade.",
     "Mission failed. As always. I'll burn this paper. It's just my grocery list.",
     "Take this. It's classified. It was classified so long ago, nobody remembers the classification.",
     "The file on you is five pages. All lies. I wrote it myself. It's quite good."),
    # 40 woman: an ex-teacher grading the cave
    ("Sit up straight. Pencils down. I'll grade your fight. I give most students a C minus.",
     "B plus. Not bad for someone with such poor posture. Take this, as an incentive.",
     "A reward for effort. I'd say good work, but that would spoil you.",
     "I graded the cave too. It scored very low on cleanliness. I gave it detention."),
    # 41 shaman: knows everyone's last words
    ("I know your last words. I won't tell you. Fight me and I might change them.",
     "Interesting. That changes the ending. Take this. It's a rewrite.",
     "A gift to commemorate your almost-last words. They were very good. You'll say them eventually.",
     "I've written down everything you said. Each page is a lie. They were all true in the end."),
    # 42 man: a tour guide with no tourists
    ("Welcome to the cave! On your left, rock. On your right, also rock. Please fight me, the tour is dull.",
     "And here, ladies and gentlemen, is the loser. Please clap. The gift shop is to your right.",
     "A souvenir. It's the last one. Tourism is dead. So is the tourist board.",
     "I do the tour for the echoes. They're excellent listeners. They never tip."),
    # 43 woman: a grandmother who outlived everyone
    ("I outlived my children, their children, and the village. Do you think you can finish me?",
     "Well, well. A little pain, a little respect. I haven't felt either in decades. Thank you, dear.",
     "Take this, dear. It was my husband's. He had no use for it. Neither do I.",
     "Eat something. You look pale. Everyone does. Everyone is. It's the cave."),
    # 44 shaman: the last hermit, tired of existing
    ("I am the last one. Truly the last. Everyone before me was only practice. Fight.",
     "Finally. Something that matters. Leave me now. Or stay. I don't care. I'm very tired.",
     "I've been saving this for the last person to find me. That's you. Congratulations.",
     "Go. The others may have been lonely. I'm lucky. I have nothing left to lose."),
]

PURG_HERMIT_SEEN = [h[0] for h in HERMITS]
PURG_HERMIT_BEATEN = [h[1] for h in HERMITS]
PURG_HERMIT_GIFT = [h[2] for h in HERMITS]
PURG_HERMIT_AFTER = [h[3] for h in HERMITS]
