from poker.card import Card
from poker.evaluator import evaluate, HandRank


def cards(text):
    return [Card(t.strip()) for t in text.split(",")]


class TestHandRankDetection:
    def test_royal_flush(self):
        result = evaluate(cards("AS, KS, QS, JS, TS"))
        assert result.rank == HandRank.ROYAL_FLUSH

    def test_straight_flush(self):
        result = evaluate(cards("9S, 8S, 7S, 6S, 5S"))
        assert result.rank == HandRank.STRAIGHT_FLUSH

    def test_ace_low_straight_flush_is_not_royal(self):
        result = evaluate(cards("5S, 4S, 3S, 2S, AS"))
        assert result.rank == HandRank.STRAIGHT_FLUSH

    def test_four_of_a_kind(self):
        result = evaluate(cards("9S, 9H, 9D, 9C, 2S"))
        assert result.rank == HandRank.FOUR_OF_A_KIND

    def test_full_house(self):
        result = evaluate(cards("9S, 9H, 9D, 2C, 2S"))
        assert result.rank == HandRank.FULL_HOUSE

    def test_flush(self):
        result = evaluate(cards("2S, 4S, 6S, 8S, KS"))
        assert result.rank == HandRank.FLUSH

    def test_straight(self):
        result = evaluate(cards("9S, 8H, 7D, 6C, 5S"))
        assert result.rank == HandRank.STRAIGHT

    def test_ace_low_straight(self):
        result = evaluate(cards("5S, 4H, 3D, 2C, AS"))
        assert result.rank == HandRank.STRAIGHT

    def test_ace_high_straight(self):
        result = evaluate(cards("AS, KH, QD, JC, TS"))
        assert result.rank == HandRank.STRAIGHT

    def test_three_of_a_kind(self):
        result = evaluate(cards("9S, 9H, 9D, 2C, 3S"))
        assert result.rank == HandRank.THREE_OF_A_KIND

    def test_two_pair(self):
        result = evaluate(cards("9S, 9H, 2D, 2C, 3S"))
        assert result.rank == HandRank.TWO_PAIR

    def test_one_pair(self):
        result = evaluate(cards("9S, 9H, 2D, 4C, 3S"))
        assert result.rank == HandRank.ONE_PAIR

    def test_high_card(self):
        result = evaluate(cards("9S, 7H, 2D, 4C, KS"))
        assert result.rank == HandRank.HIGH_CARD


class TestHandRankOrdering:
    def test_ranks_are_ordered_by_strength(self):
        ordered = [
            HandRank.HIGH_CARD,
            HandRank.ONE_PAIR,
            HandRank.TWO_PAIR,
            HandRank.THREE_OF_A_KIND,
            HandRank.STRAIGHT,
            HandRank.FLUSH,
            HandRank.FULL_HOUSE,
            HandRank.FOUR_OF_A_KIND,
            HandRank.STRAIGHT_FLUSH,
            HandRank.ROYAL_FLUSH,
        ]
        for weaker, stronger in zip(ordered, ordered[1:]):
            assert weaker.value < stronger.value


class TestTiebreakers:
    def test_straight_flush_tiebreaker_is_highest_rank(self):
        result = evaluate(cards("9S, 8S, 7S, 6S, 5S"))
        assert result.tiebreaker == (9,)

    def test_ace_low_straight_flush_tiebreaker_is_five(self):
        result = evaluate(cards("5S, 4S, 3S, 2S, AS"))
        assert result.tiebreaker == (5,)

    def test_four_of_a_kind_tiebreaker(self):
        result = evaluate(cards("9S, 9H, 9D, 9C, 2S"))
        assert result.tiebreaker == (9, 2)

    def test_full_house_tiebreaker(self):
        result = evaluate(cards("9S, 9H, 9D, 2C, 2S"))
        assert result.tiebreaker == (9, 2)

    def test_flush_tiebreaker_is_descending_ranks(self):
        result = evaluate(cards("2S, 4S, 6S, 8S, KS"))
        assert result.tiebreaker == (13, 8, 6, 4, 2)

    def test_straight_tiebreaker_is_highest_rank(self):
        result = evaluate(cards("9S, 8H, 7D, 6C, 5S"))
        assert result.tiebreaker == (9,)

    def test_ace_low_straight_tiebreaker_is_five(self):
        result = evaluate(cards("5S, 4H, 3D, 2C, AS"))
        assert result.tiebreaker == (5,)

    def test_three_of_a_kind_tiebreaker(self):
        result = evaluate(cards("9S, 9H, 9D, 2C, 3S"))
        assert result.tiebreaker == (9, 3, 2)

    def test_two_pair_tiebreaker(self):
        result = evaluate(cards("9S, 9H, 2D, 2C, 3S"))
        assert result.tiebreaker == (9, 2, 3)

    def test_one_pair_tiebreaker(self):
        result = evaluate(cards("9S, 9H, 2D, 4C, 3S"))
        assert result.tiebreaker == (9, 4, 3, 2)

    def test_high_card_tiebreaker(self):
        result = evaluate(cards("9S, 7H, 2D, 4C, KS"))
        assert result.tiebreaker == (13, 9, 7, 4, 2)

    def test_royal_flush_tiebreaker_is_constant_across_suits(self):
        a = evaluate(cards("AS, KS, QS, JS, TS"))
        b = evaluate(cards("AH, KH, QH, JH, TH"))
        assert a.tiebreaker == b.tiebreaker


class TestComparison:
    def test_higher_rank_beats_lower_rank(self):
        royal = evaluate(cards("AS, KS, QS, JS, TS"))
        full_house = evaluate(cards("9H, 9D, 9C, 2S, 2H"))
        assert royal > full_house

    def test_same_rank_compares_by_tiebreaker(self):
        higher_two_pair = evaluate(cards("9S, 9H, 3D, 3C, 4S"))
        lower_two_pair = evaluate(cards("8S, 8H, 3D, 3C, 4S"))
        assert higher_two_pair > lower_two_pair

    def test_identical_hands_are_equal(self):
        a = evaluate(cards("9S, 9H, 3D, 3C, 4S"))
        b = evaluate(cards("9C, 9D, 3S, 3H, 4C"))
        assert a == b

    def test_royal_flushes_are_always_equal(self):
        a = evaluate(cards("AS, KS, QS, JS, TS"))
        b = evaluate(cards("AH, KH, QH, JH, TH"))
        assert a == b
