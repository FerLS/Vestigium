import pygame
import os
from typing import List, Tuple
from managers.resource_manager import ResourceManager
from utils.constants import WIDTH, HEIGHT


class BackgroundLayer:
    """
    Represents a single layer of the background. Handles parallax scrolling
    based on the camera's offset and the layer's speed.
    """

    def __init__(
        self,
        resource_manager: ResourceManager,
        image_name: str,
        assets_path: str,
        speed_x: float = 1.0,
        speed_y: float = 0.0,
    ):
        """
        Initializes a background layer.

        :param resource_manager: The resource manager to load the image.
        :param image_name: The name of the image file for this layer.
        :param assets_path: The path to the folder containing the image.
        :param speed_x: The horizontal scrolling speed of the layer.
        :param speed_y: The vertical scrolling speed of the layer.
        """
        self.resource_manager: ResourceManager = resource_manager
        self.image: pygame.Surface = self.resource_manager.load_image(image_name, assets_path)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.rect: pygame.Rect = self.image.get_rect()
        self.speed_x: float = speed_x
        self.speed_y: float = speed_y

    def draw(self, screen: pygame.Surface, camera_offset: Tuple[float, float]) -> None:
        """
        Draws the background layer on the screen with parallax scrolling.

        :param screen: The pygame.Surface to draw on.
        :param camera_offset: The (x, y) offset of the camera.
        """
        offset_x: int = int(camera_offset[0] * self.speed_x)
        offset_y: int = int(camera_offset[1] * self.speed_y)

        image_width: int = self.rect.width
        image_height: int = self.rect.height

        start_x: int = -(offset_x % image_width)
        start_y: int = -(offset_y % image_height)

        x: int = start_x
        while x < screen.get_width():
            y: int = start_y
            while y < screen.get_height():
                screen.blit(self.image, (x, y))
                y += image_height
            x += image_width


class Background:
    """
    Represents the full background composed of multiple layers.
    Handles the initialization and drawing of all layers with parallax scrolling.
    """

    def __init__(
        self,
        resource_manager: ResourceManager,
        assets_path: str,
        speed_increment: float = 0.2,
        enable_vertical_scroll: bool = False,
    ):
        """
        Initializes the background with multiple layers.

        :param resource_manager: The resource manager to load images.
        :param assets_path: The path to the folder containing background layer images.
        :param speed_increment: The increment in speed for each successive layer.
        :param enable_vertical_scroll: Whether vertical scrolling is enabled.
        """
        self.layers: List[BackgroundLayer] = []
        speed: float = 0.0
        for layer in sorted(os.listdir(assets_path)):  # Ensure layers are loaded in order
            speed += speed_increment
            vertical_speed: float = speed if enable_vertical_scroll else 0.0
            self.layers.append(
                BackgroundLayer(resource_manager, layer, assets_path, speed_x=speed, speed_y=vertical_speed)
            )

    def draw(self, screen: pygame.Surface, camera_offset: Tuple[float, float]) -> None:
        """
        Draws all background layers on the screen.

        :param screen: The pygame.Surface to draw on.
        :param camera_offset: The (x, y) offset of the camera.
        """
        for layer in self.layers:
            layer.draw(screen, camera_offset)
