import pygame
from utils.light import CircularLight
from managers.resource_manager import ResourceManager
from managers.sound_manager import SoundManager
from utils.images import extract_frames
from utils.constants import SCALE_FACTOR

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y, move_distance=100, speed=0.5):
        super().__init__()
        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image("spider_spritesheet.png", "assets\\images")
        self.animations = extract_frames(sheet, 0, 0, 32, 32, 4, SCALE_FACTOR)

        self.frame_index = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.flipped = False

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_y = float(y)
        self.speed = speed
        self.start_y = y
        self.move_distance = move_distance
        self.direction = 1

        self.light = CircularLight(self.rect.center, 10 * SCALE_FACTOR)

    def update(self, dt):
        self.pos_y += self.speed * self.direction
        self.rect.y = int(self.pos_y)

        if abs(self.pos_y - self.start_y) >= self.move_distance:
            self.flipped = not self.flipped
            self.direction *= -1

        self.light.update(new_position=self.rect.center)

        self.update_animation(dt)

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            new_frame = self.animations[self.frame_index]
            self.image = pygame.transform.flip(new_frame, False, True) if self.flipped else new_frame
    
    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        # self.light.draw(screen, offset) # Manage light with animation
        draw_pos = self.rect.x - offset_x, self.rect.y - offset_y
        screen.blit(self.image, draw_pos)


        """debug_platform_rect = self.rect.move(-offset_x, -offset_y)
        pygame.draw.rect(screen, (0, 255, 0), debug_platform_rect, 1)"""

        
