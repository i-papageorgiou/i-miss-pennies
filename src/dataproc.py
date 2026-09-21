# Data Processing - scoring and summarizing 
print('Running imports')
import pandas as pd

#this is to unpack the bitpacked file
def unpack_bit_list(packed_bytes, original_length):
    bit_list = []
    
    for byte_val in packed_bytes:
        # Extract 8 bits from each byte
        for bit_index in range(8):
            if len(bit_list) < original_length:
                bit = (byte_val >> bit_index) & 1
                bit_list.append(bit)
                
    return bit_list

decks = pd.read_csv("data/shuffled_decks10.txt", header=None, names=["deck"])
print(decks.head())
card_comb = ["000", "111", ]
# ensure simulation is running unique instances every run

# shuffle the deck on each iter

