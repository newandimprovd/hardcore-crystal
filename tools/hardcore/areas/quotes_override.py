"""Exact quotations from the writers of the game.

The lines the characters speak as quotations are written in the manner of the author, because the real text of a book is not copied into
this repository by the generator.  If you want the real words in the game, paste them here as a plain string under the key (the keys are
listed below) and regenerate: the entry replaces the written line wherever the key is used.  Keep every quotation to what fits the text
box, around two to four short lines, and put the author's own punctuation in it.

Keys in use:
  CROWLEY_WHITE_STAINS   the lines of the hymn Crowley speaks at the playground (WHITE STAINS)
  CROWLEY_LAW            the line about the Law that he repeats in the Amphitheater (THE BOOK OF THE LAW)
"""
QUOTES = {}


def q(key, default):
    return QUOTES.get(key, default)
