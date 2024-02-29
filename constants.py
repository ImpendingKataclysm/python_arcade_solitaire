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

# Card Mat Spacing/Positioning
HORIZONTAL_MARGIN_PERCENT = 0.1
VERTICAL_MARGIN_PERCENT = 0.1
START_X = CARD_MAT_WIDTH / 2 + CARD_MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT
BOTTOM_Y = CARD_MAT_HEIGHT / 2 + CARD_MAT_WIDTH * VERTICAL_MARGIN_PERCENT

# Card Images
CARD_VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
CARD_SUITS = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
CARD_IMAGE_PATH = ':resources:images/cards/card'
