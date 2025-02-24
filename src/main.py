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
test_level = TestLevel(screen)



while True:

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Update scene
    test_level.update(pressed_keys)

    test_level.draw()
    # Update screen
    pygame.display.update()
    clock.tick(60)
