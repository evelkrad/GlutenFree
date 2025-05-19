import pygame

class DeathTransition:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.overlay = pygame.Surface(display_surface.get_size())
        self.overlay.fill((0, 0, 0))
        self.alpha = 0
        self.finished = False
        self.duration = 3.0  # segundos
        self.timer = 0

    def run(self, dt):
        if self.finished:
            return True  # indica que ha terminado la transición

        self.timer += dt
        progress = min(self.timer / self.duration, 1)
        self.alpha = int(progress * 255)
        self.overlay.set_alpha(self.alpha)
        self.display_surface.blit(self.overlay, (0, 0))
        pygame.display.update()

        if progress >= 1:
            self.finished = True
            return True

        return False


