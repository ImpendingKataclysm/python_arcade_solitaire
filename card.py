import arcade
import constants as c


class Card(arcade.Sprite):
    """
    Sprite for a card. Takes a suit and a value, which are used to determine
    its image file.
    """
    def __init__(self, suit, value, scale=1):
        self.suit = suit
        self.value = value
        self.image_file = f'{c.CARD_IMAGE_PATH}{self.suit}{self.value}.png'

        super().__init__(self.image_file, scale, hit_box_algorithm='None')
