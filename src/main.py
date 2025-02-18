import pygame
from entities.player import Player
from entorno.suelo import Suelo  # Clase para el suelo

# Inicialización
pygame.init()
WIDTH, HEIGHT = 800, 600  # Tamaño de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Crear jugador
player = Player(scale_factor=3)
player.rect.x = WIDTH // 2  # Posicionar al jugador en el centro de la pantalla
all_sprites = pygame.sprite.Group(player)

# Crear suelos y plataformas
ground_group = pygame.sprite.Group()
# Suelo principal
ground_group.add(Suelo((0, 550), 1600, 50))  # Suelo más largo para desplazamiento
# Plataforma de ejemplo
ground_group.add(Suelo((300, 400), 200, 20))
ground_group.add(Suelo((700, 350), 200, 20))  # Más plataformas para moverse

# Variable de desplazamiento
scroll_x = 0  # Controla el desplazamiento lateral

# Definir los límites de la "death zone"
death_zone_left = WIDTH * 0.3
death_zone_right = WIDTH * 0.7

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

    # Actualizar jugador
    player.update(actions, ground_group)

    # Scroll lateral: solo si el jugador está fuera de la "death zone"
    if player.rect.centerx > death_zone_right:
        scroll_x += player.rect.centerx - death_zone_right
        player.rect.centerx = death_zone_right  # Mantenerlo en el borde derecho
    elif player.rect.centerx < death_zone_left:
        scroll_x += player.rect.centerx - death_zone_left
        player.rect.centerx = death_zone_left  # Mantenerlo en el borde izquierdo

    # Dibujado
    screen.fill((30, 30, 30))  # Color de fondo oscuro

    # Dibujar suelos desplazándolos con el scroll_x
    for ground in ground_group:
        screen.blit(ground.image, (ground.rect.x - scroll_x, ground.rect.y))

    # Dibujar jugador ajustando su posición con el scroll
    screen.blit(player.image, (player.rect.x, player.rect.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
