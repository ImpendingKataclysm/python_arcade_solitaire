import arcade
import constants as c
from card import Card


class Game(arcade.Window):
    """
    Main window in which the game is displayed and played.
    """
    def __init__(self):
        self.card_deck = None
        self.held_cards = None
        self.held_cards_initial_position = None

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
        self.held_cards = []
        self.held_cards_initial_position = []

        self.create_deck()

    def on_draw(self):
        """
        Clear any sprites that are currently rendered and render all sprites in
        their initial positions.
        :return:
        """
        self.clear()
        self.card_deck.draw()

    def pull_card_to_top(self, card: arcade.Sprite):
        """
        Pulls the selected card to the top of the list
        :param card: The selected card
        """
        self.card_deck.remove(card)
        self.card_deck.append(card)

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Tracks mouse button presses and responds when the user clicks a card
        sprite or a card mat sprite.
        :param x: The x-coordinate of the clicked location
        :param y: The y-coordinate of the clicked location
        :param button: The mouse button
        :param key_modifiers:
        """
        clicked_cards = arcade.get_sprites_at_point((x, y), self.card_deck)

        if len(clicked_cards) > 0:
            primary_card = clicked_cards[-1]
            self.held_cards = [primary_card]
            self.held_cards_initial_position = [self.held_cards[0].position]

            self.pull_card_to_top(self.held_cards[0])

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Drag any held card sprites when the user moves the mouse while holding
        the button.
        :param x: The mouse's starting x-coordinate
        :param y: The mouse's starting y-coordinate
        :param dx: Change in horizontal distance
        :param dy: Change in vertical distance
        """
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Release any currently held cards.
        :param x: The mouse's x-coordinate on release
        :param y: The mouse's y-coordinate on release
        :param button: The mouse button
        :param key_modifiers:
        """
        if len(self.held_cards) > 0:
            self.held_cards = []
