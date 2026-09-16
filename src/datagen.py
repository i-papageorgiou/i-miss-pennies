# Data Generation & Storage

# generate cards

import random


def generate_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
    return deck

# shuffle

for iter in range(1, 11):
    deck = generate_deck()
    deck_items = list(deck.items())
    random.shuffle(deck_items)
    shuffled_deck = dict(deck_items)
    # store the shuffled deck in a variable named Deck_{iter}
    globals()[f'Deck_{iter}'] = shuffled_deck

# store the raw deck data
# try to not use .csv