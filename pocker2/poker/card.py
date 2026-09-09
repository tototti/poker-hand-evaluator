RANK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14,
}
VALID_SUITS = {"S", "H", "D", "C"}


class Card:
    def __init__(self, text):
        text = text.strip().upper()
        if len(text) != 2:
            raise ValueError(f"Invalid card: {text!r}")
        rank, suit = text[0], text[1]
        if rank not in RANK_VALUES:
            raise ValueError(f"Invalid rank: {rank!r}")
        if suit not in VALID_SUITS:
            raise ValueError(f"Invalid suit: {suit!r}")
        self.rank = rank
        self.suit = suit
        self.rank_value = RANK_VALUES[rank]

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"Card({str(self)!r})"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))
