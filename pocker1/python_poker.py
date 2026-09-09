#!/usr/bin/env python3
"""Poker hand evaluator: judges the hand for two 5-card hands and decides the winner."""

import sys
from collections import Counter

RANKS = "23456789TJQKA"
SUITS = "SHDC"
RANK_VALUES = {r: v for v, r in enumerate(RANKS, start=2)}

HAND_NAMES = {
    10: "Royal Flush",
    9: "Straight Flush",
    8: "Four of a Kind",
    7: "Full House",
    6: "Flush",
    5: "Straight",
    4: "Three of a Kind",
    3: "Two Pair",
    2: "One Pair",
    1: "High Card",
}


class Card:
    def __init__(self, text):
        normalized = text.strip().upper()
        if len(normalized) != 2:
            raise ValueError(f"Invalid card: '{text}'")
        rank_char, suit_char = normalized[0], normalized[1]
        if rank_char not in RANK_VALUES:
            raise ValueError(f"Invalid rank: '{text}'")
        if suit_char not in SUITS:
            raise ValueError(f"Invalid suit: '{text}'")
        self.rank_char = rank_char
        self.suit_char = suit_char
        self.rank = RANK_VALUES[rank_char]
        self.text = normalized

    def __repr__(self):
        return self.text


def parse_hand(arg):
    parts = [p.strip() for p in arg.split(",")]
    if len(parts) != 5:
        raise ValueError(f"Hand must contain exactly 5 cards: '{arg}'")
    cards = [Card(p) for p in parts]
    if len(set(c.text for c in cards)) != 5:
        raise ValueError(f"Duplicate card found in hand: '{arg}'")
    return cards


def check_straight(values):
    unique = sorted(set(values))
    if len(unique) != 5:
        return None
    if unique[4] - unique[0] == 4:
        return unique[4]
    if unique == [2, 3, 4, 5, 14]:
        return 5
    return None


def evaluate_hand(cards):
    ranks = [c.rank for c in cards]
    suits = [c.suit_char for c in cards]

    is_flush = len(set(suits)) == 1
    straight_high = check_straight(ranks)

    counts = Counter(ranks)
    counts_desc = sorted(counts.items(), key=lambda kv: (-kv[1], -kv[0]))
    count_shape = sorted(counts.values(), reverse=True)

    if straight_high and is_flush:
        if straight_high == 14:
            return 10, ()
        return 9, (straight_high,)

    if count_shape == [4, 1]:
        four_rank = counts_desc[0][0]
        kicker = counts_desc[1][0]
        return 8, (four_rank, kicker)

    if count_shape == [3, 2]:
        three_rank = counts_desc[0][0]
        pair_rank = counts_desc[1][0]
        return 7, (three_rank, pair_rank)

    if is_flush:
        return 6, tuple(sorted(ranks, reverse=True))

    if straight_high:
        return 5, (straight_high,)

    if count_shape == [3, 1, 1]:
        three_rank = counts_desc[0][0]
        kickers = sorted((counts_desc[1][0], counts_desc[2][0]), reverse=True)
        return 4, (three_rank, *kickers)

    if count_shape == [2, 2, 1]:
        high_pair, low_pair = sorted((counts_desc[0][0], counts_desc[1][0]), reverse=True)
        kicker = counts_desc[2][0]
        return 3, (high_pair, low_pair, kicker)

    if count_shape == [2, 1, 1, 1]:
        pair_rank = counts_desc[0][0]
        kickers = sorted((counts_desc[1][0], counts_desc[2][0], counts_desc[3][0]), reverse=True)
        return 2, (pair_rank, *kickers)

    return 1, tuple(sorted(ranks, reverse=True))


def format_hand(cards, rank_no):
    cards_str = ", ".join(c.text for c in cards)
    return f"{cards_str} => {HAND_NAMES[rank_no]}"


def main():
    if len(sys.argv) != 3:
        raise ValueError(
            'Usage: python python_poker.py "<hand1のカード5枚>" "<hand2のカード5枚>"'
        )

    hand1_cards = parse_hand(sys.argv[1])
    hand2_cards = parse_hand(sys.argv[2])

    rank1, tiebreaker1 = evaluate_hand(hand1_cards)
    rank2, tiebreaker2 = evaluate_hand(hand2_cards)

    print(f"Hand 1: {format_hand(hand1_cards, rank1)}")
    print(f"Hand 2: {format_hand(hand2_cards, rank2)}")

    score1 = (rank1, tiebreaker1)
    score2 = (rank2, tiebreaker2)
    if score1 > score2:
        winner = "Hand 1"
    elif score2 > score1:
        winner = "Hand 2"
    else:
        winner = "Draw"
    print(f"Winner: {winner}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
