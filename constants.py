import pygame

# Screen Dimensions
WIDTH = 1000
HEIGHT = 900
FPS = 60

# Colors
LIGHT_GREY = (211, 211, 211)  # Approximate for 'light grey'
GRAY = 'gray'
GOLD = 'gold'
BLACK = 'black'
WHITE = 'white'
RED = 'red'
BLUE = 'blue'
DARK_GRAY = 'dark gray'
DARK_RED = 'dark red'
DARK_BLUE = 'dark blue'

# Fonts (Initialized in Game or later to avoid pre-init issues, but we can define sizes)
FONT_SIZE_SMALL = 20
FONT_SIZE_MEDIUM = 40
FONT_SIZE_BIG = 50

# Piece Lists (used for ordering images)
PIECE_LIST = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
