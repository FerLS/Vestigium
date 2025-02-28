from abc import ABC

from enviorement.tilemap import Tilemap


class Scene(ABC):

    def __init__(self, tile_map, screen):
        self.tile_map: Tilemap = tile_map
        self.screen = screen

    def draw(self):
        self.tile_map.draw(self.screen)

        pass

    def update(self):
        self.draw()
        pass
