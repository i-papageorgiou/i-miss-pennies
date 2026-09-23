# Data Processing - scoring and summarizing 
print('Running imports')
import pandas as pd

#this is to unpack the bitpacked file
def unpack_bit_list(packed_bytes, num_decks):
    bit_list = []
    original_length = num_decks * 52
    
    for byte_val in packed_bytes:
        # Extract 8 bits from each byte
        for bit_index in range(8):
            if len(bit_list) < original_length:
                bit = (byte_val >> bit_index) & 1
                bit_list.append(bit)
                
    return bit_list

print("Unpacking bit list from file...")
test_run = unpack_bit_list(open("data/shuffled_decks10.bin", "rb").read(), 10)
#print(test_run)

# turn bit_list decks into strings
def convert_to_strings(bit_list, num_decks):
    deck_strings = []
    for i in range(num_decks):
        start_index = i * 52
        end_index = start_index + 52
        deck_string = ''.join(str(bit) for bit in bit_list[start_index:end_index])
        deck_strings.append(deck_string)
    return deck_strings

card_comb = ['000', '001', '010', '011', '100', '101', '110', '111']
card_comb_simple = ['000', '001']

test2_run = convert_to_strings(test_run, 10)
#print(test2_run)

# Version 1: count the tricks in each deck and return a list of counts
# the same card cannot be counted for 2 tricks, so we will use a set to keep track of the cards that have been counted
# tricks are defined as the card_combinations in the card_comb list, so we will check for each card in the deck if it is in the card_comb list and if it has not been counted yet, we will increment the count and add it to the counted_cards set
# every round should assign player 1 a card_comb and player 2 a different card_comb
# it has to match the exact card_comb, so if player 1 has 000, player 2 cannot have 000, but can have any other card_comb
# to score a trick, it there must be all 3 cards in a row when pulling the shuffled deck
# for example, if the first 3 cards are 0, 1 and 0, then player 1 has 010 and player 2 has 101, so player 1 wins the trick and gets a point
# but then if the next card is 1, fulfilling player 2's 101, then player 2 does not win the trick because player 1 won a trick with some overlapping cards

def count_tricks(deck_strings, card_comb):
    print("Starting trick counting...")
    for comb_idx in card_comb:
        p1_comb = card_comb[comb_idx]
        print(f"Player 1 Combination: {p1_comb}")

        for comb_idx2 in card_comb:
            if comb_idx2 != comb_idx:
                p2_comb = card_comb[comb_idx2]
                print(f"Player 2 Combination: {p2_comb}")
                for deck in deck_strings:
                    p1_count = 0
                    p2_count = 0
                    cards_left = 52
                    print(f"cards left: {cards_left}")

                    while cards_left >= 3:
                        p1_trick_loc = deck.find(p1_comb)
                        p2_trick_loc = deck.find(p2_comb)
                        print(f"Player 1 trick loc: {p1_trick_loc}, Player 2 trick loc: {p2_trick_loc}")

                        if p1_trick_loc < p2_trick_loc and p1_trick_loc != -1:
                            p1_count += 1
                            deck = deck[p1_trick_loc + 3:]
                            cards_left -= 3
                            print(f"Player 1 wins a trick! New deck: {deck}, cards left: {cards_left}")

                        elif p2_trick_loc < p1_trick_loc and p2_trick_loc != -1:
                            p2_count += 1
                            deck = deck[p2_trick_loc + 3:]
                            cards_left -= 3
                            print(f"Player 2 wins a trick! New deck: {deck}, cards left: {cards_left}")

                    # print(f"Deck: {deck}, Player 1 Combination: {p1_comb}, Player 2 Combination: {p2_comb}, Player 1 Tricks: {p1_count}, Player 2 Tricks: {p2_count}")

            else:
                continue

print("beginning trick counting test...")
test3_run = count_tricks(test2_run, card_comb_simple)
print(test3_run)
