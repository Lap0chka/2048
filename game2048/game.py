import random
from typing import List, Tuple, Optional


class Game2048:
    """
    Class for managing the game 2048 logic.

    Attributes:
        _size (int): The size of the board (e.g., 4 for a 4x4 board).
        _board (List[List[int]]): The game board represented as a 2D list.
        _score (int): The current score of the game.
    """

    __slots__ = ('_size', '_board', '_score')
    _instance: Optional["Game2048"] = None

    def __new__(cls, *args, **kwargs) -> "Game2048":
        """
        Singleton implementation: ensures only one instance of the class is created.

        Returns:
            Game2048: Single instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, board_size: int) -> None:
        """
        Initializes the game board.

        Args:
            board_size (int): The size of the game board.
        """

        self._size = board_size
        if board_size < 2:
            raise ValueError("Board size must be at least 2.")
        self._board = [[0] * self._size for _ in range(self._size)]
        self._score = 0
        self._initialize_board()

    @property
    def score(self) -> int:
        """Returns the current score."""
        return self._score

    @property
    def size(self) -> int:
        """Returns the size of the game board."""
        return self._size

    @property
    def board(self) -> List[List[int]]:
        """Returns a copy of the game board."""
        return [row[:] for row in self._board]

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

    def move(self, direction: str) -> bool:
        """
        Generalized move handler.

        Args:
            direction (str): The direction to move ('left', 'right', 'up', 'down').

        Returns:
            bool: True if the board changed, False otherwise.
        """
        changed = False
        for col in range(self._size):
            if direction in {"up", "down"}:
                column = [self._board[row][col] for row in range(self._size)]
                if direction == "down":
                    column.reverse()
                compacted, _ = self._merge(column)
                if direction == "down":
                    compacted.reverse()
                for row in range(self._size):
                    if self._board[row][col] != compacted[row]:
                        changed = True
                    self._board[row][col] = compacted[row]

            else:
                row = self._board[col]
                if direction == "right":
                    row.reverse()
                compacted, _ = self._merge(row)
                if direction == "right":
                    compacted.reverse()
                if self._board[col] != compacted:
                    changed = True
                self._board[col] = compacted
        return changed

    def move_left(self) -> bool:
        """Handles the logic for moving tiles left."""
        return self.move("left")

    def move_right(self) -> bool:
        """Handles the logic for moving tiles right."""
        return self.move("right")

    def move_up(self) -> bool:
        """Handles the logic for moving tiles up."""
        return self.move("up")

    def move_down(self) -> bool:
        """Handles the logic for moving tiles down."""
        return self.move("down")

    def is_game_over(self) -> bool:
        """
        Checks if there are no valid moves left.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        if self.get_empty_cells():
            return False

        for row in self._board:
            for i in range(self._size - 1):
                if row[i] == row[i + 1]:
                    return False

        for col in range(self._size):
            for row in range(self._size - 1):
                if self._board[row][col] == self._board[row + 1][col]:
                    return False

        return True
