from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class ChessEngine:
    def __init__(self):
        self.white_pieces = []
        self.black_pieces = []
        self.captured_pieces_white = []
        self.captured_pieces_black = []
        self.turn = 'white' # 'white' or 'black'
        self.winner = None
        self.game_over = False
        self.init_pieces()
        self.update_options()

    def init_pieces(self):
        # White
        w_types = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                   'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        w_locs = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        
        self.white_pieces = []
        for i, p_type in enumerate(w_types):
            self.white_pieces.append(self.create_piece('white', p_type, w_locs[i]))

        # Black
        b_types = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                   'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        b_locs = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        
        self.black_pieces = []
        for i, p_type in enumerate(b_types):
            self.black_pieces.append(self.create_piece('black', p_type, b_locs[i]))

    def create_piece(self, color, p_type, pos):
        if p_type == 'pawn': return Pawn(color, pos)
        if p_type == 'rook': return Rook(color, pos)
        if p_type == 'knight': return Knight(color, pos)
        if p_type == 'bishop': return Bishop(color, pos)
        if p_type == 'queen': return Queen(color, pos)
        if p_type == 'king': return King(color, pos)
        return None

    @property
    def white_locations(self):
        return [p.position for p in self.white_pieces]

    @property
    def black_locations(self):
        return [p.position for p in self.black_pieces]

    def update_options(self):
        self.black_options = self.check_options(self.black_pieces, self.black_locations)
        self.white_options = self.check_options(self.white_pieces, self.white_locations)
        
        # Determine check/checkmate logic handles filtering moves
        if self.turn == 'white':
             self.white_options = self.defend_check(self.white_pieces, self.white_options, 'white')
        else:
             self.black_options = self.defend_check(self.black_pieces, self.black_options, 'black')
             
        # Check game over conditions
        if self.turn == 'white' and not any(self.white_options):
             if self.is_in_check('white'): self.winner = 'black'
             else: self.winner = 'draw' # Stalemate
             self.game_over = True
        elif self.turn == 'black' and not any(self.black_options):
             if self.is_in_check('black'): self.winner = 'white'
             else: self.winner = 'draw'
             self.game_over = True

    def check_options(self, pieces, locations):
        all_moves_list = []
        # Note: Need both location lists for get_valid_moves
        w_locs = self.white_locations
        b_locs = self.black_locations
        for p in pieces:
            moves = p.get_valid_moves(None, w_locs, b_locs)
            all_moves_list.append(moves)
        return all_moves_list

    def defend_check(self, pieces, options, color):
        safe_options = []
        for i, p in enumerate(pieces):
            piece_safe_moves = []
            for move in options[i]:
                original_pos = p.position
                enemy_pieces = self.black_pieces if color == 'white' else self.white_pieces
                
                # Check Capture
                captured_index = -1
                temp_enemy = None
                for ei, ep in enumerate(enemy_pieces):
                    if ep.position == move:
                        captured_index = ei
                        temp_enemy = enemy_pieces.pop(captured_index)
                        break
                
                p.position = move
                
                # Check safety
                if color == 'white':
                    enemy_moves = self.check_options(self.black_pieces, self.black_locations) # Recalculate enemy moves
                    king_pos = [wp.position for wp in self.white_pieces if wp.name == 'king'][0]
                    if not any(king_pos in m_list for m_list in enemy_moves):
                         piece_safe_moves.append(move)
                else:
                    enemy_moves = self.check_options(self.white_pieces, self.white_locations)
                    king_pos = [bp.position for bp in self.black_pieces if bp.name == 'king'][0]
                    if not any(king_pos in m_list for m_list in enemy_moves):
                         piece_safe_moves.append(move)

                # Restore
                p.position = original_pos
                if temp_enemy:
                    enemy_pieces.insert(captured_index, temp_enemy)
            safe_options.append(piece_safe_moves)
        return safe_options

    def is_in_check(self, color):
        if color == 'white':
             king_pos = [p.position for p in self.white_pieces if p.name == 'king'][0]
             enemy_options = self.check_options(self.black_pieces, self.black_locations)
             return any(king_pos in moves for moves in enemy_options)
        else:
             king_pos = [p.position for p in self.black_pieces if p.name == 'king'][0]
             enemy_options = self.check_options(self.white_pieces, self.white_locations)
             return any(king_pos in moves for moves in enemy_options)

    def move_piece(self, start_pos, end_pos):
        # 1. Identify piece
        target_pieces = self.white_pieces if self.turn == 'white' else self.black_pieces
        piece_idx = -1
        piece = None
        for i, p in enumerate(target_pieces):
            if p.position == tuple(start_pos):
                piece = p
                piece_idx = i
                break
        
        if not piece: return False, "No piece at start position"
        
        # 2. Validate Move
        # We need the pre-calculated valid moves from update_options logic
        # But 'piece' object doesn't store them.
        # We stored them in self.white_options / self.black_options matching index
        options = self.white_options if self.turn == 'white' else self.black_options
        
        if piece_idx >= len(options): return False, "Internal Error"
        valid_moves = options[piece_idx]
        
        if tuple(end_pos) not in valid_moves:
             return False, "Invalid Move"
             
        # 3. Execute Move
        piece.position = tuple(end_pos)
        
        # 4. Handle Capture
        enemy_pieces = self.black_pieces if self.turn == 'white' else self.white_pieces
        captured_list = self.captured_pieces_white if self.turn == 'white' else self.captured_pieces_black
        
        for i, ep in enumerate(enemy_pieces):
            if ep.position == tuple(end_pos):
                captured_list.append(ep) # Add to captured
                enemy_pieces.pop(i) # Remove from board
                break
                
        # 5. Handle Promotion (Auto-Queen for now, or need logic)
        if piece.name == 'pawn':
            if (piece.color == 'white' and piece.position[1] == 7) or \
               (piece.color == 'black' and piece.position[1] == 0):
                # Promote to Queen by default for simpler API initially
                # Or handle promotion input
                # Let's simple promote to Queen
                 if piece.color == 'white':
                    self.white_pieces[piece_idx] = Queen('white', piece.position)
                 else:
                    self.black_pieces[piece_idx] = Queen('black', piece.position)

        # 6. Switch Turn
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.update_options()
        
        return True, "Move Successful"

    def get_state(self):
        return {
            'board': {
                'white': [{'type': p.name, 'pos': p.position} for p in self.white_pieces],
                'black': [{'type': p.name, 'pos': p.position} for p in self.black_pieces]
            },
            'turn': self.turn,
            'game_over': self.game_over,
            'winner': self.winner,
            'captured': {
                'white': [p.name for p in self.captured_pieces_white],
                'black': [p.name for p in self.captured_pieces_black]
            }
        }
