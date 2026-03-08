import pygame
from constants import *
from board import Board
from constants import *
from board import Board
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from bot import ChessBot

class Game:
    def __init__(self, play_vs_ai=True, ai_difficulty='medium', time_control='untimed'):
        import os
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('Chess Game')
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)
        self.timer = pygame.time.Clock()
        
        self.board = Board()
        self.load_images()
        self.init_pieces()
        
        # AI Config
        self.play_vs_ai = play_vs_ai
        if self.play_vs_ai:
            self.bot = ChessBot(color='black', difficulty=ai_difficulty)
            
        # Time Control Config
        self.time_control = time_control
        self.init_clocks()
        
        # Game State
        self.turn_step = 0 # 0: White Select, 1: White Move, 2: Black Select, 3: Black Move
        self.selection = 100
        self.valid_moves = []
        self.history = [] # Stack for undo (stores piece states and captured lists)
        self.move_log = [] # Stack for algebraic notation
        
        self.captured_pieces_white = []
        self.captured_pieces_black = []
        self.last_move = None
        
        self.counter = 0
        self.winner = ''
        self.game_over = False
        
        # Initial Options Calc
        self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
        self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')

    def init_clocks(self):
        # Time in milliseconds
        if self.time_control == 'blitz':
            self.white_time = 3 * 60 * 1000
            self.black_time = 3 * 60 * 1000
        elif self.time_control == 'rapid':
            self.white_time = 10 * 60 * 1000
            self.black_time = 10 * 60 * 1000
        else:
            self.white_time = float('inf')
            self.black_time = float('inf')
            
        self.last_tick = pygame.time.get_ticks()

    def load_images(self):
        # Helper to load and scale
        def load(path, size):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (size, size))
            
        self.images = {}
        pieces = ['queen', 'king', 'rook', 'bishop', 'knight', 'pawn']
        for color in ['white', 'black']:
            for piece in pieces:
                key = f"{color}_{piece}"
                path = f"images/{color}-{piece}.png"
                self.images[key] = load(path, 80)
                self.images[f"{key}_small"] = load(path, 45)

    def init_pieces(self):
        # Define initial setup matching original code
        # White
        w_types = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                   'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        w_locs = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        
        self.white_pieces = []
        for i, p_type in enumerate(w_types):
            game_piece = self.create_piece('white', p_type, w_locs[i])
            self.white_pieces.append(game_piece)

        # Black
        b_types = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                   'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        b_locs = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        
        self.black_pieces = []
        for i, p_type in enumerate(b_types):
            game_piece = self.create_piece('black', p_type, b_locs[i])
            self.black_pieces.append(game_piece)

    def create_piece(self, color, p_type, pos):
        key = f"{color}_{p_type}"
        img = self.images[key]
        small_img = self.images[f"{key}_small"]
        
        if p_type == 'pawn': return Pawn(color, pos, img, small_img)
        if p_type == 'rook': return Rook(color, pos, img, small_img)
        if p_type == 'knight': return Knight(color, pos, img, small_img)
        if p_type == 'bishop': return Bishop(color, pos, img, small_img)
        if p_type == 'queen': return Queen(color, pos, img, small_img)
        if p_type == 'king': return King(color, pos, img, small_img)
        return None

    @property
    def white_locations(self):
        return [p.position for p in self.white_pieces]

    @property
    def black_locations(self):
        return [p.position for p in self.black_pieces]

    def check_options(self, pieces, locations, turn):
        all_moves_list = []
        w_locs = self.white_locations
        b_locs = self.black_locations
        
        for p in pieces:
            # We must pass the dynamic locations
            # The piece classes expect lists of tuples
            moves = p.get_valid_moves(None, w_locs, b_locs)
            all_moves_list.append(moves)
        return all_moves_list
        
    def check_valid_moves(self):
        if self.turn_step < 2:
            options_list = self.white_options
        else:
            options_list = self.black_options
        if self.selection < len(options_list):
            valid_options = options_list[self.selection]
            return valid_options
        return []

    def draw_game(self):
        bg_color = (25, 27, 36)
        self.screen.fill(bg_color)
        self.board.draw(self.screen)
        self.board.draw_status_text(self.screen, self.font, self.turn_step, self.medium_font)
        
        # Draw Last Move Highlight
        if self.last_move:
            s_pos, e_pos = self.last_move
            highlight_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            highlight_surface.fill((245, 235, 100, 120)) # Transparent Yellow
            self.screen.blit(highlight_surface, (s_pos[0] * 100, s_pos[1] * 100))
            self.screen.blit(highlight_surface, (e_pos[0] * 100, e_pos[1] * 100))
            
        # Draw Pieces
        for i, p in enumerate(self.white_pieces):
            p.draw(self.screen)
            if self.turn_step < 2 and self.selection == i:
                pygame.draw.rect(self.screen, 'red', 
                                 [p.position[0] * 100 + 1, p.position[1] * 100 + 1, 100, 100], 2)
        
        for i, p in enumerate(self.black_pieces):
            p.draw(self.screen)
            if self.turn_step >= 2 and self.selection == i:
                pygame.draw.rect(self.screen, 'blue', 
                                 [p.position[0] * 100 + 1, p.position[1] * 100 + 1, 100, 100], 2)

        self.draw_valid()
        self.draw_captured()
        self.draw_check()
        
        # Draw Undo Button Help Text
        self.screen.blit(self.font.render('Press [U] to Undo Move', True, 'white'), (825, 750))
        
        # Draw Move History Logic
        self.draw_move_history()
        
        # Draw Clocks
        self.draw_clocks()
        
        if self.game_over:
            self.draw_game_over()
            
    def draw_valid(self):
        color = 'red' if self.turn_step < 2 else 'blue'
        for move in self.valid_moves:
            pygame.draw.circle(self.screen, color, 
                               (move[0] * 100 + 50, move[1] * 100 + 50), 5)
                               
    def draw_captured(self):
        # captured_pieces are strings in original code? 
        # Yes: captured_pieces_white.append(black_pieces[black_piece]) -> black_pieces was list of strings.
        # Here self.black_pieces is list of Objects.
        # But I need to store them. I should modify capture logic to store the Piece Object or just name.
        # Let's store Object to keep access to image.
        
        for i, piece_obj in enumerate(self.captured_pieces_white):
            # piece_obj is a Piece object
            self.screen.blit(piece_obj.small_image, (825, 5 + 50 * i))
            
        for i, piece_obj in enumerate(self.captured_pieces_black):
            self.screen.blit(piece_obj.small_image, (925, 5 + 50 * i))

    def draw_check(self):
        # Visualize check
        if self.turn_step < 2: # White turn
            kings = [p for p in self.white_pieces if p.name == 'king']
            if kings:
                king_pos = kings[0].position
                # check if king_pos in black_options
                in_check = any(king_pos in moves for moves in self.black_options)
                if in_check and self.counter < 15:
                    pygame.draw.rect(self.screen, 'dark red', 
                                     [king_pos[0] * 100 + 1, king_pos[1] * 100 + 1, 100, 100], 5)
        else:
            kings = [p for p in self.black_pieces if p.name == 'king']
            if kings:
                king_pos = kings[0].position
                in_check = any(king_pos in moves for moves in self.white_options)
                if in_check and self.counter < 15:
                    pygame.draw.rect(self.screen, 'dark blue', 
                                     [king_pos[0] * 100 + 1, king_pos[1] * 100 + 1, 100, 100], 5)

    def draw_move_history(self):
        # Background for history log using premium theme
        history_rect = pygame.Rect(810, 200, 180, 520)
        pygame.draw.rect(self.screen, (30, 32, 40), history_rect, border_radius=8)
        pygame.draw.rect(self.screen, (80, 85, 95), history_rect, 2, border_radius=8)
        
        self.screen.blit(self.font.render('Move History', True, 'white'), (835, 215))
        pygame.draw.line(self.screen, (80, 85, 95), (810, 245), (990, 245), 2)
        
        # Show last 22 moves cleanly
        log_slice = self.move_log[-22:] if len(self.move_log) > 22 else self.move_log
        
        for i, move_text in enumerate(log_slice):
            y_pos = 255 + (i * 20)
            color = (200, 200, 205) if i % 2 == 0 else (160, 160, 170)
            
            # Format numbers (1. e4 e5) 
            # We track each half-move, so index 0 = white 1, index 1 = black 1
            full_move_num = (len(self.move_log) - len(log_slice) + i) // 2 + 1
            if (len(self.move_log) - len(log_slice) + i) % 2 == 0:
                display_text = f"{full_move_num}. {move_text}"
                self.screen.blit(self.font.render(display_text, True, color), (820, y_pos))
            else:
                display_text = move_text
                # offset black moves to right column
                self.screen.blit(self.font.render(display_text, True, color), (915, y_pos - 20))

    def format_time(self, ms):
        if ms == float('inf'): return "---"
        if ms <= 0: return "0:00"
        s = ms // 1000
        m, s = divmod(s, 60)
        return f"{int(m)}:{int(s):02d}"

    def draw_clocks(self):
        if self.time_control == 'untimed':
            return
            
        color_w = 'gray' if self.turn_step >= 2 else 'white'
        color_b = 'white' if self.turn_step >= 2 else 'gray'
        
        # Timers on right panel
        border_b = (255, 212, 59) if self.turn_step >= 2 else (60, 64, 72)
        pygame.draw.rect(self.screen, (30, 32, 40), [810, 20, 180, 60], border_radius=8)
        pygame.draw.rect(self.screen, border_b, [810, 20, 180, 60], 2, border_radius=8)
        self.screen.blit(self.medium_font.render(self.format_time(self.black_time), True, color_b), (825, 30))
        
        border_w = (255, 212, 59) if self.turn_step < 2 else (60, 64, 72)
        pygame.draw.rect(self.screen, (30, 32, 40), [810, 110, 180, 60], border_radius=8)
        pygame.draw.rect(self.screen, border_w, [810, 110, 180, 60], 2, border_radius=8)
        self.screen.blit(self.medium_font.render(self.format_time(self.white_time), True, color_w), (825, 120))

    def draw_game_over(self):
        # Create translucent overlay
        overlay = pygame.Surface((1000, 900), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0,0))
        
        # Modal
        pygame.draw.rect(self.screen, (25, 27, 36), [250, 300, 500, 200], border_radius=15)
        pygame.draw.rect(self.screen, (255, 212, 59), [250, 300, 500, 200], 3, border_radius=15)
        
        if self.winner == 'draw':
             text = 'Stalemate! Draw!'
        else:
             text = f'{self.winner.upper()} WINS THE GAME!'
        
        self.screen.blit(self.big_font.render(text, True, 'white'), (280, 330))
        self.screen.blit(self.font.render(f'Press ENTER to Restart   |   Press ESC to Exit', True, (200, 200, 205)), (285, 420))

    def is_king_in_check(self, pieces, turn):
        # pieces argument seems unused in original logic?
        # definition: def is_king_in_check(my_pieces, my_locations, turn):
        # But here I can just use self.
        
        # Need to simulate if new state puts king in check OR just check current state?
        # The logic passed 'tmp_locations' in defend_check.
        
        # NOTE: This implementation is tricky with OOP because objects store state.
        # I cannot easily pass 'simulated locations' without cloning or modifying objects temporarily.
        pass
        
    def check_simulated_check(self, color, pieces_list, index_moved, new_pos):
        # Simulate a move to see if King is in check
        # color: whose king to check
        # pieces_list: list of Piece objects for that color
        # index_moved: index of piece moved
        # new_pos: where it moved
        
        # 1. Get Simulated Locations
        locs = [p.position for p in pieces_list]
        locs[index_moved] = new_pos
        
        # 2. Find King Position
        king_pos = None
        for i, p in enumerate(pieces_list):
            if p.name == 'king':
                if i == index_moved: king_pos = new_pos
                else: king_pos = p.position
                break
        
        # 3. Check if any enemy can attack 'king_pos' given 'locs' occupancy
        # We need enemy moves. Enemy moves depend on occupancy.
        # Occupancy = locs (friends) + enemy_current_locs (enemies)
        # BUT: capturing logic? If I move to captured square, enemy is gone.
        
        # This Simulation is needed for `defend_check`.
        pass
        
    def defend_check(self, pieces, options, color):
        # Need to filter 'options' (list of valid moves for each piece)
        # "pieces" is the list of objects
        
        safe_options = []
        for i, p in enumerate(pieces):
            piece_safe_moves = []
            for move in options[i]:
                # Simulate move:
                # 1. Store original
                original_pos = p.position
                captured_piece = None
                
                # We need to know if we captured someone to remove them from occupancy
                enemy_pieces = self.black_pieces if color == 'white' else self.white_pieces
                
                # Find if capture happens
                captured_index = -1
                for ei, ep in enumerate(enemy_pieces):
                    if ep.position == move:
                        captured_index = ei
                        break
                
                # Apply move
                p.position = move
                # If capture, temporarily remove enemy
                temp_enemy = None
                if captured_index != -1:
                    temp_enemy = enemy_pieces.pop(captured_index)
                
                # Check if King is attacked
                # We need to re-calculate enemy moves given new board state
                w_locs = self.white_locations
                b_locs = self.black_locations
                
                # If checking white king safety:
                if color == 'white':
                    # Check black moves
                    enemy_moves = self.check_options(self.black_pieces, b_locs, 'black') # recursive?
                    # wait check_options calls get_valid_moves which calls internal logic.
                    
                    king_pos = [wp.position for wp in self.white_pieces if wp.name == 'king'][0]
                    if not any(king_pos in m_list for m_list in enemy_moves):
                         piece_safe_moves.append(move)
                else:
                    enemy_moves = self.check_options(self.white_pieces, w_locs, 'white')
                    king_pos = [bp.position for bp in self.black_pieces if bp.name == 'king'][0]
                    if not any(king_pos in m_list for m_list in enemy_moves):
                         piece_safe_moves.append(move)
                         
                # Restore state
                p.position = original_pos
                if temp_enemy:
                    if captured_index <= len(enemy_pieces):
                        enemy_pieces.insert(captured_index, temp_enemy)
                    else:
                        enemy_pieces.append(temp_enemy)
                        
            safe_options.append(piece_safe_moves)
        return safe_options

    async def run(self):
        import asyncio
        run = True
        self.last_tick = pygame.time.get_ticks()
        
        while run:
            self.timer.tick(FPS)
            
            # --- Timer Logic ---
            current_tick = pygame.time.get_ticks()
            delta_time = current_tick - self.last_tick
            self.last_tick = current_tick
            
            if not self.game_over and self.time_control != 'untimed':
                if self.turn_step <= 1:
                    self.white_time -= delta_time
                    if self.white_time <= 0:
                        self.white_time = 0
                        self.winner = 'black (on time)'
                        self.game_over = True
                else:
                    self.black_time -= delta_time
                    if self.black_time <= 0:
                        self.black_time = 0
                        self.winner = 'white (on time)'
                        self.game_over = True
            
            if self.counter < 30: self.counter += 1
            else: self.counter = 0
            
            self.draw_game()
            await asyncio.sleep(0)  # Yield control for browser
            
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u and not self.game_over:
                        self.undo_move()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                    x_coord = event.pos[0] // 100
                    y_coord = event.pos[1] // 100
                    click_coords = (x_coord, y_coord)
                    
                    if self.turn_step <= 1:
                        # White Turn
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            self.winner = 'black'
                            
                        # Select White Piece
                        if click_coords in self.white_locations:
                            # Index from list
                            for i, p in enumerate(self.white_pieces):
                                if p.position == click_coords:
                                    self.selection = i
                                    if self.turn_step == 0: self.turn_step = 1
                                    break
                                    
                        # Move selected piece
                        if click_coords in self.valid_moves and self.selection != 100:
                            # Save state before moving
                            self.save_state()
                            
                            # Move
                            selected_piece = self.white_pieces[self.selection]
                            start_pos = selected_piece.position
                            selected_piece.position = click_coords
                            
                            is_capture = False
                            # Capture
                            if click_coords in self.black_locations:
                                is_capture = True
                                for i, bp in enumerate(self.black_pieces):
                                    if bp.position == click_coords:
                                        self.captured_pieces_white.append(bp)
                                        if bp.name == 'king': self.winner = 'white'
                                        self.black_pieces.pop(i)
                                        break
                            
                            self.check_promotion(selected_piece, click_coords)
                            
                            notation = self.get_algebraic(selected_piece.name, start_pos, click_coords, is_capture)
                            self.move_log.append(notation)
                            self.last_move = (start_pos, click_coords)
                            
                            # Update Turns
                            self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                            self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                            self.turn_step = 2
                            self.selection = 100
                            self.valid_moves = []
                            
                            # Check Defend
                            self.black_options = self.defend_check(self.black_pieces, self.black_options, 'black')
                            
                    elif self.turn_step > 1:
                        # Black Turn
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            self.winner = 'white'
                        
                        if click_coords in self.black_locations:
                             for i, p in enumerate(self.black_pieces):
                                if p.position == click_coords:
                                    self.selection = i
                                    if self.turn_step == 2: self.turn_step = 3
                                    break
                        
                        if click_coords in self.valid_moves and self.selection != 100:
                            # Save state before moving
                            self.save_state()

                            selected_piece = self.black_pieces[self.selection]
                            start_pos = selected_piece.position
                            selected_piece.position = click_coords
                            
                            is_capture = False
                            if click_coords in self.white_locations:
                                is_capture = True
                                for i, wp in enumerate(self.white_pieces):
                                    if wp.position == click_coords:
                                        self.captured_pieces_black.append(wp)
                                        if wp.name == 'king': self.winner = 'black'
                                        self.white_pieces.pop(i)
                                        break
                                        
                            self.check_promotion(selected_piece, click_coords)
                             
                            notation = self.get_algebraic(selected_piece.name, start_pos, click_coords, is_capture)
                            self.move_log.append(notation)
                            self.last_move = (start_pos, click_coords)
                                        
                            self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                            self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                            self.turn_step = 0
                            self.selection = 100
                            self.valid_moves = []
                            
                            self.white_options = self.defend_check(self.white_pieces, self.white_options, 'white')
                            
            # --- AI Move Handling ---
            if not self.game_over and self.play_vs_ai and self.turn_step >= 2:
                # Black's Turn and AI is active
                game_state = {
                    'black_options': self.black_options,
                    'black_pieces': self.black_pieces,
                    'white_pieces': self.white_pieces
                }
                
                best_move = self.bot.get_best_move(game_state)
                
                if best_move:
                    # Execute AI Move
                    piece_idx = best_move['piece_idx']
                    target_pos = best_move['end_pos']
                    
                    selected_piece = self.black_pieces[piece_idx]
                    start_pos = selected_piece.position
                    selected_piece.position = target_pos
                    
                    is_capture = False
                    # Capture Logic
                    if target_pos in self.white_locations:
                        is_capture = True
                        for i, wp in enumerate(self.white_pieces):
                            if wp.position == target_pos:
                                self.captured_pieces_black.append(wp)
                                if wp.name == 'king': self.winner = 'black'
                                self.white_pieces.pop(i)
                                break
                    
                    self.check_promotion(selected_piece, target_pos)
                    
                    notation = self.get_algebraic(selected_piece.name, start_pos, target_pos, is_capture)
                    self.move_log.append(notation)
                    self.last_move = (start_pos, target_pos)
                    
                    # Update State
                    self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                    self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
                    self.turn_step = 0
                    self.white_options = self.defend_check(self.white_pieces, self.white_options, 'white')
                else:
                    # AI has no moves (Checkmate or Stalemate)
                    # Handled by existing checkmate trigger below
                    pass

            # Game Over Reset
            if event.type == pygame.KEYDOWN and self.game_over:
                    if event.key == pygame.K_RETURN:
                         self.init_pieces()
                         self.turn_step = 0
                         self.game_over = False
                         self.winner = ''
                         self.captured_pieces_white = []
                         self.captured_pieces_black = []
                         self.selection = 100
                         self.valid_moves = []
                         self.last_move = None
                         self.history = []
                         self.move_log = []
                         self.init_clocks()
                         
                         self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
                         self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')

                    if event.key == pygame.K_ESCAPE:
                        run = False

            # Update Valid Moves for drawing
            if self.selection != 100:
                self.valid_moves = self.check_valid_moves()
            
            # Checkmate Detection
            if self.winner != '':
                self.game_over = True
            
            pygame.display.flip()
        
        pygame.quit()
        
    def save_state(self):
        import copy
        # Deep clone piece configurations to restore later
        # Pygame surfaces cannot be pickled/deepcopied easily, so we recreate the state
        # instead of full object deepcopies, we just store properties needed to reconstruct.
        state = {
            'white': [(p.name, p.position) for p in self.white_pieces],
            'black': [(p.name, p.position) for p in self.black_pieces],
            'cap_white': [(p.name, p.color) for p in self.captured_pieces_white],
            'cap_black': [(p.name, p.color) for p in self.captured_pieces_black],
            'turn': self.turn_step,
            'w_time': self.white_time,
            'b_time': self.black_time,
            'last_move': self.last_move
        }
        self.history.append(state)
        
    def get_algebraic(self, piece_name, start_pos, end_pos, is_capture):
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        rows = ['8', '7', '6', '5', '4', '3', '2', '1']
        
        start_sq = cols[start_pos[0]] + rows[start_pos[1]]
        end_sq = cols[end_pos[0]] + rows[end_pos[1]]
        
        piece_char = ''
        if piece_name == 'knight': piece_char = 'N'
        elif piece_name != 'pawn': piece_char = piece_name[0].upper()
        
        cap = 'x' if is_capture else ''
        
        if piece_name == 'pawn' and is_capture:
            return f"{start_sq[0]}{cap}{end_sq}"
        
        return f"{piece_char}{cap}{end_sq}"
        
    def undo_move(self):
        if not self.history:
             return
             
        # If playing vs AI, pop once for AI move, once for player move
        state = self.history.pop()
        
        if self.move_log:
            self.move_log.pop()
        
        # reconstruct pieces
        self.white_pieces = []
        for name, pos in state['white']:
            self.white_pieces.append(self.create_piece('white', name, pos))
            
        self.black_pieces = []
        for name, pos in state['black']:
            self.black_pieces.append(self.create_piece('black', name, pos))
            
        self.captured_pieces_white = []
        for name, color in state['cap_white']:
            self.captured_pieces_white.append(self.create_piece(color, name, (-1,-1)))
            
        self.captured_pieces_black = []
        for name, color in state['cap_black']:
            self.captured_pieces_black.append(self.create_piece(color, name, (-1,-1)))
            
        self.turn_step = state['turn']
        self.white_time = state['w_time']
        self.black_time = state['b_time']
        self.last_move = state.get('last_move', None)
        self.selection = 100
        self.valid_moves = []
        self.winner = ''
        self.game_over = False
        
        self.black_options = self.check_options(self.black_pieces, self.black_locations, 'black')
        self.white_options = self.check_options(self.white_pieces, self.white_locations, 'white')
        
        if self.turn_step == 0:
            self.white_options = self.defend_check(self.white_pieces, self.white_options, 'white')
        else:
            self.black_options = self.defend_check(self.black_pieces, self.black_options, 'black')
                
    def check_promotion(self, piece, clicked_coords):
        if piece.name == 'pawn':
             if (piece.color == 'white' and piece.position[1] == 7) or \
                (piece.color == 'black' and piece.position[1] == 0):
                self.promote_pawn(piece)
                
    def promote_pawn(self, piece):
        from promotion import PromotionHandler
        
        handler = PromotionHandler(self.screen)
        target_type = handler.select_piece()
                    
        if target_type:
            key = f"{piece.color}_{target_type}"
            img = self.images[key]
            small_img = self.images[f"{key}_small"]
            
            new_piece = None
            if target_type == 'queen': new_piece = Queen(piece.color, piece.position, img, small_img)
            elif target_type == 'rook': new_piece = Rook(piece.color, piece.position, img, small_img)
            elif target_type == 'bishop': new_piece = Bishop(piece.color, piece.position, img, small_img)
            elif target_type == 'knight': new_piece = Knight(piece.color, piece.position, img, small_img)
            
            if new_piece:
                if piece.color == 'white':
                    index = self.white_pieces.index(piece)
                    self.white_pieces[index] = new_piece
                else:
                    index = self.black_pieces.index(piece)
                    self.black_pieces[index] = new_piece
            
            # Optimization: only check checkmate if game not over?
            # Original code checkmate logic:
            if not self.game_over:
                 if self.turn_step < 2: # White to move
                      # If white is in check
                      king_w = [p for p in self.white_pieces if p.name == 'king'][0]
                      # Check if ANY black option targets king
                      in_check = any(king_w.position in moves for moves in self.black_options)
                      if in_check:
                          # If white has NO options left (after defend_check applied)
                           if not any(self.white_options):
                               self.winner = 'black'
                      else:
                           # Stalemate check
                           if not any(self.white_options):
                               self.winner = 'draw'
                 else:
                       king_b = [p for p in self.black_pieces if p.name == 'king'][0]
                       in_check = any(king_b.position in moves for moves in self.white_options)
                       if in_check:
                           if not any(self.black_options):
                               self.winner = 'white'
                       else:
                           # Stalemate check
                           if not any(self.black_options):
                               self.winner = 'draw'


