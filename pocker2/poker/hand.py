from poker.card import Card

HAND_SIZE = 5


class Hand:
    def __init__(self, cards, raw_texts):
        self.cards = cards
        self._raw_texts = raw_texts

    @classmethod
    def from_string(cls, text):
        raw_texts = [part.strip() for part in text.split(",")]
        if len(raw_texts) != HAND_SIZE:
            raise ValueError(
                f"Hand must contain exactly {HAND_SIZE} cards, got {len(raw_texts)}"
            )
        cards = [Card(raw) for raw in raw_texts]
        if len(set(cards)) != HAND_SIZE:
            raise ValueError("Hand contains duplicate cards")
        display_texts = [str(card) for card in cards]
        return cls(cards, display_texts)

    def display(self):
        return ", ".join(self._raw_texts)
