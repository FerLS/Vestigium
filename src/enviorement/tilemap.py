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
        self.offset_x = 0  # Inicializamos desplazamiento
        self.offset_y = 0

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

    def update(self, scroll_x, scroll_y):
        """Actualiza el desplazamiento en dirección opuesta al jugador"""
        self.offset_x -= scroll_x  # Mueve en sentido contrario
        self.offset_y -= scroll_y

    def draw(self, screen):
        """Dibuja todas las capas aplicando el desplazamiento"""
        for layer in self.layers:
            layer.draw(screen, self.offset_x, self.offset_y)

    def get_collision_rects(self):
        """Devuelve una lista de todos los rectángulos sólidos aplicando el desplazamiento y el factor de escala"""
        collision_rects = []
        for layer in self.layers:
            if not layer.render_as_image:
                for rect in layer.solid_tiles:
                    moved_rect = pygame.Rect(
                        (
                            rect.x + self.offset_x * SCALE_FACTOR
                        ),  # Aplicamos desplazamiento inverso y factor de escala
                        (rect.y + self.offset_y * SCALE_FACTOR),
                        rect.width,
                        rect.height,
                    )
                    collision_rects.append(moved_rect)
        return collision_rects
