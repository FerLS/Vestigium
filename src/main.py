import pygame
import sys
from pygame.locals import *
from utils.constants import MovementDirections

WIDTH, HEIGHT = 800, 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()




while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Handle user input
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()
    
    # Fill color
    screen.fill((133,133,133))

    pygame.display.update()
    clock.tick(60)
