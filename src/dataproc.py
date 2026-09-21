# Data Processing - scoring and summarizing 
import pandas as pd

decks = pd.read_csv("data/shuffled_decks10.txt", header=None, names=["deck"])
print(decks.head())
card_comb = ["000", "111", ]
# ensure simulation is running unique instances every run

# shuffle the deck on each iter

