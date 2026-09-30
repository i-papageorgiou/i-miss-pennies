"""Draw matchup results with red/black pattern labels."""
from pathlib import Path

import matplotlib.pyplot as plt
from main import log_calls
import numpy as np

from src.dataproc import CARD_COMBINATIONS


SCORING_RULES = {1: "Tricks", 2: "Cards"}

# Plot a heatmap of the matchup results.
def plot_heatmap(results: dict, num_decks: int, output: Path = Path("figures/matchup_heatmap_v1.png"), version: int = 1):
    
    # Validate the number of decks.
    if num_decks < 1:
        raise ValueError("At least one deck is required.")
    
    # Get the patterns and labels for the heatmap.
    patterns = CARD_COMBINATIONS[::-1]
    labels = [p.translate(str.maketrans("01", "RB")) for p in patterns]
    advantage = np.full((8, 8), np.nan)
    for column, first in enumerate(patterns):
        for row, second in enumerate(patterns):
            if first != second:
                # Results count wins for the second choice: the column (me).
                result = results[second, first]
                advantage[row, column] = result["wins"] / num_decks

    # Create the heatmap figure.
    fig, ax = plt.subplots(figsize=(9, 9), constrained_layout=True)
    cmap = plt.get_cmap("Purples").copy()
    cmap.set_bad("lightgray")
    ax.imshow(np.ma.masked_invalid(advantage), cmap=cmap, vmin=0, vmax=1)
    for column, first in enumerate(patterns): # Add text labels for each cell in the heatmap.
        for row, second in enumerate(patterns):
            if first == second:
                continue
            result = results[second, first]
            value = advantage[row, column]
            label = f"{int(round(100 * value))}({int(round(100 * result['ties'] / num_decks))})" # Add text labels for each cell in the heatmap.
            ax.text(column, row, label, ha="center", va="center", fontsize=11,
                    color="white" if value >= 0.5 else "#111111")
    ax.set_xticks(range(8), labels)
    ax.set_yticks(range(8), labels)
    ax.set_xticks(np.arange(-.5, 8, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 8, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlabel("My Choice", fontsize=12)
    ax.set_ylabel("Opponent Choice", fontsize=12)
    ax.set_title("My Probability of Win(Tie)\n"
                 f"Scoring By {SCORING_RULES[version]}\nN={num_decks:,}", fontsize=14) # Save the heatmap figure to the specified output path.
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    return fig
