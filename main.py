"""Analyze packed decks and save a matchup heatmap."""
import argparse

from src.dataproc import analyze_file
from src.dataviz import plot_heatmap


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="data/shuffled_decks10.bin")
    parser.add_argument("--num-decks", type=int, default=10)
    parser.add_argument("--output", default="figures/matchup_heatmap.png")
    args = parser.parse_args()
    results, num_decks = analyze_file(args.input, args.num_decks)
    plot_heatmap(results, num_decks, args.output)
    print(f"Analyzed {num_decks:,} decks. Heatmap saved to {args.output}")


if __name__ == "__main__":
    main()
