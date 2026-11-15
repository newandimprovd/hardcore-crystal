"""Debates and cultists.

DEBATES: per area, seven pairs of townsfolk who stand facing each other on a plaza and argue (one pair per plaza, the plaza number picks it).
Each pair is (the one on the left, the one on the right).  Philosophy, sex and money, dark comedy, no slur and nothing graphic: the joke is the argument.

CULT_SEEN / CULT_BEATEN: lines for the trainers who belong to FINNEGAN's wake.  They believe that dying by the player's hands is a ticket to a glorious
afterlife (the river that runs back to the start of the book), so they are not afraid of the fight, they are eager for it.  The lines are mixed into the
ordinary trainer pools of each area (areas/aN_text.py), so only some trainers are cultists.
"""

DEBATES = {
    "Tithe": [
        ("Tithing is theft with a choir. Ten percent, forever, to a man who has never seen my paycheck.",
         "Theft comes without a receipt. The Church gives you a receipt. It is called a soul."),
        ("The landlord is my father figure. Always above me, never calls, takes what he's owed.",
         "Your father figure has a name and a face. Your landlord has a limited liability company. That is a stepfather at best."),
        ("Confession is therapy with worse insurance.",
         "Therapy is confession with a bill. At least the priest has to keep it secret. Mostly. Sometimes. It's complicated."),
        ("Blessed are the poor, it says. Blessed with what? A cough? A view of the dumpster?",
         "With the best seats in heaven. The rich get standing room. Hell, I hear, has a cover charge and a dress code."),
        ("Celibacy is the purest romance. Forty years devoted to one hand.",
         "That is not purity, that is a monogamous relationship with a callus. Leave the Church out of it, it has enough on its plate."),
        ("The cops protect and serve. It's a menu. I've only ever been offered the second item.",
         "Protect and serve who? Whom. See, that's why I wasn't promoted. I corrected the commissioner."),
        ("Heaven is a queue. We're all just waiting for a number.",
         "Heaven is a queue with a premium lane. Ask the parish about the fast pass. Ask quietly. Ask in cash."),
    ],
    "Grove": [
        ("Free love works great until somebody leaves a dish in the sink.",
         "The dish is not the problem. The chore wheel is the problem. Love should be a wheel of chores and chores should be love."),
        ("Is it ethical to eat an apple that has seen things? These trees watch us all day.",
         "They watch us because we're beautiful. Also because we fertilize them with the compost. Also with the other thing. Eat the apple."),
        ("I have a spreadsheet for my four partners and a fifth tab for conflict. It's the happiest I've ever been.",
         "A fifth tab? I have a sixth, for the others' spreadsheets. We hold a meeting about it every full moon. It's ninety minutes of feelings."),
        ("The Great Hearth hums. That is not a furnace. That is a god doing breathing exercises.",
         "It's a furnace. I paid for the maintenance. If it is a god, it owes me a deposit."),
        ("Harvest-time nudity is a sacrament. We come into the world bare and we ought to leave the barn the same way.",
         "I say the sacrament is the hay. I have a rash that agrees with me. Wear a hat. Wear several."),
        ("Consensus means nobody leaves until we all agree. It's democracy at its most intimate.",
         "It's a hostage situation with snacks. Last month we decided about a gate for nine hours. The gate got old and died."),
        ("Every orgy is just a very long potluck.",
         "No no no. A potluck is voluntary and you know who brings what. An orgy is a potluck with a surprise ending and no casserole."),
    ],
    "Axiom": [
        ("Free will is a rounding error. The system rounds up and calls it a choice.",
         "Then who signs my timesheet? A rounding error does not file for overtime. I do. Free will is a payroll matter."),
        ("The dating application matched me with a man who has my exact fears. We have been miserable together for three weeks.",
         "That's perfect compatibility. Love is two people who lose to the same spreadsheet. Congratulations on the data."),
        ("The Mayoralty is not a person. It is a policy wearing a lanyard.",
         "I met the Mayor. He is a man. He is also a policy. He is a policy-shaped man who needs sleep, and who doesn't get it."),
        ("Efficiency in bed is a virtue. Eleven minutes, no reruns, a signed receipt.",
         "Eleven minutes? You've confused a performance review with intimacy. Though the receipt is a fine touch. I'd frame it."),
        ("Privacy is dead. I found out when a billboard recommended a lotion for me. By name. In a whisper.",
         "Privacy isn't dead. It's been outsourced. I get a nice quarterly statement of everything I'm hiding."),
        ("All people are fungible. Take one out, put one in. The tickets still print.",
         "Then why did the system cry when I left for a week? It sent me a survey. It never sends me surveys. I think it misses me."),
        ("The form is the soul, and the soul is a form, and the form must be filled in triplicate.",
         "In triplicate? Blasphemy. The soul is a form in quadruplicate. The fourth copy goes to God. He never replies. It's a tragic filing system."),
    ],
    "Lotus": [
        ("Pleasure is the only good. I've read the philosophers. The good ones had good wine.",
         "Pleasure is a shortcut and the road is the point. I say this from a hot tub, where I think best, with a drink I did not pay for."),
        ("An orgy needs an RSVP, a seating chart and a safe word that's also a vintage. Anything else is chaos.",
         "I disagree. The best ones have no plan and a very lenient waiter. You know it started well when somebody asks if the pool is heated, and nobody answers."),
        ("Boredom is the only sin. I say this as someone who's committed all the others.",
         "Boredom is the only punishment. The sins are the ones I enjoyed. The boredom is the bill."),
        ("A yacht is not a boat. It's a personality with a hull.",
         "My yacht is a boat and a therapist. It takes me out to sea to cry in the right light, and nobody has to hear it."),
        ("Regret is a luxury good. You have to afford the thing first.",
         "Regret is free and pays well. I've got a lifetime supply and a warehouse in a very tasteful beige."),
        ("Tantra is the slow food of sex. Four hours of breathing and then a modest, deeply meaningful snack.",
         "A quickie is fast food, and I'm not ashamed. Sometimes I want a burger. Sometimes I want a drive-through. Sometimes it's both, and a cheerful cashier."),
        ("Everything in moderation, including moderation.",
         "Moderation is a coward's excess. I'd rather commit fully to one thing and let it ruin me tastefully."),
    ],
    "Dis": [
        ("Hell is other people. Everyone says it as if Sartre had been to the lake.",
         "Hell is the commute. Other people are only the scenery. Sartre never sat on the late train in a place where the train is also on fire."),
        ("It would have been better never to have been born. Quite a few of us were consulted and said so.",
         "Then you're still arguing the point. A genuine pessimist would stop mid-sentence out of principle. You owe the argument a better ending."),
        ("Lust is the mildest sin. A hobby. A bad hobby with good lighting.",
         "Gluttony is a career. Lust is an internship. The big ones get a pension and a corner office in the lake."),
        ("The damned can't be bored. We are perpetually fascinated by the flames.",
         "The damned are bored beyond belief. The flames are the same flames. I've named them all. They're named after my exes."),
        ("The afterlife has a Human Resources department. I filed a complaint. It was approved. It was fatal.",
         "I've been in the waiting room for eleven years. It has a nice fern. The fern is also damned. It has a plaque."),
        ("Nobody in Dis is frigid. The lake took care of that centuries ago.",
         "That's physics, not romance. Besides, anybody can be lukewarm in a furnace. It takes a real devil to be tender at absolute zero."),
        ("FINNEGAN is the devil. Open and shut. He is the author, the reader and the disaster.",
         "He's a typo. A devil would be on time. Finnegan is a mistake that got promoted and then wrote a book."),
    ],
}

