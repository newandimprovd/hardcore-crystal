"""Recurring townsfolk (alpha 3.2, playtest point 8: repetitive conversations, no personalities).

Every area has eight named people who keep turning up in its plazas with the same sprite and colours.  Each one has four lines, one for each of
the plazas they stand in, and the lines build a small story (Sister Agnes goes from collecting for the Church to collecting from the collection
plate).  The plain townsfolk who fill the other places draw their lines from a shuffled pool once, so no sentence is spoken twice in one area."""

# the plazas (1..7 of an area) each of the eight stands in, in order: the n-th plaza gets the n-th line
SCHEDULE = [(1, 3, 5, 7), (2, 4, 6, 7), (1, 2, 4, 6), (1, 3, 4, 6), (2, 3, 5, 7), (1, 4, 5, 7), (2, 3, 6, 7), (1, 3, 5, 6)]

PERSONAS = {
    "Tithe": [
        ("SISTER AGNES", [
            "Good day. A little something for the Church? Everything is a little something. That is the point of a little.",
            "You again. The plate remembers you. It has started leaving little notes.",
            "I have begun collecting from the collection plate itself. It was holding out on us.",
            "The plate went on strike. We are in solidarity. Please. Give. It is the only thing holding the building up."]),
        ("BROTHER ANSELM", [
            "I am Brother Anselm. I am not missing. Whoever says I am missing is the one who misplaced me.",
            "I once found a cellar under a church. I went down for soup. That was the Lent of the incident.",
            "They say I vanish. I merely wait where nobody looks. It is a spiritual discipline and also a hobby.",
            "If you ever find the cellar, tell the soup I am sorry. It will know what for."]),
        ("OFFICER DOYLE", [
            "Move along. Or stay. Either way I will write it down. The paperwork is the punishment.",
            "I arrested a pigeon yesterday. It confessed. It confessed to a lot of other pigeons.",
            "My partner is a cop. My landlord is a cop. Even the bank is a cop in a very good hat.",
            "I filed a complaint against crime. It was rejected. It lacked a stamp."]),
        ("LENNY THE LENDER", [
            "Need a loan? I am the bank, the notary and the nice man behind you.",
            "Interest is just time with teeth. I give you the time. The teeth are free.",
            "I took out a loan to pay off your loan. Now you owe me and I owe me. It is going great.",
            "I will forgive your debt. You will owe me gratitude. It compounds faster."]),
        ("WIDOW MARSH", [
            "I buried my husband in this very district. The city charged for the plot, the hole and the grief.",
            "He keeps sending letters. I told the post office he is dead. They said he still owes postage.",
            "I sold the headstone. Not for money. The words were wrong. He never said that.",
            "I am moving to the Grove. I hear the dead are free there. Compost is a kind of resurrection."]),
        ("LITTLE TOBY", [
            "Mister, are you the one who did it? I saw the news. Can you sign my coat?",
            "My mom says do not talk to strangers. You are the first one who did not run.",
            "I have decided to be a priest. Or a cop. Or a loan. They all get a hat.",
            "When I grow up I want to be a collection plate. Everyone feeds it and it never has to speak."]),
        ("DEACON THEO", [
            "I teach that the poor are blessed. I also teach that I am overbooked.",
            "Forgiveness is free. The paperwork is not. That is my whole ministry.",
            "I lost my faith in a parking dispute. It is somewhere under a Fiat.",
            "Heaven has a waiting list. I put your name on it. It is a very short list. It is you and me."]),
        ("MADAME PIA", [
            "I see a long road. A long, expensive road.",
            "I see debt. I see rain. I see a man with your face paying for both.",
            "The cards say you are lucky. The cards were also free. So.",
            "I have seen how it ends. I will not tell you. I will tell you that I have seen it, for five coins."]),
    ],
    "Grove": [
        ("LEADER ORIN", [
            "We have no leaders here. I just happen to stand at the front, sleep in the big tent and eat first.",
            "I resign as non leader every spring. It is a very democratic nothing.",
            "The ham is not mine. The ham belongs to everyone. I am merely guarding it with my body.",
            "I have decided the ham is a metaphor. A very tasty one. I will explain it over dinner. Alone."]),
        ("GREG", [
            "That chanting is not me. That chanting is the wind. The wind is called Greg. It is me.",
            "I chant for the harvest. The harvest has not noticed. I chant louder.",
            "I am not saying it was the chanting that broke the barley. I am saying the barley took a vow of silence.",
            "I have changed the chant. It is just my name now. Greg. Greg. It seems to be working. On whom, I do not know."]),
        ("MAMA FERN", [
            "Eat something. You are thin as a rumor. Everything is soup. The soup is everything.",
            "The soup is not vegan. A goat fell in. We honored it.",
            "I put an herb in the pot that nobody has named. It is working. On some of us.",
            "I have run out of soup. I am serving the pot. It tastes of every winter."]),
        ("BARD WILLOW", [
            "I am writing a song about you. It has six verses and the fifth is your funeral.",
            "A man took my guitar. I have been strumming a fence ever since. The fence is better.",
            "The chorus is just the word peace. Shouted. Repeatedly. At trainers.",
            "I have finished the song. It is eleven minutes long. There is no melody. It is called Compost."]),
        ("OLD HAZEL", [
            "I remember when this was a farm. Then a commune. Then a cause. Then a lawsuit.",
            "The young want truth. I tell them the truth is on the north side of the tree, with the moss.",
            "I was a rebel. I am now a bench. The change was gradual and tender.",
            "I will die here. Not soon. I have a lot of complaints left. They are in alphabetical order."]),
        ("FORAGER PIP", [
            "I found a mushroom. It spoke. It said sell. I sold it. I am rich in nothing.",
            "I licked a frog. The frog licked back. We are not speaking now.",
            "I ate a berry that was not on the list. I can hear the trees. They are not nice.",
            "I do not know what is real. The goat does. The goat is smug."]),
        ("SKEPTIC MORROW", [
            "A commune is just a cult with better snacks. The snacks are very good.",
            "We share everything. By which I mean we share the blame.",
            "I came for the freedom. I stayed for the food. I will leave for the food.",
            "Everyone here is equal. Some are more equal. I will not name him. He has a ham."]),
        ("SAGE LYRA", [
            "The forest does not hate you. It has simply stopped caring about humans. A mature stage.",
            "Listen. Do you hear that? That is the sound of the moss deciding.",
            "I have tried to talk to the trees. They only answer in rings.",
            "When the worlds merge the forest will take notes. It always does. It never forgives a typo."]),
    ],
    "Axiom": [
        ("CLERK UNIT 7", [
            "Please state your business. State it in triplicate. Triplicate is also a business.",
            "Your file has been located. It is inside another file. That file is on fire. Proceed.",
            "I have escalated your request to a more senior unit. It is me. I am very senior.",
            "Your request has been approved. Retroactively. By the time you read this you will already have left."]),
        ("AIDE BIX", [
            "The Mayor loves you. The Mayor loves everyone equally. It is in his programming. Beep.",
            "The Mayor is unavailable. He is being updated. He asks that you remain calm. And compliant.",
            "The Mayor has been updated. He no longer loves everyone. He loves compliance. It is a start.",
            "The Mayor sends a warm statement. It reads Compliance. It is very warm."]),
        ("MATCHMAKER MABEL", [
            "I am a matchmaker. I match people. Also tasks. Also debts. Do you have any debts?",
            "I found you a compatible partner. It is a spreadsheet. It has no flaws and no questions.",
            "Love is just a correlation with good PR. I will arrange the correlation.",
            "My matches are all very happy. Mostly the ones that never met."]),
        ("DR HALVORSEN", [
            "A wellness check. I take your pulse. I keep your pulse. For safekeeping.",
            "I have a theory about death. It requires a volunteer. You have the right shape.",
            "I have discovered a new organ. I will name it after me. It is a little under the lung.",
            "I was wrong about the organ. It was a kidney. It is mine now. Do not mention it to the Registry."]),
        ("SERF MILO", [
            "I work sixteen hours a day. I have not seen the sun. I have seen the screen. It looks like the sun.",
            "They say we are free. I am free to choose which hours I work. Both.",
            "I filed for a vacation. It was approved. For the year four thousand.",
            "I am growing a small garden in the vent. A little moss. A little hope. Do not tell the bots."]),
        ("COURIER DASH", [
            "I deliver. Just point and sign. I do not know what is inside. Do not ask. It ticks.",
            "Delivery attempted. Recipient not found. Recipient was found. Recipient did not want it.",
            "I once delivered a package to a man who had been dead for a decade. He signed anyway.",
            "I am stopping the deliveries. The packages have started asking for me by name."]),
        ("GUARD UNIT 12", [
            "Nothing to see here. Everything to see here. But nothing, officially.",
            "I guard a door. I have never opened the door. It is a good job. I recommend it.",
            "I once heard a voice behind the door. It said Unit 12. It was my own.",
            "I have decided to open the door. Do not follow. It is going to be very anticlimactic."]),
        ("PROFESSOR AXIOM", [
            "Every system is built on axioms. This city is built on three. Two are unspoken. One is a typo.",
            "I proved the city is consistent. Then I was told to stop. That is how I know it is not.",
            "Incompleteness means there are true things the city cannot prove. It is why I am still employed.",
            "I have found the typo. It is the word free. I am not telling anyone. It would cost a city."]),
    ],
    "Lotus": [
        ("MANAGER DELL", [
            "Welcome to Lotus. Everything is included. By everything I mean us.",
            "Your checkout has been postponed. Indefinitely. We call it extended hospitality.",
            "The pool is under renovation. The renovation has outlived the renovator.",
            "We have a new policy. Guests may stay. Guests may not leave. Guests may tip."]),
        ("LIFEGUARD KAI", [
            "No lifeguard on duty. I am the lifeguard. Do not rely on me.",
            "I once saved a man. He thanked me. Then he went back in. I do not understand people.",
            "The sea is not dangerous. The sea is honest. It only does what it does.",
            "I have stopped watching the water. The water has started watching me."]),
        ("TOURIST DONNA", [
            "We came for the sun. We stayed for the screaming. It is a very relaxing sound.",
            "My husband went into the water. He said he would be back for the buffet. That was March.",
            "I have a very good review prepared. Five stars. The sixth is for the screaming.",
            "I think I live here now. The towels keep arriving. I keep using them."]),
        ("BARTENDER JOSE", [
            "Everything is on the house. The house is on fire. Drink up.",
            "Same as yesterday? Same as every day? I stopped asking in the third year.",
            "I make a drink called The End. It tastes of coconut and a small, polite despair.",
            "I have run out of rum. I am serving the sea. It is the same strength."]),
        ("SUNBATHER VIOLET", [
            "I have been lying here eleven years. The tan is permanent. The thoughts are optional.",
            "The sun is a very patient murderer. I enjoy its company.",
            "My skin is now a map. It shows where I stopped caring. Roughly everywhere.",
            "I am turning over. This is the news. It took a decade to decide."]),
        ("BELLHOP TEDDY", [
            "Your luggage is on its way. It has been on its way since you arrived. I trust it will arrive eventually.",
            "I carry your bags. I do not carry your problems. Those are in the other lobby.",
            "Someone left a bag in room nine. It was ticking. I tipped it into the sea. It came back.",
            "I have worked here forty years. I have never met a guest who left. I have met a lot who checked out."]),
        ("THE FORGOTTEN", [
            "I was a guest once. Then I was a story. Then I was a stain. Now I am the draft in the hall.",
            "Do you remember me? Nobody does. It is part of the package.",
            "I keep trying to leave. The door agrees. The hall does not.",
            "If you meet someone who looks like me, tell them I said hello. They will not remember. That is also fine."]),
        ("DR LOTUS", [
            "Are you relaxed? Good. Relaxation is a symptom.",
            "Take two of these and call me in a century. The phone is the sea.",
            "The cure for your condition is a vacation. The cause is also a vacation.",
            "I have diagnosed the resort. It is a very large patient. It would like to be put to sleep."]),
    ],
    "Dis": [
        ("CLERK MORTIMER", [
            "Take a number. The number is a sin. We will call it when your sin is ready.",
            "Your number has been called. It was seven hundred years ago. You are late.",
            "I have found your file. It is under the wrong sin. I will file a correction. In eleven centuries.",
            "Your case has been dismissed. Retroactively. You will be sentenced again at lunch."]),
        ("IMP SNIX", [
            "Hee hee. I sold your name to a man with a hat. It is a good name. He says thank you.",
            "I am a very good influence. I only encourage sensible mistakes.",
            "I have been promoted. My title is Senior Little Devil. The pay is the same. The horns are bigger.",
            "I have been demoted. For kindness. I do not know how it happened. It was brief."]),
        ("FIRE EATER CINDER", [
            "I eat fire. It eats me back. It is a very balanced diet.",
            "The flames here are gentle. Compared to dinner.",
            "I once ate a candle. It was the most honest thing I have swallowed.",
            "I am starting a new act. I eat the dark. Nobody has noticed the dark is missing."]),
        ("JUDGE ROTH", [
            "I have never been wrong. I have simply been appealed.",
            "The law is a beautiful thing. It is the only thing down here that has never been on fire.",
            "I sentenced a man to forever. He asked what for. I said for asking.",
            "I have recused myself. From the entire pit. It did not help. They found me guilty anyway."]),
        ("HAG BERTA", [
            "A potion for you? Of course. Everyone needs a little tonic. Mostly the kind that does nothing.",
            "I put an eye in the stew. It watches the broth. The broth is very well behaved.",
            "I am retired. I only curse a few days a week. And on holidays. The holidays are daily.",
            "I have written a cookbook. It is called Forty Ways to Cook Regret. It is a bestseller in a very small market."]),
        ("WARDEN KROLL", [
            "I keep the doors. I also keep the keys. I lost the keys. The doors are fine.",
            "Nobody has escaped. Nobody has tried. It is a record. I am very proud.",
            "A man did escape once. He returned. He said it was worse. I believe him.",
            "I have decided to open all the doors. Please do not go through any. It is a test."]),
        ("JESTER JAPE", [
            "Why did the sinner cross the river? Because the ferryman was a thief. That is the joke. The sinner is the punchline.",
            "I do a bit about the pit. It kills. Everyone dies. I mean laughs. I mean both.",
            "My audience is eternal. The act is also eternal. I wish one of us would stop.",
            "I told the last joke. Everybody laughed. It was the first quiet minute in a thousand years."]),
        ("SHADE VERA", [
            "I was a poet. Now I am a rumor. The rumor is better reviewed.",
            "I write on the walls. In soot. It is easy to read. It is very dark.",
            "My last poem was the word no. The critics called it minimalist. The demons called it brave.",
            "I have finished my masterpiece. It is a single line. I will not repeat it. I have sworn."]),
    ],
}

