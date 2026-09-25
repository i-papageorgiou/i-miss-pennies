import random
import unittest

from src.dataproc import CARD_COMBINATIONS, count_tricks, score_deck, unpack_bit_list


class GameTests(unittest.TestCase):
    def test_only_one_pattern_present(self):
        self.assertEqual(score_deck("000000", "000", "111"), (2, 0))
        self.assertEqual(score_deck("111111", "000", "111"), (0, 2))

    def test_discard_pile_and_reset_after_trick(self):
        self.assertEqual(score_deck("1000111", "000", "111"), (1, 1))
        self.assertEqual(score_deck("0000", "000", "111"), (1, 0))

    def test_against_card_by_card_play(self):
        rng = random.Random(42)
        for _ in range(20):
            cards = list("0" * 26 + "1" * 26)
            rng.shuffle(cards)
            for first in CARD_COMBINATIONS:
                for second in CARD_COMBINATIONS:
                    if first == second:
                        continue
                    pile = ""
                    expected = [0, 0]
                    for card in cards:
                        pile += card
                        if pile.endswith(first):
                            expected[0] += 1
                            pile = ""
                        elif pile.endswith(second):
                            expected[1] += 1
                            pile = ""
                    self.assertEqual(score_deck("".join(cards), first, second), tuple(expected))

    def test_result_perspective_and_ties(self):
        results = count_tricks(["000000", "111111", "000111"], ["000", "111"])
        self.assertEqual(results["000", "111"], {"wins": 1, "losses": 1, "ties": 1})
        self.assertEqual(count_tricks(["000000"], ["000", "111"])["000", "111"]["losses"], 1)

    def test_padding_and_incomplete_input(self):
        self.assertEqual(unpack_bit_list(bytes([255] * 7), 1), [1] * 52)
        with self.assertRaises(ValueError):
            unpack_bit_list(bytes(6), 1)


if __name__ == "__main__":
    unittest.main()
