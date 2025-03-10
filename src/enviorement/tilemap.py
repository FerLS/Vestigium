import pygame
import pytmx

from utils.constants import SCALE_FACTOR
from .layer import Layer


class Tilemap:
    def __init__(self, tmx_file):
        self.tmx_data = pytmx.load_pygame(tmx_file, pixelalpha=True)
        self.tile_size = self.tmx_data.tilewidth
        self.width = self.tmx_data.width * self.tile_size
        self.height = self.tmx_data.height * self.tile_size
        self.mask = pygame.Mask((self.width, self.height))

        self.layers = self.load_layers()
        self.entities = self.load_entities()  # Cargar entidades

    def load_layers(self):
        """Carga todas las capas del archivo TMX."""
        layers = []
        for tmx_layer in self.tmx_data.layers:
            layers.append(Layer(tmx_layer, self))
        return layers

    def load_entities(self):
        """Carga los objetos de la capa de entidades."""
        entities = {}
        for obj in self.tmx_data.objects:
            entities[obj.name] = obj

        for entity in entities:
            entities[entity].x *= SCALE_FACTOR
            entities[entity].y *= SCALE_FACTOR
        return entities

    def draw(self, screen, offset=(0, 0)):
        """Dibuja todas las capas aplicando el desplazamiento de cámara."""
        for layer in self.layers:
            layer.draw(screen, offset)

    def get_collision_rects(self):
        """Devuelve rects del mundo real (sin offset visual)."""
        collision_rects = []
        for layer in self.layers:
            if not layer.render_as_image:
                for rect in layer.solid_tiles:
                    collision_rects.append(pygame.Rect(
                        rect.x, rect.y, rect.width, rect.height
                    ))
        return collision_rects
