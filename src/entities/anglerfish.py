import pygame

from utils.constants import SCALE_FACTOR
from utils.images import extract_frames
from resource_manager import ResourceManager

class Anglerfish(pygame.sprite.Sprite):
    def __init__(self, x, y, slow_speed=1, fast_speed=3, switch_speed_time=3000):
        super().__init__()

        # Carga de imagen y animaciones
        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image("fish_spritesheet.png", "assets\\images")
        self.animations = extract_frames(sheet, 0, 0, 32, 32, 4, SCALE_FACTOR * 2)
        
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_timer = 0

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Movimiento horizontal
        self.slow_speed = slow_speed
        self.fast_speed = fast_speed
        self.current_speed = self.slow_speed

        # Movimiento vertical hacia target_y
        self.target_y = y
        self.y_speed = 2  

        # Cambio de velocidad tras cierto tiempo
        self.switch_speed_time = switch_speed_time
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt, target_y=None):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time >= self.switch_speed_time:
            self.current_speed = self.fast_speed

        self.rect.x += self.current_speed

        if target_y is not None:
            self.target_y = target_y

        if self.rect.y < self.target_y:
            self.rect.y += self.y_speed
            if self.rect.y > self.target_y:
                self.rect.y = self.target_y
        elif self.rect.y > self.target_y:
            self.rect.y -= self.y_speed
            if self.rect.y < self.target_y:
                self.rect.y = self.target_y

        self.update_animation(dt)

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            self.image = self.animations[self.frame_index]

    def draw(self, screen, camera_offset=(0, 0)):
        draw_pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        screen.blit(self.image, draw_pos)
