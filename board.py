
import pygame
from constants import WIDTH, HEIGHT

class Board:
    def __init__(self):
        pass

    def draw(self, screen):
        # Draw squares
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(screen, 'light grey', [
                    600 - (column * 200), row * 100, 100, 100])
            else:
                pygame.draw.rect(screen, 'light grey', [
                    700 - (column * 200), row * 100, 100, 100])
        
        # Draw panels and borders
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        
        # Draw grid lines
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

    def draw_status_text(self, screen, font, turn_step, medium_font):
        status_text = ['White: Select a Piece to Move !', 'White Select a Destination !',
                       'Black: Select a Piece to Move !', 'Black Select a Destination !']
        screen.blit(font.render(status_text[turn_step], True, 'black'), (20, 820))
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))
