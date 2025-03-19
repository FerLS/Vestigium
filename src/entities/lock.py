import pygame
from utils.constants import *

class Lock(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_width, on_animation_end):
        super().__init__()
        self.sheet = pygame.image.load("assets/images/lock.png").convert_alpha()
        self.frames = self._load_frames()
        self.image = self.frames[0]
        self.image = pygame.transform.scale(self.image, (self.frames[0].get_width() * SCALE_FACTOR, self.frames[0].get_height() * SCALE_FACTOR))
        self.rect = self.image.get_rect(center=(screen_width // 2, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.is_playing_animation = False
        self.on_animation_end = on_animation_end
        self.original_center = (screen_width // 2, y)

    def _load_frames(self):
        frame_width = self.sheet.get_width() // 9
        frame_height = self.sheet.get_height()
        frames = []
        for i in range(9):
            frame = self.sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * SCALE_FACTOR, frame_height * SCALE_FACTOR))
            frames.append(frame)
        return frames

    def play_animation(self):
        self.is_playing_animation = True
        self.animation_index = 0
        self.animation_timer = 0

    def update(self, dt, key):
        if self.is_playing_animation:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_index += 1
                if self.animation_index >= len(self.frames):
                    self.animation_index = len(self.frames) - 1
                    self.is_playing_animation = False
                    if self.on_animation_end:
                        self.on_animation_end()
                self.image = self.frames[self.animation_index]
                self.image = pygame.transform.scale(self.image, (self.frames[0].get_width() * SCALE_FACTOR, self.frames[0].get_height() * SCALE_FACTOR))
                self.rect = self.image.get_rect(center=self.original_center)
                self.mask = pygame.mask.from_surface(self.image)

        if not self.is_playing_animation and pygame.sprite.collide_mask(self, key):
            self.play_animation()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
