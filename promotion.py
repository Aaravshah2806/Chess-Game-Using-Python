import pygame

class PromotionHandler:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def select_piece(self):
        # Draw Promotion Menu
        pygame.draw.rect(self.screen, 'dark gray', [0, 200, 800, 100])
        text = self.font.render('Promote to: Q-Queen, R-Rook, B-Bishop, K-Knight', True, 'black')
        self.screen.blit(text, (100, 240))
        pygame.display.flip()
        
        promoting = True
        while promoting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: return 'queen'
                    elif event.key == pygame.K_r: return 'rook'
                    elif event.key == pygame.K_b: return 'bishop'
                    elif event.key == pygame.K_k: return 'knight'
        return None
