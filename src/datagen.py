# Data Generation & Storage

# generate cards

import random


def generate_deck():
    #suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    #ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    #deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
    
    #create list of 26 Red and 26 Black
    red_list = [f"R" for i in range(1, 27)]
    black_list = [f"B" for i in range(27, 53)]
    deck = red_list + black_list

    return deck

# shuffle
shuffled_decks = []
for iter in range(1, 3):
    deck = generate_deck()
    random.shuffle(deck)
    condensed_deck = "".join(deck)

    shuffled_decks.append(condensed_deck)
    
#print(shuffled_decks[0][0:3])

print(shuffled_decks)
print(type(shuffled_decks[0]))
deck_1 = shuffled_decks[0]
print(deck_1.count('R'))
# store the raw deck data
# try to not use .csv
