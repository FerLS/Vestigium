import pygame
import os

from utils.constants import (
    CAMERA_LIMITS_X,
    MOVE_SPEED,
    SCALE_FACTOR,
    MovementDirections,
    MovementType,
)
from resource_manager import ResourceManager

INITIAL_FALL_SPEED = 5
MAX_FALL_SPEED = 10


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = ResourceManager()
        self.sheet = self.resource_manager.load_image("player.png", "assets\\images")
        self.rect = pygame.Rect((0, 0), (24 * SCALE_FACTOR, 24 * SCALE_FACTOR))
        self.image = self.sheet.subsurface((0, 0, 24, 24))
        self.image = pygame.transform.scale(
            self.image, (24 * SCALE_FACTOR, 24 * SCALE_FACTOR)
        )

        self.tilemap = tilemap

        # Collisions
        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceil = False

        # Physics
        self.gravity = 0.5
        self.velocity_x = 0
        self.velocity_y = 0
        self.movement = MovementType.IDLE
        self.jump_power = -15

        # Animation
        self.fliped = False

    def move(self, direction: MovementDirections):
        if direction == MovementDirections.LEFT and not self.on_wall_left:
            self.velocity_x = -MOVE_SPEED
            if self.rect.left < CAMERA_LIMITS_X[0]:
                self.velocity_x = 0
        elif direction == MovementDirections.RIGHT and not self.on_wall_right:
            self.velocity_x = MOVE_SPEED
            if self.rect.right >= CAMERA_LIMITS_X[1]:
                self.velocity_x = 0
        else:
            self.velocity_x = 0

        print(self.velocity_x)

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity_y += self.gravity
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED

    def check_collisions(self):
        # Usamos el método correcto para obtener los rectángulos de colisión
        colliders = self.tilemap.get_collision_rects()

        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceil = False

        # Colisiones en el eje Y
        self.rect.y += self.velocity_y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y > 0:
                    self.rect.bottom = collider.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = collider.bottom
                    self.velocity_y = 0
                    self.on_ceil = True

        # Colisiones en el eje X
        self.rect.x += self.velocity_x
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_x > 0:
                    self.rect.right = collider.left
                    self.on_wall_right = True
                elif self.velocity_x < 0:
                    self.rect.left = collider.right
                    self.on_wall_left = True

    def update(self, keys, screen):
        if keys[pygame.K_LEFT]:
            self.move(MovementDirections.LEFT)
        elif keys[pygame.K_RIGHT]:
            self.move(MovementDirections.RIGHT)
        else:
            self.velocity_x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

        self.apply_gravity()
        self.check_collisions()
        self.draw(screen, keys)

    def draw(self, screen, keys_pressed):
        screen.blit(self.image, self.rect)

        if keys_pressed[pygame.K_LEFT] and not self.fliped:
            self.fliped = True
            self.image = pygame.transform.flip(self.image, True, False)
        elif keys_pressed[pygame.K_RIGHT] and self.fliped:
            self.fliped = False
            self.image = pygame.transform.flip(self.image, True, False)
