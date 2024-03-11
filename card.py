import arcade
import constants as c


class Card(arcade.Sprite):
    """
    Sprite for a card. Takes a suit parameter and a value parameter, which
    determine its image file name, and a scale parameter with a default value of
    1. The is_face_up attribute is set to False by default, so the Card will
    automatically be displayed face down.
    """
    def __init__(self, suit, value, scale=1):
        self.suit = suit
        self.value = value
        self.image_file_name = f'{c.CARD_IMAGE_PATH}{self.suit}{self.value}.png'
        self.is_face_up = False

        super().__init__(c.FACE_DOWN_IMAGE, scale, hit_box_algorithm='None')

    def turn_face_down(self):
        """
        Displays the card face down by showing its FACE_DOWN_IMAGE resource and
        setting its is_face_up attribute to False.
        """
        self.texture = arcade.load_texture(c.FACE_DOWN_IMAGE)
        self.is_face_up = False

    def turn_face_up(self):
        """
        Displays the card face up by showing the resource indicated by the card's
        image_file_name attribute and setting its is_face_up attribute to True.
        """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """
        Indicates whether a card is face down or not.
        :return: True if the card's is_face_up attribute is False, or False if
        is_face_up is True
        """
        return not self.is_face_up
