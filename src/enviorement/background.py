import pygame
import os
import resource_manager

class BackgroundLayer:
    def __init__(self, resource_manager, image_name, assets_path, speed=1.0):
        self.resource_manager = resource_manager
        self.image = self.resource_manager.load_image(image_name, assets_path)
        
        self.rect = self.image.get_rect()
        self.speed = speed 
        self.offset = 0  

    def update(self, scroll_amount):
        self.offset += scroll_amount * self.speed

        if self.offset >= self.rect.width:
            self.offset -= self.rect.width
        elif self.offset <= -self.rect.width:
            self.offset += self.rect.width

    def draw(self, screen):
        screen.blit(self.image, (-self.offset, 0))
        if self.offset > 0:
            screen.blit(self.image, (-self.offset + self.rect.width, 0))
        elif self.offset < 0:
            screen.blit(self.image, (-self.offset - self.rect.width, 0))

class Background():
    def __init__(self, resource_manager, assets_path):
        self.layers = []
        speed = 0.0
        for layer in os.listdir(assets_path):
            speed += 0.2
            self.layers.append(BackgroundLayer(resource_manager, layer, assets_path, speed))

    def update(self, scroll_amount):
        for layer in self.layers:
            layer.update(scroll_amount)

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)