import pygame, random

# Inicialización
pygame.init()
ANCHO, ALTO, FPS = 600, 800, 60
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de la carretera")
clock = pygame.time.Clock()

COLORES = {
    "NEGRO": (0, 0, 0), "AMARILLO": (255, 255, 0), "ROJO": (255, 0, 0),
    "GRIS": (169, 169, 169), "AZUL": (0, 0, 255), "BLANCO": (255, 255, 255),
    "MARRON": (139, 69, 19)}

# Clases
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(COLORES["AMARILLO"])
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO - 50))
        self.vel = 5

    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.rect.move_ip(dx * self.vel, dy * self.vel)
        self.rect.clamp_ip(pantalla.get_rect())

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(COLORES["ROJO"])
        
        self.carril = random.choice(["arriba", "abajo"])
        self.rect = self.image.get_rect()
        self.vel = random.randint(5, 10)
        
        if self.carril == "arriba":
            self.rect.x = ANCHO  # entra desde la derecha
            self.rect.y = random.choice([250, 275])  # carril superior
            self.direccion = -1  # va hacia la izquierda
        else:
            self.rect.x = -40  # entra desde la izquierda
            self.rect.y = random.choice([425, 450])  # carril inferior
            self.direccion = 1  # va hacia la derecha

    def update(self):
        self.rect.x += self.vel * self.direccion

        # Reset cuando sale de pantalla
        if self.carril == "arriba" and self.rect.right < 0:
            self.rect.x = ANCHO
            self.rect.y = random.choice([250, 275])
        elif self.carril == "abajo" and self.rect.left > ANCHO:
            self.rect.x = -40
            self.rect.y = random.choice([425, 450])

# Funciones de dibujo
def dibujar_casa(x, y, techo_y):
    pygame.draw.rect(pantalla, COLORES["AZUL"], (x, y, 100, 100))
    pygame.draw.polygon(pantalla, COLORES["MARRON"], [(x, y), (x + 100, y), (x + 50, techo_y)])

def dibujar_escenario():
    pantalla.fill(COLORES["GRIS"])
    for x in [50, 450]:
        dibujar_casa(x, 50, 10)  # Casa superior
        dibujar_casa(x, ALTO - 150, ALTO - 190)  # Casa inferior
    pygame.draw.rect(pantalla, COLORES["NEGRO"], (0, 250, ANCHO, 300))
    pygame.draw.line(pantalla, COLORES["BLANCO"], (0, 400), (ANCHO, 400), 5)

def mostrar_game_over():
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render("GAME OVER", True, COLORES["ROJO"])
    pantalla.fill(COLORES["GRIS"])
    pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2)))
    pygame.display.flip()
    pygame.time.delay(3000)

# Bucle principal
def juego():
    jugador = Jugador()
    enemigos = pygame.sprite.Group([Enemigo() for _ in range(5)])
    todos = pygame.sprite.Group(jugador, *enemigos)

    vidas = 3
    fuente = pygame.font.Font(None, 36)

    corriendo = True
    while corriendo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                corriendo = False

        todos.update()

        if pygame.sprite.spritecollideany(jugador, enemigos):
            vidas -= 1
            if vidas <= 0:
                break
            jugador.rect.center = (ANCHO // 2, ALTO - 50)

        dibujar_escenario()
        pantalla.blit(fuente.render(f"Vidas: {vidas}", True, COLORES["BLANCO"]), (10, 10))
        todos.draw(pantalla)
        pygame.display.flip()
        clock.tick(FPS)

    mostrar_game_over()
    pygame.quit()

# Ejecutar el juego
juego()

