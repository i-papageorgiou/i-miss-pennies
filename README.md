# i-miss-pennies

Generate a matchup heatmap from the existing packed decks:

```sh
python main.py
```

The chart is saved to `figures/matchup_heatmap.png`. For another dataset:

```sh
python main.py --input data/shuffled_decks1000.bin --num-decks 1000 --output figures/matchup_heatmap1000.png
```

Columns show the first player's choice; rows show the second player's response.
R means red (0), and B means black (1). Each cell lists the second player's
deck wins, losses, and ties. The player taking more tricks wins the deck.
After a matching pattern wins a trick, the entire pile through that pattern
is discarded and play starts again with the remaining cards.

Teal indicates an advantage for the response and brown for the first choice.
Color measures `(wins - losses) / decks`, including tied decks in the denominator.
Black outlines mark the best observed response(s) within each column; these
are sample results, not guarantees. Identical choices are excluded.

Run scoring checks with `python -m unittest discover -s tests`.

