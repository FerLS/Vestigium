import pygame
from managers.resource_manager import ResourceManager
from managers.sound_manager import SoundManager


class Lifes:
    """
    Represents the player's life system in the game. Displays hearts on the screen
    to indicate the remaining lives and handles animations and sounds when lives are lost.
    """

    def __init__(self) -> None:
        """
        Initializes the life system, including the heart image, animation frames,
        and sound effects.
        """
        self.resource_manager: ResourceManager = ResourceManager()
        self.sound_manager: SoundManager = SoundManager()

        # Number of lives
        self.ammount: int = 3

        # Load the static heart image
        self.heart_image: pygame.Surface = self.resource_manager.load_image("heart.png", "assets/life")
        self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))

        # Load the animated heart sprite sheet
        self.animation_sheet: pygame.Surface = self.resource_manager.load_image("heart_animated_1.png", "assets/life")
        self.frame_width: int = self.animation_sheet.get_width() // 5  # 5 frames in the sprite sheet
        self.frame_height: int = self.animation_sheet.get_height()

        # Animation properties
        self.current_frame: int = 0
        self.animation_timer: int = 0
        self.animation_duration: float = 0.1
        self.animating: bool = False

        # Preload and scale animation frames
        self.scaled_frames: list[pygame.Surface] = [
            pygame.transform.scale(
                self.animation_sheet.subsurface(
                    pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
                ),
                (40, 40),
            )
            for i in range(5)
        ]

    def decrease(self) -> None:
        """
        Decreases the number of lives by one. Starts the animation and plays a sound effect.
        """
        if self.ammount > 0:
            self.ammount -= 1
            self.animating = True
            self.current_frame = 0
            self.animation_timer = pygame.time.get_ticks()
            self.sound_manager.play_sound("damage.wav", "assets/sounds", 0.1, 0.5)

    def update(self) -> None:
        """
        Updates the animation state. Advances the animation frames if animating.
        """
        if self.animating:
            # Calculate elapsed time since the last frame
            elapsed_time: float = (pygame.time.get_ticks() - self.animation_timer) / 1000
            if elapsed_time > self.animation_duration:
                self.animation_timer = pygame.time.get_ticks() 
                self.current_frame += 1  

                # Stop the animation if all frames have been played
                if self.current_frame >= len(self.scaled_frames):
                    self.animating = False

    def reset(self) -> None:
        """
        Resets the life system to its initial state with full lives and no animation.
        """
        self.ammount = 3
        self.animating = False
        self.current_frame = 0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the hearts on the screen to represent the remaining lives.
        If animating, draws the animated heart for the last lost life.

        :param screen: The pygame.Surface to draw on.
        """
        # Draw static hearts for the remaining lives
        for i in range(self.ammount):
            screen.blit(self.heart_image, (10 + i * 50, 10))

        # Draw the animated heart if animating and lives have been lost
        if self.animating and self.ammount < 3:
            screen.blit(self.scaled_frames[self.current_frame], (10 + self.ammount * 50, 10))

