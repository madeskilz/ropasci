import io
import unittest
from unittest.mock import patch
import contextlib

import game


def run_play_and_capture(inputs, comp_choice=None):
    """Run game.play_rps() with mocked input sequence and optional comp choice.
    Returns the captured stdout as a string.
    """
    inputs_iter = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(inputs_iter)
        except StopIteration:
            # If tests forget to provide enough inputs, stop the loop
            raise EOFError

    with patch("builtins.input", side_effect=fake_input):
        if comp_choice is not None:
            with patch("random.choice", return_value=comp_choice):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    game.play_rps()
                return buf.getvalue()
        else:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                game.play_rps()
            return buf.getvalue()


class TestPlayRPS(unittest.TestCase):
    # ===== Quit Commands =====
    def test_quit_immediately(self):
        out = run_play_and_capture(["quit"])
        self.assertIn("Welcome to Rock, Paper, Scissors!", out)
        self.assertIn("Thanks for playing. Goodbye!", out)

    def test_quit_shorthand_q(self):
        out = run_play_and_capture(["q"])
        self.assertIn("Thanks for playing. Goodbye!", out)

    def test_quit_exit(self):
        out = run_play_and_capture(["exit"])
        self.assertIn("Thanks for playing. Goodbye!", out)

    # ===== All 3 Tie Outcomes =====
    def test_tie_rock_rock(self):
        out = run_play_and_capture(["rock", "n"], comp_choice="rock")
        self.assertIn("You chose: rock. Computer chose: rock.", out)
        self.assertIn("It's a tie!", out)

    def test_tie_paper_paper(self):
        out = run_play_and_capture(["paper", "n"], comp_choice="paper")
        self.assertIn("You chose: paper. Computer chose: paper.", out)
        self.assertIn("It's a tie!", out)

    def test_tie_scissors_scissors(self):
        out = run_play_and_capture(["scissors", "n"], comp_choice="scissors")
        self.assertIn("You chose: scissors. Computer chose: scissors.", out)
        self.assertIn("It's a tie!", out)

    # ===== All 3 Win Outcomes =====
    def test_win_rock_beats_scissors(self):
        out = run_play_and_capture(["rock", "n"], comp_choice="scissors")
        self.assertIn("You chose: rock. Computer chose: scissors.", out)
        self.assertIn("You win!", out)

    def test_win_paper_beats_rock(self):
        out = run_play_and_capture(["paper", "n"], comp_choice="rock")
        self.assertIn("You chose: paper. Computer chose: rock.", out)
        self.assertIn("You win!", out)

    def test_win_scissors_beats_paper(self):
        out = run_play_and_capture(["scissors", "n"], comp_choice="paper")
        self.assertIn("You chose: scissors. Computer chose: paper.", out)
        self.assertIn("You win!", out)

    # ===== All 3 Loss Outcomes =====
    def test_lose_rock_to_paper(self):
        out = run_play_and_capture(["rock", "n"], comp_choice="paper")
        self.assertIn("You chose: rock. Computer chose: paper.", out)
        self.assertIn("You lose!", out)

    def test_lose_paper_to_scissors(self):
        out = run_play_and_capture(["paper", "n"], comp_choice="scissors")
        self.assertIn("You chose: paper. Computer chose: scissors.", out)
        self.assertIn("You lose!", out)

    def test_lose_scissors_to_rock(self):
        out = run_play_and_capture(["scissors", "n"], comp_choice="rock")
        self.assertIn("You chose: scissors. Computer chose: rock.", out)
        self.assertIn("You lose!", out)

    # ===== Shorthand Inputs =====
    def test_shorthand_r_for_rock(self):
        out = run_play_and_capture(["r", "n"], comp_choice="scissors")
        self.assertIn("You chose: rock. Computer chose: scissors.", out)
        self.assertIn("You win!", out)

    def test_shorthand_p_for_paper(self):
        out = run_play_and_capture(["p", "n"], comp_choice="rock")
        self.assertIn("You chose: paper. Computer chose: rock.", out)
        self.assertIn("You win!", out)

    def test_shorthand_s_for_scissors(self):
        out = run_play_and_capture(["s", "n"], comp_choice="paper")
        self.assertIn("You chose: scissors. Computer chose: paper.", out)
        self.assertIn("You win!", out)

    # ===== Play Again Variations =====
    def test_play_again_yes_then_quit(self):
        out = run_play_and_capture(["rock", "y", "rock", "n"], comp_choice="scissors")
        # Should play twice
        self.assertEqual(out.count("You win!"), 2)
        self.assertIn("Thanks for playing. Goodbye!", out)

    def test_play_again_empty_continue(self):
        # Empty input on "Play again?" defaults to yes (continues)
        out = run_play_and_capture(["rock", "", "rock", "n"], comp_choice="scissors")
        self.assertEqual(out.count("You win!"), 2)

    def test_play_again_uppercase_Y(self):
        out = run_play_and_capture(["rock", "Y", "rock", "n"], comp_choice="scissors")
        self.assertEqual(out.count("You win!"), 2)

    def test_play_again_no_exits(self):
        out = run_play_and_capture(["rock", "n"], comp_choice="scissors")
        self.assertIn("You win!", out)
        self.assertIn("Thanks for playing. Goodbye!", out)

    def test_play_again_uppercase_N(self):
        out = run_play_and_capture(["rock", "N"], comp_choice="scissors")
        self.assertIn("Thanks for playing. Goodbye!", out)

    # ===== Invalid Input Handling =====
    def test_empty_input_prompts_retry(self):
        out = run_play_and_capture(["", "rock", "n"], comp_choice="scissors")
        self.assertIn("Please enter a choice.", out)
        self.assertIn("You chose: rock. Computer chose: scissors.", out)

    def test_invalid_choice_prompts_retry(self):
        out = run_play_and_capture(["banana", "rock", "n"], comp_choice="scissors")
        self.assertIn("Invalid choice. Please try again.", out)
        self.assertIn("You chose: rock. Computer chose: scissors.", out)

    def test_multiple_invalid_inputs(self):
        out = run_play_and_capture(["", "lizard", "spock", "rock", "n"], comp_choice="scissors")
        self.assertIn("Please enter a choice.", out)
        self.assertEqual(out.count("Invalid choice. Please try again."), 2)
        self.assertIn("You win!", out)

    # ===== Case Insensitivity =====
    def test_uppercase_ROCK(self):
        out = run_play_and_capture(["ROCK", "n"], comp_choice="scissors")
        self.assertIn("You chose: rock. Computer chose: scissors.", out)
        self.assertIn("You win!", out)

    def test_mixed_case_PaPeR(self):
        out = run_play_and_capture(["PaPeR", "n"], comp_choice="rock")
        self.assertIn("You chose: paper. Computer chose: rock.", out)
        self.assertIn("You win!", out)

    # ===== Whitespace Handling =====
    def test_input_with_leading_trailing_spaces(self):
        out = run_play_and_capture(["  rock  ", "n"], comp_choice="scissors")
        self.assertIn("You chose: rock. Computer chose: scissors.", out)
        self.assertIn("You win!", out)

    # ===== Keyboard Interrupt =====
    def test_keyboard_interrupt(self):
        def fake_input_with_interrupt(prompt=""):
            raise KeyboardInterrupt

        with patch("builtins.input", side_effect=fake_input_with_interrupt):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                game.play_rps()
            out = buf.getvalue()
            self.assertIn("Interrupted. Goodbye!", out)

    # ===== Multiple Rounds =====
    def test_multiple_rounds_different_outcomes(self):
        # Win, then lose, then tie, then quit
        inputs = ["rock", "y", "rock", "y", "rock", "n"]
        comp_choices = ["scissors", "paper", "rock"]
        
        inputs_iter = iter(inputs)
        comp_iter = iter(comp_choices)

        def fake_input(prompt=""):
            return next(inputs_iter)

        def fake_choice(seq):
            return next(comp_iter)

        with patch("builtins.input", side_effect=fake_input):
            with patch("random.choice", side_effect=fake_choice):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    game.play_rps()
                out = buf.getvalue()
                
        self.assertIn("You win!", out)
        self.assertIn("You lose!", out)
        self.assertIn("It's a tie!", out)


if __name__ == "__main__":
    unittest.main()
