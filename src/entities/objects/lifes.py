import pygame
from managers.resource_manager import ResourceManager
from managers.sound_manager import SoundManager

class Lifes:
    def __init__(self):
        self.resource_manager = ResourceManager()
        self.ammount = 3
        self.heart_image = self.resource_manager.load_image("heart.png", "assets/life")
        self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))
        self.animation_sheet = self.resource_manager.load_image("heart_animated_1.png", "assets/life")
        self.frame_width = self.animation_sheet.get_width() // 5
        self.frame_height = self.animation_sheet.get_height()
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_duration = 0.1
        self.animating = False
        self.scaled_frames = [
            pygame.transform.scale(
                self.animation_sheet.subsurface(pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)),
                (40, 40)
            )
            for i in range(5)
        ]
        
        self.sound_manager = SoundManager()

    def decrease(self):
        if self.ammount > 0:
            self.ammount -= 1
            self.animating = True
            self.current_frame = 0
            self.animation_timer = pygame.time.get_ticks()
            self.sound_manager.play_sound("damage.wav", "assets/sounds", 0.1, 0.5)

    def update(self):
        if self.animating:
            elapsed_time = (pygame.time.get_ticks() - self.animation_timer) / 1000
            if elapsed_time > self.animation_duration:
                self.animation_timer = pygame.time.get_ticks()
                self.current_frame += 1
                if self.current_frame >= 5:
                    self.animating = False

    def reset(self):
        self.ammount = 3
        self.animating = False
        self.current_frame = 0

    def draw(self, screen):
        for i in range(self.ammount):
            screen.blit(self.heart_image, (10 + i * 50, 10))
    
        if self.animating and self.ammount < 3:
            screen.blit(self.scaled_frames[self.current_frame], (10 + self.ammount * 50, 10))

