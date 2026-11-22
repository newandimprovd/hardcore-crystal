"""Dialogue pools of the hollows: small hidden caves behind a gap in the tree line, two to an area.  One pool per area, in the voice of the place.
Every pool has SEEN (before the fight), BEATEN, AFTER lists.  Short lines, the generator wraps them."""

TITHE = dict(
    seen=[
        "Soup is for the faithful. You smell like a visitor. Battle.",
        "We hide the donations down here. From the Church. From the poor. From ourselves.",
        "The Lord provides. I provide the part where you lose.",
        "Mind the bones. Some of them are still paying rent.",
        "I took a vow of silence. I am breaking it for this. Specifically for this.",
        "Forgive me, I am about to be very unforgiving.",
        "A penny for your thoughts. A fight for your trespass.",
        "Brother Anselm is not in. Brother Anselm has not been in since the Lent of the incident.",
        "This cellar has a roof, a rule and a rat. You are breaking two.",
        "Kneel. Or fall. The floor does not care which.",
        "Every candle down here is a prayer. Every prayer is a complaint.",
        "Do you have a donation slip? No? Then you will donate your time. In pain.",
    ],
    beaten=[
        "Mercy. I was told there would be mercy. I was misinformed.",
        "I fall. The ground receives me. It is the only thing that ever did.",
        "Bless you. Genuinely. Please leave.",
        "That was divine. Mostly the part where it ended.",
        "I will say a prayer for you. It will be about the stairs.",
        "The soup was not even that good.",
        "Amen. And also ow.",
        "Take what you came for. The saints are looking away. They are good at it.",
    ],
    after=[
        "The candles burn down here without anyone lighting them. Do not ask.",
        "Somewhere above, a bell rings for a sin nobody has committed yet.",
        "I have forgiven you. It cost me nothing. That is the nature of forgiveness.",
        "Take the long way out. The short way has Brother Anselm.",
        "The soup is cold. The soup was always cold. Tradition.",
        "You should confess. To someone. Preferably not to me. I would remember.",
        "Down here the dead and the poor share a room. The dead complain less.",
        "Do come back. We have a lot of floor to cover.",
    ])

GROVE = dict(
    seen=[
        "The oak remembers every footstep. It remembers yours. It is unimpressed.",
        "We came here to leave the world. The world followed. I am angry about it.",
        "Moss grows on the north side of everything. I grow on the north side of you. Battle.",
        "I have not spoken to a living soul in a year. You will have to do.",
        "Shh. The roots are listening. They report to the mushrooms.",
        "My herbal tea is steeping. You have exactly one fight to spare.",
        "Peace is a great thing. Let me demonstrate by ending yours.",
        "The commune said I could stay if I stayed out of sight. I took it literally.",
        "I was a mother, a baker and a mystic. Now I am a hollow. You are a visitor.",
        "Take off your shoes. Not for respect. For the fight. It is a long story.",
        "Every tree here has a name and a grievance. Mine is Gerald.",
        "The old ones say do no harm. The old ones are not here. Battle.",
    ],
    beaten=[
        "Beaten by a stranger in a tree. I will tell the squirrels. They gossip.",
        "The roots hold me. Gently. Contemptuously.",
        "Fine. I yield. I was going to yield anyway. Tuesdays I yield.",
        "May your path be soft and your shoes be dry.",
        "The forest forgives. I only pretend.",
        "You fight like the weather. Without apology.",
        "Compost me. I have earned it.",
        "That stung. The nettles are jealous.",
    ],
    after=[
        "The oak is older than the commune. It will outlast the next one too.",
        "Take a leaf from the floor. It is the only free thing down here.",
        "I keep the hollow tidy. The hollow does not thank me. Neither do you.",
        "The gift is for people who find me. You found me. Congratulations on being nosy.",
        "There is another hollow somewhere on these roads. It has more moss and more attitude.",
        "Do not tell the commune. They would charge admission.",
        "A forest is just patience with leaves.",
        "Leave the way you came. Stepping somewhere new is how people start religions.",
    ])

