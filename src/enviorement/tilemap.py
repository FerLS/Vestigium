import pygame
import pytmx
from .layer import Layer


class Tilemap:
    def __init__(self, tmx_file):
        self.tmx_data = pytmx.load_pygame(tmx_file, pixelalpha=True)
        self.tile_size = self.tmx_data.tilewidth
        self.width = self.tmx_data.width * self.tile_size
        self.height = self.tmx_data.height * self.tile_size
        self.mask = pygame.Mask((self.width, self.height))

        # Cargar todas las capas
        self.layers = self.load_layers()

    def load_layers(self):
        """Carga todas las capas del archivo TMX."""
        layers = []
        for tmx_layer in self.tmx_data.layers:
            layers.append(Layer(tmx_layer, self))
        return layers

    def draw(self, screen):
        """Dibuja todas las capas en orden."""
        for layer in self.layers:
            layer.draw(screen)

    def get_collision_rects(self):
        """Devuelve una lista de todos los rectángulos sólidos en el mapa."""
        collision_rects = []
        for layer in self.layers:
            collision_rects.extend(layer.solid_tiles)
        return collision_rects
