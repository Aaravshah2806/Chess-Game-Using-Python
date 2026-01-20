from .piece import Piece

class Rook(Piece):
    def __init__(self, color, position, image=None, small_image=None):
        super().__init__('rook', color, position, image, small_image)

    def get_valid_moves(self, pieces, white_locations, black_locations):
        moves_list = []
        if self.color == 'white':
            enemies_list = black_locations
            friends_list = white_locations
        else:
            enemies_list = white_locations
            friends_list = black_locations
            
        # Directions: up, down, left, right
        # (0, 1), (0, -1), (1, 0), (-1, 0)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            path = True
            chain = 1
            while path:
                target = (self.position[0] + (chain * dx), self.position[1] + (chain * dy))
                if 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                    if target not in friends_list:
                        moves_list.append(target)
                        if target in enemies_list:
                            path = False
                        chain += 1
                    else:
                        path = False
                else:
                    path = False
        return moves_list
