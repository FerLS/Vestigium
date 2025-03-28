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
        self.animations = extract_frames(sheet, 0, 24, 24, 24, 12, SCALE_FACTOR * 2)
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Invisible platform
        platform_width = 60
        platform_height = 30
        platform_x = self.rect.centerx - 20
        platform_y = self.rect.centery - 30
        self.platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)

        # Light
        self.light_radius = 0
        self.light = CircularLight(self.platform_rect.center, self.light_radius, segments=275, use_obstacles=False)
        self.glow = False
        self.bounce = False
        self.bounce_index = 0
        self.bounce_timer = 0
        self.bounce_speed = 10 
        self.frame_counter = 0
        self.light_direction = 1

    def manage_light(self):
        """
        Manage the light of the mushroom.
        """
        # Activate glowing
        if self.glow and self.frame_counter % 2 == 0:
            self.light_radius += 1 * self.light_direction
            self.light.change_radius(self.light_radius)
            # Stop glowing
            if self.light_radius == 40:
                self.light_direction = -1
            # Continue glowing
            elif self.light_radius == 0:
                if self.light_direction < 0:
                    self.glow = False
                self.light_direction = 1

    def update_animation(self):
        """
        Update the animation of the mushroom.
        """
        if self.bounce:
            self.bounce_timer += 1
            if self.bounce_timer >= self.bounce_speed:
                self.bounce_timer = 0
                self.bounce_index += 1
                if self.bounce_index >= len(self.animations):
                    self.bounce_index = 0
                    self.bounce = False
                self.image = self.animations[self.bounce_index]

    def update(self):
        self.light.update(new_position=self.platform_rect.center)
        self.manage_light()
        self.update_animation()
        self.frame_counter += 1 # Used for light animation control

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
        # self.light.draw(screen, offset) # Manage light with animation
        
        """debug_platform_rect = self.platform_rect.move(-offset_x, -offset_y)
        pygame.draw.rect(screen, (0, 255, 0), debug_platform_rect, 1)"""
