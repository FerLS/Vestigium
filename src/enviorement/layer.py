import pygame
import pytmx

from utils.constants import SCALE_FACTOR


class Layer:
    def __init__(self, tmx_layer, tilemap):
        self.tmx_layer = tmx_layer
        from .tilemap import Tilemap

        self.tilemap: Tilemap = tilemap
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
                        tile,
                        (
                            self.tilemap.tile_size * SCALE_FACTOR,
                            self.tilemap.tile_size * SCALE_FACTOR,
                        ),
                    )
                    tiles.append((tile, x, y))
        return tiles

    def render_layer_as_image(self):
        """Renderiza toda la capa como una imagen y la guarda en memoria."""
        surface = pygame.Surface(
            (self.tilemap.width * SCALE_FACTOR, self.tilemap.height * SCALE_FACTOR),
            pygame.SRCALPHA,
        ).convert_alpha()

        if isinstance(self.tmx_layer, pytmx.TiledTileLayer):
            for x, y, gid in self.tmx_layer:
                tile = self.tilemap.tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tile = pygame.transform.scale(
                        tile,
                        (
                            self.tilemap.tile_size * SCALE_FACTOR,
                            self.tilemap.tile_size * SCALE_FACTOR,
                        ),
                    )
                    surface.blit(
                        tile,
                        (
                            x * self.tilemap.tile_size * SCALE_FACTOR,
                            y * self.tilemap.tile_size * SCALE_FACTOR,
                        ),
                    )

        return surface

    def get_solid_tiles(self):
        """Obtiene los tiles sólidos si es un TileLayer y debe manejar colisiones."""
        solid_tiles = []
        if isinstance(self.tmx_layer, pytmx.TiledTileLayer):
            for x, y, gid in self.tmx_layer:
                if gid != 0:
                    rect = pygame.Rect(
                        x * self.tilemap.tile_size * SCALE_FACTOR,
                        y * self.tilemap.tile_size * SCALE_FACTOR,
                        self.tilemap.tile_size * SCALE_FACTOR,
                        self.tilemap.tile_size * SCALE_FACTOR,
                    )
                    solid_tiles.append(rect)

        return solid_tiles

    def draw(self, screen, offset_x=0):
        """Dibuja la capa aplicando el desplazamiento"""
        if self.render_as_image and self.image:
            screen.blit(
                self.image, (offset_x * SCALE_FACTOR, 0)
            )  # Aplica desplazamiento escalado
        else:
            for tile, x, y in self.tiles:
                screen.blit(
                    tile,
                    (
                        x * self.tilemap.tile_size * SCALE_FACTOR
                        + offset_x * SCALE_FACTOR,
                        y * self.tilemap.tile_size * SCALE_FACTOR,
                    ),
                )
