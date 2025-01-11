from game2048.db import DatabaseManager
from game2048.game import Game2048
from game2048.manager import GameManager


def main() -> None:
    """
    Main entry point for running the 2048 game.

    - Initializes the game board and manager.
    - Runs the game loop.
    - Saves the score to the database.
    - Displays the leaderboard.

    """
    size = 4
    name = input("Enter your name: ").strip() or "Anonymous"
    game = Game2048(size)
    manager = GameManager(game)
    manager.run()
    score = game.score
    print(f"Game over! Final score for {name}: {score}")
    db = DatabaseManager()
    try:
        db.update_or_create_row(name, score)
        rows = db.get_all_rows()
        for index, row in enumerate(rows, 1):
            name, score = row
            print(f"{index}. {name} has score {score}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
