"""The rare held-item boutiques: one shop in the mid-act plaza of every act, a living room with a clerk behind the table.

The names are built the way Pokemon names are: two real words run together, one half swallowed by the other, and the plain meaning
follows the way the Pokedex explains a species (PAWNDORA = pawn + Pandora).  The stock climbs with the act: the first boutique sells the
small held items, the third the ones that win games (Leftovers, Amulet Coin, Lucky Egg), and each sells two type boosters of its area's
theme.  The prices are set in data/items/attributes.asm."""
from .text import Text

# (shop name, what the name is made of, what the clerk says about the act)
SHOP = {
    "Tithe": ("PAWNDORA", "Pawn plus Pandora. Open the box. Regret is sold separately.",
              ["Every item here was somebody's last hope. Now it's your first mistake.",
               "A better class of last hope in this district. Slightly warmer.",
               "The good stuff. Don't ask where from. The Parish already did."]),
    "Grove": ("BARTEROOT", "Barter plus root. Cash only. Roots are not legal tender. I checked.",
              ["Everything is held in common. Mostly in my hands.",
               "These came off the orchard's best people. They don't need them anymore.",
               "The Hearth's own stock. Please leave the receipt under a tree."]),
    "Axiom": ("ESCROWBOT", "Escrow plus robot. Your funds are held in trust. Mine too. Everyone's, really.",
              ["Item condition: acceptable. Item provenance: redacted.",
               "Premium inventory. Each item has a certificate. The certificate has an item.",
               "Class A holdings. Handle with the forms attached."]),
    "Lotus": ("TRADEWIND", "Trade plus wind. Items drift in on the tide. Prices drift out.",
              ["Take your time. Take everything. I'll take the money.",
               "A lovely selection. The sea gave it back. The sea has regrets.",
               "The best the shore ever coughed up. Cash, please. The ocean doesn't do cards."]),
    "Dis": ("DEVILDEAL", "Devil plus deal. Read the contract. Nobody reads the contract. I'll wait.",
            ["Cheap, and the cost is mostly spiritual.",
             "Better goods, steeper fine print. Sign here. Or here. Here is also fine.",
             "Our finest. Nobody leaves unchanged. Prices are in cash. For now."]),
}

TIER = [  # what every boutique of that act sells, before the two boosters
    ["BRIGHTPOWDER", "SMOKE_BALL", "QUICK_CLAW", "FOCUS_BAND"],
    ["SCOPE_LENS", "KINGS_ROCK", "CLEANSE_TAG", "EVERSTONE"],
    ["LEFTOVERS", "AMULET_COIN", "LUCKY_EGG", "SCOPE_LENS"],
]

BOOST = {  # the type boosters of the area's theme, two to a shop, a different pair in every act
    "Tithe": ["BLACKGLASSES", "BLACKBELT_I", "METAL_COAT", "SPELL_TAG"],
    "Grove": ["MIRACLE_SEED", "SILVERPOWDER", "POISON_BARB", "SOFT_SAND"],
    "Axiom": ["METAL_COAT", "MAGNET", "TWISTEDSPOON", "HARD_STONE"],
    "Lotus": ["MYSTIC_WATER", "SHARP_BEAK", "NEVERMELTICE", "SOFT_SAND"],
    "Dis": ["CHARCOAL", "SPELL_TAG", "BLACKGLASSES", "DRAGON_SCALE"],
}


def stock(tag, act):
    """Item constants for the boutique of act 0..2 of area `tag`."""
    b = BOOST[tag]
    items = list(TIER[act]) + [b[act], b[act + 1]]
    return list(dict.fromkeys(items))


def spec(tag, act):
    name, gloss, lines = SHOP[tag]
    return dict(items=stock(tag, act), greet=Text(f"{name}. {gloss} {lines[act]}"))
