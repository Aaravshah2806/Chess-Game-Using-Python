import pygame

class Piece:
    def __init__(self, name, color, position, image, small_image):
        self.name = name
        self.color = color
        self.position = position  # Tuple (x, y)
        self.image = image
        self.small_image = small_image
        self.rect = self.image.get_rect()
    
    def draw(self, screen):
        # Position is grid coordinates (0-7), we need to convert to pixels
        # Grid 0,0 is top-left.
        # Original code: (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10)
        pixel_x = self.position[0] * 100 + 10
        pixel_y = self.position[1] * 100 + 10
        screen.blit(self.image, (pixel_x, pixel_y))

    def get_valid_moves(self, board_state):
        """
        board_state: A list of all pieces or a board object that allows checking occupancy.
        Returns a list of valid move tuples (x, y).
        """
        raise NotImplementedError("Subclasses must implement get_valid_moves")
