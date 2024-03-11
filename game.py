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

    def pull_card_to_top(self, card: arcade.Sprite):
        """
        Pulls the selected card to the top of the list
        :param card: The selected card
        """
        self.card_deck.remove(card)
        self.card_deck.append(card)

    def validate_color(self, pile_index):
        """
        Check that the currently held card is the opposite color from the top
        card on its new pile.
        :param pile_index: The pile on which the card is being placed
        :return: True if the colors do not match (move is valid), False if not
        """
        top_card_suit = self.card_piles[pile_index][-1].suit
        held_card_suit = self.held_cards[0].suit
        red_on_black = held_card_suit in c.RED_SUITS and top_card_suit in c.BLACK_SUITS
        black_on_red = held_card_suit in c.BLACK_SUITS and top_card_suit in c.RED_SUITS

        return red_on_black or black_on_red

    def check_card_order(self, top_card):
        """
        Get the difference in positions (indices) of the top card's value and
        the currently held card's value.
        :param top_card: The top card in the pile to which the held card is
        being moved
        :return: The difference between the top card value index and the held
        card value index
        """
        top_card_index = c.CARD_VALUES.index(top_card.value)
        held_card_index = c.CARD_VALUES.index(self.held_cards[0].value)

        return top_card_index - held_card_index

    def move_card(self, card, card_pile, new_x, new_y):
        """
        Moves a selected card to a new pile by updating the card sprite's
        position and moving the sprite to the list corresponding to the new pile.
        :param card: The card being moved
        :param card_pile: The pile to which the card is being moved
        :param new_x: The card's updated x coordinate
        :param new_y: The card's updated y coordinate
        """
        pile_index = self.card_mats.index(card_pile)
        card.position = new_x, new_y
        self.move_card_to_pile(card, pile_index)

    def play_to_middle(self, card_pile):
        """
        Checks the validity of moves to the middle play section. For a move to pass:
        1. The card cannot be an Ace.
        2. If the new pile is empty, the card must be a King.
        3. If the new pile is not empty:
        - The top card must be the opposite color of the played card
        - The played card must be 1 value lower than the top card
        :param card_pile: The Sprite for the pile on which the card sprite is
        placed
        :return: True if the move is valid, False if not
        """
        reset_move = True
        pile_index = self.card_mats.index(card_pile)

        if self.held_cards[0].value == 'A':
            pass
        elif len(self.card_piles[pile_index]) > 0:
            top_card = self.card_piles[pile_index][-1]

            if self.validate_color(pile_index) \
                    and self.check_card_order(top_card) == 1:
                for i, dropped_card in enumerate(self.held_cards):
                    fan_offset = c.CARD_VERTICAL_FAN * (i + 1)
                    self.move_card(
                        dropped_card,
                        card_pile,
                        top_card.center_x,
                        top_card.center_y - fan_offset
                    )

                reset_move = False
        else:
            if self.held_cards[0].value == 'K':
                for i, dropped_card in enumerate(self.held_cards):
                    fan_offset = c.CARD_VERTICAL_FAN * i
                    self.move_card(
                        dropped_card,
                        card_pile,
                        card_pile.center_x,
                        card_pile.center_y - fan_offset
                    )

                reset_move = False

        return reset_move

    def play_to_top(self, card_pile):
        """
        Checks the validity of moves to the top play section. For a move to pass:
        1. If the new pile is empty, the card must be an Ace.
        2. If the new pile is not empty:
        - The top card must be the same suit as the played card
        - The played card must be 1 value higher than the top card
        :param card_pile: The Sprite for the pile on which the card sprite is
        placed.
        :return: True if the move is valid, false if not
        """
        reset_position = True
        primary_held_card = self.held_cards[0]
        pile_index = self.card_mats.index(card_pile)
        new_pile = self.card_piles[pile_index]

        if len(self.held_cards) == 1:
            if len(new_pile) == 0:
                if primary_held_card.value == 'A':
                    self.move_card(
                        primary_held_card,
                        card_pile,
                        card_pile.center_x,
                        card_pile.center_y
                    )

                    reset_position = False
            else:
                top_card = self.card_piles[pile_index][-1]
                if self.check_card_order(top_card) == -1 \
                        and top_card.suit == primary_held_card.suit:
                    self.move_card(
                        primary_held_card,
                        card_pile,
                        card_pile.center_x,
                        card_pile.center_y
                    )

                    reset_position = False

        return reset_position

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
                reset_position = self.play_to_middle(closest_card_pile)
            elif c.TOP_PILE_1 <= pile_index <= c.TOP_PILE_4:
                reset_position = self.play_to_top(closest_card_pile)

        if reset_position:
            for i, card in enumerate(self.held_cards):
                card.position = self.held_cards_initial_position[i]

    def draw_cards_with_skip(self, card_pile):
        """
        Draws CARDS_TO_SKIP cards from the bottom face down mat and places them face up
        on the bottom face up mat, with the last card on top.
        :param card_pile: The card pile from which the cards are drawn
        """
        card_mat = self.card_mats[c.BOTTOM_FACE_UP_PILE]
        for i in range(c.CARDS_TO_SKIP):
            if len(card_pile) == 0:
                break
            top_card = card_pile[-1]
            top_card.turn_face_up()
            self.move_card(
                top_card,
                card_mat,
                card_mat.center_x,
                card_mat.center_y
            )
            self.pull_card_to_top(top_card)

    def flip_deck(self, mat_index):
        """
        Flips the deck back to the bottom left (face down) pile when all cards
        have been moved to the bottom right (face up) pile.
        :param mat_index: The index indicating the mat which has been clicked
        (the function only runs when the mat in the bottom left corner is clicked
        while empty).
        """
        bottom_left_pile = self.card_piles[c.BOTTOM_FACE_DOWN_PILE]
        bottom_right_pile = self.card_piles[c.BOTTOM_FACE_UP_PILE]
        bottom_left_mat = self.card_mats[c.BOTTOM_FACE_DOWN_PILE]

        if mat_index == c.BOTTOM_FACE_DOWN_PILE and len(bottom_left_pile) == 0:
            temp_list = bottom_right_pile.copy()

            for card in reversed(temp_list):
                card.turn_face_down()
                self.move_card(
                    card,
                    bottom_left_mat,
                    bottom_left_mat.center_x,
                    bottom_left_mat.center_y
                )

    def setup(self):
        """
        Create the deck of cards and display the initial game state: all the
        rows are dealt out with the remaining cards in the bottom face down
        pile.
        """
        self.held_cards = []
        self.held_cards_initial_position = []
        self.card_piles = [[] for _ in range(c.PILE_COUNT)]
        self.card_mats: arcade.SpriteList = arcade.SpriteList()

        self.create_deck()
        self.shuffle_deck()
        self.create_card_mats()

        for card in self.card_deck:
            self.card_piles[c.BOTTOM_FACE_DOWN_PILE].append(card)

        for pile_index in range(c.MIDDLE_PILE_1, c.MIDDLE_PILE_7 + 1):
            for i in range(pile_index - c.MIDDLE_PILE_1 + 1):
                card = self.card_piles[c.BOTTOM_FACE_DOWN_PILE].pop()
                self.card_piles[pile_index].append(card)

                fan_offset = c.CARD_VERTICAL_FAN * i
                card.position = self.card_mats[pile_index].center_x, \
                                self.card_mats[pile_index].center_y - fan_offset

                self.pull_card_to_top(card)

            last_card = self.card_piles[pile_index][-1]
            last_card.turn_face_up()

    def on_draw(self):
        """
        Clear any sprites that are currently rendered and render all sprites in
        their initial positions.
        """
        self.clear()
        self.card_mats.draw()
        self.card_deck.draw()

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Registers a clicked card sprite as a held card so that it can be dragged
        and dropped, provided that the card is not in the top row.
        :param x: The x-coordinate of the clicked location
        :param y: The y-coordinate of the clicked location
        :param button: The mouse button
        :param key_modifiers:
        """
        clicked_cards = arcade.get_sprites_at_point((x, y), self.card_deck)

        if len(clicked_cards) > 0:
            primary_card = clicked_cards[-1]
            pile_index = self.get_pile_for_card(primary_card)
            card_pile = self.card_piles[pile_index]

            if pile_index == c.BOTTOM_FACE_DOWN_PILE:
                self.draw_cards_with_skip(card_pile)
            elif pile_index < c.TOP_PILE_1:
                self.held_cards = [primary_card]
                self.held_cards_initial_position = [self.held_cards[0].position]
                self.pull_card_to_top(self.held_cards[0])

                card_index = card_pile.index(primary_card)

                for i in range(card_index + 1, len(card_pile)):
                    card = card_pile[i]
                    self.held_cards.append(card)
                    self.held_cards_initial_position.append(card.position)
                    self.pull_card_to_top(card)
        else:
            clicked_mats = arcade.get_sprites_at_point((x, y), self.card_mats)

            if len(clicked_mats) > 0:
                mat = clicked_mats[0]
                mat_index = self.card_mats.index(mat)
                self.flip_deck(mat_index)

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
            self.update_card_position()

            self.held_cards = []

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Restarts the game when the user presses 'R'.
        :param symbol: The key entered by the user
        :param modifiers:
        """
        if symbol == arcade.key.R:
            self.setup()
