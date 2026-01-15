from .piece import Piece

class Pawn(Piece):
    def __init__(self, color, position, image, small_image):
        super().__init__('pawn', color, position, image, small_image)

    def get_valid_moves(self, pieces, white_locations, black_locations):
        moves_list = []
        # Combine locations for occupancy check
        all_occupied = white_locations + black_locations
        
        # 1. Setup direction and rules based on color
        # White moves +1 (down) in y?? Wait, original code:
        # white_locations ... (0,0) etc.
        # black_locations ... (0,7) etc.
        #
        # IN ORIGINAL CODE check_pawn:
        # direction = 1 if color == 'white' else -1
        # start_row = 1 if color == 'white' else 6
        #
        # Wait, usually white is at bottom (row 6/7) and moves UP (-1).
        # Let's check original logic again.
        # white_locations = [(0, 0), (1, 0), ... (0, 1) ... ] -> Rows 0 and 1.
        # black_locations = [(0, 7) ... (0, 6) ... ] -> Rows 7 and 6.
        # Board drawing:
        # row * 100
        # So row 0 is top.
        # row 7 is bottom.
        #
        # Code says:
        # direction = 1 if color == 'white' else -1.
        # So White moves DOWN (y increases).
        # Black moves UP (y decreases).
        # This is inverted from standard chess but I must follow the original code's logic.
        
        direction = 1 if self.color == 'white' else -1
        start_row = 1 if self.color == 'white' else 6
        
        enemies_list = black_locations if self.color == 'white' else white_locations
        
        x, y = self.position
        
        # 2. Forward Movement (One Square)
        forward_one = (x, y + direction)
        if 0 <= forward_one[1] <= 7 and forward_one not in all_occupied:
            moves_list.append(forward_one)
            
            # Check for 2-square move ONLY if the 1st square was empty
            # And we are at start row
            forward_two = (x, y + (2 * direction))
            if y == start_row and forward_two not in all_occupied:
                moves_list.append(forward_two)
                
        # 3. Diagonal Captures
        for dx in [-1, 1]:
            capture_square = (x + dx, y + direction)
            if capture_square in enemies_list:
                moves_list.append(capture_square)
        
        return moves_list
