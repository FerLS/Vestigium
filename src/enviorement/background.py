import pygame
import os
import resource_manager
from utils.constants import WIDTH, HEIGHT


class BackgroundLayer:
    def __init__(self, resource_manager, image_name, assets_path, speed=1.0):
        self.resource_manager = resource_manager
        self.image = self.resource_manager.load_image(image_name, assets_path)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.rect = self.image.get_rect()
        self.speed = speed

    def draw(self, screen, camera_offset):
        offset_x = int(camera_offset[0] * self.speed)
        image_width = self.rect.width

        start_x = - (offset_x % image_width)

        x = start_x
        while x < screen.get_width():
            screen.blit(self.image, (x, 0))
            x += image_width



class Background:
    def __init__(self, resource_manager, assets_path):
        self.layers = []
        speed = 0.0
        for layer in sorted(os.listdir(assets_path)):  
            speed += 0.2
            self.layers.append(
                BackgroundLayer(resource_manager, layer, assets_path, speed)
            )

    def draw(self, screen, camera_offset):
        for layer in self.layers:
            layer.draw(screen, camera_offset)
