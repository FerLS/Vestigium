import pygame
from managers.resource_manager import ResourceManager
import math
from utils.constants import SCALE_FACTOR


class Lantern(pygame.sprite.Sprite):
    """
    Represents a lantern object in the game. The lantern moves along a predefined path,
    interacts with the player, and emits a light effect.
    """

    def __init__(
        self,
        position: tuple[int, int],
        path: list[tuple[int, int]],
        scale: int = 4,
        speed: float = 2,
    ) -> None:
        """
        Initializes the lantern object.

        :param position: The initial position of the lantern.
        :param path: A list of points defining the lantern's movement path.
        :param scale: The scale factor for the lantern and light images.
        :param speed: The speed at which the lantern moves along its path.
        """
        super().__init__()
        self.speed: float = speed
        self.radius: float = 190 * SCALE_FACTOR 
        self.angle: float = 0  # Inclination angle for rotation
        self.float_offset: float = 0  # Vertical offset for floating effect
        self.float_speed: float = 0.1  # Speed of the floating effect
        self.float_amplitude: float = 20  # Amplitude of the floating effect
        self.time: float = 0  # Time counter for floating effect

        # Load the lantern image
        original_image = ResourceManager().load_image("Lantern.png", "assets/images")
        width, height = original_image.get_size()
        self.original_image: pygame.Surface = pygame.transform.scale(
            original_image, (width * scale, height * scale)
        )
        self.image: pygame.Surface = self.original_image.copy()

        # Load the light image
        light_image = ResourceManager().load_image("Light.png", "assets/images")
        light_width, light_height = light_image.get_size()
        self.light_image: pygame.Surface = pygame.transform.scale(
            light_image, (light_width * scale, light_height * scale)
        )

        self.rect: pygame.Rect = self.image.get_rect(center=position)
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(position)

        self.path: list[pygame.math.Vector2] = [pygame.math.Vector2(p) for p in path]

        self.current_point_index: int = 0
        self.target: pygame.math.Vector2 = self.path[self.current_point_index]

    def update(
        self, player: pygame.sprite.Sprite, tilemap: object, offset: tuple[int, int] = (0, 0)
    ) -> None:
        """
        Updates the lantern's position, floating effect, and interactions with the player.

        :param player: The player object to check for collisions.
        :param tilemap: The tilemap object to check for safe zones.
        :param offset: The camera offset for rendering.
        """
        # Calculate the vector and distance to the target point
        vector_to_target: pygame.math.Vector2 = self.target - self.pos
        distance: float = vector_to_target.length()

        # Move to the next point if close enough
        if distance <= self.speed:
            self.pos = self.target
            self.current_point_index = (self.current_point_index + 1) % len(self.path)
            self.target = self.path[self.current_point_index]
        elif distance > 0:
            # Normalize the direction and move towards the target
            direction: pygame.math.Vector2 = vector_to_target.normalize()
            self.pos += direction * min(self.speed, distance)

            # Smoothly adjust the rotation angle based on horizontal movement
            target_angle: float = direction.x * -10
            self.angle += (target_angle - self.angle) * 0.1

        # Apply the floating effect
        self.time += self.float_speed
        self.float_offset = math.sin(self.time) * self.float_amplitude

        # Rotate the lantern image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.center = (
            round(self.pos.x - offset[0]),
            round(self.pos.y - offset[1] + self.float_offset),
        )

        # Check for collision with the player
        distance_to_player: float = self.pos.distance_to((player.rect.x, player.rect.y))
        if distance_to_player <= self.radius and not player.is_dying and not player.dead:
            safe_tiles = tilemap.get_safe_rects()
            player_in_safe_zone = any(
                player.rect.colliderect(safe_tile) for safe_tile in safe_tiles
            )
            if not player_in_safe_zone:
                player.dying()

    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        """
        Draws the lantern and its light effect on the screen.

        :param screen: The pygame.Surface to draw on.
        :param offset: The camera offset for rendering.
        """
        light_pos: tuple[float, float] = (
            self.pos.x - self.light_image.get_width() // 2 - offset[0],
            self.pos.y
            - self.light_image.get_height() // 2
            - offset[1]
            + self.float_offset,
        )

        light_surface: pygame.Surface = self.light_image.copy()
        light_surface.set_alpha(128)
        screen.blit(light_surface, light_pos)

        screen.blit(self.image, (self.rect.x, self.rect.y))
