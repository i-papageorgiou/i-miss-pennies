"""Score the trick-counting version of Nishiyama's game."""
from pathlib import Path

CARD_COMBINATIONS = tuple(f"{value:03b}" for value in range(8))


def unpack_bit_list(packed_bytes, num_decks):
    length = num_decks * 52
    if num_decks < 1 or len(packed_bytes) != (length + 7) // 8:
        raise ValueError("File size must match the requested number of 52-card decks.")
    return [(packed_bytes[i // 8] >> (i % 8)) & 1 for i in range(length)]


def convert_to_strings(bit_list, num_decks):
    if len(bit_list) != num_decks * 52:
        raise ValueError("Expected exactly 52 bits per deck.")
    return ["".join(str(bit) for bit in bit_list[i:i + 52])
            for i in range(0, len(bit_list), 52)]


def score_deck_v1(deck, first, second):
    """Count tricks, discarding the pile through each winning pattern."""
    if first == second:
        raise ValueError("Players must choose different patterns.")
    first_tricks = second_tricks = 0
    while len(deck) >= 3:
        first_pos, second_pos = deck.find(first), deck.find(second)
        if first_pos == second_pos == -1:
            break
        if first_pos != -1 and (second_pos == -1 or first_pos < second_pos):
            first_tricks += 1
            deck = deck[first_pos + 3:]
        else:
            second_tricks += 1
            deck = deck[second_pos + 3:]
    return first_tricks, second_tricks

def score_deck_v2(deck, first, second):
    """Count tricks, discarding the pile through each winning pattern."""
    if first == second:
        raise ValueError("Players must choose different patterns.")
    first_tricks = second_tricks = 0
    while len(deck) >= 3:
        first_pos, second_pos = deck.find(first), deck.find(second)
        if first_pos == second_pos == -1:
            break
        if first_pos != -1 and (second_pos == -1 or first_pos < second_pos):
            first_tricks += first_pos+3
            deck = deck[first_pos + 3:]
        else:
            second_tricks += second_pos+3
            deck = deck[second_pos + 3:]
    return first_tricks, second_tricks


def count_tricks(deck_strings, card_comb=CARD_COMBINATIONS):
    """Return deck wins/losses/ties for each (first choice, response).

    Results are from the response player's perspective. A deck is won by
    taking more tricks; equal trick counts are a tie.
    """
    results = {}
    for first in card_comb:
        for second in card_comb:
            if first == second:
                continue
            wins = losses = ties = 0
            for deck in deck_strings:
                a, b = score_deck_v1(deck, first, second)
                wins += b > a
                losses += b < a
                ties += b == a
            results[first, second] = {"wins": wins, "losses": losses, "ties": ties}
    return results


def analyze_file(filename, num_decks):
    bits = unpack_bit_list(Path(filename).read_bytes(), num_decks)
    decks = convert_to_strings(bits, num_decks)
    return count_tricks(decks), len(decks)
