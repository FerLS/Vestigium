import pygame
from utils.constants import SCALE_FACTOR
from managers.resource_manager import ResourceManager
from managers.sound_manager import SoundManager


class Lock(pygame.sprite.Sprite):
    """
    Represents a lock object in the game. The lock can play an animation when a key interacts with it.
    """

    def __init__(self, x: int, y: int, screen_width: int) -> None:
        """
        Initializes the lock object.

        :param x: The x-coordinate of the lock's position (not used directly, center is used instead).
        :param y: The y-coordinate of the lock's position.
        :param screen_width: The width of the screen, used to center the lock horizontally.
        """
        super().__init__()
        resource_manager = ResourceManager()

        self.sheet: pygame.Surface = resource_manager.load_image("lock.png", "assets/images")

        self.frames: list[pygame.Surface] = self._load_frames()

        self.image: pygame.Surface = self.frames[0]
        self.image = pygame.transform.scale(
            self.image,
            (self.frames[0].get_width() * SCALE_FACTOR, self.frames[0].get_height() * SCALE_FACTOR),
        )

        self.rect: pygame.Rect = self.image.get_rect(center=(screen_width // 2, y))
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)

        self.animation_index: int = 0
        self.animation_speed: float = 0.1 
        self.animation_timer: float = 0
        self.is_playing_animation: bool = False
        self.original_center: tuple[int, int] = (screen_width // 2, y)
        self.end: bool = False 

        self.sound_manager: SoundManager = SoundManager()

    def _load_frames(self) -> list[pygame.Surface]:
        """
        Loads the animation frames from the sprite sheet.

        :return: A list of scaled pygame.Surface objects representing the animation frames.
        """
        frame_width: int = self.sheet.get_width() // 9
        frame_height: int = self.sheet.get_height()
        frames: list[pygame.Surface] = []

        # Extract and scale each frame
        for i in range(9):
            frame = self.sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(
                frame, (frame_width * SCALE_FACTOR, frame_height * SCALE_FACTOR)
            )
            frames.append(frame)
        return frames

    def play_animation(self) -> None:
        """
        Starts the lock's animation and plays the associated sound.
        """
        self.sound_manager.play_sound("iron-gate.ogg", "assets/sounds", 0.5)
        self.is_playing_animation = True
        self.animation_index = 0
        self.animation_timer = 0

    def update(self, dt: float, key: pygame.sprite.Sprite) -> None:
        """
        Updates the lock's animation and checks for interaction with the key.

        :param dt: The time delta since the last frame.
        :param key: The key object to check for collision.
        """
        # Update the animation if it's playing
        if self.is_playing_animation:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_index += 1

                # Check if the animation has finished
                if self.animation_index >= len(self.frames):
                    self.animation_index = len(self.frames) - 1
                    self.end = True 

                # Update the image, rectangle, and mask
                self.image = self.frames[self.animation_index]
                self.image = pygame.transform.scale(
                    self.image,
                    (self.frames[0].get_width() * SCALE_FACTOR, self.frames[0].get_height() * SCALE_FACTOR),
                )
                self.rect = self.image.get_rect(center=self.original_center)
                self.mask = pygame.mask.from_surface(self.image)

        # Check for collision with the key to start the animation
        if not self.is_playing_animation and pygame.sprite.collide_mask(self, key):
            self.play_animation()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the lock on the screen.

        :param screen: The pygame.Surface to draw on.
        """
        screen.blit(self.image, self.rect.topleft)
