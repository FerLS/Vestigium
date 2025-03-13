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
        self.animations = extract_frames(sheet, 48, 24, 24, 24, 2, SCALE_FACTOR)
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=(x , y))
        self.pos = (x, y)
        #self.mask = pygame.mask.from_surface(self.image)
        
        self.light_radius = 0
        self.light = CircularLight(self.pos, self.light_radius)
        self.glow = False
        self.frame_counter = 0
        self.light_direction = 1
    
    def manage_light(self):
        if self.glow:
            if self.frame_counter == 0:  
                if self.light_radius == 30:
                    self.light_direction = -1
                elif self.light_radius == 0:
                    if self.light_direction < 0:
                        self.glow = False
                    self.light_direction = 1
                else:
                    self.light_radius += 1 * self.light_direction
                    self.light.change_radius(self.light_radius)

    def update(self):
        self.manage_light()
        self.frame_counter = (self.frame_counter + 1) % 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        debug_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(screen, (255, 0, 0), debug_rect, 1)

