import pygame
import pytmx


class Layer:
    def __init__(self, tmx_layer, tilemap):
        self.tmx_layer = tmx_layer
        self.tilemap = tilemap
        self.render_as_image = self.check_if_render_as_image()
        self.solid_tiles = []

        if self.render_as_image:
            self.image = self.render_layer_as_image()
        else:
            self.tiles = self.load_tiles()
            self.solid_tiles = self.get_solid_tiles()

    def check_if_render_as_image(self):
        """Verifica si la capa tiene una propiedad para renderizarse como imagen."""
        return self.tmx_layer.properties.get("render_as_image", False)

    def load_tiles(self):
        """Carga los tiles si la capa es un TileLayer."""
        tiles = []
        if isinstance(self.tmx_layer, pytmx.TiledTileLayer):
            for x, y, gid in self.tmx_layer:
                tile = self.tilemap.tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile = pygame.transform.scale(
                        tile, (self.tilemap.tile_size, self.tilemap.tile_size)
                    )
                    tiles.append((tile, x, y))
        return tiles

    def render_layer_as_image(self):
        """Renderiza toda la capa como una imagen y la guarda en memoria."""
        surface = pygame.Surface(
            (self.tilemap.width, self.tilemap.height), pygame.SRCALPHA
        )

        if isinstance(self.tmx_layer, pytmx.TiledTileLayer):
            for x, y, gid in self.tmx_layer:
                tile = self.tilemap.tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile = pygame.transform.scale(
                        tile, (self.tilemap.tile_size, self.tilemap.tile_size)
                    )
                    surface.blit(
                        tile, (x * self.tilemap.tile_size, y * self.tilemap.tile_size)
                    )

        return surface

    def get_solid_tiles(self):
        """Obtiene los tiles sólidos si es un TileLayer y debe manejar colisiones."""
        solid_tiles = []
        if isinstance(self.tmx_layer, pytmx.TiledTileLayer):
            for x, y, id in self.tmx_layer:

                if id != 0:  # Suponiendo que 0 es espacio vacío

                    rect = pygame.Rect(
                        x * self.tilemap.tile_size,
                        y * self.tilemap.tile_size,
                        self.tilemap.tile_size,
                        self.tilemap.tile_size,
                    )
                    solid_tiles.append(rect)

        return solid_tiles

    def draw(self, screen):
        """Dibuja la capa en pantalla."""
        if self.render_as_image and self.image:
            screen.blit(self.image, (0, 0))
        else:
            for tile, x, y in self.tiles:
                screen.blit(
                    tile,
                    (
                        x * self.tilemap.tile_size,
                        y * self.tilemap.tile_size,
                    ),
                )
