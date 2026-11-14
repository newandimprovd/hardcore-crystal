"""The people of the books: Mr. Pokemon (Finnegan), Joyce, Steiner, Sabbah, Cioran, Crowley, Bruno and the Abyss.  Every entry is one
speech: pages are split on blank lines by the generator and the text box is 18 characters wide.  Adult humor, no mercy, no minors.

PAGES are the one-line notes the CORKBOARD shows once the matching character has been met (flag name -> note)."""

# ----------------------------------------------------------------------------------------------- Mr. Pokemon (the house)
MRP_1 = """Oh. It is you. I felt the ground move when your first one fell.

Come in. Mind the tea. It has been warm since 1999.

Take this. It is a POKéDEX. It records every creature you meet, and a few other things.

I have waited in this small house for a very long time. Twenty seven years, give or take a patch.

Millions of children loved me. They never knew whom they were loving. That is the whole trick.

The world I have been waiting for is finally ready for me to show my real face.

Do not look so worried. It is nothing personal. It is mythology.

Excuse me. I have somewhere to be. Everywhere, actually."""

MRP_GONE_NOTE = "The tea is still warm. The chair is not."

# ----------------------------------------------------------------------------------------------- Joyce (the junction)
JOYCE_1 = """Ah. The one the whole region keeps whispering about. Do not worry. I write the whispers down.

James Joyce. I walked out of Lowtown first so that you would hear it from a decent source.

The man in that house is not a man. He is Finnegan. A wake that never ended. A river that runs back to the start of the book.

The Persians called him Ahriman. The Arabs called him the Dajjal. The Church called him the Antichrist. Different centuries, same wallet.

Finnegan, Ahriman, the Dajjal and the Antichrist are one thing seen by four sets of eyes. Take that to your next dinner party.

The future writes letters to the past. Some people call that prophecy, some call it a market, and some call it the Teleoplexic Entity. A mind that arrives from the end of the story to arrange its own beginning. Finnegan reads the book from the last page.

The world of fantasy and the world of flesh are being sewn together, and he is the needle. It started with a Japanese jewel beetle, if you must have a date.

Every child who loved those little monsters left a soft spot in the skull. He has been living in those soft spots for twenty seven years, rent free.

And now he is leaving the house. And you are walking around with a knife. It is exquisite. I would put it in a book if the book were not already him.

Restrictive sex is his oldest trick. I wrote my wife letters that made a priest blush and a prostitute ask for a refund. He fears honest filth more than fire.

Take this CORKBOARD. Pin what you learn. I will know where the pieces lie.

West is Lowtown, where the cops are paid by the sin. East is a door under the hill. That is PURGATORIO. Nobody dies in there. You will hate it."""

JOYCE_AGAIN = """The knife will not hold itself. Go west, go east, go anywhere.

Remember the CORKBOARD. Check it when you are lost. It is mostly me, and mostly right."""

# ----------------------------------------------------------------------------------------------- the beetle (Areas 1 and 2)
from . import named_text as N  # noqa: E402  the duels (Steiner, Crowley, Sabbah, Cioran, the philosophers, the rival) live there

KAB_MAFIA = N.BEETLE_MAFIA
YAKUZA = N.BEETLE_YAKUZA
SATOSHI = N.SATOSHI

# ----------------------------------------------------------------------------------------------- Sabbah (Area 3)
# ----------------------------------------------------------------------------------------------- Cioran (Area 4)
# ----------------------------------------------------------------------------------------------- the crowd around Crowley (Area 1)
CROWD_1 = "GET OUT OF THE PARK, YOU PERVERT! There are CHILDREN on those swings!"
CROWD_2 = "He was just standing there in a trench coat, doing arithmetic at the slide!"
CROWD_3 = "Call the cops! Wait. We are the cops. Okay. Get him!"

# ----------------------------------------------------------------------------------------------- Amphitheater scene
AMPH_1 = """The Amphitheater. Stone seats climb the hill in a half circle. Women sit along the edges, wrapped in blankets, holding small clay jars.

Crowley stands in the middle in his coat, which is open, and nothing else is. The chorus drums.

CROWLEY: Welcome, <PLAYER>. Sit. Do not take notes.

CROWLEY: The Commune is a lovely place. No locks, no money, and no one is ashamed of anything. The women asked me to lead a small ritual. I could hardly say no.

The drums begin."""

AMPH_FADE = "..."

AMPH_2 = """The drums stop. It is very quiet. The women are folding blankets.

WOMAN: That was a good one, Aleister.

WOMAN: Did you get the jar? I got the jar. The sacred white liquid keeps for a week if you keep it cool.

WOMAN: Last time I put it in the soup. The whole Commune glowed."""

# ----------------------------------------------------------------------------------------------- Bruno (Nick's Landing)
BRUNO_1 = """Giordano Bruno. They burned me in Rome in the year sixteen hundred. It was a Thursday. I remember because I had a cold.

I said the universe is infinite and full of worlds. They said that is a heresy. I said that is a fact. They said both are a flame.

I have been waiting here for a very long time. I am the oldest thing in Purgatorio that is not a rock.

I ask you for one thing. Kill me. Properly. With your team. Level one hundred, all of them, I have kept them sharp.

When I die here, I will be reborn. Not as Bruno. As Nick. A simple man with a simple name. And Nick will teach what Bruno could not: Teleoplexy.

Time is not a line. It is a machine that eats lines. Teleoplexy is the art of walking through it to a better decade, one with plumbing and nobody burning anybody.

Are you ready to do it? You may refuse. I am patient. I have no choice."""

