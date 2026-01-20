from .piece import Piece

class King(Piece):
    def __init__(self, color, position, image=None, small_image=None):
        super().__init__('king', color, position, image, small_image)

    def get_valid_moves(self, pieces, white_locations, black_locations):
        moves_list = []
        if self.color == 'white':
            friends_list = white_locations
        else:
            friends_list = black_locations
            
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0),
                   (-1, 1), (-1, -1), (0, 1), (0, -1)]
        
        for i in range(8):
            target = (self.position[0] + targets[i][0], self.position[1] + targets[i][1])
            if 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                 if target not in friends_list:
                    moves_list.append(target)
        return moves_list
