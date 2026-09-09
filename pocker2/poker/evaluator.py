from collections import Counter
from enum import IntEnum
from functools import total_ordering


class HandRank(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


HAND_RANK_NAMES = {
    HandRank.HIGH_CARD: "High Card",
    HandRank.ONE_PAIR: "One Pair",
    HandRank.TWO_PAIR: "Two Pair",
    HandRank.THREE_OF_A_KIND: "Three of a Kind",
    HandRank.STRAIGHT: "Straight",
    HandRank.FLUSH: "Flush",
    HandRank.FULL_HOUSE: "Full House",
    HandRank.FOUR_OF_A_KIND: "Four of a Kind",
    HandRank.STRAIGHT_FLUSH: "Straight Flush",
    HandRank.ROYAL_FLUSH: "Royal Flush",
}

ACE_LOW_STRAIGHT_VALUES = frozenset({14, 2, 3, 4, 5})


@total_ordering
class EvaluatedHand:
    def __init__(self, rank, tiebreaker):
        self.rank = rank
        self.tiebreaker = tiebreaker

    @property
    def name(self):
        return HAND_RANK_NAMES[self.rank]

    def _key(self):
        return (self.rank, self.tiebreaker)

    def __eq__(self, other):
        return self._key() == other._key()

    def __lt__(self, other):
        return self._key() < other._key()

    def __repr__(self):
        return f"EvaluatedHand({self.rank!r}, {self.tiebreaker!r})"


def _find_straight_high(values):
    unique_values = set(values)
    if len(unique_values) != 5:
        return None
    if unique_values == ACE_LOW_STRAIGHT_VALUES:
        return 5
    if max(unique_values) - min(unique_values) == 4:
        return max(unique_values)
    return None


def evaluate(cards):
    values = [card.rank_value for card in cards]
    is_flush = len({card.suit for card in cards}) == 1
    straight_high = _find_straight_high(values)

    if is_flush and straight_high is not None:
        rank = HandRank.ROYAL_FLUSH if straight_high == 14 else HandRank.STRAIGHT_FLUSH
        return EvaluatedHand(rank, (straight_high,))

    counts = Counter(values)
    groups = sorted(counts.items(), key=lambda item: (-item[1], -item[0]))
    group_sizes = [size for _, size in groups]
    group_values = [value for value, _ in groups]

    if group_sizes == [4, 1]:
        return EvaluatedHand(HandRank.FOUR_OF_A_KIND, tuple(group_values))

    if group_sizes == [3, 2]:
        return EvaluatedHand(HandRank.FULL_HOUSE, tuple(group_values))

    if is_flush:
        return EvaluatedHand(HandRank.FLUSH, tuple(sorted(values, reverse=True)))

    if straight_high is not None:
        return EvaluatedHand(HandRank.STRAIGHT, (straight_high,))

    if group_sizes == [3, 1, 1]:
        return EvaluatedHand(HandRank.THREE_OF_A_KIND, tuple(group_values))

    if group_sizes == [2, 2, 1]:
        return EvaluatedHand(HandRank.TWO_PAIR, tuple(group_values))

    if group_sizes == [2, 1, 1, 1]:
        return EvaluatedHand(HandRank.ONE_PAIR, tuple(group_values))

    return EvaluatedHand(HandRank.HIGH_CARD, tuple(sorted(values, reverse=True)))
