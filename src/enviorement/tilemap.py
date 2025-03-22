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


    def load_layers(self):
        """Carga todas las capas del archivo TMX."""
        layers = {}
        for tmx_layer in self.tmx_data.layers:
            layers[tmx_layer.name] = Layer(tmx_layer, self)
        return layers

    def load_layer_entities(self, entity):
        """Carga los objetos de una de las capas."""
        entities = {}
        object_layer = self.tmx_data.get_layer_by_name(entity)

        for obj in object_layer:
            entities[obj.name] = obj

        for entity in entities:
            entities[entity].x *= SCALE_FACTOR
            entities[entity].y *= SCALE_FACTOR
        return entities
    
    def load_entity(self, entity):
        """Carga un objeto de una capa."""
        for obj in self.tmx_data.objects:
            if obj.name == entity:
                obj.x *= SCALE_FACTOR
                obj.y *= SCALE_FACTOR
                obj.width *= SCALE_FACTOR
                obj.height *= SCALE_FACTOR
                return obj

    def draw(self, screen, offset=(0, 0)):
        """Dibuja todas las capas aplicando el desplazamiento de cámara."""
        for _, v in self.layers.items():
            v.draw(screen, offset)

    def get_collision_rects(self):
        """Devuelve rects del mundo real (sin offset visual)."""
        collision_rects = []
        for k, v in self.layers.items():
            if not v.render_as_image:
                for rect in v.solid_tiles:
                    collision_rects.append(pygame.Rect(
                        rect.x, rect.y, rect.width, rect.height
                    ))
        return collision_rects
