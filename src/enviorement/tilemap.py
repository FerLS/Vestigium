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
        self.solid_tiles = self.calculate_solid_tiles()

        self.offset = 0  

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
    
    def update(self, scroll_amount):
        scroll_speed = 0.5
        self.offset += scroll_amount * scroll_speed  # Solo actualizamos el offset

    def draw(self, screen):
        self.solid_tiles = []  # Reiniciamos los tiles sólidos antes de calcularlos de nuevo

        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile in self.tileset:
                    screen.blit(
                        self.tileset[tile],
                        (
                            x * self.tile_size - self.offset,  # Aplicamos el offset al dibujo
                            HEIGHT - (self.height - y * self.tile_size),
                        ),
                    )

                    # Actualizar la posición del tile sólido en base al offset
                    rect = pygame.Rect(
                        x * self.tile_size - self.offset,  # Aplicar mismo desplazamiento
                        HEIGHT - (self.height - y * self.tile_size),
                        self.tile_size,
                        self.tile_size
                    )
                    self.solid_tiles.append(rect)  # Agregar a la lista de colisiones


    @staticmethod
    def load_tileset(image_path, tile_size, columns=5, rows=5, spacing=16):
        image = pygame.image.load(
            image_path
        ).convert_alpha()  
        tileset = {}

        for y in range(rows):
            for x in range(columns):
                tile = image.subsurface(
                    pygame.Rect(
                        x * (tile_size + spacing),
                        y * (tile_size + spacing),
                        tile_size,
                        tile_size,
                    )
                ).copy() 

                tileset[y * columns + x] = tile 

        return tileset

    def calculate_solid_tiles(self):
        solid_tiles = []
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                if tile != -1:  
                    rect = pygame.Rect(
                        x * self.tile_size,
                        HEIGHT - (self.height - y * self.tile_size),
                        self.tile_size,
                        self.tile_size
                    )
                    solid_tiles.append(rect)
        return solid_tiles

