import pytest

from poker.card import Card


class TestCardParsing:
    def test_parses_rank_and_suit(self):
        card = Card("AS")
        assert card.rank == "A"
        assert card.suit == "S"

    def test_rank_value_for_number_cards(self):
        assert Card("2H").rank_value == 2
        assert Card("9H").rank_value == 9

    def test_rank_value_for_face_cards(self):
        assert Card("TD").rank_value == 10
        assert Card("JD").rank_value == 11
        assert Card("QD").rank_value == 12
        assert Card("KD").rank_value == 13

    def test_rank_value_for_ace_is_14(self):
        assert Card("AS").rank_value == 14

    def test_lowercase_input_is_normalized_to_uppercase(self):
        card = Card("as")
        assert card.rank == "A"
        assert card.suit == "S"
        assert str(card) == "AS"

    def test_str_representation(self):
        assert str(Card("TD")) == "TD"


class TestCardEquality:
    def test_equal_cards_are_equal(self):
        assert Card("AS") == Card("AS")

    def test_different_cards_are_not_equal(self):
        assert Card("AS") != Card("AH")


class TestCardValidation:
    def test_raises_on_invalid_rank(self):
        with pytest.raises(ValueError):
            Card("XS")

    def test_raises_on_invalid_suit(self):
        with pytest.raises(ValueError):
            Card("AX")

    def test_raises_on_wrong_length(self):
        with pytest.raises(ValueError):
            Card("A")
        with pytest.raises(ValueError):
            Card("ASD")
