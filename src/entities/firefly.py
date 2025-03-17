import pygame
import random
from light2 import CircularLight

class Firefly(pygame.sprite.Sprite):
    def __init__(self, x, y, movement_bounds=None):
        super().__init__()
        self.RADIUS = 5
        self.radius_variation = 2
        self.blink_interval = 15
        self.current_radius = self.RADIUS

        self.light = CircularLight((x, y), self.RADIUS + 20, use_obstacles=False)
        self.rect = pygame.Rect(x, y, self.RADIUS * 2, self.RADIUS * 2)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_speed = 1.5
        self.acceleration_change = 0.2
        self.movement_bounds = movement_bounds

        self.blink_timer = 0
        self.blink_up = True

    def update(self):
        # Movimiento oscilante
        delta = pygame.math.Vector2(
            random.uniform(-self.acceleration_change, self.acceleration_change),
            random.uniform(-self.acceleration_change, self.acceleration_change)
        )
        self.velocity += delta

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.movement_bounds:
            if not self.movement_bounds.contains(self.rect):
                if self.rect.left < self.movement_bounds.left or self.rect.right > self.movement_bounds.right:
                    self.velocity.x *= -1
                if self.rect.top < self.movement_bounds.top or self.rect.bottom > self.movement_bounds.bottom:
                    self.velocity.y *= -1
                self.rect.clamp_ip(self.movement_bounds)

        # Parpadeo
        self.blink_timer += 1
        if self.blink_timer >= self.blink_interval:
            self.blink_up = not self.blink_up
            self.blink_timer = 0

        self.current_radius = self.RADIUS + self.radius_variation if self.blink_up else self.RADIUS

        self.light.update(new_position=self.rect.center)
        self.light.change_radius(self.current_radius + 20)

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        image = pygame.Surface((self.current_radius * 2, self.current_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(image, (255, 255, 100), (self.current_radius, self.current_radius), self.current_radius)
        draw_pos = self.rect.centerx - self.current_radius - offset_x, self.rect.centery - self.current_radius - offset_y
        screen.blit(image, draw_pos)
        self.light.draw(screen, offset)