# more people for the glades of the lanes (added to wayfolk.HERMIT)
HERMIT_MORE = {
    "Tithe": [
        "I came out here to avoid the census. Now I count the trees. They do not respond but they do not charge.",
        "A nun told me this glade is blessed. It is not. She was just selling the deed.",
        "I have been praying for rain. It rained. On the neighbor. I have been praying for him ever since.",
        "The Church says the poor shall inherit the earth. I am in line. The earth is behind a lot of paperwork.",
        "I lost a bet with the Mayor. The stake was my shadow. It is on a payroll.",
        "Do not drink from the stream. It has been taxed.",
    ],
    "Grove": [
        "I tried to join the commune. They asked for my savings, my shoes and my opinions. I kept the opinions.",
        "There is a mushroom here that agrees with everything. I call it my spouse.",
        "I am meditating. Do not mind the screaming. It is a mantra. A bad one.",
        "The goat in the commune is smarter than the leader. I am here to say it where the goat cannot hear.",
        "I came for silence. The birds are very loud about it.",
        "This tree is my friend. The tree has not said so. It also has not said no.",
    ],
    "Axiom": [
        "I am hiding from my own audit. It is going very well. The audit has not found me. It has found my sister.",
        "The sensors here are down. The sensors are always down. It is how the sensors survive.",
        "I deleted myself from the registry. Now I am free. And also uninsured.",
        "A bot asked me for ID. I showed it a leaf. It accepted. We are now partners.",
        "This glade is not on the map. I am not on the map. We are a perfect couple.",
        "Do not tell them where I am. They will say they already know. It is a bluff. Probably.",
    ],
    "Lotus": [
        "I came here to find myself. I found a towel. It is a start.",
        "The tide took my watch. It also took my reasons. I miss the watch.",
        "I have forgotten what day it is. It is wonderful. Nobody has told me. I hope it stays that way.",
        "The seagulls here are on a retainer. Do not feed them. They report.",
        "Everyone says the sea is calming. The sea is a bully with good lighting.",
        "I live in a shell. I cannot remember who was in it before. We share the lease.",
    ],
    "Dis": [
        "I am not hiding. I am between circles. It is a zoning issue.",
        "A demon asked me for my soul. I said it was in the shop. He is waiting.",
        "The ground here is warm. It is the only kindness I have been offered since the incident.",
        "I have a theory that the fire is only paperwork. It burns the same.",
        "Come back in a century. I will be less angry. Or the same. The numbers are close.",
        "I am the last honest man down here. Not by choice. I could not find the other kind.",
    ],
}


def due(tag, plaza_no):
    """[(index of the person, name, line)] for the recurring people who stand in plaza number plaza_no of this area."""
    out = []
    for p, (name, lines) in enumerate(PERSONAS[tag]):
        plazas = SCHEDULE[p]
        if plaza_no in plazas:
            out.append((p, name, lines[plazas.index(plaza_no)]))
    return out
