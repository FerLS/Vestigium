import pygame
from managers.resource_manager import ResourceManager
from utils.light import CircularLight
from utils.images import extract_frames
from utils.constants import WIDTH, HEIGHT, SCALE_FACTOR


class Mushroom(pygame.sprite.Sprite):
    """
    Represents a glowing mushroom NPC in the game. The mushroom emits light,
    bounces with an animation, and provides an invisible platform for interaction.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes the mushroom NPC.

        :param x: The x-coordinate of the mushroom's position.
        :param y: The y-coordinate of the mushroom's position.
        """
        super().__init__()
        self.resource_manager: ResourceManager = ResourceManager()

        # Load mushroom animations
        sheet: pygame.Surface = self.resource_manager.load_image("mushrooms.png", "assets/images")
        self.animations: list[pygame.Surface] = extract_frames(sheet, 0, 24, 24, 24, 12, SCALE_FACTOR * 2)
        self.image: pygame.Surface = self.animations[0]
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))

        # Invisible platform for interaction
        platform_width = 60
        platform_height = 30
        platform_x = self.rect.centerx - 20
        platform_y = self.rect.centery - 30
        self.platform_rect: pygame.Rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)

        # Light properties
        self.light_radius: int = 0
        self.light: CircularLight = CircularLight(
            self.platform_rect.center, self.light_radius, segments=275, use_obstacles=False
        )
        self.glow: bool = False

        # Bounce animation properties
        self.bounce: bool = False
        self.bounce_index: int = 0
        self.bounce_timer: int = 0
        self.bounce_speed: int = 10

        # Frame counter for light animation
        self.frame_counter: int = 0
        self.light_direction: int = 1

    def manage_light(self) -> None:
        """
        Manages the glowing light effect of the mushroom.
        """
        # Activate glowing
        if self.glow and self.frame_counter % 2 == 0:
            self.light_radius += 1 * self.light_direction
            self.light.change_radius(self.light_radius)
            # Stop glowing
            if self.light_radius == 40:
                self.light_direction = -1
            # Continue glowing
            elif self.light_radius == 0:
                if self.light_direction < 0:
                    self.glow = False
                self.light_direction = 1

    def update_animation(self) -> None:
        """
        Updates the bounce animation of the mushroom.
        """
        if self.bounce:
            self.bounce_timer += 1
            if self.bounce_timer >= self.bounce_speed:
                self.bounce_timer = 0
                self.bounce_index += 1
                if self.bounce_index >= len(self.animations):
                    self.bounce_index = 0
                    self.bounce = False
                self.image = self.animations[self.bounce_index]

    def update(self) -> None:
        """
        Updates the mushroom's light, animation, and frame counter.
        """
        self.light.update(new_position=self.platform_rect.center)
        self.manage_light()
        self.update_animation()
        self.frame_counter += 1

    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        """
        Draws the mushroom on the screen.

        :param screen: The pygame.Surface to draw on.
        :param offset: The camera offset for rendering.
        """
        offset_x, offset_y = offset
        screen.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
