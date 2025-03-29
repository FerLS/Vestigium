import pygame
from pygame.locals import *

from utils.constants import *
from managers.resource_manager import ResourceManager

vec = pygame.math.Vector2

class Key(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        resource_manager = ResourceManager()
        self.image = resource_manager.load_image("key.png", "assets/images")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.3), int(self.image.get_height() * 0.3)))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = vec((WIDTH//2, 700))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.player_position = vec(0, 0)
        self.dead = False

    def update(self, lock=None):
        if lock and pygame.sprite.collide_mask(self, lock):
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            return

        self.acc = vec(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = +ACC
        if pressed_keys[K_UP]:
            self.acc.y = -ACC
        if pressed_keys[K_DOWN]:
            self.acc.y = +ACC

        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.player_position = self.pos.copy()

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > HEIGHT-100:
            self.pos.y = HEIGHT-100
        if self.pos.y < 200:
            self.pos.y = 200

        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset(self):
        self.pos = vec((WIDTH//2, 700))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)