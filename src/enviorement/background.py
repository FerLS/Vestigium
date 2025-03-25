import pygame
import os
import resource_manager
from utils.constants import WIDTH, HEIGHT


class BackgroundLayer:
    def __init__(self, resource_manager, image_name, assets_path, speed_x=1.0, speed_y=0.0):
        self.resource_manager = resource_manager
        self.image = self.resource_manager.load_image(image_name, assets_path)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.rect = self.image.get_rect()
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self, screen, camera_offset):
        offset_x = int(camera_offset[0] * self.speed_x)
        offset_y = int(camera_offset[1] * self.speed_y)

        image_width = self.rect.width
        image_height = self.rect.height

        start_x = - (offset_x % image_width)
        start_y = - (offset_y % image_height)

        x = start_x
        while x < screen.get_width():
            y = start_y
            while y < screen.get_height():
                screen.blit(self.image, (x, y))
                y += image_height
            x += image_width


class Background:
    def __init__(self, resource_manager, assets_path, speed_increment=0.2, enable_vertical_scroll=False):
        self.layers = []
        speed = 0.0
        for layer in sorted(os.listdir(assets_path)):  
            speed += speed_increment
            vertical_speed = speed if enable_vertical_scroll else 0.0
            self.layers.append(
                BackgroundLayer(resource_manager, layer, assets_path, speed_x=speed, speed_y=vertical_speed)
            )

    def draw(self, screen, camera_offset):
        for layer in self.layers:
            layer.draw(screen, camera_offset)
