import pygame
from abc import ABC, abstractmethod
from utils.light import CircularLight
from managers.resource_manager import ResourceManager
from utils.images import extract_frames
from utils.constants import SCALE_FACTOR


class FloatingEntity(pygame.sprite.Sprite, ABC):
    """
    Represents a generic floating entity in the game. This class serves as a base class
    for floating NPCs, handling movement, animation, and optional light emission.
    """

    def __init__(
        self,
        x: int,
        y: int,
        sprite_sheet_path: str,
        frame_width: int,
        frame_height: int,
        frame_count: int,
        move_distance: int,
        speed: float,
        initial_direction: int = 1,
        scale: float = SCALE_FACTOR,
        flip_on_reverse: bool = False,
        move_axis: str = "vertical",
        draw_light: bool = True,
        light_radius: int = 10 * SCALE_FACTOR,
    ) -> None:
        """
        Initializes the floating entity.

        :param x: The initial x-coordinate of the entity.
        :param y: The initial y-coordinate of the entity.
        :param sprite_sheet_path: Path to the sprite sheet for animations.
        :param frame_width: Width of each frame in the sprite sheet.
        :param frame_height: Height of each frame in the sprite sheet.
        :param frame_count: Number of frames in the sprite sheet.
        :param move_distance: Maximum distance the entity can move along its axis.
        :param speed: Speed of the entity's movement.
        :param initial_direction: Initial direction of movement (1 for forward, -1 for backward).
        :param scale: Scale factor for the entity's sprite.
        :param flip_on_reverse: Whether to flip the sprite when reversing direction.
        :param move_axis: Axis of movement ('vertical' or 'horizontal').
        :param draw_light: Whether the entity emits light.
        :param light_radius: Radius of the emitted light.
        """
        super().__init__()
        # Calls the parent class constructor to initialize the entity's properties.

        self.resource_manager = ResourceManager()
        sheet = self.resource_manager.load_image(sprite_sheet_path, "assets\\images")
        self.animations = extract_frames(sheet, 0, 0, frame_width, frame_height, frame_count, scale)

        self.frame_index = 0
        self.animation_speed = 0.2
        self.animation_timer = 0
        self.flipped = False

        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_x = float(x)
        self.pos_y = float(y)
        self.start_x = x
        self.start_y = y
        self.speed = speed
        self.move_distance = move_distance
        self.direction = initial_direction
        self.move_axis = move_axis
        self.flip_on_reverse = flip_on_reverse

        self.draw_light_flag = draw_light
        self.light = CircularLight(self.rect.center, light_radius, use_obstacles=False)

    def update(self, dt: float) -> None:
        """
        Updates the entity's position, light, and animation.

        :param dt: The time delta since the last frame.
        """
        if self.move_axis == "vertical":
            self.pos_y += self.speed * self.direction
            self.rect.y = int(self.pos_y)
            if abs(self.pos_y - self.start_y) >= self.move_distance:
                self.direction *= -1
                if self.flip_on_reverse:
                    self.flipped = not self.flipped

        elif self.move_axis == "horizontal":
            self.pos_x += self.speed * self.direction
            self.rect.x = int(self.pos_x)
            if abs(self.pos_x - self.start_x) >= self.move_distance:
                self.direction *= -1
                if self.flip_on_reverse:
                    self.flipped = not self.flipped


        self.light.update(new_position=self.rect.center)

        self.update_animation(dt)

    def update_animation(self, dt: float) -> None:
        """
        Updates the entity's animation based on the elapsed time.

        :param dt: The time delta since the last frame.
        """
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations)
            frame = self.animations[self.frame_index]
            if self.flip_on_reverse and self.move_axis == "vertical":
                self.image = pygame.transform.flip(frame, False, self.flipped)
            else:
                self.image = frame

    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        """
        Draws the entity and its light on the screen.

        :param screen: The pygame.Surface to draw on.
        :param offset: The camera offset for rendering.
        """
        offset_x, offset_y = offset
        if self.draw_light_flag:
            self.light.draw(screen, offset)
        draw_pos = self.rect.x - offset_x, self.rect.y - offset_y
        screen.blit(self.image, draw_pos)
