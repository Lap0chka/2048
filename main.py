import random
from typing import List, Tuple, Dict

import pygame

# Colors for different tiles
colors: Dict[int, Tuple[int, int, int]] = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 200, 55),
    32: (200, 200, 200),
    64: (140, 100, 200),
    128: (175, 100, 40),
    256: (51, 250, 40),
}


class Game2048:
    """
    Class for managing the 2048 game logic.

    Attributes:
        _size (int): The size of the board (e.g., 4 for a 4x4 board).
        _board (List[List[int]]): The game board represented as a 2D list.
    """
    __slots__ = ('_size', '_board')

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
        self._initialize_board()

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
                print(self._board[row][col])
        return changed

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
                skip = True
            elif row[i] != 0:
                merged.append(row[i])
        merged += [0] * (self._size - len(merged))
        return merged, len(merged) != len(row)


# Game Settings
black = (0, 0, 0)
size_block = 110
margin = 10
size = 4
width = size * size_block + (size + 1) * margin
height = width + 110

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 55)

# Game Initialization
game = Game2048(size)


def draw_board(game2048: Game2048) -> None:
    """Draws the game board on the screen."""
    screen.fill(black)
    font_score = pygame.font.SysFont('Arial', 48)
    text_score = font_score.render(f'Score: ', True, colors[256])
    screen.blit(text_score, (20, 35))
    for row in range(size):
        for col in range(size):
            value = game2048.board[row][col]
            w = col * size_block + (col + 1) * margin
            h = row * size_block + (row + 1) * margin + 110
            pygame.draw.rect(screen, colors[value], (w, h, size_block, size_block))
            if value != 0:
                text = font.render(str(value), True, black)
                text_rect = text.get_rect(center=(w + size_block // 2, h + size_block // 2))
                screen.blit(text, text_rect)
    pygame.display.update()


# Game Loop
running = True
while running:
    draw_board(game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if game.move_left():
                    empty = game.get_empty_cells()
                    if empty:
                        game.insert_2_or_4(random.choice(empty))
            elif event.key == pygame.K_RIGHT:
                if game.move_right():
                    empty = game.get_empty_cells()
                    if empty:
                        game.insert_2_or_4(random.choice(empty))
            elif event.key == pygame.K_UP:
                if game.move_up():
                    empty = game.get_empty_cells()
                    if empty:
                        game.insert_2_or_4(random.choice(empty))
            elif event.key == pygame.K_DOWN:
                if game.move_down():
                    empty = game.get_empty_cells()
                    if empty:
                        game.insert_2_or_4(random.choice(empty))

pygame.quit()
