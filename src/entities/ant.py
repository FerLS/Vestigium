import pygame
import random
from light2 import CircularLight

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y, movement_bounds=None):
        super().__init__()
        self.WIDTH = 10
        self.HEIGHT = 6
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

        self.velocity_y = random.uniform(-1, 1)
        self.acceleration_change = 0.5
        self.max_speed = 2

        self.movement_bounds = movement_bounds

        self.light_offset = pygame.math.Vector2(-5, self.HEIGHT // 2)
        self.light = CircularLight(self.rect.center + self.light_offset, 20)

    def update(self):
        delta_y = random.uniform(-self.acceleration_change, self.acceleration_change)
        self.velocity_y += delta_y
        self.velocity_y = max(-self.max_speed, min(self.velocity_y, self.max_speed))

        self.rect.y += self.velocity_y

        if self.movement_bounds:
            if self.rect.top < self.movement_bounds.top or self.rect.bottom > self.movement_bounds.bottom:
                self.velocity_y *= -1
                self.rect.clamp_ip(self.movement_bounds)

        light_pos = (self.rect.left + self.light_offset.x, self.rect.top + self.light_offset.y)
        self.light.update(new_position=light_pos)

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset

        image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.ellipse(image, (50, 50, 50), (0, 0, self.WIDTH, self.HEIGHT)) 
        draw_pos = self.rect.x - offset_x, self.rect.y - offset_y
        screen.blit(image, draw_pos)

        self.light.draw(screen, offset)
