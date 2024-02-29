import arcade
from game import Game


def main():
    game_window = Game()
    game_window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
