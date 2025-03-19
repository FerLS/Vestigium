import pygame
from utils.constants import SCALE_FACTOR
from utils.images import extract_frames
from resource_manager import ResourceManager

class Anglerfish(pygame.sprite.Sprite):
    def __init__(self, x, y, slow_speed=1, fast_speed=1000000, switch_speed_time=5000):
        super().__init__()

        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image("fish_spritesheet.png", "assets\\images")
        self.animations = extract_frames(sheet, 0, 0, 32, 32, 4, SCALE_FACTOR * 3)

        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.flipped = False

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.prev_x = self.rect.x

        self.slow_speed = slow_speed
        self.fast_speed = fast_speed
        self.current_speed = self.slow_speed

        self.switch_speed_time = switch_speed_time
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt, player_position=None):

        # Change speed after a certain amount of time
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time >= self.switch_speed_time:
            self.current_speed = self.fast_speed

        # Follow player
        if player_position:
            player_x, player_y = player_position

            if self.rect.x < player_x:
                self.rect.x += self.current_speed
                if self.rect.x > player_x:
                    self.rect.x = player_x
            elif self.rect.x > player_x:
                self.rect.x -= self.current_speed
                if self.rect.x < player_x:
                    self.rect.x = player_x

            follow_strength = 0.025
            self.rect.y += int((player_y - self.rect.y) * follow_strength)

        # Check if the fish is flipped
        if self.rect.x > self.prev_x:
            self.flipped = False
        elif self.rect.x < self.prev_x:
            self.flipped = True 

        self.prev_x = self.rect.x

        self.update_animation(dt)

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            new_frame = self.animations[self.frame_index]
            self.image = pygame.transform.flip(new_frame, True, False) if self.flipped else new_frame

    def draw(self, screen, camera_offset=(0, 0)):
        draw_pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        screen.blit(self.image, draw_pos)
