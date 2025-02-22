import pygame
from utils.constants import *

# ANTES DE LOS IMPORTS
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


import sys
from pygame.locals import *
from entities.player import Player
from levels.test_level import TestLevel


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
test_level = TestLevel(screen)
player = Player(WIDTH//2, HEIGHT//2, test_level.tile_map)
all_sprites.add(player)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Fill color
    screen.fill((133, 133, 133))

    # Update scene
    test_level.update()
    
    # Update and draw sprites
    all_sprites.update(pressed_keys)
    all_sprites.draw(screen)
    player.draw(screen)
    # Update screen
    pygame.display.update()
    clock.tick(60)
