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
        self.sprites = []  # Lista de sprites dentro del Tilemap

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
                return obj

    def insert_sprite(self, sprite, layer_index):
        """Inserta un sprite en una posición específica de las capas."""
        self.sprites.append(
            (sprite, layer_index)
        )  # Guarda el sprite con su índice de capa
        self.sprites.sort(key=lambda x: x[1])  # Ordena los sprites según la capa

    def draw(self, screen, offset=(0, 0)):
        """Dibuja las capas y los sprites en el orden correcto"""
        sorted_layers = sorted(
            self.layers.items(), key=lambda x: x[0], reverse=False
        )  # Invertir el orden
        sprite_index = 0
        # Dibuja los sprites con índice de capa negativo (detrás de todas las capas)
        while sprite_index < len(self.sprites) and self.sprites[sprite_index][1] < 0:
            self.sprites[sprite_index][0].draw(screen, offset)
            sprite_index += 1
        for i, (_, layer) in enumerate(sorted_layers):
            layer.draw(screen, offset)
            # Dibuja los sprites en su posición de capa correcta
            while (
                sprite_index < len(self.sprites) and self.sprites[sprite_index][1] == i
            ):
                self.sprites[sprite_index][0].draw(screen, offset)
                sprite_index += 1

    def get_solid_rects(self):
        """Obtiene rectángulos de colisión sólidos (todas las direcciones)."""
        solid_rects = []
        for layer in self.layers.values():
            solid_rects.extend(layer.solid_tiles)
        return solid_rects

    def get_platform_rects(self):
        """Obtiene rectángulos de plataformas (solo colisión desde arriba)."""
        platform_rects = []
        for layer in self.layers.values():
            platform_rects.extend(layer.platform_tiles)
        return platform_rects

    def get_stairs_rects(self):
        """Obtiene rectángulos de escaleras."""
        stairs_rects = []
        for layer in self.layers.values():
            stairs_rects.extend(layer.stairs_tiles)
        return stairs_rects

    def get_safe_rects(self):
        """Obtiene rectángulos de zonas seguras."""
        safe_rects = []
        for layer in self.layers.values():
            safe_rects.extend(layer.safe_tiles)
        return safe_rects
