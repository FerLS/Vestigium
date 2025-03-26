import math
import random

import pygame

from utils.constants import *
from entities.firefly import Firefly
from light2 import CircularLight

from resource_manager import ResourceManager
from sound_manager import SoundManager

class MinigameFirefly(Firefly):
    def __init__(self, firefly_side: Fireflies):
        super().__init__(0, 0, movement_type="wave")
        self.speed = random.uniform(2.5, 3)
        self.y = 0
        self.x = 0
        self.side = firefly_side
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.wave_amplitude = 0
        self.wave_frequency = 0
        self.time = 0
        
        self.resource_manager = ResourceManager()
        self.sheet = self.resource_manager.load_image("firefly.png", "assets\\images").convert_alpha()
   
        self._load_firefly()

    def reset(self):
        
        if self.side == Fireflies.RIGHT:
            self.y = random.randint(200, 650)
            self.speed = random.uniform(3, 8)
            if self.y < 1000:
                self.x = 1000
            else:
                self.x = 600

        if self.side == Fireflies.LEFT:
            self.y = random.randint(200, 650)
            self.speed = random.uniform(2, 6)
            if self.y < 1000:
                self.x = -0  
            else:
                self.x = 400
        
        self.wave_amplitude = random.uniform(random.uniform(2, 4), random.uniform(6, 9))
        self.wave_frequency = random.uniform(0.02, 0.15)
        self.time = 0
    
    def stop(self):
        self.speed = 0
        self.x = 0

    def _load_firefly(self):
        if self.side == Fireflies.RIGHT:
            self._load_right_firefly()

        if self.side == Fireflies.LEFT:
            self._load_left_firefly()

    def _load_left_firefly(self):
        self.frames = self._get_firefly_image(Fireflies.LEFT)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
        self.light = CircularLight(self.rect.center, 15 * SCALE_FACTOR, segments=400, use_obstacles=False)
        
        self.x = random.randint(150, 450)
        self.y = 0

    def _load_right_firefly(self):
        self.frames = self._get_firefly_image(Fireflies.RIGHT)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
        self.light = CircularLight(self.rect.center, 15 * SCALE_FACTOR, segments=400, use_obstacles=False)

        self.x = random.randint(500, 800)
        self.y = 40
        
    def _get_firefly_image(self, side):
        sheet = self.sheet
        frames = []
        frame_width = 32
        frame_height = 32
        y_offset = 0 if side == Fireflies.RIGHT else sheet.get_height() - frame_height
        for i in range(4):
            frame = sheet.subsurface((i * frame_width, y_offset, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * SCALE_FACTOR, frame_height * SCALE_FACTOR))
            frames.append(frame)
        return frames

    def move(self):
        if self.speed == 0:
            return

        self.time += 1
        wave_offset = self.wave_amplitude * math.sin(self.time * self.wave_frequency)

        if self.side == Fireflies.RIGHT:
            self.x -= self.speed
            self.y += wave_offset
        elif self.side == Fireflies.LEFT:
            self.x += self.speed
            self.y += wave_offset

        self.rect.center = (self.x, self.y)

        if self.rect.left > 1000 or self.rect.right < 0:
            self.reset()

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def update(self, dt):
        self.move()
        self.light.update(self.rect.center)
        self.update_animation(dt)

    def draw(self, screen, offset=(0, 0)):
        self.light.draw(screen, offset)
        screen.blit(self.image, self.rect.topleft)