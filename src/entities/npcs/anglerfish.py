import pygame
from utils.light import ConeLight
from utils.constants import SCALE_FACTOR
from utils.images import extract_frames
from managers.resource_manager import ResourceManager


class Anglerfish(pygame.sprite.Sprite):
    """
    Represents an anglerfish NPC in the game. The anglerfish can follow the player,
    change its speed, and emit a cone-shaped light.
    """

    def __init__(
        self,
        x: int,
        y: int,
        slow_speed: float = 1,
        fast_speed: float = 1000000,
        switch_speed_time: int = 5000,
        light_obstacles: list[pygame.Rect] = None,
    ) -> None:
        """
        Initializes the anglerfish NPC.

        :param x: The initial x-coordinate of the anglerfish.
        :param y: The initial y-coordinate of the anglerfish.
        :param slow_speed: The slow movement speed of the anglerfish.
        :param fast_speed: The fast movement speed of the anglerfish.
        :param switch_speed_time: The time (in milliseconds) before switching to fast speed.
        :param light_obstacles: A list of obstacles that block the light.
        """
        super().__init__()
        # Calls the parent class constructor to initialize the anglerfish's properties.

        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image("anglerfish_spritesheet.png", "assets\\images")
        self.animations = extract_frames(sheet, 0, 0, 32, 32, 4, SCALE_FACTOR * 3)

        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.flipped = False

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.prev_x = self.rect.x

        self.slow_speed = slow_speed
        self.fast_speed = fast_speed
        self.current_speed = self.slow_speed

        self.switch_speed_time = switch_speed_time
        self.spawn_time = pygame.time.get_ticks()

        self.light = ConeLight(
            (self.rect.topright[0] - 40, self.rect.topright[1] + 35),
            pygame.Vector2(1, 0),
            segments=10,
            angle=40,
            distance=300,
        )
        self.light_obstacles = light_obstacles

    def change_speed(self) -> None:
        """
        Changes the anglerfish's speed after a certain amount of time.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time >= self.switch_speed_time:
            self.current_speed = self.fast_speed

    def follow_player(self, player_position: tuple[int, int]) -> None:
        """
        Makes the anglerfish follow the player's position.

        :param player_position: The (x, y) position of the player.
        """
        if player_position:
            player_x, player_y = player_position

            if self.rect.x < player_x:
                self.rect.x += self.current_speed
                if self.rect.x > player_x:
                    self.rect.x = player_x
            elif self.rect.x > player_x:
                self.rect.x -= self.current_speed
                if self.rect.x < player_x:
                    self.rect.x = player_x

            follow_strength = 0.025
            self.rect.y += int((player_y - self.rect.y) * follow_strength)

    def update(self, dt: float, player_position: tuple[int, int] = None) -> None:
        """
        Updates the anglerfish's animation, light, speed, and position.

        :param dt: The time delta since the last frame.
        :param player_position: The (x, y) position of the player.
        """
        self.update_animation(dt)
        self.light.update(new_position=self.update_light_and_get_position(), obstacles=self.light_obstacles)
        self.change_speed()
        self.follow_player(player_position)

    def update_light_and_get_position(self) -> tuple[int, int]:
        """
        Updates the light's position and direction based on the anglerfish's orientation.

        :return: The new position of the light.
        """
        if self.flipped:
            self.light.direction = pygame.Vector2(-1, 0)
            new_light_position = (self.rect.topleft[0] + 40, self.rect.topleft[1] + 35)
        else:
            self.light.direction = pygame.Vector2(1, 0)
            new_light_position = (self.rect.topright[0] - 40, self.rect.topright[1] + 35)
        return new_light_position

    def update_animation(self, dt: float) -> None:
        """
        Updates the anglerfish's animation based on its movement and elapsed time.

        :param dt: The time delta since the last frame.
        """
        if self.rect.x > self.prev_x:
            self.flipped = False
        elif self.rect.x < self.prev_x:
            self.flipped = True

        self.prev_x = self.rect.x

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            new_frame = self.animations[self.frame_index]
            self.image = pygame.transform.flip(new_frame, True, False) if self.flipped else new_frame

    def draw(self, screen: pygame.Surface, camera_offset: tuple[int, int] = (0, 0)) -> None:
        """
        Draws the anglerfish and its light on the screen.

        :param screen: The pygame.Surface to draw on.
        :param camera_offset: The camera offset for rendering.
        """
        offset_x, offset_y = camera_offset
        self.light.draw(screen, camera_offset)
        draw_pos = (self.rect.x - offset_x, self.rect.y - offset_y)
        screen.blit(self.image, draw_pos)

        # Uncomment the following lines to debug the anglerfish's rectangle
        # debug_platform_rect = self.rect.move(-offset_x, -offset_y)
        # pygame.draw.rect(screen, (0, 255, 0), debug_platform_rect, 1)



