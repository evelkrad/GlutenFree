import pygame
from os.path import join

class GameOver:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'PressStart2P-Regular.ttf'), 40)
        self.small_font = pygame.font.Font(join('..', 'graphics', 'ui', 'PressStart2P-Regular.ttf'), 20)
        self.alpha_surface = pygame.Surface(self.display_surface.get_size())
        self.alpha_surface.fill((0, 0, 0))
        self.alpha = 0
        self.fade_speed = 5
        self.finished = False

    def fade_to_black(self):
        if self.alpha < 255:
            self.alpha += self.fade_speed
            self.alpha_surface.set_alpha(self.alpha)
            self.display_surface.blit(self.alpha_surface, (0, 0))
        else:
            self.display_game_over_text()
            self.finished = True

    def display_game_over_text(self):
        # Texto principal "GAME OVER"
        text_surface = self.font.render('GAME OVER', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - 40))
        self.display_surface.blit(text_surface, text_rect)

        # Instrucciones en tamaño pequeño
        exit_surface = self.small_font.render('Pulsa "ESC" para salir', True, (255, 255, 255))
        exit_rect = exit_surface.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 + 20))
        self.display_surface.blit(exit_surface, exit_rect)

        restart_surface = self.small_font.render('Pulsa "ESPACIO" para reiniciar', True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 + 50))
        self.display_surface.blit(restart_surface, restart_rect)

    def run(self, events):
        if not self.finished:
            self.fade_to_black()
        else:
            self.display_game_over_text()
            for event in events:
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
                    elif event.key == pygame.K_SPACE:
                        return "restart"

