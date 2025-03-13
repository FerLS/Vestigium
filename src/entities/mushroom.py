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
        self.animations = extract_frames(sheet, 48, 24, 24, 24, 2, SCALE_FACTOR * 2)
        self.image = self.animations[0]
        self.rect = pygame.Rect(x, y, 24 * SCALE_FACTOR, 24 * SCALE_FACTOR)
        #self.rect = self.image.get_rect(topleft=(x , y))
        self.pos = (x, y)
        #self.mask = pygame.mask.from_surface(self.image)
        
        self.light_radius = 0
        self.light = CircularLight(self.pos, self.light_radius)
        self.glow = False
        self.frame_counter = 0
        self.light_direction = 1
    
    def manage_light(self):
        print(self.frame_counter)
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
        print(self.glow)
        self.manage_light()
        self.frame_counter = (self.frame_counter + 1) % 5
        self.light.update(self.rect.center)

    def draw(self, screen, offset=(0, 0)):
        offset_x, offset_y = offset
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
        self.light.draw(screen, offset)

