import pygame
from light2 import CircularLight
from resource_manager import ResourceManager
from utils.images import extract_frames
from utils.constants import SCALE_FACTOR

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y, move_distance=100, speed=0.5):
        super().__init__()
        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image("ant_spritesheet.png", "assets\\images")
        self.animations = extract_frames(sheet, 0, 64, 32, 32, 4, SCALE_FACTOR)  # Ajusta si el spritesheet tiene más frames

        self.frame_index = 0
        self.animation_speed = 0.2
        self.animation_timer = 0

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_y = float(y)
        self.speed = speed
        self.start_y = y
        self.move_distance = move_distance
        self.direction = 1

        self.light_offset = pygame.math.Vector2(-5, self.rect.height // 2)
        self.light = CircularLight(self.rect.center + self.light_offset, 10 * SCALE_FACTOR)

    def update(self, dt):
        self.pos_y += self.speed * self.direction
        self.rect.y = int(self.pos_y)

        if abs(self.pos_y - self.start_y) >= self.move_distance:
            self.direction *= -1

        light_pos = (self.rect.left + self.light_offset.x, self.rect.top + self.light_offset.y)
        self.light.update(new_position=light_pos)

        self.update_animation(dt)

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            self.image = self.animations[self.frame_index]

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        draw_pos = self.rect.x - offset_x, self.rect.y - offset_y
        screen.blit(self.image, draw_pos)

        debug_platform_rect = self.rect.move(-offset_x, -offset_y)
        pygame.draw.rect(screen, (0, 255, 0), debug_platform_rect, 1)

        self.light.draw(screen, offset)
