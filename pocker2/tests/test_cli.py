import subprocess
import sys
from pathlib import Path

import pytest

from python_poker import main

SCRIPT = Path(__file__).resolve().parent.parent / "python_poker.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


class TestMainReturnValue:
    def test_prints_hands_and_winner(self, capsys):
        exit_code = main(["AS, KS, QS, JS, TS", "9H, 9D, 9C, 2S, 2H"])
        captured = capsys.readouterr()
        assert captured.out == (
            "Hand 1: AS, KS, QS, JS, TS => Royal Flush\n"
            "Hand 2: 9H, 9D, 9C, 2S, 2H => Full House\n"
            "Winner: Hand 1\n"
        )
        assert exit_code == 0

    def test_hand2_wins(self, capsys):
        main(["9H, 9D, 9C, 2S, 2H", "AS, KS, QS, JS, TS"])
        captured = capsys.readouterr()
        assert captured.out == (
            "Hand 1: 9H, 9D, 9C, 2S, 2H => Full House\n"
            "Hand 2: AS, KS, QS, JS, TS => Royal Flush\n"
            "Winner: Hand 2\n"
        )

    def test_draw(self, capsys):
        main(["9S, 9H, 3D, 3C, 4S", "9C, 9D, 3S, 3H, 4C"])
        captured = capsys.readouterr()
        assert captured.out == (
            "Hand 1: 9S, 9H, 3D, 3C, 4S => Two Pair\n"
            "Hand 2: 9C, 9D, 3S, 3H, 4C => Two Pair\n"
            "Winner: Draw\n"
        )

    def test_lowercase_input_is_normalized_in_output(self, capsys):
        main(["as, ks, qs, js, ts", "9h, 9d, 9c, 2s, 2h"])
        captured = capsys.readouterr()
        assert "Hand 1: AS, KS, QS, JS, TS => Royal Flush\n" in captured.out

    def test_invalid_argument_count_returns_error_status(self, capsys):
        exit_code = main(["AS, KS, QS, JS, TS"])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert captured.err != ""

    def test_invalid_hand_size_returns_error_status(self, capsys):
        exit_code = main(["AS, KS, QS, JS", "9H, 9D, 9C, 2S, 2H"])
        captured = capsys.readouterr()
        assert exit_code == 1
        assert captured.err != ""

    def test_duplicate_card_in_hand_returns_error_status(self, capsys):
        exit_code = main(["AS, AS, QS, JS, TS", "9H, 9D, 9C, 2S, 2H"])
        assert exit_code == 1

    def test_invalid_card_returns_error_status(self, capsys):
        exit_code = main(["XX, KS, QS, JS, TS", "9H, 9D, 9C, 2S, 2H"])
        assert exit_code == 1


class TestCliSubprocess:
    def test_runs_as_script_and_prints_expected_output(self):
        result = run_cli("AS, KS, QS, JS, TS", "9H, 9D, 9C, 2S, 2H")
        assert result.returncode == 0
        assert result.stdout == (
            "Hand 1: AS, KS, QS, JS, TS => Royal Flush\n"
            "Hand 2: 9H, 9D, 9C, 2S, 2H => Full House\n"
            "Winner: Hand 1\n"
        )

    def test_invalid_input_exits_with_status_1_and_stderr_message(self):
        result = run_cli("AS, KS, QS, JS", "9H, 9D, 9C, 2S, 2H")
        assert result.returncode == 1
        assert result.stdout == ""
        assert result.stderr != ""
