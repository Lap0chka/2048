import unittest
from unittest.mock import patch

from game2048.game import Game2048


class TestGame2048(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game2048(4)
        self.initial_board = [
            [2, 2, 4, 4],
            [0, 0, 0, 2],
            [2, 0, 2, 0],
            [0, 0, 0, 0],
        ]

    def test_initial_board(self) -> None:
        """Test that the board initializes with exactly two tiles."""
        board = self.game.board
        non_zero_count = sum(cell != 0 for row in board for cell in row)
        self.assertEqual(non_zero_count, 2)

    def test_score_initially_zero(self) -> None:
        """Test that the score starts at 0."""
        self.assertEqual(self.game.score, 0)

    def test_get_empty_cells(self) -> None:
        """Test that empty cells are identified correctly."""
        self.game._board = self.initial_board
        empty_cells = self.game.get_empty_cells()
        self.assertEqual(len(empty_cells), 9)

    def test_merge(self) -> None:
        """Test the _merge function."""
        row = [2, 2, 4, 4]
        expected = [4, 8, 0, 0]
        merged_row, _ = self.game._merge(row)
        self.assertEqual(merged_row, expected)

    def test_move_left(self) -> None:
        """Test moving tiles to the left."""
        self.game._board = self.initial_board
        changed = self.game.move_left()
        expected = [
            [4, 8, 0, 0],
            [2, 0, 0, 0],
            [4, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertTrue(changed)
        self.assertEqual(self.game.board, expected)

    def test_move_right(self) -> None:
        """Test moving tiles to the right."""
        self.game._board = self.initial_board
        changed = self.game.move_right()
        expected = [
            [0, 0, 4, 8],
            [0, 0, 0, 2],
            [0, 0, 0, 4],
            [0, 0, 0, 0],
        ]
        self.assertTrue(changed)
        self.assertEqual(self.game.board, expected)

    def test_move_up(self) -> None:
        """Test moving tiles up."""
        self.game._board = [
            [2, 0, 2, 0],
            [2, 0, 0, 4],
            [0, 0, 2, 4],
            [0, 0, 0, 4],
        ]
        changed = self.game.move_up()
        expected = [
            [4, 0, 4, 8],
            [0, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertTrue(changed)
        self.assertEqual(self.game.board, expected)

    def test_move_down(self) -> None:
        """Test moving tiles down."""
        self.game._board = [
            [2, 0, 2, 0],
            [2, 0, 0, 4],
            [0, 0, 2, 4],
            [0, 0, 0, 4],
        ]
        changed = self.game.move_down()
        expected = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 4],
            [4, 0, 4, 8],
        ]
        self.assertTrue(changed)
        self.assertEqual(self.game.board, expected)

    def test_game_over(self) -> None:
        """Test the game over condition."""
        self.game._board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        self.assertTrue(self.game.is_game_over())

    @patch("random.choice", side_effect=[(0, 0), (1, 1)])
    @patch("random.random", side_effect=[0.1, 0.9])
    def test_initialize_board(self, mock_random: patch, mock_choice: patch) -> None:
        """Test that the board initializes correctly with predictable random values."""
        game = Game2048(4)
        expected = [
            [2, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(game.board, expected)


if __name__ == "__main__":
    unittest.main()
