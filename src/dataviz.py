"""Draw matchup results with red/black pattern labels."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

from src.dataproc import CARD_COMBINATIONS


SCORING_RULES = {1: "most tricks wins", 2: "most cards wins"}

#CURRENT FEEDBACK
#heatmap has transposed results. Want the win rate for us to be better
#follow his heatmap format

def plot_heatmap(results, num_decks, output="figures/matchup_heatmap_v1.png", version=1):
    if num_decks < 1:
        raise ValueError("At least one deck is required.")
    patterns = CARD_COMBINATIONS
    labels = [p.translate(str.maketrans("01", "RB")) for p in patterns]
    advantage = np.full((8, 8), np.nan)
    for column, first in enumerate(patterns):
        for row, second in enumerate(patterns):
            if first != second:
                result = results[first, second]
                advantage[row, column] = (result["wins"] - result["losses"]) / num_decks

    fig, ax = plt.subplots(figsize=(12, 10), constrained_layout=True)
    cmap = plt.get_cmap("BrBG").copy()
    cmap.set_bad("#e5e7eb")
    chart = ax.imshow(np.ma.masked_invalid(advantage), cmap=cmap, vmin=-1, vmax=1)
    for column, first in enumerate(patterns):
        best = np.nanmax(advantage[:, column])
        for row, second in enumerate(patterns):
            if first == second:
                ax.text(column, row, "-", ha="center", va="center", color="#555555")
                continue
            result = results[first, second]
            value = advantage[row, column]
            label = f"{result['wins']} W / {result['losses']} L\n{result['ties']} ties"
            ax.text(column, row, label, ha="center", va="center", fontsize=9,
                    color="white" if abs(value) >= 0.6 else "#111111")
            if np.isclose(value, best):
                ax.add_patch(Rectangle((column - .46, row - .46), .92, .92,
                                       fill=False, edgecolor="black", linewidth=2.5))
    ax.set_xticks(range(8), labels)
    ax.set_yticks(range(8), labels)
    ax.set_xlabel("First player's combination", fontsize=12)
    ax.set_ylabel("Second player's response", fontsize=12)
    ax.set_title(f"Nishiyama's game (v{version}) - {num_decks:,} decks analyzed\n"
                 f"Deck wins and losses for the second player ({SCORING_RULES[version]})", pad=18)
    bar = fig.colorbar(chart, ax=ax, shrink=.8)
    bar.set_label("Second-player advantage: (wins - losses) / decks")
    fig.supxlabel("R = red (0) | B = black (1)\n"
                  "Teal: response wins more | Brown: first choice wins more\n"
                  "Black outline: best response(s) in each column, including equal results", fontsize=10)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    return fig
