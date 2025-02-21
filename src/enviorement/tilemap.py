import pygame

from utils.constants import HEIGHT


class Tilemap:
    def __init__(self, tile_size, map_data, tileset, scale_factor):
        self.tile_size = int(tile_size * scale_factor)
        self.map_data = map_data  # Matriz con valores de los tiles
        self.tileset = self.scale_tileset(
            tileset, scale_factor
        )  # Diccionario con imágenes de tiles escaladas
        self.width = len(map_data[0]) * self.tile_size
        self.height = len(map_data) * self.tile_size
        self.mask = pygame.Mask((self.width, self.height))

    def scale_tileset(self, tileset, scale_factor):
        scaled_tileset = {}
        for key, tile in tileset.items():
            new_size = (
                round(tile.get_width() * scale_factor),
                round(tile.get_height() * scale_factor),
            )
            scaled_tile = pygame.transform.scale(tile, new_size)
            scaled_tileset[key] = scaled_tile
        return scaled_tileset

    def draw(self, screen):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile in self.tileset:
                    screen.blit(
                        self.tileset[tile],
                        (
                            x * self.tile_size,
                            HEIGHT - (self.height - y * self.tile_size),
                        ),
                    )
                elif tile == -1:
                    # Aire
                    pass

    @staticmethod
    def load_tileset(image_path, tile_size, columns=5, rows=5, spacing=16):
        image = pygame.image.load(
            image_path
        ).convert_alpha()  # Cargar con transparencia
        tileset = {}

        for y in range(rows):
            for x in range(columns):
                # Extraer correctamente la parte exacta del tileset
                tile = image.subsurface(
                    pygame.Rect(
                        x * (tile_size + spacing),
                        y * (tile_size + spacing),
                        tile_size,
                        tile_size,
                    )
                ).copy()  # Copia para evitar referencias erróneas

                tileset[y * columns + x] = tile  # Guardar en el diccionario

        return tileset
