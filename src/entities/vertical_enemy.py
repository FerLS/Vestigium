import pygame
from light2 import CircularLight
from utils.constants import SCALE_FACTOR

class VerticalEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, move_distance=100, speed=0.75, light_radius=10, light_offset=None):
        super().__init__()
        self.WIDTH = width
        self.HEIGHT = height
        self.rect = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)

        self.pos_y = float(y)
        self.speed = speed
        self.start_y = y
        self.move_distance = move_distance
        self.direction = 1

        self.light_offset = light_offset or pygame.math.Vector2(-5, self.HEIGHT // 2)
        self.light = CircularLight(self.rect.center + self.light_offset, light_radius * SCALE_FACTOR)

    def update(self):
        self.pos_y += self.speed * self.direction
        self.rect.y = int(self.pos_y)

        if abs(self.pos_y - self.start_y) >= self.move_distance:
            self.direction *= -1

        light_pos = (self.rect.left + self.light_offset.x, self.rect.top + self.light_offset.y)
        self.light.update(new_position=light_pos)

    def draw(self, screen, offset=(0, 0)):
        # Este método debe ser sobreescrito por clases hijas si quieren usar sprites específicos
        offset_x, offset_y = offset
        image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.ellipse(image, (100, 100, 100), (0, 0, self.WIDTH, self.HEIGHT))
        draw_pos = self.rect.x - offset_x, self.rect.y - offset_y
        screen.blit(image, draw_pos)
        self.light.draw(screen, offset)
