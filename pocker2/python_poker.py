#!/usr/bin/env python3
import sys

from poker.evaluator import evaluate
from poker.hand import Hand

USAGE = 'Usage: python python_poker.py "<hand1のカード5枚>" "<hand2のカード5枚>"'


def _judge_winner(result1, result2):
    if result1 > result2:
        return "Hand 1"
    if result2 > result1:
        return "Hand 2"
    return "Draw"


def main(argv):
    if len(argv) != 2:
        print(USAGE, file=sys.stderr)
        return 1

    try:
        hand1 = Hand.from_string(argv[0])
        hand2 = Hand.from_string(argv[1])
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    result1 = evaluate(hand1.cards)
    result2 = evaluate(hand2.cards)

    print(f"Hand 1: {hand1.display()} => {result1.name}")
    print(f"Hand 2: {hand2.display()} => {result2.name}")
    print(f"Winner: {_judge_winner(result1, result2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
