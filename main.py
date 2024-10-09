import random
import sys

import pygame
from pygame.examples.setmodescale import screen

colors = {
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
    __slots__ = ('_size', '_board')

    def __init__(self, size):
        self._size = size
        self._board = [[0] * self._size for _ in range(self._size)]

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        if isinstance(new_size, int) and new_size != self._size:
            self._size = new_size
            self._board = [[0] * self._size for _ in range(self._size)]
        raise TypeError('You can use only integers')

    @property
    def mas(self):
        return [row[:] for row in self._board]

    def get_empty_board(self):
        empty_board = []
        for i in range(self._size):
            for j in range(self._size):
                if self._board[i][j] == 0:
                    empty_board.append([i, j])
        return empty_board

    def draw_board(self):
        """ Function to draw the board with the current state of the game """
        for row in range(size):
            for col in range(size):
                value = self._board[row][col]  # Get value from the game board
                w = col * size_block + (col + 1) * margin
                h = row * size_block + (row + 1) * margin + 110
                # Draw the rectangle for each tile
                pygame.draw.rect(screen, colors[value], (w, h, size_block, size_block))
                # Render the number if the tile is not empty
                if value != 0:
                    text = font.render(str(value), True, black)  # Render text with the number
                    text_rect = text.get_rect(center=(w + size_block // 2, h + size_block // 2))
                    screen.blit(text, text_rect)  # Blit the text on the screen

    def insert_2_or_4(self, indexes):
        x, y = indexes
        if random.random() <= 0.75:
            self._board[x][y] = 2
        else:
            self._board[x][y] = 4

    def move_left(self):
        for row in self._board:
            while 0 in row:
                row.remove(0)
            while len(row) != self._size:
                row.append(0)
        for i in range(self._size):
            for j in range(self._size - 1):
                if self._board[i][j] != 0 and self._board[i][j] == self._board[i][j + 1]:
                    self._board[i][j] *= 2
                    self._board[i][j + 1] = 0

    def move_right(self):
        for row in self._board:
            while 0 in row:
                row.remove(0)
            while len(row) != self._size:
                row.insert(0, 0)
        for i in range(self._size):
            for j in range(self._size - 1, 0, -1):
                if self._board[i][j] != 0 and self._board[i][j] == self._board[i][j - 1]:
                    self._board[i][j] *= 2
                    self._board[i][j - 1] = 0

    def move_up(self):
        for col in range(self._size):
            column = [self._board[row][col] for row in range(self._size)]
            while 0 in column:
                column.remove(0)
            while len(column) != self._size:
                column.append(0)
            for row in range(self._size):
                self._board[row][col] = column[row]
        for i in range(self._size - 1):
            for j in range(self._size):
                if self._board[i][j] != 0 and self._board[i][j] == self._board[i + 1][j]:
                    self._board[i][j] *= 2
                    self._board[i + 1][j] = 0

    def move_down(self):
        for col in range(self._size):
            column = [self._board[row][col] for row in range(self._size)]
            while 0 in column:
                column.remove(0)
            while len(column) != self._size:
                column.insert(0, 0)
            for row in range(self._size):
                self._board[row][col] = column[row]
        for i in range(self._size - 1):
            for j in range(self._size):
                if self._board[i][j] != 0 and self._board[i][j] == self._board[i + 1][j]:
                    self._board[i + 1][j] *= 2
                    self._board[i][j] = 0


size = 4
game = Game2048(size)
game.move_up()

white = (245, 245, 245)
gray = (128, 128, 128)
black = (0, 0, 0)

blocks = 4
size_block = 110
margin = 10
width = blocks * size_block + (blocks + 1) * margin
title_rect = pygame.Rect(0, 0, width, 110)
height = width + 110

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('2048')

# Set font for rendering numbers
pygame.font.init()
font = pygame.font.Font(None, 55)  # You can replace 'None' with a font file if needed

while game.get_empty_board():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_left()
            if event.key == pygame.K_RIGHT:
                game.move_right()
            if event.key == pygame.K_UP:
                game.move_up()
            if event.key == pygame.K_DOWN:
                game.move_down()
            pygame.draw.rect(screen, white, title_rect)
            # Handle game logic, e.g., move the tiles based on the key press
            empty = game.get_empty_board()
            random.shuffle(empty)
            random_num = empty.pop()
            game.insert_2_or_4(random_num)

            # Clear the screen
            screen.fill(white)

            # Draw the updated board
            game.draw_board()

    # Update the display
    pygame.display.update()
