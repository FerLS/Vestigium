import pygame
import pytmx
from typing import List, Tuple, Union
from utils.constants import SCALE_FACTOR


class Layer:
    """
    Represents a single layer in a tilemap. Handles rendering, loading tiles,
    and managing different types of tiles (e.g., solid, platform, stairs, safe zones).
    """

    def __init__(self, tmx_layer: Union[pytmx.TiledTileLayer, pytmx.TiledObjectGroup], tilemap):
        """
        Initializes the layer.

        :param tmx_layer: The Tiled layer (either a TileLayer or ObjectGroup) from the TMX file.
        :param tilemap: The Tilemap object that owns this layer.
        """
        self.tmx_layer: Union[pytmx.TiledTileLayer, pytmx.TiledObjectGroup] = tmx_layer
        self.tilemap = tilemap

        self.solid_tiles: List[pygame.Rect] = []
        self.platform_tiles: List[pygame.Rect] = []
        self.stairs_tiles: List[pygame.Rect] = []
        self.safe_tiles: List[pygame.Rect] = []

        self.render_as_image: bool = self.tmx_layer.properties.get("render_as_image", False)

        if self.render_as_image:
            self.image: pygame.Surface = self.render_layer_as_image()
        else:
            self.tiles: List[Tuple[pygame.Surface, int, int]] = self.load_tiles()

            # Load tiles based on layer type
            if self.tmx_layer.properties.get("platform_layer", False):
                self.platform_tiles = self.get_platform_objects()
            elif self.tmx_layer.properties.get("stairs_layer", False):
                self.stairs_tiles = self.get_solid_tiles()
            elif self.tmx_layer.properties.get("safe_zone", False):
                self.safe_tiles = self.get_solid_tiles()
            else:
                self.solid_tiles = self.get_solid_tiles()

    def load_tiles(self) -> List[Tuple[pygame.Surface, int, int]]:
        """
        Loads tiles if the layer is a TiledTileLayer.

        :return: A list of tuples containing the tile surface and its (x, y) position.
        """
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

    def render_layer_as_image(self) -> pygame.Surface:
        """
        Renders the entire layer as a single image and stores it in memory.

        :return: A pygame.Surface containing the rendered layer.
        """
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

    def get_platform_objects(self) -> List[pygame.Rect]:
        """
        Retrieves platform objects as rectangles.

        :return: A list of pygame.Rect objects representing platform objects.
        """
        platform_objects = []
        if isinstance(self.tmx_layer, pytmx.TiledObjectGroup):
            for obj in self.tmx_layer:
                rect = pygame.Rect(
                    obj.x * SCALE_FACTOR,
                    obj.y * SCALE_FACTOR,
                    obj.width * SCALE_FACTOR,
                    obj.height * SCALE_FACTOR,
                )
                platform_objects.append(rect)
        return platform_objects

    def get_solid_tiles(self) -> List[pygame.Rect]:
        """
        Retrieves solid tiles as rectangles if the layer is a TiledTileLayer.

        :return: A list of pygame.Rect objects representing solid tiles.
        """
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

    def draw(self, screen: pygame.Surface, offset: Tuple[int, int] = (0, 0)) -> None:
        """
        Draws the layer on the screen with the given offset.

        :param screen: The pygame.Surface to draw on.
        :param offset: The (x, y) offset for rendering the layer.
        """
        offset_x, offset_y = offset

        if self.render_as_image and hasattr(self, "image"):
            screen.blit(self.image, (-offset_x, -offset_y))
        else:
            for tile, x, y in self.tiles:
                screen.blit(
                    tile,
                    (
                        x * self.tilemap.tile_size * SCALE_FACTOR - offset_x,
                        y * self.tilemap.tile_size * SCALE_FACTOR - offset_y,
                    ),
                )
