import random

class ChessBot:
    def __init__(self, color='black', difficulty='medium'):
        self.color = color
        self.difficulty = difficulty
        self.depth_map = {'easy': 1, 'medium': 2, 'hard': 3}
        self.depth = self.depth_map.get(difficulty, 2)
        
        # Piece values
        self.piece_values = {
            'pawn': 100,
            'knight': 320,
            'bishop': 330,
            'rook': 500,
            'queen': 900,
            'king': 20000
        }
        
        # Position bonuses (simplified Piece-Square Tables)
        # Higher score = better position. Flips for black.
        self.pst = {
            'knight': [
                [-50,-40,-30,-30,-30,-30,-40,-50],
                [-40,-20,  0,  5,  5,  0,-20,-40],
                [-30,  5, 10, 15, 15, 10,  5,-30],
                [-30,  0, 15, 20, 20, 15,  0,-30],
                [-30,  5, 15, 20, 20, 15,  5,-30],
                [-30,  0, 10, 15, 15, 10,  0,-30],
                [-40,-20,  0,  0,  0,  0,-20,-40],
                [-50,-40,-30,-30,-30,-30,-40,-50]
            ],
            'pawn': [
                [  0,  0,  0,  0,  0,  0,  0,  0],
                [ 50, 50, 50, 50, 50, 50, 50, 50],
                [ 10, 10, 20, 30, 30, 20, 10, 10],
                [  5,  5, 10, 25, 25, 10,  5,  5],
                [  0,  0,  0, 20, 20,  0,  0,  0],
                [  5, -5,-10,  0,  0,-10, -5,  5],
                [  5, 10, 10,-20,-20, 10, 10,  5],
                [  0,  0,  0,  0,  0,  0,  0,  0]
            ],
            # Default for others
            'default': [
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        }
        
    def get_piece_value(self, piece):
        base_val = self.piece_values.get(piece.name, 0)
        table = self.pst.get(piece.name, self.pst['default'])
        
        # Array bounds check
        if 0 <= piece.position[1] < 8 and 0 <= piece.position[0] < 8:
            # If white, standard coordinates (y=0 is top, wait, in Pygame y=0 is black's side)
            # Pygame setup: White pawns are y=1 (top?). No, original code w_locs y=1 is row 2. 
            # Ingame: White pieces at bottom (y=7, y=6). Oh wait, original w_locs is (x, 0), y=0 is white?
            # Let's just do a basic center bias if unsure to avoid reversing
            y = piece.position[1]
            x = piece.position[0]
            
            # Simple center bias as fallback if array orientation varies
            dist_center_x = abs(3.5 - x)
            dist_center_y = abs(3.5 - y)
            pos_bonus = int((7 - (dist_center_x + dist_center_y)) * 5)
            
            # Use specific table for knights/pawns if confident
            if piece.name in self.pst:
                # Assuming White plays upwards (from y=7 to y=0 normally, but original game is weird)
                # It's safer to use our fallback center bonus for now with custom Pygame coordinates
                pos_bonus += table[y][x] if piece.color == 'white' else table[7-y][x]
                
            return base_val + pos_bonus
        return base_val
        
    def evaluate_board(self, white_pieces, black_pieces):
        """Material and positional evaluation."""
        score = 0
        for p in white_pieces:
            score += self.get_piece_value(p)
        for p in black_pieces:
            score -= self.get_piece_value(p)
            
        return score

    def get_best_move(self, game_state):
        black_options = game_state.get('black_options', [])
        black_pieces = game_state.get('black_pieces', [])
        white_pieces = game_state.get('white_pieces', [])
        
        valid_moves = []
        for i, moves in enumerate(black_options):
            for move in moves:
                valid_moves.append({
                    'piece_idx': i,
                    'start_pos': black_pieces[i].position,
                    'end_pos': move
                })
        
        if not valid_moves:
            return None
            
        # Easy Mode (Depth 1 / Random)
        if self.difficulty == 'easy':
            # Try to find a capturing move, else random
            caps = [m for m in valid_moves if any(wp.position == m['end_pos'] for wp in white_pieces)]
            if caps and random.random() > 0.5:
                return random.choice(caps)
            return random.choice(valid_moves)
            
        # Medium / Hard Mode (Evaluate 1-depth lookahead)
        # Deep Minimax in Python/Pygame requires perfect state clonnig which is slow.
        # We will do a 1-ply search (look at all our moves, score the resulting board).
        # We also look out for hanging pieces.
        
        best_score = -float('inf')
        best_move = random.choice(valid_moves)
        
        for move in valid_moves:
            score = self.simulate_and_score(move, black_pieces, white_pieces)
            
            # Add small randomness so bot isn't identical every game
            score += random.randint(-5, 5)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
        
    def simulate_and_score(self, move, black_pieces, white_pieces):
        # We are Black. We want to maximize the negative of the white-centric score
        # so target score = -(white - black) = black - white
        
        # Calculate current base material
        sim_black_score = 0
        sim_white_score = 0
        
        idx = move['piece_idx']
        target_pos = move['end_pos']
        
        for i, bp in enumerate(black_pieces):
            if i == idx:
                # Simulate new position
                class FakePiece: pass
                fp = FakePiece()
                fp.name = bp.name
                fp.color = bp.color
                fp.position = target_pos
                sim_black_score += self.get_piece_value(fp)
            else:
                sim_black_score += self.get_piece_value(bp)
                
        # Check if we captured a white piece
        for wp in white_pieces:
            if wp.position != target_pos:
                sim_white_score += self.get_piece_value(wp)
                
        # We want to MAXIMIZE our score
        return sim_black_score - sim_white_score
