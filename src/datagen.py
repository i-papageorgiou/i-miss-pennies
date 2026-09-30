# Data Generation & Storage
# generate cards

import random
from pathlib import Path
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = PROJECT_ROOT / "data/shuffled_decks.bin"
LEGACY_DATA = PROJECT_ROOT / "data/shuffled_decks10.bin"

# generate a deck of 52 cards with 0s and 1s
def generate_deck():
    red_list = [0 for i in range(1, 27)]
    black_list = [1 for i in range(27, 53)]
    deck = red_list + black_list

    return deck

# shuffle the integer lists (aka decks) and return a list of shuffled decks
def shuffle_deck(rounds: int) -> list:
    shuffled_decks = []
    for iter in range(0, rounds):
        deck = generate_deck()
        random.shuffle(deck)
        shuffled_decks.extend(deck)

    return shuffled_decks

# function for bitpacking
def pack_bit_list(shuffled_decks: list) -> bytearray:
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
def save_decks_to_file(packed_bytes: bytearray, filename: Path):
    with open(filename, "wb") as f:
        f.write(packed_bytes)

# Preserve old cards and append new decks, repacking any padding bits.
def add_decks(number: int, filename: Path = DEFAULT_DATA, seed_file: Path = LEGACY_DATA):

    # Validate the input number of decks.
    if not isinstance(number, int) or number < 0:
        raise ValueError("The number of additional decks must be a nonnegative integer.")
    
    # Use the seed file only if the default data file is empty or missing.
    filename = Path(filename)
    source = filename if filename.exists() else seed_file
    packed = Path(source).read_bytes() if source is not None and Path(source).exists() else b""
    previous_count = len(packed) * 8 // 52

    # Validate that the existing file contains complete decks.
    if len(packed) != (previous_count * 52 + 7) // 8:
        raise ValueError("Existing file does not contain complete packed decks.")
    
    # Unpack the existing decks into a list of bits.
    bits = [(packed[i // 8] >> (i % 8)) & 1 for i in range(previous_count * 52)]
    
    # Validate that at least one deck will be present after adding the new decks.
    if previous_count + number == 0:
        raise ValueError("Add at least one deck to start a dataset.")
    
    # Generate and append the new shuffled decks to the list of bits.
    bits.extend(shuffle_deck(number))
    filename.parent.mkdir(parents=True, exist_ok=True)

    # Replace only after the entire combined dataset has been written.
    temporary = filename.with_suffix(filename.suffix + ".tmp")
    save_decks_to_file(pack_bit_list(bits), temporary)
    temporary.replace(filename)
    return previous_count + number

# Show saved heatmap images without re-analyzing the decks.
def show_heatmaps(paths: list):
    for path in paths:
        fig, ax = plt.subplots(figsize=(9, 9), constrained_layout=True)
        ax.imshow(plt.imread(path))
        ax.axis("off")
        fig.canvas.manager.set_window_title(path.name)
    plt.show()

def main():
    import argparse
    # Support both `python src/datagen.py` and importing from main.py.
    if __package__ in (None, ""):
        import sys
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.dataproc import analyze_file
    from src.dataviz import plot_heatmap

    parser = argparse.ArgumentParser(description="Add shuffled decks and regenerate the heatmap.")
    parser.add_argument("--input", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--add-decks", type=int, help="Skip the prompt; 0 shows current heatmap.")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "figures/matchup_heatmap.png",
                        help="Base path; _v1/_v2 is appended to the file name.")
    args = parser.parse_args()
    number = args.add_decks
    while number is None:
        try:
            number = int(input("How many more decks would you like to analyze? (0 to show current heatmap): "))
            if number == 0:
                print("Showing current heatmap only.")
            if number < 0:
                raise ValueError
        except ValueError:
            print("Please enter a whole number of zero or more.")
            number = None
    outputs = [args.output.with_stem(f"{args.output.stem}_v{version}") for version in (1, 2)]
    if number == 0:
        missing = [output for output in outputs if not output.exists()]
        if missing:
            parser.exit(1, f"Error: no heatmap found at {missing[0]}; add decks to generate it.\n")
        show_heatmaps(outputs)
        return
    try:
        seed = LEGACY_DATA if args.input.resolve() == DEFAULT_DATA.resolve() else None
        total = add_decks(number, args.input, seed)
        for version, output in zip((1, 2), outputs):
            results, _ = analyze_file(args.input, total, version)
            plot_heatmap(results, total, output, version)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Added {number:,} decks; {total:,} decks analyzed in total.")
    print(f"Decks saved to {args.input}")
    for output in outputs:
        print(f"Heatmap saved to {output}")


if __name__ == "__main__":
    main()
