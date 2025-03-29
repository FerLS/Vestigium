import pygame
import os
import random

from managers.resource_manager import ResourceManager
from utils.constants import MovementDirections, MovementType, SCALE_FACTOR
from utils.light import CircularLight


class Gravedigger(pygame.sprite.Sprite):
    """
    Represents a gravedigger NPC in the game. The gravedigger can walk within a defined range,
    emit light, and interact with the player.
    """

    def __init__(self, x: int, y: int, tilemap: object) -> None:
        """
        Initializes the gravedigger NPC.

        :param x: The initial x-coordinate of the gravedigger.
        :param y: The initial y-coordinate of the gravedigger.
        :param tilemap: The tilemap object for collision detection.
        """
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager: ResourceManager = ResourceManager()

        # Load and scale sprite sheets
        self.walk_sheet: pygame.Surface = self.scale_image(
            self.resource_manager.load_image("enemy-walk.png", "assets\\enemy")
        )
        self.idle_sheet: pygame.Surface = self.scale_image(
            self.resource_manager.load_image("enemy-idle.png", "assets\\enemy")
        )

        # Tilemap and rectangle setup
        self.tilemap = tilemap
        self.rect: pygame.Rect = pygame.Rect((0, 0), (42 * SCALE_FACTOR, 47 * SCALE_FACTOR))
        self.image: pygame.Surface = self.idle_sheet.subsurface(self.rect)
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)

        # Position and movement properties
        self.initial_position: tuple[int, int] = (x, y)
        self.rect.x = x
        self.rect.y = y
        self.velocity: int = 1
        self.range: tuple[int, int] = (200, 500)
        self.state: MovementType = MovementType.IDLE
        self.movement: MovementDirections = MovementDirections.LEFT
        self.time: int = random.randint(60, 120)

        # Animation properties
        self.walk_frames: list[pygame.Surface] = self.load_frames(self.walk_sheet)
        self.idle_frames: list[pygame.Surface] = self.load_frames(self.idle_sheet)
        self.imagePosture: int = 0
        self.animationSpeed: int = 5
        self.animationCounter: int = 0

        # Collision and light properties
        self.collided: bool = False
        self.offset_x: int = 0
        self.light: CircularLight = CircularLight(
            (self.rect.centerx - 20, self.rect.centery), radius=15
        )

    def scale_image(self, image: pygame.Surface) -> pygame.Surface:
        """
        Scales the given image by the defined scale factor.

        :param image: The pygame.Surface to scale.
        :return: The scaled pygame.Surface.
        """
        width, height = image.get_width(), image.get_height()
        return pygame.transform.scale(
            image, (width * SCALE_FACTOR, height * SCALE_FACTOR)
        )

    def load_frames(self, sheet: pygame.Surface) -> list[pygame.Surface]:
        """
        Loads animation frames from a sprite sheet.

        :param sheet: The sprite sheet to extract frames from.
        :return: A list of pygame.Surface objects representing the frames.
        """
        frames = []
        frame_width = 42 * SCALE_FACTOR
        frame_height = 47 * SCALE_FACTOR
        num_frames = sheet.get_width() // frame_width
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def animate(self) -> None:
        """
        Updates the gravedigger's animation based on its current state.
        """
        self.animationCounter += 1
        if self.animationCounter >= self.animationSpeed:
            self.animationCounter = 0
            self.imagePosture = (self.imagePosture + 1) % len(
                self.walk_frames
                if self.state == MovementType.WALK
                else self.idle_frames
            )
        if self.state == MovementType.WALK:
            self.image = self.walk_frames[self.imagePosture]
        else:
            self.image = self.idle_frames[self.imagePosture]

    def move(self) -> None:
        """
        Moves the gravedigger within its defined range.
        """
        if self.state == MovementType.WALK:
            if self.movement == MovementDirections.LEFT:
                self.rect.x -= self.velocity
            else:
                self.rect.x += self.velocity

            if self.rect.x <= self.initial_position[0] + self.range[0]:
                self.movement = MovementDirections.RIGHT
            elif self.rect.x >= self.initial_position[0] + self.range[1]:
                self.movement = MovementDirections.LEFT

            self.time -= 1
            if self.time <= 0:
                self.movement = random.choice(
                    [MovementDirections.LEFT, MovementDirections.RIGHT]
                )
                self.time = random.randint(60, 120)

    def collide(self, player: pygame.sprite.Sprite) -> None:
        """
        Checks for collision with the player and triggers the player's death if collided.

        :param player: The player object to check for collision.
        """
        if self.mask.overlap(
            player.mask, (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        ) and not player.is_dying and not player.dead:
            player.dying()

    def stop(self) -> None:
        """
        Stops the gravedigger's movement and sets it to idle state.
        """
        self.state = MovementType.IDLE
        self.collided = True

    def start(self, player: pygame.sprite.Sprite) -> None:
        """
        Starts the gravedigger's movement if the player is within range.

        :param player: The player object to check the distance.
        """
        if not self.collided:
            distance = abs(self.rect.x - player.rect.x)
            if distance < 300:
                self.state = MovementType.WALK

    def update(self, player: pygame.sprite.Sprite) -> None:
        """
        Updates the gravedigger's state, movement, animation, and light.

        :param player: The player object to interact with.
        """
        self.start(player)
        self.collide(player)
        self.move()
        self.animate()

        # Update the light's position
        light_offset = -25 if self.movement == MovementDirections.LEFT else 25
        self.light.update(
            new_position=(self.rect.centerx + light_offset, self.rect.centery + 15)
        )

    def draw(self, screen: pygame.Surface, camera_scroll: tuple[int, int]) -> None:
        """
        Draws the gravedigger and its light on the screen.

        :param screen: The pygame.Surface to draw on.
        :param camera_scroll: The camera offset for rendering.
        """
        img = self.image

        if self.movement == MovementDirections.LEFT:
            img = pygame.transform.flip(img, 1, 0)

        offset_x, offset_y = camera_scroll
        screen.blit(img, (self.rect.x - offset_x, self.rect.y - offset_y))

        # Draw the light
        self.light.draw(screen, offset=camera_scroll)
