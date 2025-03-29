import math
import pygame
import random
from utils.light import CircularLight


class Firefly(pygame.sprite.Sprite):
    """
    Represents a firefly NPC in the game. The firefly moves in different patterns,
    emits light, and blinks periodically.
    """

    def __init__(
        self,
        x: int,
        y: int,
        movement_bounds: pygame.Rect = None,
        movement_type: str = "random",
    ) -> None:
        """
        Initializes the firefly NPC.

        :param x: The initial x-coordinate of the firefly.
        :param y: The initial y-coordinate of the firefly.
        :param movement_bounds: The rectangular bounds within which the firefly can move.
        :param movement_type: The type of movement ('random', 'wave', 'vertical', 'horizontal').
        """
        super().__init__()

        self.RADIUS = 5
        self.radius_variation = 2
        self.blink_interval = 15
        self.current_radius = self.RADIUS

        self.light = CircularLight((x, y), self.RADIUS + 20, use_obstacles=False)
        self.rect = pygame.Rect(x, y, self.RADIUS * 2, self.RADIUS * 2)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_speed = 1.5
        self.acceleration_change = 0.2
        self.movement_bounds = movement_bounds
        self.movement_type = movement_type

        self.start_x = x
        self.start_y = y

        self.blink_timer = 0
        self.blink_up = True

        self.time = 0
        self.speed = random.uniform(8, 10) if y > 500 else random.uniform(2, 4)
        self.wave_amplitude = random.uniform(1, 4) if y > 250 else 6
        self.wave_frequency = random.uniform(0.01, 0.1)

        self.vertical_direction = random.choice([1, -1])
        self.horizontal_direction = random.choice([1, -1])

    def update(self) -> None:
        """
        Updates the firefly's position, blinking state, and light properties.
        """
        self._update_position()
        self._update_blinking()
        self._update_light()

    def _update_position(self) -> None:
        """
        Updates the firefly's position based on its movement type.
        """
        if self.movement_type == "random":
            self._update_random_movement()
        elif self.movement_type == "wave":
            self._move()
        elif self.movement_type == "vertical":
            self._update_vertical_movement()
        elif self.movement_type == "horizontal":
            self._update_horizontal_movement()

    def _update_random_movement(self) -> None:
        """
        Updates the firefly's position for random movement.
        """
        delta = pygame.math.Vector2(
            random.uniform(-self.acceleration_change, self.acceleration_change),
            random.uniform(-self.acceleration_change, self.acceleration_change),
        )
        self.velocity += delta

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.movement_bounds:
            self._handle_bounds_collision()

    def _handle_bounds_collision(self) -> None:
        """
        Handles collision with movement bounds for random movement.
        """
        if not self.movement_bounds.contains(self.rect):
            if self.rect.left < self.movement_bounds.left or self.rect.right > self.movement_bounds.right:
                self.velocity.x *= -1
            if self.rect.top < self.movement_bounds.top or self.rect.bottom > self.movement_bounds.bottom:
                self.velocity.y *= -1
            self.rect.clamp_ip(self.movement_bounds)

    def _update_vertical_movement(self) -> None:
        """
        Updates the firefly's position for vertical movement.
        """
        self.rect.y += 1 * self.vertical_direction
        if abs(self.rect.y - self.start_y) >= 100:
            self.vertical_direction *= -1
        self.time += 1

    def _update_horizontal_movement(self) -> None:
        """
        Updates the firefly's position for horizontal movement.
        """
        self.rect.x += 1 * self.horizontal_direction
        if abs(self.rect.x - self.start_x) >= 100:
            self.horizontal_direction *= -1
        self.time += 1

    def _update_blinking(self) -> None:
        """
        Updates the blinking state of the firefly.
        """
        self.blink_timer += 1
        if self.blink_timer >= self.blink_interval:
            self.blink_up = not self.blink_up
            self.blink_timer = 0

        self.current_radius = self.RADIUS + self.radius_variation if self.blink_up else self.RADIUS

    def _update_light(self) -> None:
        """
        Updates the light properties of the firefly.
        """
        self.light.update(new_position=self.rect.center)
        self.light.change_radius(self.current_radius + 20)

    def _move(self) -> None:
        """
        Moves the firefly in a wave pattern.
        """
        if self.velocity == pygame.math.Vector2(0, 0):
            return

        self.time += 1
        wave_offset = self.wave_amplitude * math.sin(self.time * self.wave_frequency)

        if self.start_x < 500:
            self.rect.x += self.speed
        elif self.start_x > 500:
            self.rect.x -= self.speed

        self.rect.y += wave_offset

        if self.rect.left > 1000 or self.rect.right < 0:
            self.reset()

    def reset(self, reason: str = "touched_bounds", delay: bool = False) -> None:
        """
        Resets the firefly's position and properties.

        :param reason: The reason for the reset ('touched_bounds' or 'life_decreased').
        :param delay: Whether to delay the reset.
        """
        if reason == "touched_bounds":
            self.rect.x = random.choice([0, 1000])
            if self.start_y <= 250:
                self.rect.y = random.randint(100, 250)
            else:
                self.rect.y = random.randint(250, 700)

        elif reason == "life_decreased" and not delay:
            self.rect.x = self.start_x
            self.rect.y = self.start_y

        self.speed = random.uniform(8, 10) if self.rect.y > 500 else random.uniform(2, 4)
        self.wave_amplitude = random.uniform(1, 4) if self.rect.y > 250 else 6
        self.wave_frequency = random.uniform(0.01, 0.1)

        if not delay:
            self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            self.time = 0
            self.light.update(new_position=self.rect.center)

    def stop(self) -> None:
        """
        Stops the firefly's movement and updates its light position.
        """
        self.velocity = pygame.math.Vector2(0, 0)
        self.light.update(new_position=self.rect.center)

    def draw(self, screen: pygame.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        """
        Draws the firefly and its light on the screen.

        :param screen: The pygame.Surface to draw on.
        :param offset: The camera offset for rendering.
        """
        offset_x, offset_y = offset
        image = pygame.Surface((self.current_radius * 3, self.current_radius * 3), pygame.SRCALPHA)
        pygame.draw.circle(image, (255, 255, 100), (self.current_radius, self.current_radius), self.current_radius)
        draw_pos = self.rect.centerx - self.current_radius - offset_x, self.rect.centery - self.current_radius - offset_y
        screen.blit(image, draw_pos)
        self.light.draw(screen, offset)
