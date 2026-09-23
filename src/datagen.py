# Data Generation & Storage
# generate cards

import random


def generate_deck():
    red_list = [0 for i in range(1, 27)]
    black_list = [1 for i in range(27, 53)]
    deck = red_list + black_list

    return deck

#shuffle the integer lists
def shuffle_deck(rounds):
    shuffled_decks = []
    for iter in range(0, rounds):
        deck = generate_deck()
        random.shuffle(deck)
        shuffled_decks.extend(deck)

    return shuffled_decks

#FUNCTIION for bitpacking
#will replace save_decks_to_file
def pack_bit_list(shuffled_decks):
    packed_bytes = bytearray()
    
    # Process the list in chunks of 8 bits
    for i in range(0, len(shuffled_decks), 8):
        chunk = shuffled_decks[i:i+8]
        byte_val = 0
        
        # Pack up to 8 bits into a single integer
        for bit_index, bit in enumerate(chunk):
            byte_val |= (bit << bit_index)
            
        packed_bytes.append(byte_val)

    return packed_bytes

        # save the shuffled decks to a file in the data subfolder
def save_decks_to_file(packed_bytes, filename):
    with open(filename, "wb") as f:
        f.write(packed_bytes)

shuffle_decks = shuffle_deck(10)
decks_bit_list = pack_bit_list(shuffle_decks)
save_decks_to_file(decks_bit_list, "data/shuffled_decks10.bin")