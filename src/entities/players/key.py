import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN
from utils.constants import WIDTH, HEIGHT, ACC, FRIC
from managers.resource_manager import ResourceManager

vec = pygame.math.Vector2

class Key(pygame.sprite.Sprite):
    """
    Represents the key entity in the game. The key can move in response to player input
    and interacts with other game objects, such as locks.
    """

    def __init__(self) -> None:
        """
        Initializes the key entity, including its image, position, velocity, and acceleration.
        """
        super().__init__()
        resource_manager = ResourceManager()
        self.image: pygame.Surface = resource_manager.load_image("key.png", "assets/images")
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * 0.3), int(self.image.get_height() * 0.3))
        )
        self.rect: pygame.Rect = self.image.get_rect()
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)
        self.pos: vec = vec((WIDTH // 2, 700))  # Initial position
        self.vel: vec = vec(0, 0)  # Velocity
        self.acc: vec = vec(0, 0)  # Acceleration
        self.player_position: vec = vec(0, 0)  # Tracks the player's position
        self.dead: bool = False  # Indicates if the key is inactive

    def update(self, lock: pygame.sprite.Sprite = None, ammount: int = None) -> None:
        """
        Updates the key's position and handles collisions with a lock or other conditions.

        :param lock: The lock object to check for collisions.
        :param ammount: A value to determine if the key should stop moving.
        """
        if (lock and pygame.sprite.collide_mask(self, lock)) or ammount == 0:
            self.stop()
            return

        self.acc = vec(0, 0)  # Reset acceleration

        # Handle player input
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        if pressed_keys[K_UP]:
            self.acc.y = -ACC
        if pressed_keys[K_DOWN]:
            self.acc.y = ACC

        # Apply friction
        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC

        # Update velocity and position
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Save the player's position
        self.player_position = self.pos.copy()

        # Keep the key within screen boundaries
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > HEIGHT - 100:
            self.pos.y = HEIGHT - 100
        if self.pos.y < 200:
            self.pos.y = 200

        # Update the rectangle's position
        self.rect.center = self.pos

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the key on the screen.

        :param screen: The pygame.Surface to draw on.
        """
        screen.blit(self.image, self.rect)

    def reset(self) -> None:
        """
        Resets the key's position to its initial state and stops its movement.
        """
        self.pos = vec((WIDTH // 2, 700))
        self.stop()

    def stop(self) -> None:
        """
        Stops the key's movement by resetting its velocity and acceleration.
        """
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)