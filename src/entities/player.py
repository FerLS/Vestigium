import pygame
import os

from utils.constants import MovementDirections, MovementType
from resource_manager import ResourceManager 

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = ResourceManager()
        self.sheet = self.resource_manager.load_image("player.png", "assets\\images")
        self.rect = pygame.Rect((0, 0), (24, 24))
        self.image = self.sheet.subsurface(self.rect)
        self.movement = MovementType.IDLE
        self.rect.x = x
        self.rect.y = y
        self.velocity = 5

    def move(self, direction : MovementDirections):
        if direction == MovementDirections.LEFT:
            self.rect.x -= self.velocity
        if direction == MovementDirections.RIGHT:
            self.rect.x += self.velocity
    
    def draw(self, screen):
        screen.blit(self.sheet, (self.rect.x, self.rect.y), self.rect)
    
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.move(MovementDirections.LEFT)
        if keys[pygame.K_RIGHT]:
            self.move(MovementDirections.RIGHT)