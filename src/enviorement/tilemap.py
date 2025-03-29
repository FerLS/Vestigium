import pygame
import pytmx
from typing import Dict, List, Tuple, Union
from utils.constants import SCALE_FACTOR
from .layer import Layer


class Tilemap:
    """
    Represents a tilemap loaded from a TMX file. Handles layers, entities, sprites,
    and collision data for the game world.
    """

    def __init__(self, tmx_file: str):
        """
        Initializes the tilemap.

        :param tmx_file: The path to the TMX file to load.
        """
        self.tmx_data: pytmx.TiledMap = pytmx.load_pygame(tmx_file, pixelalpha=True)
        self.tile_size: int = self.tmx_data.tilewidth
        self.width: int = self.tmx_data.width * self.tile_size
        self.height: int = self.tmx_data.height * self.tile_size
        self.mask: pygame.Mask = pygame.Mask((self.width, self.height))

        self.layers: Dict[str, Layer] = self.load_layers()
        self.sprites: List[Tuple[pygame.sprite.Sprite, int]] = []

    def load_layers(self) -> Dict[str, Layer]:
        """
        Loads all layers from the TMX file.

        :return: A dictionary mapping layer names to `Layer` objects.
        """
        layers = {}
        for tmx_layer in self.tmx_data.layers:
            layers[tmx_layer.name] = Layer(tmx_layer, self)
        return layers

    def load_layer_entities(self, entity: str) -> Dict[str, pytmx.TiledObject]:
        """
        Loads all objects from a specific layer.

        :param entity: The name of the layer to load objects from.
        :return: A dictionary mapping object names to `pytmx.TiledObject` objects.
        """
        entities = {}
        object_layer = self.tmx_data.get_layer_by_name(entity)

        for obj in object_layer:
            entities[obj.name] = obj

        for entity in entities.values():
            entity.x *= SCALE_FACTOR
            entity.y *= SCALE_FACTOR
            entity.width *= SCALE_FACTOR
            entity.height *= SCALE_FACTOR
        return entities

    def load_entity(self, entity: str) -> Union[pytmx.TiledObject, None]:
        """
        Loads a single object by name from the TMX file.

        :param entity: The name of the object to load.
        :return: The `pytmx.TiledObject` if found, otherwise `None`.
        """
        for obj in self.tmx_data.objects:
            if obj.name == entity:
                obj.x *= SCALE_FACTOR
                obj.y *= SCALE_FACTOR
                obj.width *= SCALE_FACTOR
                obj.height *= SCALE_FACTOR
                return obj
        return None

    def insert_sprite(self, sprite: pygame.sprite.Sprite, layer_index: int) -> None:
        """
        Inserts a sprite into the tilemap at a specific layer index.

        :param sprite: The sprite to insert.
        :param layer_index: The index of the layer where the sprite should be drawn.
        """
        self.sprites.append((sprite, layer_index))
        self.sprites.sort(key=lambda x: x[1])  # Sort sprites by layer index

    def draw(self, screen: pygame.Surface, offset: Tuple[int, int] = (0, 0)) -> None:
        """
        Draws all layers and sprites in the correct order.

        :param screen: The pygame.Surface to draw on.
        :param offset: The (x, y) offset for rendering the tilemap.
        """
        sorted_layers = sorted(self.layers.items(), key=lambda x: x[0], reverse=False)
        sprite_index = 0

        # Draw sprites with negative layer indices (behind all layers)
        while sprite_index < len(self.sprites) and self.sprites[sprite_index][1] < 0:
            self.sprites[sprite_index][0].draw(screen, offset)
            sprite_index += 1

        # Draw layers and sprites in their respective order
        for i, (_, layer) in enumerate(sorted_layers):
            layer.draw(screen, offset)
            while sprite_index < len(self.sprites) and self.sprites[sprite_index][1] == i:
                self.sprites[sprite_index][0].draw(screen, offset)
                sprite_index += 1

    def get_collision_rects(self) -> List[pygame.Rect]:
        """
        Retrieves solid collision rectangles from all layers.

        :return: A list of `pygame.Rect` objects representing solid tiles.
        """
        solid_rects = []
        for layer in self.layers.values():
            solid_rects.extend(layer.solid_tiles)
        return solid_rects

    def get_platform_rects(self) -> List[pygame.Rect]:
        """
        Retrieves platform collision rectangles (only collidable from above).

        :return: A list of `pygame.Rect` objects representing platform tiles.
        """
        platform_rects = []
        for layer in self.layers.values():
            platform_rects.extend(layer.platform_tiles)
        return platform_rects

    def get_stairs_rects(self) -> List[pygame.Rect]:
        """
        Retrieves stair collision rectangles.

        :return: A list of `pygame.Rect` objects representing stair tiles.
        """
        stairs_rects = []
        for layer in self.layers.values():
            stairs_rects.extend(layer.stairs_tiles)
        return stairs_rects

    def get_safe_rects(self) -> List[pygame.Rect]:
        """
        Retrieves safe zone rectangles.

        :return: A list of `pygame.Rect` objects representing safe zones.
        """
        safe_rects = []
        for layer in self.layers.values():
            safe_rects.extend(layer.safe_tiles)
        return safe_rects
