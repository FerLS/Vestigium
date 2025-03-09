import pygame
import os

from utils.constants import (
    CAMERA_LIMITS_X,
    CAMERA_LIMITS_Y,
    MAX_FALL_SPEED,
    HEIGHT,
    MOVE_SPEED,
    SCALE_FACTOR,
    MovementDirections,
    MovementType,
)
from resource_manager import ResourceManager

INITIAL_FALL_SPEED = 5


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tilemap):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = ResourceManager()
        self.sheet = self.resource_manager.load_image("player.png", "assets\\images")
        self.rect = pygame.Rect((x, y), (24 * SCALE_FACTOR, 24 * SCALE_FACTOR))
        self.image = self.sheet.subsurface((0, 0, 24, 24))
        self.image = pygame.transform.scale(
            self.image, (24 * SCALE_FACTOR, 24 * SCALE_FACTOR)
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.dead = False

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
        self.jump_power = -10

        # Animation
        self.fliped = False

    def move(self, direction: MovementDirections, camera_scroll_x):
        if direction == MovementDirections.LEFT and not self.on_wall_left:
            self.velocity_x = (-MOVE_SPEED - camera_scroll_x) * SCALE_FACTOR

        elif direction == MovementDirections.RIGHT and not self.on_wall_right:
            self.velocity_x = (MOVE_SPEED - camera_scroll_x) * SCALE_FACTOR

        else:
            self.velocity_x = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power * SCALE_FACTOR

    def apply_gravity(self):

        if not self.on_ground:
            self.velocity_y += self.gravity * SCALE_FACTOR
            if self.velocity_y >= MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED

        if self.rect.bottom > CAMERA_LIMITS_Y[1]:
            self.velocity_y = 0

    def check_collisions(self, camera_scroll_x, camera_scroll_y):
        # Usamos el método correcto para obtener los rectángulos de colisión
        colliders = self.tilemap.get_collision_rects()

        self.on_ground = False
        self.on_wall_left = False
        self.on_wall_right = False
        self.on_ceil = False

        # Colisiones en el eje Y
        if camera_scroll_y >= 0:
            self.rect.y += self.velocity_y
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_y > 0 or camera_scroll_y > 0:
                    self.rect.bottom = collider.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0 or camera_scroll_y < 0:
                    self.rect.top = collider.bottom
                    self.velocity_y = 0
                    self.on_ceil = True

        # Colisiones en el eje X

        self.rect.x += self.velocity_x
        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.velocity_x > 0 or camera_scroll_x > 0:
                    self.rect.right = collider.left
                    self.on_wall_right = True
                    self.velocity_x = 0
                elif self.velocity_x < 0 or camera_scroll_x < 0:
                    self.rect.left = collider.right
                    self.on_wall_left = True
                    self.velocity_x = 0

    def get_key(self):
        print("You won")

    def die(self):
        self.dead = True
        print("You died")

    def update(self, keys, screen, camera_scroll_x, camera_scroll_y):
        if not self.dead:
            if keys[pygame.K_LEFT]:
                self.move(MovementDirections.LEFT, camera_scroll_x)
            elif keys[pygame.K_RIGHT]:
                self.move(MovementDirections.RIGHT, camera_scroll_x)
            else:
                self.velocity_x = 0

            if keys[pygame.K_SPACE]:
                self.jump()

            self.apply_gravity()
            self.check_collisions(camera_scroll_x, camera_scroll_y)

    def draw(self, screen, keys_pressed):
        screen.blit(self.image, self.rect)

        if keys_pressed[pygame.K_LEFT] and not self.fliped:
            self.fliped = True
            self.image = pygame.transform.flip(self.image, True, False)
        elif keys_pressed[pygame.K_RIGHT] and self.fliped:
            self.fliped = False
            self.image = pygame.transform.flip(self.image, True, False)
