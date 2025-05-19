import pygame
from os.path import join

class TitleScreen:
    def __init__(self, display_surface, intro_music):
        self.display_surface = display_surface
        self.intro_music = intro_music
        self.title_image = pygame.image.load(join('..', 'graphics', 'ui', 'title_screen.png')).convert()
        self.title_image = pygame.transform.scale(self.title_image, self.display_surface.get_size())

        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'PressStart2P-Regular.ttf'), 20)
        self.font_big = pygame.font.Font(join('..', 'graphics', 'ui', 'PressStart2P-Regular.ttf'), 22)
        self.running = True
        self.choice = None
        self.show_controls = False

    def display_text(self, text, y_offset):
        base_x = self.display_surface.get_width() // 2
        base_y = self.display_surface.get_height() // 2 + y_offset
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(base_x, base_y))

        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            shadow_surface = self.font.render(text, True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect(center=(base_x + dx, base_y + dy))
            self.display_surface.blit(shadow_surface, shadow_rect)

        self.display_surface.blit(text_surface, text_rect)

    def fade_message(self, lines):
        clock = pygame.time.Clock()
        overlay = pygame.Surface(self.display_surface.get_size())
        overlay.fill((0, 0, 0))
        alpha = 255
        fade_out = False
        duration = 3
        timer = 0

        while True:
            dt = clock.tick(60) / 1000
            timer += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.display_surface.fill((0, 0, 0))
            for i, line in enumerate(lines):
                text_surface = self.font_big.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.display_surface.get_width() // 2, 200 + i * 50))
                self.display_surface.blit(text_surface, text_rect)

            if timer > duration:
                fade_out = True
                alpha += 5
                if alpha >= 255:
                    break
            elif fade_out:
                continue
            else:
                alpha = max(0, alpha - 5)

            overlay.set_alpha(alpha)
            self.display_surface.blit(overlay, (0, 0))
            pygame.display.update()

    def run_intro_sequence(self):
        self.intro_music.play(-1)
        intro_texts = [
            ["Durante siglos, un enemigo invisible",
            "ha habitado entre nosotros...",
             "oculto en pan, galletas y pizzas."],

            ["Pero una heroína ha despertado.",
             "No busca venganza… busca justicia sin gluten."],

            ["En un mundo lleno de trampas invisibles,",
             "su misión es clara: sobrevivir, aprender y vencer."]
        ]

        for lines in intro_texts:
            self.fade_message(lines)

        self.intro_music.stop()



    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if self.show_controls and event.key == pygame.K_ESCAPE:
                        self.show_controls = False
                    elif not self.show_controls:
                        if event.key == pygame.K_SPACE:
                            self.display_surface.fill((0, 0, 0))
                            pygame.display.update()
                            self.run_intro_sequence()
                            self.choice = "start"
                            self.running = False
                            return
                        elif event.key == pygame.K_c:
                            self.show_controls = True
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()

            self.display_surface.blit(self.title_image, (0, 0))

            if self.show_controls:
                self.display_text('Pulsa "-> DERECHA" para ir a la derecha', -60)
                self.display_text('Pulsa "<- IZQUIERDA" para ir a la izquierda', -20)
                self.display_text('Pulsa "X" para atacar', 20)
                self.display_text('Pulsa "ESPACIO" para saltar', 60)
                self.display_text('Pulsa "ABAJO" para bajar de una plataforma', 100)
                self.display_text('Pulsa "ESC" para pausar la partida', 140)
                self.display_text('Pulsa ESC de nuevo para volver', 200)
            else:
                self.display_text('Pulsa ESPACIO para comenzar a jugar', 60)
                self.display_text('Pulsa C para ver los controles', 100)
                self.display_text('Pulsa ESC para salir del juego', 140)

            pygame.display.update()


class PauseScreen:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.overlay = pygame.Surface(display_surface.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))  # Negro con transparencia

        self.font_big = pygame.font.Font(join('..', 'graphics', 'ui', 'PressStart2P-Regular.ttf'), 40)
        self.font_small = pygame.font.Font(join('..', 'graphics', 'ui', 'PressStart2P-Regular.ttf'), 20)
        self.active = True

    def draw_text(self, text, y_offset, font):
        base_x = self.display_surface.get_width() // 2
        base_y = self.display_surface.get_height() // 2 + y_offset
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(base_x, base_y))

        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            shadow_surface = font.render(text, True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect(center=(base_x + dx, base_y + dy))
            self.display_surface.blit(shadow_surface, shadow_rect)

        self.display_surface.blit(text_surface, text_rect)

    def run(self):
        self.display_surface.blit(self.overlay, (0, 0))
        self.draw_text("PAUSA", -30, self.font_big)
        self.draw_text("Pulsa ESC para volver al juego", 40, self.font_small)
        pygame.display.update()

        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.active = False


class CreditScreen:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.image = pygame.image.load(join('..', 'graphics', 'ui', 'title_credit.png')).convert()
        self.image = pygame.transform.scale(self.image, self.display_surface.get_size())
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'PressStart2P-Regular.ttf'), 16)

    def run(self):
        self.display_surface.blit(self.image, (0, 0))

        text = self.font.render("Pulsa cualquier tecla para continuar", True, (255, 255, 255))
        rect = text.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() - 50))
        self.display_surface.blit(text, rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    return




