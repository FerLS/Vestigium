import pygame
from typing import Callable, Optional

class FadeTransition:
    def __init__(self, 
                 screen: pygame.Surface, 
                 duration: float = 1.0, 
                 on_complete: Optional[Callable] = None):
        self.screen: pygame.Surface = screen
        self.duration: float = duration
        self.on_complete: Optional[Callable] = on_complete
        self.completed: bool = False
        self.active: bool = False
        self.timer: float = 0
        self.overlay: pygame.Surface = pygame.Surface(screen.get_size()).convert()
        self.overlay.fill((0, 0, 0))
        self.alpha: int = 0

    def start(self) -> None:
        """
        Starts the fade transition if it's not already active.
        """
        if not self.active:
            self.active = True
            self.timer = 0

    def update(self, dt: float) -> None:
        """
        Updates the state of the transition. Should be implemented in subclasses.

        :param dt: Time elapsed since the last update (in seconds).
        """
        raise NotImplementedError("Implement this in FadeIn or FadeOut")

    def draw(self) -> None:
        """
        Draws the transition overlay if the transition is active.
        """
        if self.active:
            self.overlay.set_alpha(self.alpha)
            self.screen.blit(self.overlay, (0, 0))


class FadeOut(FadeTransition):
    def __init__(self, 
                 screen: pygame.Surface, 
                 duration: float = 2.5, 
                 on_complete: Optional[Callable] = None):
        super().__init__(screen, duration, on_complete)
        self.alpha: int = 0

    def update(self, dt: float) -> None:
        """
        Updates the fade-out transition by increasing the alpha.

        :param dt: Time elapsed since the last update (in seconds).
        """
        if not self.active:
            return

        self.timer += dt
        progress = min(self.timer / self.duration, 1.0)
        self.alpha = int(progress * 255)

        if progress >= 1.0:
            self.active = False
            if self.on_complete:
                self.on_complete()
            self.alpha = 0


class FadeIn(FadeTransition):
    def __init__(self, 
                 screen: pygame.Surface, 
                 duration: float = 2.5, 
                 on_complete: Optional[Callable] = None):
        super().__init__(screen, duration, on_complete)
        self.alpha: int = 255

    def update(self, dt: float) -> None:
        """
        Updates the fade-in transition by decreasing the alpha.
        
        :param dt: Time elapsed since the last update (in seconds).
        """
        if not self.active:
            return

        self.timer += dt
        progress = min(self.timer / self.duration, 1.0)
        self.alpha = int((1 - progress) * 255)

        if progress >= 1.0:
            self.active = False
            if self.on_complete:
                self.on_complete()
            self.alpha = 255
