import random
from typing import List, Tuple


class Game2048:
    """
    Class for managing the game2048 game logic.

    Attributes:
        _size (int): The size of the board (e.g., 4 for a 4x4 board).
        _board (List[List[int]]): The game board represented as a 2D list.
        _score (int): The current score of the game.
    """
    __slots__ = ('_size', '_board', '_score')

    def __init__(self, board_size: int) -> None:
        """
        Initializes the game board.

        Args:
            board_size (int): The size of the game board.
        """
        if board_size < 2:
            raise ValueError("Size must be at least 2.")
        self._size = board_size
        self._board = [[0] * self._size for _ in range(self._size)]
        self._score = 0
        self._initialize_board()

    @property
    def score(self) -> int:
        """Returns the current score."""
        return self._score

    def _merge(self, row: List[int]) -> Tuple[List[int], bool]:
        """
        Merges tiles in a row or column for one direction.

        Args:
            row (List[int]): The row or column to merge.

        Returns:
            Tuple[List[int], bool]: The merged row and a flag indicating if merging occurred.
        """
        merged = []
        skip = False
        for i in range(len(row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(row) and row[i] == row[i + 1] and row[i] != 0:
                merged.append(row[i] * 2)
                self._score += row[i] * 2  # Update the score
                skip = True
            elif row[i] != 0:
                merged.append(row[i])
        merged += [0] * (self._size - len(merged))
        return merged, len(merged) != len(row)

    def _initialize_board(self) -> None:
        """Starts the game by placing two random tiles on the board."""
        for _ in range(2):
            empty_cells = self.get_empty_cells()
            if empty_cells:
                self.insert_2_or_4(random.choice(empty_cells))

    @property
    def size(self) -> int:
        """Returns the size of the game board."""
        return self._size

    @property
    def board(self) -> List[List[int]]:
        """Returns a copy of the game board."""
        return [row[:] for row in self._board]

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Returns a list of coordinates of empty cells."""
        return [(i, j) for i in range(self._size) for j in range(self._size) if self._board[i][j] == 0]

    def insert_2_or_4(self, position: Tuple[int, int]) -> None:
        """
        Inserts a 2 or 4 in the specified position.

        Args:
            position (Tuple[int, int]): The (row, column) position for insertion.
        """
        x, y = position
        self._board[x][y] = 2 if random.random() < 0.9 else 4

    def move_left(self) -> bool:
        """Handles the logic for moving tiles left. Returns True if the board changed."""
        changed = False
        for row in self._board:
            compacted, merged = self._merge(row)
            if row != compacted:
                changed = True
            row[:] = compacted
        return changed

    def move_right(self) -> bool:
        """Handles the logic for moving tiles right. Returns True if the board changed."""
        changed = False
        for row in self._board:
            reversed_row = row[::-1]
            compacted, merged = self._merge(reversed_row)
            if row != compacted[::-1]:
                changed = True
            row[:] = compacted[::-1]
        return changed

    def move_up(self) -> bool:
        """Handles the logic for moving tiles up. Returns True if the board changed."""
        changed = False
        for col in range(self._size):
            column = [self._board[row][col] for row in range(self._size)]
            compacted, merged = self._merge(column)
            if column != compacted:
                changed = True
            for row in range(self._size):
                self._board[row][col] = compacted[row]
        return changed

    def move_down(self) -> bool:
        """Handles the logic for moving tiles down. Returns True if the board changed."""
        changed = False
        for col in range(self._size):
            column = [self._board[row][col] for row in range(self._size)][::-1]
            compacted, merged = self._merge(column)
            if column[::-1] != compacted[::-1]:
                changed = True
            for row in range(self._size):
                self._board[row][col] = compacted[::-1][row]

        return changed

    def is_game_over(self) -> bool:
        """
        Checks if there are no valid moves left.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        # Check for empty cells
        if self.get_empty_cells():
            return False

        # Check for possible merges in rows
        for row in self._board:
            for i in range(self._size - 1):
                if row[i] == row[i + 1]:
                    return False

        # Check for possible merges in columns
        for col in range(self._size):
            for row in range(self._size - 1):
                if self._board[row][col] == self._board[row + 1][col]:
                    return False

        # No moves left
        return True