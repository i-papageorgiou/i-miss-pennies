# Data Generation & Storage

# generate cards

import random


def generate_deck():
    red_list = [f"0" for i in range(1, 27)]
    black_list = [f"1" for i in range(27, 53)]
    deck = red_list + black_list

    return deck

def shuffle_deck(rounds):
    shuffled_decks = []
    for iter in range(0, rounds):
        deck = generate_deck()
        random.shuffle(deck)
        condensed_deck = "".join(deck)

        shuffled_decks.append(condensed_deck)
    return shuffled_decks

# save the shuffled decks to a file in the data subfolder
def save_decks_to_file(shuffled_decks, filename):
    with open(filename, "w") as f:
        for deck in shuffled_decks:
            f.write(deck + "\n")

shuffle_decks = shuffle_deck(10)
save_decks_to_file(shuffle_decks, "data/shuffled_decks10.txt")