AXIOM = dict(
    seen=[
        "This room is not on the floor plan. You are not on the visitor log. Battle.",
        "Form 27-B requires a fight. I am the form.",
        "I am between meetings. The meetings are between me. Fight.",
        "Break time ends in four minutes. I will use all four on you.",
        "You are in a room no budget approved. I enforce it anyway.",
        "Please take a number. The number is seven. The fight is now.",
        "Nobody ever comes here. Nobody ever leaves. We have a very low churn rate.",
        "My badge says Supervisor. My ID says Temp. My heart says Fight.",
        "The coffee machine is broken. The coffee machine is also my boss. Battle.",
        "I was promised a promotion. I got this closet. I have a lot of feelings.",
        "Efficiency is a form of violence. Allow me to be efficient.",
        "Per my last email. Per my last battle. Per my last mercy.",
    ],
    beaten=[
        "Noted. Escalating to nobody.",
        "Resignation accepted. Mine.",
        "Filed under unfortunate. Cross referenced under Tuesday.",
        "That is going in my performance review.",
        "Task complete. The task was losing.",
        "I will circle back. Never. But I will circle.",
        "Please rate this fight. One star. Out of respect.",
        "Out of office until the heat death.",
    ],
    after=[
        "This room does not exist. Neither do I. It is very freeing.",
        "There is a gift behind the filing cabinet. Do not open the cabinet.",
        "Meetings here run long. The last one began before the founding of the city.",
        "Take the stairs. The elevator keeps asking how you feel.",
        "You have no clearance. You also have no witnesses. Congratulations.",
        "I will keep this between me and the compliance department.",
        "The break room has a plant. The plant has tenure.",
        "Please leave quietly. The walls take notes.",
    ])

LOTUS = dict(
    seen=[
        "The pool was drained for maintenance. The maintenance was drained for budget. I remain.",
        "Welcome to paradise. The towels are extra. The fight is complimentary.",
        "I was a guest once. Checkout was in the contract. Fine print is a lifestyle.",
        "The tide went out and took the staff. I am what is left of hospitality.",
        "Sun cream. Sun cream. Sun cream. Sun cream. Battle.",
        "All inclusive means all of us are included. Welcome to the lower floor.",
        "The cabana boy is dead. Long live the cabana boy. That is me. Fight.",
        "No lifeguard on duty. There is me, which is worse.",
        "The sea does not want you. Neither does the buffet. Battle.",
        "I am on holiday. It has lasted nine years. I am furious about it.",
        "Do you hear the waves? Those are the pipes. The waves left.",
        "Sand gets everywhere. So do I. Mostly into your plans.",
    ],
    beaten=[
        "Washed up. Again.",
        "Leave a review. Leave it very low.",
        "The sea takes some. You took me. Same energy.",
        "I deserve this. The pool deserves better.",
        "Refund denied. Refund denied. Fight denied.",
        "That was less relaxing than advertised.",
        "Out for the season. All seasons.",
        "Pass the sun cream. I have a feeling I will need it.",
    ],
    after=[
        "The deep end is dry. Do not go in. It has a view of the abyss.",
        "There is a gift in the locker. The locker is mostly lint.",
        "They tell you the sun is good for you. They lie. Everyone down here lies.",
        "Leave your name at the desk. There is no desk. Leave it anyway.",
        "The tide will come back. It always lies about that too.",
        "The last cabana is the best cabana. The best cabana has the ghosts.",
        "Wave if you see anyone. No one waves back. That is the resort experience.",
        "Drink something. Anything. It is all the same drink.",
    ])

DIS = dict(
    seen=[
        "Sentence handed down. Appeal denied. Fight now.",
        "I filed you under Damnation. You were filed incorrectly. I will fix it.",
        "Welcome to the pit. We kept your file. It is very thick.",
        "Fire is merely a bad idea that caught on. I will show you.",
        "I am a clerk of eternal suffering. I take lunch at three.",
        "Order. Order! No. Not that kind. The other kind.",
        "Your name is on a list. The list is on fire. Fight.",
        "The pit is full. The pit has always been full. You are an exception and the pit is rude about it.",
        "I judge you. It is my only talent. Sadly it is also my hobby.",
        "Do not mind the screaming. It is the ventilation.",
        "Hell is other people. I am other people. Battle.",
        "I have waited a thousand years for a case. Yours will do.",
    ],
    beaten=[
        "Overruled. By you. Delightful.",
        "The flames have gone out. I take it personally.",
        "Appeal granted. Retroactively. Bring a lawyer next time.",
        "That was a fair verdict. I hate fair.",
        "Fine. Take your item. Take your sins. Take mine.",
        "Damnation postponed pending paperwork.",
        "I am not mad. I am eternal. It reads the same.",
        "You win this ring. There are nine.",
    ],
    after=[
        "The files go down forever. The prizes sit at the bottom. Mind the heat.",
        "Every drawer here is a sin. This one is greed. Do not open it.",
        "The furnace is off. For once. It was a good day for the damned.",
        "You do not belong here. Neither do I. It is the one thing we share.",
        "The gifts are the only real thing in the building.",
        "Come again. Bring snacks. We have not eaten since the last reformation.",
        "Leave the way you came. The other ways have meetings.",
        "I will remember you. Mostly because I am forbidden from forgetting.",
    ])