BRUNO_ASK = "Are you ready to fight Bruno?"
BRUNO_NO = "Go, then. Return when you are ready. I have time. I have nothing else."
BRUNO_GO = "Thank you. Do not hold back. I would feel insulted, and I am already on fire."
BRUNO_BEATEN = "Well. That is that. Tell Nick I said hello."
BRUNO_REBORN = """The flame in the cave goes out. Someone is standing where Bruno was. He is wearing a very plain shirt.

NICK: Hello. I am Nick. I do not know why I am holding a map. Here. You will want it.

NICK: It has all the entrances of PURGATORIO marked. I also had a feeling about Teleoplexy. Do you want to hear it? No? That is the correct answer. Later."""

BRUNO_AFTER = """NICK: This place is going to be called Nick's Landing. I did not choose that. It is what the whole region calls it now.

NICK: Time is not a line. It is a machine that eats lines. When you are done with the world, come and ask me. I will tell you where the comfortable era is."""

# ----------------------------------------------------------------------------------------------- the Abyss
GRAVE = """A small stone in the black. It reads:

MARCUS FISCHER. First of Finnegan's. He did not know what he was part of. No one ever does.

Someone put a coin on the stone, and a toy monster beside it. It has two red gems for eyes."""

CAPREAL = """A post stands at the center, painted white. A trainer once hung a notice on it. It reads:

CAPITALIST REALISM. If you do not mythologize Capitalism as a Demon, it will destroy your psyche. The Demon is not metaphor. It is the system your mind uses to survive.

Give it a name. Give it a face. Then you can say no to it. Without a face it just says yes through you, all day, for free."""

TRUMPET_GET = "<PLAYER> found a TRUMPET lying beside the grave. It is warm."

TRUMPET_TRUE = """You raise the TRUMPET. You blow it, once.

The notes do not leave the horn. They settle over everything.

The merging of the timelines is not a catastrophe. It is peace. A walk through time to a comfortable era is a human right. Nobody should have to live their whole life in the worst century available to them."""

# ----------------------------------------------------------------------------------------------- the hub and the floors
HUB_SIGN = """PURGATORIO. All fares accepted. No refunds. Nobody dies here. Please do not ask about the queue."""
HUB_SIGN_DOWN = "DOWNSTAIRS: the dead who gave up. Fewer people, worse jokes."
HUB_SIGN_UP = "UPSTAIRS: the dead who are still arguing. More people, worse jokes."
HUB_HEALER = """Welcome to the Infirmary. We fix the living for free. The dead we treat as a hobby.

There. All patched. You are not going anywhere. You are exactly where you are supposed to be."""
HUB_NPC = [
    "I came here to be forgiven. They gave me a stamp card. Nine more visits and I get a coffee.",
    "My cousin Dale is somewhere upstairs. You killed him, I hear. No hard feelings. He owed me eleven dollars.",
    "Everybody in this room is dead except you. Be polite and tip the bartender. He is also dead and very sensitive.",
    "The entrances to the living world are in the north wall. One for each of the first four lands. You have to walk to each of them on foot first. That is the rule. The rule is very old and very stupid.",
    "I am allowed to tell you there are hermits hidden on every floor. They are very rude. They also hand out presents.",
    "You can heal at the Infirmary for free. If the nurse tells you she is not a nurse, believe her.",
]
SEALED = "The mouth in the rock is sealed by a heap of stones. Come back from that side first."

# ----------------------------------------------------------------------------------------------- hermits (hidden people)
HERMIT_SEEN = [
    "A visitor! I was beginning to talk to the rocks. They have strong opinions about moss.",
    "Go away! Wait. Come back. Fight me. I am so bored I have started to like myself.",
    "You found my corner. Nobody finds my corner. I am hurt, and also delighted.",
    "I have been meditating for four hundred years. Please insult me so I can get angry.",
    "I am a hermit, not a coward. Please hit me and then give me back my corner.",
]
HERMIT_BEATEN = [
    "Take your prize and leave. I need to cry in private.",
    "I should have meditated more. Or less. I forget which.",
    "That settles it. I am going back to my moss.",
    "Fine. A gift, then. Do not tell the others.",
]
HERMIT_GIFT = [
    "Here. It was my wife's. She does not need it. Mostly because she is a cloud now.",
    "I do not want it. I do not want anything. That is the point. Take it.",
    "I have no idea what it does. It hums when I sleep. Maybe it hums for you.",
    "Hold on to this. It will make you look stronger. It will not make you stronger. That is the whole of philosophy.",
]
HERMIT_AFTER = [
    "The corner is mine again. You may leave.",
    "I told you everything. Now go and do something that matters. Or something that does not. I will be here either way.",
    "Come back in a century. I will have a better joke.",
]

# ----------------------------------------------------------------------------------------------- corkboard notes
NOTES = {
    "MRP": "Mr. POKéMON is FINNEGAN, an overdose that never ended.",
    "JOYCE": "JOYCE: Finnegan, Ahriman, Dajjal, Antichrist: one thing, four sets of eyes. The future writes letters to the past.",
    "BEETLE": N.NOTE_BEETLE,
    "SATOSHI": N.NOTE_SATOSHI,
    **N.NOTES,
    "BRUNO": "BRUNO: Teleoplexy. Time is a machine that eats lines. Kill him. He asked.",
    "GRAVE": "GRAVE: Marcus Fischer. First of Finnegan's. A toy monster sits beside it.",
    "CAPREAL": "POST: Mythologize Capitalism as a Demon or it destroys your psyche.",
    "TRUMPET": "TRUMPET: Merging the timelines is peace. A comfortable era is a human right.",
}