CULT_SEEN = {
    "Tithe": [
        "I am one of FINNEGAN's. My seat at the wake is booked. Send me ahead, friend.",
        "They say whoever falls to you gets a glorious afterlife. I would like a glorious afterlife. Please.",
        "The river runs backward at the end of the book. I'd like to be the first in. Aim for the neck.",
        "I paid my tithe to FINNEGAN. The receipt says one death, paid in full.",
        "I've read the last page. It says you come for us. Make it quick. Make it theological.",
    ],
    "Grove": [
        "The Commune taught me that all things return. FINNEGAN says it faster. Send me back, friend.",
        "We of the wake do not fear you. We are the compost of the next book. Please spread us well.",
        "I came to the Grove to find peace. FINNEGAN found me first. Take my hand. Then my life.",
        "Free love, free death. Those are the only two free things, and I'd like the second today.",
        "The apples told me you were coming. They said bring a towel. I brought the towel. Let's begin.",
    ],
    "Axiom": [
        "I am a member of FINNEGAN's wake. Your kill count is a rounding error in my favor. Proceed.",
        "Dying by your hands is a promotion. HR confirmed. It's in writing and signed by the river.",
        "My death will be a data point. FINNEGAN collects data points. He collects them in a very large and patient bucket.",
        "The wake has a loyalty program. Ten deaths, one free resurrection. I'm so close. Please help.",
        "You are the instrument of a grander process. I'd like to thank you in advance. Form 17 is attached.",
    ],
    "Lotus": [
        "I am here for a good time and a better death, courtesy of FINNEGAN's wake. Shall we?",
        "They say a death at your hands is the finest cocktail. I'd like mine shaken, not stirred, and bloody.",
        "We of the wake are very relaxed about dying. We are also very relaxed about everything. Please begin.",
        "FINNEGAN promised a glorious afterlife with a poolside bar. I read the fine print. It's fine print about the bar.",
        "A death in the afternoon. A river at dusk. That's all I want, friend. Spare the face.",
    ],
    "Dis": [
        "The wake is my church. You are the priest. Do your office, brother.",
        "Hell is already here. FINNEGAN says the exit is behind you. Send me through.",
        "I'm already damned. A death at your hands is the only upgrade on offer. Please.",
        "The river runs to the start of the book. I'd like to arrive early. Take me, friend.",
        "I die for FINNEGAN, for the loop, and for the discount. Mostly the discount.",
    ],
}

CULT_BEATEN = {
    "Tithe": [
        "Oh. The river. It runs backward. I see the wake. Thank you.",
        "A glorious afterlife, signed and stamped. I forgive you in advance. And in arrears.",
        "It's beautiful. There's a priest. There's a landlord. They are both so small.",
    ],
    "Grove": [
        "I feel the soil. It's warm. It's calling. Spread me well.",
        "The apples were right. They're always right. It's the pits.",
        "I'm going home. Tell the Commune my chore is done.",
    ],
    "Axiom": [
        "The data point is submitted. Thank you for your service. I'd like a receipt.",
        "Form accepted. The river approves. I feel properly filed.",
        "It's remarkably efficient. Eleven seconds. No reruns.",
    ],
    "Lotus": [
        "A good death, a good drink, a good light. Cheers, friend.",
        "The pool is heated. I can feel it. It's heaven. It's also a pool.",
        "Beautiful. Please tell the bartender I tipped in advance.",
    ],
    "Dis": [
        "Down is up. The lake is a river. I see FINNEGAN. He's waving. He's also a typo.",
        "I'm out. Oh, I'm out. It's so warm and it's all so far away.",
        "Thank you. I'll save you a seat at the wake. Bring snacks.",
    ],
}
