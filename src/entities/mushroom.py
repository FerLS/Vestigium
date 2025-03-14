import pygame
from resource_manager import ResourceManager
from light2 import CircularLight
from utils.images import extract_frames
from utils.constants import WIDTH, HEIGHT, SCALE_FACTOR

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image("mushrooms.png", "assets/images")
        self.animations = extract_frames(sheet, 0, 24, 24, 24, 7, SCALE_FACTOR * 2)
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        platform_width = 30
        platform_height = 60
        platform_x = self.rect.centerx - 5
        platform_y = self.rect.centery - 30

        self.platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)

        self.light_radius = 0
        self.light = CircularLight(self.platform_rect.center, self.light_radius, segments=275)
        self.glow = False
        self.frame_counter = 0
        self.light_direction = 1

    def manage_light(self):
        if self.glow:
            if self.frame_counter == 0:  
                self.light_radius += 1 * self.light_direction
                self.light.change_radius(self.light_radius)
                if self.light_radius == 40:
                    self.light_direction = -1
                elif self.light_radius == 0:
                    if self.light_direction < 0:
                        self.glow = False
                    self.light_direction = 1

    def update(self):
        self.platform_rect.x = self.rect.centerx - 5
        self.platform_rect.y = self.rect.centery - 30
        self.light.update(new_position=self.platform_rect.center)
        self.manage_light()
        self.frame_counter = (self.frame_counter + 1) % 5

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
        self.light.draw(screen, offset)
        
        """debug_platform_rect = self.platform_rect.move(-offset_x, -offset_y)
        pygame.draw.rect(screen, (0, 255, 0), debug_platform_rect, 1)"""
