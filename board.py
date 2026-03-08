
import pygame
from constants import WIDTH, HEIGHT

class Board:
    def __init__(self):
        pass

    def draw(self, screen):
        # Modern Chess Colors
        light_color = (235, 236, 208) # Cream
        dark_color = (115, 149, 82)   # Green
        
        # Fill base with dark color
        pygame.draw.rect(screen, dark_color, [0, 0, 800, 800])
        
        # Draw light squares Over it
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 == 0:
                pygame.draw.rect(screen, light_color, [
                    600 - (column * 200), row * 100, 100, 100])
            else:
                pygame.draw.rect(screen, light_color, [
                    700 - (column * 200), row * 100, 100, 100])
        
        # Draw panels and borders with premium dark theme
        bg_panel = (40, 42, 48)
        border_panel = (60, 64, 72)
        
        pygame.draw.rect(screen, bg_panel, [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, border_panel, [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, border_panel, [800, 0, 200, HEIGHT], 5)
        
        # Draw grid lines
        for i in range(9):
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

    def draw_status_text(self, screen, font, turn_step, medium_font):
        status_text = ['White Turn', 'White Select Destination',
                       'Black Turn', 'Black Select Destination']
        screen.blit(font.render(status_text[turn_step], True, 'white'), (20, 840))
        
        # Draw Forfeit button with modern style
        pygame.draw.rect(screen, (180, 50, 50), [825, 825, 150, 50], border_radius=8)
        screen.blit(font.render('FORFEIT', True, 'white'), (860, 840))
