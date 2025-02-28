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

        self.layers = self.load_layers()
        self.offset = 0  # Inicializamos desplazamiento

    def load_layers(self):
        """Carga todas las capas del archivo TMX."""
        layers = []
        for tmx_layer in self.tmx_data.layers:
            layers.append(Layer(tmx_layer, self))
        return layers

    def update(self, scroll_amount):
        """Actualiza el desplazamiento en dirección opuesta al jugador"""
        self.offset -= scroll_amount  # Mueve en sentido contrario

    def draw(self, screen):
        """Dibuja todas las capas aplicando el desplazamiento"""
        for layer in self.layers:
            layer.draw(screen, self.offset)

    def get_collision_rects(self):
        """Devuelve una lista de todos los rectángulos sólidos aplicando el desplazamiento"""
        collision_rects = []
        for layer in self.layers:
            if not layer.render_as_image:
                for rect in layer.solid_tiles:
                    moved_rect = pygame.Rect(
                        rect.x + self.offset,  # Aplicamos desplazamiento inverso
                        rect.y,
                        rect.width,
                        rect.height,
                    )
                    collision_rects.append(moved_rect)
        return collision_rects
