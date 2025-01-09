import random
from typing import Tuple, Dict

import pygame

from game2048.game import Game2048

# Game Settings
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
    512: (240, 150, 50),
    1024: (240, 100, 50),
    2048: (240, 50, 50),
}

black = (0, 0, 0)


class GameManager:
    """
    A class to manage the graphical interface and gameplay loop for the 2048 game.
    """

    def __init__(self, game: Game2048) -> None:
        """
        Initialize the GameManager.

        Args:
            game (Game2048): The game logic instance.
        """
        self.game = game
        self.size_block = max(20, 600 // self.game.size)  # Dynamically calculate block size
        self.margin = max(5, self.size_block // 10)  # Margin proportional to block size
        self.width = self.game.size * self.size_block + (self.game.size + 1) * self.margin
        self.height = self.width + 110

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("game2048")
        self.font = pygame.font.Font(None, self.size_block // 2)

    def get_color(self, value: int) -> Tuple[int, int, int]:
        """
        Get the color for a given value.

        Args:
            value (int): The tile value.

        Returns:
            Tuple[int, int, int]: The RGB color for the value.
        """
        return colors.get(value, (255 - min(value, 255), 255 - (min(value, 255) // 2), 200))

    def draw_board(self) -> None:
        """
        Draw the game board on the screen.
        """
        self.screen.fill(black)
        font_score = pygame.font.SysFont('Arial', self.size_block // 3)
        text_score = font_score.render(f'Score: {self.game.score}', True, colors[256])
        self.screen.blit(text_score, (20, 35))

        for row in range(self.game.size):
            for col in range(self.game.size):
                value = self.game.board[row][col]
                w = col * self.size_block + (col + 1) * self.margin
                h = row * self.size_block + (row + 1) * self.margin + 110
                pygame.draw.rect(self.screen, self.get_color(value), (w, h, self.size_block, self.size_block))
                if value != 0:
                    text = self.font.render(str(value), True, black)
                    text_rect = text.get_rect(center=(w + self.size_block // 2, h + self.size_block // 2))
                    self.screen.blit(text, text_rect)
        pygame.display.update()

    def display_game_over(self) -> None:
        """
        Display the 'Game Over' message.
        """
        font_game_over = pygame.font.SysFont('Arial', self.size_block // 2)
        text_game_over = font_game_over.render("Game Over!", True, (255, 0, 0))
        text_rect = text_game_over.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_game_over, text_rect)
        pygame.display.update()

    def handle_events(self) -> bool:
        """
        Handle user input events.

        Returns:
            bool: False if the game should exit, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.game.move_left():
                    self.game.insert_2_or_4(random.choice(self.game.get_empty_cells()))
                elif event.key == pygame.K_RIGHT and self.game.move_right():
                    self.game.insert_2_or_4(random.choice(self.game.get_empty_cells()))
                elif event.key == pygame.K_UP and self.game.move_up():
                    self.game.insert_2_or_4(random.choice(self.game.get_empty_cells()))
                elif event.key == pygame.K_DOWN and self.game.move_down():
                    self.game.insert_2_or_4(random.choice(self.game.get_empty_cells()))
        return True

    def run(self) -> None:
        """
        Run the main game loop.
        """
        try:
            running = True
            while running:
                self.draw_board()
                if self.game.is_game_over():
                    self.display_game_over()
                    pygame.time.wait(2000)
                    break
                running = self.handle_events()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            pygame.quit()