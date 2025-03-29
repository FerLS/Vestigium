import pygame
from utils.light import CircularLight
from managers.resource_manager import ResourceManager
from utils.images import extract_frames
from utils.constants import SCALE_FACTOR

class Jellyfish(pygame.sprite.Sprite):
    def __init__(self, x, y, move_distance=180*SCALE_FACTOR, speed=2, initial_direction=1, move_axis='vertical'):
        super().__init__()
        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image("jellyfish_spritesheet.png", "assets\\images")
        self.animations = extract_frames(sheet, 0, 0, 64, 64, 8, SCALE_FACTOR // 1.5)

        self.frame_index = 0
        self.animation_speed = 0.3
        self.animation_timer = 0

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Movement
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.start_x = x
        self.start_y = y
        self.speed = speed
        self.move_distance = move_distance
        self.direction = initial_direction
        self.move_axis = move_axis 

        # Light
        self.light = CircularLight(self.rect.center, 25 * SCALE_FACTOR, segments=400, use_obstacles=False)

    def update(self, dt):
        if self.move_axis == 'vertical':
            self.pos_y += self.speed * self.direction
            self.rect.y = int(self.pos_y)
            if abs(self.pos_y - self.start_y) >= self.move_distance:
                self.direction *= -1

        elif self.move_axis == 'horizontal':
            self.pos_x += self.speed * self.direction
            self.rect.x = int(self.pos_x)
            if abs(self.pos_x - self.start_x) >= self.move_distance:
                self.direction *= -1

        # Light
        self.light.update(new_position=self.rect.center)

        # Animation
        self.update_animation(dt)

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            self.image = self.animations[self.frame_index]

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        self.light.draw(screen, offset)
        draw_pos = self.rect.x - offset_x, self.rect.y - offset_y
        screen.blit(self.image, draw_pos)


        
