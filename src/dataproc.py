# Data Processing - scoring and summarizing 
print('Running imports')
import pandas as pd


def main():
    print('Entered main')
    decks = pd.read_csv("data/shuffled_decks10.txt", header=None, names=["deck"])
    print('imported file')
    print(decks.head())
    card_comb = ["000", "001", "010", "011", "100", "101", "110", "111"]
    print('done')