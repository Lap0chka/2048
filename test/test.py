import unittest

from main import Game2048


class TestGame(unittest.TestCase):
    def setUp(self):
        self.size = 4
        self.game = Game2048(self.size)

    def test_print_board(self):
        mas = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(mas, self.game._board)


