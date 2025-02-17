import pygame
from entities.player import Player
from entorno.suelo import Suelo  # Nueva clase para el suelo

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Crear jugador
player = Player(scale_factor=3)
all_sprites = pygame.sprite.Group(player)

# Crear suelos y plataformas
ground_group = pygame.sprite.Group()
# Suelo principal
ground_group.add(Suelo((0, 550), 800, 50))
# Plataforma de ejemplo
ground_group.add(Suelo((300, 400), 200, 20))

# Bucle principal
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capturar teclas
    keys = pygame.key.get_pressed()
    actions = {
        "left": keys[pygame.K_LEFT],
        "right": keys[pygame.K_RIGHT],
        "jump": keys[pygame.K_SPACE],
    }

    # Actualizar elementos
    player.update(actions, ground_group)  # Pasamos el grupo de suelos
    ground_group.update()

    # Dibujado
    screen.fill((30, 30, 30))  # Color de fondo oscuro
    ground_group.draw(screen)  # Dibujar suelos primero
    all_sprites.draw(screen)  # Dibujar jugador encima

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
