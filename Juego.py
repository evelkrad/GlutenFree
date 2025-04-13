import pygame
import random

pygame.init()

# =========================
# CONFIGURACIÓN DE VENTANA
# =========================
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de plataformas con menú de pausa")

clock = pygame.time.Clock()

# =========================
# FUENTE PARA MENSAJES
# =========================
font = pygame.font.SysFont("Arial", 36)

# =========================
# CARGA DE IMÁGENES
# =========================
enemigo_original = pygame.image.load("enemigo.png").convert_alpha()
img_plataforma_base = pygame.image.load("sprites/plataforma_base.png").convert_alpha()

# Cargar una imagen de fondo
fondo = pygame.image.load("fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

corazon_lleno = pygame.transform.scale(
    pygame.image.load("sprites/corazon_lleno.png").convert_alpha(), (48, 48)
)
corazon_vacio = pygame.transform.scale(
    pygame.image.load("sprites/corazon_vacio.png").convert_alpha(), (48, 48)
)

# Ajustar tamaños
nuevo_ancho = 50
nuevo_alto = 75

#Personaje
idle_image = pygame.transform.scale(pygame.image.load("sprites/idle.png").convert_alpha(), (nuevo_ancho, nuevo_alto))
walk_frames = [
    pygame.transform.scale(pygame.image.load("sprites/walk.png").convert_alpha(), (nuevo_ancho, nuevo_alto)),
    pygame.transform.scale(pygame.image.load("sprites/walk1.png").convert_alpha(), (nuevo_ancho, nuevo_alto))
]
jump_image = pygame.transform.scale(pygame.image.load("sprites/jump.png").convert_alpha(), (nuevo_ancho, nuevo_alto))

enemigo_ancho = 40
enemigo_alto = 50
enemigo_original = pygame.transform.scale(enemigo_original, (enemigo_ancho, enemigo_alto))

# Puntuacion y vidas

puntuacion = 0
vidas = 3 

# Enemigos:
enemigo_izquierda = enemigo_original
enemigo_derecha = pygame.transform.flip(enemigo_original, True, False)

# =========================
# CLASE ENEMIGO
# =========================
class Enemigo:
    def __init__(self, x, y, plataforma):
        self.x = x
        self.y = y
        self.velocidad = 2
        self.direccion = 1  
        self.plataforma = plataforma
        self.vivo = True
        self.puntuado = False  # <-- NUEVA LÍNEA
        self.imagen = enemigo_derecha if self.direccion == 1 else enemigo_izquierda
    def mover(self):
        if not self.vivo:
            return
        self.x += self.velocidad * self.direccion * (clock.get_time() / 16.67)

        # Comprobar bordes de la plataforma
        if self.x < self.plataforma.left:
            self.x = self.plataforma.left
            self.direccion = 1
            self.imagen = enemigo_derecha
        elif self.x + enemigo_ancho > self.plataforma.right:
            self.x = self.plataforma.right - enemigo_ancho
            self.direccion = -1
            self.imagen = enemigo_izquierda

    def colision_con_personaje(self, player_rect, vel_y):
        if not self.vivo:
            return None
        enemigo_rect = pygame.Rect(self.x, self.y, enemigo_ancho, enemigo_alto)

        if enemigo_rect.colliderect(player_rect):
            if (player_rect.bottom - vel_y) <= self.y + 5 and vel_y > 0:
                self.vivo = False 
            else:
                return "game_over"

        return None

    def actualizar(self):
        if self.vivo:
            self.mover()
        else:
            self.y += 5

    def dibujar(self, offset_x):
        if self.vivo or self.y < ALTO:
            pantalla.blit(self.imagen, (self.x - offset_x, self.y))

# =========================
# GENERACIÓN DE NIVEL
# =========================
def generar_nivel():
    plataformas = []
    enemigos = []

    # Primera plataforma en el suelo
    x_actual = 50
    ground_y = ALTO // 2 + 60
    PLATURA_ALTURA = 40
    first_plat = pygame.Rect(x_actual, ground_y, 300, PLATURA_ALTURA)
    plataforma_inicial = first_plat


    plataformas.append((first_plat, (100, 50, 0)))
    x_actual = first_plat.right
    prev_y = ground_y

    # Ajustar para controlar cuánto pueden subir/bajar las plataformas
    delta_up = 50
    delta_down = 50
    MIN_PLAT_Y = 150
    MAX_PLAT_Y = ALTO // 2 + 100


    # Generar 24 plataformas más
    for i in range(1, 25):
        gap = random.randint(100, 200)
        x_new = x_actual + gap
        width = random.randint(100, 300)

        min_y = max(MIN_PLAT_Y, prev_y - delta_up)
        max_y = min(MAX_PLAT_Y, prev_y + delta_down)
        new_y = random.randint(min_y, max_y)

        plat = pygame.Rect(x_new, new_y, width, PLATURA_ALTURA)
        plataformas.append((plat, (100, 50, 0)))

        x_actual = plat.right
        prev_y = new_y

        # Un enemigo cada 4 plataformas
        if i % 4 == 0:
            enemigo_x = x_new + (width // 2) - (enemigo_ancho // 2)
            enemigo_y = new_y - enemigo_alto
            enemigos.append(Enemigo(enemigo_x, enemigo_y, plat))

    # Plataforma final verde
    gap = random.randint(100, 200)
    x_new = x_actual + gap
    width = random.randint(100, 300)

    min_y = max(MIN_PLAT_Y, prev_y - delta_up)
    max_y = min(MAX_PLAT_Y, prev_y + delta_down)
    new_y = random.randint(min_y, max_y)

    plat = pygame.Rect(x_new, new_y, width, PLATURA_ALTURA)
    plataformas.append((plat, (0, 255, 0)))

    return plataformas, enemigos, plataforma_inicial


# =========================
# REINICIAR NIVEL
# =========================
def reiniciar_nivel():
    global player_x, player_y, velocidad_x, velocidad_y, camera_offset_x, state, plataformas, enemigos, plataforma_inicial, puntuacion, vidas, mensaje_final
    puntuacion = 0
    vidas = 3
    mensaje_final = False
    velocidad_x = 0
    velocidad_y = 0
    camera_offset_x = 0

    plataformas, enemigos, plataforma_inicial = generar_nivel() 

    player_x = plataforma_inicial.left + 40                   
    player_y = plataforma_inicial.top - nuevo_alto

    state = "jugando"
    return plataformas, enemigos


# =========================
# FUNCIONES PARA MENÚS
# =========================
def dibujar_menu_inicial():
    pantalla.blit(fondo, (0, 0))

    titulo = font.render("MENÚ INICIAL", True, (255, 255, 255))
    opcion_jugar = font.render("Pulsa J para JUGAR", True, (255, 255, 0))
    opcion_salir = font.render("Pulsa S para SALIR", True, (255, 255, 0))
    opcion_controles = font.render("Pulsa C para CONTROLES", True, (255, 255, 0))
    info_pausa = font.render("Pulsa ESC para PAUSA (en juego)", True, (200, 200, 200))


    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
    pantalla.blit(opcion_jugar, (ANCHO//2 - opcion_jugar.get_width()//2, 200))
    pantalla.blit(opcion_salir, (ANCHO//2 - opcion_salir.get_width()//2, 250))
    pantalla.blit(opcion_controles, (ANCHO//2 - opcion_controles.get_width()//2, 300))
    pantalla.blit(info_pausa, (ANCHO//2 - info_pausa.get_width()//2, 360))

def dibujar_menu_pausa():
    pantalla.blit(fondo, (0, 0))
    
    for plat, color in plataformas:
        plataforma_img = pygame.transform.scale(img_plataforma_base, (plat.width, plat.height))
        pantalla.blit(plataforma_img, (plat.x - camera_offset_x, plat.y))

    for enemigo in enemigos:
        enemigo.dibujar(camera_offset_x)
    pantalla.blit(idle_image, (player_x - camera_offset_x, player_y))

    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    pantalla.blit(overlay, (0, 0))

    titulo = font.render("PAUSA", True, (255, 255, 255))
    reanudar = font.render("Pulsa R para REANUDAR", True, (255, 255, 0))
    controles = font.render("Pulsa C para CONTROLES", True, (255, 255, 0))
    salir = font.render("Pulsa S para SALIR", True, (255, 255, 0))

    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))
    pantalla.blit(reanudar, (ANCHO//2 - reanudar.get_width()//2, 200))
    pantalla.blit(controles, (ANCHO//2 - controles.get_width()//2, 250))
    pantalla.blit(salir, (ANCHO//2 - salir.get_width()//2, 300))

def dibujar_controles():
    # Dibujar el fondo del juego actual
    pantalla.blit(fondo, (0, 0))

    # Dibujar plataformas y enemigos (estado congelado)
    for plat, color in plataformas:
        plataforma_img = pygame.transform.scale(img_plataforma_base, (plat.width, plat.height))
        pantalla.blit(plataforma_img, (plat.x - camera_offset_x, plat.y))

    for enemigo in enemigos:
        enemigo.dibujar(camera_offset_x)

    # Dibujar personaje congelado
    pantalla.blit(idle_image, (player_x - camera_offset_x, player_y))

    # Superponer capa semitransparente
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Oscurecer para resaltar el texto
    pantalla.blit(overlay, (0, 0))

    # Dibujar texto del menú de controles
    titulo = font.render("CONTROLES", True, (255, 255, 255))
    texto1 = font.render("Flechas IZQ/DCHA para moverte", True, (255, 255, 0))
    texto2 = font.render("Espacio para saltar", True, (255, 255, 0))
    texto3 = font.render("ESC para pausar el juego", True, (255, 255, 0))
    texto4 = font.render("Pulsa ESC para volver al menú de pausa", True, (255, 255, 0))

    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 80))
    pantalla.blit(texto1, (ANCHO//2 - texto1.get_width()//2, 180))
    pantalla.blit(texto2, (ANCHO//2 - texto2.get_width()//2, 220))
    pantalla.blit(texto3, (ANCHO//2 - texto3.get_width()//2, 260))
    pantalla.blit(texto4, (ANCHO//2 - texto4.get_width()//2, 340))

# =========================
# VARIABLES GLOBALES
# =========================
player_x = 100
player_y = 400
velocidad_x = 0
velocidad_y = 0
direccion = "derecha"
gravedad = 0.5
salto = -13
en_suelo = False
camera_offset_x = 0
inmune = False
inmune_timer = 0
mensaje_vida = False
mensaje_final = False
mensaje_timer = 0


# Estados: "menu_inicial", "jugando", "pause", "controles", "game_over", "nivel_completado"
state = "menu_inicial"

plataformas = []
enemigos = []
frame_index = 0
frame_timer = 0

ejecutando = True
while ejecutando:
    clock.tick(60)

    # ========================
    # GESTIÓN DE EVENTOS
    # ========================
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if state == "menu_inicial":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_j:
                    plataformas, enemigos = reiniciar_nivel()
                    state = "jugando"
                elif evento.key == pygame.K_s:
                    ejecutando = False
                elif evento.key == pygame.K_c:
                    plataformas, enemigos = reiniciar_nivel()
                    state = "controles"

        elif state == "jugando":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                state = "pause"

        elif state == "pause":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    state = "jugando"
                elif evento.key == pygame.K_c:
                    state = "controles"
                elif evento.key == pygame.K_s:
                    ejecutando = False

        elif state == "controles":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                state = "pause"

        elif state in ["game_over", "nivel_completado"]:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                plataformas, enemigos = reiniciar_nivel()

    # ========================
    # LÓGICA DE CADA ESTADO
    # ========================
    if state == "jugando":
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            velocidad_x = -5
        elif teclas[pygame.K_RIGHT]:
            velocidad_x = 5
        else:
            velocidad_x = 0
        if velocidad_x < 0:
            direccion = "izquierda"
        elif velocidad_x > 0:
            direccion = "derecha"


        if teclas[pygame.K_SPACE] and en_suelo:
            velocidad_y = salto
            en_suelo = False

        velocidad_y += gravedad
        player_y += velocidad_y
        player_x += velocidad_x

        # Actualización de la cámara
        target_offset = player_x - (ANCHO // 2)
        smoothing = 0.1
        camera_offset_x += (target_offset - camera_offset_x) * smoothing

        player_rect = pygame.Rect(player_x, player_y, nuevo_ancho, nuevo_alto)

        en_suelo = False
        player_rect_inferior = pygame.Rect(player_x, player_y, nuevo_ancho, nuevo_alto + 5)


        for plat, color in plataformas:
            if player_rect_inferior.colliderect(plat):
                distancia_a_plataforma = player_rect.bottom - plat.top

                # Comprobar caida
                if velocidad_y >= 0 and 0 <= distancia_a_plataforma <= 20:
                    if color == (0, 255, 0):
                        state = "nivel_completado"
                    player_y = plat.top - nuevo_alto
                    velocidad_y = 0
                    en_suelo = True
                    break

    if player_y > ALTO:
        vidas -= 1

        if vidas <= 0:
            state = "game_over"
            mensaje_final = True
        else:
            inmune = True
            inmune_timer = pygame.time.get_ticks()
            mensaje_vida = True
            mensaje_timer = pygame.time.get_ticks()
            player_x = plataforma_inicial.left + 40
            player_y = plataforma_inicial.top - nuevo_alto

            velocidad_x, velocidad_y = 0, 0
            camera_offset_x = 0


    if state == "jugando":
        for enemigo in enemigos:
            resultado = enemigo.colision_con_personaje(player_rect, velocidad_y)
            if resultado == "game_over":
                vidas -= 1

                if vidas <= 0:
                    state = "game_over"
                    mensaje_final = True
                else:
                    inmune = True
                    inmune_timer = pygame.time.get_ticks()
                    mensaje_vida = True
                    mensaje_timer = pygame.time.get_ticks()
                    player_x = plataforma_inicial.left + 40
                    player_y = plataforma_inicial.top - nuevo_alto

                    velocidad_x, velocidad_y = 0, 0
                    camera_offset_x = 0
                break

                break
            elif resultado is None and not enemigo.vivo and not enemigo.puntuado:
                puntuacion += 10
                enemigo.puntuado = True


        for enemigo in enemigos:
            enemigo.actualizar()

    # ========================
    # DIBUJADO
    # ========================
    if state == "menu_inicial":
        dibujar_menu_inicial()

    elif state == "jugando":

        # Fondo estático
        pantalla.blit(fondo, (0, 0))
        
        # Dibujar plataformas
        for plat, color in plataformas:
            plataforma_img = pygame.transform.scale(img_plataforma_base, (plat.width, plat.height))
            pantalla.blit(plataforma_img, (plat.x - camera_offset_x, plat.y))

        # Dibujar enemigos
        for enemigo in enemigos:
            enemigo.dibujar(camera_offset_x)

        if not en_suelo:
            personaje_actual = jump_image
        elif velocidad_x != 0:
            frame_timer += 1
            if frame_timer >= 10:
                frame_index = (frame_index + 1) % len(walk_frames)
                frame_timer = 0
            personaje_actual = walk_frames[frame_index]
        else:
            personaje_actual = idle_image

        # Girar sprite si está mirando a la izquierda
        if direccion == "izquierda":
            personaje_actual = pygame.transform.flip(personaje_actual, True, False)

        # Mostrar personaje parpadeo
        mostrar_personaje = True
        if inmune:
            if (pygame.time.get_ticks() // 200) % 2 == 0:
                mostrar_personaje = False

        if mostrar_personaje:
            pantalla.blit(personaje_actual, (player_x - camera_offset_x, player_y))

        # Mostrar corazones en pantalla
        espaciado = 2
        for i in range(3):
            x = 20 + i * (48 + espaciado)
            if i < vidas:
                pantalla.blit(corazon_lleno, (x, 20))
            else:
                pantalla.blit(corazon_vacio, (x, 20))

        # Mostrar puntuación
        score_text = font.render(f"SCORE: {puntuacion}", True, (0, 0, 0))
        pantalla.blit(score_text, (ANCHO - score_text.get_width() - 20, 20))


    elif state == "pause":
        pantalla.blit(fondo, (0, 0))
        for plat, color in plataformas:
            plataforma_img = pygame.transform.scale(img_plataforma_base, (plat.width, plat.height))
            pantalla.blit(plataforma_img, (plat.x - camera_offset_x, plat.y))

        for enemigo in enemigos:
            enemigo.dibujar(camera_offset_x)
        dibujar_menu_pausa()

    elif state == "controles":
        dibujar_controles()

    elif state == "game_over":
        # Mostrar fondo del juego
        pantalla.blit(fondo, (0, 0))

        # Dibujar plataformas y enemigos como "congelados"
        for plat, color in plataformas:
            plataforma_img = pygame.transform.scale(img_plataforma_base, (plat.width, plat.height))
            pantalla.blit(plataforma_img, (plat.x - camera_offset_x, plat.y))


        for enemigo in enemigos:
            enemigo.dibujar(camera_offset_x)

        pantalla.blit(personaje_actual, (player_x - camera_offset_x, player_y))

        # Capa oscura
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        pantalla.blit(overlay, (0, 0))

        # Mensajes de GAME OVER
        texto1 = font.render("GAME OVER", True, (255, 50, 50))
        texto2 = font.render("Pulsa ENTER para reiniciar", True, (255, 50, 50))
        pantalla.blit(texto1, (ANCHO//2 - texto1.get_width()//2, ALTO//2 - 30))
        pantalla.blit(texto2, (ANCHO//2 - texto2.get_width()//2, ALTO//2 + 10))

        if mensaje_final:
            mensaje_extra = font.render("Te has quedado sin vidas", True, (255, 255, 255))
            pantalla.blit(mensaje_extra, (ANCHO//2 - mensaje_extra.get_width()//2, ALTO//2 + 60))



    elif state == "nivel_completado":
        pantalla.fill((135, 206, 235))
        texto1 = font.render("¡NIVEL COMPLETADO!", True, (0, 255, 0))
        texto2 = font.render("Pulsa ENTER para reiniciar", True, (0, 255, 0))
        pantalla.blit(texto1, (ANCHO//2 - texto1.get_width()//2, ALTO//2 - 30))
        pantalla.blit(texto2, (ANCHO//2 - texto2.get_width()//2, ALTO//2 + 10))

    if inmune and pygame.time.get_ticks() - inmune_timer > 2000:
        inmune = False

    if mensaje_vida and pygame.time.get_ticks() - mensaje_timer > 2000:
        mensaje_vida = False

    if mensaje_vida:
        mensaje = font.render("¡Has perdido una vida!", True, (255, 255, 0))
        pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, 60))

        

    pygame.display.update()

pygame.quit()
