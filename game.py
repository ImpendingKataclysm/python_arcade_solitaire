import arcade
import random
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
        self.card_mats = None
        self.card_piles = None

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

    def shuffle_deck(self):
        """
        Shuffles the deck of cards by taking each card and swapping its position
        with that of another, randomly selected card.
        """
        for pos1 in range(len(self.card_deck)):
            pos2 = random.randrange(len(self.card_deck))
            self.card_deck.swap(pos1, pos2)

    def define_card_mat(self):
        """
        Create a slate blue card mat sprite with the preset width and height.
        :return: The new card mat sprite
        """
        return arcade.SpriteSolidColor(
            int(c.CARD_MAT_WIDTH),
            int(c.CARD_MAT_HEIGHT),
            arcade.csscolor.MIDNIGHT_BLUE
        )

    def create_card_row(self, row_len, y):
        """
        Create a new row of card piles
        :param row_len: The number of card piles in the row
        :param y: The y-axis position of the row
        """
        for i in range(row_len):
            pile = self.define_card_mat()
            pile.position = c.START_X + i * c.X_SPACING, y
            self.card_mats.append(pile)

    def create_card_mats(self):
        """
        Create the rows of card mat sprites on which the cards will be rendered.
        """
        self.card_mats: arcade.SpriteList = arcade.SpriteList()
        pile = self.define_card_mat()

        # Create bottom face down pile
        pile.position = c.START_X, c.BOTTOM_Y
        self.card_mats.append(pile)

        # Create bottom face up pile
        pile = self.define_card_mat()
        pile.position = c.START_X + c.X_SPACING, c.BOTTOM_Y
        self.card_mats.append(pile)

        # Create the 7 middle piles
        self.create_card_row(c.MIDDLE_ROW_LEN, c.MIDDLE_Y)

        # Create the top 4 piles
        self.create_card_row(c.TOP_ROW_LEN, c.TOP_Y)

    def get_pile_for_card(self, card):
        """
        Identify the index for a given card from a pile list
        :param card: The card whose index to search for
        :return: The card's index in the pile list, or None if the card is not
        present
        """
        for i, pile in enumerate(self.card_piles):
            if card in pile:
                return i

        return None

    def remove_card_from_pile(self, card):
        """
        Searches the card piles for the given card, and removes the card from
        its pile if found.
        :param card: The card to search for and remove
        """
        for pile in self.card_piles:
            if card in pile:
                pile.remove(card)
                break

    def move_card_to_pile(self, card, pile_index):
        """
        Move a given card from its current pile to a new one.
        :param card: The card to move
        :param pile_index: The index of the new pile where the card is being moved
        """
        self.remove_card_from_pile(card)
        self.card_piles[pile_index].append(card)

    def setup(self):
        """
        Create the deck of cards and display the initial game state: all the
        rows are dealt out with the remaining cards in the bottom face down
        pile.
        """
        self.held_cards = []
        self.held_cards_initial_position = []
        self.card_piles = [[] for _ in range(c.PILE_COUNT)]

        self.create_deck()
        self.shuffle_deck()
        self.create_card_mats()

        for card in self.card_deck:
            self.card_piles[c.BOTTOM_FACE_DOWN_PILE].append(card)

    def on_draw(self):
        """
        Clear any sprites that are currently rendered and render all sprites in
        their initial positions.
        :return:
        """
        self.clear()
        self.card_mats.draw()
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

    def play_to_middle(self, pile_index, card_pile):
        """
        Moves the currently held card(s) from their current pile to a new pile
        in the middle play area.
        :param pile_index: The index of the pile to which the card is being moved.
        :param card_pile: The Sprite for the pile on which the card sprite is
        placed
        """
        if len(self.card_piles[pile_index]) > 0:
            top_card = self.card_piles[pile_index][-1]

            for i, dropped_card in enumerate(self.held_cards):
                dropped_card.position = top_card.center_x, \
                                        top_card.center_y - c.CARD_VERTICAL_FAN * (i + 1)
                self.move_card_to_pile(dropped_card, pile_index)
        else:
            for i, dropped_card in enumerate(self.held_cards):
                dropped_card.position = card_pile.center_x, \
                                        card_pile.center_y - c.CARD_VERTICAL_FAN * i
                self.move_card_to_pile(dropped_card, pile_index)

    def update_card_position(self):
        """
        Checks to see if the held card is touching a mat sprite or a card sprite.
        If the card is touching another sprite, its position is updated to match
        the closest card mat's position, otherwise the card is sent back to its
        initial position.
        """
        primary_held_card = self.held_cards[0]

        closest_card_pile, distance = arcade.get_closest_sprite(
            primary_held_card,
            self.card_mats
        )

        other_card_sprites = arcade.SpriteList()
        for card in self.card_deck:
            if card != primary_held_card:
                other_card_sprites.append(card)

        closest_card_sprite, sprite_distance = arcade.get_closest_sprite(
            primary_held_card,
            other_card_sprites
        )

        reset_position = True

        if arcade.check_for_collision(primary_held_card, closest_card_pile) \
                or arcade.check_for_collision(primary_held_card, closest_card_sprite):
            pile_index = self.card_mats.index(closest_card_pile)

            if pile_index == self.get_pile_for_card(primary_held_card):
                pass
            elif c.MIDDLE_PILE_1 <= pile_index <= c.MIDDLE_PILE_7:
                self.play_to_middle(pile_index, closest_card_pile)
                reset_position = False
            elif c.TOP_PILE_1 <= pile_index <= c.TOP_PILE_4:
                if len(self.held_cards) == 1:
                    primary_held_card.position = closest_card_pile.center_x, closest_card_pile.center_y
                    self.move_card_to_pile(primary_held_card, pile_index)
                    reset_position = False

        if reset_position:
            for i, card in enumerate(self.held_cards):
                card.position = self.held_cards_initial_position[i]

    def on_mouse_release(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Release any currently held cards.
        :param x: The mouse's x-coordinate on release
        :param y: The mouse's y-coordinate on release
        :param button: The mouse button
        :param key_modifiers:
        """
        if len(self.held_cards) > 0:
            self.update_card_position()

            self.held_cards = []
