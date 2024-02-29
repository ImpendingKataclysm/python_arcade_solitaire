import arcade
import constants as c
from card import Card


class Game(arcade.Window):
    """
    Main window in which the game is displayed and played.
    """
    def __init__(self):
        self.card_deck = None

        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)
        arcade.set_background_color(arcade.color.CERULEAN_FROST)

    def create_deck(self):
        """
        Creates a Card Sprite with each possible card value for each possible
        card suit and adds each card to the card_deck.
        """
        self.card_deck = arcade.SpriteList()
        for suit in c.CARD_SUITS:
            for value in c.CARD_VALUES:
                card = Card(suit, value, c.CARD_SCALE)
                card.position = c.START_X, c.BOTTOM_Y
                self.card_deck.append(card)

    def setup(self):
        """
        Create and shuffle the deck of cards and display the initial game state.
        """
        self.create_deck()

    def on_draw(self):
        """
        Clear any sprites that are currently rendered and render all sprites in
        their initial positions.
        :return:
        """
        self.clear()
        self.card_deck.draw()

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        pass

    def on_mouse_release(self, x: float, y: float, button: int, key_modifiers: int):
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        pass
