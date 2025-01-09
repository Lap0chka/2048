from game2048.game import Game2048
from game2048.manager import GameManager

size = 4

def main():
    game = Game2048(size)
    manager = GameManager(game)
    manager.run()

if __name__ == '__main__':
    main()