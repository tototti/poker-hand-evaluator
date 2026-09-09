import pytest

from poker.card import Card
from poker.hand import Hand


class TestHandParsing:
    def test_parses_five_cards_from_comma_separated_string(self):
        hand = Hand.from_string("AS, KS, QS, JS, TS")
        assert hand.cards == [Card("AS"), Card("KS"), Card("QS"), Card("JS"), Card("TS")]

    def test_ignores_whitespace_around_commas(self):
        hand = Hand.from_string("AS,KS ,  QS,JS,TS")
        assert [str(c) for c in hand.cards] == ["AS", "KS", "QS", "JS", "TS"]

    def test_normalizes_lowercase_to_uppercase(self):
        hand = Hand.from_string("as, ks, qs, js, ts")
        assert [str(c) for c in hand.cards] == ["AS", "KS", "QS", "JS", "TS"]

    def test_preserves_input_order_for_display(self):
        hand = Hand.from_string("2H, AS, KS, QS, JS")
        assert hand.display() == "2H, AS, KS, QS, JS"


class TestHandValidation:
    def test_raises_when_not_five_cards(self):
        with pytest.raises(ValueError):
            Hand.from_string("AS, KS, QS, JS")
        with pytest.raises(ValueError):
            Hand.from_string("AS, KS, QS, JS, TS, 9H")

    def test_raises_on_duplicate_card_within_hand(self):
        with pytest.raises(ValueError):
            Hand.from_string("AS, AS, QS, JS, TS")

    def test_raises_on_invalid_card(self):
        with pytest.raises(ValueError):
            Hand.from_string("XX, KS, QS, JS, TS")
