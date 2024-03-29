# Screen Dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Screen Title (includes game instructions)
SCREEN_TITLE = 'Drag and Drop Cards. Press "R" to restart.'

# Card Sprite Sizing
CARD_SCALE = 0.6
CARD_WIDTH = CARD_SCALE * 140
CARD_HEIGHT = CARD_SCALE * 190

# Card Mat Sprite Sizing
CARD_MAT_OVERSIZE_PERCENT = 1.25
CARD_MAT_WIDTH = CARD_MAT_OVERSIZE_PERCENT * CARD_WIDTH
CARD_MAT_HEIGHT = CARD_MAT_OVERSIZE_PERCENT * CARD_HEIGHT

# Card Display
CARD_VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
RED_SUITS = ['Hearts', 'Diamonds']
BLACK_SUITS = ['Spades', 'Clubs']
CARD_SUITS = RED_SUITS + BLACK_SUITS
CARD_IMAGE_PATH = ':resources:images/cards/card'
FACE_DOWN_IMAGE = ':resources:images/cards/cardBack_blue5.png'
CARDS_TO_SKIP = 3

# Card Row Spacing/Positioning
HORIZONTAL_MARGIN_PERCENT = 0.1
VERTICAL_MARGIN_PERCENT = 0.1
HORIZONTAL_MAT_OFFSET = CARD_MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT
VERTICAL_MAT_OFFSET = CARD_MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
START_X = CARD_MAT_WIDTH / 2 + HORIZONTAL_MAT_OFFSET
BOTTOM_Y = CARD_MAT_HEIGHT / 2 + VERTICAL_MAT_OFFSET
TOP_Y = SCREEN_HEIGHT - CARD_MAT_HEIGHT / 2 - VERTICAL_MAT_OFFSET
MIDDLE_Y = TOP_Y - CARD_MAT_HEIGHT - VERTICAL_MAT_OFFSET
X_SPACING = CARD_MAT_WIDTH + HORIZONTAL_MAT_OFFSET
MIDDLE_ROW_LEN = 7
TOP_ROW_LEN = 4
CARD_VERTICAL_FAN = CARD_HEIGHT * CARD_SCALE * 0.3

# Card Pile Tracking
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
MIDDLE_PILE_1 = 2
MIDDLE_PILE_2 = 3
MIDDLE_PILE_3 = 4
MIDDLE_PILE_4 = 5
MIDDLE_PILE_5 = 6
MIDDLE_PILE_6 = 7
MIDDLE_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12
