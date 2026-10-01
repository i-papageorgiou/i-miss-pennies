# i-miss-pennies
By: Ilias Papageorgiou & Natasha Guharoy

## Background

In Penney's Game, two players each choose a pattern of three coin flips, such as Heads-Heads-Tails. Player 1 picks first, then Player 2 picks a different pattern after seeing it. A coin is flipped over and over, and whoever's pattern shows up first wins. You might expect every pattern to be equally good, but they aren't: whatever Player 1 picks, Player 2 can always choose a pattern that tends to come up first. Going second is the advantage.

The Humble-Nishiyama (H-N) Game plays the same idea with a standard deck of 26 red and 26 black cards. Players pick three-color patterns (like Red-Black-Red), and cards are turned over one at a time into a pile. When a player's pattern appears, they take the pile (a "trick"), and play continues with the rest of the deck. Cards left over at the end don't count. There are two ways to decide the winner. In the trick version, the player who won more piles wins. In the card version, the player who collected more cards wins, so taking a few big piles can beat taking many small ones. In our code, the trick version is v1 and the card version is v2. 

## Our Project

This project uses computer simulation to find the best strategy in the H-N card game and to check whether that strategy depends on how the game is scored. The code shuffles millions of decks and plays every possible pairing of three-color patterns on each one. It plays each pairing under both the trick version and the card version and records how often Player 2 wins, loses, or ties. Those results become heatmaps that show which reply works best against each of Player 1's choices. Comparing the two heatmaps shows whether Player 2's winning advantage from Penney's coin game carries over to the card game, and whether counting tricks or counting cards changes which pattern is the best pick.

## How to Run

Requirements: Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).

1. Install the dependencies:
   ```sh
   uv sync
   ```
2. Run the simulation:
   ```sh
   uv run python main.py
   ```
   The program asks how many more decks you want to add.
   - Enter a number (for example `1000`) to shuffle that many new decks and add them to the saved decks in `data/shuffled_decks.bin`. The program then plays both versions of the game on every saved deck and redraws the heatmaps.
   - Enter `0` to open the current heatmaps without running anything new.
3. View the results. The heatmaps are saved to:
   - `figures/matchup_heatmap_v1.png`: trick version (most piles wins)
   - `figures/matchup_heatmap_v2.png`: card version (most cards wins)

Additional Options

| Option | What it does | Default |
|---|---|---|
| `--add-decks N` | Adds N decks without asking (`0` shows the current heatmaps) | asks you |
| `--input PATH` | The file where the decks are saved | `data/shuffled_decks.bin` |
| `--output PATH` | Base name for the heatmap images (`_v1`/`_v2` gets added) | `figures/matchup_heatmap.png` |

Example: `uv run python main.py --add-decks 1000`

**Note:** each run replays *every* saved deck, not only the new ones. The saved file already holds millions of decks, so a run can take a long time.

## Findings

After playing 4,000,000 shuffled decks under each scoring rule, the second player has a large advantage in both versions of the game. Whatever the first player picks, the second player can reply with a pattern that wins at least 80% of decks when counting tricks and at least 92% when counting cards. The best reply usually follows the same rule as Penney's coin game: take the opposite of the first player's middle color, then add the first player's first two colors. For example, against BRB, reply BBR. The first player can't avoid being at a disadvantage, but picking BRB or RBR makes them hardest to beat. Even against the best reply, the first player still wins about 12% of decks when counting tricks and about 7% when counting cards.

The two versions mostly agree. The best reply is the same for 6 of the 8 possible patterns. The exceptions are BRB and RBR. Against those, the top two replies (BBR and RRB) are nearly tied when counting tricks (80% vs. 79%), but player 2 pulls ahead when counting cards (92% vs. 86%). Counting cards also makes the second player's advantage stronger and ties much rarer: ties happen in at most 4% of decks, compared with up to 35% when counting tricks. Overall, the same strategies win in both versions. The card version just makes the gap between good and bad choices wider.