POOLS = {"HL1": TITHE, "HL2": GROVE, "HL3": AXIOM, "HL4": LOTUS, "HL5": DIS}

# the plaques: a sign by the ladder that names the place, and a longer one at the far end
SIGNS = {
    "AlmsCellar": ("THE ALMS CELLAR. Soup served at all hours that have ended.",
                   "Chalk on the wall, in a careful hand: THIS CELLAR WAS DUG FOR THE POOR TO HIDE FROM THE CHARITY. THE CHARITY DUG ITS OWN. "
                   "THEY MET IN THE MIDDLE AND SHARED A SOUP. THEN THEY FOUGHT OVER THE LADLE. THE LADLE IS STILL MISSING."),
    "Ossuary": ("THE OSSUARY. Bones sorted by guilt.",
                "Each skull carries a number and a debt. The numbers are the parish's. The debts are the parish's too. Nobody has ever paid. "
                "The collection plate is a coffin lid. It is full."),
    "HollowOak": ("THE HOLLOW OAK. Please wipe your roots.",
                  "Carved into the heartwood: THE COMMUNE BEGAN HERE WITH THREE PEOPLE AND ONE ARGUMENT. THE ARGUMENT SURVIVED THE PEOPLE. "
                  "IT IS STILL BEING HELD. THE OAK HAS VOTED TO ABSTAIN."),
    "MossChapel": ("THE MOSS CHAPEL. No bells. The moss muffles them.",
                   "The altar is a stump with a brass plate: HERE THE FIRST ELDER FORGAVE THE FIRST THIEF. THE THIEF THANKED HER AND TOOK THE PLATE. "
                   "THIS ONE IS A REPLACEMENT. THE THIEF TOOK THAT TOO."),
    "SpareRoom": ("THE SPARE ROOM. Not on any plan. Not on any budget.",
                  "A laminated note: THIS ROOM WAS BUILT IN CASE THE CITY NEEDED A ROOM. THE CITY NEVER NEEDED A ROOM. THE CITY ONLY NEEDED A BUDGET LINE. "
                  "THE LINE STILL RUNS. THE ROOM STILL WAITS. SO DO WE."),
    "BreakRoom": ("THE BREAK ROOM. Break ends: never.",
                  "A calendar stuck on one date. Under it: THE LAST EMPLOYEE TO CLOCK OUT FROM HERE IS STILL ON HIS BREAK. WE DO NOT WAKE HIM. "
                  "HE IS THE ONLY ONE WHO HAS READ THE POLICY."),
    "DryPool": ("THE DRY POOL. No diving. No water. No hope. Enjoy.",
                "Tiles spell out a depth marker. THREE FEET. SIX FEET. NINE FEET. Then, in a different hand: DEEPER THAN ADVERTISED."),
    "LastCabana": ("THE LAST CABANA. Reserved for those who stayed.",
                   "A guest book, damp but legible. Every entry reads WONDERFUL STAY. Every entry is in the same handwriting. "
                   "The last line reads WE ARE STILL CHECKING OUT."),
    "FilingPit": ("THE FILING PIT. Sort by sin. Then by weight.",
                  "A card index the size of a hall. Under G, GREED, GLUTTONY, GRUDGE. Under M, MERCY, MISSING. Nothing is filed under F. "
                  "The clerk says forgiveness was never a category."),
    "FurnaceRoom": ("THE FURNACE ROOM. Warm to the touch. Warmer to the argument.",
                    "A brass dial reads LOW, MEDIUM, HIGH, JUST. The needle has been bent past JUST for centuries. The foreman's note says DO NOT TOUCH. "
                    "THE FURNACE HAS FEELINGS. THEY ARE ALL ABOUT YOU."),
}
