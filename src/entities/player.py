import pygame
import os

from utils.constants import SCALE_FACTOR, MovementDirections, MovementType
from resource_manager import ResourceManager

INITIAL_FALL_SPEED = 5
MAX_FALL_SPEED = 10 

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = ResourceManager()
        self.sheet = self.resource_manager.load_image("player.png", "assets\\images")
        self.rect = pygame.Rect((0, 0), (24, 24))
        self.image = self.sheet.subsurface(self.rect)
        self.image = pygame.transform.scale(
            self.image, (24 * SCALE_FACTOR, 24 * SCALE_FACTOR)
        )
        self.on_ground = True
        self.gravity = 10
        self.movement = MovementType.IDLE
        self.rect.x = x
        self.rect.y = y
        self.velocity = 5
        self.time_falling = 0.0
        self.jump_power = 0
        

    def move(self, direction: MovementDirections):
        if direction == MovementDirections.LEFT:
            self.rect.x -= self.velocity
        if direction == MovementDirections.RIGHT:
            self.rect.x += self.velocity

    def jump(self):
        if self.on_ground:
            self.jump_power = 13
            self.on_ground = False

    def apply_gravity(self):
        if not self.on_ground:
            self.time_falling += 0.04
            speed = (INITIAL_FALL_SPEED + self.time_falling * (MAX_FALL_SPEED - INITIAL_FALL_SPEED)) - self.jump_power
            if speed > MAX_FALL_SPEED:
                speed = MAX_FALL_SPEED
            self.rect.y += speed
        else:
            self.jump_power = 0

    #TODO: Check collisions with tilemap:

    def check_collisions(self):
        print("cesped")

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y), self.rect)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.move(MovementDirections.LEFT)
        if keys[pygame.K_RIGHT]:
            self.move(MovementDirections.RIGHT)
        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_g]:
            self.check_on_ground()

        self.apply_gravity()
